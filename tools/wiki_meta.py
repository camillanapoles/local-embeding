#!/usr/bin/env python3
"""wiki_meta.py — reconstrói meta/ do vault .llm-wiki (emulação das ferramentas da extensão pi).

Uso:
  python tools/wiki_meta.py                  # rebuild registry/backlinks/index/log + evento rebuild
  python tools/wiki_meta.py --event "kind" "detalhe"   # anexa evento custom ao events.jsonl

Regras honradas: raw/ imutável (não tocado); meta/ gerado (registry.json, backlinks.json,
index.md, log.md); events.jsonl append-only (criado só se não existir).
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, ".llm-wiki", "wiki")
META = os.path.join(ROOT, ".llm-wiki", "meta")
EVENTS = os.path.join(META, "events.jsonl")

MD_LINK = re.compile(r"\[[^\]]*\]\((/[^)#]+?)(#[^)]*)?\)")
WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_page(path: str):
    rel = os.path.relpath(path, WIKI).replace(os.sep, "/")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm = {}
    if text.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip()
    title = ""
    h1 = re.search(r"^# (.+)$", text, re.M)
    if h1:
        title = h1.group(1).strip()
    links = set(MD_LINK.findall(x for x in [text])[0] if False else {m.group(1) for m in MD_LINK.finditer(text)})
    links |= {m.group(1).strip() for m in WIKI_LINK.finditer(text)}
    # normaliza wikilinks sem sufixo para página na própria árvore
    norm = set()
    for l in links:
        l = l.strip()
        if l.startswith("sources/SRC-"):
            l = "/sources/" + l.split("/")[-1].lower() + "-x"  # packet refs não são páginas
            continue
        norm.add(l)
    return {"id": rel, "path": rel, "type": fm.get("type", "page"), "title": title or rel,
            "created": fm.get("created"), "updated": fm.get("updated", fm.get("created")),
            "links": sorted(n for n in norm if not n.startswith("sources/SRC-")), "words": len(text.split())}


def main():
    os.makedirs(META, exist_ok=True)
    pages = []
    for dirpath, _, names in os.walk(WIKI):
        for n in sorted(names):
            if n.endswith(".md"):
                pages.append(parse_page(os.path.join(dirpath, n)))
    by_id = {p["id"]: p for p in pages}

    # backlinks: link target -> inbound pages (resolve /folder/page.md e folder/page)
    backlinks = {}
    for p in pages:
        for l in p["links"]:
            key = l.lstrip("/")
            if not key.endswith(".md"):
                key += ".md"
            if key in by_id:
                backlinks.setdefault(key, []).append(p["id"])
    backlinks = {k: sorted(set(v)) for k, v in sorted(backlinks.items())}

    with open(os.path.join(META, "registry.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_at": now(), "page_count": len(pages), "pages": pages}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(META, "backlinks.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_at": now(), "backlinks": backlinks}, f, ensure_ascii=False, indent=1)

    # index.md humano
    by_type = {}
    for p in pages:
        by_type.setdefault(p["type"], []).append(p)
    lines = [f"# Índice do wiki — gerado {now()} ({len(pages)} páginas)", ""]
    for t in sorted(by_type):
        lines.append(f"## {t} ({len(by_type[t])})")
        for p in sorted(by_type[t], key=lambda x: x["id"]):
            bl = len(backlinks.get(p["id"], []))
            lines.append(f"- [{p['title']}](../wiki/{p['id']}) — {p['id']} · {bl} backlink(s)")
        lines.append("")
    with open(os.path.join(META, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # events.jsonl append-only
    if len(sys.argv) >= 4 and sys.argv[1] == "--event":
        events = [{"ts": now(), "kind": sys.argv[2], "detail": sys.argv[3]}]
        with open(EVENTS, "a", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    if not os.path.exists(EVENTS):
        with open(EVENTS, "w", encoding="utf-8") as f:
            f.write(json.dumps({"ts": now(), "kind": "bootstrap", "detail": "vault criado (emulação manual llm-wiki)"}, ensure_ascii=False) + "\n")
    with open(EVENTS, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now(), "kind": "meta_rebuild",
                            "detail": f"{len(pages)} páginas, {sum(len(v) for v in backlinks.values())} arestas"}, ensure_ascii=False) + "\n")

    # log.md gerado de events
    with open(EVENTS, encoding="utf-8") as f:
        evs = [json.loads(l) for l in f if l.strip()]
    log = ["# Log de atividade (gerado de events.jsonl — não editar)", ""]
    log += [f"- {e['ts']} · **{e['kind']}** — {e['detail']}" for e in evs[-200:]]
    with open(os.path.join(META, "log.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")

    orphans = [p["id"] for p in pages if p["id"] not in backlinks and p["type"] not in ("source", "retro")]
    print(f"OK: {len(pages)} páginas · {len(backlinks)} com backlinks · orphans(não-source): {orphans}")


if __name__ == "__main__":
    main()
