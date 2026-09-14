#!/usr/bin/env bash
# verify_vps.sh — smoke test do stack de embedding + voz num VPS Linux (ou Pop!_OS).
# Uso: bash verify_vps.sh [--full]   (--full inclui Speaches/Kokoro/voz)
# Env overrides: EMBED_PORT TTS_STT MODEL_ID QDRANT_PORT SPEACHES_PORT
# Sai com código !=0 se qualquer etapa essencial falhar. Idempotente (containers com nomes fixos, --rm).
set -uo pipefail

EMBED_PORT="${EMBED_PORT:-8080}"; QDRANT_PORT="${QDRANT_PORT:-6333}"
SPEACHES_PORT="${SPEACHES_PORT:-9000}"; TTS_PORT="${TTS_PORT:-5000}"
MODEL_ID="${MODEL_ID:-Qwen/Qwen3-Embedding-0.6B}"
FULL="${1:-}"; PASS=0; FAIL=0

ok()   { echo "  ✅ $1"; PASS=$((PASS+1)); }
bad()  { echo "  ❌ $1"; FAIL=$((FAIL+1)); }
hdr()  { echo; echo "== $1 =="; }

need() { command -v "$1" >/dev/null 2>&1 || { echo "Falta o binário '$1' — instale antes."; exit 2; }; }

hdr "0. Pré-requisitos"
for b in docker curl jq; do need "$b"; done && ok "docker/curl/jq presentes"
docker info >/dev/null 2>&1 && ok "docker daemon ativo" || { bad "docker daemon inativo"; exit 1; }

hdr "1. Endpoint de embedding (TEI cpu)"
if ! curl -sf "http://127.0.0.1:${EMBED_PORT}/health" >/dev/null 2>&1; then
  echo "  subindo TEI cpu-2.0 (${MODEL_ID})…"
  docker run -d --rm --name tei-verify -p "${EMBED_PORT}:80" \
    ghcr.io/huggingface/text-embeddings-inference:cpu-2.0 --model-id "${MODEL_ID}" \
    >/dev/null 2>&1
  for i in $(seq 1 60); do curl -sf "http://127.0.0.1:${EMBED_PORT}/health" >/dev/null 2>&1 && break; sleep 2; done
fi
curl -sf "http://127.0.0.1:${EMBED_PORT}/health" >/dev/null 2>&1 && ok "TEI /health" || bad "TEI não subiu (checar 'docker logs tei-verify')"

DIMS=$(curl -s "http://127.0.0.1:${EMBED_PORT}/v1/embeddings" -H 'Content-Type: application/json' \
  -d '{"model":"verify","input":"verificação de embedding"}' \
  | jq -r '.data[0].embedding | length' 2>/dev/null)
[ "${DIMS:-0}" -gt 0 ] 2>/dev/null && ok "/v1/embeddings respondeu (dims=${DIMS})" || bad "/v1/embeddings sem resposta válida"

hdr "2. Qdrant (vector store + híbrido)"
if ! curl -sf "http://127.0.0.1:${QDRANT_PORT}/readyz" >/dev/null 2>&1; then
  docker run -d --rm --name qdrant-verify -p "${QDRANT_PORT}:6333" -v "$PWD/.verify-qdrant:/qdrant/storage" \
    qdrant/qdrant >/dev/null 2>&1
  for i in $(seq 1 30); do curl -sf "http://127.0.0.1:${QDRANT_PORT}/readyz" >/dev/null 2>&1 && break; sleep 1; done
fi
curl -sf "http://127.0.0.1:${QDRANT_PORT}/readyz" >/dev/null 2>&1 && ok "Qdrant /readyz" || bad "Qdrant não subiu"

if [ "${DIMS:-0}" -gt 0 ] 2>/dev/null; then
  curl -s -X PUT "http://127.0.0.1:${QDRANT_PORT}/collections/verify" -H 'Content-Type: application/json' \
    -d "{\"vectors\":{\"size\":${DIMS},\"distance\":\"Cosine\"}}" >/dev/null
  # upsert determinístico (id=1) + busca
  VEC=$(curl -s "http://127.0.0.1:${EMBED_PORT}/v1/embeddings" -H 'Content-Type: application/json' \
    -d '{"model":"verify","input":"documento de teste do verify_vps"}' | jq -c '.data[0].embedding')
  curl -s -X PUT "http://127.0.0.1:${QDRANT_PORT}/collections/verify/points" -H 'Content-Type: application/json' \
    -d "{\"points\":[{\"id\":1,\"vector\":${VEC},\"payload\":{\"path\":\"teste.md\"}}]}" >/dev/null
  HITS=$(curl -s "http://127.0.0.1:${QDRANT_PORT}/collections/verify/points/search" -H 'Content-Type: application/json' \
    -d "{\"vector\":${VEC},\"limit\":1,\"with_payload\":true}" | jq -r '.result[0].payload.path' 2>/dev/null)
  [ "${HITS:-}" = "teste.md" ] && ok "round-trip embed→upsert→search (payload=${HITS})" || bad "round-trip Qdrant falhou"
