---
name: block-hardcoded-model-ids
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
    pattern: (gpt-|claude-|gemini-|text-embedding-)[a-z0-9.\-]+
---

**ZERO HARDCODE**: id de modelo no código é proibido — nome de modelo é configuração (`EMB_MODEL`), não código.
