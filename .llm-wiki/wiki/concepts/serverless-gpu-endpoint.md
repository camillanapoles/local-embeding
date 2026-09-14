---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# Endpoint GPU serverless (Salad Gateway)

Servir embeddings de contêiner em GPUs de consumidor, com URL pública e API-key.

## Definição

Container Group Salad: imagem TEI/llama.cpp + GPU class + Container Gateway (porta, auth API-key, URL estática, LB entre réplicas). Storage efêmero OK p/ stateless. Nós comunitários = best-effort (cold start, churn) → desenhar idempotente e com retry; dados sensíveis → Secure GPU Clusters.

## Como funciona / Como aplicar

Regra: modelo carregado na imagem (volume no build) p/ cold start curto; healthcheck `/health`; réplicas × throughput; KEDA (padrão A) ou API Salad (padrão B) p/ escala.

## Exemplos

- TEI 89-2.0 em RTX 4070/A5000; llama.cpp Vulkan em RX 7800 XT

## Relacionados

- [Entidades: SaladCloud](/entities/saladcloud.md), [VK](/entities/virtual-kubelet-saladcloud.md)
- [Fonte: gateway](/sources/saladcloud-container-gateway.md)
- [Conceito: isolamento K8s](/concepts/k8s-workload-isolation.md)
