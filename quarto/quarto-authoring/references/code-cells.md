# Code Cells

Quarto uses a hashpipe (`#|`) syntax for code cell options, providing a clean, YAML-based approach that works across R, Python, Julia, and other languages.

## Hashpipe Syntax

Code cell options are specified with `#|` at the start of lines within the code block:

````markdown
```{language}
#| label: fig-scatter
#| echo: false
#| fig-cap: "A scatter plot of x versus y."
#| fig-width: 8
#| fig-height: 6

# code that produces a scatter plot
```
````

**Important:** Options use **dashes, not dots**. Use `fig-cap` not `fig.cap`, `fig-width` not `fig.width`.

The hashpipe prefix is `#|` for R, Python, and Julia; diagram cells use a different prefix. See [engines.md](engines.md) for the full table.

## Execution Options

Control whether and how code is executed:

| Option    | Description                               | Values                    |
| --------- | ----------------------------------------- | ------------------------- |
| `eval`    | Evaluate the code                         | `true`, `false`           |
| `echo`    | Include source code in output             | `true`, `false`, `fenced` |
| `output`  | Include results in output                 | `true`, `false`, `asis`   |
| `warning` | Include warnings                          | `true`, `false`           |
| `error`   | Include errors (stop on error if `false`) | `true`, `false`           |
| `include` | Include cell in output at all             | `true`, `false`           |

### Examples

Show code but don't run it:

````markdown
```{language}
#| eval: false

# This code is displayed but not executed
```
````

Run code but hide it:

````markdown
```{language}
#| echo: false

# This code runs but is not shown
```
````

Show fenced code block with attributes:

````markdown
```{language}
#| echo: fenced

# code here
```
````

### output: asis

`output: asis` passes the cell output through as raw content without further Quarto processing.
Use it when your code prints a pre-formatted markdown or raw string that Quarto should treat as document content.

Requirements:

- The output must already be valid markdown (pipe table, headings, prose) or a raw block (` ```{=html} `, ` ```{=latex} `).
- `tbl-cap` on an `output: asis` cell does not behave identically to the knitr table-rendering path; prefer a div-wrapped caption for reliability.

````markdown
```{language}
#| output: asis

# print("| Col A | Col B |\n| ----- | ----- |\n| 1     | 2     |")
```
````

## Figure Options

Options for controlling figure output:

| Option             | Description                      | Example                         |
| ------------------ | -------------------------------- | ------------------------------- |
| `fig-cap`          | Figure caption                   | `"A descriptive caption."`      |
| `fig-subcap`       | Subcaptions for multiple figures | `["Plot A", "Plot B"]`          |
| `fig-width`        | Width in inches                  | `8`                             |
| `fig-height`       | Height in inches                 | `6`                             |
| `fig-alt`          | Alt text for accessibility       | `"Scatter plot showing..."`     |
| `fig-align`        | Alignment                        | `"left"`, `"center"`, `"right"` |
| `fig-cap-location` | Caption position                 | `"top"`, `"bottom"`, `"margin"` |
| `fig-format`       | Output format                    | `"png"`, `"svg"`, `"pdf"`       |
| `fig-dpi`          | Resolution in DPI                | `300`                           |

### Figure Example

````markdown
```{language}
#| label: fig-analysis
#| fig-cap: "Analysis results showing the relationship between variables."
#| fig-alt: "Scatter plot with trend line showing positive correlation."
#| fig-width: 10
#| fig-height: 6
#| fig-align: center

# code that produces a scatter plot with trend line
```
````

### Multiple Figures

````markdown
```{language}
#| label: fig-panels
#| fig-cap: "Multiple panel figure."
#| fig-subcap:
#|   - "Distribution of X"
#|   - "Distribution of Y"
#| layout-ncol: 2

# code that produces two figures (one per panel)
```
````

## Table Options

Options for controlling table output:

| Option             | Description                     | Example                         |
| ------------------ | ------------------------------- | ------------------------------- |
| `tbl-cap`          | Table caption                   | `"Summary statistics."`         |
| `tbl-subcap`       | Subcaptions for multiple tables | `["Table A", "Table B"]`        |
| `tbl-colwidths`    | Column widths                   | `[40, 60]` or `"auto"`          |
| `tbl-cap-location` | Caption position                | `"top"`, `"bottom"`, `"margin"` |

### Table Example

````markdown
```{language}
#| label: tbl-summary
#| tbl-cap: "Summary statistics by group."

# code that produces a table
```
````

Table rendering behaviour differs between the knitr and jupyter engines; see [tables.md](tables.md) for details.
For markdown table output from code, use `output: asis` (see the [output: asis](#output-asis) section above).

## Caching and Freeze

Only suggest `#| cache: true` for R code cells (knitr engine).
It is not valid for Python or Julia cells — the jupyter engine silently ignores it.

For Python and Julia, caching is document-level only.
Install `jupyter-cache` (`pip install jupyter-cache`) and set in YAML front matter:

```yaml
execute:
  cache: true
```

For details see <https://quarto.org/docs/projects/code-execution.html#cache>.

### Project-Level Freeze

In `_quarto.yml`:

```yaml
execute:
  freeze: auto # Re-render only when source changes
```

## Document-Level Defaults

Set defaults for all code cells in YAML front matter:

```yaml
title: "My Document"
execute:
  echo: false
  warning: false
  message: false
```

Or per-format:

```yaml
format:
  html:
    code-fold: true
  pdf:
    echo: false
```

## Code Display Options

Control how code is displayed in HTML output:

| Option              | Description          | Values                    |
| ------------------- | -------------------- | ------------------------- |
| `code-fold`         | Collapsible code     | `true`, `false`, `"show"` |
| `code-summary`      | Text for fold toggle | `"Show code"`             |
| `code-tools`        | Code tools menu      | `true`, `false`           |
| `code-line-numbers` | Show line numbers    | `true`, `false`           |
| `code-overflow`     | Handle overflow      | `"scroll"`, `"wrap"`      |

### Code Folding

In YAML front matter:

```yaml
format:
  html:
    code-fold: true
    code-summary: "Click to see code"
```

Per cell override:

````markdown
```{language}
#| code-fold: show

# This code is visible by default
```
````

## Code Annotations

Add annotations to explain code:

````markdown
```{language}
#| code-annotations: hover

step_one()   # <1>
step_two()   # <2>
step_three() # <3>
```
````

1. First step description.
2. Second step description.
3. Third step description.

Annotation styles: `hover`, `select`, `below`, `beside`.

## Filename Display

Show a filename above the code block:

````markdown
```{language}
#| filename: "analysis.ext"

# code here
```
````

## R Markdown Migration

R Markdown uses dots (`.`), Quarto uses dashes (`-`): `fig.cap` → `fig-cap`, `fig.width` → `fig-width`. Options move from chunk header to `#|` lines. `results="asis"` becomes `output: asis`. Setup chunks with `knitr::opts_chunk$set(...)` become `execute:` in YAML. See [conversion-rmarkdown.md](conversion-rmarkdown.md) for full details.

## Resources

- [Quarto Execution Options](https://quarto.org/docs/computations/execution-options.html)
- [Code Annotation](https://quarto.org/docs/authoring/code-annotation.html)
- [Code Cells: Knitr](https://quarto.org/docs/reference/cells/cells-knitr.html)
- [Code Cells: Jupyter](https://quarto.org/docs/reference/cells/cells-jupyter.html)
