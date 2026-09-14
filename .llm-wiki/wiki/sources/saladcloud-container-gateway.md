---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-005/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# SaladCloud — Container Groups & Container Gateway

> _Original: [https://docs.salad.com/container-engine/explanation/container-groups/container-groups](https://docs.salad.com/container-engine/explanation/container-groups/container-groups) · Publicado: docs vivas · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-005]]_

## Resumo

Container Group = imagem + requisitos de hardware + réplicas. Container Gateway expõe o grupo publicamente: porta custom, API-key auth opcional por request, URL estática load-balanced (IPv4/IPv6). Storage efêmero → workloads stateless.

## Key Takeaways

- Gateway resolve o problema clássico do Salad (sem inbound): URL pública + auth embutida
- Embedding server é stateless → fit perfeito p/ storage efêmero
- Secure GPU Clusters (datacenter) p/ requisitos corporativos

## Entidades Mencionadas

- [SaladCloud](/entities/saladcloud.md)

## Conceitos Mencionados

- [Serverless GPU endpoint](/concepts/serverless-gpu-endpoint.md)

## Fonte

- [SRC-2026-09-14-005/extracted.md](../../raw/sources/SRC-2026-09-14-005/extracted.md)
