"""E2E (S7) — conversa FSM completa contra um endpoint OpenAI-compat STUB em HTTP real.

Cenários negativos = o cerne do gate-driven: budget estourado bloqueia, intent fora
da allowlist bloqueia, schema inválida não roda. Nada de LLM de verdade — stub local.
"""
import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)


class StubHandler(BaseHTTPRequestHandler):
    replies = ["RESPOSTA-UM", "RESPOSTA-DOIS"]
    calls = []

    def do_POST(self):
        self._req_body()  # consome o corpo
        idx = len(StubHandler.calls)
        StubHandler.calls.append(idx)
        reply = {"choices": [{"message": {"content": StubHandler.replies[min(idx, len(StubHandler.replies) - 1)]}}]}
        data = json.dumps(reply).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _req_body(self) -> bytes:
        n = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(n)

    def log_message(self, *a):
        pass


@pytest.fixture()
def stub_url():
    StubHandler.calls = []
    srv = HTTPServer(("127.0.0.1", 0), StubHandler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_port}/v1"
    srv.shutdown()


def _prompt_v2(tmp_path, **over):
    obj = {"id": "e2e", "name": "E2E", "initial": "a", "states": [
        {"id": "a", "prompt": "primeiro: {{input}}", "transitions": [{"to": "b"}]},
        {"id": "b", "prompt": "segundo: {{prev}}", "terminal": True},
    ]}
    obj.update(over)
    p = tmp_path / "p.json"
    p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    return str(p)


def _run_cli(args, env_extra):
    env = {**os.environ, "PYTHONPATH": ROOT, **env_extra}
    return subprocess.run([sys.executable, "-m", "apps.core", *args],
                          capture_output=True, text=True, env=env, cwd=ROOT, timeout=60)


def test_conversa_completa_happy_path(stub_url, tmp_path):
    p = _prompt_v2(tmp_path)
    r = _run_cli(["run", p, "pergunta"], {"EMB_BASE_URL": stub_url, "EMB_MODEL": "stub"})
    assert r.returncode == 0, r.stderr + r.stdout
    assert "RESPOSTA-UM" in r.stdout and "RESPOSTA-DOIS" in r.stdout
    assert len(StubHandler.calls) == 2  # dois estados, duas chamadas reais via HTTP


def test_budget_estourado_bloqueia_fail_closed(stub_url, tmp_path):
    p = _prompt_v2(tmp_path)
    r = _run_cli(["run", p, "pergunta"],
                 {"EMB_BASE_URL": stub_url, "EMB_MODEL": "stub", "EMB_MAX_CALLS": "1"})
    assert r.returncode == 3
    assert "GATE BLOQUEOU" in r.stdout and "chamadas" in r.stdout
    assert len(StubHandler.calls) == 1  # parou na 2ª chamada — não estourou


def test_intent_fora_da_allowlist_nao_dispara(stub_url, tmp_path):
    p = _prompt_v2(tmp_path, intent_action="android.intent.action.DIAL")
    r = _run_cli(["run", p, "pergunta"],
                 {"EMB_BASE_URL": stub_url, "EMB_MODEL": "stub",
                  "EMB_INTENTS_ALLOWLIST": "android.intent.action.SEND"})
    assert r.returncode == 3
    assert "policy" in r.stdout and "DIAL" in r.stdout


def test_intent_na_allowlist_passa(stub_url, tmp_path):
    p = _prompt_v2(tmp_path, intent_action="android.intent.action.SEND")
    r = _run_cli(["run", p, "pergunta"],
                 {"EMB_BASE_URL": stub_url, "EMB_MODEL": "stub",
                  "EMB_INTENTS_ALLOWLIST": "android.intent.action.SEND"})
    assert r.returncode == 0 and "intent liberada" in r.stdout


def test_schema_invalida_falha_antes_de_chamar_llm(stub_url, tmp_path):
    bad = {"id": "ruim", "name": "R", "initial": "x", "states": [{"id": "a", "prompt": "p"}]}
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    r = _run_cli(["run", str(p), "q"], {"EMB_BASE_URL": stub_url, "EMB_MODEL": "stub"})
    assert r.returncode != 0
    assert StubHandler.calls == []  # fail-closed: LLM nem foi chamado