fi

hdr "3. Latência do endpoint (5 chamadas)"
TIMES=(); for i in 1 2 3 4 5; do
  T=$(curl -s -o /dev/null -w '%{time_total}' "http://127.0.0.1:${EMBED_PORT}/v1/embeddings" \
    -H 'Content-Type: application/json' -d '{"model":"verify","input":"latência"}')
  TIMES+=("$T")
done
echo "  tempos(s): ${TIMES[*]}"

if [ "${FULL}" = "--full" ]; then
  hdr "4. STT — Speaches (faster-whisper, OpenAI-compat)"
  if ! curl -sf "http://127.0.0.1:${SPEACHES_PORT}/health" >/dev/null 2>&1; then
    docker run -d --rm --name speaches-verify -p "${SPEACHES_PORT}:9000" \
      -e ASR_MODEL=base -e ASR_ENGINE=faster_whisper ghcr.io/speaches-ai/speaches:latest >/dev/null 2>&1
    for i in $(seq 1 90); do curl -sf "http://127.0.0.1:${SPEACHES_PORT}/health" >/dev/null 2>&1 && break; sleep 2; done
  fi
  # gera 1s de silêncio wav p/ testar o contrato (resultado textual de silêncio pode ser vazio — valida HTTP 200)
  python3 - <<'PY' 2>/dev/null || printf 'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x00\x02\x00\x10\x00data\x00$\x00\x00' > /tmp/silence.wav
import struct, wave
w = wave.open("/tmp/silence.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
w.writeframes(b"\x00\x00" * 16000); w.close()
PY
  CODE=$(curl -s -o /tmp/stt.json -w '%{http_code}' "http://127.0.0.1:${SPEACHES_PORT}/v1/audio/transcriptions" \
    -F file=@/tmp/silence.wav -F model=base -F language=pt)
  [ "$CODE" = "200" ] && ok "/v1/audio/transcriptions HTTP 200 ($(cat /tmp/stt.json | jq -c . 2>/dev/null | head -c 80))" \
    || bad "STT HTTP=${CODE} (checar 'docker logs speaches-verify')"

  hdr "5. TTS — Kokoro (pt-BR pf_dora)"
  pip show kokoro-onnx >/dev/null 2>&1 || pip install -q kokoro-onnx soundfile 2>/dev/null
  python3 - <<'PY' && ok "Kokoro sintetizou WAV pt-BR (pf_dora)" || bad "Kokoro falhou (onnxruntime/modelo ausentes?)"
import urllib.request, os
for url, dst in [
    ("https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/kokoro-v1_0.onnx", "kokoro-v1_0.onnx"),
    ("https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/voices-v1_0.bin", "voices-v1_0.bin")]:
    if not os.path.exists(dst):
        urllib.request.urlretrieve(url, dst)
from kokoro_onnx import Kokoro
k = Kokoro("kokoro-v1_0.onnx", "voices-v1_0.bin")
audio, sr = k.create("Verificação de voz em português do Brasil.", voice="pf_dora", speed=1.0, lang="pt-br")
import soundfile as sf; sf.write("/tmp/verify_tts.wav", audio, sr)
print("wav ok", sr)
PY
  [ -f /tmp/verify_tts.wav ] && echo "  → ouça: /tmp/verify_tts.wav"
fi

hdr "Limpeza"
docker rm -f tei-verify qdrant-verify speaches-verify >/dev/null 2>&1 || true
rm -rf .verify-qdrant /tmp/silence.wav /tmp/stt.json

echo; echo "RESULTADO: ${PASS} passaram, ${FAIL} falharam"
[ "$FAIL" -eq 0 ] && echo "✅ VPS pronto para servir embedding${FULL:+ e voz}" || exit 1
