# Best Embedding Models for RAG (2026) — PremAI

Publicado 2026-03-17, atualizado 2026-09-04. Leitura completa feita em 2026-09-14.

## Tabela comparativa (valores-chave)

| Modelo | MTEB | Contexto | Dimensões | Custo/1M | Self-host | Licença |
|---|---|---|---|---|---|---|
| Gemini embedding-001 | 68.32 | 2.048 | 3072 (flex) | $0.15 | Não | Proprietária |
| Qwen3-Embedding-8B | 70.58 (multiling.) | 32.000 | 7168 (flex p/ 32) | grátis | Sim | Apache 2.0 |
| voyage-3-large | ~67+ | 32.000 | 2048 (flex) | $0.06 | Não | Proprietária |
| text-embedding-3-large | 64.6 | 8.192 | 3072 (flex) | $0.13 | Não | Proprietária |
| Cohere embed-v4 | 65.2 | 128.000 | 1024 | $0.10 | VPC/On-prem | Proprietária |
| BGE-M3 | 63.0 | 8.192 | 1024 | grátis | Sim | MIT |
| NV-Embed-v2 | 69.32 | 32.768 | 4096 | grátis | Sim | CC-BY-NC-4.0 |
| Jina embeddings-v3 | ~62+ | 8.192 | 1024 (flex p/ 32) | $0.018 | Sim | CC-BY-NC-4.0 |
| Nomic embed-text-v1.5 | ~62+ | 8.192 | 768 (flex) | $0.10 | Sim | Apache 2.0 |
| all-MiniLM-L6-v2 | 56.3 | 512 | 384 | grátis | Sim | Apache 2.0 |

## Pontos-chave

- MTEB é média de 56+ tarefas; para RAG o que importa é **NDCG@10 de retrieval** — usar score retrieval-específico.
- Qwen3-Embedding-8B: #1 open-source (Apache 2.0), 32K ctx, MRL 32→7168 dims, variantes 0.6B/4B.
- Qwen3-Embedding é **instruction-aware**: prefixo `Instruct: Represent this document for retrieval\nQuery:` melhora +1-5%.
- BGE-M3: dense+sparse+multi-vector num único modelo (MIT, 568M params) — híbrido com menos infra.
- Voyage-3-large: melhor NDCG@10 proprietário a $0.06/1M; Anthropic recomenda no ecossistema Claude.
- Cohere embed-v4: 128K ctx (chunking quase desnecessário), robusto a OCR/ruído; fraco sem reranker.
- MRL: 3072→1024 dims corta storage 3x com ~2% de perda.
- Recomendação da fonte: rodar eval de retrieval no próprio corpus antes de commitir.
