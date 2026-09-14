import pytest

from apps.core.fsm import FsmError, load, render, validate


def fake_llm(responses):
    calls = []
    def llm(prompt):
        calls.append(prompt)
        return responses[len(calls) - 1]
    return llm, calls


def test_legacy_steps_vira_fsm_linear():
    fsm = load({"id": "leg", "name": "Legado", "steps": [
        {"id": "a", "template": "primeiro {{input}}"},
        {"id": "b", "template": "segundo {{prev}}"},
    ]})
    llm, calls = fake_llm(["SAIDA1", "SAIDA2"])
    res = __import__("apps.core.ooda", fromlist=["OodaRunner"]).OodaRunner(fsm, llm).run("pergunta")
    assert res.outputs == ["SAIDA1", "SAIDA2"]
    assert "primeiro pergunta" in calls[0]
    assert "segundo SAIDA1" in calls[1]


def test_schema_v2_valida_e_rodar_com_guarda():
    obj = {
        "id": "rev", "name": "Revisão", "initial": "triagem",
        "states": [
            {"id": "triagem", "prompt": "problemas de {{input}}",
             "transitions": [
                 {"to": "curto", "when": {"var": "prev", "op": "contains", "val": "CURTO"}},
                 {"to": "longo"}]},
            {"id": "curto", "prompt": "resumo curto de {{prev}}", "terminal": True},
            {"id": "longo", "prompt": "detalhe de {{prev}}", "terminal": True},
        ],
    }
    assert validate(obj) == []
    fsm = load(obj)
    llm, _ = fake_llm(["tem CURTO aqui", "final curto"])
    res = __import__("apps.core.ooda", fromlist=["OodaRunner"]).OodaRunner(fsm, llm).run("codigo")
    assert res.final_output == "final curto"
    assert [t.state for t in res.trace] == ["triagem", "curto"]


def test_validate_rejeita_sem_terminal_e_transicao_fantasma():
    errs = validate({"id": "x", "name": "X", "initial": "a",
                     "states": [{"id": "a", "prompt": "p", "transitions": [{"to": "fantasma"}]}]})
    assert any("terminal" in e for e in errs)
    assert any("inexistente" in e for e in errs)


def test_validate_rejeita_sem_initial_e_prompt_vazio():
    errs = validate({"id": "x", "name": "X", "states": [{"id": "a", "terminal": True}]})
    assert any("initial" in e for e in errs)
    assert any("prompt" in e for e in errs)


def test_on_error_recupera_para_estado_de_erro():
    obj = {"id": "e", "name": "E", "initial": "a", "states": [
        {"id": "a", "prompt": "vai explodir", "on_error": "fallback",
         "transitions": [{"to": "b"}]},
        {"id": "b", "prompt": "nunca", "terminal": True},
        {"id": "fallback", "prompt": "recuperado: {{input}}", "terminal": True},
    ]}
    fsm = load(obj)
    state = {"boom": True}
    def llm(prompt):
        if state["boom"]:
            state["boom"] = False
            raise RuntimeError("llm fora")
        return "OK-RECOVER"
    res = __import__("apps.core.ooda", fromlist=["OodaRunner"]).OodaRunner(fsm, llm).run("entrada")
    assert res.final_output == "OK-RECOVER"


def test_render_substitui_variaveis():
    assert render("a {{x}} b {{y}}", {"x": "1", "y": "2"}) == "a 1 b 2"


def test_from_dict_recusa_schema_invalido():
    with pytest.raises(FsmError):
        load({"id": "z", "name": "Z", "initial": "nao-existe", "states": []})
