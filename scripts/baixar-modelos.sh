#!/usr/bin/env bash
# baixar-modelos.sh — baixa os modelos INDICADOS PELO OPERADOR (models.json) p/ ~/models
# Uso: bash scripts/baixar-modelos.sh --list | --id chat | --all
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="${MODELS_DIR:-$HOME/models}"
MODE="${1:---list}"; ID="${2:-}"
mkdir -p "$DEST"
listar() { jq -r '.models[] | "\(.id)\t\(.size_mb)MB\tverified=\(.verified)\t\(.name)"' models.json; }
case "$MODE" in
  --list) listar ;;
  --all)
    while IFS=$'\t' read -r mid _; do
      url=$(jq -r --arg i "$mid" '.models[] | select(.id==$i) | .url' models.json)
      [ -n "$url" ] && [ "$url" != "null" ] && { echo "➜ $mid"; curl -fL -C - -o "$DEST/$(basename "$url")" "$url"; }
    done < <(listar | cut -f1) ;;
  --id)
    url=$(jq -r --arg i "$ID" '.models[] | select(.id==$i) | .url' models.json)
    [ -n "$url" ] && [ "$url" != "null" ] || { echo "id '$ID' sem URL (ver models.json)"; exit 1; }
    echo "➜ $ID -> $DEST/$(basename "$url")"; curl -fL -C - -o "$DEST/$(basename "$url")" "$url" ;;
  *) echo "uso: $0 --list | --all | --id <id>"; exit 2 ;;
esac
