---
name: quarto-migration
description: >
  Guidance for migrating R Markdown ecosystem projects to Quarto.
  Use this skill when:
  (1) Converting R Markdown (.Rmd) documents to Quarto (.qmd),
  (2) Migrating bookdown projects to Quarto book format,
  (3) Migrating blogdown sites to Quarto websites,
  (4) Converting xaringan slides to Quarto RevealJS,
  (5) Migrating distill articles or blogs to Quarto.
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
