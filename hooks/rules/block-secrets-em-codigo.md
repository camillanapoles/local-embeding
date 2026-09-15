---
name: block-secrets-em-codigo
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: contains
    pattern: apps/
  - field: file_path
    operator: not_contains
    pattern: test
  - field: new_text
    operator: regex_match
    pattern: (?i)(api[_\-]?key|secret|password)\s*[:=]
---

**SEGREDO NÃO VAI NO CÓDIGO**: use env (`export ...`) ou secret manager. `backend.toml` fica fora do git (.gitignore).
