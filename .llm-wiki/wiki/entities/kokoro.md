---
type: entity
category: model
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-015, raw/sources/SRC-2026-09-14-018]
---

# Kokoro-82M

TTS 82M (StyleTTS-2 lineage), Apache 2.0, ONNX: **melhor qualidade local em CPU** 2026 (topo TTS Arena local), faster-than-real-time, ~4GB RAM.

- Bundle: `kokoro-v1.0.onnx` + `voices-v1.0.bin` (54 vozes, 8 idiomas).
- **pt-BR nativo**: `pf_dora` (F), `pm_alex` (M), `pm_santa` (M).
- Serving: kokoro-onnx (pip) + wrapper FastAPI `/v1/audio/speech` (padrão OpenAI).
- ⚠️ Termux: depende de onnxruntime (sem wheel android) → phone usa [Piper](/entities/piper.md) ou TTS remoto.

Links: [fonte ranking](/sources/tts-2026-rankings.md) · [fonte pt-BR](/sources/kokoro-ptbr-voices.md) · [loop de voz](/concepts/voice-loop-latency.md)
