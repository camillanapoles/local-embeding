---
type: entity
category: platform
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# SaladCloud

Nuvem de GPUs distribuídas (consumidor/datacenter) a partir de $0.01/hr.

## O que é

Container Groups (imagem + hardware + réplicas) com **Container Gateway**: URL pública estática load-balanced, porta custom, **API-key auth opcional**, IPv4/IPv6. Storage efêmero → stateless. 37+ GPUs (RTX 2060→A5000, RX 7800 XT...); Secure GPU Clusters p/ enterprise.

## Papel neste projeto

GPU do caso **cloud**: TEI 89-2.0 em RTX 40xx serve Qwen3-Embedding-4B/8B em batch; AMD RX → llama.cpp Vulkan. Stateless = fit perfeito.

## Links

- [Fonte: gateway](/sources/saladcloud-container-gateway.md)
- [Fonte: preços](/sources/computeprices-salad.md)
- [Conceito: serverless GPU endpoint](/concepts/serverless-gpu-endpoint.md)
