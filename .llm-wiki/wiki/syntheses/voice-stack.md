---
type: synthesis
topic: stack de voz (STT+TTS) para conversa fluida
created: 2026-09-14
updated: 2026-09-14
sources_count: 4
---

# Stack de voz 2026 — conversar fluentemente com o modelo

> _Síntese de 4 fontes. Doc operacional: [docs/VOICE-LLM.md](../../../docs/VOICE-LLM.md)_

## Pergunta

Como montar áudio➞texto e texto➞áudio de boa qualidade, nos mesmos ambientes do embedding (Termux / Pop!_OS / VPS+Salad), p/ conversar com o LLM?

## Análise

- **STT**: [whisper.cpp](/entities/whisper-cpp.md) no Termux (build nativo, `/inference`, `--language pt`); [Speaches](/entities/speaches.md) no VPS/Pop!_OS (`/v1/audio/transcriptions` OpenAI-compat, streaming). Modelo: small = equilíbrio; large-v3 = GPU/batch.
- **TTS**: [Kokoro-82M](/entities/kokoro.md) = qualidade local 2026 (Apache 2.0, CPU RTF<1, **pt-BR: pf_dora/pm_alex/pm_santa**); [Piper](/entities/piper.md) = fallback leve (faber M). Clonagem: Chatterbox/Qwen3-TTS (GPU).
- **Fluidez**: [loop de voz](/concepts/voice-loop-latency.md) — sentence-streaming + VAD + barge-in; TTFA alvo <800ms (VPS) / <2s (phone).
- **Topologia**: mesmo **Padrão C** da [decisão](/syntheses/local-vs-cloud-decision.md) — hub de voz na VPS (STT+TTS stateless e leves), phone como cliente fino; Termux offline = modo avião.

## Conclusões

1. TTS é onde a qualidade se decide: Kokoro pf_dora é o padrão pt-BR local 2026.
2. Fluidez é onde a experiência se decide: sentence-streaming > modelo maior.
3. Contrato uniforme (`STT_BASE_URL`/`TTS_BASE_URL` OpenAI-compat) mantém ambientes intercambiáveis igual ao embedding.

## Fontes

- [TTS rankings](/sources/tts-2026-rankings.md) · [faster-whisper/Speaches](/sources/faster-whisper-speaches.md) · [latência do pipeline](/sources/voice-latency-2026.md) · [Kokoro pt-BR](/sources/kokoro-ptbr-voices.md) — packets SRC-2026-09-14-015..018

## Relacionados

- [Decisão local vs cloud (Padrão C)](/syntheses/local-vs-cloud-decision.md)
