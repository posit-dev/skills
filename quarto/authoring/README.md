# Quarto Authoring Skill

Comprehensive guidance for Quarto document authoring and R Markdown migration.

## Overview

This skill provides best practices for writing Quarto documents (.qmd) and converting existing R Markdown projects to Quarto. It covers the full range of Quarto authoring features including code cells, cross-references, figures, tables, citations, callouts, diagrams, and more.

## When to Use This Skill

- Writing new Quarto documents with best practices.
- Converting R Markdown (.Rmd) files to Quarto (.qmd).
- Migrating bookdown, blogdown, xaringan, or distill projects.
- Understanding Quarto's cell options syntax (comment symbol + `|`).
- Setting up cross-references for figures, tables, sections, and equations.
- Using Quarto-specific features like callouts, divs, and spans.
- Configuring YAML frontmatter for documents and projects.
- Finding and using Quarto extensions.

## Quick Start

### Basic Document

```yaml
title: "My Document"
author: "Author Name"
date: today
format: html
```

### Code Cell Options Syntax

Quarto uses the language's comment symbol + `|` for cell options:

- R/Python: `#|`
- Mermaid: `%%|`
- Graphviz/DOT: `//|`

```r
#| label: fig-example
#| echo: false
#| fig-cap: "Example figure."

plot(1:10)
```

**Important:** Quarto options use dashes, not dots (e.g., `fig-cap` not `fig.cap`).

### Cross-References

```markdown
See @fig-example for the results.
```

### Callouts

```markdown
::: {.callout-note}
This is a note.
:::
```

## Reference Documentation

### Quarto Features

| Reference                                                   | Description                                      |
| ----------------------------------------------------------- | ------------------------------------------------ |
| [code-cells.md](references/code-cells.md)                   | Hashpipe syntax, execution options, code display |
| [cross-references.md](references/cross-references.md)       | Labels, prefixes, all reference types            |
| [figures.md](references/figures.md)                         | Figures, subfigures, layouts, lightbox           |
| [tables.md](references/tables.md)                           | Pipe tables, grid tables, styling                |
| [citations.md](references/citations.md)                     | Bibliography, CSL, footnotes                     |
| [callouts.md](references/callouts.md)                       | Callout types, appearance, collapsible           |
| [diagrams.md](references/diagrams.md)                       | Mermaid, Graphviz/DOT diagrams                   |
| [layout.md](references/layout.md)                           | Column classes, margin content                   |
| [shortcodes.md](references/shortcodes.md)                   | Built-in shortcodes                              |
| [conditional-content.md](references/conditional-content.md) | Format-specific content                          |
| [divs-and-spans.md](references/divs-and-spans.md)           | Fenced divs, spans, raw blocks                   |
| [yaml-frontmatter.md](references/yaml-frontmatter.md)       | Document and project YAML                        |
| [extensions.md](references/extensions.md)                   | Using and finding extensions                     |

### Migration Guides

| Reference                                                     | Description                |
| ------------------------------------------------------------- | -------------------------- |
| [conversion-rmarkdown.md](references/conversion-rmarkdown.md) | R Markdown to Quarto       |
| [conversion-bookdown.md](references/conversion-bookdown.md)   | bookdown to Quarto         |
| [conversion-xaringan.md](references/conversion-xaringan.md)   | xaringan to RevealJS       |
| [conversion-distill.md](references/conversion-distill.md)     | distill to Quarto          |
| [conversion-blogdown.md](references/conversion-blogdown.md)   | blogdown to Quarto website |

## External Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Community Extensions List](https://m.canouil.dev/quarto-extensions/)

## Authors

- [Mickaël CANOUIL](https://github.com/mcanouil)
