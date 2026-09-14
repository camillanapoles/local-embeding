---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-016]
---

# Speaches (ex-faster-whisper-server)

Servidor STT **OpenAI-compat `/v1/audio/transcriptions`** sobre faster-whisper (CTranslate2): streaming, live transcription, docker 1 comando, CPU/CUDA/Metal/Vulkan.

- `docker run -p 9000:9000 -e ASR_MODEL=small ghcr.io/speaches-ai/speaches:latest`
- 2-4× mais rápido que whisper de referência (int8/fp16).

Papel: STT do **Pop!_OS/VPS** (e large-v3 em GPU). Links: [fonte faster-whisper](/sources/faster-whisper-speaches.md) · [whisper.cpp](/entities/whisper-cpp.md) · [loop de voz](/concepts/voice-loop-latency.md)
