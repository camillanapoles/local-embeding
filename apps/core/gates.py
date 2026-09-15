"""Gates fail-closed (S4) — nada executa sem gate verde.

Protocolo de evento (dict): {"kind": "llm_call"|"prompt_load"|"intent", ...}
Gates são chamados pelo OodaRunner (llm_call) e pelo CLI/TUI (prompt_load/intent).
Qualquer violação levanta GateError e a operação NÃO acontece.
"""
from __future__ import annotations

import time

from .fsm import validate


class GateError(Exception):
    """Gate bloqueou a operação (fail-closed)."""


class Budget:
    """Budget de execução: nº de chamadas, tokens estimados e prazo."""

    def __init__(self, max_calls: int = 32, max_tokens: int = 200_000, deadline_s: int = 180):
        self.max_calls = max_calls
        self.max_tokens = max_tokens
        self.deadline_s = deadline_s
        self.calls = 0
        self.tokens = 0
        self._t0 = time.monotonic()

    @classmethod
    def from_config(cls, cfg) -> "Budget":
        return cls(max_calls=cfg.max_calls, max_tokens=cfg.max_tokens, deadline_s=cfg.timeout_s)

    def check(self, event: dict) -> None:
        if event.get("kind") != "llm_call":
            return
        self.calls += 1
        self.tokens += len(event.get("prompt", "")) // 4  # estimativa ~4 chars/token
        if self.calls > self.max_calls:
            raise GateError(f"budget: {self.calls} chamadas > máximo {self.max_calls}")
        if self.tokens > self.max_tokens:
            raise GateError(f"budget: ~{self.tokens} tokens > máximo {self.max_tokens}")
        elapsed = time.monotonic() - self._t0
        if elapsed > self.deadline_s:
            raise GateError(f"budget: {elapsed:.0f}s > prazo {self.deadline_s}s")


class SchemaGate:
    """Prompt só roda se o dict passar no validate() da FSM (fail-closed)."""

    def __init__(self, obj: dict):
        self.obj = obj

    def check(self, event: dict) -> None:
        if event.get("kind") != "prompt_load":
            return
        errors = validate(self.obj)
        if errors:
            raise GateError("schema FSM inválida: " + "; ".join(errors))


class PolicyGate:
    """Intents: deny-all por default — só roda o que está na allowlist."""

    def __init__(self, allowlist: list[str]):
        self.allowlist = list(allowlist)

    def check(self, event: dict) -> None:
        if event.get("kind") != "intent":
            return
        intent = event.get("intent", "")
        if intent and intent not in self.allowlist:
            raise GateError(
                f"policy: intent {intent!r} fora da allowlist "
                f"({self.allowlist or 'VAZIA — deny-all'}). Configure EMB_INTENTS_ALLOWLIST."
            )
