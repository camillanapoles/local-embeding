---
name: block-prompt-sem-fsm
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: prompts/.*\.json$
  - field: new_text
    operator: not_contains
    pattern: states
  - field: new_text
    operator: not_contains
    pattern: steps
---

**SEMPRE FSM**: todo prompt precisa de schema explícita (`states` v2 — ou `steps` legado, aceito por compat).
Prompt sem máquina de estados não passa. Valide com `python3 -m apps.core validate prompts/<arquivo>`.
