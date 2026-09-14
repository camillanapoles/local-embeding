---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-010/extracted.md
ingested: 2026-09-14
topics: [embedding-models-2026, local-serving, cloud-gpu, rag-pipeline]
tier: A
---

# sqlite-vec v0.1.9 — verificado no Termux

> _Original: [https://github.com/asg017/sqlite-vec](https://github.com/asg017/sqlite-vec) · Publicado: v0.1.9 (v0.1.0 estável 2024-05) · Verificação: local-test · Packet: [[sources/SRC-2026-09-14-010]]_

## Resumo

Extensão SQLite de vector search portátil (vec0 virtual tables). VERIFICADO NESTE DISPOSITIVO: pip falha no Termux (sem wheel android/cp314), mas a release loadable-android-aarch64 (vec0.so, NDK r27, min Android 21) carrega via db.load_extension e faz KNN 1024-dim corretamente.

## Key Takeaways

- Caminho Termux: baixar tarball da release, extrair vec0.so, load_extension — sem pip, sem compilar
- KNN brute-force: ms até ~centenas de milhares de vetores
- Sem ANN ainda → acima disso, Qdrant
- Vecores como blob struct.pack(nf, *vec)

## Entidades Mencionadas

- [sqlite-vec](/entities/sqlite-vec.md)

## Conceitos Mencionados

- [Indexação incremental](/concepts/incremental-indexing.md)

## Fonte

- [SRC-2026-09-14-010/extracted.md](../../raw/sources/SRC-2026-09-14-010/extracted.md)
