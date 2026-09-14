# KaLM-Embedding-Gemma3-12B-2511

- **SOTA em MMTEB** (até 11-2025), ~72.32 agregado (páginas MTEB 2026) — acima de Gemini-embedding-001 (68.32) e NV-Embed (69.32).
- Licença "KaLM-Embedding": uso/cópia/modificação/venda permitidos sem restrição adicional (além de componentes third-party no NOTICE) → comercial-OK.
- GGUFs i1 (mradermacher) existem, mas 12B exige GPU (~8-12GB VRAM quantizado) → target = Salad RTX 3090/4090-class, não CPU.
- Alternativa compacta da mesma org: `KaLM-embedding-multilingual-mini-instruct-v2.5` + KaLM Reranker.
