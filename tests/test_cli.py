"""Tests for CLI commands."""

import responses
from click.testing import CliRunner

from claude_publish import config
from claude_publish.cli import cli
from claude_publish.platforms.medium import API_BASE


@responses.activate
def test_medium_publish_draft(tmp_path, tmp_config_dir):
    """End-to-end: publish a markdown file as a draft."""
    # Set up token
    config.save_token("medium", "test-token")

    # Create markdown file
    md = tmp_path / "post.md"
    md.write_text("# Test Title\n\nHello world.\n")

    # Mock Medium API
    responses.get(
        f"{API_BASE}/me",
        json={"data": {"id": "u1", "username": "will"}},
    )
    responses.post(
        f"{API_BASE}/users/u1/posts",
        json={"data": {"id": "p1", "url": "https://medium.com/@will/test-title"}},
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["medium", str(md)])

    assert result.exit_code == 0
    assert "Authenticated as @will" in result.output
    assert "Draft created: https://medium.com/@will/test-title" in result.output


def test_medium_no_token(tmp_path, tmp_config_dir):
    """Error when no token is configured."""
    md = tmp_path / "post.md"
    md.write_text("# Title\n\nBody.\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["medium", str(md)])

    assert result.exit_code == 1
    assert "Medium is not configured" in result.output


def test_medium_no_h1(tmp_path, tmp_config_dir):
    """Error when markdown has no H1."""
    config.save_token("medium", "token")
    md = tmp_path / "bad.md"
    md.write_text("## Only H2\n\nBody.\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["medium", str(md)])

    assert result.exit_code == 1
    assert "No H1 title found" in result.output


def test_status_none_configured(tmp_config_dir):
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert "No platforms configured" in result.output


def test_status_with_medium(tmp_config_dir):
    config.save_token("medium", "token")
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert "medium" in result.output


def test_setup_medium_interactive(tmp_config_dir):
    runner = CliRunner()
    result = runner.invoke(cli, ["setup", "medium"], input="my-secret-token\n")
    assert result.exit_code == 0
    assert "Token saved" in result.output
    assert config.get_token("medium") == "my-secret-token"
