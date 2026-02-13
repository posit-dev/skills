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

When multiple fill items share a fillable container, they divide the available space equally:

**Example:**
```r
card(
  height = 400,
  card_body(plotOutput("plot1")),  # Gets 200px
  card_body(plotOutput("plot2"))   # Gets 200px
)
```

### Mixed Fill and Non-Fill Items

Non-fill items keep their natural size. Fill items divide whatever space remains.

**Example:**
```r
card(
  height = 400,
  # Non-fill header (50px natural height)
  card_header("Title"),
  # Fill item gets remaining 350px
  card_body(plotOutput("plot"))
)
```

**Warning:** If non-fill items are larger than the container, fill items won't be visible!

**Problematic example:**
```r
card(
  height = 300,
  card_body(fill = FALSE, lorem::ipsum(paragraphs = 10)),  # 500px content
  card_body(plotOutput("plot"))  # Not visible!
)
```

## Fill Carriers

### The Problem

Fill items require their **immediate parent** to be a fillable container. Non-fill elements between a fillable container and fill item break the chain.

**Broken chain example:**
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

A **fill carrier** is both a fill item and a fillable container, preserving the fill chain.

**Fixed example:**
```r
card(
  height = 400,
  card_body(
    # Make the div a fill carrier
    as_fill_carrier(
      div(
        plotOutput("plot")  # Now fills properly
      )
    )
  )
)
```

**Automatic fill carrier:** `card_body()` is a fill carrier by default (both `fillable = TRUE` and `fill = TRUE`).

## Key Components and Their Fill Behavior

### page_fillable()

- **Is fillable:** Yes
- **Is fill item:** N/A (top level)
- **Behavior:** Sets height to browser viewport, activating fill for direct children
- **Mobile:** Disabled by default (`fillable_mobile = FALSE`)

**Example:**
```r
page_fillable(
  card(plotOutput("plot"))  # Fills viewport
)
```

### card() and card_body()

- **Is fillable:** Yes (default `fillable = TRUE`)
- **Is fill item:** Yes (default `fill = TRUE`)
- **Role:** Fill carriers by default
- **Behavior:** Grow/shrink themselves AND allow children to do the same

**Example:**
```r
page_fillable(
  card(  # Fills page
    card_header("Plot"),
    card_body(  # Fills card
      plotOutput("plot")  # Fills card_body
    )
  )
)
```

### layout_columns()

- **Is fillable:** Yes (default `fillable = TRUE`)
- **Is fill item:** Yes (default)
- **Behavior:** Each column wrapped in a fillable container

**Example:**
```r
page_fillable(
  layout_columns(
    card(plotOutput("plot1")),
    card(plotOutput("plot2"))
  )
)
```

### layout_column_wrap()

- **Is fillable:** Depends on context
- **Is fill item:** Yes (default `fill = TRUE`)
- **Behavior:** Children can be fill items

**Example:**
```r
page_fillable(
  layout_column_wrap(
    width = 1/2,
    card(plotOutput("plot1")),
    card(plotOutput("plot2"))
  )
)
```

### layout_sidebar()

- **Is fillable:** Main content area is fillable by default
- **Is fill item:** Yes (default)
- **Behavior:** Allows outputs in main area to fill

**Example:**
```r
card(
  height = 400,
  layout_sidebar(
    fillable = TRUE,  # Ensure main area is fillable
    sidebar = sidebar("Controls"),
    plotOutput("plot")  # Fills main area
  )
)
```

### value_box()

- **Is fillable:** Depends
- **Is fill item:** Yes (default)
- **Behavior:** Maintains common baseline in multi-column layouts

**Example:**
```r
layout_column_wrap(
  width = 1/3,
  value_box(title = "Users", value = "1,234"),
  value_box(title = "Revenue", value = "$56K"),
  value_box(title = "Growth", value = "+12%")
)
```

All value boxes maintain equal height.

## When Filling May Not Be Desired

### Flexbox Side Effects

Fillable containers use CSS flexbox, which changes child rendering:
- Inline elements appear on separate lines
- Normal flow is disrupted

**Solution:** Use `fillable = FALSE` when needed:
```r
card_body(
  fillable = FALSE,
  "Text with ", tags$a("inline link"), " and more text."
)
```

### Value Boxes in Filling Layouts

Value boxes shouldn't expand excessively. Set `fill = FALSE` on the layout container:

**Example:**
```r
page_fillable(
  # Value boxes at top - fixed height
  layout_column_wrap(
    width = 1/3,
    fill = FALSE,  # Important!
    value_box(title = "KPI 1", value = "123"),
    value_box(title = "KPI 2", value = "456"),
    value_box(title = "KPI 3", value = "789")
  ),
  # Plot fills remaining space
  card(plotOutput("main_plot"))
)
```

### Disabling Filling for Scrolling

Switch from `page_fillable()` to `page_fluid()` or `page_fixed()` to disable filling:

**Example:**
```r
page_fluid(  # Scrolling page
  card(plotOutput("plot1")),  # 400px default
  card(plotOutput("plot2")),  # 400px default
  card(plotOutput("plot3")),  # 400px default
  # Page scrolls
)
```

Even without page-level filling, cards with `full_screen = TRUE` still fill when expanded.

## Scrolling vs Filling

### Filling Layout

**Characteristics:**
- Content adapts to viewport size
- No page scrolling (when content fits)
- Professional dashboard feel
- Requires careful height management

