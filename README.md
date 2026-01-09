# Posit Claude Skills

A collection of Claude Skills from Posit!

Claude Skills extend Claude's capabilities with specialized knowledge and workflows. Skills are automatically activated by Claude based on your task and can be used in Claude.ai, Claude Code, or via the Claude API. Learn more at the [Claude Skills documentation](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

## Available Skills

### Open Source

Open Source skills support internal open-source package workflows.

- **[release-post](./open-source/release-post/)** - Create professional package release blog posts following Tidyverse or Shiny blog conventions, with support for both R and Python packages

### R Package Development

R package development skills for working with the r-lib ecosystem and modern R package workflows.

- **[testing-r-packages](./r-lib/testing-r-packages/)** - Best practices for writing R package tests using testthat 3+, including test structure, expectations, fixtures, snapshots, mocking, and BDD-style testing

### Shiny

Skills for Shiny app development in both R and Python.

- **[brand-yml](./brand-yml/)** - Create and apply brand.yml files for consistent styling across Shiny apps, with support for bslib (R) and ui.Theme (Python), including automatic brand discovery and theming functions for plots and tables

### Quarto

Skills for Quarto document creation and publishing.

- **[brand-yml](./brand-yml/)** - Create and apply brand.yml files for consistent styling across Quarto projects, supporting HTML documents, dashboards, RevealJS presentations, Typst PDFs, and websites with automatic brand discovery and theme layering
- **[authoring](quarto/README.md#quarto-authoring-skill)** - Comprehensive guidance for Quarto document authoring and R Markdown migration. Write new Quarto documents with best practices, convert R Markdown files, migrate bookdown/blogdown/xaringan/distill projects, and use Quarto-specific features like hashpipe syntax, cross-references, callouts, and extensions

## Installation

### Claude Code

#### Method 1: Add Marketplace

Add this repository as a plugin marketplace in Claude Code:

```
/plugin marketplace add posit-dev/skills
```

Then browse and install the skill categories you need through the Claude Code UI.

#### Method 2: Direct Installation

Install specific skill categories directly:

```
/plugin install open-source@posit-dev-skills
/plugin install r-lib@posit-dev-skills
/plugin install shiny@posit-dev-skills
/plugin install quarto@posit-dev-skills
```

Each command installs all skills in that category.

#### Method 3: Manual Installation

For customization or offline use:

1. Clone this repository:

   ```bash
   git clone https://github.com/posit-dev/skills.git
   cd skills
   ```

2. Copy individual skills to your Claude Code skills directory:

   ```bash
   cp -r open-source/release-post ~/.config/claude-code/skills/
   ```

3. Or install all skills from a category:
   ```bash
   for skill in open-source/*/; do
     cp -r "$skill" ~/.config/claude-code/skills/
   done
   ```

### Claude.ai

Skills can be uploaded to Claude.ai following the [Creating Custom Skills guide](https://support.claude.com/en/articles/12512198-creating-custom-skills).

### Claude API

Use the [Skills API](https://docs.claude.com/en/api/skills-guide) to programmatically load and manage skills in your applications.

## Using Skills

Once installed, Claude will automatically activate relevant skills based on your task. You don't need to explicitly invoke them.

For example, with the `release-post` skill installed:

```
You: Help me write a release post for dplyr 1.2.0

Claude: I'll help you create a release post. First, let me gather some information...
```

Claude will use the skill's knowledge to guide you through creating a properly formatted release post.

## Skill Categories

This repository organizes skills into categories to make it easier to find and install skills relevant to your work:

| Category        | Description                                             |
| --------------- | ------------------------------------------------------- |
| **open-source** | General open-source package development and maintenance |
| **r-lib**       | R package development with the r-lib ecosystem          |
| **shiny**       | Shiny app development and deployment (R and Python)     |
| **quarto**      | Quarto document creation and publishing                 |

<!-- Future category ideas

| **tidyverse** | Tidyverse-specific package development |
| **connect** | Posit Connect deployment and management |
-->

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on creating new skills.

**We highly recommend using Anthropic's [skill-creator](https://github.com/anthropics/skills) skill** to help you build high-quality skills. Skills should be grouped together by category, but the category groups are flexible. Feel free to propose new categories as needed.

## License

This repository is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

## Resources

- [Claude Skills Overview](https://www.anthropic.com/news/skills)
- [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Skills API Documentation](https://docs.claude.com/en/api/skills-guide)
- [Anthropic's Official Skills Repository](https://github.com/anthropics/skills)

## Support

If you have questions or encounter issues, check the [Claude Skills documentation](https://support.claude.com/en/articles/12512180-using-skills-in-claude) or [open an issue](https://github.com/posit-dev/skills/issues/new) on GitHub.

---

**Built with ❤️ + ☕ + 🤖 at Posit**
