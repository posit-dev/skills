# Cross-References

Quarto provides a unified cross-reference system for figures, tables, equations, sections, theorems, and more.

## Label Prefix System

All cross-referenceable elements require a label starting with a type prefix:

| Type              | Prefix | Example Label    | Reference         |
| ----------------- | ------ | ---------------- | ----------------- |
| Figure            | `fig-` | `fig-plot`       | `@fig-plot`       |
| Table             | `tbl-` | `tbl-data`       | `@tbl-data`       |
| Section           | `sec-` | `sec-intro`      | `@sec-intro`      |
| Equation          | `eq-`  | `eq-model`       | `@eq-model`       |
| Theorem           | `thm-` | `thm-main`       | `@thm-main`       |
| Lemma             | `lem-` | `lem-helper`     | `@lem-helper`     |
| Corollary         | `cor-` | `cor-result`     | `@cor-result`     |
| Proposition       | `prp-` | `prp-statement`  | `@prp-statement`  |
| Conjecture        | `cnj-` | `cnj-hypothesis` | `@cnj-hypothesis` |
| Definition        | `def-` | `def-term`       | `@def-term`       |
| Example           | `exm-` | `exm-case`       | `@exm-case`       |
| Exercise          | `exr-` | `exr-problem`    | `@exr-problem`    |
| Listing           | `lst-` | `lst-code`       | `@lst-code`       |
| Note callout      | `nte-` | `nte-info`       | `@nte-info`       |
| Tip callout       | `tip-` | `tip-hint`       | `@tip-hint`       |
| Warning callout   | `wrn-` | `wrn-alert`      | `@wrn-alert`      |
| Important callout | `imp-` | `imp-key`        | `@imp-key`        |
| Caution callout   | `cau-` | `cau-danger`     | `@cau-danger`     |

## Recommended Syntax

For consistency, prefer using div syntax for cross-referenceable elements:

````markdown
::: {#tbl-example}

| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |

Table caption.
:::
````

Instead of inline caption syntax:

````markdown
| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |

: Table caption. {#tbl-example}
````

Both syntaxes work, but div syntax provides a more consistent pattern across all element types (figures, tables, theorems, etc.).

## Reference Syntax

Use `@` followed by the label to create a reference:

````markdown
See @fig-plot for the visualization.
The data is shown in @tbl-results.
As discussed in @sec-methods, we used...
````

### Capitalization

Use capital letter to get capitalized prefix:

````markdown
@fig-plot → Figure 1
@Fig-plot → Figure 1 (same, but ensures capital)
````

### Prefix Customization

Use square brackets for custom prefix:

````markdown
[Figure @fig-plot] → Figure 1
[See @fig-plot] → See 1
[-@fig-plot] → 1 (number only)
````

### Multiple References

````markdown
See @fig-plot and @fig-scatter.
Tables [-@tbl-one; -@tbl-two] show...
````

## Figures

### Code-Generated Figures

````markdown
```{r}
#| label: fig-scatter
#| fig-cap: "Scatter plot of x versus y."

plot(x, y)
```
````

Reference: `See @fig-scatter.`

### Markdown Figures

````markdown
![Elephant](elephant.png){#fig-elephant}

See @fig-elephant for the image.
````

### Subfigures

````markdown
::: {#fig-animals layout-ncol=2}

![Cat](cat.png){#fig-cat}

![Dog](dog.png){#fig-dog}

Comparison of animals.
:::

See @fig-animals, specifically @fig-cat.
````

## Tables

### Code-Generated Tables

````markdown
```{r}
#| label: tbl-summary
#| tbl-cap: "Summary statistics."

knitr::kable(summary_data)
```

Reference: `See @tbl-summary.`
````

### Markdown Tables

````markdown
::: {#tbl-data}

| Col 1 | Col 2 |
| ----- | ----- |
| A     | B     |

Summary data.
:::

See @tbl-data for details.
````

### Subtables

````markdown
::: {#tbl-panel layout-ncol=2}

::: {#tbl-first}

| Col A |
| ----- |
| 1     |

First table.
:::

::: {#tbl-second}

| Col B |
| ----- |
| 2     |

Second table.
:::

Combined tables.
:::

See @tbl-panel, including @tbl-first.
````

## Sections

Enable numbered sections to reference them:

```yaml
number-sections: true
```

Add label to heading:

````markdown
## Introduction {#sec-intro}

As discussed in @sec-intro...
````

## Equations

````markdown
$$
y = mx + b
$$ {#eq-line}

Equation @eq-line shows...
$$
````

Or display-style:

````markdown
$$
E = mc^2
$$ {#eq-einstein}

See @eq-einstein.
$$
````

## Theorems and Proofs

````markdown
::: {#thm-pythagorean}

## Pythagorean Theorem

For a right triangle with legs $a$ and $b$ and hypotenuse $c$:
$$a^2 + b^2 = c^2$$
:::

By @thm-pythagorean, we know...
````

Available theorem types: `thm`, `lem`, `cor`, `prp`, `cnj`, `def`, `exm`, `exr`.

## Code Listings

````markdown
```{#lst-example .python lst-cap="Example Python code"}
def hello():
    print("Hello, world!")
```

See @lst-example for the code.
````

## Callouts

Make callouts cross-referenceable by adding an ID:

````markdown
::: {#nte-important .callout-note}

## Important Note

This is cross-referenceable.
:::

See @nte-important for details.
````

## Custom Cross-Reference Types

Define custom types in YAML:

```yaml
crossref:
  custom:
    - kind: float
      key: vid
      reference-prefix: "Video"
      caption-prefix: "Video"
```

Use:

````markdown
::: {#vid-demo}
<video src="demo.mp4"></video>

Demo video.
:::

See @vid-demo.
````

## Cross-Reference Options

Configure in YAML front matter:

```yaml
crossref:
  fig-title: "Figure" # Prefix for figures
  tbl-title: "Table" # Prefix for tables
  eq-prefix: "Equation" # Prefix for equations
  sec-prefix: "Section" # Prefix for sections
  fig-prefix: "Figure" # In-text prefix
  tbl-prefix: "Table" # In-text prefix
  chapters: true # Number by chapter
```

### Localization

```yaml
lang: de
crossref:
  fig-title: "Abbildung"
  tbl-title: "Tabelle"
```

## bookdown Migration

- `\@ref(fig:name)` → `@fig-name`
- `\@ref(tab:name)` → `@tbl-name`
- `\@ref(eq:name)` → `@eq-name`
- `\@ref(thm:name)` → `@thm-name`
- `(#fig:name)` → `{#fig-name}` or `#| label: fig-name`
- `(#tab:name)` → `{#tbl-name}` or `#| label: tbl-name`

Note: Quarto uses `tbl-` prefix (not `tab-`) for tables.

## Resources

- [Quarto Cross-References](https://quarto.org/docs/authoring/cross-references.html)
- [Figures](https://quarto.org/docs/authoring/figures.html)
- [Tables](https://quarto.org/docs/authoring/tables.html)