**Example:**
```r
page_fillable(
  layout_columns(
    col_widths = c(4, 8),
    card(height = "100%", "Sidebar content"),
    card(plotlyOutput("plot"))
  )
)
```

### Scrolling Layout

**Characteristics:**
- Content uses natural heights
- Page scrolls vertically
- Simpler to implement
- Better for long-form content

**Example:**
```r
page_fluid(
  card(plotOutput("plot1")),
  card(plotOutput("plot2")),
  card(plotOutput("plot3")),
  card(plotOutput("plot4"))
)
```

### Hybrid Approach

**Mixed scrolling and filling:**
```r
page_sidebar(
  fillable = FALSE,  # Page scrolls
  sidebar = sidebar("Controls"),
  # Each card can still use filling internally
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

`uiOutput()` wraps content in an extra element, breaking the fill chain.

**Solution:** Mark it as a fill carrier:
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

**Example:**
```r
# Server
output$table <- DT::renderDataTable({
  DT::datatable(
    data,
    fillContainer = TRUE,  # Required!
    options = list(scrollY = "300px")
  )
})
```

### htmlwidgets

Most htmlwidgets are fill items by default, but behavior can be controlled:

**Disable filling for specific widget:**
```r
card_body(
  remove_all_fill(plotlyOutput("plot"))
)
```

**Enable filling explicitly:**
```r
card_body(
  as_fill_item(custom_widget_output("widget"))
)
```

### fluidRow() and column()

The traditional Shiny grid system is "mostly incompatible" with filling layout due to Bootstrap's flexbox grid.

**Solution:** Use `layout_columns()` instead:

**Avoid:**
```r
page_fillable(
  fluidRow(  # Incompatible with filling
    column(6, plotOutput("plot1")),
    column(6, plotOutput("plot2"))
  )
)
```

**Prefer:**
```r
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

**Symptoms:** Output stays at default height despite being in filling layout.

**Common causes:**
1. Container doesn't have defined height
2. Broken fill chain (non-fill carrier in between)
3. Output isn't a fill item by default

**Solutions:**
```r
# 1. Ensure container has height
card(
  height = 400,  # Add explicit height
  plotOutput("plot")
)

# 2. Fix fill chain
card_body(
  as_fill_carrier(
    div(
      plotOutput("plot")
    )
  )
)

# 3. Mark output as fill item
card_body(
  as_fill_item(custom_output("out"))
)
```

### Output Too Small

**Symptoms:** Fill item shrinks below usable size.

**Solution:** Set `min_height`:
```r
card_body(
  min_height = 300,
  plotOutput("plot")
)
```

### Multiple Outputs Not Dividing Space

**Symptoms:** Only one output visible or unequal spacing.

**Solution:** Ensure all are fill items in same fillable container:
```r
card_body(
  plotOutput("plot1"),  # Fill item
  plotOutput("plot2"),  # Fill item
  plotOutput("plot3")   # Fill item
  # All three divide space equally
)
```

### Full-Screen Mode Not Working

**Symptoms:** Full-screen button doesn't appear or doesn't work properly.

**Solution:** Ensure card contains fill items:
```r
card(
  full_screen = TRUE,
  card_header("Plot"),
  plotlyOutput("plot")  # Must be a fill item
)
```

## Best Practices

### Use Filling for Dashboards

Filling layouts create professional dashboards:
```r
page_fillable(
  layout_columns(
    col_widths = c(12, 4, 8),
    # Header with KPIs
    layout_column_wrap(
      width = 1/3,
      fill = FALSE,
      value_box(...), value_box(...), value_box(...)
    ),
    # Sidebar
    card(...),
    # Main plot
    card(plotlyOutput("main"))
  )
)
```

### Set Appropriate Heights

Use these height constraints:
- `height`: Fixed height
- `min_height`: Minimum height (prevents shrinking too small)
- `max_height`: Maximum height (enables scrolling when exceeded)

**Example:**
```r
card(
  min_height = 300,  # Don't shrink below 300px
  max_height = 600,  # Scroll if content exceeds 600px
  verbatimTextOutput("output")
)
```

### Test Fill Behavior

Always test:
- Different viewport sizes
- Content with varying amounts of data
- Full-screen expansion
- Mobile devices

### Use page_fillable() for Single-Page Apps

Best for:
- Dashboards
- Data exploration apps
- Apps where all content should be visible

### Use page_fluid() for Long-Form Content

Best for:
- Reports with many sections
- Documentation
- Apps with extensive text content
- When natural scrolling is preferred

### Combine Approaches

Use filling layouts for main dashboard areas and scrolling for detail pages:

```r
page_navbar(
  title = "App",
  fillable = c("Dashboard"),  # Only "Dashboard" page fills
  nav_panel("Dashboard",
    layout_columns(...)  # Content fills viewport
  ),
  nav_panel("Details",
    # Scrolling layout (not in fillable list)
    card(...), card(...), card(...)
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

When wrapping outputs, ensure the wrapper is a fill carrier:

**Problematic:**
```r
card_body(
  div(class = "my-wrapper",
    plotOutput("plot")  # Won't fill
  )
)
```

**Fixed:**
```r
card_body(
  as_fill_carrier(
    div(class = "my-wrapper",
      plotOutput("plot")  # Fills properly
    )
  )
)
```

### Document Fill Behavior

When creating custom components, document whether they're:
- Fillable containers
- Fill items
- Fill carriers
- None of the above

This helps other developers use them correctly in filling layouts.
