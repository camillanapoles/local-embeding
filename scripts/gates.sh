#!/usr/bin/env bash
# gates.sh — os mesmos gates do CI, localmente (pre-push). Fail-closed.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "[gate 1/3] unit tests"
python3 -m pytest tests -q
echo "[gate 2/3] hardcode scan"
python3 -m apps.core.hardcode_scan
echo "[gate 3/3] prompts = FSM válidas"
python3 - <<'PY'
import glob, json, sys
from apps.core.fsm import validate
bad = []
for f in glob.glob("prompts/*.json"):
    errs = validate(json.load(open(f, encoding="utf-8")))
    if errs:
        bad.append((f, errs))
for f, errs in bad:
    print(f"✗ {f}: {errs}")
sys.exit(1 if bad else 0)
PY
echo "✔ gates verdes"
