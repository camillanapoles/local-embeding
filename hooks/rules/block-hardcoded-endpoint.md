---
name: block-hardcoded-endpoint
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
    pattern: (https?://|([0-9]{1,3}\.){3}[0-9]{1,3})
---

**ZERO HARDCODE**: endpoint/IP no código de `apps/` é proibido.
Use `EMB_BASE_URL` (env) ou `backend.toml` — veja `backend.toml.example` e `apps/core/config.py`.
Falhou no editor, falha também no CI (job Hardcode scan).
