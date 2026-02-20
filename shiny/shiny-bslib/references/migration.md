# Migrating from Legacy Shiny to Modern bslib

This reference maps legacy Shiny UI patterns to their modern bslib equivalents. Use this when modernizing existing apps or when tempted to use outdated patterns.

## Table of Contents

- [Legacy to Modern Mapping](#legacy-to-modern-mapping)
- [Page Functions](#page-functions)
- [Layout Functions](#layout-functions)
- [Containers and Outputs](#containers-and-outputs)
- [Navigation](#navigation)
- [Theming](#theming)
- [Inputs](#inputs)
- [Complete Migration Example](#complete-migration-example)

## Legacy to Modern Mapping

| Legacy Pattern | Modern bslib Replacement | Why |
|---|---|---|
| `fluidPage()` | `page_sidebar()` or `page_navbar()` | Built-in sidebar, filling, theming |
| `navbarPage()` | `page_navbar()` | Same concept, Bootstrap 5 |
| `fluidRow(column(...))` | `layout_columns()` or `layout_column_wrap()` | Works with filling layouts |
| `tabsetPanel(tabPanel(...))` | `navset_card_underline(nav_panel(...))` | Card integration, full-screen |
| `wellPanel()` | `card()` | Full-screen, headers, filling |
| `shinythemes::shinytheme()` | `bs_theme(preset = ...)` | Bootstrap 5, Sass variables |
| `plotOutput("plot")` (bare) | `card(full_screen = TRUE, plotOutput("plot"))` | Full-screen expansion |
| `conditionalPanel()` in sidebar | `accordion()` in `sidebar()` | Better organization, native styling |
| `checkboxInput()` for toggles | `input_switch()` | Modern toggle UI |
| `actionButton()` for slow tasks | `input_task_button()` | Built-in loading state |
| `sidebarLayout(sidebarPanel(), mainPanel())` | `page_sidebar(sidebar = sidebar(), ...)` | Filling, collapsible |

## Page Functions

### Do Not Use

- **`fluidPage()`** -- No sidebar, no filling, no theming integration
- **`navbarPage()`** -- Bootstrap 3 era, use `page_navbar()` instead
- **`fixedPage()`** -- Use `page_fixed()` if scrolling layout needed
- **`sidebarLayout()` + `sidebarPanel()` + `mainPanel()`** -- Replaced entirely by `page_sidebar()`

### Use Instead

```r
# Single-page dashboard
page_sidebar(
  title = "Dashboard",
  theme = bs_theme(version = 5),
  sidebar = sidebar(...),
  card(...)
)

# Multi-page app
page_navbar(
  title = "App",
  theme = bs_theme(version = 5),
  nav_panel("Page 1", ...),
  nav_panel("Page 2", ...)
)

# Scrolling layout (rare)
page_fluid(
  theme = bs_theme(version = 5),
  card(...),
  card(...)
)
```

## Layout Functions

### Do Not Use

- **`fluidRow()`** -- Incompatible with filling layouts
- **`column()`** -- Does not participate in fill system
- **`fluidRow(column(4, ...), column(8, ...))`** -- Use `layout_columns(col_widths = c(4, 8))`

### Use Instead

Use `layout_columns()` when columns have unequal or explicit widths, and `layout_column_wrap()` when all columns should be equal or auto-sized.

**Legacy:**
```r
fluidRow(
  column(4, plotOutput("plot1")),
  column(8, plotOutput("plot2"))
)
```

**Modern:**
```r
layout_columns(
  col_widths = c(4, 8),
  card(full_screen = TRUE, card_header("Plot 1"), plotOutput("plot1")),
  card(full_screen = TRUE, card_header("Plot 2"), plotOutput("plot2"))
)
```

**Legacy:**
```r
fluidRow(
  column(4, plotOutput("a")),
  column(4, plotOutput("b")),
  column(4, plotOutput("c"))
)
```

**Modern:**
```r
layout_column_wrap(
  width = 1/3,
  card(full_screen = TRUE, card_header("A"), plotOutput("a")),
  card(full_screen = TRUE, card_header("B"), plotOutput("b")),
  card(full_screen = TRUE, card_header("C"), plotOutput("c"))
)
```

## Containers and Outputs

### Do Not Use

- **`wellPanel()`** -- Use `card()` for all content grouping
- **Bare outputs** (`plotOutput("x")` without a container) -- Always wrap in `card()`

### Use Instead

**Legacy:**
```r
wellPanel(
  h3("Results"),
  plotOutput("plot"),
  verbatimTextOutput("summary")
)
```

**Modern:**
```r
card(
  full_screen = TRUE,
  card_header("Results"),
  plotOutput("plot"),
  card_footer(verbatimTextOutput("summary"))
)
```

## Navigation

### Do Not Use

- **`tabsetPanel(tabPanel(...))`** -- Use `navset_*()` functions
- **`navlistPanel()`** -- Use `navset_pill_list()`
- **`navbarMenu()`** -- Use `nav_menu()` inside `page_navbar()`

### Use Instead

Replace `tabsetPanel()` with a `navset_card_*()` variant (e.g., `navset_card_underline()`), and replace each `tabPanel()` with `nav_panel()`. The navset card variant accepts `title` and `full_screen` arguments directly.

For top-level navigation, `navbarPage()` with `tabPanel()` and `navbarMenu()` maps directly to `page_navbar()` with `nav_panel()` and `nav_menu()`:

**Legacy:**
```r
tabsetPanel(
  tabPanel("Plot", plotOutput("plot")),
  tabPanel("Summary", verbatimTextOutput("summary")),
  tabPanel("Data", tableOutput("data"))
)
```

**Modern:**
```r
navset_card_underline(
  title = "Analysis",
  full_screen = TRUE,
  nav_panel("Plot", plotOutput("plot")),
  nav_panel("Summary", verbatimTextOutput("summary")),
  nav_panel("Data", tableOutput("data"))
)
```

**Legacy multi-page:**
```r
navbarPage(
  "My App",
  tabPanel("Home", ...),
  tabPanel("Analysis", ...),
  navbarMenu("More",
    tabPanel("Settings", ...),
    tabPanel("About", ...)
  )
)
```

**Modern:**
```r
page_navbar(
  title = "My App",
  theme = bs_theme(version = 5),
  nav_panel("Home", ...),
  nav_panel("Analysis", ...),
  nav_menu("More",
    nav_panel("Settings", ...),
    nav_panel("About", ...)
  )
)
```

## Theming

### Do Not Use

- **`shinythemes::shinytheme()`** -- Bootstrap 3 only
- **Custom CSS files for basic styling** -- Use `bs_theme()` variables instead
- **Hardcoded colors in CSS** -- Use Sass variables via `bs_add_rules()`

### Use Instead

**Legacy:**
```r
fluidPage(
  theme = shinythemes::shinytheme("cerulean"),
  ...
)
```

**Modern:**
```r
page_sidebar(
  theme = bs_theme(
    version = 5,
    preset = "cerulean",
    base_font = font_google("Roboto")
  ),
  ...
)
```

## Inputs

### Prefer Modern Equivalents

| Legacy | Modern | When to prefer modern |
|---|---|---|
| `checkboxInput()` | `input_switch()` | On/off toggles with immediate effect |
| `actionButton()` | `input_task_button()` | Operations taking >2 seconds |
| `textAreaInput()` | `input_submit_textarea()` | Expensive downstream computations |

Standard Shiny inputs (`selectInput`, `sliderInput`, `dateInput`, etc.) remain correct and do not need replacement.

## Complete Migration Example

### Before (Legacy)

```r
library(shiny)
library(shinythemes)

ui <- navbarPage(
  "Sales Dashboard",
  theme = shinytheme("flatly"),
  tabPanel("Overview",
    sidebarLayout(
      sidebarPanel(
        selectInput("region", "Region", choices = regions),
        dateRangeInput("dates", "Date range"),
        checkboxInput("show_trend", "Show trend")
      ),
      mainPanel(
        fluidRow(
          column(6, plotOutput("sales_plot")),
          column(6, plotOutput("growth_plot"))
        ),
        fluidRow(
          column(12, tableOutput("data_table"))
        )
      )
    )
  ),
  tabPanel("Details",
    tabsetPanel(
      tabPanel("By Region", plotOutput("region_plot")),
      tabPanel("By Product", plotOutput("product_plot"))
    )
  )
)
```

### After (Modern bslib)

```r
library(shiny)
library(bslib)

ui <- page_navbar(
  title = "Sales Dashboard",
  theme = bs_theme(version = 5, preset = "flatly"),
  nav_panel("Overview",
    layout_sidebar(
      sidebar = sidebar(
        selectInput("region", "Region", choices = regions),
        dateRangeInput("dates", "Date range"),
        input_switch("show_trend", "Show trend")
      ),
      layout_columns(
        col_widths = c(6, 6, 12),
        card(full_screen = TRUE, card_header("Sales"), plotOutput("sales_plot")),
        card(full_screen = TRUE, card_header("Growth"), plotOutput("growth_plot")),
        card(full_screen = TRUE, card_header("Data"), tableOutput("data_table"))
      )
    )
  ),
  nav_panel("Details",
    navset_card_underline(
      title = "Detailed Analysis",
      full_screen = TRUE,
      nav_panel("By Region", plotOutput("region_plot")),
      nav_panel("By Product", plotOutput("product_plot"))
    )
  )
)

server <- function(input, output, session) {
  thematic::thematic_shiny()
  # ... server logic unchanged
}
```
