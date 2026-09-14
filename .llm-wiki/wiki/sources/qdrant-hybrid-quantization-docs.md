---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-009/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# Qdrant — Hybrid Query API + Quantization

> _Original: [https://qdrant.tech/documentation/manage-data/quantization](https://qdrant.tech/documentation/manage-data/quantization) · Publicado: docs vivas 2026 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-009]]_

## Resumo

Query API (v1.10+) combina dense+sparse+BM25+filtros server-side. Quantização scalar (uint8 SIMD), binary (32x menos RAM / 40x mais rápido, 2-5% perda), asymmetric e product. HNSW+ACORN.

## Key Takeaways

- Híbrido num único store (sem segundo sistema p/ BM25)
- Binary quantization = primeira otimização a ligar em produção
- Sparse vectors nativos casam com BGE-M3/Qwen3 sparse

## Entidades Mencionadas

- [Qdrant](/entities/qdrant.md)

## Conceitos Mencionados

- [Híbrido+rerank](/concepts/hybrid-search-rerank.md)
- [Matryoshka/quantização](/concepts/matryoshka-quantization.md)

## Fonte

- [SRC-2026-09-14-009/extracted.md](../../raw/sources/SRC-2026-09-14-009/extracted.md)
