---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-011/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# Infinity — michaelfeil/infinity

> _Original: [https://github.com/michaelfeil/infinity](https://github.com/michaelfeil/infinity) · Publicado: repo ativo · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-011]]_

## Resumo

Servidor FastAPI OpenAI-compat p/ embeddings, rerankers, CLIP/CLAP/ColPali. Backends PyTorch/optimum(ONNX/TensorRT)/CTranslate2; CPU rápido com --engine optimum. Docker michaelf34/infinity:0.0.70-cpu ou pip.

## Key Takeaways

- Melhor opção CPU x86 sem GPU p/ throughput (ONNX int8)
- embeddings + rerank no mesmo server
- pip install infinity-emb[all] — funciona em Pop!_OS sem Docker

## Entidades Mencionadas

- [Infinity](/entities/infinity-emb.md)

## Conceitos Mencionados

- [Endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)
- [Híbrido+rerank](/concepts/hybrid-search-rerank.md)

## Fonte

- [SRC-2026-09-14-011/extracted.md](../../raw/sources/SRC-2026-09-14-011/extracted.md)
