---
type: analysis
created: 2026-09-14
updated: 2026-09-14
---

# Política de fontes: confiáveis e 2026

## Pergunta

Como garantir que o wiki só use fontes confiáveis publicadas em 2026?

## Resposta

Duas camadas (definidas em [config](../../config.json)):

1. **TIER A (default)** — publicado ou atualizado em 2026, de fonte confiável na ordem: docs oficial > GitHub da organização > benchmark vivo (MTEB/MMS) > blog técnico de vendor (PremAI, Milvus, Qdrant, Redis). Manifest do packet carrega `published_at` + `verification` (full-text / snippet / local-test).
2. **TIER B (exceção flagada)** — pré-2026 quando não existe equivalente 2026 (ex.: model card de release 2025, guia de API sem data). Sempre com nota de caveat no manifest e no extracted.md.

Vetados: blogs comunitários sem data/afiliação, agregadores de conteúdo, vídeos como única evidência de fato técnico.

**Estado atual**: 14 fontes capturadas — 13 TIER A (1 com verificação full-text: PremAI; 11 snippet; 1 local-test: sqlite-vec) e 1 TIER B flagada (Software.Land). Snippet ≠ verdade completa: pacotes com corpo não lido (Milvus 403) carregam caveat explícito.

## Fontes

- [PremAI (full-text)](/sources/premai-best-embedding-models-2026.md) · [sqlite-vec (local-test)](/sources/sqlite-vec-release.md) · [Software.Land (TIER B)](/sources/llamacpp-embeddings-api.md)
- Ver também: [skill stack de pesquisa (skill-scout)](/analyses/research-skill-stack.md) — como as fontes foram levantadas.
