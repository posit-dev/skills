---
name: quarto/authoring
description: >
  Comprehensive guidance for Quarto document authoring and R Markdown migration.
  Use this skill when: (1) Writing new Quarto documents (.qmd) with best practices,
  (2) Converting R Markdown (.Rmd) documents to Quarto, (3) Migrating bookdown,
  blogdown, xaringan, or distill projects to Quarto, (4) Understanding Quarto's
  code cell syntax with hashpipe (#|) options, (5) Setting up cross-references
  for figures, tables, sections, and equations, (6) Using Quarto-specific markdown
  features like callouts, divs, and spans, (7) Configuring YAML frontmatter for
  documents and projects, (8) Finding and using Quarto extensions.
---

# Quarto Authoring

> This skill is based on Quarto CLI v1.8.26.

## When to Use What

Task: Write a new Quarto document
Use: Follow "QMD Essentials" below, then see specific reference files

Task: Convert R Markdown to Quarto
Use: [references/conversion-rmarkdown.md](references/conversion-rmarkdown.md)

Task: Migrate bookdown project
Use: [references/conversion-bookdown.md](references/conversion-bookdown.md)

Task: Migrate xaringan slides
Use: [references/conversion-xaringan.md](references/conversion-xaringan.md)

Task: Migrate distill article
Use: [references/conversion-distill.md](references/conversion-distill.md)

Task: Migrate blogdown site
Use: [references/conversion-blogdown.md](references/conversion-blogdown.md)

Task: Add cross-references
Use: [references/cross-references.md](references/cross-references.md)

Task: Configure code cells
Use: [references/code-cells.md](references/code-cells.md)

Task: Add figures with captions
Use: [references/figures.md](references/figures.md)

Task: Create tables
Use: [references/tables.md](references/tables.md)

Task: Add citations and bibliography
Use: [references/citations.md](references/citations.md)

Task: Add callout blocks
Use: [references/callouts.md](references/callouts.md)

Task: Add diagrams (Mermaid, Graphviz)
Use: [references/diagrams.md](references/diagrams.md)

Task: Control page layout
Use: [references/layout.md](references/layout.md)

Task: Use shortcodes
Use: [references/shortcodes.md](references/shortcodes.md)

Task: Add conditional content
Use: [references/conditional-content.md](references/conditional-content.md)

Task: Use divs and spans
Use: [references/divs-and-spans.md](references/divs-and-spans.md)

Task: Configure YAML frontmatter
Use: [references/yaml-frontmatter.md](references/yaml-frontmatter.md)

Task: Find and use extensions
Use: [references/extensions.md](references/extensions.md)

Task: Apply markdown linting rules
Use: [references/markdown-linting.md](references/markdown-linting.md)

## QMD Essentials

### Basic Document Structure

```yaml
title: "Document Title"
author: "Author Name"
date: today
format: html
```

### Code Cell Options Syntax

Quarto uses the language's comment symbol + `|` for cell options. Options use **dashes, not dots** (e.g., `fig-cap` not `fig.cap`).

| Language     | Syntax |
| ------------ | ------ |
| R, Python    | `#\|`  |
| Mermaid      | `%%\|` |
| Graphviz/DOT | `//\|` |

```r
#| label: fig-example
#| echo: false
#| fig-cap: "A scatter plot example."
#| fig-width: 8
#| fig-height: 6

plot(x, y)
```

Common execution options:

| Option    | Description       | Values                    |
| --------- | ----------------- | ------------------------- |
| `eval`    | Evaluate code     | `true`, `false`           |
| `echo`    | Show code         | `true`, `false`, `fenced` |
| `output`  | Include output    | `true`, `false`, `asis`   |
| `warning` | Show warnings     | `true`, `false`           |
| `error`   | Show errors       | `true`, `false`           |
| `include` | Include in output | `true`, `false`           |

Set document-level defaults in YAML:

```yaml
execute:
  echo: false
  warning: false
```

### Cross-References

Labels must start with a type prefix. Reference with `@`:

| Type     | Prefix | Example Label         | Reference        |
| -------- | ------ | --------------------- | ---------------- |
| Figure   | `fig-` | `#\| label: fig-plot` | `@fig-plot`      |
| Table    | `tbl-` | `#\| label: tbl-data` | `@tbl-data`      |
| Section  | `sec-` | `{#sec-intro}`        | `@sec-intro`     |
| Equation | `eq-`  | `{#eq-model}`         | `@eq-model`      |

Example:

```markdown
See @fig-plot for the results.
```

### Callout Blocks

Five types: `note`, `warning`, `important`, `tip`, `caution`.

```markdown
::: {.callout-note}
This is a note callout.
:::

::: {.callout-warning}

## Custom Title

This is a warning with a custom title.

:::
```

### Divs and Spans

Divs use fenced syntax with three colons:

```markdown
::: {.class-name}
Content inside the div.
:::
```

Spans use bracketed syntax:

```markdown
This is [important text]{.highlight}.
```

### Figures

Basic figure with caption:

```markdown
![Caption text](image.png){#fig-name fig-alt="Alt text"}
```

Subfigures:

```markdown
::: {#fig-group layout-ncol=2}
![Sub caption 1](image1.png){#fig-sub1}

![Sub caption 2](image2.png){#fig-sub2}

Main caption for the group.
:::
```

### Tables

Pipe table with caption:

```markdown
| Column 1 | Column 2 |
| -------- | -------- |
| Data 1   | Data 2   |

: Table caption {#tbl-example}
```

### Citations

Basic syntax:

```markdown
According to @smith2020, the results show...
Multiple citations [@smith2020; @jones2021].
Parenthetical only [-@smith2020].
```

Configure in YAML:

```yaml
bibliography: references.bib
csl: apa.csl
```

## Common Workflows

### Creating an HTML Document

```yaml
title: "My Report"
author: "Your Name"
date: today
format:
  html:
    toc: true
    code-fold: true
    theme: cosmo
```

### Creating a PDF Document

```yaml
title: "My Report"
format:
  pdf:
    documentclass: article
    papersize: a4
```

### Creating a RevealJS Presentation

```markdown
---
title: "My Presentation"
format: revealjs
---

## First Slide

Content here.

## Second Slide

More content.
```

### Setting Up a Quarto Project

Create `_quarto.yml` in the project root:

```yaml
project:
  type: website

website:
  title: "My Site"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: about.qmd
        text: About

format:
  html:
    theme: cosmo
```

## Resources

### Reference Files

- [references/code-cells.md](references/code-cells.md) - Hashpipe syntax, execution options, code display
- [references/cross-references.md](references/cross-references.md) - Labels, prefixes, all reference types
- [references/figures.md](references/figures.md) - Figures, subfigures, layouts, lightbox
- [references/tables.md](references/tables.md) - Pipe tables, grid tables, styling
- [references/citations.md](references/citations.md) - Bibliography, CSL, footnotes
- [references/callouts.md](references/callouts.md) - Callout types, appearance, collapsible
- [references/diagrams.md](references/diagrams.md) - Mermaid, Graphviz/DOT
- [references/layout.md](references/layout.md) - Column classes, margin content
- [references/shortcodes.md](references/shortcodes.md) - Built-in shortcodes
- [references/conditional-content.md](references/conditional-content.md) - Format-specific content
- [references/divs-and-spans.md](references/divs-and-spans.md) - Fenced divs, spans, raw blocks
- [references/yaml-frontmatter.md](references/yaml-frontmatter.md) - Document and project YAML
- [references/extensions.md](references/extensions.md) - Using and finding extensions
- [references/markdown-linting.md](references/markdown-linting.md) - Markdown linting rules for Quarto

### Conversion Guides

- [references/conversion-rmarkdown.md](references/conversion-rmarkdown.md) - R Markdown to Quarto
- [references/conversion-bookdown.md](references/conversion-bookdown.md) - bookdown to Quarto
- [references/conversion-xaringan.md](references/conversion-xaringan.md) - xaringan to RevealJS
- [references/conversion-distill.md](references/conversion-distill.md) - distill to Quarto
- [references/conversion-blogdown.md](references/conversion-blogdown.md) - blogdown to Quarto website

### External Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Community Extensions List](https://m.canouil.dev/quarto-extensions/)
