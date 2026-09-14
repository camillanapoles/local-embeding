# sqlite-vec — verificado localmente no Termux

- Extensão SQLite de vector search "que roda em qualquer lugar"; sem dependências; virtual tables `vec0`.
- **VERIFICAÇÃO LOCAL (2026-09-14, Termux/Android arm64, Python 3.14, SQLite 3.53.4):**
  - `pip install sqlite-vec` FALHA no Termux (sem wheel android/cp314; nenhuma distribuição compatível no PyPI) → **usar release pré-compilada**.
  - Release v0.1.9 traz `sqlite-vec-0.1.9-loadable-android-aarch64.tar.gz` com `vec0.so` (ELF aarch64, "for Android 21", NDK r27).
  - Carregar: `db.enable_load_extension(True); db.load_extension(".../vec0")` → `vec_version()` = v0.1.9.
  - KNN 1024-dim float: `SELECT rowid, distance FROM chunks WHERE embedding MATCH ? AND k=3 ORDER BY distance` → distâncias corretas.
- Estado: produção-OK p/ workloads leves/médios (KNN brute-force); sem índice ANN ainda — escala grande → Qdrant.
- Inserção: blob `struct.pack(nf, *vec)`; consultas em ms para ~centenas de milhares de vetores em hardware típico.
