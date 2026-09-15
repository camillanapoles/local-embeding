---
name: warn-push-sem-gates
enabled: true
event: bash
action: warn
pattern: git\s+push
---

Antes de pushar: rode `bash scripts/gates.sh` (unit + hardcode scan + validação de prompts).
O CI vai rodar os mesmos gates — vermelho local = vermelho no GitHub.
