"""Config externa (S3) — ZERO hardcode: tudo vem de env ou backend.toml.

Fail-closed: base_url/model são obrigatórios (erro claro ensinando a resolver);
allowlist de intents default VAZIA (deny-all) — liberar é decisão explícita.
Precedência: env > backend.toml > (nenhum default mágico).
"""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field


class ConfigError(Exception):
    pass


@dataclass
class Config:
    base_url: str
    model: str
    max_calls: int = 32
    max_tokens: int = 200_000
    timeout_s: int = 180
    intents_allowlist: list = field(default_factory=list)

    @classmethod
    def from_env(cls, env: dict | None = None, path: str | None = None) -> "Config":
        env = dict(os.environ if env is None else env)
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                data = tomllib.load(f)
            env = {**{k: str(v) if not isinstance(v, list) else ",".join(v) for k, v in data.get("harness", {}).items()},
                   **{k: str(v) if not isinstance(v, list) else ",".join(v) for k, v in data.get("policy", {}).items()},
                   **env}  # env sobrescreve arquivo
        missing = [k for k in ("EMB_BASE_URL", "EMB_MODEL") if not env.get(k)]
        if missing:
            raise ConfigError(
                f"config obrigatória ausente: {missing}. "
                "Defina EMB_BASE_URL/EMB_MODEL no ambiente ou backend.toml (veja backend.toml.example). Zero hardcode."
            )
        allow = [i.strip() for i in env.get("EMB_INTENTS_ALLOWLIST", "").split(",") if i.strip()]
        return cls(
            base_url=env["EMB_BASE_URL"].rstrip("/"),
            model=env["EMB_MODEL"],
            max_calls=int(env.get("EMB_MAX_CALLS", cls.max_calls)),
            max_tokens=int(env.get("EMB_MAX_TOKENS", cls.max_tokens)),
            timeout_s=int(env.get("EMB_TIMEOUT_S", cls.timeout_s)),
            intents_allowlist=allow,
        )
