---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# virtual-kubelet-saladcloud

Virtual Kubelet da Salad: pods K8s executam como container groups Salad.

## O que é

Provider oficial SaladTechnologies. O cluster enxerga um node virtual; Deployment/Service/KEDA funcionam normalmente e o VK traduz réplicas em container groups Salad.

## Papel neste projeto

Padrão A do caso **cloud**: k3s no VPS + VK → pods de embedding agendam em GPU Salad com o tooling K8s padrão.

## Links

- [Fonte: repo VK](/sources/virtual-kubelet-saladcloud-repo.md)
- [Conceito: isolamento K8s](/concepts/k8s-workload-isolation.md)
- [Conceito: serverless GPU endpoint](/concepts/serverless-gpu-endpoint.md)
