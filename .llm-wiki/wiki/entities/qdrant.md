---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# Qdrant

Vector database Rust com híbrido server-side e quantização.

## O que é

Query API (1.10+) junta dense + sparse (BM25/SPLADE) + filtros numa consulta; quantização scalar/binary/asymmetric (binary: 32x menos RAM, 40x mais rápido, 2-5% perda de recall); HNSW+ACORN; mmap+WAL.

## Papel neste projeto

Vector store no **Pop!_OS** (Docker) e no **VPS/k3s** (Deployment+PVC). No Termux, só se via proot — lá preferimos [sqlite-vec](/entities/sqlite-vec.md).

## Links

- [Fonte: docs híbrido/quantização](/sources/qdrant-hybrid-quantization-docs.md)
- [Conceito: híbrido+rerank](/concepts/hybrid-search-rerank.md)
- [Conceito: matryoshka/quantização](/concepts/matryoshka-quantization.md)
