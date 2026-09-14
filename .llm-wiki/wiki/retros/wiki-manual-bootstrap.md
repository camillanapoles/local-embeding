---
type: analysis
created: 2026-09-14
updated: 2026-09-14
retro: true
---

# Retro: bootstrap de wiki llm-wiki sem a extensão pi

**Insight:** o harness omp não expõe as ferramentas `wiki_*` da extensão pi — o bootstrap manual segue o mesmo contrato (raw imutável com manifest+extracted, wiki editável, meta gerado por script) e fica compatível quando a extensão assumir. Chaves: (1) `tools/wiki_meta.py` regenera registry/backlinks/index/log a partir de `wiki/`; (2) events.jsonl só é recriado se não existir (append-only); (3) política de fontes (tiers 2026) vai no config.json, não em prosa solta.

**Aplicável a:** qualquer projeto que queira o fluxo llm-wiki fora do pi. Ver [config](../../config.json) e [política de fontes](/analyses/source-policy-2026.md).
