---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-004/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# TEI v2 — Hugging Face text-embeddings-inference

> _Original: [https://github.com/huggingface/text-embeddings-inference](https://github.com/huggingface/text-embeddings-inference) · Publicado: repo ativo, v2 2026 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-004]]_

## Resumo

Servidor Rust de produção para embeddings/rerank com REST OpenAI-compat (/v1/embeddings, /v1/rerank, /v1/predict). Imagens Docker por hardware: cpu-2.0 (x86_64), cpu-arm64-2.0, 2.0 (A100), 86-2.0 (A10/A40), 89-2.0 (RTX 40xx), hopper-2.0 (H100), rocm-2.0 (Instinct).

## Key Takeaways

- GPU launch: `docker run --gpus all -p 8080:80 ghcr.io/huggingface/text-embeddings-inference:2.0 --model-id BAAI/bge-m3 --dtype float16 --max-batch-tokens 65536 --max-concurrent-requests 512`
- CPU: tag cpu-2.0 sem --gpus
- Batching/concorrência tuneáveis; auto-detecção de hardware
- Integracao LangChain nativa

## Entidades Mencionadas

- [TEI](/entities/text-embeddings-inference.md)

## Conceitos Mencionados

- [Isolamento K8s](/concepts/k8s-workload-isolation.md)
- [Híbrido+rerank](/concepts/hybrid-search-rerank.md)

## Fonte

- [SRC-2026-09-14-004/extracted.md](../../raw/sources/SRC-2026-09-14-004/extracted.md)
