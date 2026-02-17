# Navigation in bslib

This reference covers navigation patterns in bslib, including tabsets, multi-page apps, and navigation containers. Navigation helps organize content into logical sections and pages.

## Table of Contents

- [Core Concept](#core-concept)
- [Navigation Containers](#navigation-containers)
  - [navset_underline()](#navset_underline)
  - [navset_tab()](#navset_tab)
  - [navset_pill()](#navset_pill)
  - [navset_pill_list()](#navset_pill_list)
  - [navset_bar()](#navset_bar)
  - [navset_hidden()](#navset_hidden)
- [Card Navigation](#card-navigation)
- [Navigation Items](#navigation-items)
- [Multi-Page Apps](#multi-page-apps)
- [Accessing Active Tab](#accessing-active-tab)
- [Dynamic Navigation](#dynamic-navigation)
- [Best Practices](#best-practices)

## Core Concept

Tabsets and navigation are created by combining `nav_panel()`s in a navigation container. Each `nav_panel()` has a label (shown in the navigation) and content (shown when selected).

**Basic pattern:**
```r
navset_*(
  nav_panel("Tab 1", "Content 1"),
  nav_panel("Tab 2", "Content 2"),
  nav_panel("Tab 3", "Content 3")
)
```

## Navigation Containers

### navset_underline()

Modern underline-style navigation (recommended for most use cases).

**Example:**
```r
navset_underline(
  nav_panel("Overview", plotOutput("overview")),
  nav_panel("Details", tableOutput("details")),
  nav_panel("Settings", uiOutput("settings"))
)
```

**Use when:** You want a clean, modern look with subtle visual emphasis on the active tab.

### navset_tab()

Traditional tab-style navigation with filled backgrounds.

**Example:**
```r
navset_tab(
  nav_panel("Plot", plotOutput("plot")),
  nav_panel("Summary", verbatimTextOutput("summary")),
  nav_panel("Data", tableOutput("data"))
)
```

**Use when:** You want classic Bootstrap tab styling or need stronger visual separation between tabs.

### navset_pill()

Horizontal pill-style navigation with rounded backgrounds.

**Example:**
```r
navset_pill(
  nav_panel("Analysis", plotOutput("analysis")),
  nav_panel("Report", uiOutput("report")),
  nav_panel("Export", downloadButton("export"))
)
```

**Use when:** You want a more button-like appearance for navigation items.

### navset_pill_list()

Vertical pill list navigation, sidebar-style.

**Example:**
```r
navset_pill_list(
  nav_panel("Section 1", "Content 1"),
  nav_panel("Section 2", "Content 2"),
  nav_panel("Section 3", "Content 3"),
  nav_panel("Section 4", "Content 4")
)
```

**Use when:** You have many navigation items and want them displayed vertically, or when the vertical layout fits your design better.

### navset_bar()

Navigation bar style, similar to page_navbar() but without being a full page layout.

**Example:**
```r
navset_bar(
  title = "App Section",
  nav_panel("Home", "Home content"),
  nav_panel("About", "About content"),
  nav_menu(
    "More",
    nav_panel("Option 1", "Content 1"),
    nav_panel("Option 2", "Content 2")
  )
)
```

**Use when:** You want navbar-style navigation within a section of your app rather than at the page level.

### navset_hidden()

Navigation container without visible navigation controls. Useful for programmatic tab switching.

**Example:**
```r
# UI
navset_hidden(
  id = "wizard",
  nav_panel("step1", "Step 1 content", actionButton("next1", "Next")),
  nav_panel("step2", "Step 2 content", actionButton("next2", "Next")),
  nav_panel("step3", "Step 3 content", actionButton("submit", "Submit"))
)

# Server
observeEvent(input$next1, {
  nav_select("wizard", "step2")
})
observeEvent(input$next2, {
  nav_select("wizard", "step3")
})
```

**Use when:** You need programmatic control over navigation (wizards, workflows, complex state machines).

## Card Navigation

Functions with `card` in their name wrap the navigation in a card container:

### navset_card_underline()

**Example:**
```r
navset_card_underline(
  title = "Analysis Results",
  full_screen = TRUE,
  nav_panel("Plot", plotOutput("plot")),
  nav_panel("Summary", verbatimTextOutput("summary")),
  nav_panel("Table", tableOutput("table"))
)
```

**Key features:**
- The `title` parameter adds a card header above the navigation
- Supports `full_screen = TRUE` for expandable content
- Each `nav_panel()` behaves like a card body — do **not** wrap panel content in `card()`

**Don't nest cards inside navset_card_* panels.** The navset already provides the card container. Wrapping content in `card()` inside `nav_panel()` creates a card-within-a-card:

```r
# Wrong: double-nested card
navset_card_underline(
  nav_panel("Plot", card(plotOutput("plot")))  # card() is redundant
)

# Right: output directly in nav_panel
navset_card_underline(
  nav_panel("Plot", plotOutput("plot"))
)
```

The same applies to `navset_card_tab()` and `navset_card_pill()`.

### navset_card_tab()

Tab-style navigation in a card.

```r
navset_card_tab(
  title = "Data Explorer",
  nav_panel("Visualize", plotOutput("plot")),
  nav_panel("Summarize", verbatimTextOutput("summary"))
)
```

### navset_card_pill()

Pill-style navigation in a card.

```r
navset_card_pill(
  title = "Reports",
  nav_panel("Monthly", uiOutput("monthly")),
  nav_panel("Quarterly", uiOutput("quarterly")),
  nav_panel("Annual", uiOutput("annual"))
)
```

**Best practice:** Card navigation containers are excellent for organizing related outputs within a dashboard. Always enable `full_screen = TRUE` when panels contain visualizations.

## Navigation Items

Beyond `nav_panel()`, several helper functions control navigation appearance:

### nav_panel()

The primary content container.

**Parameters:**
```r
nav_panel(
  title = "Panel Label",     # Shown in navigation
  value = "panel_id",         # Optional ID for programmatic control
  icon = bsicons::bs_icon("graph-up"),  # Optional icon
  # Content: outputs, text, layout functions — not card() when inside navset_card_*
  plotOutput("plot")
)
```

### nav_spacer()

Adds flexible space, pushing subsequent items to the right (horizontal) or bottom (vertical).

**Example:**
```r
page_navbar(
  title = "My App",
  nav_panel("Home", "..."),
  nav_panel("About", "..."),
  nav_spacer(),  # Everything after goes to the right
  nav_item(tags$a("Help", href = "/help")),
  nav_item(tags$a("Login", href = "/login"))
)
```

### nav_menu()

Creates a dropdown menu of nav panels.

**Example:**
```r
navset_tab(
  nav_panel("Overview", "..."),
  nav_menu(
    "Analysis",
    nav_panel("Trends", plotOutput("trends")),
    nav_panel("Comparisons", plotOutput("comparisons")),
    nav_panel("Forecasts", plotOutput("forecasts"))
  ),
  nav_menu(
    "Admin",
    nav_panel("Users", tableOutput("users")),
    nav_panel("Settings", uiOutput("settings"))
  )
)
```

### nav_item()

Adds arbitrary HTML to navigation without creating a panel. Useful for links, buttons, or custom elements.

**Example:**
```r
page_navbar(
  title = "Dashboard",
  nav_panel("Home", "..."),
  nav_item(tags$a("Docs", href = "https://docs.example.com", target = "_blank")),
  nav_item(actionLink("refresh", "Refresh Data"))
)
```

### nav_panel_hidden()

A panel that exists but isn't shown in navigation. Useful for programmatically accessible panels.

**Example:**
```r
navset_tab(
  id = "tabs",
  nav_panel("Public 1", "..."),
  nav_panel("Public 2", "..."),
  nav_panel_hidden("admin", "Admin-only content")
)

# Server: show admin panel based on user role
observe({
  if (user_is_admin()) {
    nav_show("tabs", "admin")
  }
})
```

## Multi-Page Apps

Use `page_navbar()` to create full multi-page applications. This is covered in detail in [page-layouts.md](page-layouts.md), but here's the navigation pattern:

**Basic multi-page app:**
```r
page_navbar(
  title = "My Application",
  nav_panel("Home", homepage_ui),
  nav_panel("Analysis", analysis_ui),
  nav_panel("Reports", reports_ui),
  nav_menu(
    "More",
    nav_panel("Settings", settings_ui),
    nav_panel("About", about_ui)
  )
)
```

**Relationship to tabsets:** `page_navbar()` uses the same `nav_panel()` system as tabsets. The main difference is that `page_navbar()` creates a full-page layout, while `navset_*()` creates a component-level navigation container.

## Accessing Active Tab

Provide an `id` argument to track which panel is selected:

**Example:**
```r
# UI
navset_card_underline(
  id = "selected_tab",
  nav_panel("Plot", plotOutput("plot")),
  nav_panel("Summary", verbatimTextOutput("summary")),
  nav_panel("Data", tableOutput("data"))
)

# Server
observe({
  # Access current tab
  current_tab <- input$selected_tab

  # Do something based on active tab
  if (current_tab == "Plot") {
    # Trigger plot-specific actions
  }
})

# Display current tab
output$current_display <- renderText({
  paste("Currently viewing:", input$selected_tab)
})
```

**Use cases:**
- Conditional logic based on active panel
- Analytics tracking
- Loading data only when needed
- Updating other UI elements based on navigation state

## Dynamic Navigation

Programmatically control navigation with these functions:

### nav_select()

Switch to a specific panel.

```r
# UI
actionButton("show_plot", "View Plot"),
navset_tab(
  id = "tabs",
  nav_panel("Home", "Home content"),
  nav_panel("Plot", plotOutput("plot"))
)

# Server
observeEvent(input$show_plot, {
  nav_select("tabs", "Plot")
})
```

### nav_show() / nav_hide()

Show or hide specific panels dynamically.

```r
# Server
observeEvent(input$enable_advanced, {
  nav_show("tabs", "advanced_panel")
})

observeEvent(input$disable_advanced, {
  nav_hide("tabs", "advanced_panel")
})
```

### nav_insert()

Add a new panel dynamically.

```r
# Server
observeEvent(input$add_panel, {
  nav_insert(
    "tabs",
    nav_panel("New Panel", "Dynamic content"),
    position = "after",
    target = "Home"
  )
})
```

### nav_remove()

Remove a panel dynamically.

```r
# Server
observeEvent(input$remove_panel, {
  nav_remove("tabs", "panel_to_remove")
})
```

## Best Practices

### Choose Appropriate Navigation Style

**Use `navset_underline()` for:**
- Modern, clean interfaces
- 2-5 top-level navigation items
- When you want subtle visual emphasis

**Use `navset_tab()` for:**
- Traditional interfaces
- When users expect classic tab styling
- Stronger visual separation needed

**Use `navset_pill_list()` for:**
- Many navigation items (5+)
- When vertical space is available
- Sidebar-style navigation within a section

**Use card variants for:**
- Organizing related outputs in a dashboard
- When the navigation is part of a specific content section
- Always with `full_screen = TRUE` for viz-heavy content

### Organize Content Logically

**Group related panels:**
```r
navset_card_underline(
  title = "User Analysis",
  nav_panel("Demographics", plotOutput("demographics")),
  nav_panel("Behavior", plotOutput("behavior")),
  nav_panel("Segments", plotOutput("segments"))
)
```

**Use menus for secondary content:**
```r
page_navbar(
  title = "Dashboard",
  nav_panel("Overview", overview_ui),    # Primary
  nav_panel("Analysis", analysis_ui),    # Primary
  nav_menu(                              # Secondary
    "More",
    nav_panel("Settings", settings_ui),
    nav_panel("Help", help_ui),
    nav_panel("About", about_ui)
  )
)
```

### Prevent Redundant Computation

When multiple tabs share data, use reactive expressions:

**Example:**
```r
# Server
# Single reactive for shared data
filtered_data <- reactive({
  data |>
    filter(species == input$species) |>
    filter(island == input$island)
})

# Each tab uses the shared reactive
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

This prevents recalculating the same filtered data for each tab.

### Use IDs Consistently

When providing `id` to navigation containers:
- Use descriptive, semantic IDs (`id = "main_tabs"`, not `id = "t1"`)
- Document which IDs are used for programmatic control
- Keep track of panel `value` parameters when using dynamic navigation

### Lazy Loading for Performance

For tabs with expensive computations, use `bindEvent()` or `req()` to load content only when the tab is viewed:

```r
# Server
output$expensive_plot <- renderPlot({
  req(input$tabs == "Analysis")  # Only render when Analysis tab is active

  # Expensive computation
  run_complex_analysis(data)
}) |> bindEvent(input$tabs)
```

### Test Navigation Flow

Always test:
- Switching between all tabs
- Navigation on mobile (especially dropdowns)
- Programmatic navigation if implemented
- Deep linking if using bookmarking

### Consider Bookmarking

For apps with important navigation state, enable bookmark support:

```r
shinyApp(
  ui = page_navbar(
    id = "nav",
    nav_panel("Home", "..."),
    nav_panel("Analysis", "...")
  ),
  server = function(input, output, session) {
    # Navigation state is automatically bookmarkable
  },
  enableBookmarking = "url"
)
```

This allows users to share links to specific tabs.

### Accessibility

- Use clear, descriptive panel titles
- Avoid relying solely on icons for navigation
- Ensure keyboard navigation works (test with Tab key)
- Test with screen readers for public-facing apps
- Consider ARIA labels for complex navigation patterns
