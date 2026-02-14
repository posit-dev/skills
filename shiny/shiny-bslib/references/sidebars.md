# Sidebars in bslib

Sidebars organize inputs and controls in Shiny dashboards. bslib provides flexible sidebar layouts at multiple levels: page-level, component-level, and within cards.

## Table of Contents

- [Basic Sidebar Usage](#basic-sidebar-usage)
- [Page-Level Sidebars](#page-level-sidebars)
- [Component-Level Sidebars](#component-level-sidebars)
- [Varied Sidebars Across Pages](#varied-sidebars-across-pages)
- [Conditional Sidebar Contents](#conditional-sidebar-contents)
- [Reactive Open/Close](#reactive-openclose)
- [Accordions in Sidebars](#accordions-in-sidebars)
- [Nested Sidebars](#nested-sidebars)
- [Styling](#styling)
- [Best Practices](#best-practices)

## Basic Sidebar Usage

```r
sidebar(
  title = "Controls",
  open = TRUE,
  position = "left",
  selectInput("var", "Variable", choices = names(data)),
  sliderInput("bins", "Bins", min = 1, max = 50, value = 30)
)
```

**Key parameters:**

| Parameter | Default | Description |
|---|---|---|
| `title` | `NULL` | Title at top |
| `open` | `TRUE` | Initial state: `TRUE`, `FALSE`, `"desktop"`, `"closed"`, `"always"` |
| `position` | `"left"` | `"left"` or `"right"` |
| `width` | `"250px"` | CSS width. Users can resize by dragging the edge |
| `id` | `NULL` | For programmatic control via `toggle_sidebar()` |
| `bg` | | Background color (auto-contrasts `fg`) |
| `fg` | | Foreground color |
| `fillable` | `FALSE` | Whether contents fill vertically |
| `gap` | | CSS spacing between children |
| `padding` | | CSS padding within sidebar |

## Page-Level Sidebars

### page_sidebar()

Most common pattern for single-page dashboards:

```r
page_sidebar(
  title = "My Dashboard",
  sidebar = sidebar(
    title = "Filters",
    selectInput("species", "Species", choices = unique(penguins$species)),
    selectInput("island", "Island", choices = unique(penguins$island))
  ),
  card(full_screen = TRUE, card_header("Plot"), plotOutput("scatter")),
  card(card_header("Summary"), verbatimTextOutput("summary"))
)
```

### page_navbar() with Sidebar

Sidebar visible on **all** pages:

```r
page_navbar(
  title = "Multi-Page App",
  sidebar = sidebar(
    title = "Global Filters",
    selectInput("region", "Region", choices = regions),
    dateRangeInput("dates", "Date range")
  ),
  nav_panel("Overview", overview_ui),
  nav_panel("Details", details_ui)
)
```

**Caveat:** `page_navbar(sidebar = ...)` puts the same sidebar on every page. See [Varied Sidebars Across Pages](#varied-sidebars-across-pages) for per-page alternatives.

## Component-Level Sidebars

### layout_sidebar() in Cards

Keep controls close to the outputs they affect:

```r
card(
  full_screen = TRUE,
  card_header("Customizable Plot"),
  layout_sidebar(
    fillable = TRUE,  # Important for fill behavior
    sidebar = sidebar(
      position = "right",
      width = "200px",
      selectInput("color", "Color scheme", ...),
      sliderInput("alpha", "Transparency", ...)
    ),
    plotlyOutput("plot")
  )
)
```

**Key insight:** Set `fillable = TRUE` on `layout_sidebar()` to preserve fill behavior for outputs like plotly, leaflet, etc.

### layout_sidebar() in Filling Pages

`page_sidebar()` is a convenience wrapper around `page_fillable()` + `layout_sidebar()`. Use this directly for more control:

```r
page_fillable(
  layout_sidebar(
    sidebar = sidebar("Sidebar content"),
    layout_columns(card(...), card(...))
  )
)
```

## Varied Sidebars Across Pages

When different pages need different sidebars, place `layout_sidebar()` within individual pages instead of using `page_navbar(sidebar = ...)`.

**Some pages with sidebars, some without:**
```r
page_navbar(
  title = "App",
  fillable = c("Analysis", "Comparison"),
  nav_panel(
    "Analysis",
    layout_sidebar(
      sidebar = sidebar(title = "Analysis Controls", selectInput("metric", "Metric", ...)),
      card(plotOutput("analysis_plot"))
    )
  ),
  nav_panel(
    "Comparison",
    layout_sidebar(
      sidebar = sidebar(title = "Comparison Controls", selectInput("compare_by", "Compare by", ...)),
      card(plotOutput("comparison_plot"))
    )
  ),
  nav_panel("About", "No sidebar on this page")
)
```

## Conditional Sidebar Contents

Change sidebar contents based on the active page using `conditionalPanel()`:

```r
page_navbar(
  title = "App",
  id = "nav",  # Required: enables tracking active page
  sidebar = sidebar(
    conditionalPanel(
      "input.nav === 'Scatter'",
      selectInput("x_var", "X variable", ...),
      selectInput("y_var", "Y variable", ...)
    ),
    conditionalPanel(
      "input.nav === 'Histogram'",
      selectInput("hist_var", "Variable", ...),
      sliderInput("bins", "Bins", ...)
    )
  ),
  nav_panel("Scatter", plotOutput("scatter")),
  nav_panel("Histogram", plotOutput("histogram"))
)
```

**Key:** Navigation container must have an `id`. JavaScript conditions use `===` and string values matching panel titles exactly.

## Reactive Open/Close

Programmatically toggle sidebar visibility with `toggle_sidebar()` (requires `id` on the sidebar):

```r
ui <- page_navbar(
  title = "App",
  id = "nav",
  sidebar = sidebar(id = "main_sidebar", open = FALSE, "Content"),
  nav_panel("Page 1", "Sidebar starts closed"),
  nav_panel("Page 2", "Sidebar opens automatically")
)

server <- function(input, output, session) {
  observe({
    toggle_sidebar("main_sidebar", open = input$nav == "Page 2")
  })
}
```

## Accordions in Sidebars

When `accordion()` is an immediate child of `sidebar()`, panels render flush for clean organization:

```r
sidebar(
  title = "Controls",
  accordion(
    accordion_panel(
      "Data Filters",
      selectInput("species", "Species", ...),
      dateRangeInput("dates", "Date range", ...)
    ),
    accordion_panel(
      "Plot Options",
      selectInput("color", "Color by", ...),
      sliderInput("alpha", "Transparency", ...)
    ),
    accordion_panel(
      "Advanced",
      checkboxInput("show_outliers", "Show outliers"),
      numericInput("threshold", "Threshold", ...)
    )
  )
)
```

**Gotcha:** Accordion must be an immediate child of `sidebar()` for flush rendering. Wrapping in another element adds extra padding.

See [accordions.md](accordions.md) for more.

## Nested Sidebars

Create dual left/right sidebars by nesting `layout_sidebar()`:

```r
page_fillable(
  layout_sidebar(
    sidebar = sidebar(title = "Left Sidebar", "Primary controls"),
    layout_sidebar(
      sidebar = sidebar(title = "Right Sidebar", position = "right", open = FALSE, "Secondary controls"),
      card(plotOutput("main_plot")),
      border = FALSE
    ),
    border_radius = FALSE,
    fillable = TRUE,
    class = "p-0"
  )
)
```

Use `fillable = TRUE`, `class = "p-0"`, and `border = FALSE` for seamless nesting.

## Styling

**Background color** (auto-contrasts `fg`):
```r
sidebar(bg = "#f8f9fa", ...)
sidebar(bg = "primary", ...)    # Theme color name
```

**Width:**
```r
sidebar(width = "300px", ...)   # Fixed
sidebar(width = "20%", ...)     # Proportional
```

**Bootstrap utility classes:**
```r
sidebar(class = "border-start border-3 border-primary", ...)
```

## Best Practices

**Organize many inputs with accordions:**
```r
sidebar(
  accordion(
    accordion_panel("Essential", essential_inputs),
    accordion_panel("Advanced", advanced_inputs)
  )
)
```

**Handle sidebar state responsively:**
- `open = "desktop"` — open on desktop, closed on mobile (good default)
- `open = FALSE` — start closed for secondary sidebars
- `open = "always"` — no collapse button

**Use right sidebars** for secondary/optional controls, keeping content focus on the left.

**When the sidebar gets crowded:**
1. Use accordions to group inputs
2. Move less important controls into card header popovers
3. Split into multiple pages with page-specific sidebars

**Card header popover for advanced options:**
```r
card(
  card_header(
    "Plot",
    popover(
      bsicons::bs_icon("gear"),
      title = "Advanced Options",
      sliderInput("param", "Parameter", ...)
    )
  ),
  plotOutput("plot")
)
```
