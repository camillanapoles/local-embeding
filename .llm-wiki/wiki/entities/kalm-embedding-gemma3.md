---
type: entity
category: model
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# KaLM-Embedding-Gemma3-12B-2511

SOTA MMTEB (~72.3), open-weight comercial-OK — mas 12B, GPU-only.

## O que é

Tencent, nov/2025. Topo do agregado MMTEB acima de Gemini-embedding-001 e NV-Embed-v2; licença permissiva; GGUFs i1 existentes. Exige ~8-12GB VRAM quantizado.

## Papel neste projeto

Candidato a upgrade do endpoint **cloud** (Salad 3090/4090-class) se o eval mostrar ganho vs Qwen3-8B no corpus alvo. Fora de alcance local.

## Links

- [Fonte: model card](/sources/kalm-embedding-gemma3-card.md)
- [Conceito: MTEB](/concepts/mteb-benchmark.md)
- [Entidade: SaladCloud](/entities/saladcloud.md)
