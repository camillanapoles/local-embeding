---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-014/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# KaLM-Embedding-Gemma3-12B-2511 — Tencent

> _Original: [https://huggingface.co/tencent/KaLM-Embedding-Gemma3-12B-2511](https://huggingface.co/tencent/KaLM-Embedding-Gemma3-12B-2511) · Publicado: 2511 (nov/2025), card vigente 2026 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-014]]_

## Resumo

SOTA MMTEB (~72.32 agregado) acima de Gemini-embedding-001 (68.32) e NV-Embed-v2 (69.32). Licença permissiva (uso comercial OK). 12B → exige GPU 8-12GB quantizado; alvo natural para Salad RTX 3090/4090-class.

## Key Takeaways

- Topo do leaderboard 2026 é open-weight e comercial-OK
- GGUFs i1 existem (mradermacher)
- Fora do alcance de CPU/telefone — usar Qwen3-Embedding lá

## Entidades Mencionadas

- [KaLM-Embedding-Gemma3](/entities/kalm-embedding-gemma3.md)

## Conceitos Mencionados

- [MTEB benchmark](/concepts/mteb-benchmark.md)
- [Matryoshka/quantização](/concepts/matryoshka-quantization.md)

## Fonte

- [SRC-2026-09-14-014/extracted.md](../../raw/sources/SRC-2026-09-14-014/extracted.md)
