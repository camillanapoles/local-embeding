---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-016/extracted.md
ingested: 2026-09-14
topics: [voice-stack, embedding-models-2026]
tier: A
---

# faster-whisper + Speaches + whisper.cpp v1.8.x

> _Original: [https://github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) · Publicado: repo ativo 2026 (whisper.cpp v1.8.6 jun/2026) · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-16]]_

## Resumo

STT 2026: Speaches serve faster-whisper em API OpenAI-compat (/v1/audio/transcriptions) com streaming; whisper.cpp mantém foco em VAD streaming/server e compila nativo em Termux.

## Key Takeaways

- Speaches: docker 1 comando, CPU/CUDA/Metal/Vulkan
- faster-whisper 2-4× o whisper de referência (int8/fp16)
- whisper.cpp: mesmo toolchain do llama.cpp no Android

## Entidades Mencionadas

- [Speaches](/entities/speaches.md)
- [whisper.cpp](/entities/whisper-cpp.md)

## Conceitos Mencionados

- [Loop de voz](/concepts/voice-loop-latency.md)

## Fonte

- [SRC-2026-09-14-016/extracted.md](../../raw/sources/SRC-2026-09-14-016/extracted.md)
