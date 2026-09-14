---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-017/extracted.md
ingested: 2026-09-14
topics: [voice-stack, embedding-models-2026]
tier: A
---

# Pipeline de voz 2026 — latência, VAD, barge-in

> _Original: [https://arxiv.org/html/2603.05413v1](https://arxiv.org/html/2603.05413v1) · Publicado: 2026 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-17]]_

## Resumo

Medições 2026 de pipelines de voz: TTFA ~755ms medido end-to-end; ~400-520ms com WebSocket e componentes afinados; barge-in alvo <150ms.

## Key Takeaways

- Sentence-boundary streaming = maior ganho único
- VAD Silero com endpointing ~200ms
- Echo cancellation é pré-requisito do barge-in

## Entidades Mencionadas

- [whisper.cpp](/entities/whisper-cpp.md)
- [Kokoro](/entities/kokoro.md)

## Conceitos Mencionados

- [Loop de voz](/concepts/voice-loop-latency.md)

## Fonte

- [SRC-2026-09-14-017/extracted.md](../../raw/sources/SRC-2026-09-14-017/extracted.md)
