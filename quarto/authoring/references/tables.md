# Tables

Quarto supports multiple table formats including pipe tables, list tables, and computational tables with extensive styling options.

## Pipe Tables

The most common table format:

````markdown
| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| Row 1    | Data     | More     |
| Row 2    | Data     | More     |
````

### Column Alignment

Use colons to specify alignment:

````markdown
| Left    | Center  |   Right |
| :------ | :-----: | ------: |
| Left    | Center  |   Right |
| aligned | aligned | aligned |
````

- `:---` Left align
- `:---:` Center align
- `---:` Right align

### With Caption

````markdown
::: {#tbl-example}

| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |

Table caption.
:::
````

Reference with `@tbl-example`.

## Column Widths

### Using Dashes

More dashes = wider column:

````markdown
| Narrow | Wide Column |
| ------ | ----------- |
| A      | B           |
````

This creates approximately 33%/67% split.

### Explicit Widths

````markdown
| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |

: Caption {tbl-colwidths="[25,75]"}
````

### Document Level

```yaml
tbl-colwidths: [40, 60]
```

Or auto-fit:

```yaml
tbl-colwidths: auto
```

## List Tables

For complex content including multiple paragraphs, lists, and code blocks. Quarto natively supports pandoc list table syntax.

### Basic Syntax

Use bullet lists where top-level items (`-`) are columns and nested items are rows:

````markdown
::: {.list-table}

- - Header 1
  - Row 1, Col 1
  - Row 2, Col 1
- - Header 2
  - Row 1, Col 2
  - Row 2, Col 2

:::
````

### List Table Caption

Add a paragraph at the start for the caption:

````markdown
::: {.list-table #tbl-example}

Table caption here.

- - Column A
  - Column B
  - Column C
- - Data 1
  - Data 2
  - Data 3

:::
````

### List Table Attributes

| Attribute     | Description                  | Example                |
| ------------- | ---------------------------- | ---------------------- |
| `header-rows` | Rows in header (default: 1)  | `header-rows=2`        |
| `header-cols` | Columns as headers           | `header-cols=1`        |
| `aligns`      | Column alignment             | `aligns="l,c,r"`       |
| `widths`      | Relative column widths       | `widths="30,70"`       |

### Header Configuration

````markdown
::: {.list-table header-rows=1 header-cols=1}

- - 
  - Col Header 1
  - Col Header 2
- - Row Header
  - Data 1
  - Data 2

:::
````

Set `header-rows=0` for tables without headers.

### List Table Alignment

````markdown
::: {.list-table aligns=l,c,r}

- - Left
  - Center
  - Right
- - Left Content 1
  - Center Content 1
  - Right Content 1
- - Left Content 2
  - Center Content 2
  - Right Content 2

:::
````

Alignment options: `l` (left), `c` (center), `r` (right), `d` (default).

### List Table Widths

````markdown
::: {.list-table widths="30,70"}

- - Narrow
  - Wide
- - Narrow Content
  - Wide Content

:::
````

### Cell-Level Alignment

Override column alignment for individual cells:

````markdown
::: {.list-table}

- - Column 1
  - Column 2
- - []{align=r}Right-aligned cell
  - Normal cell
- - Normal cell
  - []{align=c}Centered cell

:::
````

### Row and Column Spans

Use empty spans with `colspan` or `rowspan`:

````markdown
::: {.list-table}

- - Column A
  - Column B
  - Column C
- - []{colspan=2}Spans two columns
  - Normal
- - Normal
  - Normal
  - Normal
- - []{rowspan=2}Spans two rows
  - Data 1
  - Data 2
- - Data 3
  - Data 4

:::
````

### Row Attributes

Apply attributes to entire rows using an empty span:

````markdown
::: {.list-table}

- - Column 1
  - Column 2
- - []{.highlight}This row has the highlight class
  - Content
- - Normal row
  - Content

:::
````

### Empty Cells

Use a lone `-` for empty cells:

````markdown
::: {.list-table}

- - Column A
  - Column B
- - Data
  -
- -
  - Data

:::
````

### Complex Cell Content

List tables support any markdown content in cells:

````markdown
::: {.list-table}

- - Column A
  - Column B
- - Simple text
  - More text
- - - Nested list item 1
    - Nested list item 2
  - ```python
    code_block()
    ```

:::
````

## Computational Tables

Tables generated from code:

### R with knitr

````markdown
```{r}
#| label: tbl-summary
#| tbl-cap: "Summary statistics."

knitr::kable(summary_data)
```
````

### R with gt

````markdown
```{r}
#| label: tbl-styled
#| tbl-cap: "Styled table."

library(gt)
gt(data) |>
  tab_header(title = "My Table")
```
````

### Python with pandas

````markdown
```{python}
#| label: tbl-pandas
#| tbl-cap: "Data summary."

import pandas as pd
df.to_markdown()
```
````

### Table Options

| Option             | Description      | Example      |
| ------------------ | ---------------- | ------------ |
| `tbl-cap`          | Table caption    | `"Summary."` |
| `tbl-subcap`       | Subcaptions      | `["A", "B"]` |
| `tbl-colwidths`    | Column widths    | `[40, 60]`   |
| `tbl-cap-location` | Caption position | `"top"`      |

## Caption Location

### Document Level

```yaml
tbl-cap-location: top
```

### Per Table

````markdown
```{r}
#| label: tbl-data
#| tbl-cap: "Data."
#| tbl-cap-location: bottom

knitr::kable(data)
```
````

Options: `top`, `bottom`, `margin`.

## Subtables

Multiple tables with shared caption:

````markdown
::: {#tbl-panel layout-ncol=2}

::: {#tbl-first}

| A   | B   |
| --- | --- |
| 1   | 2   |

First.
:::

::: {#tbl-second}

| C   | D   |
| --- | --- |
| 3   | 4   |

Second.
:::

Combined tables.
:::

See @tbl-panel, including @tbl-first.
````

### From Code

````markdown
```{r}
#| label: tbl-multi
#| tbl-cap: "Multiple tables."
#| tbl-subcap:
#|   - "Summary"
#|   - "Details"
#| layout-ncol: 2

knitr::kable(summary_df)
knitr::kable(detail_df)
```
````

## Bootstrap Styling (HTML)

Add Bootstrap classes for styling:

````markdown
::: {#tbl-styled .striped .hover}

| A   | B   |
| --- | --- |
| 1   | 2   |

Styled table.
:::
````

Available classes:

| Class         | Effect                 |
| ------------- | ---------------------- |
| `.striped`    | Alternating row colors |
| `.hover`      | Highlight on hover     |
| `.bordered`   | Add borders            |
| `.borderless` | Remove borders         |
| `.sm`         | Smaller text           |
| `.responsive` | Horizontal scroll      |

### Combining Classes

````markdown
::: {#tbl-combined .striped .hover .bordered}

| A   | B   |
| --- | --- |
| 1   | 2   |

Table caption.
:::
````

### Disable Striping for Code Tables

````markdown
```{r}
#| label: tbl-plain
#| tbl-cap: "Plain table."
#| classes: plain

knitr::kable(data)
```
````

## HTML Tables

Quarto can process HTML tables:

```html
<table>
  <tr>
    <th>Header 1</th>
    <th>Header 2</th>
  </tr>
  <tr>
    <td>Data 1</td>
    <td>Data 2</td>
  </tr>
</table>
```

### Cell Spanning

```html
<table>
  <tr>
    <td colspan="2">Spanning cell</td>
  </tr>
  <tr>
    <td>A</td>
    <td>B</td>
  </tr>
</table>
```

### Markdown in HTML Tables

Use `data-qmd` attribute:

```html
<table>
  <tr>
    <td data-qmd="**Bold** and *italic*">Fallback</td>
  </tr>
</table>
```

### Disable HTML Processing

```yaml
html-table-processing: none
```

## Table Layouts

Same as figures:

````markdown
::: {layout-ncol=2}

| A   | B   |
| --- | --- |
| 1   | 2   |

| C   | D   |
| --- | --- |
| 3   | 4   |

:::
````

## Long Tables

For tables spanning multiple pages (PDF):

````markdown
```{r}
#| label: tbl-long
#| tbl-cap: "Long table."

knitr::kable(long_data, longtable = TRUE)
```
````

## Cross-Referencing

Tables are referenced with `tbl-` prefix:

````markdown
::: {#tbl-summary}

| Data |
| ---- |
| 1    |

Summary.
:::

See @tbl-summary for details.
````

## Resources

- [Quarto Tables](https://quarto.org/docs/authoring/tables.html)
- [Table Cross-References](https://quarto.org/docs/authoring/cross-references.html#tables)
- [Pandoc List Tables](https://github.com/pandoc-ext/list-table)
