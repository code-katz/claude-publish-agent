"""Shared test fixtures."""

import pytest
from pathlib import Path

from claude_publish import config as config_module


@pytest.fixture
def tmp_config_dir(tmp_path, monkeypatch):
    """Redirect config storage to a temp directory."""
    config_dir = tmp_path / ".config" / "claude-publish"
    config_dir.mkdir(parents=True)
    monkeypatch.setattr(config_module, "CONFIG_DIR", config_dir)
    return config_dir


@pytest.fixture
def sample_markdown(tmp_path):
    """Create a sample markdown file with an H1 title."""
    md = tmp_path / "post.md"
    md.write_text("# My Test Post\n\nHello world.\n")
    return md


@pytest.fixture
def sample_markdown_no_title(tmp_path):
    """Create a markdown file with no H1."""
    md = tmp_path / "no-title.md"
    md.write_text("## Only H2\n\nNo H1 here.\n")
    return md
