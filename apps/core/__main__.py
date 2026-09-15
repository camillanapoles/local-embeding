"""CLI do harness — python3 -m apps.core <comando>

  validate <prompts/*.json>   # gate de schema (a mesma validação do CI)
  list                        # lista prompts de prompts/
  run <file.json> "entrada"   # FSM+OODA+gates via endpoint configurado (env/backend.toml)

Fail-closed em tudo: sem config não roda; gates violados abortam; intent fora da
allowlist não dispara (exit 3).
"""
from __future__ import annotations

import glob
import json
import os
import sys

from .config import Config, ConfigError
from .fsm import load
from .gates import Budget, GateError, PolicyGate, SchemaGate
from .llm import make_llm
from .ooda import OodaRunner

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PROMPTS = os.path.join(ROOT, "prompts")


def cmd_validate(path: str) -> int:
    obj = json.load(open(path, encoding="utf-8"))
    try:
        fsm = load(obj)  # load valida (fail-closed)
        SchemaGate(obj).check({"kind": "prompt_load"})
        print(f"✓ {path}: FSM válida — {len(fsm.states)} estados, inicial={fsm.initial}")
        return 0
    except Exception as e:
        print(f"✗ {path}: {e}")
        return 1


def cmd_list() -> int:
    for f in sorted(glob.glob(os.path.join(PROMPTS, "*.json"))):
        obj = json.load(open(f, encoding="utf-8"))
        print(f"- {obj.get('id')}: {obj.get('name')} ({os.path.basename(f)})")
    return 0


def cmd_run(path: str, text: str) -> int:
    obj = json.load(open(path, encoding="utf-8"))
    SchemaGate(obj).check({"kind": "prompt_load"})  # fail-closed antes de qualquer chamada
    fsm = load(obj)
    try:
        cfg = Config.from_env(path=os.path.join(ROOT, "backend.toml"))
    except ConfigError as e:
        print(e)
        return 2
    llm = make_llm(cfg.base_url, cfg.model, cfg.timeout_s)
    policy = PolicyGate(cfg.intents_allowlist)
    runner = OodaRunner(fsm, llm, gates=[Budget.from_config(cfg)])
    res = runner.run(text)
    for i, out in enumerate(res.outputs, 1):
        print(f"[saída {i}] {out}")
    if res.intent_action:
        policy.check({"kind": "intent", "intent": res.intent_action})
        print(f"[intent liberada] {res.intent_action}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "validate" and len(argv) > 2:
        return cmd_validate(argv[2])
    if cmd == "list":
        return cmd_list()
    if cmd == "run" and len(argv) > 3:
        try:
            return cmd_run(argv[2], argv[3])
        except GateError as e:
            print(f"GATE BLOQUEOU: {e}")
            return 3
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
