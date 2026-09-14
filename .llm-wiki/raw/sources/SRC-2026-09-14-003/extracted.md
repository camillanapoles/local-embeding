# Working with llama.cpp Embeddings — Software.Land

## Rotas de embedding do llama-server

- `/embeddings` — nativa: shape llama-cpp, suporta TODOS os pooling modes (incl. `none` p/ vetores por token).
- `/v1/embeddings` — OpenAI-compat: aceita `model`, `input`, `encoding_format`, `dimensions`, `user`; retorna 1 embedding pooled por input (pooling != none exigido).
- Uso típico: `llama-server --model Qwen3-Embedding-4B-Q4_K_M.gguf --port 8080 --embedding -c 2048`.
- Ambas rotas usam nomes de campo OpenAI → trocar endpoint local por remoto não muda código cliente.

Flag TIER B: data da publicação não confirmada; conteúdo confere com as docs do repo.
