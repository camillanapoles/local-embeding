# Qwen3-Reranker via llama-server --rerank

- `llama-server --model Qwen3_Reranker-4B_GGUF --host 0.0.0.0 --port 11435 --ctx-size 8192 --rerank` → endpoint REST com payload `model`, `query`, `documents` retorna scores ranqueados.
- ⚠️ Muitas conversões GGUF de comunidade estão **quebradas** (faltam `cls.output.weight`/`pooling_type=RANK`); usar coleções testadas (Voodisss, mar/2026) ou converter com o script oficial.
- Ollama também hospeda `AuditAid/Qwen3_Reranker:0.6B_Q8` (639MB, 40K ctx).
- Composição recomendada: embedding endpoint (porta 8080) + rerank endpoint (porta 11435) — mesmo binário llama-server.
