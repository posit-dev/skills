---
name: quarto-migration
description: >
  Migrating R Markdown ecosystem projects to Quarto, including R Markdown (.Rmd)
  documents, bookdown books, blogdown websites, xaringan presentations, and
  distill articles. Covers common migration patterns such as option naming
  (dots to dashes), YAML structure changes, cross-reference syntax, and
  chunk option conversion to hashpipe (#|) syntax.
metadata:
  author: Mickaël Canouil (@mcanouil)
  version: "1.0"
license: MIT
---

# Quarto Migration

> This skill is based on Quarto CLI v1.8.26.

## When to Use What

Task: Convert R Markdown to Quarto
Use: [references/rmarkdown.md](references/rmarkdown.md)

Task: Migrate bookdown project
Use: [references/bookdown.md](references/bookdown.md)

Task: Migrate xaringan slides
Use: [references/xaringan.md](references/xaringan.md)

Task: Migrate distill article
Use: [references/distill.md](references/distill.md)

Task: Migrate blogdown site
Use: [references/blogdown.md](references/blogdown.md)

## Common Migration Patterns

All R Markdown ecosystem migrations share these key changes:

- **Option naming**: dots to dashes (`fig.cap` to `fig-cap`).
- **YAML**: `output: html_document` to `format: html`.
- **Cross-references**: `\@ref(fig:plot)` to `@fig-plot`, `\@ref(tab:data)` to `@tbl-data`.
- **Chunk options**: inline `{r, echo=TRUE}` to hashpipe `#| echo: true`.

## Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
