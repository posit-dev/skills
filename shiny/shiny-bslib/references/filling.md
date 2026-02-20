# Filling Layouts in bslib

Understanding fillable containers and fill items is crucial for creating modern, responsive bslib dashboards. This reference explains how the fill system works and when to use it.

## Table of Contents

- [Core Concepts](#core-concepts)
- [How Fill Activation Works](#how-fill-activation-works)
- [Fill Carriers](#fill-carriers)
- [Key Components and Their Fill Behavior](#key-components-and-their-fill-behavior)
- [When Filling May Not Be Desired](#when-filling-may-not-be-desired)
- [Scrolling vs Filling](#scrolling-vs-filling)
- [Special Cases](#special-cases)
- [Troubleshooting Fill Issues](#troubleshooting-fill-issues)
- [Best Practices](#best-practices)

## Core Concepts

**Fillable container:** A CSS flexbox container (`flex-direction: column`) that can make its children grow or shrink.

**Fill item:** A child element with `flex: 1` that can grow or shrink to match its parent's height.

**Fill carrier:** An element that is both a fill item AND a fillable container, allowing fill behavior to propagate through the UI hierarchy.

### Technical Implementation

Technically, a fillable container is a `div()` with:
```css
display: flex;
flex-direction: column;
```

A fill item has:
```css
flex: 1;
```

This CSS flexbox system enables dynamic resizing.

## How Fill Activation Works

### The Key Rule

**Fill only activates when the container has a defined height.**

By default, a fillable container's height depends on its children's heights (normal HTML behavior). Fill behavior activates when you constrain the container's height.

**Example without height constraint:**
```r
page_fluid(  # No height constraint
  plotOutput("plot")  # Uses default 400px height
)
```

**Example with height constraint:**
```r
page_fillable(  # Height set to viewport
  plotOutput("plot")  # Fills available space
)
```

### Multiple Fill Items

When multiple fill items share a fillable container, they divide the available space equally. Non-fill items keep their natural size; fill items divide whatever space remains.

**Warning:** If non-fill items are larger than the container, fill items won't be visible:

```r
card(
  height = 300,
  card_body(fill = FALSE, lorem::ipsum(paragraphs = 10)),  # 500px content
  card_body(plotOutput("plot"))  # Not visible!
)
```

## Fill Carriers

### Parent-Child Relationship

Fill items require their **immediate parent** to be a fillable container. Non-fill elements between a fillable container and fill item break the chain:

```r
card(
  height = 400,
  card_body(
    # This div() is not a fill carrier
    div(
      plotOutput("plot")  # Won't fill because parent div isn't fillable
    )
  )
)
```

### The Solution

A **fill carrier** is both a fill item and a fillable container, preserving the fill chain. Use `as_fill_carrier()` to promote any element:

```r
card(
  height = 400,
  card_body(
    as_fill_carrier(
      div(
        plotOutput("plot")  # Now fills properly
      )
    )
  )
)
```

`card_body()` is a fill carrier by default (both `fillable = TRUE` and `fill = TRUE`).

## Key Components and Their Fill Behavior

| Component | Fillable | Fill item | Notes |
|---|---|---|---|
| `page_fillable()` | Yes | N/A | Sets height to viewport; `fillable_mobile = FALSE` by default |
| `card()` | Yes | Yes | Fill carrier by default |
| `card_body()` | Yes | Yes | Fill carrier by default |
| `layout_columns()` | Yes | Yes | Each column wrapped in a fillable container |
| `layout_column_wrap()` | Context-dependent | Yes | Children can be fill items |
| `layout_sidebar()` | Main area yes | Yes | Set `fillable = TRUE` to ensure main area is fillable |
| `value_box()` | Context-dependent | Yes | Maintains equal height in multi-column layouts |

## When Filling May Not Be Desired

### Flexbox Side Effects

Fillable containers use CSS flexbox, which changes child rendering:
- Inline elements appear on separate lines
- Normal flow is disrupted

Use `fillable = FALSE` when needed:

```r
card_body(
  fillable = FALSE,
  "Text with ", tags$a("inline link"), " and more text."
)
```

### Value Boxes in Filling Layouts

Value boxes shouldn't expand to fill the entire page. Use `fill = FALSE` on the wrapping layout container so value boxes keep a natural height and the remaining space goes to other fill items:

```r
page_fillable(
  layout_column_wrap(
    width = 1/3,
    fill = FALSE,  # Important!
    value_box(title = "KPI 1", value = "123"),
    value_box(title = "KPI 2", value = "456"),
    value_box(title = "KPI 3", value = "789")
  ),
  card(plotOutput("main_plot"))  # Fills remaining space
)
```

### Disabling Filling for Scrolling

Switch from `page_fillable()` to `page_fluid()` or `page_fixed()` to get a scrolling page with natural content heights. Even without page-level filling, cards with `full_screen = TRUE` still fill when expanded.

## Scrolling vs Filling

**Filling layout** (`page_fillable()`): content adapts to viewport size with no page scroll — professional dashboard feel, but requires careful height management.

**Scrolling layout** (`page_fluid()` / `page_fixed()`): content uses natural heights and the page scrolls — simpler to implement and better for long-form content.

### Hybrid Approach

Use `fillable = FALSE` on the page but explicit heights on individual cards so each card can still use `full_screen = TRUE` filling:

```r
page_sidebar(
  fillable = FALSE,  # Page scrolls
  sidebar = sidebar("Controls"),
  card(
    height = 400,
    full_screen = TRUE,
    card_header("Plot 1"),
    plotlyOutput("plot1")
  ),
  card(
    height = 400,
    full_screen = TRUE,
    card_header("Plot 2"),
    plotlyOutput("plot2")
  )
)
```

## Special Cases

### Dynamic UI (uiOutput)

`uiOutput()` wraps content in an extra element, breaking the fill chain. Mark it as a fill carrier:

```r
card_body(
  as_fill_carrier(
    uiOutput("dynamic_plot")
  )
)

# Server
output$dynamic_plot <- renderUI({
  plotOutput("plot", height = "100%")
})
```

### DT DataTables

DataTables require explicit configuration to participate in filling:

```r
output$table <- DT::renderDataTable({
  DT::datatable(
    data,
    fillContainer = TRUE,  # Required!
    options = list(scrollY = "300px")
  )
})
```

### htmlwidgets

Most htmlwidgets are fill items by default. Use `remove_all_fill()` to opt a widget out, or `as_fill_item()` to explicitly opt a custom widget in.

### fluidRow() and column()

The traditional Shiny grid system is mostly incompatible with filling layout due to Bootstrap's flexbox grid. Prefer `layout_columns()` instead:

```r
# Avoid
page_fillable(
  fluidRow(
    column(6, plotOutput("plot1")),
    column(6, plotOutput("plot2"))
  )
)

# Prefer
page_fillable(
  layout_columns(
    col_widths = c(6, 6),
    plotOutput("plot1"),
    plotOutput("plot2")
  )
)
```

## Troubleshooting Fill Issues

### Output Not Filling

**Symptoms:** Output stays at default height despite being in a filling layout.

**Common causes and solutions:**

1. **Container has no defined height** — add an explicit `height` to the card or use `page_fillable()`.
2. **Broken fill chain** — wrap the intermediate element with `as_fill_carrier()`.
3. **Output isn't a fill item** — mark it with `as_fill_item()`.

### Output Too Small

**Symptoms:** Fill item shrinks below usable size.

Set `min_height` on the containing `card_body()` to prevent shrinking too small. Similarly, `max_height` enables scrolling when content exceeds a threshold.

### Multiple Outputs Not Dividing Space

**Symptoms:** Only one output visible or unequal spacing.

Ensure all outputs are fill items inside the same fillable container (e.g., directly inside one `card_body()`). Multiple `plotOutput()` calls in a single `card_body()` will divide space equally.

### Full-Screen Mode Not Working

**Symptoms:** Full-screen button doesn't appear or content doesn't fill the expanded card.

Ensure the card contains fill items (e.g., `plotlyOutput()`, `plotOutput()`) and that `full_screen = TRUE` is set on the `card()`.

## Best Practices

### Use Filling for Dashboards

`page_fillable()` creates professional dashboards where content adapts to the viewport. A typical pattern combines a fixed-height KPI row with filling plot cards:

```r
page_fillable(
  layout_columns(
    col_widths = c(12, 4, 8),
    layout_column_wrap(
      width = 1/3,
      fill = FALSE,
      value_box(...), value_box(...), value_box(...)
    ),
    card(...),
    card(plotlyOutput("main"))
  )
)
```

### Set Appropriate Heights

Use `height` for a fixed size, `min_height` to prevent shrinking too small, and `max_height` to cap growth and enable scrolling beyond that point.

### Use page_fillable() for Single-Page Apps

Best for dashboards, data exploration apps, and apps where all content should be visible without scrolling.

### Use page_fluid() for Long-Form Content

Best for reports, documentation, apps with extensive text, or when natural vertical scrolling is preferred.

### Combine Approaches

Use `page_navbar()` with a `fillable` vector to enable filling on specific tabs only:

```r
page_navbar(
  title = "App",
  fillable = c("Dashboard"),  # Only "Dashboard" page fills
  nav_panel("Dashboard",
    layout_columns(...)
  ),
  nav_panel("Details",
    card(...), card(...), card(...)  # Scrolling layout
  )
)
```

### Preserve Fill with layout_sidebar()

When using sidebars inside fillable containers, set `fillable = TRUE`:

```r
card(
  height = 400,
  layout_sidebar(
    fillable = TRUE,  # Important!
    sidebar = sidebar(...),
    plotOutput("plot")
  )
)
```

### Be Mindful of Fill Carriers

When wrapping outputs in custom `div()` elements, use `as_fill_carrier()` on the wrapper; otherwise the fill chain is broken and the output won't resize.

### Document Fill Behavior

When creating custom components, document whether they are fillable containers, fill items, fill carriers, or none of the above, so other developers can use them correctly in filling layouts.
