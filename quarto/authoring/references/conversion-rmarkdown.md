# Converting R Markdown to Quarto

Guide for converting R Markdown (.Rmd) documents to Quarto (.qmd).

## Overview

Most R Markdown documents can be rendered by Quarto with minimal changes. The main differences are:

1. YAML structure (output → format)
2. Chunk options (inline → hashpipe)
3. Option naming (dots → dashes)

## Quick Start

### Rename File

```bash
mv document.Rmd document.qmd
```

### Update YAML

#### R Markdown

```yaml
output: html_document
````

#### Quarto

```yaml
format: html
```

### Update Chunk Options

#### R Markdown

````markdown
```{r, echo=TRUE, fig.cap="My figure"}
plot(1:10)
```
````

#### Quarto

````markdown
```{r}
#| echo: true
#| fig-cap: "My figure"

plot(1:10)
```
````

## Format Mapping

| R Markdown                | Quarto     |
| ------------------------- | ---------- |
| `html_document`           | `html`     |
| `pdf_document`            | `pdf`      |
| `word_document`           | `docx`     |
| `github_document`         | `gfm`      |
| `beamer_presentation`     | `beamer`   |
| `ioslides_presentation`   | `revealjs` |
| `slidy_presentation`      | `revealjs` |
| `powerpoint_presentation` | `pptx`     |

## YAML Conversion

### Basic Document

#### R Markdown

```yaml
title: "My Document"
author: "Jane Doe"
date: "2024-01-15"
output:
  html_document:
    toc: true
    toc_float: true
    code_folding: show
```

#### Quarto

```yaml
title: "My Document"
author: "Jane Doe"
date: 2024-01-15
format:
  html:
    toc: true
    toc-location: left
    code-fold: show
```

### Multiple Outputs

#### R Markdown

```yaml
output:
  html_document:
    toc: true
  pdf_document:
    toc: true
```

#### Quarto

```yaml
format:
  html:
    toc: true
  pdf:
    toc: true
```

### Common Options

| R Markdown              | Quarto                   |
| ----------------------- | ------------------------ |
| `toc: true`             | `toc: true`              |
| `toc_float: true`       | `toc-location: left`     |
| `toc_depth: 3`          | `toc-depth: 3`           |
| `number_sections: true` | `number-sections: true`  |
| `code_folding: show`    | `code-fold: show`        |
| `theme: cosmo`          | `theme: cosmo`           |
| `highlight: tango`      | `highlight-style: tango` |
| `fig_width: 8`          | `fig-width: 8`           |
| `fig_height: 6`         | `fig-height: 6`          |
| `df_print: kable`       | (use knitr::kable or gt) |

## Chunk Options

### Syntax Change

Options move inside the code block with `#|` prefix:

#### R Markdown

````markdown
```{r my-chunk, echo=FALSE, fig.cap="Caption", fig.width=8}
plot(1:10)
```
````

#### Quarto

````markdown
```{r}
#| label: my-chunk
#| echo: false
#| fig-cap: "Caption"
#| fig-width: 8

plot(1:10)
```
````

### Option Naming: Dots to Dashes

| R Markdown   | Quarto                   |
| ------------ | ------------------------ |
| `fig.cap`    | `fig-cap`                |
| `fig.width`  | `fig-width`              |
| `fig.height` | `fig-height`             |
| `fig.align`  | `fig-align`              |
| `fig.alt`    | `fig-alt`                |
| `out.width`  | (use `fig-width` or CSS) |
| `results`    | `output`                 |
| `message`    | `message`                |
| `warning`    | `warning`                |
| `include`    | `include`                |

### Results Option

#### R Markdown

```yaml
results='asis'
results='hide'
results='markup'
```

#### Quarto

```yaml
#| output: asis
#| output: false
#| output: true
```

## Setup Chunks

### R Markdown

````markdown
```{r setup, include=FALSE}
knitr::opts_chunk$set(
  echo = TRUE,
  warning = FALSE,
  message = FALSE,
  fig.width = 8,
  fig.height = 6
)
```
````

### Quarto

Use YAML instead:

```yaml
execute:
  echo: true
  warning: false
  message: false
format:
  html:
    fig-width: 8
    fig-height: 6
```

Or keep setup chunk for R-specific options.

## Inline Code

### R Markdown

````markdown
The value is `r mean(x)`.
````

### Quarto

Same syntax works:

````markdown
The value is `r mean(x)`.
````

Or with explicit language:

````markdown
The value is `{r} mean(x)`.
````

## Cross-References

### Figures

#### R Markdown (requires bookdown)

````markdown
```{r my-fig, fig.cap="Caption"}
plot(1:10)
```

See Figure \@ref(fig:my-fig).
````

#### Quarto

````markdown
```{r}
#| label: fig-myplot
#| fig-cap: "Caption"

plot(1:10)
```

See @fig-myplot.
````

### Tables

#### R Markdown (requires bookdown)

````markdown
```{r my-table}
knitr::kable(mtcars[1:5,], caption = "My table")
```

See Table \@ref(tab:my-table).
````

#### Quarto

````markdown
```{r}
#| label: tbl-mydata
#| tbl-cap: "My table"

knitr::kable(mtcars[1:5,])
```

See @tbl-mydata.
````

Note: Quarto uses `tbl-` prefix (not `tab-`).

## Package Dependencies

### Required Packages

R Markdown requires:

- `rmarkdown`
- `knitr`

Quarto doesn't require these packages, but they're useful for:

- `knitr` - Tables, chunk options
- `rmarkdown` - Some helper functions

### Checking Compatibility

Most R Markdown features work in Quarto. Check:

````markdown
```{r}
# Works in both
knitr::kable()
knitr::include_graphics()
```
````

## Step-by-Step Conversion

### 1. Rename File

```bash
mv document.Rmd document.qmd
```

### 2. Update YAML

- Change `output:` to `format:`
- Update format names
- Convert underscores to dashes

### 3. Convert Setup Chunk

Move global options to YAML `execute:` block.

### 4. Update Chunk Options

For each chunk:

1. Move options inside chunk with `#|`
2. Change dots to dashes
3. Add quotes around string values

### 5. Update Cross-References

If using bookdown:

1. Change `\@ref(fig:name)` to `@fig-name`
2. Change `\@ref(tab:name)` to `@tbl-name`
3. Update labels to use prefixes

### 6. Test Render

```bash
quarto render document.qmd
```

## Automation

### Using Editor

RStudio and VS Code can assist with conversion.

### Command Line

Quarto can render .Rmd files directly:

```bash
quarto render document.Rmd
```

This uses R Markdown compatibility mode.

## Common Issues

### Output Not Found

```txt
ERROR: Unknown format
```

Check format name mapping (e.g., `html_document` → `html`).

### Figure Not Appearing

Ensure label starts with `fig-` for cross-references.

### Table Cross-Reference Fails

Use `tbl-` prefix (not `tab-`).

### Chunk Options Ignored

Verify `#|` syntax and dashes (not dots).

## Resources

- [Quarto for R Markdown Users](https://quarto.org/docs/faq/rmarkdown.html)
- [Quarto vs R Markdown](https://quarto.org/docs/faq/rmarkdown.html#quarto-vs.-r-markdown)
