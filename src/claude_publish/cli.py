"""CLI entry point for claude-publish."""

import subprocess
from pathlib import Path

import click
import requests

from claude_publish import __version__
from claude_publish import config
from claude_publish.markdown import extract_title
from claude_publish.platforms import get_platform
from claude_publish.platforms.medium import DEFAULT_TAGS


@click.group()
@click.version_option(version=__version__, prog_name="claude-publish")
def cli():
    """Publish markdown content to blogging platforms."""
    pass


@cli.group()
def setup():
    """Configure platform credentials."""
    pass


MEDIUM_SETUP_INSTRUCTIONS = """
To get a Medium integration token:

  1. Go to Medium.com → Settings → Security and apps → Integration tokens
  2. Enter a description (e.g., "claude-publish") and click "Get token"
  3. Copy the token and paste it below
"""


@setup.command("medium")
def setup_medium():
    """Set up Medium integration token."""
    # Check for legacy token
    legacy = config.check_legacy_medium_token()
    if legacy:
        click.echo("Found existing token at ~/.medium-token")
        if click.confirm("Migrate it to the new location?", default=True):
            path = config.save_token("medium", legacy)
            click.echo(f"Token saved to {path}")
            return

    # Check if already configured
    if config.is_configured("medium"):
        if not click.confirm("Medium is already configured. Replace token?", default=False):
            return

    click.echo(MEDIUM_SETUP_INSTRUCTIONS)
    token = click.prompt("Paste your Medium integration token", hide_input=True)

    if not token.strip():
        click.echo("Error: empty token.", err=True)
        raise SystemExit(1)

    path = config.save_token("medium", token)
    click.echo(f"Token saved to {path} (permissions: 600)")


@cli.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--publish", "publish_now", is_flag=True, help="Publish immediately (default: draft)")
@click.option("--tags", default=None, help="Comma-separated tags (max 5)")
def medium(file, publish_now, tags):
    """Publish a markdown file to Medium."""
    filepath = Path(file)
    publish_status = "public" if publish_now else "draft"

    # Load token
    token = config.get_token("medium")
    if not token:
        click.echo("Medium is not configured.", err=True)
        click.echo("Run 'claude-publish setup medium' to set up your token.", err=True)
        raise SystemExit(1)

    # Extract title
    try:
        title = extract_title(filepath)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    # Parse tags
    tag_list = [t.strip() for t in tags.split(",")] if tags else DEFAULT_TAGS

    # Authenticate
    platform = get_platform("medium")
    click.echo("Authenticating with Medium...")

    try:
        username = platform.authenticate(token)
    except (ValueError, requests.RequestException) as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(f"Authenticated as @{username}")

    # Publish
    content = filepath.read_text()
    click.echo()
    click.echo(f"  Title:  {title}")
    click.echo(f"  Status: {publish_status}")
    click.echo(f"  Tags:   {', '.join(tag_list)}")
    click.echo()

    try:
        result = platform.publish(title, content, tag_list, publish_status)
    except (ValueError, requests.RequestException) as e:
        click.echo(f"Publish failed: {e}", err=True)
        raise SystemExit(1)

    if publish_status == "draft":
        click.echo(f"Draft created: {result.url}")
        click.echo("Review your draft on Medium, then publish when ready.")
    else:
        click.echo(f"Published: {result.url}")


@cli.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--public", is_flag=True, help="Create a public gist (default: secret)")
@click.option("--description", "-d", default=None, help="Gist description")
def gist(file, public, description):
    """Create a GitHub Gist from a markdown file for Medium import.

    Creates a gist via `gh`, then prints the raw URL you can paste
    into Medium's "Import a story" tool.
    """
    filepath = Path(file)

    # Verify gh is available
    try:
        subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True, check=True, text=True,
        )
    except FileNotFoundError:
        click.echo("Error: 'gh' CLI not found. Install it: https://cli.github.com", err=True)
        raise SystemExit(1)
    except subprocess.CalledProcessError:
        click.echo("Error: 'gh' is not authenticated. Run 'gh auth login'.", err=True)
        raise SystemExit(1)

    # Extract title for description
    try:
        title = extract_title(filepath)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    desc = description or title

    # Create gist
    cmd = ["gh", "gist", "create", str(filepath), "--desc", desc]
    if public:
        cmd.append("--public")

    click.echo(f"Creating gist: {title}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        click.echo(f"Gist creation failed: {result.stderr.strip()}", err=True)
        raise SystemExit(1)

    gist_url = result.stdout.strip()

    # Build the raw URL for Medium import
    # gh returns https://gist.github.com/user/id
    # Medium needs a URL it can fetch — the gist URL itself works
    click.echo()
    click.echo(f"  Gist: {gist_url}")
    click.echo()
    click.echo("To import into Medium:")
    click.echo(f"  1. Go to Medium.com → Your stories → Import a story")
    click.echo(f"  2. Paste this URL: {gist_url}")
    click.echo(f"  3. Click Import, then review and publish")


@cli.command()
def status():
    """Show configured platforms."""
    configured = config.list_configured()
    if not configured:
        click.echo("No platforms configured.")
        click.echo("Run 'claude-publish setup medium' to get started.")
        return

    click.echo("Configured platforms:")
    for name in configured:
        click.echo(f"  ✓ {name}")
