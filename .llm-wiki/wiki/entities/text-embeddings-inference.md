---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# TEI (text-embeddings-inference)

Servidor Rust da Hugging Face p/ embeddings/rerank em produção — o padrão p/ GPU.

## O que é

REST OpenAI-compat: `/v1/embeddings`, `/v1/rerank`, `/v1/predict`. Imagens Docker por compute capability: `cpu-2.0`, `cpu-arm64-2.0`, `2.0` (A100), `86-2.0` (A10/A40), `89-2.0` (RTX 40xx), `hopper-2.0` (H100), `rocm-2.0`. Flags de batching: `--max-batch-tokens 65536 --max-concurrent-requests 512`.

## Papel neste projeto

Server de embedding no **Salad GPU** (imagen 89-2.0 em RTX 40xx) e alternativa Docker no **Pop!_OS** (`cpu-2.0`).

## Links

- [Fonte: repo TEI](/sources/text-embeddings-inference-repo.md)
- [Conceito: serverless GPU endpoint](/concepts/serverless-gpu-endpoint.md)
- [Conceito: isolamento K8s](/concepts/k8s-workload-isolation.md)
