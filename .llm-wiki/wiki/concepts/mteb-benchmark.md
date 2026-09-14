---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# MTEB / MMTEB

Benchmark de referência de embeddings — ler com foco em retrieval, não na média.

## Definição

MTEB agrega 56+ tarefas (classificação, clustering, STS, retrieval...); MMTEB estende multilingual/multimodal. A média esconde: um modelo pode dominar classificação e perder em retrieval — para RAG usar **NDCG@10 de retrieval** e, idealmente, eval no próprio corpus.

## Como funciona / Como aplicar

Topo 2026: KaLM-Gemma3-12B ~72.3 > Qwen3-Embedding-8B 70.58 > NV-Embed-v2 69.32 (NC) > Gemini-embedding-001 68.32. Verificar leaderboard vivo antes de decidir; scores mudam mensalmente.

## Exemplos

- Escolha final do projeto: Qwen3-Embedding (Apache 2.0, MRL, 0.6B→8B) em vez de perseguir o topo bruto

## Relacionados

- [Fonte: ranking](/sources/premai-best-embedding-models-2026.md)
- [Fonte: Milvus snippet](/sources/milvus-embedding-2026.md)
- [Conceito: MRL](/concepts/matryoshka-quantization.md)
