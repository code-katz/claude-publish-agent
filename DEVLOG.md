# claude-publish-agent — Development Log

A living record of architectural decisions, milestones, key insights, and strategic direction.
Auto-maintained via [claude-devlog-skill](https://github.com/d6veteran/claude-devlog-skill). Entries are reverse-chronological.

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
