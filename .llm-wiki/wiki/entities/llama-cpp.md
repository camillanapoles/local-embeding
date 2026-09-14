---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# llama.cpp (llama-server)

Runtime C/C++ de inferência GGUF — o único servidor de embedding que roda nativo no Termux.

## O que é

Projeto ggml-org. `llama-server` sobe API HTTP com rotas `/v1/embeddings` (OpenAI-compat) e `/embeddings` (nativa, pooling arbitrário), flags `--embedding` e `--rerank`. Build nativo em Termux com clang/cmake (sem NDK, sem root); em x86 compila ou usa release. Consome qualquer GGUF: Qwen3-Embedding 0.6B/4B/8B, BGE-M3, rerankers.

## Papel neste projeto

Servidor de embedding+rerank no **Termux** (0.6B) e no **Pop!_OS** (4B); mesma stack em AMD RX no Salad via Vulkan.

## Links

- [Fonte: docs android](/sources/llama-cpp-android-docs.md)
- [Fonte: API embeddings](/sources/llamacpp-embeddings-api.md)
- [Fonte: reranker](/sources/qwen3-reranker-gguf-llamacpp.md)
- [Conceito: endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)
