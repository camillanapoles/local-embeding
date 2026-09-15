#!/usr/bin/env bash
# instala as hookify rules versionadas (hooks/rules/) em .agents/ (padrão do hookify).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .agents
for rule in hooks/rules/*.md; do
  name=$(basename "$rule" .md)
  dest=".agents/hookify.${name}.local.md"
  cp "$rule" "$dest"
  echo "instalado $dest"
done
grep -q "hookify" .gitignore 2>/dev/null || printf "\n.agents/*.local.md\nbackend.toml\n" >> .gitignore
echo "✔ rules instaladas (action:block falham fechado no editor; .agents/*.local.md e backend.toml no .gitignore)"
