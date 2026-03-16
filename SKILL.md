---
name: publish
description: Publish markdown files to blogging platforms (Medium via GitHub Gist import, LinkedIn coming soon). Use this skill whenever the user says "publish this", "publish to Medium", "/publish", "post this to Medium", "push this to my blog", or references publishing, posting, or sharing a markdown file to a blogging platform.
---

# Publish Skill

This skill publishes markdown files to blogging platforms using the `claude-publish` CLI tool.

## Prerequisites

The `claude-publish` CLI must be installed:

```bash
pipx install claude-publish-agent
```

The `gh` CLI must be installed and authenticated (for GitHub Gist creation):

```bash
gh auth status
```

## Trigger Conditions

Activate this skill when the user:
- Says "/publish", "publish this", "publish to Medium", "post this to Medium"
- Says "push this to my blog", "share this on Medium"
- References publishing, posting, or sharing a markdown file to a blogging platform
- Has just finished writing or editing a blog post and wants to publish it

## Workflow

### Step 1: Identify the File

- If the user specifies a file path (e.g., `/publish posts/my-article.md`), use that file
- If the user says "publish this" in the context of a file they just created or edited, use that file
- If ambiguous, ask: "Which markdown file should I publish?"
- Verify the file exists and has an `# H1` title line before proceeding

### Step 2: Choose the Platform

Ask the user where they want to publish:

- **Medium** — Uses the gist-based import workflow (Medium's API is closed to new tokens)
- **LinkedIn** — Coming soon

If the user already specified the platform (e.g., "publish to Medium"), skip this step.

### Step 3: Preview and Confirm

Before publishing, show the user what will be published:

1. Read the file and extract the title (first `# H1` line)
2. Show a confirmation message:

```
Ready to publish to Medium:

  Title:  [extracted title]
  File:   [file path]
  Method: GitHub Gist → Medium Import

Proceed?
```

### Step 4: Publish (Medium via Gist)

Run the gist command:

```bash
claude-publish gist <file.md>
```

This creates a secret GitHub Gist and returns a URL.

### Step 5: Report Result and Guide Import

On success, show the gist URL and walk the user through the import:

```
Gist created: [URL]

To finish importing into Medium:
  1. Go to Medium.com → Your stories → Import a story
  2. Paste this URL: [URL]
  3. Click Import, then review and publish
```

On failure, show the error message from the CLI and suggest next steps.

## Medium API (Legacy Token Users)

If the user already has a Medium integration token (from before January 2025), they can use the direct API instead:

```bash
claude-publish setup medium
claude-publish medium <file.md>
```

This publishes directly as a draft without the gist step. Only offer this if the user mentions having an existing token.

## Important Notes

- **Do not modify the markdown file.** Publish it as-is. If the user wants changes, they should edit the file first.
- **One file at a time.** Do not batch-publish multiple files without explicit instruction.
- **Gists are secret by default.** Only use `--public` if the user explicitly asks.
