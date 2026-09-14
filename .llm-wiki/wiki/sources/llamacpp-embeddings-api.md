---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-003/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: B
---

# Working with llama.cpp Embeddings — Software.Land

> _Original: [https://software.land/working-with-llama-cpp-embeddings](https://software.land/working-with-llama-cpp-embeddings) · Publicado: não confirmada (API vigente) · Verificação: snippet-tierB · Packet: [[sources/SRC-2026-09-14-003]]_

## Resumo

Detalha as duas rotas de embedding do llama-server: nativa /embeddings (todos pooling modes, vetores por token) e OpenAI-compat /v1/embeddings (um vetor pooled por input; aceita dimensions/encoding_format).

## Key Takeaways

- Mesmos nomes de campo OpenAI → swap de endpoint local↔remoto sem mudar cliente
- Rota nativa dá controle fino (pooling none p/ late chunking por token)
- Ex.: `llama-server --model Qwen3-Embedding-4B-Q4_K_M.gguf --port 8080 --embedding`

## Entidades Mencionadas

- [llama.cpp](/entities/llama-cpp.md)

## Conceitos Mencionados

- [Endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)

## Fonte

- [SRC-2026-09-14-003/extracted.md](../../raw/sources/SRC-2026-09-14-003/extracted.md)
