# Contributing to Posit Agent Skills

Thank you for your interest in contributing to the Posit Agent Skills repository! This document provides guidelines for creating and submitting new skills.

## Quick Start

1. **Use the skill-creator skill**: We highly recommend using [Anthropic's skill-creator skill](https://github.com/anthropics/skills) to help you build high-quality skills
1. Check for duplicates: Search existing skills to avoid duplication
1. Follow our structure: Use the directory structure and format described below

## Creating a New Skill

### 1. Choose the Right Category

Determine which category your skill belongs to:

| Category | Description |
|----------|-------------|
| **posit-dev** | General-purpose developer skills (code review, architecture docs) |
| **open-source** | Open-source R/Python package workflows (releases, changelogs) |
| **r-lib** | R package development with the r-lib ecosystem |
| **shiny** | Shiny app development and deployment |
| **quarto** | Quarto document creation and publishing |
| **connect** | Posit Connect deployment and management |

**Prefer a category-based name prefix**: When a category has a natural short prefix, name your skill with it so skills are self-describing and unambiguous across categories. The prefix should echo the category (e.g., `r-lib` skills use `r-*` like `r-cli`, `r-testthat`; `shiny` skills could use `shiny-*`; `quarto` skills could use `quarto-*`; `connect` skills could use `connect-*`). This matters most when the bare name would be generic or ambiguous — a skill named `cli` or `lifecycle` doesn't signal that it's about an R package. If the category name already says it all or no clean prefix exists (e.g., `posit-dev`, `open-source`), a plain descriptive name is fine.

**When renaming a skill**, update every reference: the `name:` frontmatter, `marketplace.json`, the category and root READMEs, and cross-references in other skills. Then run `./find-stale-references.py` (see the repo root) to catch any stragglers — pass `--rename old=new` for renames not already in its default set, and note in the PR how users should migrate (plugin updates, or removing/reinstalling with `npx skills`).

Other ideas for categories include:

| Category | Description |
|----------|-------------|
| **tidyverse** | Tidyverse-specific package development |

Feel free to propose new categories if needed.

### 2. Skill Structure

Each skill should follow this structure:

```
category-name/
└── your-skill-name/
    ├── SKILL.md              # Required: Main skill file
    ├── references/           # Optional: Supporting documentation
    │   └── guide.md
    ├── scripts/              # Optional: Helper scripts
    │   ├── helper.sh
    │   └── use_package.R
    └── templates/            # Optional: Document templates
        └── template.md
```

**Note**: Do NOT create a README.md within individual skill directories. Documentation about skill organization, design principles, or resources should go in the skill category's README.md (e.g., `open-source/README.md`).

Runnable R scripts should start with a shebang line, include internal usage documentation, use minimal package dependencies, and error if required packages are missing.

```r
#!/usr/bin/env Rscript
# Add a package dependency to DESCRIPTION using usethis::use_package()
#
# Usage:
#   Rscript add_package.R <package> [<type>] [<min_version>]
#
# Arguments:
#   package: Name of the package to add as a dependency
#   type: Optional dependency type (Imports, Suggests, Depends, LinkingTo)
#         Default: "Imports"
#   min_version: Optional minimum version (e.g., "2.5.0" or "TRUE" for current)
#
# Examples:
#   Rscript add_package.R "ggplot2"
#   Rscript add_package.R "dplyr" "Suggests"
#   Rscript add_package.R "rlang" "Imports" "1.0.0"

args <- commandArgs(trailingOnly = TRUE)

# Check if usethis is installed
if (!requireNamespace("usethis", quietly = TRUE)) {
  cat("Error: usethis package is not installed\n")
  cat("Install it with: install.packages('usethis')\n")
  quit(status = 1)
}

# check and setup arguments (this would be more developed in practice)...
package <- args[1]
type <- if (length(args) >= 2) args[2] else "Imports"
min_version <- if (length(args) >= 3) args[3] else NULL

usethis::use_package(package, type, min_version)
```

### 3. SKILL.md Format

The `SKILL.md` file is the core of your skill. It must include YAML frontmatter:

```markdown
---
name: your-skill-name
description: >
  A clear, concise description of what this skill does and when to use it.
  Focus on the use cases and capabilities. The agent will read this to decide
  when to activate your skill.
---

# Skill Name

[Detailed instructions for the agent on how to execute this skill]

## When to Use This Skill

- Use case 1
- Use case 2
- Use case 3

## Instructions

[Step-by-step instructions the agent should follow]

## Examples

[Real-world examples showing the skill in action]

## Resources

- Links to relevant documentation
- Helper scripts
- Reference materials
```

### 4. Writing Effective Skill Instructions

**For the agent, not end users**: Write instructions for the agent to follow, not for human users. Think of it as teaching the agent how to help users.

**Be specific and actionable**: Provide clear, step-by-step instructions that the agent can follow autonomously.

**Include examples**: Show concrete examples of inputs, outputs, and workflows.

**Handle edge cases**: Document how the agent should handle errors, ambiguity, and special situations.

**Reference supporting files**: Use relative paths to reference other files in your skill directory:
```markdown
See `references/formatting-guide.md` for detailed formatting requirements.
```

### 5. Best Practices

- **Focus on real use cases**: Base your skill on actual needs, not hypothetical scenarios
- **Keep it focused**: One skill should do one thing well. If you find yourself adding many unrelated features, consider splitting into multiple skills
- **Provide comprehensive documentation**: Write clear agent-facing instructions in SKILL.md. Optionally document organization, design principles, or resources in your skill group's README.md (e.g., `{category-name}/README.md`)
- **Test across harnesses**: Verify your skill works in the harnesses you target — e.g., Posit Assistant and Claude Code
- **Use clear naming**: Skill names should be descriptive and use kebab-case. When reasonable, include a category-based prefix (e.g., `r-*` for `r-lib`, `shiny-*`, `quarto-*`, `connect-*`) — see [Choose the Right Category](#1-choose-the-right-category)
- **Document dependencies**: If your skill requires specific tools or packages, document them clearly
- **Include error handling**: Guide the agent on how to handle common errors
- **Declare harness assumptions**: If your skill assumes a specific coding harness or tools, note it in the `compatibility` frontmatter field and in the skill's description in the root README. Where possible, prefer harness-agnostic instructions; when a skill genuinely needs harness-specific behavior, put those instructions in a separate reference file and select it at runtime based on tool availability (see `posit-dev/implement/references/` for an example of this pattern)

### 6. Using the skill-creator Skill

We **strongly recommend** using [Anthropic's skill-creator skill](https://github.com/anthropics/skills) to build your skill. This skill provides:

- Guidance on effective skill structure
- Help with writing clear instructions
- Validation of your skill format
- Best practices and examples

To use the skill-creator:

1. Install the skill from Anthropic's repository
2. Start a conversation with your coding assistant about creating your skill
3. The agent will guide you through the process using skill-creator's expertise

## Adding Your Skill to the Repository

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/skills.git
cd skills
```

### 2. Create Your Skill Directory

```bash
mkdir -p category-name/your-skill-name
cd category-name/your-skill-name
```

### 3. Add Your Skill Files

Create your SKILL.md and any supporting files following the structure above.

### 4. Update marketplace.json

Add your skill to the appropriate category plugin in `.claude-plugin/marketplace.json`.

Skills are organized by category plugins. Find the plugin that matches your skill's category and add your skill path to its `skills` array:

```json
{
  "name": "category",
  "description": "Collection of skills for [category purpose]",
  "source": "./",
  "strict": false,
  "skills": [
    "./existing-category/existing-skill",
    "./your-category/your-skill-name"  // Add your skill here
  ]
}
```

**Example**: If you're adding a skill to the open-source category:

```json
{
  "name": "open-source",
  "description": "Collection of skills for general open-source package development and maintenance, including release post creation and changelog management",
  "source": "./",
  "strict": false,
  "skills": [
    "./open-source/release-post",
    "./open-source/your-new-skill"  // Your new skill
  ]
}
```

**If creating a new category**: Add a new plugin entry to the `plugins` array:

```json
{
  "name": "your-category",
  "description": "Collection of skills for [category purpose]",
  "source": "./",
  "strict": false,
  "skills": [
    "./your-category/your-skill-name"
  ]
}
```

### 5. Update the Skill Category README (Optional)

You may optionally document your skill in the skill category's README.md (e.g., `open-source/README.md`, `r-lib/README.md`). This is where you can add:

- Notes about your skill's organization or structure
- Design principles and architectural decisions
- Resources, references, or related documentation used

Not every skill needs to be listed or documented in the group README. Use this space when you have important context to share with future contributors or users.

If you're adding a **new category directory**, create a README.md with this structure:

```markdown
# Category Name Skills

Brief description of what skills in this category do.

## Skills

Brief notes about individual skills (optional - only document when needed):

- **[skill-name](./skill-name/)** - Organization notes, design principles, or key resources

## Common Use Cases

- Use case 1
- Use case 2
```

### 6. Test Your Skill

Before submitting:

1. **Install locally**:
   ```bash
   cp -r category-name/your-skill-name ~/.agents/skills/
   # or, for Posit Assistant specifically:
   cp -r category-name/your-skill-name ~/.posit/assistant/skills/
   ```

2. **Test with your coding harness**: Verify the agent activates your skill appropriately (e.g., in Posit Assistant or Claude Code)

3. **Test edge cases**: Try various inputs and scenarios

4. **Check formatting**: Ensure YAML frontmatter is valid and markdown is well-formatted

5. **Check token counts**: Run the token counter and review the output for warnings:
   ```bash
   ./count-skill-tokens.py category-name/your-skill-name
   # or
   uv run count-skill-tokens.py category-name/your-skill-name
   ```
   The script warns if `SKILL.md` exceeds **5,000 tokens / 500 lines**, or if the `description` frontmatter exceeds **100 tokens**. Address any warnings before submitting. Save the output — you'll include it in your PR.

### 7. Submit a Pull Request

Open a Pull Request on GitHub with:

- Clear description of what the skill does
- Test results showing it works
- Any dependencies or requirements
- Links to related issues (if applicable)

## Pull Request Guidelines

### Required Information

Your PR description should include:

- **Purpose**: What does this skill do?
- **Use cases**: When would someone use this skill?
- **Testing**: How did you test it? What scenarios did you try?
- **Dependencies**: Does it require any specific tools, packages, or configurations?
- **Documentation**: Is the skill well-documented for both the agent and users?
- **Token count**: Paste the full output of `count-skill-tokens.py` for your skill. This confirms the skill is within size limits and helps reviewers assess its footprint.


## Code of Conduct

This project follows Posit's Code of Conduct. By participating, you agree to:

- Be respectful and inclusive
- Welcome newcomers
- Give and receive constructive feedback gracefully
- Focus on what's best for the community
- Show empathy towards others

## Questions?

If you have questions about contributing:

1. Check the [Agent Skills specification](https://agentskills.io/specification.md)
2. Look at existing skills for examples
3. Open an issue to discuss your idea
4. Use the skill-creator skill for guidance

## Resources

- [Agent Skills specification](https://agentskills.io/specification.md)
- [Posit Assistant skills documentation](https://assistant.posit.co/docs/features/skills.md)
- [Anthropic's skill-creator](https://github.com/anthropics/skills)
- [Creating Custom Skills Guide](https://support.claude.com/en/articles/12512198-creating-custom-skills)

