---
type: analysis
created: 2026-09-14
updated: 2026-09-14
---

# Skill stack de pesquisa (skill-scout)

## Pergunta

Quais skills pré-selecionar (via skill-scout) para cada fase deste tipo de pesquisa/implementação?

## Resposta

skill-scout (rank local > marketplace/GitHub > web; máx 10) aplicado ao catálogo local (~/.agents/skills, 200+):

| Fase | Skill | Por quê |
|---|---|---|
| Planejamento da pesquisa | `research-ops` | classifica o ask, separa fato/inferência/recomendação, exige datas |
| Busca web | `web_search` nativo + `exa-search`/`parallel-web` quando MCP/CLI disponíveis | cobertura corrente 2026 |
| Decisão/comparação | `market-research` | formato decision-memo ranqueado |
| Persistência do conhecimento | `llm-wiki` (este vault) + `knowledge-ops` | fontes + sínteses duráveis |
| Docs | `markdown-mermaid-writing` | docs com diagramas padronizados |
| Implementação local | `python-patterns`, `content-hash-cache-pattern` | pipeline de ingestão + cache por hash |
| Cloud/K8s | `kubernetes-patterns`, `docker-patterns` | manifests e imagens corretos |
| Medição | `benchmark`, `observability-and-instrumentation` | throughput/latência do endpoint |
| Segurança | `security-review` | endpoint exposto (gateway/TLS/auth) |

**Decisão skill-scout**: usar existentes (nenhum gap que exija criar skill nova) — "Use existing" em todas as linhas; não criar skill própria até o pipeline de ingestão estabilizar (aí vira `skill` page aqui no wiki via trajectories).

## Fontes

- Metodologia: skill `skill-scout` (ECC) — catálogo local inventariado na sessão de 2026-09-14
