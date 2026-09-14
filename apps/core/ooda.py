"""OODA runner (S2) — ciclo Observe→Orient→Decide→Act por estado da FSM.

observe: consolida variáveis (+ input)
orient : context_provider opcional injeta {{context}} (ex.: RAG)
decide : render do prompt + LLM (passando pelos gates, se houver)
act    : grava saída, resolve transição/intent
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .fsm import Fsm, FsmError, render


@dataclass
class StepTrace:
    state: str
    observe: dict
    orient: str
    decide_prompt: str
    decide_output: str
    act: str  # "transition:<to>" | "terminal" | "error:<state>"


@dataclass
class RunResult:
    final_output: str
    outputs: list = field(default_factory=list)
    trace: list = field(default_factory=list)
    intent_action: str | None = None
    stopped_reason: str = "terminal"


class OodaRunner:
    def __init__(self, fsm: Fsm, llm: Callable[[str], str],
                 context_provider: Callable[[str, dict], str] | None = None,
                 gates: list | None = None, max_steps: int | None = None):
        self.fsm = fsm
        self.llm = llm
        self.context_provider = context_provider
        self.gates = gates or []
        self.max_steps = max_steps or (len(fsm.states) + 2)

    def _gate(self, event: dict) -> None:
        for g in self.gates:
            g.check(event)  # fail-closed: GateError propaga e encerra

    def run(self, text_input: str, extra_vars: dict | None = None) -> RunResult:
        variables = {"input": text_input, "prev": "", "context": ""}
        variables.update(extra_vars or {})
        current = self.fsm.states[self.fsm.initial]
        result = RunResult(final_output="", intent_action=self.fsm.intent_action)
        for _ in range(self.max_steps):
            # OBSERVE
            variables["state"] = current.id
            # ORIENT
            if self.context_provider:
                variables["context"] = self.context_provider(text_input, dict(variables))
            # DECIDE
            prompt = render(current.prompt, variables)
            self._gate({"kind": "llm_call", "state": current.id, "prompt": prompt, "variables": dict(variables)})
            try:
                output = self.llm(prompt)
            except Exception:
                if current.on_error:
                    nxt = self.fsm.states[current.on_error]
                    result.trace.append(StepTrace(current.id, dict(variables), variables["context"], prompt, "", f"error:{current.on_error}"))
                    current = nxt
                    continue
                raise
            variables["prev"] = output
            result.outputs.append(output)
            # ACT
            nxt = self.fsm.next_state(current, variables)
            if current.terminal or nxt is None:
                result.trace.append(StepTrace(current.id, dict(variables), variables["context"], prompt, output, "terminal"))
                result.final_output = output
                if current.intent_action:
                    result.intent_action = current.intent_action
                result.stopped_reason = "terminal"
                return result
            result.trace.append(StepTrace(current.id, dict(variables), variables["context"], prompt, output, f"transition:{nxt.id}"))
            if current.intent_action:
                result.intent_action = current.intent_action
            current = nxt
        raise FsmError(f"FSM não terminou em {self.max_steps} passos (loop de transições?)")
