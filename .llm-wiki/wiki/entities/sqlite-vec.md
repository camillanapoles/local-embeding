---
type: entity
category: tool
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001, raw/sources/SRC-2026-09-14-002]
---

# sqlite-vec

Extensão SQLite de vector search que roda em qualquer lugar — verificada no Termux.

## O que é

Alex Garcia (asg017). Virtual tables `vec0`, KNN via `WHERE embedding MATCH ? AND k=N`. **Verificado 2026-09-14 neste Android**: `vec0.so` da release `loadable-android-aarch64` v0.1.9 (NDK r27) carrega via `db.load_extension()` no Python 3.14 do Termux; `pip install` NÃO funciona (sem wheel android/cp314).

## Papel neste projeto

Vector store do **Termux**: arquivo único, portável, zero serviço. KNN brute-force ms-scale até ~centenas de milhares de vetores 1024-dim; acima disso migrar p/ Qdrant.

## Links

- [Fonte: release verificada](/sources/sqlite-vec-release.md)
- [Conceito: indexação incremental](/concepts/incremental-indexing.md)
- [Conceito: matryoshka/quantização](/concepts/matryoshka-quantization.md)
