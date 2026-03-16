# claude-publish-agent — Development Log

A living record of architectural decisions, milestones, key insights, and strategic direction.
Auto-maintained via [claude-devlog-skill](https://github.com/d6veteran/claude-devlog-skill). Entries are reverse-chronological.

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
