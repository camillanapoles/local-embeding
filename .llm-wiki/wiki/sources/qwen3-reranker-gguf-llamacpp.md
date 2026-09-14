---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-012/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# Qwen3-Reranker GGUF + llama-server --rerank

> _Original: [https://huggingface.co/collections/Voodisss/qwen3-reranker-gguf-for-llamacpp](https://huggingface.co/collections/Voodisss/qwen3-reranker-gguf-for-llamacpp) · Publicado: 2026-03-10 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-012]]_

## Resumo

Como servir reranker local: llama-server --rerank com GGUF do Qwen3-Reranker (0.6B/4B/8B). Alerta: conversões de comunidade quebradas — usar GGUFs convertidos com convert_hf_to_gguf.py oficial (cls.output.weight + pooling_type=RANK).

## Key Takeaways

- `llama-server --rerank --port 11435` → endpoint REST {model, query, documents}
- 0.6B_Q8 = 639MB — roda até em telefone
- Rerank é o maior ganho único de precisão no RAG 2026

## Entidades Mencionadas

- [llama.cpp](/entities/llama-cpp.md)
- [Qwen3-Embedding (família)](/entities/qwen3-embedding-family.md)

## Conceitos Mencionados

- [Híbrido+rerank](/concepts/hybrid-search-rerank.md)

## Fonte

- [SRC-2026-09-14-012/extracted.md](../../raw/sources/SRC-2026-09-14-012/extracted.md)
