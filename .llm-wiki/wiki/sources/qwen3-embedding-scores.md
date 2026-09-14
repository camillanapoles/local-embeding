---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-019/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026]
tier: A
---

# Qwen3-Embedding — scores oficiais (0.6B/4B/8B)

> _Original: [model card 0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) · [GitHub QwenLM](https://github.com/QwenLM/Qwen3-Embedding) · arXiv 2506.05176 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-019]]_

## Resumo

Scores oficiais por variante: 0.6B (MTEB-R 61.82 / MMTEB-R 64.64 / **MTEB-Code 75.41**), 8B 70.58 multilingual (#1 open-source). Referência de mercado text-embedding-3-large: MTEB-R 58.93.

## Key Takeaways

- **0.6B > padrão OpenAI em retrieval**, mesmo rodando em telefone
- MTEB-Code 75.41 = topo p/ knowledge base de código (o caso de diretórios de dev)
- MMTEB-R 64.64 = forte em PT-BR

## Entidades Mencionadas

- [Qwen3-Embedding (família)](/entities/qwen3-embedding-family.md)

## Conceitos Mencionados

- [MTEB benchmark](/concepts/mteb-benchmark.md)

## Fonte

- [SRC-2026-09-14-019/extracted.md](../../raw/sources/SRC-2026-09-14-019/extracted.md)
