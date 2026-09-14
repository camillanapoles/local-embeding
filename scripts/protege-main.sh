#!/usr/bin/env bash
# ============================================================================
# github-ops-cicd — protege-main: merge 100% automatizado e determinístico.
# Faz: required status checks (seus gates) + allow_auto_merge + PR obrigatório
# + strict (branch atualizado). Uso:
#   bash protege-main.sh owner/repo "Check 1" "Check 2" ...
# Dica: os nomes EXATOS dos checks saem de:
#   gh pr view <n> --repo owner/repo --json statusCheckRollup
# ============================================================================
set -euo pipefail
REPO="${1:?uso: protege-main.sh owner/repo \"Check A\" \"Check B\" ...}"
shift
[ "$#" -ge 1 ] || { echo "erro: informe ao menos um check required"; exit 1; }

CONTEXTS=$(printf '%s\n' "$@" | jq -R . | jq -s . | jq -c .)

gh api -X PUT "repos/$REPO/branches/main/protection" --input - <<EOF
{
  "required_status_checks": {"strict": true, "contexts": $CONTEXTS},
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "dismiss_stale_reviews": false
  },
  "restrictions": null,
  "allow_auto_merge": true,
  "allow_deletions": true,
  "allow_force_pushes": false
}
EOF

# repo-level: auto-merge precisa estar habilitado também no repo
gh api -X PATCH "repos/$REPO" -f allow_auto_merge=true -q '.full_name' >/dev/null

echo "✔ main protegido: gates required = $* · auto-merge ON · strict ON"
