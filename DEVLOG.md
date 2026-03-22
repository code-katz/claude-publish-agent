# claude-publish-agent — Development Log

A living record of architectural decisions, milestones, key insights, and strategic direction.
Auto-maintained via [claude-devlog-skill](https://github.com/code-katz/claude-devlog-skill). Entries are reverse-chronological.

---

## [2026-03-21] Moved posts/ to publish/posts/ and added Medium formatting conventions

**Category:** `feature`
**Tags:** `skill`, `content-kit`, `medium`, `formatting`
**Risk Level:** `low`
**Breaking Change:** `no`

### Summary
Relocated the blog posts directory from `posts/` to `publish/posts/` so posts live inside the content kit directory alongside the style guide and header assets. Added a Medium Formatting Conventions section to SKILL.md with rules for rendering prompts, slash commands, CLI commands, and project names in code formatting.

### Detail
- All references to `posts/` in SKILL.md updated to `publish/posts/` — scaffolding flow, posts directory section, and content kit confirmation output
- New "Medium Formatting Conventions" section added to SKILL.md with four rules: user prompts as inline code, slash commands as inline code, CLI commands as fenced code blocks, project names as inline code
- README updated: content kit tree now includes `posts/` directory, example command uses `publish/posts/` path

### Decisions Made
- **Posts inside publish/ over project root** — Posts are publishing artifacts, not source code. Nesting them under `publish/` keeps the content kit self-contained and makes `.gitignore` patterns cleaner.
- **Medium formatting rules in SKILL.md** — These conventions ensure consistent rendering on Medium specifically, where markdown interpretation differs from GitHub. Rules are guidance for Claude, not programmatic enforcement.

### Related
- Previous entry: [2026-03-16] post file naming convention
- Also applied: `claude-team-cli/.gitignore` updated to match

---

## [2026-03-16] Added post file naming convention and posts/ directory scaffolding to SKILL.md

**Category:** `feature`
**Tags:** `skill`, `naming-convention`, `content-kit`, `scaffolding`
**Risk Level:** `low`
**Breaking Change:** `no`

### Summary
Added a post file naming convention (`post-{NN}-{slug}.md` with 1-2 word slugs) to the publish skill so all projects using claude-publish-agent get consistent, scannable filenames. Updated the content kit scaffolding flow to create a `posts/` directory on first use.

### Detail
- New "Post File Naming Convention" section in SKILL.md defines the pattern: `post-{NN}-{slug}.md` where the slug is 1-2 words max (persona name, topic keyword, or short label). Full titles live in the H1 heading inside the file.
- Includes a good/bad examples table showing the difference (e.g., `post-01-river.md` vs. `post-01-river-what-problem-does-a-jet-pack-solve.md`).
- Skill now instructs Claude to suggest short filenames when users create posts and to offer to shorten long ones.
- Updated the content kit scaffolding flow to create a `posts/` directory alongside `publish/style-guide.md` and the header SVG.
- Applied the convention retroactively to `claude-team-cli/posts/` — renamed all 12 post files from long descriptive names to short slug format.

### Decisions Made
- **1-2 word slug, not full title** — Long filenames are hard to scan in file explorers and tab bars, and they duplicate information already in the H1 heading. The slug is a navigation aid, not a description.
- **Convention lives in SKILL.md, not a separate config** — The naming convention is guidance for Claude, not a programmatic rule. Putting it in the skill instructions means it applies to every project without requiring config files.
- **`posts/` directory created during scaffolding** — Rather than letting posts scatter through the repo root, the skill now creates `posts/` alongside the content kit. Consistent across projects.

### Related
- Applied to: `claude-team-cli/posts/` (12 files renamed)
- Content kit scaffolding: SKILL.md § Content Kit Detection → Scaffolding Flow

---

## [2026-03-15] Full CLI built, Medium API pivot to Gist workflow, content kit convention established

**Category:** `milestone`
**Tags:** `cli`, `medium`, `gist`, `content-kit`, `style-guide`, `platform-adapter`
**Risk Level:** `low`
**Breaking Change:** `no`

### Summary
Built the complete `claude-publish-agent` Python CLI with platform adapter pattern, discovered Medium's API is closed to new tokens since Jan 2025, pivoted to a GitHub Gist import workflow, and established the `publish/` content kit convention for on-brand publishing across projects.

### Detail
- Implemented full Python CLI distributed via `pipx install` with click, requests, and platform adapter pattern (ABC + registry)
- Medium adapter ports the bash prototype to Python: `GET /v1/me` for auth, `POST /v1/users/{id}/posts` for publishing
- Token storage at `~/.config/claude-publish/` with `chmod 600`, migration from legacy `~/.medium-token`
- 31 tests passing across config, markdown, Medium adapter, CLI integration, and gist commands
- Discovered Medium closed API to new integration tokens as of January 2025 — no new tokens can be generated
- Built `claude-publish gist` command as workaround: creates a secret GitHub Gist via `gh` CLI, user pastes URL into Medium's "Import a story" tool
- Established `publish/` directory convention as project-level content kit: `style-guide.md` + `{project}-header.svg`
- Updated `/publish` skill to detect and scaffold missing content kits — walks user through project name, tagline, and accent color
- Dogfooded the convention on `claude-publish-agent` itself with Muted Purple (`#8b7eb8`) accent

### Decisions Made
- **Python over bash** — Originally planned bash to match claude-team-cli. Pivoted to Python because LinkedIn (next platform) requires OAuth2 flows that are painful in bash. Click for CLI, requests for HTTP, pipx for distribution.
- **Platform adapter pattern over flat module** — `Platform` ABC with registry dict. Adding LinkedIn = one new file + one registry line. Plugin discovery via entry_points was rejected as overkill for 2-3 platforms.
- **Gist workflow over abandoning Medium** — Medium's API closure could have killed the project. Instead, `claude-publish gist` creates a secret Gist and the user pastes the URL into Medium's import tool. One extra step, but preserves canonical URLs and SEO.
- **`publish/` at project root over `.claude/publish/`** — More visible, matches the tool name, signals "this project has publishing assets." `.claude/publish/` was considered but rejected as too buried.
- **Muted Purple (`#8b7eb8`) for claude-publish-agent** — Completes the suite palette: Rust Orange (team-cli), Slate Blue (devlog), Sage Green (roadmap), Muted Purple (publish).
- **Content kit is optional** — The tool works without `publish/`. The content kit adds brand consistency but is not a hard dependency. Skill scaffolds it on first use if missing.

### Related
- Inception entry: [2026-03-15] Project inception
- Style guide reference: `claude-team-cli/publish/style-guide.md`
- Medium API closure: https://help.medium.com/hc/en-us/articles/213480228-API-Importing

---

## [2026-03-15] Project inception — scope and positioning decided

**Category:** `strategy`
**Tags:** `positioning`, `naming`, `scope`, `medium-api`
**Risk Level:** `low`
**Breaking Change:** `no`

### Summary
Decided to build claude-publish-agent as a CLI + Claude Code skill for publishing markdown content to Medium (and eventually other platforms). Name chosen over alternatives after evaluating positioning.

### Detail
- Originated from work on the claude-team-cli GTM content series (13 blog posts targeting LinkedIn users exploring Claude Code)
- Initial prototype exists as `claude-team-cli/posts/publish.sh` — a bash script that publishes markdown to Medium via their API using python3 for JSON handling and HTTP calls
- The prototype authenticates via a token stored at `~/.medium-token`, extracts the title from the first H1 in the markdown, applies default tags, and publishes as a draft
- Decided this should be a standalone project rather than a script embedded in claude-team-cli, so it can be used across any project

### Decisions Made
- **Name: `claude-publish-agent`** — chosen over `claude-blog-cli` and `claude-blog-agent`. "publish" is broader than "blog" (extensible to LinkedIn, Dev.to, Hashnode later). "agent" signals it does autonomous work (API calls, error handling) rather than just shaping Claude's behavior. Follows the `claude-*` namespace convention.
- **Architecture: CLI + companion skill** — same pattern as claude-team-cli. The CLI (`claude-publish`) handles the actual API work. A companion Claude Code skill triggers conversationally ("publish this to Medium", `/publish`).
- **Medium first** — Medium's API accepts markdown directly via `contentFormat: "markdown"`, which means no pandoc or HTML conversion needed. Other platforms can be added later.
- **Draft by default** — publishes as draft so the user reviews on Medium before going live. `--publish` flag for immediate publish.
- **Token stored at `~/.medium-token`** — simple file-based auth, `chmod 600`. No environment variables or config files needed for v1.

### Related
- Prototype: `claude-team-cli/posts/publish.sh`
- GTM context: `claude-team-cli/gtm.md` (gitignored — contains the 13-post content series plan)
- Blog post stubs: `claude-team-cli/posts/` (gitignored — 13 markdown files, Post 0 fully drafted, Posts 1-11 stubbed with TODO conversation prompts)
