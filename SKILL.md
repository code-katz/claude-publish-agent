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

## Content Kit (publish/ directory)

The `publish/` directory at the project root is the **content kit** — it stores branding assets and style guidance that ensure published content is on-brand and consistent.

### Expected Structure

```
publish/
├── style-guide.md          # Colors, typography, image style, voice/tone
├── images/
│   └── {project}-header.svg  # SVG banner for README and blog posts (1280×320)
├── posts/                  # Blog post files (post-{NN}-{slug}.md)
├── boilerplate.md          # (optional) Standard footer, CTAs, about section
└── tags.json               # (optional) Default tags per platform
```

### Content Kit Detection

**Before every publish action**, check if the project has a `publish/` directory:

1. **If `publish/style-guide.md` exists:** Read it and use its guidance when the user asks you to draft, review, or format content for this project. Reference the color palette, typography, and image style when generating illustrations or diagrams.

2. **If `publish/` directory is missing or incomplete:** Walk the user through creating it before publishing. Use this flow:

#### Scaffolding Flow

When the content kit is missing, say:

```
This project doesn't have a content kit yet. The publish/ directory stores
your branding assets so content stays on-brand across posts.

Let's set one up. I need a few things:

1. **Project name** — What's the short name for this project?
2. **Tagline** — One line describing what it does
3. **Accent color** — Pick a hex color for your project's accent
   (or I can suggest one)
```

Then create:

**a) `publish/style-guide.md`** — Generate a style guide using this template structure:
- Brand identity (project name, short label, role)
- Color palette (charcoal #141413, warm white #faf9f5 as base, plus the user's accent color)
- Typography (Poppins headings, Lora body, JetBrains Mono for code/project names)
- GitHub README header spec (1280×320 SVG, dark background, monospace project name)
- Image style guidelines (flat vector, minimal, no gradients/shadows)
- Do's and Don'ts
- File naming convention

**b) `publish/images/{project}-header.svg`** — Generate the SVG header banner:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 320" width="1280" height="320">
  <rect width="1280" height="320" fill="#141413"/>
  <text x="640" y="155" text-anchor="middle" font-family="JetBrains Mono, Fira Code, Consolas, monospace" font-size="52" font-weight="600" fill="{ACCENT_COLOR}">{PROJECT_NAME}</text>
  <text x="640" y="205" text-anchor="middle" font-family="JetBrains Mono, Fira Code, Consolas, monospace" font-size="20" fill="#b0aea5">{TAGLINE}</text>
  <line x1="440" y1="240" x2="840" y2="240" stroke="{ACCENT_COLOR}" stroke-width="2" stroke-opacity="0.4"/>
</svg>
```

**c) `publish/posts/` directory** — Create it if missing. This is where blog post files live, using the short naming convention (`post-{NN}-{slug}.md`).

After creating the files, confirm:
```
Content kit created:
  publish/style-guide.md — your brand guidelines
  publish/images/{project}-header.svg — README banner
  publish/posts/ — blog post directory (use post-{NN}-{slug}.md naming)
  .gitignore — added publish/posts/ (drafts stay out of version control)

You can add this header to your README:
  <p align="center">
    <img src="publish/images/{project}-header.svg" alt="{project}" width="100%">
  </p>
