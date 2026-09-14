from apps.core.fsm import load
from apps.core.ooda import OodaRunner


def test_orient_injeta_contexto_no_prompt():
    obj = {"id": "o", "name": "O", "initial": "a", "states": [
        {"id": "a", "prompt": "ctx={{context}} q={{input}}", "terminal": True}]}
    fsm = load(obj)
    llm = lambda p: p.upper()
    res = OodaRunner(fsm, llm, context_provider=lambda inp, vars: "RAG-DOC").run("pergunta")
    assert "RAG-DOC" in res.final_output
    assert res.trace[0].orient == "RAG-DOC"
    assert res.trace[0].act == "terminal"


def test_trace_registra_as_quatro_fases():
    obj = {"id": "t", "name": "T", "initial": "a", "states": [
        {"id": "a", "prompt": "p1 {{input}}", "transitions": [{"to": "b"}]},
        {"id": "b", "prompt": "p2 {{prev}}", "terminal": True}]}
    res = OodaRunner(load(obj), lambda p: "x").run("in")
    assert len(res.trace) == 2
    assert res.trace[0].act.startswith("transition:")
    assert res.trace[-1].act == "terminal"


def test_intent_do_estado_propaga_no_resultado():
    obj = {"id": "i", "name": "I", "initial": "a", "states": [
        {"id": "a", "prompt": "resume {{input}}", "intent_action": "android.intent.action.SEND", "terminal": True}]}
    res = OodaRunner(load(obj), lambda p: "ok").run("txt")
    assert res.intent_action == "android.intent.action.SEND"
