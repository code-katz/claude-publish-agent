# claude-publish-agent

Publish markdown to blogging platforms from the command line and Claude Code.

## Install

```bash
pipx install claude-publish-agent
```

## Setup

### Medium

1. Go to [Medium Settings > Security and apps > Integration tokens](https://medium.com/me/settings/security)
2. Create a token
3. Run:

```bash
claude-publish setup medium
```

## Usage

```bash
# Publish as draft (default)
claude-publish medium post.md

# Publish immediately
claude-publish medium post.md --publish

# Custom tags (max 5)
claude-publish medium post.md --tags "AI,Productivity,Tools"

# Check configured platforms
claude-publish status
```

## Claude Code Skill

Install the `/publish` skill for Claude Code:

```bash
# Copy to global skills directory
mkdir -p ~/.claude/skills/publish
cp SKILL.md ~/.claude/skills/publish/SKILL.md
```

Or upload `publish.skill` via Claude.ai Project Settings.

Then in Claude Code:

```
/publish posts/my-article.md
```

## Supported Platforms

- **Medium** — via integration token
- **LinkedIn** — coming soon

## Development

```bash
git clone https://github.com/d6veteran/claude-publish-agent.git
cd claude-publish-agent
pipx install -e ".[dev]"
pytest tests/ -v
```