```

### Using the Content Kit

When the content kit exists and the user asks you to:
- **Draft a blog post:** Follow the style guide's voice, tone, and formatting rules
- **Create illustrations:** Use the image style guidelines and color palette from the style guide
- **Generate a Medium/LinkedIn post:** Reference the style guide for consistent branding
- **Review content:** Check that colors, fonts, and image specs match the style guide

### Medium Formatting Conventions

When drafting or reviewing posts destined for Medium, apply these formatting rules:

- **Conversation dialogue as code:** In blog posts that show a conversation between the user and a Claude persona, wrap ALL dialogue text — both the user's prompts and the persona's responses — in backticks so they render as inline code on Medium. This creates a consistent "terminal/chat" visual for the entire conversation.
  - Speaker labels (`**Me:**`, `**River:**`, etc.) go on their own line as bold text — NOT inside backticks or blockquotes.
  - Each dialogue paragraph gets its own backtick-wrapped line, separated by a blank line from the speaker label.
  - Do NOT use blockquote (`>`) formatting for dialogue — blockquotes render differently from backtick code on Medium.
  - Tables, bullet lists, and other structured content within a response stay as regular markdown between backtick paragraphs.
  - Example:
    ```
    **Me:**

    `We're building a personal jet pack for consumers. I need to write the requirements for v1.`

    **River:**

    `Before we write requirements, I need to understand the problem. What specific user problem does a personal jet pack solve?`
    ```
- **Slash commands as code:** Always render slash commands in backticks: `/river`, `/akira`, `/devlog`.
- **CLI commands as code blocks:** Use fenced code blocks (triple backticks) for terminal commands, not inline code.
- **Project names as code:** Render project names like `claude-team-cli` in backticks throughout the post.

## Post File Naming Convention

When creating or organizing blog post files, use short, scannable filenames:

```
post-{NN}-{slug}.md
```

**Rules:**
- `{NN}` — two-digit sequence number (`00`, `01`, `02`, ...)
- `{slug}` — **1-2 words maximum**. Use the persona name, topic keyword, or short label. Not the full title.
- The full title lives inside the file as the `# H1` heading — never duplicate it in the filename.

**Examples:**
| Good | Bad |
|---|---|
| `post-00-intro.md` | `post-00-meet-my-claude-dev-team.md` |
| `post-01-river.md` | `post-01-river-what-problem-does-a-jet-pack-solve.md` |
| `post-05-auth.md` | `post-05-implementing-jwt-refresh-token-rotation.md` |
| `post-11-skills.md` | `post-11-tools-that-make-the-team-remember.md` |

When the user creates a new post, suggest a short filename. If they provide a long one, offer to shorten it.

### Posts Directory

Blog post files should live in `publish/posts/` — inside the content kit directory. If the user asks to create a new post and no `publish/posts/` directory exists, create it.

When creating `publish/posts/` (either during scaffolding or on first post creation), automatically add `publish/posts/` to the project's `.gitignore`. Blog drafts should not be committed to version control by default. If the `.gitignore` doesn't exist, create it.

---

## Workflow

### Step 1: Check Content Kit

Before anything else, check for `publish/style-guide.md` in the project root.
- If missing, run the scaffolding flow above
- If present, read it for context

### Step 1b: Lint Check

Verify that the project has a linter configured. Check for stack-appropriate lint configuration files:

- **Python**: `ruff.toml`, `pyproject.toml` with `[tool.ruff]`, `.flake8`
- **JavaScript/TypeScript**: `.eslintrc*`, `eslint.config.*`, `biome.json`, or a `lint` script in `package.json`
- **Swift/iOS**: `.swiftlint.yml`
- **Go**: `.golangci.yml`
- **Rust**: `clippy` configuration in `Cargo.toml`
- **General**: `.pre-commit-config.yaml`

If no linter is configured, flag it to the user before proceeding. Recommend: Ruff for Python, ESLint or Biome for JS/TS, SwiftLint for Swift, golangci-lint for Go, clippy for Rust. Frame it as a prerequisite, not an afterthought.

### Step 2: Identify the File

- If the user specifies a file path (e.g., `/publish posts/my-article.md`), use that file
- If the user says "publish this" in the context of a file they just created or edited, use that file
- If ambiguous, ask: "Which markdown file should I publish?"
- Verify the file exists and has an `# H1` title line before proceeding

### Step 3: Choose the Platform

Ask the user where they want to publish:

- **Medium** — Uses the gist-based import workflow (Medium's API is closed to new tokens)
- **LinkedIn** — Coming soon

If the user already specified the platform (e.g., "publish to Medium"), skip this step.

### Step 4: Preview and Confirm

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

### Step 5: Publish (Medium via Gist)

Run the gist command:

```bash
claude-publish gist <file.md>
```

This creates a secret GitHub Gist and returns a URL.

### Step 6: Report Result and Guide Import

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
- **Content kit is optional but recommended.** The tool works without it — the content kit adds brand consistency, not a hard dependency.
