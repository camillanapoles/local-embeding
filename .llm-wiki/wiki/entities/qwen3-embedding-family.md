---
type: entity
category: model
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# Qwen3-Embedding (0.6B/4B/8B) + Qwen3-Reranker

Família open-source Apache 2.0 #1 MTEB multilingual — o modelo default do projeto.

## O que é

8B: 70.58 MTEB multilingual (jun/2025, segue top-3 em 2026), ctx 32K, MRL 32→7168 dims; 4B: 2560 dims; 0.6B: 1024 dims, GGUF Q8 ~600MB — roda em telefone. Instruction-aware (+1-5% com prefixo `Instruct:`). Reranker correspondente: 0.6B/4B/8B via `llama-server --rerank` (cuidado com GGUFs quebrados).

## Papel neste projeto

Scores oficiais (card/arXiv 2506.05176): 0.6B MTEB-R 61.82 · MMTEB-R 64.64 · MTEB-Code 75.41 (batendo o padrão text-embedding-3-large, 58.93) — ver [scores](/sources/qwen3-embedding-scores.md). 8B: 70.58 multilingual.

Modelo escolhido: 0.6B no Termux, 4B no Pop!_OS CPU, 4B/8B no Salad GPU — **mesma família = mesmas instruções e normalização; index portável via MRL truncando p/ 1024**.

## Links

- [Fonte: ranking 2026](/sources/premai-best-embedding-models-2026.md)
- [Fonte: reranker GGUF](/sources/qwen3-reranker-gguf-llamacpp.md)
- [Conceito: MTEB](/concepts/mteb-benchmark.md)
- [Conceito: endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)
