"""Tests for token storage and configuration."""

import os
import stat

from claude_publish import config


def test_save_and_get_token(tmp_config_dir):
    config.save_token("medium", "test-token-123")
    assert config.get_token("medium") == "test-token-123"


def test_save_token_permissions(tmp_config_dir):
    path = config.save_token("medium", "secret")
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert mode == 0o600


def test_save_token_strips_whitespace(tmp_config_dir):
    config.save_token("medium", "  token-with-spaces  \n")
    assert config.get_token("medium") == "token-with-spaces"


def test_get_token_missing(tmp_config_dir):
    assert config.get_token("nonexistent") is None


def test_get_token_empty_file(tmp_config_dir):
    path = tmp_config_dir / "empty.token"
    path.write_text("")
    assert config.get_token("empty") is None


def test_is_configured(tmp_config_dir):
    assert config.is_configured("medium") is False
    config.save_token("medium", "token")
    assert config.is_configured("medium") is True


def test_list_configured(tmp_config_dir):
    assert config.list_configured() == []
    config.save_token("medium", "tok1")
    config.save_token("linkedin", "tok2")
    assert config.list_configured() == ["linkedin", "medium"]


def test_list_configured_skips_empty(tmp_config_dir):
    config.save_token("medium", "tok")
    (tmp_config_dir / "empty.token").write_text("")
    assert config.list_configured() == ["medium"]


def test_check_legacy_medium_token(tmp_path, monkeypatch):
    legacy_path = tmp_path / ".medium-token"
    legacy_path.write_text("legacy-tok\n")
    monkeypatch.setattr(config, "LEGACY_MEDIUM_TOKEN", legacy_path)
    assert config.check_legacy_medium_token() == "legacy-tok"


def test_check_legacy_medium_token_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "LEGACY_MEDIUM_TOKEN", tmp_path / "nope")
    assert config.check_legacy_medium_token() is None
