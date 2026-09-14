# Qdrant — híbrido + quantização

- **Query API** (v1.10+): combina dense, sparse, BM25, fusion e filtros **server-side**; filtros aplicados durante a travessia do índice.
- Sparse vectors nativos → BM25/SPLADE no mesmo store (híbrido sem segundo sistema).
- Quantização: **scalar** (uint8, SIMD), **binary** (1 bit/componente: até **32x menos RAM, até 40x mais rápido**, 2-5% perda de recall), **asymmetric** (armazena binário, consulta escalar), product.
- HNSW + ACORN (1.16); storage Rust com mmap+WAL.
- Benchmarks 2026 (ailog): binary quantization = primeira otimização de produção a ligar.
