---
name: publish
description: Publish markdown files to blogging platforms (Medium, LinkedIn). Use this skill whenever the user says "publish this", "publish to Medium", "/publish", "post this to Medium", "push this to my blog", or references publishing, posting, or sharing a markdown file to a blogging platform. Draft by default — always confirm before publishing live.
---

# Publish Skill

This skill publishes markdown files to blogging platforms using the `claude-publish` CLI tool.

## Prerequisites

The `claude-publish` CLI must be installed:

```bash
pipx install claude-publish-agent
```

At least one platform must be configured. Check with:

```bash
claude-publish status
```

If no platforms are configured, guide the user through setup:

```bash
claude-publish setup medium
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
- Verify the file exists before proceeding

### Step 2: Check Platform Configuration

Run `claude-publish status` to see which platforms are configured.

- If **no platforms** are configured, tell the user and offer to run setup:
  "No platforms are configured yet. Want me to run `claude-publish setup medium` to get you started?"
- If **one platform** is configured, use it automatically
- If **multiple platforms** are configured, ask which one to use

### Step 3: Preview and Confirm

Before publishing, show the user what will be published:

1. Read the file and extract the title (first `# H1` line)
2. Show a confirmation message:

```
Ready to publish to Medium:

  Title:  [extracted title]
  File:   [file path]
  Status: Draft (review on Medium before going live)
  Tags:   Claude, Claude Code, AI Development, Developer Tools, AI Agents

Proceed?
```

3. If the user wants custom tags, ask for them (comma-separated, max 5)
4. If the user explicitly asks to publish live (not as a draft), confirm with an extra warning:
   "This will publish immediately — it will be visible to readers right away. Are you sure?"

### Step 4: Publish

Run the appropriate command:

```bash
# Draft (default)
claude-publish medium <file.md>

# With custom tags
claude-publish medium <file.md> --tags "Tag1,Tag2,Tag3"

# Publish immediately (only when explicitly confirmed)
claude-publish medium <file.md> --publish
```

### Step 5: Report Result

On success, show the URL clearly:

- **Draft:** "Draft created at [URL]. Review your draft on Medium, then publish when ready."
- **Published:** "Published at [URL]."

On failure, show the error message from the CLI and suggest next steps (e.g., check token, check network).

## Important Notes

- **Always default to draft.** Never publish live unless the user explicitly asks and confirms.
- **Do not modify the markdown file.** Publish it as-is. If the user wants changes, they should edit the file first.
- **Tags are optional.** The CLI has sensible defaults. Only ask about tags if the user mentions them.
- **One file at a time.** Do not batch-publish multiple files without explicit instruction.
