# Claude Tool Suite — Visual Style Guide

> **Applies to:** `claude-publish-agent` (part of the Claude Tool Suite)

---

## 1. Brand Identity

### 1.1 Suite Context

This project is part of the **Claude Tool Suite**, sharing a visual identity with:

| Project | Short Label | Accent Color | Role |
|---|---|---|---|
| `claude-team-cli` | **Team CLI** | Rust Orange `#d97757` | Multi-agent orchestration from the terminal |
| `claude-devlog-skill` | **Devlog Skill** | Slate Blue `#6a9bcc` | Structured development changelog skill |
| `claude-roadmap-skill` | **Roadmap Skill** | Sage Green `#788c5d` | Project planning and roadmap skill |
| `claude-publish-agent` | **Publish Agent** | Muted Purple `#8b7eb8` | Publish markdown to blogging platforms |

---

## 2. Color Palette

### 2.1 Primary Colors

| Name | Hex | Usage |
|---|---|---|
| **Charcoal** | `#141413` | Primary text, dark backgrounds |
| **Warm White** | `#faf9f5` | Light backgrounds, text on dark |
| **Mid Gray** | `#b0aea5` | Secondary text, borders, dividers |
| **Light Gray** | `#e8e6dc` | Subtle backgrounds, code blocks |

### 2.2 Project Accent

| Name | Hex | Usage |
|---|---|---|
| **Muted Purple** | `#8b7eb8` | Primary accent, CTAs, highlights |

### 2.3 Extended Palette (for illustrations)

| Name | Hex | Usage |
|---|---|---|
| **Soft Teal** | `#7ab5b0` | Secondary illustration color |
| **Warm Tan** | `#c4a882` | Background accents in illustrations |

---

## 3. Typography

| Context | Font | Fallback |
|---|---|---|
| **Headings** | Poppins (SemiBold 600) | Arial, Helvetica |
| **Body Text** | Lora (Regular 400) | Georgia, serif |
| **Code / Project Names** | JetBrains Mono | Fira Code, Consolas, monospace |

Project name rendered in monospace with accent color: `claude-publish-agent` in `#8b7eb8`.

---

## 4. GitHub README Header

- **Format:** SVG banner, 1280x320px
- **Style:** Dark background (`#141413`), project name in monospace accent color, tagline in `#b0aea5`
- **Location:** `publish/images/claude-publish-agent-header.svg`

```markdown
<p align="center">
  <img src="publish/images/claude-publish-agent-header.svg" alt="claude-publish-agent" width="100%">
</p>
```

---

## 5. Image Style

All illustrations follow a **flat vector / minimal cartoon** style:

- Clean white or `#faf9f5` backgrounds
- Simple geometric shapes, rounded rectangles, soft edges
- Flat coloring — no shadows, no 3D effects, no gradients
- Outlined icons preferred (2px stroke weight)

### Prompt Template for Image Generation

```
Simple, clean flat vector illustration on a white (#faf9f5) background.
Minimal detail, soft muted colors (palette: #8b7eb8, #7ab5b0, #c4a882,
#141413). No text. No logos. Rounded shapes, 2px outlines, no gradients
or shadows. Suitable for a tech blog header.
```

---

## 6. Do's and Don'ts

### Do
- Use Muted Purple (`#8b7eb8`) as the primary accent consistently
- Keep illustrations simple
- Maintain generous whitespace
- Use monospace for project name references

### Don't
- Don't use gradients, drop shadows, or 3D effects
- Don't mix accent colors from other suite projects
- Don't use photography or realistic illustrations
- Don't add the Anthropic logo (independent community project)

---

## 7. File Naming Convention

```
{project-short-name}-{description}-{size}.{ext}
```

Examples:
- `publish-agent-header-1280x320.svg`
- `publish-agent-workflow-1200x675.png`

---

*Last updated: March 2026*
