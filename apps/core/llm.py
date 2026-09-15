"""Cliente LLM do core — OpenAI-compat via urllib (zero dependências, zero hardcode)."""
from __future__ import annotations

import json
import urllib.request


class LlmHttpError(Exception):
    pass


def make_llm(base_url: str, model: str, timeout_s: int = 180):
    """Devolve callable(prompt)->resposta apontando para {base_url}/chat/completions."""
    url = base_url.rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    url += "/chat/completions"

    def llm(prompt: str) -> str:
        payload = json.dumps({"model": model, "stream": False,
                              "messages": [{"role": "user", "content": prompt}]}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as r:
                data = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            raise LlmHttpError(f"HTTP {e.code}: {e.read().decode(errors='replace')[:200]}")
        return data["choices"][0]["message"]["content"].strip()

    return llm
