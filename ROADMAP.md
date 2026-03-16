# claude-publish-agent — Product Roadmap

> Maintained by claude-roadmap-skill. Last updated: 2026-03-15.

---

## Current Roadmap

### Current State Snapshot

**What works:** CLI publishes markdown to Medium via GitHub Gist import or legacy API token. `/publish` skill scaffolds content kits and guides the publishing workflow in Claude Code. Content kit convention (`publish/` directory with style-guide.md + SVG header) is live across all four suite repos. 31 tests passing.

**What's fragile:** Medium-only. The tool's value is tied to a single platform whose API is closed to new users. The Gist import workaround works but adds a manual step.

### ICP & Jobs-to-be-Done

**Who this is for:** Solo developers and small teams using Claude Code who publish technical content to build audience and credibility around their projects.

**Core jobs:**
1. "Get my content from where I write it (terminal) to where my audience reads it — without context-switching"
2. "Keep my published content visually consistent and on-brand across platforms"
3. "Adapt one piece of content for different platforms without manual reformatting"
4. "Know what I've published, where, and when — without checking each platform"

### Opportunities — Prioritized

#### Tier 1 — Ship Next

| # | Feature | Job it solves | Why now |
|---|---------|--------------|---------|
| 1 | **LinkedIn Adapter** | "Get it in front of my professional network" | #1 channel for ICP; GTM series needs it; OAuth2 is why we chose Python |
| 2 | **Publishing Log** | "What did I publish, where, and when?" | Table stakes for multi-platform; tracks history at `~/.config/claude-publish/publish-log.json` |
| 3 | **Dev.to Adapter** | "Reach developers where they already read" | Completes the "big three" (Medium + LinkedIn + Dev.to); clean REST API, accepts markdown natively |

#### Tier 2 — High Value, Plan Next

| # | Feature | Job it solves | Why it matters |
|---|---------|--------------|----------------|
| 4 | **Cross-Post Command** | "Publish everywhere in one command" | Changes value prop from "publish" to "distribute" — the force multiplier feature |
| 5 | **Platform-Adaptive Formatting** | "Handle each platform's quirks for me" | Removes the #1 reason people don't cross-post: manual reformatting |
| 6 | **Content Drafting Assistance** | "Help me write on-brand content" | The AI-native differentiator — no other CLI helps you *write*, not just publish |

#### Tier 3 — Strategic / Longer Horizon

| # | Feature | Why |
|---|---------|-----|
| 7 | **Hashnode & Substack Adapters** | Expands platform reach; one new file + one registry line each |
| 8 | **Content Series Management** | The GTM plan has a 13-post series — managing that across 3 platforms is painful |
| 9 | **Scheduled Publishing Queue** | Consistent cadence builds audience; a queue enforces it |
| 10 | **Analytics Pull** | Closes the feedback loop — publishing without measurement is guessing |

### Recommended Sequencing

```
v0.1.0 (shipped) → LinkedIn → Publishing Log → Dev.to → Cross-Post
                                                          ↓
                                              Platform-Adaptive Formatting
                                                          ↓
                                              Content Drafting Assistance
                                                          ↓
                                              Series Management → Queue → Analytics
```

### Open Questions

1. **LinkedIn OAuth2 scope:** Does the LinkedIn API allow posting articles (long-form) via OAuth2 for individual developers, or only organization pages? Need to verify API access tier.
2. **Canonical URL strategy:** When cross-posting, which platform gets the canonical URL? User preference, or default to the first platform published?
3. **Content Drafting scope:** Should `/publish draft` generate a full post or just a structured outline? Full post risks being generic; outline lets the user steer.
4. **Dev.to API key availability:** Confirm Dev.to still issues API keys to individual developers (last checked: early 2026).

### OKR

**Objective:** Make claude-publish-agent the default way Claude Code users distribute technical content.

| Key Result | Target | Current |
|---|---|---|
| Platforms supported | 3 (Medium, LinkedIn, Dev.to) | 1 (Medium) |
| Commands available | 8+ (per-platform + cross-post + log + draft) | 4 (gist, medium, setup, status) |
| GTM series posts published via tool | 13 | 0 |
| Content kit adoption across suite repos | 4/4 | 4/4 |

---

## Revision History

### [2026-03-15] Initial roadmap — 10 features across 3 tiers

**Change Type:** `snapshot`
**Triggered by:** `planning-session`
**Items Affected:** All

#### What Changed
Created initial product roadmap with Toni (PMM) framing each feature around the job it solves for the ICP. Established three tiers of priority based on user value and GTM urgency.

#### Why
v0.1.0 shipped with Medium-only support. The tool needs multi-platform reach to deliver on its core promise ("publish from terminal") and to unblock the 13-post GTM content series for claude-team-cli.

#### Open Questions Resolved / Added
- **Added:** LinkedIn OAuth2 scope verification needed
- **Added:** Canonical URL strategy for cross-posting
- **Added:** Content drafting scope (full post vs. outline)
- **Added:** Dev.to API key availability confirmation
