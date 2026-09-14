---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# Isolamento de workload em Kubernetes

Rodar o container de embedding no VPS isolado por namespace/rede/runtime.

## Definição

k3s leve no VPS; namespace dedicado (`rag`); NetworkPolicy default-deny (só API do gateway → Qdrant/TEI); resource requests/limits; Secrets p/ API keys (Salad, HF); sem privileged/hostPID; RuntimeClass gVisor/Kata opcional p/ sandbox forte; TLS via cert-manager + ingress (Traefik do k3s).

## Como funciona / Como aplicar

Embedding é stateless → Deployment + HPA/KEDA; Qdrant com PVC. Pods GPU ficam no Salad via [virtual-kubelet](/entities/virtual-kubelet-saladcloud.md) (node virtual) ou fora do cluster (padrão B).

## Exemplos

- NetworkPolicy + gVisor = defesa em profundidade barata

## Relacionados

- [Serverless GPU endpoint](/concepts/serverless-gpu-endpoint.md)
- [Fonte: VK](/sources/virtual-kubelet-saladcloud-repo.md)
- [Fonte: TEI](/sources/text-embeddings-inference-repo.md)
