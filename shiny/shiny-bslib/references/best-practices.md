# Best Practices for Modern Shiny Apps with bslib

This reference compiles best practices, common patterns, and tips for building professional Shiny dashboards and applications using bslib.

## Table of Contents

- [Application Structure](#application-structure)
- [Layout Patterns](#layout-patterns)
- [Performance Optimization](#performance-optimization)
- [Mobile and Responsive Design](#mobile-and-responsive-design)
- [User Experience](#user-experience)
- [Code Organization](#code-organization)
- [Production Deployment](#production-deployment)
- [Common Gotchas](#common-gotchas)

## Application Structure

### Start with the Right Page Function

**Single-page dashboard:** `page_sidebar()`
```r
page_sidebar(
  title = "Sales Dashboard",
  sidebar = sidebar(...),
  # Main content
)
```

**Multi-page dashboard:** `page_navbar()`
```r
page_navbar(
  title = "Analytics Platform",
  nav_panel("Overview", ...),
  nav_panel("Details", ...),
  nav_panel("Reports", ...)
)
```

**Filling layout:** `page_fillable()`
```r
page_fillable(
  layout_columns(...)
)
```

**Scrolling layout:** `page_fluid()` or `page_fixed()`
```r
page_fluid(
  card(...),
  card(...),
  card(...)
)
```

### Always Use card() for Outputs

Wrap outputs in cards for visual organization and features:

**Good:**
```r
card(
  full_screen = TRUE,
  card_header("Sales Trend"),
  plotOutput("sales_plot")
)
```

**Avoid:**
```r
plotOutput("sales_plot")  # No container
```

### Enable Full-Screen for Visualizations

Always add `full_screen = TRUE` to cards containing plots, maps, or tables:

**Example:**
```r
card(
  full_screen = TRUE,  # Important!
  card_header("Interactive Map"),
  leafletOutput("map")
)
```

Users greatly value the ability to expand visualizations.

### Use Layout Functions Over Legacy Grid

**Prefer:**
```r
layout_columns(
  col_widths = c(4, 8),
  card(...),
  card(...)
)
```

**Avoid:**
```r
fluidRow(
  column(4, card(...)),
  column(8, card(...))
)
```

Why: `layout_columns()` works properly with filling layouts; `fluidRow()`/`column()` don't.

## Layout Patterns

### Dashboard Header with KPIs

Common pattern: value boxes at top, detailed content below:

```r
page_sidebar(
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

### Sidebar + Main with Multiple Outputs

Use `layout_column_wrap()` for uniform grid of outputs:

```r
page_sidebar(
  sidebar = sidebar(
    selectInput("metric", "Metric", ...),
    dateRangeInput("dates", "Date range", ...)
  ),
  layout_column_wrap(
    width = 1/2,
    card(full_screen = TRUE, card_header("Overview"), plotOutput("overview")),
    card(full_screen = TRUE, card_header("By Region"), plotOutput("by_region")),
    card(full_screen = TRUE, card_header("By Product"), plotOutput("by_product")),
    card(full_screen = TRUE, card_header("Trend"), plotOutput("trend"))
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

Don't use `page_navbar(sidebar = ...)` for page-specific controls:

**Good:**
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

**Avoid:**
```r
page_navbar(
  sidebar = sidebar(...),  # Shows on ALL pages
  nav_panel("Analysis", ...),
  nav_panel("Comparison", ...)
)
```

## Performance Optimization

### Use Reactive Expressions for Shared Data

When multiple outputs use the same data transformation:

**Good:**
```r
# Server
filtered_data <- reactive({
  data |>
    filter(species == input$species) |>
    filter(island == input$island)
})

output$plot <- renderPlot({
  ggplot(filtered_data(), aes(x, y)) + geom_point()
})

output$summary <- renderPrint({
  summary(filtered_data())
})

output$table <- renderTable({
  filtered_data()
})
```

**Avoid:**
```r
# Server - repeated filtering
output$plot <- renderPlot({
  data |>
    filter(species == input$species) |>
    filter(island == input$island) |>
    ggplot(aes(x, y)) + geom_point()
})

output$summary <- renderPrint({
  summary(
    data |>
      filter(species == input$species) |>
      filter(island == input$island)
  )
})
```

### Debounce Fast-Changing Inputs

For continuous inputs that trigger expensive computations:

```r
# Debounce slider updates
filtered_data <- reactive({
  data |> filter(value >= input$threshold)
}) |> debounce(500)  # Wait 500ms after last change
```

Or use action button for explicit triggering:

```r
sidebar(
  sliderInput("threshold", "Threshold", ...),
  selectInput("category", "Category", ...),
  actionButton("apply", "Apply Filters", class = "btn-primary w-100")
)

# Only update on button click
filtered_data <- eventReactive(input$apply, {
  data |> filter(
    value >= input$threshold,
    category == input$category
  )
})
```

### Lazy Load Tab Content

For expensive computations in tabs, only render when tab is active:

```r
output$expensive_plot <- renderPlot({
  req(input$tabs == "Analysis")  # Only render when tab is active

  # Expensive computation
  run_analysis(data())
})
```

### Use bindEvent() for Controlled Reactivity

Control when outputs update:

```r
output$report <- renderUI({
  # Only regenerate when button clicked, not on every input change
  generate_report(input$param1, input$param2, input$param3)
}) |> bindEvent(input$generate)
```

### Profile with profvis

Identify bottlenecks:

```r
library(profvis)

profvis({
  runApp("app.R")
  # Interact with app
})
```

## Mobile and Responsive Design

### Test at Multiple Breakpoints

Always test:
- Desktop: 1920px, 1440px, 1280px
- Tablet: 1024px, 768px
- Mobile: 414px, 375px, 360px

Use browser dev tools to simulate different devices.

### Use Responsive Column Widths

```r
layout_column_wrap(
  width = "250px",  # Auto-adjusts column count
  card(...),
  card(...),
  card(...)
)
```

Or with breakpoints:

```r
layout_columns(
  col_widths = breakpoints(
    sm = 12,     # Stack on mobile
    md = c(6, 6),  # Two columns on tablet
    lg = c(4, 4, 4)  # Three columns on desktop
  ),
  card(...),
  card(...),
  card(...)
)
```

### Mobile-Friendly Sidebars

**Default behavior (recommended):**
```r
sidebar(
  open = "desktop",  # Open on desktop, closed on mobile
  ...
)
```

**Always collapsible:**
```r
sidebar(
  open = TRUE,  # Open initially, but collapsible on all devices
  ...
)
```

### Set Minimum Heights

Prevent cards from becoming too small on mobile:

```r
card(
  min_height = 300,
  plotOutput("plot")
)
```

### Consider fillable_mobile

By default, filling is disabled on mobile. Enable if appropriate:

```r
page_sidebar(
  fillable_mobile = TRUE,
  ...
)
```

Test thoroughly before enabling - filling on mobile can be problematic.

## User Experience

### Provide Clear Visual Hierarchy

**Use value boxes for key metrics:**
```r
layout_column_wrap(
  width = 1/4,
  fill = FALSE,
  value_box(...),
  value_box(...),
  value_box(...),
  value_box(...)
)
```

**Use card headers:**
```r
card(
  card_header("Section Title"),
  ...
)
```

**Use accordions to organize inputs:**
```r
sidebar(
  accordion(
    accordion_panel("Essential", ...),
    accordion_panel("Advanced", ...)
  )
)
```

### Add Contextual Help

**Tooltips for quick help:**
```r
card_header(
  "Revenue",
  tooltip(
    bsicons::bs_icon("info-circle"),
    "Total revenue from all sources"
  )
)
```

**Popovers for detailed help:**
```r
card_header(
  "Settings",
  popover(
    bsicons::bs_icon("gear"),
    title = "Advanced Options",
    selectInput("option1", "Option 1", ...),
    checkboxInput("option2", "Option 2")
  )
)
```

### Show Loading States

**For task buttons:**
```r
input_task_button("process", "Process Data")
# Automatically shows loading state
```

**For long-running outputs:**
```r
output$plot <- renderPlot({
  # Show spinner while loading
  withProgress(message = "Generating plot...", {
    expensive_plot()
  })
})
```

### Provide Feedback

**Toast notifications for actions:**
```r
observeEvent(input$save, {
  save_data(data())

  show_toast(
    toast(
      toast_header("Success", class = "bg-success text-white"),
      "Data saved successfully"
    )
  )
})
```

**Update UI to reflect state:**
```r
observeEvent(input$export, {
  export_data()

  update_task_button(
    "export",
    label = "Exported!",
    icon = bsicons::bs_icon("check")
  )
})
```

### Handle Empty States

Show helpful messages when no data is available:

```r
output$plot <- renderPlot({
  req(nrow(filtered_data()) > 0, cancelOutput = TRUE)

  ggplot(filtered_data(), aes(x, y)) + geom_point()
})

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

## Code Organization

### Separate UI and Server

**app.R:**
```r
source("ui.R")
source("server.R")

shinyApp(ui, server)
```

**ui.R:**
```r
ui <- page_navbar(
  theme = app_theme(),
  ...
)
```

**server.R:**
```r
server <- function(input, output, session) {
  # Server logic
}
```

### Modularize Complex Apps

Use Shiny modules for reusable components:

**plot_module.R:**
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

plot_module_server <- function(id, data) {
  moduleServer(id, function(input, output, session) {
    output$plot <- renderPlot({
      ggplot(data(), aes_string("x", "y", color = input$color)) +
        geom_point()
    })
  })
}
```

### Extract Theme Configuration

**theme.R:**
```r
app_theme <- function() {
  bs_theme(
    version = 5,
    bootswatch = "flatly",
    primary = "#2c3e50",
    base_font = font_google("Lato")
  ) |>
    bs_add_rules(sass::sass_file("www/custom.scss"))
}
```

### Use Helper Functions

**utils.R:**
```r
# Data processing helpers
clean_data <- function(data) {
  data |>
    filter(!is.na(value)) |>
    mutate(date = as.Date(date))
}

# UI helpers
metric_card <- function(title, value, theme = "primary") {
  value_box(
    title = title,
    value = value,
    theme = theme,
    showcase = bsicons::bs_icon("graph-up")
  )
}
```

## Production Deployment

### Pin Bootstrap Version

```r
page_navbar(
  theme = bs_theme(version = 5),
  ...
)
```

### Remove Development Tools

Remove before deployment:
- `bs_themer()`
- `browser()` debugging calls
- Verbose print statements
- Test data

### Set Appropriate Options

**app.R:**
```r
options(
  shiny.maxRequestSize = 30*1024^2,  # 30MB upload limit
  shiny.sanitize.errors = TRUE        # Hide error details in production
)
```

### Add Error Handling

```r
output$plot <- renderPlot({
  tryCatch({
    validate(
      need(nrow(data()) > 0, "No data available"),
      need(input$variable %in% names(data()), "Invalid variable")
    )

    ggplot(data(), aes_string(input$variable)) + geom_histogram()
  }, error = function(e) {
    # Log error
    message("Plot error: ", e$message)

    # Show user-friendly message
    NULL
  })
})
```

### Optimize for Performance

- Pre-calculate expensive computations
- Cache static data
- Use efficient data structures (data.table, arrow)
- Minimize reactive dependencies
- Profile and identify bottlenecks

### Test Across Browsers

Test on:
- Chrome/Edge (Chromium)
- Firefox
- Safari (especially for Apple users)

### Monitor and Log

```r
# Log user actions
observeEvent(input$export, {
  message(sprintf("[%s] User exported data", Sys.time()))
})

# Track errors
options(shiny.error = function() {
  message(sprintf("[%s] Error occurred", Sys.time()))
})
```

## Common Gotchas

### Fill Chain Breaks

**Problem:** Output doesn't fill despite being in filling layout.

**Solution:** Ensure no non-fill carriers in the chain.

```r
# Broken
card_body(
  div(plotOutput("plot"))  # div breaks chain
)

# Fixed
card_body(
  as_fill_carrier(
    div(plotOutput("plot"))
  )
)
```

### Value Boxes Expanding Too Much

**Problem:** Value boxes take up too much vertical space.

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

**Solution:** Use `layout_sidebar()` within individual pages.

```r
page_navbar(
  nav_panel(
    "Page 1",
    layout_sidebar(
      sidebar = sidebar("Page 1 controls"),
      ...
    )
  )
)
```

### Accordion in Sidebar Not Flush

**Problem:** Accordion has extra padding in sidebar.

**Cause:** Accordion might not be immediate child of `sidebar()`.

**Solution:** Place accordion directly in sidebar:

```r
sidebar(
  accordion(  # Immediate child
    accordion_panel(...)
  )
)
```

### fluidRow/column Doesn't Fill

**Problem:** Used `fluidRow()`/`column()` in filling layout.

**Solution:** Use `layout_columns()` instead.

```r
# Avoid
page_fillable(
  fluidRow(...)
)

# Prefer
page_fillable(
  layout_columns(...)
)
```

### Plotly Doesn't Resize

**Problem:** plotly plot doesn't resize in card.

**Solution:** Ensure card has height and plotly is fill item:

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

**Solution:** Use `thematic` package:

```r
# Server
thematic::thematic_shiny()
```

### Custom CSS Overriding Theme

**Problem:** Custom CSS not respecting theme changes.

**Solution:** Use `bs_add_rules()` with Sass variables:

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
