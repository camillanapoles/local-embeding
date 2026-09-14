#!/usr/bin/env bash
# ============================================================================
# github-ops-cicd — flip-public: abre a janela PÚBLICA (Actions em plano que
# exige repo público), dispara CI catch-up e a sentinela do watchdog.
# Uso: bash flip-public.sh owner/repo [watchdog_owner/watchdog_repo]
# ============================================================================
set -euo pipefail
REPO="${1:?uso: flip-public.sh owner/repo [watchdog_owner/watchdog_repo]}"
WATCHDOG="${2:-}"

gh repo edit "$REPO" --visibility public --accept-visibility-change-consequences

# Catch-up: valida HEAD (commits feitos na janela fechada não dispararam CI)
gh workflow run ci.yml --ref main --repo "$REPO" 2>/dev/null || \
  echo "⚠ ci.yml não disparou (sem workflow_dispatch? chegue manualmente)"

# Sentinela: watchdog detecta a abertura NO ATO (schedule tem jitter alto)
if [ -n "$WATCHDOG" ]; then
  gh workflow run sentinel.yml --repo "$WATCHDOG" 2>/dev/null || true
fi

echo "✔ $REPO público. CI catch-up disparado. Watchdog reverte após inatividade."
