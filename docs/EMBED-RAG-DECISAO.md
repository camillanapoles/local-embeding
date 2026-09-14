# Local vs Cloud — Decisão de Endpoint de Embedding para RAG
### Qual usar para: "LLM embedding para RAG com endpoint que apps consomem"

> Compara [EMBED-RAG-LOCAL.md](EMBED-RAG-LOCAL.md) (Termux + Pop!_OS) com [EMBED-RAG-CLOUD.md](EMBED-RAG-CLOUD.md) (VPS k3s + SaladCloud GPU). Evidências 2026 no vault `.llm-wiki/`. Estimativas marcadas [inferência].

---

## 1. Comparação direta

| Critério | **LOCAL** (Pop!_OS CPU + Termux) | **CLOUD** (VPS k3s + Salad GPU) |
|---|---|---|
| Custo inicial | **$0** | VPS ~$5-12/mês + GPU $0.01-0.07/hr |
| Throughput de ingestão | baixo-médio (ONNX CPU: ~5-40 docs/s desktop; 1-8 no telefone [inf.]) | **alto** (TEI + RTX 40xx, batch 64-256) |
| Latência de query | **~10-50 ms** (sem rede) | 100-500 ms + WAN (dep. de réplica/região) |
| Qualidade máxima | 0.6B/4B em CPU (Q4/Q8, ONNX int8) | **4B/8B fp16 na GPU; upgrade p/ KaLM-12B SOTA** |
| Privacidade | **dados nunca saem do device** | tráfego em nós comunitários (ou Secure Clusters) |
| Disponibilidade | ligado quando você liga | 24/7, mas best-effort (churn) → réplicas |
| Multi-app | LAN/ADB (limitado) | **URL pública + API-key + LB** |
| Ops | baixo (1 binário + 1 arquivo .db) | médio (k3s, TLS, secrets, monitoramento) |
| Índice | sqlite-vec (portátil, 1 arquivo) / Qdrant | Qdrant + PVC + backup |
| Escala de corpus | ≤ ~300-500k chunks (brute-force) | milhões (HNSW + quantização) |

**Leitura**: cloud ganha em *volume, disponibilidade e qualidade de pico*; local ganha em *custo fixo, latência, privacidade e simplicidade*. Nenhum ganha em tudo — por isso a decisão abaixo é híbrida por padrão.

### 1.1 Padrão C — endpoint na VPS (CPU), consumo local [novo]

Há uma terceira topologia, entre o local puro e o Salad: **a VPS serve o embedding e os dispositivos apenas consomem** (`EMBED_BASE_URL=https://vps…/v1`). Nada de k3s/Salad obrigatório — TEI `cpu-2.0` ou Infinity via Docker/compose, WireGuard para acesso privado.

| Critério | Padrão C (VPS CPU) |
|---|---|
| Custo | flat ~$5-12/mês (já cobre Qdrant + BFF + voz) |
| Latência query | ~30-80ms sobre WireGuard/LAN [inf.] |
| Throughput | médio (CPU do VPS; 2-4 vCPU serve bem uso pessoal multi-app) |
| Privacidade | **seu** servidor (melhor que nó comunitário Salad; pior que local) |
| Disponibilidade | 24/7, sem churn de terceiros |
| Papel do phone/desktop | clientes finos — capturam query e mostram resposta |

**Veredito**: para uso pessoal multi-dispositivo, o Padrão C é de fato o melhor ponto de partida de *serving* (como você suspeitou) — o local continua valendo para dev/privacidade/offline, e o Salad entra só quando volume de ingestão ou qualidade de pico (8B/12B fp16) exigirem. Evolução: **C ➞ B** é só trocar o backend do BFF.

### 1.2 Knowledge base: na VPS ou local? (resposta direta)

**Se o embedding model está na VPS ➞ o KB (Qdrant/índice) fica na VPS também.** Razões:

1. **Query-time depende do endpoint**: toda pergunta precisa virar embedding *na hora* → se o modelo está na VPS, o índice local só seria alcançável depois de uma ida-e-volta à rede. KB local + embedding remoto = o pior dos dois mundos (rede na query E sincronização de índice manual).
2. **Round-trip colapsa**: embedding + busca + rerank no mesmo host (LAN interna do VPS) ≈ 1 hop de rede em vez de 3; BFF devolve a resposta pronta.
3. **Fonte única de verdade**: múltiplas apps veem o mesmo índice; backup/snapshot é um lugar; sem conflito de versão de índice.
4. **Privacidade já foi decidida antes**: embeddar na VPS = o texto já passou pelo VPS — manter só os vetores no bolso não recupera privacidade. Se o conteúdo é sensível, a decisão certa é *tudo* local (doc LOCAL), não metade.

