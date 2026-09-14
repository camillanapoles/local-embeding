# Qwen3-Embedding — scores oficiais por variante

| Modelo | MTEB-R (EN) | MMTEB-R (multiling.) | MTEB-Code |
|---|---|---|---|
| Qwen3-Embedding-0.6B | 61.82 | 64.64 | **75.41** |
| Qwen3-Embedding-8B | 70.58 (MTEB multiling.) | #1 open-source | — |
| text-embedding-3-large (referência de mercado) | 58.93 | ~62 | ~63 |

- 0.6B **bate o padrão OpenAI em retrieval** (61.82 vs 58.93) e é topo em código (75.41) — mesmo sendo a variante de telefone.
- Comparativos: multilingual-e5-large-instruct 0.6B-param class similar (63.22 coluna na tabela do card); BGE-M3 abaixo em todas as dimensões avaliadas (análise comparativa).
