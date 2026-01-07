# Quarto Skills

Skills for Quarto document creation and publishing.

## Overview

This category contains skills that help with creating, styling, and publishing Quarto documents, presentations, websites, and PDFs. Skills support all major Quarto output formats.

## Available Skills

- **[authoring](#quarto-authoring-skill)** - Comprehensive guidance for Quarto document authoring and R Markdown migration. Write new Quarto documents with best practices, convert R Markdown files, migrate bookdown/blogdown/xaringan/distill projects, and use Quarto-specific features like hashpipe syntax, cross-references, callouts, and extensions.
- **[brand-yml](../brand-yml/)** - Create and apply brand.yml files for consistent styling across Quarto projects. Supports HTML documents, dashboards, RevealJS presentations, Typst PDFs, websites, and more with automatic brand discovery and theme layering.

## Potential Skills

This category could include skills for:

- Publishing workflows
- Extension development
- Template creation
- Multi-format output
- Parameterized reports
- Website and book publishing
- Presentation design

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new skills to this category. We encourage you to use [Anthropic's skill-creator](https://github.com/anthropics/skills) when building new skills.

## Resources

- [Quarto](https://quarto.org/)
- [Quarto brand.yml docs](https://quarto.org/docs/authoring/brand.html)
- [brand.yml project](https://posit-dev.github.io/brand-yml/)
- [Quarto extensions](https://quarto.org/docs/extensions/)

---

## Skills

### Quarto Authoring Skill

Comprehensive guidance for Quarto document authoring and R Markdown migration.

This skill provides best practices for writing Quarto documents (.qmd) and converting existing R Markdown projects to Quarto. It covers the full range of Quarto authoring features including code cells, cross-references, figures, tables, citations, callouts, diagrams, and more.

#### When to Use This Skill

- Writing new Quarto documents with best practices.
- Converting R Markdown (.Rmd) files to Quarto (.qmd).
- Migrating bookdown, blogdown, xaringan, or distill projects.
- Understanding Quarto's cell options syntax (comment symbol + `|`).
- Setting up cross-references for figures, tables, sections, and equations.
- Using Quarto-specific features like callouts, divs, and spans.
- Configuring YAML front matter for documents and projects.
- Finding and using Quarto extensions.

#### Maintenance

- Review skill content when new Quarto versions are released.
- Check the [Quarto changelog](https://github.com/quarto-dev/quarto-cli/blob/main/news/) for breaking changes and new features.
- Cross-check syntax examples against [Quarto Documentation](https://quarto.org/).
- Update examples to reflect current best practices.
- Remove deprecated syntax or features.

#### Skills Reference Documentation

##### Quarto Features

| Reference                                                             | Description                                      |
| --------------------------------------------------------------------- | ------------------------------------------------ |
| [code-cells.md](authoring/references/code-cells.md)                   | Hashpipe syntax, execution options, code display |
| [cross-references.md](authoring/references/cross-references.md)       | Labels, prefixes, all reference types            |
| [figures.md](authoring/references/figures.md)                         | Figures, subfigures, layouts, lightbox           |
| [tables.md](authoring/references/tables.md)                           | Pipe tables, grid tables, styling                |
| [citations.md](authoring/references/citations.md)                     | Bibliography, CSL, footnotes                     |
| [callouts.md](authoring/references/callouts.md)                       | Callout types, appearance, collapsible           |
| [diagrams.md](authoring/references/diagrams.md)                       | Mermaid, Graphviz/DOT diagrams                   |
| [layout.md](authoring/references/layout.md)                           | Column classes, margin content                   |
| [shortcodes.md](authoring/references/shortcodes.md)                   | Built-in shortcodes                              |
| [conditional-content.md](authoring/references/conditional-content.md) | Format-specific content                          |
| [divs-and-spans.md](authoring/references/divs-and-spans.md)           | Fenced divs, spans, raw blocks                   |
| [yaml-front-matter.md](authoring/references/yaml-front-matter.md)     | Document and project YAML                        |
| [extensions.md](authoring/references/extensions.md)                   | Using and finding extensions                     |

##### Migration Guides

| Reference                                                               | Description                |
| ----------------------------------------------------------------------- | -------------------------- |
| [conversion-rmarkdown.md](authoring/references/conversion-rmarkdown.md) | R Markdown to Quarto       |
| [conversion-bookdown.md](authoring/references/conversion-bookdown.md)   | bookdown to Quarto         |
| [conversion-xaringan.md](authoring/references/conversion-xaringan.md)   | xaringan to RevealJS       |
| [conversion-distill.md](authoring/references/conversion-distill.md)     | distill to Quarto          |
| [conversion-blogdown.md](authoring/references/conversion-blogdown.md)   | blogdown to Quarto website |

#### External Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Quarto CLI Code](https://github.com/quarto-dev/quarto-cli)
- [Community Extensions List](https://m.canouil.dev/quarto-extensions/)

#### Authors

- [Mickaël CANOUIL](https://github.com/mcanouil)
