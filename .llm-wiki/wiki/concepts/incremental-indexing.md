---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-001]
---

# Indexação incremental (content-hash)

Re-embeddar só o que mudou, usando hash de conteúdo como identidade do chunk.

## Definição

Para cada arquivo: `sha256(conteúdo)` na tabela `files`; se mudou → apagar chunks antigos (por file_id), chunkar de novo, embeddar em batch e upsertar. Watcher (inotify/watchdog) dispara re-index em save; corrida evitada com single-writer (SQLite WAL / lock no Qdrant por collection). Cache por hash = idempotência entre dispositivos.

## Como funciona / Como aplicar

Tabelas SQLite: `files(path, sha256, mtime, updated_at)` + `chunks(file_id, idx, text, embedding blob)` (+ FTS5 espelho p/ BM25). No Qdrant: point id = hash(path+idx) → upsert idempotente.

## Exemplos

- skill ECC `content-hash-cache-pattern` aplica o mesmo princípio em pipelines de arquivos

## Relacionados

- [Chunking recursivo](/concepts/recursive-directory-chunking.md)
- [Entidade: sqlite-vec](/entities/sqlite-vec.md)
- [Fonte: sqlite-vec](/sources/sqlite-vec-release.md)
