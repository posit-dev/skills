# Converting bookdown to Quarto

Guide for converting bookdown projects to Quarto book format.

## Overview

Key differences:

1. Configuration file: `_bookdown.yml` → `_quarto.yml`
2. Cross-references: `\@ref()` → `@`
3. Chapter organization
4. Theorem environments

## Quick Start

### 1. Create Quarto Config

Replace `_bookdown.yml` with `_quarto.yml`:

```yaml
project:
  type: book

book:
  title: "My Book"
  author: "Author Name"
  chapters:
    - index.qmd
    - chapter1.qmd
    - chapter2.qmd

format:
  html:
    theme: cosmo
  pdf:
    documentclass: book
```

### 2. Rename Files

```bash
for f in *.Rmd; do mv "$f" "${f%.Rmd}.qmd"; done
```

### 3. Update Cross-References

#### Bookdown

````markdown
See Figure \@ref(fig:myplot)
See Table \@ref(tab:mytable)
````

#### Quarto

````markdown
See @fig-myplot
See @tbl-mytable
````

## Configuration Mapping

### bookdown (`_bookdown.yml`)

```yaml
book_filename: "my-book"
output_dir: "docs"
delete_merged_file: true
language:
  ui:
    chapter_name: "Chapter "
rmd_files:
  - index.Rmd
  - 01-intro.Rmd
  - 02-methods.Rmd
  - 03-results.Rmd
  - references.Rmd
```

### Quarto (`_quarto.yml`)

```yaml
project:
  type: book
  output-dir: docs

book:
  title: "My Book"
  author: "Author Name"
  date: today
  chapters:
    - index.qmd
    - intro.qmd
    - methods.qmd
    - results.qmd
  appendices:
    - references.qmd

format:
  html:
    theme: cosmo
  pdf:
    documentclass: book
```

## Chapter Organization

### With Parts

```yaml
book:
  chapters:
    - index.qmd
    - part: "Part I: Foundation"
      chapters:
        - basics.qmd
        - setup.qmd
    - part: "Part II: Advanced"
      chapters:
        - advanced1.qmd
        - advanced2.qmd
  appendices:
    - appendix.qmd
```

### Numbered vs Unnumbered

Add `{.unnumbered}` to exclude from numbering:

````markdown
# Preface {.unnumbered}
````

## Cross-Reference Conversion

### Figures

#### bookdown

````markdown
```{r myplot, fig.cap="My figure"}
plot(1:10)
```

See Figure \@ref(fig:myplot).
````

#### Quarto

````markdown
```{r}
#| label: fig-myplot
#| fig-cap: "My figure"

plot(1:10)
```

See @fig-myplot.
````

### Tables

#### bookdown

````markdown
```{r mytable}
knitr::kable(head(iris), caption = "Iris data")
```

See Table \@ref(tab:mytable).
````

#### Quarto

````markdown
```{r}
#| label: tbl-iris
#| tbl-cap: "Iris data"

knitr::kable(head(iris))
```

See @tbl-iris.
````

Note: Quarto uses `tbl-` not `tab-`.

### Equations

#### bookdown

````markdown
# bookdown
\begin{equation}
y = mx + b (\#eq:line)
\end{equation}
See Equation \@ref(eq:line).
````

#### Quarto

````markdown
$$
y = mx + b
$$ {#eq-line}

See @eq-line.
````

### Sections

#### bookdown

````markdown
# Introduction {#intro}

See Section \@ref(intro).
````

#### Quarto

````markdown
# Introduction {#sec-intro}

See @sec-intro.
````

### Theorems

#### bookdown

````markdown
```{theorem, name="Pythagorean"}
For a right triangle, $a^2 + b^2 = c^2$.
```

See Theorem \@ref(thm:pythagorean).
````

#### Quarto

````markdown
::: {#thm-pythagorean}

## Pythagorean Theorem

For a right triangle, $a^2 + b^2 = c^2$.
:::

See @thm-pythagorean.
````

## Theorem Environments

### bookdown

````markdown
```{theorem, label="main", name="Main Theorem"}
Statement here.
```

```{lemma}
Lemma statement.
```

```{proof}
Proof here.
```
````

### Quarto

````markdown
::: {#thm-main}

## Main Theorem

Statement here.

:::

::: {#lem-helper}

## Helper Lemma

Lemma statement.

:::

::: {.proof}
Proof here.
:::
````

Supported types: `thm`, `lem`, `cor`, `prp`, `cnj`, `def`, `exm`, `exr`.

## Custom Blocks

### bookdown

````markdown
```{block, type='rmdnote'}
This is a note.
```
````

### Quarto

````markdown
::: {.callout-note}
This is a note.
:::
````

## Output Formats

### bookdown

```yaml
output:
  bookdown::gitbook:
    css: style.css
  bookdown::pdf_book:
    includes:
      in_header: preamble.tex
```

### Quarto

```yaml
format:
  html:
    theme: cosmo
    css: style.css
  pdf:
    documentclass: book
    include-in-header: preamble.tex
```

### Format Mapping

| bookdown         | Quarto |
| ---------------- | ------ |
| `gitbook`        | `html` |
| `pdf_book`       | `pdf`  |
| `epub_book`      | `epub` |
| `word_document2` | `docx` |

## Bibliography

### bookdown

```yaml
# _bookdown.yml
bibliography: [book.bib, packages.bib]
```

### Quarto

In `_quarto.yml`:

```yaml
book:
  bibliography: references.bib
```

Or in individual files:

```yaml
bibliography: references.bib
```

## Custom Styling

### HTML

```yaml
format:
  html:
    theme:
      - cosmo
      - custom.scss
    css: styles.css
```

### PDF

```yaml
format:
  pdf:
    documentclass: book
    include-in-header: preamble.tex
```

## Step-by-Step Conversion

### 1. Create `_quarto.yml`

```yaml
project:
  type: book

book:
  title: "Book Title"
  author: "Author"
  chapters:
    - index.qmd
    # List chapters
```

### 2. Rename Files

```bash
for f in *.Rmd; do mv "$f" "${f%.Rmd}.qmd"; done
```

### 3. Remove `_bookdown.yml`

```bash
rm _bookdown.yml
```

### 4. Update Cross-References

Search and replace:

| Find         | Replace  |
| ------------ | -------- |
| `\@ref(fig:` | `@fig-`  |
| `\@ref(tab:` | `@tbl-`  |
| `\@ref(eq:`  | `@eq-`   |
| `\@ref(thm:` | `@thm-`  |
| `)` at end   | (remove) |

### 5. Update Chunk Labels

```yaml
# From
{r myplot, fig.cap="..."}

# To
{r}
#| label: fig-myplot
#| fig-cap: "..."
```

### 6. Convert Theorem Blocks

Replace ````{theorem}` with `::: {#thm-name}`.

### 7. Update Custom Blocks

Replace custom blocks with callouts.

### 8. Test Render

```bash
quarto render
```

## Common Issues

### Chapters Not Found

Check file names in `_quarto.yml` match actual files.

### Cross-Reference Not Working

Ensure:

- Label has correct prefix (`fig-`, `tbl-`, etc.)
- Reference uses `@` syntax

### Theorem Numbering Wrong

Check theorem IDs are unique and properly formatted.

## Resources

- [Quarto Books](https://quarto.org/docs/books/)
- [Cross-References](https://quarto.org/docs/authoring/cross-references.html)
- [Theorems](https://quarto.org/docs/authoring/cross-references.html#theorems-and-proofs)
