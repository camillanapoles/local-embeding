# HISTORY (WAL do projeto)

- 2026-09-14 — vault .llm-wiki + docs (LOCAL/CLOUD/DECISAO/VOICE) criados e verificados (llama-server build+serve no Android: 1024 dims, 135ms solo).
- 2026-09-14 — scaffold do repo GitHub: app Android (IME/teclado + voz + prompts FSM), TUI Termux, models.json, CI build-APK, CD release.
- 2026-09-14 — CI verde no branch fix/ci-sem-setup-android (run 34909110800): setup-android removido (SDK do runner), distribution restaurada, APIs Android corrigidas (Handler/commitText/onPartialResults). APK artifact OK.
- 2026-09-15 — harness FSM+OODA gate-driven (S1-S8, PRs #2-#4): core python, 23 unit + 5 e2e (stub HTTP + cenários negativos), scanner zero-hardcode (corrigiu 4 no APK), 5 hookify rules, gates.sh, HARNESS.md, prompts v2.
