---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-021/extracted.md
ingested: 2026-09-14
topics: [android-stack]
tier: A
---

# On-device LLM Android 2026 — MediaPipe vs llama.cpp vs llama.rn

> _Original: [blog](https://meetprajapati.com/blogs/running-on-device-ai-models-android-mediapipe-llamacpp-executorch) · [SmolChat](https://github.com/shubham0204/SmolChat-Android) · [MediaPipe](https://developers.google.com/edge/mediapipe/solutions/genai/llm_inference/android) · [llama.rn](https://www.npmjs.com/package/llama.rn) · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-021]]_

## Resumo

Três caminhos p/ LLM no APK: llama.cpp+JNI (SmolChat), MediaPipe LLM Inference (Kotlin-first), llama.rn (RN). RAG local típico: embeddings on-device + SQLite/FAISS/Qdrant mobile.

## Key Takeaways

- Escolha do projeto: APK **cliente do endpoint** (contract-first) — sem NDK no CI; JNI embutido é evolução
- llama.cpp permanece o runtime mais flexível (GGUF, mesma base do Termux verificado)

## Entidades Mencionadas

- [llama.cpp](/entities/llama-cpp.md)

## Conceitos Mencionados

- [Endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)

## Fonte

- [SRC-2026-09-14-021/extracted.md](../../raw/sources/SRC-2026-09-14-021/extracted.md)
