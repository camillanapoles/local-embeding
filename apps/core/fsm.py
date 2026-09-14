"""FSM v2 — prompts/conversas como máquina de estados explícita (S1).

Schema v2 (JSON/dict):
  {"id","name","initial","states":[{"id","prompt","terminal"?,"on_error"?,"intent_action"?,
    "transitions":[{"to","when"?}]}], "intent_action"?}
Compat legado: {"steps":[{"template"...}]} -> FSM linear terminal no último.

Regras (fail-closed): validate() devolve TODOS os erros; from_dict recusa inválida.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Mapping

_GUARD_OPS = {"eq", "contains", "nonempty"}


class FsmError(Exception):
    """FSM inválida ou execução quebrou um invariantes."""


def render(template: str, variables: Mapping[str, str]) -> str:
    out = template
    for k, v in variables.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out


@dataclass
class Transition:
    to: str
    when: dict | None = None

    def matches(self, variables: Mapping[str, str]) -> bool:
        if not self.when:
            return True
        var = self.when.get("var", "")
        cur = str(variables.get(var, ""))
        op = self.when.get("op", "nonempty")
        val = str(self.when.get("val", ""))
        if op == "eq":
            return cur == val
        if op == "contains":
            return val in cur
        if op == "nonempty":
            return bool(cur.strip())
        raise FsmError(f"op de guarda desconhecida: {op}")


@dataclass
class State:
    id: str
    prompt: str
    transitions: list[Transition] = field(default_factory=list)
    terminal: bool = False
    on_error: str | None = None
    intent_action: str | None = None


@dataclass
class Fsm:
    id: str
    name: str
    initial: str
    states: dict[str, State]
    intent_action: str | None = None

    # ---- construção/validação (fail-closed) ----
    @classmethod
    def from_dict(cls, obj: dict) -> "Fsm":
        errors = validate(obj)
        if errors:
            raise FsmError("FSM inválida: " + "; ".join(errors))
        states = {}
        for s in obj["states"]:
            states[s["id"]] = State(
                id=s["id"], prompt=s["prompt"], terminal=bool(s.get("terminal", False)),
                on_error=s.get("on_error"), intent_action=s.get("intent_action"),
                transitions=[Transition(t["to"], t.get("when")) for t in s.get("transitions", [])],
            )
        return cls(obj["id"], obj["name"], obj["initial"], states, obj.get("intent_action"))

    @classmethod
    def from_legacy_steps(cls, obj: dict) -> "Fsm":
        steps = obj.get("steps", [])
        states = {}
        n = len(steps)
        for i, st in enumerate(steps):
            sid = st.get("id", f"s{i + 1}")
            states[sid] = State(id=sid, prompt=st["template"], terminal=(i == n - 1))
        ids = list(states)
        for a, b in zip(ids, ids[1:]):
            states[a].transitions = [Transition(to=b)]
        return cls(obj.get("id", "legacy"), obj.get("name", obj.get("id", "legacy")), ids[0] if ids else "", states, obj.get("intent_action"))

    # ---- execução ----
    def next_state(self, current: State, variables: Mapping[str, str]) -> State | None:
        if current.terminal:
            return None
        for t in current.transitions:
            if t.matches(variables):
                return self.states[t.to]
        return None


def _validate_guard(w: dict, errs: list, where: str) -> None:
    if not isinstance(w, dict):
        errs.append(f"{where}: guarda 'when' deve ser objeto")
        return
    if w.get("op", "nonempty") not in _GUARD_OPS:
        errs.append(f"{where}: op inválida {w.get('op')!r} (use {sorted(_GUARD_OPS)})")
    if w.get("op") in ("eq", "contains") and "val" not in w:
        errs.append(f"{where}: guarda eq/contains exige 'val'")


def validate(obj: dict) -> list[str]:
    """Devolve a lista COMPLETA de violações (vazia = válida)."""
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["raiz deve ser objeto"]
    if not obj.get("id"):
        errs.append("faltando 'id'")
    if not obj.get("name") and obj.get("steps") is None:
        errs.append("faltando 'name' (ou use schema legado com 'steps')")
    if "steps" in obj:  # legado: templates obrigatórios
        for i, st in enumerate(obj["steps"] or []):
            if not st.get("template"):
                errs.append(f"steps[{i}]: faltando 'template'")
        return errs
    states = obj.get("states")
    if not states:
        return errs + ["faltando 'states' (não vazio)"]
    ids = set()
    for s in states:
        sid = s.get("id", "?")
        if sid in ids:
            errs.append(f"states[{sid}]: id duplicado")
        ids.add(sid)
        if not s.get("prompt"):
            errs.append(f"states[{sid}]: faltando 'prompt'")
        for t in s.get("transitions", []):
            _validate_guard(t.get("when", {}), errs, f"states[{sid}]")
    initial = obj.get("initial")
    if initial not in ids:
        errs.append(f"initial {initial!r} não existe em states")
    if not any(s.get("terminal") for s in states):
        errs.append("nenhum estado terminal — conversa não termina")
    for s in states:
        for t in s.get("transitions", []):
            if t.get("to") not in ids:
                errs.append(f"states[{s.get('id','?')}]: transição para estado inexistente {t.get('to')!r}")
        if s.get("on_error") and s["on_error"] not in ids:
            errs.append(f"states[{s.get('id','?')}]: on_error inexistente {s['on_error']!r}")
    return errs


def load(obj: dict) -> Fsm:
    if "steps" in obj:
        errors = validate(obj)
        if errors:
            raise FsmError("; ".join(errors))
        return Fsm.from_legacy_steps(obj)
    return Fsm.from_dict(obj)
