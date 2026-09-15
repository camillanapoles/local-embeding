"""Scanner zero-hardcode (S4) — URLs/IPs/model-ids/secrets em código = falha.

Uso: python3 -m apps.core.hardcode_scan [caminhos...]
Default: apps/ scripts/ (código). Exclui: tests/, docs/, *.example, *.md, .llm-wiki/.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = {
    "url": re.compile(r"https?://[^\s\"\'`]+"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "model-id": re.compile(r"\b(?:gpt-|claude-|gemini-|text-embedding-)[\w.\-]+"),
    "secret": re.compile(r"(?i)(api[_\-]?key|secret|password)\s*[:=]\s*[\"\'][^\"\']{8,}[\"\']"),
}

EXCLUDE_PARTS = {"tests", "docs", ".llm-wiki", "node_modules", "build", "__pycache__"}
EXCLUDE_SUFFIX = {".md", ".example", ".toml", ".txt", ".json"}


def is_scannable(path: Path) -> bool:
    s = str(path)
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return False
    if path.suffix in EXCLUDE_SUFFIX:
        return False
    return path.suffix in {".py", ".kt", ".kts", ".sh", ".yml", ".yaml"}


def scan_file(path: Path) -> list[dict]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return findings
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, rx in PATTERNS.items():
            for m in rx.finditer(line):
                frag = m.group(0)
                findings.append({"file": str(path), "line": lineno, "kind": name, "match": frag[:60]})
    return findings


def scan(roots: list[str]) -> list[dict]:
    findings = []
    for root in roots:
        p = Path(root)
        paths = [p] if p.is_file() else sorted(p.rglob("*")) if p.is_dir() else []
        for f in paths:
            if f.is_file() and is_scannable(f):
                findings += scan_file(f)
    return findings


def main(argv: list[str]) -> int:
    roots = argv[1:] or ["apps", "scripts"]
    findings = scan(roots)
    for f in findings:
        print(f"HARDCODE {f['kind']}: {f['file']}:{f['line']} {f['match']}")
    if findings:
        print(f"\n✗ {len(findings)} ocorrências de hardcode — mova para env/backend.toml (zero hardcode)")
        return 1
    print("✓ zero hardcode em " + ", ".join(roots))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
