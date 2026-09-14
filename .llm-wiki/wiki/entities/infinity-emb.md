---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# Infinity (infinity-emb)

Servidor FastAPI de embeddings/rerank com backend ONNX — melhor throughput em CPU x86.

## O que é

Michael Feil. `/v1/embeddings` OpenAI-compat; backends PyTorch/**optimum (ONNX)**/CTranslate2; `--engine optimum` p/ CPU; rerank e CLIP/ColPali no mesmo server. `pip install infinity-emb[all]` (sem Docker) ou `michaelf34/infinity:0.0.70-cpu`.

## Papel neste projeto

Opção A p/ **Pop!_OS** sem GPU (ONNX int8); serve embeddings + reranker juntos.

## Links

- [Fonte: repo Infinity](/sources/infinity-emb-repo.md)
- [Conceito: endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)
- [Conceito: híbrido+rerank](/concepts/hybrid-search-rerank.md)
