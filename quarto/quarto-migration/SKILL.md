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

## Migration Overview

All migrations from the R Markdown ecosystem to Quarto share common patterns.

### Option Naming

R Markdown uses dots in option names; Quarto uses dashes:

- `fig.cap` becomes `fig-cap`.
- `fig.width` becomes `fig-width`.
- `out.width` becomes `out-width` (or use `fig-width` instead).

### YAML Structure

R Markdown uses `output:` with underscored format names; Quarto uses `format:` with short names:

```yaml
# R Markdown
output: html_document

# Quarto
format: html
```

### Cross-Reference Prefixes

R Markdown/bookdown uses `\@ref(fig:name)`; Quarto uses `@fig-name`:

- Figures: `\@ref(fig:plot)` becomes `@fig-plot`.
- Tables: `\@ref(tab:data)` becomes `@tbl-data`.
- Sections: `\@ref(intro)` becomes `@sec-intro`.
- Equations: `\@ref(eq:model)` becomes `@eq-model`.

### Chunk Options

R Markdown uses inline chunk options; Quarto uses hashpipe (`#|`) syntax:

````markdown
# R Markdown

```{r, echo=TRUE, fig.cap="A plot"}
plot(1)
```

# Quarto

```{r}
#| echo: true
#| fig-cap: "A plot"
plot(1)
```
````

## Resources

### Reference Files

- [references/rmarkdown.md](references/rmarkdown.md) - R Markdown to Quarto.
- [references/bookdown.md](references/bookdown.md) - bookdown to Quarto book.
- [references/xaringan.md](references/xaringan.md) - xaringan to RevealJS.
- [references/distill.md](references/distill.md) - distill to Quarto.
- [references/blogdown.md](references/blogdown.md) - blogdown to Quarto website.

### External Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
