# HARNESS — práticas e sequência (FSM sempre · OODA · gates · zero hardcode)

> Implementado em `apps/core/` (Python). CLI: `python3 -m apps.core list|validate|run`.
> Regras de bloqueio no editor: `hooks/rules/` (instale com `bash scripts/install-hooks.sh`).
> Gates locais = gates do CI: `bash scripts/gates.sh`.

## As 4 práticas (invioláveis — hooks e CI bloqueiam)

1. **SEMPRE FSM** — prompt é máquina de estados explícita (`prompts/*.json`, schema v2:
   `states[{id,prompt,terminal,transitions[{to,when}],on_error,intent_action}]`, `initial`).
   Guardas: `{"var","op":"eq|contains|nonempty","val"}` sobre `{{input}}/{{prev}}/{{context}}`.
   Legado `steps[]` é aceito por compat (linear). Regra hookify: `block-prompt-sem-fsm`.
2. **OODA por estado** — o runner (`apps/core/ooda.py`) executa Observe (variáveis+input) →
   Orient (`context_provider` opcional injeta `{{context}}` — ex.: RAG) → Decide (render+LLM
   atrás dos gates) → Act (saída, transição, intent). Trace completo por estado.
3. **GATE-DRIVEN (fail-closed)** — nada roda sem gate verde (`apps/core/gates.py`):
   - **SchemaGate**: prompt inválido NUNCA chama o LLM;
   - **Budget**: chamadas/tokens/prazo estourados → aborta (`GateError`);
   - **Policy**: intents deny-all por default — allowlist via `EMB_INTENTS_ALLOWLIST`.
   No CI: `Core unit`, `E2E backend` (inclui cenários negativos), `Hardcode scan`.
4. **ZERO HARDCODE** — endpoint/modelo/limites/secrets vêm de env ou `backend.toml`
   (`backend.toml.example`); faltando config → erro claro, sem default mágico.
   Scanner `python3 -m apps.core.hardcode_scan` varre apps/ e scripts/ (URLs, IPs,
   model-ids, secrets) e FALHA o build. Regras hookify: `block-hardcoded-endpoint`,
   `block-hardcoded-model-ids`, `block-secrets-em-codigo`.
   Exceção documentada: defaults de UI do APK vivem em `res/values/strings.xml`
   (recurso, não código) — o scanner continua cobrindo .kt/.py.

## Sequência de desenvolvimento (como foi construído — repita para novos slices)

```
S1 FSM v2 → S2 OODA → S3 config externa → S4 gates+scanner → S5 hookify rules
→ S6 CLI/TUI no core → S7 E2E (stub HTTP + cenários negativos) → S8 prompts v2+docs
```

Cada slice: **branch {feat|fix|docs}/slug → testes primeiro (TDD) → implementação →
`bash scripts/gates.sh` verde local → push → CI gateia → PR → auto-merge → main**.
Branch protection exige os gates — merge determinístico, sem humano.

## Como adicionar um prompt novo

1. Crie `prompts/<id>.json` (schema v2; a regra hookify bloqueia sem `states`);
2. `python3 -m apps.core validate prompts/<id>.json`;
3. Rode: `EMB_BASE_URL=... EMB_MODEL=... python3 -m apps.core run prompts/<id>.json "texto"`;
4. Se usar `intent_action`, libere a intent em `EMB_INTENTS_ALLOWLIST` (deny-all!);
5. Sincronize a cópia do APK (`apps/android/.../assets/prompts/`) se quiser no teclado.

## Testes

- `tests/unit/` — fsm/ooda/config/gates/scan/hookify (23)
- `tests/e2e/` — stub OpenAI-compat em HTTP real + happy path + cenários negativos
  (budget estoura, intent negada, schema inválida não chama LLM) (5)
- CI: mesmos gates, mais APK/Docs/YAML. `protege-main` exige todos.
