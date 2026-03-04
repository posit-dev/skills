# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A collection of Claude Skills published by Posit PBC. Skills are structured markdown files that teach Claude specialized workflows (e.g., Shiny app development, R package testing, GitHub PR workflows). There is no application code to build, compile, or deploy — the primary artifacts are Markdown files consumed directly by Claude's skill system.

## Utility Script

The only runnable utility is `count-skill-tokens.py`, which reports line and token counts for a skill:

```bash
# Requires uv
./count-skill-tokens.py shiny/shiny-bslib
# or
uv run count-skill-tokens.py r-lib/cli
```

Warns when `SKILL.md` exceeds **5,000 tokens / 500 lines**, or when the skill `description` frontmatter exceeds **100 tokens**.

## Directory Structure

```
<category>/
  README.md                   # Category-level notes (optional per skill)
  <skill-name>/
    SKILL.md                  # Required: skill definition with YAML frontmatter
    references/               # Optional: supplementary docs loaded on demand
      *.md
    scripts/                  # Optional: R or shell helpers
    templates/                # Optional: document templates
```

Do **not** create a `README.md` inside individual skill directories — documentation about a skill's design goes in the category README.

## SKILL.md Format

Every skill requires YAML frontmatter at minimum:

```yaml
---
name: your-skill-name        # kebab-case, matches directory name
description: >               # Claude reads this to decide when to activate the skill
  Clear description of what this skill does and when to trigger it.
  Keep under 100 tokens.
---
```

The body is instructions written **for Claude**, not end users — imperative, step-by-step, covering edge cases.

## Registering a New Skill

After creating the skill directory, add it to the appropriate plugin in `.claude-plugin/marketplace.json`:

```json
{
  "name": "open-source",
  "skills": [
    "./open-source/release-post",
    "./open-source/your-new-skill"   ← add here
  ]
}
```

If a skill spans multiple categories (like `brand-yml` for both Shiny and Quarto), add its path to multiple plugin `skills` arrays. The `source` field is always `"./"` (repo root).

## Skill Categories

| Category | Purpose |
|----------|---------|
| `posit-dev/` | General developer skills (code review, architecture docs) |
| `github/` | PR creation and review thread workflows |
| `open-source/` | R/Python package release and changelog workflows |
| `r-lib/` | R package development with the r-lib ecosystem |
| `shiny/` | Shiny app development |
| `quarto/` | Quarto document authoring |
| `brand-yml/` | Shared skill registered under both `shiny` and `quarto` plugins |

## Key Conventions

- **Progressive disclosure**: Put specialized or large reference content in `references/*.md` and instruct Claude to read those files only when needed. This keeps the main `SKILL.md` within token limits.
- **R scripts**: Use a shebang (`#!/usr/bin/env Rscript`), include inline usage docs, check for required packages at startup, and exit non-zero on error.
- **Testing**: Install locally via `cp -r <category>/<skill> ~/.config/claude-code/skills/` and verify Claude activates the skill in Claude Code.
