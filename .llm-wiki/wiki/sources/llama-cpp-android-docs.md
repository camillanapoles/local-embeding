---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-002/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# llama.cpp docs — Android/Termux

> _Original: [https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md) · Publicado: living doc 2026 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-002]]_

## Resumo

Documento oficial do llama.cpp para Android: Termux suportado sem root; build nativo com clang/cmake do Termux (NDK só para APKs). llama-server expõe API OpenAI-compat incluindo /v1/embeddings com --embedding.

## Key Takeaways

- Build Termux: `pkg install git clang cmake ninja python` → `cmake -B build && cmake --build build -j`
- `llama-server --embedding` = endpoint local no telefone
- Tutoriais 2026 confirmam ssh (porta 8022) + tmux como daemon

## Entidades Mencionadas

- [llama.cpp](/entities/llama-cpp.md)

## Conceitos Mencionados

- [Endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)

## Fonte

- [SRC-2026-09-14-002/extracted.md](../../raw/sources/SRC-2026-09-14-002/extracted.md)
