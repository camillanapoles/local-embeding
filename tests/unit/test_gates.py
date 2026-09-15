import pytest

from apps.core.fsm import load
from apps.core.gates import Budget, GateError, PolicyGate, SchemaGate
from apps.core.ooda import OodaRunner


def _fsm_n(n):
    states = []
    for i in range(n):
        states.append({"id": f"s{i}", "prompt": f"p{i} {{{{input}}}}",
                       **({"terminal": True} if i == n - 1 else {"transitions": [{"to": f"s{i+1}"}]})})
    return load({"id": "n", "name": "N", "initial": "s0", "states": states})


def test_budget_bloqueia_excesso_de_chamadas():
    b = Budget(max_calls=2, max_tokens=10**9, deadline_s=10**6)
    gate = b.check({"kind": "llm_call", "prompt": "x"})
    b.check({"kind": "llm_call", "prompt": "x"})
    with pytest.raises(GateError, match="chamadas"):
        b.check({"kind": "llm_call", "prompt": "x"})


def test_budget_ignora_outros_eventos():
    b = Budget(max_calls=0, max_tokens=1, deadline_s=0)
    b.check({"kind": "intent", "intent": "x"})  # não conta


def test_ooda_com_gate_budget_fail_closed():
    fsm = _fsm_n(3)
    with pytest.raises(GateError):
        OodaRunner(fsm, lambda p: "x", gates=[Budget(max_calls=2, max_tokens=10**9, deadline_s=10**6)]).run("in")


def test_policy_deny_all_por_default():
    g = PolicyGate([])
    with pytest.raises(GateError, match="deny-all"):
        g.check({"kind": "intent", "intent": "android.intent.action.SEND"})


def test_policy_permite_allowlisted():
    g = PolicyGate(["android.intent.action.SEND"])
    g.check({"kind": "intent", "intent": "android.intent.action.SEND"})  # não levanta


def test_schema_gate_recusa_prompt_invalido():
    with pytest.raises(GateError, match="terminal"):
        SchemaGate({"id": "x", "name": "X", "initial": "a", "states": [{"id": "a", "prompt": "p"}]}).check(
            {"kind": "prompt_load"})
