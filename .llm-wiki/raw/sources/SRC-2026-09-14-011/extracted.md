# Infinity (infinity-emb)

- Servidor FastAPI **OpenAI-compat /v1/embeddings** p/ embeddings, rerankers, CLIP, CLAP e ColPali do HF.
- Backends: PyTorch, **optimum (ONNX/TensorRT)**, CTranslate2 — **CPU via `--engine optimum`** (rápido sem GPU).
- Docker CPU: `docker run -p 7997:7997 michaelf34/infinity:0.0.70-cpu v2 --model-id Snowflake/snowflake-arctic-embed-m --engine optimum`.
- Também `pip install infinity-emb[all]` (bom p/ x86 sem Docker). Integra LangChain `InfinityEmbeddings`.
- Suporta reranking (ex.: bge-reranker-v2-m3) no mesmo server.
