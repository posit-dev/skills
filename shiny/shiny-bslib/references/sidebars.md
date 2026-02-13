# Sidebars in bslib

Sidebars are a fundamental pattern for organizing inputs and controls in Shiny dashboards. bslib provides flexible sidebar layouts that work at multiple levels: page-level, component-level, and within cards.

## Table of Contents

- [Three Main Layout Types](#three-main-layout-types)
- [Basic Sidebar Usage](#basic-sidebar-usage)
- [Page-Level Sidebars](#page-level-sidebars)
- [Component-Level Sidebars](#component-level-sidebars)
- [Varied Sidebars Across Pages](#varied-sidebars-across-pages)
- [Conditional Sidebar Contents](#conditional-sidebar-contents)
- [Reactive Open/Close Updates](#reactive-openclose-updates)
- [Accordions in Sidebars](#accordions-in-sidebars)
- [Nested Sidebars](#nested-sidebars)
- [Styling Sidebars](#styling-sidebars)
- [Best Practices](#best-practices)

## Three Main Layout Types

### 1. Floating Layout (layout_sidebar())

Place sidebars anywhere on a page using `layout_sidebar()`. Good for visually grouping related inputs and outputs.

### 2. Filling Layout (page_sidebar())

Page-level sidebar that fills the viewport. Built on `page_fillable()` and `layout_sidebar()`.

### 3. Multi-Page/Tab Sidebar

Sidebar visible across all pages or tabs via `page_navbar()` or `navset_card_tab()`.

## Basic Sidebar Usage

### Creating a Sidebar

**The sidebar() function:**
```r
sidebar(
  title = "Controls",
  open = TRUE,
  position = "left",
  # Sidebar content
  selectInput("var", "Variable", choices = names(data)),
  sliderInput("bins", "Number of bins", min = 1, max = 50, value = 30)
)
```

**Key parameters:**
- `title`: Optional title displayed at the top
- `open`: Initial state (TRUE/FALSE) or responsive ("desktop", "closed", "always")
- `position`: "left" (default) or "right"
- `width`: Width as CSS unit (default "250px")
- `id`: For programmatic control
- `bg`: Background color
- `class`: Bootstrap utility classes
- `style`: Custom inline CSS

## Page-Level Sidebars

### page_sidebar()

The most common pattern for single-page dashboards with a sidebar.

**Example:**
```r
page_sidebar(
  title = "My Dashboard",
  sidebar = sidebar(
    title = "Filters",
    selectInput("species", "Species", choices = unique(penguins$species)),
    selectInput("island", "Island", choices = unique(penguins$island)),
    checkboxInput("show_trend", "Show trend line", value = FALSE)
  ),
  # Main content
  card(
    full_screen = TRUE,
    card_header("Bill Length vs Depth"),
    plotOutput("scatter")
  ),
  card(
    card_header("Summary Statistics"),
    verbatimTextOutput("summary")
  )
)
```

**Best practice:** Keep inputs in the sidebar, outputs in the main area.

### page_navbar() with Sidebar

Add a sidebar that appears on all pages:

**Example:**
```r
page_navbar(
  title = "Multi-Page App",
  sidebar = sidebar(
    title = "Global Filters",
    selectInput("region", "Region", choices = regions),
    dateRangeInput("dates", "Date range")
  ),
  nav_panel("Overview", overview_ui),
  nav_panel("Details", details_ui),
  nav_panel("Reports", reports_ui)
)
```

**Important caveat:** `page_navbar()`'s `sidebar` argument puts the same sidebar on **every page**. See [Varied Sidebars Across Pages](#varied-sidebars-across-pages) for alternatives.

## Component-Level Sidebars

### layout_sidebar() in Cards

Create sidebars within individual cards to keep controls close to the outputs they affect:

**Example:**
```r
card(
  full_screen = TRUE,
  card_header("Customizable Plot"),
  layout_sidebar(
    fillable = TRUE,  # Important for fill behavior
    sidebar = sidebar(
      title = "Plot Options",
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

Use `layout_sidebar()` as a root element for flexible sidebar placement:

**Example:**
```r
page_fillable(
  layout_sidebar(
    sidebar = sidebar("Sidebar content"),
    # Main content area
    layout_columns(
      card(...),
      card(...)
    )
  )
)
```

**Note:** `page_sidebar()` is just a convenience wrapper around `page_fillable()` + `layout_sidebar()`.

## Varied Sidebars Across Pages

When different pages need different sidebars, avoid using `page_navbar(sidebar = ...)`. Instead, place `layout_sidebar()` within individual pages.

**Pattern 1: Some pages with sidebars, some without**

```r
page_navbar(
  title = "App",
  fillable = c("Analysis", "Comparison"),  # Only these pages fill
  nav_panel(
    "Analysis",
    layout_sidebar(
      sidebar = sidebar(
        title = "Analysis Controls",
        selectInput("metric", "Metric", ...)
      ),
      card(plotOutput("analysis_plot"))
    )
  ),
  nav_panel(
    "Comparison",
    layout_sidebar(
      sidebar = sidebar(
        title = "Comparison Controls",
        selectInput("compare_by", "Compare by", ...)
      ),
      card(plotOutput("comparison_plot"))
    )
  ),
  nav_panel(
    "About",
    "No sidebar on this page"
  )
)
```

**Pattern 2: Multiple sidebars per page**

```r
page_navbar(
  title = "Dashboard",
  fillable = "Data Explorer",
  nav_panel(
    "Data Explorer",
    layout_columns(
      col_widths = c(6, 6),
      # Left card with its own sidebar
      card(
        full_screen = TRUE,
        card_header("Plot 1"),
        layout_sidebar(
          fillable = TRUE,
          sidebar = sidebar(position = "left", "Controls for plot 1"),
          plotOutput("plot1")
        )
      ),
      # Right card with its own sidebar
      card(
        full_screen = TRUE,
        card_header("Plot 2"),
        layout_sidebar(
          fillable = TRUE,
          sidebar = sidebar(position = "right", "Controls for plot 2"),
          plotOutput("plot2")
        )
      )
    )
  )
)
```

## Conditional Sidebar Contents

Change sidebar contents based on the active page/tab using `conditionalPanel()`:

**Example:**
```r
shinyApp(
  ui = page_navbar(
    title = "Conditional Sidebar",
    id = "nav",  # Important: ID enables tracking active page
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
      ),
      conditionalPanel(
        "input.nav === 'Summary'",
        checkboxGroupInput("vars", "Variables to summarize", ...)
      )
    ),
    nav_panel("Scatter", plotOutput("scatter")),
    nav_panel("Histogram", plotOutput("histogram")),
    nav_panel("Summary", verbatimTextOutput("summary"))
  ),
  server = function(input, output, session) {
    # Server logic
  }
)
```

**Key requirement:** The navigation container must have an `id` so inputs can be tracked.

**JavaScript condition syntax:**
- Use `===` for equality
- Access as `input.<nav_id>`
- String values match panel titles exactly

## Reactive Open/Close Updates

Programmatically toggle sidebar visibility using `toggle_sidebar()`:

**Example:**
```r
ui <- page_navbar(
  title = "Dynamic Sidebar",
  id = "nav",
  sidebar = sidebar(
    id = "main_sidebar",  # Required for programmatic control
    open = FALSE,
    "Sidebar content"
  ),
  nav_panel("Page 1", "Sidebar starts closed"),
  nav_panel("Page 2", "Sidebar opens automatically")
)

server <- function(input, output, session) {
  # Open sidebar when navigating to Page 2
  observe({
    toggle_sidebar(
      id = "main_sidebar",
      open = input$nav == "Page 2"
    )
  })
}
```

**Use cases:**
- Open sidebar on specific pages
- Close sidebar when showing certain content
- Toggle based on user actions
- Implement "guided tour" workflows

## Accordions in Sidebars

When an `accordion()` appears as an immediate child of `sidebar()`, panels render flush to the sidebar, providing clean organization for grouped inputs:

**Example:**
```r
sidebar(
  title = "Controls",
  accordion(
    accordion_panel(
      "Data Filters",
      selectInput("species", "Species", ...),
      selectInput("island", "Island", ...),
      dateRangeInput("dates", "Date range", ...)
    ),
    accordion_panel(
      "Plot Options",
      selectInput("color", "Color by", ...),
      checkboxInput("facet", "Facet by species"),
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

**Benefits:**
- Organizes many inputs without overwhelming users
- Saves vertical space
- Provides clear groupings
- Users can focus on relevant sections

See [components.md](components.md) for more on accordions.

## Nested Sidebars

Create multiple left/right sidebars by nesting `layout_sidebar()`:

**Example:**
```r
page_fillable(
  layout_sidebar(
    sidebar = sidebar(
      title = "Left Sidebar",
      "Primary controls"
    ),
    # Main content area contains another layout_sidebar
    layout_sidebar(
      sidebar = sidebar(
        title = "Right Sidebar",
        position = "right",
        open = FALSE,
        "Secondary controls"
      ),
      # Inner content
      card(plotOutput("main_plot")),
      border = FALSE
    ),
    # Remove borders and padding for seamless nesting
    border_radius = FALSE,
    fillable = TRUE,
    class = "p-0"
  )
)
```

**Best practices for nesting:**
- Set `fillable = TRUE` on outer layout
- Use `class = "p-0"` to remove padding
- Consider `border = FALSE` and `border_radius = FALSE` for cleaner appearance
- Test responsiveness carefully

## Styling Sidebars

### Background Color

Use `bg` for background color with automatic high-contrast foreground:

**Example:**
```r
sidebar(
  bg = "#f8f9fa",  # Light gray background
  "Sidebar content"
)
```

**Using theme colors:**
```r
sidebar(
  bg = "primary",
  "Themed sidebar"
)
```

### Bootstrap Utility Classes

Add utility classes via `class` parameter:

**Example:**
```r
sidebar(
  class = "border-start border-3 border-primary",
  "Sidebar with custom border"
)
```

**Common utilities:**
- Spacing: `"p-3"`, `"px-4"`, `"py-2"`
- Borders: `"border-end"`, `"border-primary"`
- Text: `"text-center"`, `"fw-bold"`

### Custom CSS

Use `style` for inline CSS:

**Example:**
```r
sidebar(
  style = css(
    background = "linear-gradient(180deg, #667eea 0%, #764ba2 100%)",
    color = "white"
  ),
  "Custom styled sidebar"
)
```

### Width Control

Adjust sidebar width with `width` parameter:

**Example:**
```r
sidebar(
  width = "300px",  # Wider sidebar
  "More space for controls"
)

sidebar(
  width = "200px",  # Narrower sidebar
  "Compact controls"
)
```

**Responsive widths:**
```r
sidebar(
  width = "20%",  # Proportional width
  "Sidebar"
)
```

## Best Practices

### Organize Inputs Logically

**Group related inputs:**
```r
sidebar(
  title = "Filters",
  h5("Date Selection"),
  dateRangeInput("dates", "Date range", ...),
  hr(),
  h5("Categories"),
  selectInput("category", "Category", ...),
  checkboxGroupInput("subcategory", "Subcategory", ...),
  hr(),
  h5("Display Options"),
  checkboxInput("show_trend", "Show trend"),
  numericInput("smooth_span", "Smoothing", ...)
)
```

**Use accordions for many inputs:**
```r
sidebar(
  accordion(
    accordion_panel("Essential", essential_inputs),
    accordion_panel("Advanced", advanced_inputs),
    accordion_panel("Appearance", appearance_inputs)
  )
)
```

### Choose Appropriate Sidebar Position

**Left sidebar (default):**
- Most common pattern
- Natural reading order (LTR languages)
- Good for primary controls

**Right sidebar:**
- Good for secondary/optional controls
- Useful when main content is left-aligned
- Keeps focus on content first

**Example with right sidebar:**
```r
layout_sidebar(
  sidebar = sidebar(
    position = "right",
    title = "Options",
    "Secondary controls"
  ),
  # Main content gets primary focus
  card(plotOutput("main_plot"))
)
```

### Handle Sidebar State Thoughtfully

**Keep open on desktop by default:**
```r
sidebar(
  open = "desktop",  # Open on desktop, closed on mobile
  ...
)
```

**Start closed for secondary sidebars:**
```r
sidebar(
  open = FALSE,
  title = "Advanced Options",
  ...
)
```

**Always open (no collapse button):**
```r
sidebar(
  open = "always",
  ...
)
```

### Optimize for Mobile

**Key considerations:**
- Sidebars auto-collapse on small screens by default
- Test sidebar content at mobile widths
- Ensure inputs work well when stacked
- Consider reducing the number of inputs visible at once

**Mobile-friendly pattern:**
```r
sidebar(
  open = "desktop",  # Closed on mobile, open on desktop
  # Prioritize most important inputs first
  selectInput("primary_filter", "Main Filter", ...),
  hr(),
  # Secondary inputs in accordion
  accordion(
    accordion_panel("More Filters", ...)
  )
)
```

### Use Consistent Sidebar Widths

Within an app, maintain consistent sidebar widths for visual coherence:

**Define width once:**
```r
SIDEBAR_WIDTH <- "275px"

# Use throughout app
sidebar(width = SIDEBAR_WIDTH, ...)
```

### Provide Clear Titles

Use descriptive sidebar titles:

**Good:**
```r
sidebar(title = "Data Filters", ...)
sidebar(title = "Plot Options", ...)
sidebar(title = "Export Settings", ...)
```

**Avoid:**
```r
sidebar(title = "Settings", ...)  # Too vague
sidebar(title = "Options", ...)   # Too generic
```

### Avoid Sidebar Overload

**If sidebar becomes crowded:**
1. Use accordions to group inputs
2. Move some controls to a secondary sidebar
3. Consider moving less important controls into a popover in the card header
4. Split into multiple pages/tabs with page-specific sidebars

**Example - popover for advanced options:**
```r
card(
  card_header(
    "Plot",
    popover(
      bsicons::bs_icon("gear"),
      title = "Advanced Options",
      sliderInput("advanced_param", "Parameter", ...)
    )
  ),
  plotOutput("plot")
)
```

### Test Responsiveness

Always test:
- Desktop (sidebar open)
- Tablet (sidebar collapse behavior)
- Mobile (sidebar closed by default)
- Different sidebar widths
- Content reflow when sidebar toggles

### Consider Performance

**For expensive reactive computations triggered by sidebar inputs:**
```r
# Use debounce for continuous inputs
filtered_data <- reactive({
  # Debounce prevents excessive updates while slider moves
  data |> filter(value >= input$slider)
}) |> debounce(500)

# Or use action button to apply filters
sidebar(
  selectInput("var", "Variable", ...),
  sliderInput("threshold", "Threshold", ...),
  actionButton("apply", "Apply Filters", class = "btn-primary w-100")
)
```

### Accessibility

- Ensure sidebar toggle button is keyboard accessible (built-in)
- Use clear labels for all inputs
- Maintain sufficient color contrast
- Test sidebar with screen readers for public apps
- Consider ARIA labels for complex sidebar interactions
