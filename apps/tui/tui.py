#!/usr/bin/env python3
"""Local Embed TUI (Termux) — prompts FSM + chat + teste de endpoint + download de modelos.

Zero dependências (curses + urllib + json). Config por env:
  EMB_TUI_BASE  (default http://127.0.0.1:8080/v1)   EMB_TUI_MODEL (default qwen3-1.7b)
"""
import curses, json, os, subprocess, sys, urllib.request

BASE = os.environ.get("EMB_TUI_BASE", "http://127.0.0.1:8080/v1")
MODEL = os.environ.get("EMB_TUI_MODEL", "qwen3-1.7b")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PROMPTS_DIR = os.path.join(ROOT, "prompts")


def http_post(path, payload, timeout=300):
    req = urllib.request.Request(BASE.rstrip("/") + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def chat(prompt: str) -> str:
    d = http_post("/chat/completions", {"model": MODEL, "stream": False,
                                        "messages": [{"role": "user", "content": prompt}]})
    return d["choices"][0]["message"]["content"].strip()


def list_prompts():
    out = []
    if os.path.isdir(PROMPTS_DIR):
        for f in sorted(os.listdir(PROMPTS_DIR)):
            if f.endswith(".json"):
                try:
                    out.append(json.load(open(os.path.join(PROMPTS_DIR, f), encoding="utf-8")))
                except Exception:
                    pass
    return out


def render(template, vars_):
    for k, v in vars_.items():
        template = template.replace("{{" + k + "}}", v)
    return template


def getline(stdscr, row, prompt, default=""):
    curses.echo()
    stdscr.addstr(row, 2, prompt)
    win = stdscr.subwin(1, 60, row + 1, 2)
    win.addstr(0, 0, default, curses.A_DIM)
    stdscr.refresh()
    line = stdscr.getstr(row + 1, 2, 512).decode() or default
    curses.noecho()
    return line.strip()


def show_text(stdscr, title, text):
    stdscr.clear()
    stdscr.addstr(0, 0, f"── {title} ──  (setas/pgup/pgdn rolam, q volta)", curses.A_BOLD)
    pad = curses.newpad(max(len(text.splitlines()), 1) + 2, max(max(len(l) for l in text.splitlines() or [""]), 60))
    for i, l in enumerate(text.splitlines()):
        pad.addstr(i, 0, l)
    top = 0
    h = curses.LINES - 2
    while True:
        pad.refresh(top, 0, 1, 0, h, curses.COLS - 1)
        k = stdscr.getch()
        if k in (ord("q"), 27): return
        if k == curses.KEY_DOWN: top += 1
        if k == curses.KEY_UP: top = max(0, top - 1)
        if k == curses.KEY_NPAGE: top += h
        if k == curses.KEY_PPAGE: top = max(0, top - h)
        top = max(0, top)


def run_fsm(stdscr, fsm):
    stdscr.clear()
    inp = getline(stdscr, 1, "Entrada ({{input}}):")
    prev, out = "", inp
    for step in fsm.get("steps", []):
        prompt = render(step["template"], {"input": inp, "prev": prev})
        stdscr.addstr(6, 2, f"⏳ {step.get('label', step.get('id', '?'))}…")
        stdscr.refresh()
        try:
            out = chat(prompt); prev = out
        except Exception as e:
            show_text(stdscr, "ERRO", str(e)); return
    show_text(stdscr, fsm.get("name", "resultado"), out)
    if fsm.get("intent_action"):
        stdscr.addstr(8, 2, f"(intent declarada: {fsm['intent_action']} — dispare via APK)")


def create_prompt(stdscr):
    stdscr.clear()
    pid = getline(stdscr, 1, "id (kebab-case):")
    name = getline(stdscr, 3, "nome:")
    tpl = getline(stdscr, 5, "template (use {{input}} e {{prev}}):")
    obj = {"id": pid, "name": name, "steps": [{"id": "s1", "label": name, "template": tpl}]}
    path = os.path.join(PROMPTS_DIR, f"{pid}.json")
    json.dump(obj, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    show_text(stdscr, "salvo", f"{path}\n(sincronize a cópia em apps/android/.../assets/prompts/ se quiser no teclado)")


def test_endpoint(stdscr):
    stdscr.clear()
    try:
        req = urllib.request.Request(BASE.rstrip("/") + "/models")
        with urllib.request.urlopen(req, timeout=5) as r:
            models = [m.get("id") for m in json.loads(r.read().decode()).get("data", [])]
        txt = f"endpoint: {BASE}\nmodelos: {models}"
    except Exception as e:
        txt = f"FALHOU {BASE}: {e}"
    show_text(stdscr, "teste de endpoint", txt)


def download_models(stdscr):
    stdscr.clear()
    r = subprocess.run(["bash", os.path.join(ROOT, "scripts", "baixar-modelos.sh"), "--list"],
                       capture_output=True, text=True)
    show_text(stdscr, "modelos indicados (models.json)", r.stdout + "\n(baixe com: bash scripts/baixar-modelos.sh --id chat)")


def main(stdscr):
    curses.curs_set(0)
    menu = ["1) Executar prompt FSM", "2) Chat rápido", "3) Testar endpoint",
            "4) Modelos indicados (operador)", "5) Criar prompt FSM", "q) Sair"]
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Local Embed TUI — Termux", curses.A_BOLD)
        stdscr.addstr(1, 0, f"endpoint: {BASE}  modelo: {MODEL}", curses.A_DIM)
        for i, m in enumerate(menu):
            stdscr.addstr(3 + i, 2, m)
        stdscr.addstr(3 + len(menu) + 1, 2, "prompts em ./prompts/*.json (master)")
        stdscr.refresh()
        k = stdscr.getch()
        if k in (ord("q"), 27): break
        if k == ord("1"):
            ps = list_prompts()
            show_text(stdscr, "prompts", "\n".join(f"- {p['id']}: {p['name']}" for p in ps) or "(vazio)")
            pid = getline(stdscr, 1, "id do prompt:")
            fsm = next((p for p in ps if p["id"] == pid), None)
            if fsm: run_fsm(stdscr, fsm)
        elif k == ord("2"):
            q = getline(stdscr, 1, "pergunta:")
            try: show_text(stdscr, "resposta", chat(q))
            except Exception as e: show_text(stdscr, "ERRO", str(e))
        elif k == ord("3"): test_endpoint(stdscr)
        elif k == ord("4"): download_models(stdscr)
        elif k == ord("5"): create_prompt(stdscr)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke":
        print("ok: tui importavel,", len(list_prompts()), "prompts carregados")
        sys.exit(0)
    curses.wrapper(main)
