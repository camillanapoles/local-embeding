# Chunking 2026 — síntese de 3 guias

- Chunks **200-400 tokens com 20-30% overlap** = baseline equilibrado (recall vs custo).
- **Late chunking** (Jina): embeda o documento inteiro primeiro, depois recorta — ganho cresce com o tamanho do doc (~3% BEIR médio; mais em docs longos).
- **Contextual retrieval** (Anthropic): prefixar chunk com resumo LLM do contexto → **-67% falhas top-20** combinado com rerank.
- **Híbrido + RRF**: dense + BM25, fusão Reciprocal Rank Fusion, depois cross-encoder rerank (top 5-20).
- Metadados de caminho (file path, headers) e chunking por AST p/ código = prática padrão 2026.
- Monitorar recall@k / MRR continuamente; benchmark público ≠ seu corpus.
