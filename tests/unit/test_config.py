import pytest

from apps.core.config import Config, ConfigError


def test_sem_env_falha_fail_closed_com_instrucao():
    with pytest.raises(ConfigError, match="EMB_BASE_URL"):
        Config.from_env(env={})


def test_toml_fornece_e_env_sobrescreve(tmp_path):
    toml = tmp_path / "backend.toml"
    toml.write_text(chr(10).join([
        "[harness]",
        'EMB_BASE_URL = "http://arquivo:9/v1"',
        'EMB_MODEL = "m-arq"',
        "[policy]",
        'EMB_INTENTS_ALLOWLIST = "android.intent.action.SEND"',
        "",
    ]), encoding="utf-8")
    cfg = Config.from_env(env={}, path=str(toml))
    assert cfg.base_url == "http://arquivo:9/v1"
    assert cfg.intents_allowlist == ["android.intent.action.SEND"]
    cfg2 = Config.from_env(env={"EMB_BASE_URL": "http://env:1/v1"}, path=str(toml))
    assert cfg2.base_url == "http://env:1/v1"


def test_allowlist_default_vazia_deny_all(tmp_path):
    cfg = Config.from_env(env={"EMB_BASE_URL": "http://x:1/v1", "EMB_MODEL": "m"})
    assert cfg.intents_allowlist == []
