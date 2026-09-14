---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-006/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# SaladTechnologies/virtual-kubelet-saladcloud

> _Original: [https://github.com/SaladTechnologies/virtual-kubelet-saladcloud](https://github.com/SaladTechnologies/virtual-kubelet-saladcloud) · Publicado: repo ativo · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-006]]_

## Resumo

Virtual Kubelet oficial da Salad: pods Kubernetes rodam como SaladCloud container groups; KEDA e kubectl funcionam normalmente, o VK traduz réplicas.

## Key Takeaways

- K8s do VPS agenda pods em GPUs Salad sem mudar tooling
- KEDA pode escalar container groups por métricas externas (ex.: profundidade de fila)

## Entidades Mencionadas

- [virtual-kubelet-saladcloud](/entities/virtual-kubelet-saladcloud.md)
- [SaladCloud](/entities/saladcloud.md)

## Conceitos Mencionados

- [Isolamento K8s](/concepts/k8s-workload-isolation.md)
- [Serverless GPU endpoint](/concepts/serverless-gpu-endpoint.md)

## Fonte

- [SRC-2026-09-14-006/extracted.md](../../raw/sources/SRC-2026-09-14-006/extracted.md)
