"""Tests for CLI commands."""

from unittest.mock import patch, MagicMock

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


@patch("claude_publish.cli.subprocess.run")
def test_gist_creates_secret_gist(mock_run, tmp_path):
    """Gist command creates a secret gist and prints import instructions."""
    # Mock gh auth status (success)
    auth_result = MagicMock(returncode=0)
    # Mock gh gist create
    gist_result = MagicMock(
        returncode=0,
        stdout="https://gist.github.com/code-katz/abc123\n",
        stderr="",
    )
    mock_run.side_effect = [auth_result, gist_result]

    md = tmp_path / "post.md"
    md.write_text("# My Blog Post\n\nContent here.\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["gist", str(md)])

    assert result.exit_code == 0
    assert "https://gist.github.com/code-katz/abc123" in result.output
    assert "Import a story" in result.output

    # Verify --public was NOT passed (secret by default)
    gist_cmd = mock_run.call_args_list[1][0][0]
    assert "--public" not in gist_cmd


@patch("claude_publish.cli.subprocess.run")
def test_gist_public_flag(mock_run, tmp_path):
    """--public flag is passed through to gh."""
    auth_result = MagicMock(returncode=0)
    gist_result = MagicMock(returncode=0, stdout="https://gist.github.com/u/123\n", stderr="")
    mock_run.side_effect = [auth_result, gist_result]

    md = tmp_path / "post.md"
    md.write_text("# Public Post\n\nContent.\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["gist", "--public", str(md)])

    assert result.exit_code == 0
    gist_cmd = mock_run.call_args_list[1][0][0]
    assert "--public" in gist_cmd


@patch("claude_publish.cli.subprocess.run")
def test_gist_gh_not_authenticated(mock_run, tmp_path):
    """Error when gh is not authenticated."""
    import subprocess
    mock_run.side_effect = subprocess.CalledProcessError(1, "gh")

    md = tmp_path / "post.md"
    md.write_text("# Title\n\nBody.\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["gist", str(md)])

    assert result.exit_code == 1
    assert "not authenticated" in result.output
