---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# Endpoint de embedding OpenAI-compat

Contrato `/v1/embeddings` que permite trocar provedor sem tocar no código das apps.

## Definição

POST `/v1/embeddings` com `{model, input, dimensions?, encoding_format?}` → `{data: [{embedding, index}], model, usage}`. Suportado por llama.cpp, TEI, Infinity, Ollama e todos os vendors — virou lingua franca 2026.

## Como funciona / Como aplicar

Fixar no cliente: `base_url` configurável, `model` = alias lógico (`embed-small`/`embed-large`), `dimensions` fixo (MRL) e normalização L2 sempre ligada. Assim Termux/Pop!_OS/Salad/API são intercambiáveis por variável de ambiente.

## Exemplos

- llama.cpp: `llama-server --embedding` (porta 8080)
- TEI: `/v1/embeddings` + `/v1/rerank` no mesmo server
- Infinity: idem, CPU ONNX

## Relacionados

- [Endpoint rerank](/concepts/hybrid-search-rerank.md)
- [MRL](/concepts/matryoshka-quantization.md)
- [Entidades: llama.cpp](/entities/llama-cpp.md), [TEI](/entities/text-embeddings-inference.md)
