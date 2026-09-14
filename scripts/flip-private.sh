#!/usr/bin/env bash
# ============================================================================
# github-ops-cicd — flip-private: fechamento manual imediato da janela
# (não espera o watchdog). Uso: bash flip-private.sh owner/repo
# ============================================================================
set -euo pipefail
REPO="${1:?uso: flip-private.sh owner/repo}"
gh repo edit "$REPO" --visibility private --accept-visibility-change-consequences
echo "✔ $REPO privado (estado padrão)."
