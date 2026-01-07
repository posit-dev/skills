# Layout

Quarto provides column classes for controlling content width and placement, including margin content.

## Column Classes

### Available Columns

| Class                  | Description                     |
| ---------------------- | ------------------------------- |
| `.column-body`         | Default body width              |
| `.column-body-outset`  | Slightly wider than body        |
| `.column-page`         | Page width (narrower than full) |
| `.column-page-inset`   | Page width with inset           |
| `.column-screen`       | Full screen width               |
| `.column-screen-inset` | Screen width with margins       |
| `.column-margin`       | Right margin                    |

### Body Column (Default)

Standard content width:

````markdown
::: {.column-body}
Default body-width content.
:::
````

### Body Outset

Slightly wider than body:

````markdown
::: {.column-body-outset}
![Wide image](wide.png)
:::
````

### Page Width

Extends to page margins:

````markdown
::: {.column-page}
![Page-width image](panorama.png)
:::
````

### Screen Width

Full browser width (no margins):

````markdown
::: {.column-screen}
![Full-width image](banner.png)
:::
````

### Screen Inset

Full width with small margins:

````markdown
::: {.column-screen-inset}
Content with small margins.
:::
````

### Shaded Screen Inset

With background shading:

````markdown
::: {.column-screen-inset-shaded}
Shaded full-width content.
:::
````

## Directional Variants

Each column class has left/right variants:

````markdown
::: {.column-body-outset-left}
Extends left only.
:::

::: {.column-page-right}
Extends to right page margin.
:::

::: {.column-screen-left}
Full width on left side.
:::
````

## Margin Content

### Text in Margin

````markdown
::: {.column-margin}
This appears in the right margin.
:::
````

### Figures in Margin

````markdown
```{r}
#| column: margin
#| fig-cap: "Margin figure."

plot(1:10)
```
````

Or for markdown images:

````markdown
::: {.column-margin}
![Margin image](small.png)
:::
````

### Tables in Margin

````markdown
```{r}
#| column: margin
#| tbl-cap: "Margin table."

knitr::kable(small_data)
```
````

### Mixed Content

````markdown
Main text here.

::: {.column-margin}
Margin note explaining the main content.
:::

More main text.
```

## Code Cell Layout Options

Control output placement from code cells:

### Column Option

````markdown
```{r}
#| column: page

# Output spans page width
plot(1:100)
```
````

Options: `body`, `body-outset`, `page`, `page-inset`, `screen`, `screen-inset`, `margin`.

### Figure Column

Target figure outputs specifically:

````markdown
```{r}
#| fig-column: margin

plot(1:10)
```
````

### Table Column

Target table outputs:

````markdown
```{r}
#| tbl-column: page

knitr::kable(wide_data)
```
````

## Caption Location

### In Margin

````markdown
```{r}
#| fig-cap: "Figure with margin caption."
#| cap-location: margin

plot(1:10)
```
````

### Document Default

```yaml
fig-cap-location: margin
tbl-cap-location: margin
```

## References in Margin

### Footnotes in Margin

```yaml
reference-location: margin
```

### Citations in Margin

```yaml
citation-location: margin
```

### Combined

```yaml
reference-location: margin
citation-location: margin
```

## Page Layout

### Document-Wide Settings

```yaml
format:
  html:
    page-layout: article   # Default
    page-layout: full      # Full width
    page-layout: custom    # Custom layout
```

### Grid Customization

```yaml
format:
  html:
    grid:
      sidebar-width: 300px
      body-width: 800px
      margin-width: 300px
      gutter-width: 1.5rem
```

## Two-Column Layout

Create side-by-side columns:

````markdown
::: {.columns}

::: {.column width="50%"}
Left column content.
:::

::: {.column width="50%"}
Right column content.
:::

:::
````

### Unequal Columns

````markdown
::: {.columns}

::: {.column width="30%"}
Narrow column.
:::

::: {.column width="70%"}
Wide column.
:::

:::
````

## Content Layout Divs

Arrange any content (images, tables, text) in grid layouts.

### Column Layout

````markdown
::: {layout-ncol=2}
![](image1.png)

![](image2.png)
:::
````

### Row Layout

````markdown
::: {layout-nrow=2}
Content 1.

Content 2.
:::
````

### Complex Layouts

Use layout array for precise control. Values represent relative widths:

````markdown
::: {layout="[[1,1], [1]]"}
First row, left.

First row, right.

Second row, full width.
:::
````

### With Spacing

Negative values add spacing between elements:

````markdown
::: {layout="[[40,-20,40], [100]]"}
Content 1.

Content 2.

Full width below.
:::
````

### Vertical Alignment

````markdown
::: {layout-ncol=2 layout-valign="bottom"}
Tall content.

Short content.
:::
````

Options: `top`, `center`, `bottom`.

### Layout Attributes

| Attribute       | Description            | Example                |
| --------------- | ---------------------- | ---------------------- |
| `layout-ncol`   | Number of columns      | `layout-ncol=3`        |
| `layout-nrow`   | Number of rows         | `layout-nrow=2`        |
| `layout`        | Custom layout array    | `layout="[[1,2],[1]]"` |
| `layout-valign` | Vertical alignment     | `layout-valign=center` |

## Tabsets

Create tabbed content:

````markdown
::: {.panel-tabset}

## Tab 1

Content for tab 1.

## Tab 2

Content for tab 2.

:::
````

### With Groups

````markdown
::: {.panel-tabset group="language"}

## R

```r
x <- 1
```

## Python

```python
x = 1
```

:::

````

Tabs with same group stay synchronized.

## Asides

For inline margin notes:

````markdown
Main text content.
[This is an aside that appears in the margin.]{.aside}
More main text.
````

## PDF Layout

PDF uses different layout system. Key options:

```yaml
format:
  pdf:
    documentclass: article
    geometry:
      - margin=1in
    classoption:
      - twocolumn
```

### Margin Notes in PDF

```yaml
format:
  pdf:
    documentclass: scrartcl # KOMA-Script
```

KOMA classes support margin content automatically.

## Examples

### Article with Margin Notes

```yaml
format:
  html:
    page-layout: article
reference-location: margin
citation-location: margin
```

### Wide Figures

````markdown
::: {.column-page}

```{r}
#| fig-width: 12
#| fig-height: 6

ggplot(data) + geom_point()
```

:::

````

### Dashboard-Style Layout

```yaml
format:
  html:
    page-layout: full
```

## Resources

- [Quarto Article Layout](https://quarto.org/docs/authoring/article-layout.html)
- [Page Layout](https://quarto.org/docs/output-formats/page-layout.html)
- [Figures Layout](https://quarto.org/docs/authoring/figures.html#figure-panels)
