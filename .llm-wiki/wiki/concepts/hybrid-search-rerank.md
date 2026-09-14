---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# Busca híbrida + rerank

Dense + lexical (BM25/sparse) com fusão RRF, depois cross-encoder — maior ganho de precisão por esforço.

## Definição

Dense pega semântica, BM25/sparse pega termos exatos (nomes de função, IDs). Fusão Reciprocal Rank Fusion (k=60 típico) dos top-k de cada; reranker cross-encoder (Qwen3-Reranker 0.6B/4B) reordena e devolve top 5-20. Qdrant faz fusão server-side (Query API); BGE-M3 gera dense+sparse numa passada.

## Como funciona / Como aplicar

Pipeline: retrieve dense top-50 + BM25 top-50 → RRF → rerank top-100 → top-10 final. Contextual retrieval (-67% falhas top-20) multiplica o ganho.

## Exemplos

- Local: BM25 em SQLite (FTS5) + KNN sqlite-vec + rerank llama-server --rerank
- Cloud: Qdrant Query API (prefetch dense+sparse, fusion RRF) + TEI /v1/rerank

## Relacionados

- [Chunking](/concepts/recursive-directory-chunking.md)
- [Entidades: Qdrant](/entities/qdrant.md), [llama.cpp](/entities/llama-cpp.md), [TEI](/entities/text-embeddings-inference.md)
- [Fonte: chunking 2026](/sources/rag-chunking-2026-guides.md)
