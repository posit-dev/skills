# bslib Best Practices and Common Gotchas

This reference covers bslib-specific layout patterns, UX tips, and common pitfalls. For general Shiny best practices (reactive expressions, modules, deployment), refer to standard Shiny documentation.

## Table of Contents

- [Layout Patterns](#layout-patterns)
- [Mobile and Responsive Design](#mobile-and-responsive-design)
- [User Experience with bslib Components](#user-experience-with-bslib-components)
- [bslib Module Patterns](#bslib-module-patterns)
- [Common Gotchas](#common-gotchas)

## Layout Patterns

### Dashboard Header with KPIs

Value boxes at top, detailed content below:

```r
page_sidebar(
  class = "bslib-page-dashboard",  # Light gray background; looks best with cards
  sidebar = sidebar(...),
  # KPIs at top - don't fill
  layout_column_wrap(
    width = 1/4,
    fill = FALSE,
    value_box(title = "Revenue", value = "$125K", theme = "success"),
    value_box(title = "Users", value = "1,234", theme = "primary"),
    value_box(title = "Growth", value = "+18%", theme = "info"),
    value_box(title = "Churn", value = "2.3%", theme = "warning")
  ),
  # Main content fills remaining space
  layout_columns(
    col_widths = c(8, 4),
    card(full_screen = TRUE, card_header("Trend"), plotOutput("trend")),
    card(card_header("Breakdown"), plotOutput("breakdown"))
  )
)
```

### Component-Level Controls

When controls are specific to one visualization, use `layout_sidebar()` within the card:

```r
card(
  full_screen = TRUE,
  card_header("Customizable Plot"),
  layout_sidebar(
    fillable = TRUE,
    sidebar = sidebar(
      position = "right",
      width = "200px",
      selectInput("color_by", "Color by", ...),
      sliderInput("alpha", "Transparency", ...)
    ),
    plotOutput("plot")
  )
)
```

### Tabbed Content Organization

Use navset cards to organize related outputs:

```r
navset_card_underline(
  title = "Sales Analysis",
  full_screen = TRUE,
  nav_panel("Overview", plotOutput("overview")),
  nav_panel("By Region", plotOutput("by_region")),
  nav_panel("By Product", plotOutput("by_product")),
  nav_panel("Raw Data", tableOutput("raw_data"))
)
```

### Multi-Page with Page-Specific Sidebars

Use `layout_sidebar()` within individual pages instead of `page_navbar(sidebar = ...)`:

```r
page_navbar(
  title = "App",
  nav_panel(
    "Analysis",
    layout_sidebar(
      sidebar = sidebar("Analysis controls"),
      card(plotOutput("analysis_plot"))
    )
  ),
  nav_panel(
    "Comparison",
    layout_sidebar(
      sidebar = sidebar("Comparison controls"),
      card(plotOutput("comparison_plot"))
    )
  )
)
```

### Scrolling Page with Card Heights

When content requires scrolling rather than filling:

```r
page_sidebar(
  fillable = FALSE,  # Enable scrolling
  sidebar = sidebar(...),
  card(
    height = 400,
    full_screen = TRUE,
    card_header("Plot 1"),
    plotOutput("plot1")
  ),
  card(
    height = 400,
    full_screen = TRUE,
    card_header("Plot 2"),
    plotOutput("plot2")
  )
)
```

## Mobile and Responsive Design

### Responsive Column Widths

```r
# Auto-adjusting columns based on viewport
layout_column_wrap(
  width = "250px",
  card(...),
  card(...),
  card(...)
)

# Explicit breakpoints
layout_columns(
  col_widths = breakpoints(
    sm = 12,        # Stack on mobile
    md = c(6, 6),   # Two columns on tablet
    lg = c(4, 4, 4) # Three columns on desktop
  ),
  card(...),
  card(...),
  card(...)
)
```

### Mobile-Friendly Designs

* Set `min_height` on cards (e.g., `min_height = 300`) to prevent them from becoming too small on narrow viewports.
* By default, filling is disabled on mobile. Enable `fillable_mobile = TRUE` on the page function only after thorough testing on actual mobile devices.

## User Experience with bslib Components

### Add Contextual Help

Place a `tooltip()` or `popover()` in `card_header()` to provide inline help. Use `tooltip()` for a brief one-line description and `popover()` when secondary controls or longer content are needed:

```r
card_header(
  "Revenue",
  tooltip(
    bsicons::bs_icon("info-circle"),
    "Total revenue from all sources"
  )
)

card_header(
  "Plot",
  popover(
    bsicons::bs_icon("gear"),
    title = "Advanced Options",
    selectInput("option1", "Option 1", ...),
    checkboxInput("option2", "Option 2")
  )
)
```

### Show Loading States

```r
input_task_button("process", "Process Data")
# Automatically shows loading state and prevents duplicate clicks
```

### Toast Notifications for Feedback

```r
observeEvent(input$save, {
  save_data(data())

  show_toast(
    toast("Data saved successfully", header = "Success", type = "success")
  )
})
```

### Handle Empty States with bslib Components

```r
output$empty_message <- renderUI({
  if (nrow(filtered_data()) == 0) {
    card(
      card_body(
        class = "text-center text-muted",
        bsicons::bs_icon("inbox", size = "3em"),
        tags$p("No data matches the selected filters"),
        tags$p("Try adjusting your filter criteria")
      )
    )
  }
})
```

## bslib Module Patterns

When creating Shiny modules with bslib, wrap module UI in cards:

```r
plot_module_ui <- function(id) {
  ns <- NS(id)

  card(
    full_screen = TRUE,
    card_header("Plot"),
    layout_sidebar(
      sidebar = sidebar(
        selectInput(ns("color"), "Color by", ...)
      ),
      plotOutput(ns("plot"))
    )
  )
}
```

Extract theme configuration into a helper:

```r
# theme.R
app_theme <- function() {
  bs_theme(
    version = 5,
    preset = "flatly",
    primary = "#2c3e50",
    base_font = font_google("Lato")
  ) |>
    bs_add_rules(sass::sass_file("www/custom.scss"))
}
```

Create reusable metric helpers:

```r
metric_card <- function(title, value, theme = "primary") {
  value_box(
    title = title,
    value = value,
    theme = theme,
    showcase = bsicons::bs_icon("graph-up")
  )
}
```

## Common Gotchas

### Unnecessary Card Nesting

**Problem:** Wrapping content in `card()` inside a context that already provides a card container.

**Cause:** `navset_card_*()` functions (`navset_card_underline()`, `navset_card_tab()`, `navset_card_pill()`) are already cards. Each `nav_panel()` inside them behaves like a card body. Adding `card()` inside a `nav_panel()` creates a card-within-a-card.

```r
# Wrong: double-nested card
navset_card_underline(
  nav_panel("Plot", card(plotOutput("plot")))
)

# Right: content goes directly in nav_panel
navset_card_underline(
  nav_panel("Plot", plotOutput("plot"))
)
```

More broadly, not every piece of content needs a card. Cards are for grouping and visually separating content at the dashboard level — content that's already inside a card context doesn't need another one.

### Fill Chain Breaks

**Problem:** Output doesn't fill despite being in a filling layout.

**Cause:** A non-fill-carrier element (like `div()`) breaks the fill chain.

```r
# Broken
card_body(
  div(plotOutput("plot"))  # div breaks fill chain
)

# Fixed
card_body(
  as_fill_carrier(
    div(plotOutput("plot"))
  )
)
```

### Value Boxes Expanding Too Much

**Problem:** Value boxes take up too much vertical space in filling layouts.

**Solution:** Set `fill = FALSE` on layout container.

```r
layout_column_wrap(
  width = 1/3,
  fill = FALSE,  # Important!
  value_box(...),
  value_box(...),
  value_box(...)
)
```

### Sidebar on Every Page

**Problem:** Used `page_navbar(sidebar = ...)` but need different sidebars per page.

**Solution:** Use `layout_sidebar()` within individual `nav_panel()` elements.

### Accordion in Sidebar Not Flush

**Problem:** Accordion has extra padding in sidebar.

**Cause:** Accordion is not an immediate child of `sidebar()`.

**Solution:** Place accordion directly in sidebar (not nested in another wrapper).

### fluidRow/column Doesn't Fill

**Problem:** Used `fluidRow()`/`column()` in filling layout.

**Cause:** These legacy functions are incompatible with the bslib fill system.

**Solution:** Use `layout_columns()` instead. See [migration.md](migration.md).

### Plotly Doesn't Resize

**Problem:** Plotly plot doesn't resize in card.

**Solution:** Ensure card has a defined height (from page filling or explicit `height`):

```r
card(
  height = 400,
  card_body(
    plotlyOutput("plot")  # Already a fill item by default
  )
)
```

### Dark Mode Doesn't Affect Plots

**Problem:** Switched to dark mode but plots still use light colors.

**Cause:** `bs_theme()` only controls CSS; `renderPlot()` generates images server-side.

**Solution:** Use the `thematic` package:

```r
# At top of server function
thematic::thematic_shiny()
```

### Custom CSS Overriding Theme

**Problem:** Custom CSS uses hardcoded colors that don't adapt to theme changes.

**Solution:** Use `bs_add_rules()` with Sass variables instead of raw CSS:

```r
theme <- bs_theme(...) |>
  bs_add_rules("
    .custom-element {
      background: $bg;
      color: $fg;
      border-color: $primary;
    }
  ")
```

### uiOutput Breaks Fill

**Problem:** Dynamic UI via `uiOutput()` breaks filling behavior.

**Cause:** `uiOutput()` wraps content in an extra element that isn't a fill carrier.

**Solution:** Wrap it as a fill carrier:

```r
card_body(
  as_fill_carrier(
    uiOutput("dynamic_plot")
  )
)
```

### DT DataTable Doesn't Fill

**Problem:** DataTable doesn't resize to fill card.

**Solution:** Set `fillContainer = TRUE` in `datatable()`:

```r
output$table <- DT::renderDataTable({
  DT::datatable(
    data,
    fillContainer = TRUE,
    options = list(scrollY = "300px")
  )
})
```
