---
type: analysis
created: 2026-09-14
updated: 2026-09-14
retro: true
---

# Retro: verificação real do stack Termux (llama.cpp + Qwen3-Embedding-0.6B)

**Insight:** o caminho documentado funciona de ponta a ponta no Android — mas **3 detalhes só aparecem executando**: (1) `--mlock` não existe mais no llama-server (usar `--mmap mmap+mlock` ou nada); (2) o build compartilhado exige rodar de `build/bin` com `LD_LIBRARY_PATH=.`; (3) o aviso `n_batch > n_ubatch` é inofensivo p/ embeddings. Números âncora p/ replanejar custo de ingestão no phone: 135ms/input solo, 253ms/batch-8 curto, carga 3,15s.

**Aplicável a:** qualquer doc "how-to" de serving local — marcar o que foi medido vs estimado, e re-testar flags ao subir de versão do binário. Ver [síntese local](/syntheses/local-embedding-stack.md) e [sqlite-vec](/entities/sqlite-vec.md) (também verificado no mesmo dia).
