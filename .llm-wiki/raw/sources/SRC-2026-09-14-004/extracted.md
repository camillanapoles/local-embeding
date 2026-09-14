# TEI v2 — Hugging Face

- Endpoints REST **OpenAI-compat**: `/v1/embeddings`, `/v1/rerank`, `/v1/predict`.
- Imagens por hardware: `cpu-2.0` (x86_64), `cpu-arm64-2.0`, `2.0` (A100/A30, CC 80), `86-2.0` (A10/A40), `89-2.0` (RTX 40xx), `hopper-2.0` (H100), `rocm-2.0` (Instinct MI2xx/3xx).
- Launch GPU típico:
  `docker run --gpus all -p 8080:80 ghcr.io/huggingface/text-embeddings-inference:2.0 --model-id BAAI/bge-m3 --dtype float16 --max-batch-tokens 65536 --max-concurrent-requests 512`
- CPU: trocar tag por `cpu-2.0` e remover `--gpus all`.
- Auto-detecção de hardware no startup; `--dtype float16|bfloat16`; tuning de batch/concorrência.
- LangChain integra nativamente (`HuggingFaceTEIEmbeddings`).
