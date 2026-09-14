---
type: synthesis
topic: stack local de embedding (Termux + Pop!_OS)
created: 2026-09-14
updated: 2026-09-14
sources_count: 7
---

# Stack local de embedding para RAG (Termux + Pop!_OS)

> _Síntese de 7 fontes. Detalhe operacional completo: [docs/EMBED-RAG-LOCAL.md](../../../docs/EMBED-RAG-LOCAL.md)_

## Pergunta

Como montar um endpoint de embedding OpenAI-compat, 100% local, para RAG sobre diretórios recursivos — num Android (Termux, root, ADB) e num desktop CPU Pop!_OS?

## Análise

**Camada de contrato** — tudo fala `/v1/embeddings` OpenAI-compat ([llama.cpp](/entities/llama-cpp.md), [TEI](/entities/text-embeddings-inference.md), [Infinity](/entities/infinity-emb.md)). Apps apontam `base_url`; hardware vira detalhe.

**Modelo** — [Qwen3-Embedding](/entities/qwen3-embedding-family.md) (Apache 2.0, #1 open-source no MTEB multilingual, instruction-aware, MRL): 0.6B (1024d) no telefone; 4B no desktop; mesma família → mesmo prefixo de instrução e normalização; `dimensions=1024` via MRL padroniza o índice entre dispositivos.

**Servidor** — Termux: build nativo do llama.cpp (sem root) + `llama-server --embedding`; daemon via tmux/termux-services; acesso externo via `adb forward` ou ssh (8022). Pop!_OS: Infinity `--engine optimum` (ONNX CPU, sem Docker) ou TEI `cpu-2.0` (Docker); llama.cpp como opção C simples.

**Vector store** — Termux: [sqlite-vec](/entities/sqlite-vec.md) v0.1.9 `vec0.so` android-aarch64 — **verificado localmente** (pip falha; release loadable funciona). Pop!_OS: Qdrant (híbrido server-side + quantização).

**Pipeline** — [chunking recursivo](/concepts/recursive-directory-chunking.md) (200-400 tok, path-aware) + [indexação incremental](/concepts/incremental-indexing.md) por sha256 + BM25 (FTS5 / Qdrant sparse) + rerank ([Qwen3-Reranker 0.6B](/sources/qwen3-reranker-gguf-llamacpp.md)).

## Verificação real (2026-09-14, neste Android)

- Build `llama-server` (alvo único, Release): **4m54s** — Clang 21.1.8, v0.4.1-dev Android aarch64; libs `.so` no mesmo dir (`LD_LIBRARY_PATH=.`).
- GGUF **oficial** `Qwen/Qwen3-Embedding-0.6B-GGUF` (Q8_0, 639MB): carga em **3,15s** (mmap).
- `/health` ok · `/v1/embeddings` = **1024 dims** + `usage` · **135ms solo** · **253ms batch×8**.
- Quebrou no caminho: `--mlock` foi removido do llama-server atual (agora `--mmap mmap+mlock`) — lesson em [retro](/retros/llamacpp-termux-verified.md).

## Conclusões

1. O stack local 2026 é viável e barato: telefone serve 0.6B em ~0.7GB RAM; desktop CPU serve 4B com ONNX.
2. O gargalo local é throughput (ingestão de corpus grande), não qualidade — reranker 0.6B corrige precisão por pouco custo.
3. Índice portátil (mesmo modelo+dimensions) é o que permite promover p/ cloud sem re-embeddar tudo — decidir `dimensions=1024` no dia 1.

## Fontes

- [PremAI ranking 2026](/sources/premai-best-embedding-models-2026.md) · [llama.cpp android](/sources/llama-cpp-android-docs.md) · [API embeddings](/sources/llamacpp-embeddings-api.md) · [TEI](/sources/text-embeddings-inference-repo.md) · [Infinity](/sources/infinity-emb-repo.md) · [sqlite-vec](/sources/sqlite-vec-release.md) · [chunking 2026](/sources/rag-chunking-2026-guides.md)

## Relacionados

- [Síntese cloud](/syntheses/cloud-embedding-stack.md) · [Decisão local vs cloud](/syntheses/local-vs-cloud-decision.md)
