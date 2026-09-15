import glob
import re
import yaml


def test_regras_versionadas_sao_validas_e_bloqueiam():
    rules = sorted(glob.glob("hooks/rules/*.md"))
    assert len(rules) >= 5
    for path in rules:
        text = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        assert m, f"{path}: sem frontmatter"
        fm = yaml.safe_load(m.group(1))
        assert fm["enabled"] is True
        assert fm["name"] and re.fullmatch(r"[a-z0-9\-]+", fm["name"])
        assert fm["event"] in {"bash", "file", "stop", "prompt", "all"}
        if "warn" not in fm["name"]:
            assert fm.get("action") == "block", f"{path}: regra de bloqueio precisa action: block"
        # patterns compilam
        if "pattern" in fm:
            re.compile(fm["pattern"])
        for c in fm.get("conditions", []):
            re.compile(c["pattern"])
