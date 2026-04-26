# Tables

Quarto supports multiple table formats including pipe tables, list tables, and computational tables with extensive styling options.

## Pipe Tables

The most common table format:

```markdown
| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| Row 1    | Data     | More     |
| Row 2    | Data     | More     |
```

### Column Alignment

Use colons to specify alignment:

```markdown
| Left    | Center  |   Right |
| :------ | :-----: | ------: |
| Left    | Center  |   Right |
| aligned | aligned | aligned |
```

- `:---` Left align
- `:---:` Center align
- `---:` Right align

### With Caption

```markdown
::: {#tbl-example}

| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |

Table caption.
:::
```

Reference with `@tbl-example`.

## Column Widths

### Using Dashes

More dashes = wider column:

```markdown
| Narrow | Wide Column |
| ------ | ----------- |
| A      | B           |
```

This creates approximately 33%/67% split.

### Explicit Widths

```markdown
| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |

: Caption {tbl-colwidths="[25,75]"}
```

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

```markdown
::: {.list-table}

- - Header 1
  - Row 1, Col 1
  - Row 2, Col 1
- - Header 2
  - Row 1, Col 2
  - Row 2, Col 2

:::
```

### List Table Caption

Add a paragraph at the start for the caption:

```markdown
::: {.list-table #tbl-example}

Table caption here.

- - Column A
  - Column B
  - Column C
- - Data 1
  - Data 2
  - Data 3

:::
```

### List Table Attributes

| Attribute     | Description                 | Example          |
| ------------- | --------------------------- | ---------------- |
| `header-rows` | Rows in header (default: 1) | `header-rows=2`  |
| `header-cols` | Columns as headers          | `header-cols=1`  |
| `aligns`      | Column alignment            | `aligns="l,c,r"` |
| `widths`      | Relative column widths      | `widths="30,70"` |

### Header Configuration

```markdown
::: {.list-table header-rows=1 header-cols=1}

- -
  - Col Header 1
  - Col Header 2
- - Row Header
  - Data 1
  - Data 2

:::
```

Set `header-rows=0` for tables without headers.

### Row and Column Spans

Use empty spans with `colspan` or `rowspan`:

```markdown
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
```

List tables also support row/cell attributes (`[]{.highlight}`, `[]{align=r}`), empty cells (lone `-`), and any markdown content in cells.

## Computational Tables

Tables generated from code:

````markdown
```{language}
#| label: tbl-summary
#| tbl-cap: "Summary statistics."

# code that produces a table
```
````

**Engine note — table rendering differs by engine:**

- **knitr engine**: Recognised table objects are rendered automatically (e.g. a data frame is printed as a markdown table without extra configuration).
- **jupyter engine**: Cells that return a display-protocol object auto-display as HTML in HTML output only. For portable output across all formats, print a markdown table string and set `output: asis`:

````markdown
```{language}
#| label: tbl-summary
#| tbl-cap: "Summary statistics."
#| output: asis

# print a markdown table string to stdout
```
````

See [engines.md](engines.md) for full engine details.

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
```{language}
#| label: tbl-data
#| tbl-cap: "Data."
#| tbl-cap-location: bottom

# code that produces a table
```
````

Options: `top`, `bottom`, `margin`.

## Subtables

Multiple tables with shared caption:

```markdown
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
```

### From Code

````markdown
```{language}
#| label: tbl-multi
#| tbl-cap: "Multiple tables."
#| tbl-subcap:
#|   - "Summary"
#|   - "Details"
#| layout-ncol: 2

# code that produces two tables
```
````

## Bootstrap Styling (HTML)

Add Bootstrap classes for styling:

```markdown
::: {#tbl-styled .striped .hover}

| A   | B   |
| --- | --- |
| 1   | 2   |

Styled table.
:::
```

Available classes:

| Class         | Effect                 |
| ------------- | ---------------------- |
| `.striped`    | Alternating row colors |
| `.hover`      | Highlight on hover     |
| `.bordered`   | Add borders            |
| `.borderless` | Remove borders         |
| `.sm`         | Smaller text           |
| `.responsive` | Horizontal scroll      |

Combine multiple classes: `::: {#tbl-name .striped .hover .bordered}`. Use `classes: plain` in code cells to disable default striping.

Quarto also processes HTML tables with `data-qmd` attribute for markdown content. Disable with `html-table-processing: none`.

## Table Layouts

Same as figures:

```markdown
::: {layout-ncol=2}

| A   | B   |
| --- | --- |
| 1   | 2   |

| C   | D   |
| --- | --- |
| 3   | 4   |

:::
```

## Long Tables

For tables spanning multiple pages (PDF), use a longtable option appropriate to your engine/package.

## Cross-Referencing

Tables are referenced with `tbl-` prefix:

```markdown
::: {#tbl-summary}

| Data |
| ---- |
| 1    |

Summary.
:::

See @tbl-summary for details.
```

## Resources

- [Quarto Tables](https://quarto.org/docs/authoring/tables.html)
- [Table Cross-References](https://quarto.org/docs/authoring/cross-references.html#tables)
- [Pandoc List Tables](https://github.com/pandoc-ext/list-table)
