# Grid Layouts in bslib

This reference covers the multi-column layout systems in bslib for arranging cards, value boxes, and other UI elements in responsive grid patterns.

## Table of Contents

- [layout_column_wrap()](#layout_column_wrap)
  - [Fixed Number of Columns](#fixed-number-of-columns)
  - [Responsive Columns](#responsive-columns)
  - [Height Control](#height-control)
  - [Varying Column Widths](#varying-column-widths)
  - [Nested Layouts](#nested-layouts)
- [layout_columns()](#layout_columns)
  - [Basic Grid System](#basic-grid-system)
  - [Row Heights](#row-heights)
  - [Negative Space](#negative-space)
  - [Responsive Layouts](#responsive-layouts)
- [Choosing Between layout_column_wrap() and layout_columns()](#choosing-between-layout_column_wrap-and-layout_columns)

## layout_column_wrap()

**Purpose:** Creates grid-based layouts optimized for displaying multiple UI elements with uniform sizing. Provides a simplified interface to CSS Grid.

**Recommended use:** Most common for arranging cards and value boxes with consistent sizing. Easier and provides a cleaner uniform look than `layout_columns()`.

### Fixed Number of Columns

Use `width = 1/n` where n is the desired column count.

**Example - 2 columns:**
```r
layout_column_wrap(
  width = 1/2,
  height = 300,
  card(...),
  card(...),
  card(...)  # Wraps to new row
)
```

**Example - 3 columns:**
```r
layout_column_wrap(
  width = 1/3,
  value_box(title = "Users", value = "1,234"),
  value_box(title = "Revenue", value = "$56K"),
  value_box(title = "Growth", value = "+12%")
)
```

**Important:** Do NOT use percent-based widths like `"50%"` instead of `1/2`. Percentages won't produce expected results.

**Drawback:** On medium-sized screens, card width may become too small with fixed column counts.

### Responsive Columns

Provide a CSS unit (e.g., `"200px"`, `"300px"`) to make column count adapt to viewport size. Cards equally distribute free space on wider screens and wrap when space is insufficient.

**Example:**
```r
layout_column_wrap(
  width = "250px",
  height = 300,
  card(...),
  card(...),
  card(...),
  card(...)
)
```

This creates as many columns as will fit given the minimum 250px width, automatically adjusting from 4 columns on wide screens → 3 → 2 → 1 as the viewport narrows.

**Fixed column width:**
Set `fixed_width = TRUE` to prevent cards from growing beyond the specified width:

```r
layout_column_wrap(
  width = "200px",
  height = 300,
  fixed_width = TRUE,
  card(...),
  card(...),
  card(...)
)
```

### Height Control

By default, all rows are given equal height — all cards in all rows match the height of the tallest card. Set `heights_equal = "row"` to allow each row to have its own independent height instead.

Since cards are fill items by default (`fill = TRUE`), they stretch to fill row height. Set `fill = FALSE` on individual cards to prevent stretching:

```r
layout_column_wrap(
  width = 1/2,
  card(fill = FALSE,
    card_header("Short card"),
    "This won't stretch"
  ),
  card(
    card_header("Tall card"),
    lorem::ipsum(paragraphs = 5)
  )
)
```

### Varying Column Widths

For unequal column sizing, set `width = NULL` and provide a custom `grid-template-columns` CSS property:

```r
layout_column_wrap(
  width = NULL,
  height = 300,
  fill = FALSE,
  style = css(grid_template_columns = "2fr 1fr 2fr"),
  card(...),  # 2x width
  card(...),  # 1x width
  card(...)   # 2x width
)
```

### Nested Layouts

Create complex arrangements by nesting `layout_column_wrap()`:

```r
layout_column_wrap(
  width = 1/2,
  height = 300,
  card(...),  # Left column
  layout_column_wrap(  # Right column contains 2 stacked cards
    width = 1,
    heights_equal = "row",
    card(...),
    card(...)
  )
)
```

### Responsive/Mobile Behavior

At small window widths, all layouts collapse into a mobile-friendly "show each card at maximum width" approach, stacking cards vertically.

## layout_columns()

**Purpose:** More flexible grid system based on Bootstrap's 12-column grid. Better for complex layouts requiring precise control.

### Basic Grid System

Without specifying `col_widths`, space is divided evenly among children. Supply `col_widths` to allocate columns out of a 12-column grid — common patterns include `c(6, 6)` for two equal columns, `c(4, 8)` for a sidebar/main split, `c(4, 4, 4)` for three equal columns, or `c(12, 4, 4, 4)` for a full-width top row followed by three equal columns below. Elements whose widths exceed 12 columns wrap to a new row.

```r
layout_columns(
  col_widths = c(4, 8, 12),
  card(...),   # 4/12 width (33%)
  card(...),   # 8/12 width (67%)
  card(...)    # 12/12 width (100%, new row)
)
```

**Common patterns:**
```r
# Two equal columns
col_widths = c(6, 6)

# Sidebar + main (1:2 ratio)
col_widths = c(4, 8)

# Three equal columns
col_widths = c(4, 4, 4)

# Full width top, three equal below
col_widths = c(12, 4, 4, 4)
```

### Row Heights

Customize with `row_heights` (numeric values are fractional units):

```r
layout_columns(
  col_widths = c(4, 8, 12),
  row_heights = c(2, 3),
  card(card_header("Sidebar"), height = "100%"),
  card(card_header("Main plot"), plotOutput("main")),
  card(card_header("Full width table"), tableOutput("table"))
)
```

### Negative Space

Negative `col_widths` create empty space, useful for gutters or visual separation:

```r
layout_columns(
  col_widths = c(4, 8, -2, 8, -2),
  card(...),  # 4 cols
  card(...),  # 8 cols
  # 2 cols empty space
  card(...),  # 8 cols (new row)
  # 2 cols empty space (new row)
)
```

### Responsive Layouts

Use `breakpoints()` to specify different widths at different screen sizes:

```r
layout_columns(
  col_widths = breakpoints(
    sm = c(12, 12),     # Small screens: stack vertically
    md = c(6, 6),       # Medium screens: two columns
    lg = c(4, 8)        # Large screens: sidebar + main
  ),
  card(...),
  card(...)
)
```

**Bootstrap breakpoints:**
- `xs`: < 576px (extra small - phones)
- `sm`: ≥ 576px (small - phones landscape)
- `md`: ≥ 768px (medium - tablets)
- `lg`: ≥ 992px (large - desktops)
- `xl`: ≥ 1200px (extra large - large desktops)
- `xxl`: ≥ 1400px (extra extra large)

## Choosing Between layout_column_wrap() and layout_columns()

### Use layout_column_wrap() when:
- You want uniform sizing across cards/value boxes
- You want simple responsive behavior (auto-wrapping)
- You're building a dashboard with consistent card sizes
- You want cleaner, more readable code

**Example use case:** Dashboard with multiple value boxes or cards showing metrics.

### Use layout_columns() when:
- You need precise control over column widths
- You want different column proportions (e.g., 4-8 sidebar-main split)
- You need negative space or complex grid patterns
- You want fine-grained responsive behavior with different layouts per breakpoint

**Example use case:** Complex dashboard layout with sidebar, main content, and multiple regions with specific proportions.

### Common Pattern: Combine Both

Use `layout_columns()` for overall page structure and `layout_column_wrap()` for uniform content sections:

```r
page_fillable(
  layout_columns(
    col_widths = c(12, 4, 8),
    # Full-width header with value boxes
    layout_column_wrap(
      width = 1/3,
      value_box(...),
      value_box(...),
      value_box(...)
    ),
    # Left sidebar
    card(...),
    # Main content with multiple plots
    layout_column_wrap(
      width = 1/2,
      card(...),
      card(...),
      card(...),
      card(...)
    )
  )
)
```

## Beyond These Functions

For layouts exceeding what these functions can handle, consider:
- The `{gridlayout}` package for more complex CSS Grid configurations
- The Shiny UI editor for visual layout design
- Custom CSS Grid properties via `style` parameter
