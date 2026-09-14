---
type: synthesis
topic: stack cloud de embedding (VPS k3s + SaladCloud GPU)
created: 2026-09-14
updated: 2026-09-14
sources_count: 6
---

# Stack cloud de embedding para RAG (VPS k3s + SaladCloud GPU)

> _Síntese de 6 fontes. Detalhe operacional completo: [docs/EMBED-RAG-CLOUD.md](../../../docs/EMBED-RAG-CLOUD.md)_

## Pergunta

Como servir embeddings com GPU barata, isolando o container via Kubernetes num VPS, usando SaladCloud — mantendo o mesmo contrato de endpoint das apps?

## Análise

**Dois padrões, mesmo contrato**:

- **Padrão A (K8s-native)**: k3s no VPS + [virtual-kubelet-saladcloud](/entities/virtual-kubelet-saladcloud.md) → pods de embedding agendam como container groups Salad; KEDA escala por métrica externa (fila). Tooling K8s único.
- **Padrão B (serviço dedicado)**: container group Salad (TEI 89-2.0 / llama.cpp Vulkan) exposto pelo **Container Gateway** (URL estática, LB, API-key opcional); VPS roda apps+Qdrant+workers de ingestão e chama o gateway. Menos acoplamento, mais simples de operar.

**Servidor** — [TEI v2](/entities/text-embeddings-inference.md): `/v1/embeddings` + `/v1/rerank`, batching `--max-batch-tokens 65536`; imagem por compute capability (RTX 40xx = `89-2.0`). AMD RX (baratas no Salad) → llama.cpp Vulkan. Modelo: Qwen3-Embedding-4B/8B fp16; upgrade candidato: [KaLM-Gemma3-12B](/entities/kalm-embedding-gemma3.md) (SOTA MMTEB, comercial-OK).

**Isolamento** — [k8s-workload-isolation](/concepts/k8s-workload-isolation.md): namespace `rag`, NetworkPolicy default-deny, Secrets, limits, gVisor opcional, TLS cert-manager.

**Custo** — Salad a partir de $0.01/hr ([ComputePrices](/sources/computeprices-salad.md)); embedding de 1M tokens em RTX 40xx ≈ minutos de GPU ≈ fração de centavo [inferência] → abaixo das APIs ($0.06-0.15/1M) em volume.

**Riscos** — nós comunitários = best-effort (churn/cold start): réplicas + retry + healthcheck; storage efêmero → stateless obrigatório (embedding é); dados sensíveis → Secure GPU Clusters.

## Conclusões

1. Padrão B primeiro (menor superfície de erro), Padrão A quando a frota K8s já existir.
2. Salad quebra o custo de embedding em volume, mas SLO de latência p95 exige réplicas e medição — não é grátis.
3. Stateless + contrato idêntico ao local = fallback cloud→local (e vice-versa) sem mudança de código.

## Fontes

- [Salad gateway](/sources/saladcloud-container-gateway.md) · [VK repo](/sources/virtual-kubelet-saladcloud-repo.md) · [preços](/sources/computeprices-salad.md) · [TEI](/sources/text-embeddings-inference-repo.md) · [KaLM](/sources/kalm-embedding-gemma3-card.md) · [híbrido Qdrant](/sources/qdrant-hybrid-quantization-docs.md)

## Relacionados

- [Síntese local](/syntheses/local-embedding-stack.md) · [Decisão](/syntheses/local-vs-cloud-decision.md)
