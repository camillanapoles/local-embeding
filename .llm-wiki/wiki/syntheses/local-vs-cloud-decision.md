---
type: synthesis
topic: decisão local vs cloud
created: 2026-09-14
updated: 2026-09-14
sources_count: 10
---

# Local vs Cloud — qual usar para endpoint de embedding RAG

> _Análise cruzada de 10+ fontes. Documento de decisão: [docs/EMBED-RAG-DECISAO.md](../../../docs/EMBED-RAG-DECISAO.md)_

## Pergunta

Para o objetivo — endpoint de embedding ([OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)) que apps usam p/ RAG sobre diretórios recursivos — qual implantação: local (Termux/Pop!_OS) ou cloud (VPS k3s + Salad GPU)?

## Análise

| Critério | Local (Pop!_OS CPU) | Local (Termux) | Cloud (VPS+Salad GPU) |
|---|---|---|---|
| Custo fixo | $0 | $0 | VPS ~$5-12/mês + GPU ~$0.01-0.07/hr |
| Custo/1M tokens ingestão | alto em tempo (CPU lenta) | altíssimo (tempo) | baixo (GPU batch) [inferência] |
| Latência query (single) | ~10-50ms | ~50-300ms | 100-500ms + rede (dep. réplica) |
| Throughput ingestão | médio (ONNX) | baixo | alto (TEI batch 64-256) |
| Privacidade | dados nunca saem | dados no bolso | sai p/ nós comunitários (ou Secure Clusters) |
| Disponibilidade | sua máquina ligada | seu telefone | 24/7, best-effort churn |
| Ops | baixo | baixo | médio (k3s, secrets, TLS) |
| Índice compartilhado entre apps | LAN | ADB/LAN | URL pública auth |

Regra de bolso 2026: **ingestão grande/contínua → GPU cloud; consultas e dev → local**. O contrato idêntico permite híbrido: apps com `EMBED_BASE_URL` configurável e fallback.

## Conclusões

1. **Recomendação: híbrido com padrão-B cloud** — dev/privacidade no Pop!_OS (Infinity CPU + Qdrant), produção/volume no Salad (TEI + Qwen3-4B), Termux como nó offline/edge; mesmo modelo (Qwen3-Embedding) e `dimensions=1024` em todos.
2. Break-even: enquanto ingestão < ~10-50M tokens/mês, API barata ($0.018-0.06/1M) compete com self-host cloud — self-host compensa acima disso, com privacidade e controle de modelo (KaLM/Qwen3) como diferenciais.

**Padrão C (rev. 2)**: endpoint na **VPS com CPU** (TEI `cpu-2.0`/Infinity + WireGuard), dispositivos como clientes finos — melhor ponto de partida de *serving* p/ uso pessoal multi-dispositivo (flat $5-12/mês, 1 hop, seu hardware). Evolução C➞B (Salad GPU) troca só o backend. **KB junto do endpoint**: se o modelo está na VPS, o índice (Qdrant) fica na VPS — query-time depende do embedding na hora; KB local + embedding remoto = anti-pattern (rede na query E sync manual; o texto já passou pelo VPS ao embeddar). KB local só com endpoint local. Detalhe: [docs/EMBED-RAG-DECISAO.md §1.1-1.2](../../../docs/EMBED-RAG-DECISAO.md).
3. Nunca re-embeddar por troca de endpoint: fixar modelo+dims desde o dia 1 ([MRL](/concepts/matryoshka-quantization.md)).

## Fontes

- Ver sínteses [local](/syntheses/local-embedding-stack.md) e [cloud](/syntheses/cloud-embedding-stack.md)

## Relacionados

- [Endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md) · [Serverless GPU](/concepts/serverless-gpu-endpoint.md) · [Stack de voz](/syntheses/voice-stack.md)
