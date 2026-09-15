from pathlib import Path

from apps.core.hardcode_scan import scan, scan_file


def test_detecta_url_e_secret(tmp_path):
    f = tmp_path / "core.py"
    f.write_text('BASE = "https://api.exemplo.com/v1"\nKEY = "token: abcdefghijk"\n', encoding="utf-8")
    kinds = {d["kind"] for d in scan_file(f)}
    assert "url" in kinds


def test_arquivo_limpo_nao_gera_finding(tmp_path):
    f = tmp_path / "ok.py"
    f.write_text("import os\nBASE = os.environ[\"EMB_BASE_URL\"]\n", encoding="utf-8")
    assert scan_file(f) == []


def test_scan_exclui_tests_docs_example(tmp_path):
    (tmp_path / "tests").mkdir()
    t = tmp_path / "tests" / "test_x.py"
    t.write_text('URL = "https://exemplo.com"\n', encoding="utf-8")
    (tmp_path / "docs").mkdir()
    d = tmp_path / "docs" / "a.md"
    d.write_text("veja https://exemplo.com", encoding="utf-8")
    assert scan([str(tmp_path)]) == []
