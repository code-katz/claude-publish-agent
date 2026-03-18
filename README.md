<p align="center">
  <img src="publish/claude-publish-agent-header.svg" alt="claude-publish-agent" width="100%">
</p>

![License: MIT](https://img.shields.io/badge/license-MIT-blue) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue) ![Works with Claude Code](https://img.shields.io/badge/works%20with-Claude%20Code-8A2BE2)

Publish markdown to blogging platforms from the command line and Claude Code.

## Install

```bash
pipx install claude-publish-agent
```

## Usage

### Publish to Medium (via GitHub Gist)

Medium's API is closed to new tokens. Instead, `claude-publish` creates a secret GitHub Gist and gives you a URL to paste into Medium's import tool.

```bash
# Create a gist and get the import URL
claude-publish gist post.md

# Then: Medium.com → Your stories → Import a story → paste URL
```

### Medium API (legacy token holders)

If you have a Medium integration token from before January 2025:

```bash
claude-publish setup medium
claude-publish medium post.md
claude-publish medium post.md --publish    # publish immediately
claude-publish medium post.md --tags "AI,Productivity"
```

### Check status

```bash
claude-publish status
```

## Claude Code Skill

Install the `/publish` skill for Claude Code:

```bash
mkdir -p ~/.claude/skills/publish
cp SKILL.md ~/.claude/skills/publish/SKILL.md
```

Or upload `publish.skill` via Claude.ai Project Settings.

Then in Claude Code:

```
/publish posts/my-article.md
```

## Content Kit

Each project can have a `publish/` directory with branding assets that the `/publish` skill uses to keep content on-brand:

```
publish/
├── style-guide.md          # Colors, typography, image style, voice/tone
├── {project}-header.svg    # SVG banner for README and blog posts
├── boilerplate.md          # (optional) Standard footer, CTAs
└── tags.json               # (optional) Default tags per platform
```

If the `/publish` skill detects a missing content kit, it walks you through creating one — just provide a project name, tagline, and accent color.

See this project's own [`publish/`](publish/) directory for an example.

## Supported Platforms

- **Medium** — via GitHub Gist import or legacy API token
- **LinkedIn** — coming soon

## Development

```bash
git clone https://github.com/code-katz/claude-publish-agent.git
cd claude-publish-agent
pipx install -e ".[dev]"
pytest tests/ -v
```
