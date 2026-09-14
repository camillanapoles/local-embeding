---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-016]
---

# whisper.cpp

Port C/C++ do Whisper (ggml) — STT que roda nativo em Termux/Android com o mesmo toolchain do llama.cpp.

- v1.8.x (2026): foco em VAD streaming e estabilidade do server.
- `whisper-server -m ggml-small.bin --port 8081 --language pt` → POST `/inference` (multipart).
- Modelos: base 142MB, small ~466MB; quantização GGML disponível.

Papel: STT do **Termux** (edge offline). Links: [fonte](/sources/faster-whisper-speaches.md) · [Speaches](/entities/speaches.md) · [loop de voz](/concepts/voice-loop-latency.md) · [llama.cpp](/entities/llama-cpp.md)
