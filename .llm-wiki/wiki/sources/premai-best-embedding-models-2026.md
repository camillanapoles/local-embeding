---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-001/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# Best Embedding Models for RAG (2026) — PremAI

> _Original: [https://www.premai.io/blog/best-embedding-models-for-rag-2026-ranked-by-mteb-score-cost-and-self-hosting/](https://www.premai.io/blog/best-embedding-models-for-rag-2026-ranked-by-mteb-score-cost-and-self-hosting/) · Publicado: 2026-03-17 (upd. 2026-09-04) · Verificação: full-text · Packet: [[sources/SRC-2026-09-14-001]]_

## Resumo

Ranking 2026 de 10 modelos por MTEB (com foco em NDCG@10 de retrieval), custo/1M tokens, contexto, dimensões e licença. Qwen3-Embedding-8B lidera o open-source (Apache 2.0, 32K ctx, MRL); Gemini embedding-001 lidera APIs (68.32, ctx 2.048); BGE-M3 é o workhorse híbrido MIT.

## Key Takeaways

- Qwen3-Embedding: 70.58 multilingual, #1 open-source, instruction-aware (+1-5% com prefixo de tarefa)
- MRL permite truncar dimensões (3072→1024 = 3x menos storage, ~2% perda)
- BGE-M3: dense+sparse+multi-vector num modelo só (MIT)
- NV-Embed-v2 é CC-BY-NC → vetado p/ uso comercial
- Sempre rodar eval no próprio corpus

## Entidades Mencionadas

- [Qwen3-Embedding (família)](/entities/qwen3-embedding-family.md)
- [BGE-M3 → ver conceito híbrido](/concepts/hybrid-search-rerank.md)

## Conceitos Mencionados

- [MTEB benchmark](/concepts/mteb-benchmark.md)
- [Matryoshka/quantização](/concepts/matryoshka-quantization.md)

## Fonte

- [SRC-2026-09-14-001/extracted.md](../../raw/sources/SRC-2026-09-14-001/extracted.md)
