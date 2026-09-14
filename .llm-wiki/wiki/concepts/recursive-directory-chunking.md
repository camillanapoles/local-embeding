---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# Chunking de diretórios recursivos

Transformar uma árvore de arquivos em chunks recuperáveis preservando origem e estrutura.

## Definição

Caminhar a árvore (os.walk), filtrar por extensão/ignore, extrair texto (código/markdown/pdf), chunkar **200-400 tokens com 20-30% overlap**; metadados obrigatórios: `path` relativo, `mtime`, `sha256`, headers/seção. Código: chunk por AST/função. Docs longos: late chunking (embeda inteiro, recorta depois) ou contextual retrieval (prefixo gerado por LLM).

## Como funciona / Como aplicar

Regras de ouro: (1) chunk carrega `path + header` — é o que permite resposta citar arquivo/linha; (2) nunca misturar arquivos no mesmo chunk; (3) binários/imagens fora do pipeline text-only (multimodal é caso separado, Qwen3-VL).

## Exemplos

- LlamaIndex `SimpleDirectoryReader(recursive=True)` + `SentenceSplitter`
- Custom: os.walk + tiktoken + sqlite (FTS5 para BM25)

## Relacionados

- [Indexação incremental](/concepts/incremental-indexing.md)
- [Híbrido+rerank](/concepts/hybrid-search-rerank.md)
- [Fonte: chunking 2026](/sources/rag-chunking-2026-guides.md)
