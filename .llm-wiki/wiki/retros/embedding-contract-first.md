---
type: analysis
created: 2026-09-14
updated: 2026-09-14
retro: true
---

# Retro: contrato antes do hardware

**Insight:** em RAG, o custo real de trocar de embedding é re-embeddar o corpus inteiro — não o servidor. Decisões que travam a arquitetura desde o dia 1: (1) endpoint OpenAI-compat `/v1/embeddings`; (2) `dimensions` fixado via MRL (1024) mesmo em modelos maiores; (3) normalização L2 sempre; (4) prefixo de instrução Qwen3 padronizado p/ query vs documento. Com isso Termux↔Pop!_OS↔Salad↔API são intercambiáveis e o índice sobrevive a troca de provedor.

**Aplicável a:** qualquer pipeline RAG multi-ambiente. Ver [endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md) e [MRL](/concepts/matryoshka-quantization.md).
