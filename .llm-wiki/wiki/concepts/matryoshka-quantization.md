---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# Matryoshka (MRL) + quantização

Reduzir dimensão do vetor (MRL) e precisão numérica (int8/binary) para caber storage/latência no orçamento.

## Definição

Modelos MRL (Qwen3-Embedding, voyage, OpenAI v3) treinam dims aninhadas: truncar 4096→1024→256 mantém quase toda a semântica (~2% perda em 3x menos storage). Quantização em runtime (Qdrant scalar/binary; ONNX int8 no Infinity) comprime mais: binary = 32x menos RAM / 40x mais rápido com 2-5% perda.

## Como funciona / Como aplicar

Projeto: fixar `dimensions=1024` em TODOS os endpoints (0.6B nativo 1024; 4B/8B truncados via MRL) → índice idêntico entre Termux, Pop!_OS e Salad; no Qdrant ligar quantização binary/scalar no collection.

## Exemplos

- Qwen3-0.6B: 1024d nativo (telefone)
- Qwen3-4B: 2560d → truncar p/ 1024 via param `dimensions`

## Relacionados

- [Endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)
- [Entidades: Qdrant](/entities/qdrant.md), [Qwen3](/entities/qwen3-embedding-family.md)
- [Fonte: Qdrant](/sources/qdrant-hybrid-quantization-docs.md)