KB local só faz sentido com **endpoint também local** (modo offline-first do doc LOCAL — phone com índice no bolso via sqlite-vec). Não existe bom meio-termo.


## 2. Matriz de decisão por cenário

| Seu cenário | Use | Por quê |
|---|---|---|
| Dev/experimentos, corpus próprio pequeno (<50k chunks) | **Local (Pop!_OS)** | custo 0, latência mínima, sem ops |
| Privacidade total (código/contratos sensíveis) | **Local** (Termux = bolso) | nada sai do hardware |
| Uso pessoal multi-dispositivo 24/7, sem ops de GPU | **Padrão C (VPS CPU)** | flat barato, 1 hop, seu hardware |
| Ingestão contínua / re-index frequente (>10-50M tok/mês [inf.]) | **Cloud GPU** | batch GPU esmaga CPU em custo/token |
| Corpus gigante (>500k chunks) com queries rápidas | **Cloud** (Qdrant+quantização) | sqlite-vec é brute-force |
| Sem internet / campo | **Termux** | nó edge offline |
| Pico de qualidade (SOTA MMTEB) | **Cloud** (KaLM-12B) | 12B não roda em CPU |

## 3. Recomendação para o SEU goal (endpoint p/ apps RAG)

**Fase 1 — hoje (local-first):**
1. Pop!_OS: `infinity_emb v2 --model-id Qwen/Qwen3-Embedding-0.6B --engine optimum` (ou TEI `cpu-2.0` Docker) → `EMBED_BASE_URL=http://192.168.x.x:7997/v1`.
2. Qdrant com quantização + alias `chunks-alias`; `ingest.py` idempotente por sha256 nos diretórios recursivos.
3. Termux: llama.cpp `--embedding` (0.6B GGUF) + sqlite-vec ✅ — nó offline de testes/desenvolvimento mobile.
4. Apps já em OpenAI SDK com `EMBED_BASE_URL`/`EMBED_DIMS=1024` configuráveis.

**Fase 2 — quando estressar o local (produção/volume):**
1. Container group Salad com TEI `89-2.0` + Qwen3-Embedding-4B baked, Container Gateway com API-key.
2. VPS k3s: BFF (auth próprio) + Qdrant + workers; apps apontam o BFF, nunca a URL Salad.
3. Failover `cloud → local` por health check no BFF (contrato idêntico).
4. Se a frota K8s crescer: Padrão A (virtual-kubelet + KEDA).

**Ordem de evolução de modelo** (sem quebrar o índice): 0.6B → 4B → 8B são a **mesma família Qwen3-Embedding** — mas atenção: embeddings de tamanhos diferentes **não são comparáveis entre si**; cada upgrade = nova collection versionada + re-embed + gold set (seção 7.1 do doc local). O que se mantém é o *contrato* (`/v1/embeddings`, dims=1024 via MRL), não os vetores.

## 4. Break-even financeiro [inferência — calibrar]

| Volume mensal | Local (CPU) | Salad GPU | API paga (voyage $0.06/1M) |
|---|---|---|---|
| 1M tokens | ~horas de CPU (grátis, lento) | ~$0.5-1 GPU + $5-12 VPS | **~$0.06** ✓ |
| 10M tokens | dias de CPU (inviável p/ SLA) | ~$3-8 GPU + VPS | ~$0.60 ✓ ainda |
| 100M tokens | inviável | **~$20-50 total** ✓ | ~$6.000 ✗ |

Regra: **abaixo de ~10M tokens/mês, API paga é mais barata que self-host cloud; acima, Salad vira 10-100x mais barato**. O custo do VPS é amortizado por tudo mais que ele hospeda (Qdrant, BFF, apps).

## 5. Riscos que puxam a decisão

- Dados sensíveis → **local, sem discussão** (nó comunitário = máquina de terceiro).
- Latência p95 <100ms é requisito → local (rede mata).
- Re-index total frequente (corpus muda muito) → GPU cloud obrigatória na prática.

## 6. Resumo em uma frase

> **Comece local no Pop!_OS com Qwen3-Embedding + Infinity/Qdrant (custo $0, contrato Openai-compat), mantenha o Termux como nó edge verificado (llama.cpp + sqlite-vec), e promova o embedding para SaladCloud GPU (TEI padrão B) quando ingestão/disponibilidade/multi-app exigirem — apps nunca percebem a troca porque `dimensions=1024` e `/v1/embeddings` foram fixados no dia 1.**

---
Espelho no wiki: `.llm-wiki/wiki/syntheses/local-vs-cloud-decision.md` · Fontes: ver docs gêmeos (todas 2026).
