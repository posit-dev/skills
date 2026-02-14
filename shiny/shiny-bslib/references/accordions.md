# Accordions in bslib

Accordions provide collapsible sections for organizing content vertically. Especially useful for grouping inputs in sidebars and providing progressive disclosure.

## Table of Contents

- [Basic Usage](#basic-usage)
- [In Sidebars](#accordions-in-sidebars)
- [Dynamic Control](#dynamic-accordion-control)
- [Best Practices](#best-practices)

## Basic Usage

**Create an accordion with `accordion()` and `accordion_panel()`:**

```r
accordion(
  accordion_panel(
    "Section 1",
    "Content for section 1"
  ),
  accordion_panel(
    "Section 2",
    "Content for section 2"
  ),
  accordion_panel(
    "Section 3",
    "Content for section 3"
  )
)
```

**With icons:**
```r
accordion(
  accordion_panel(
    icon = bsicons::bs_icon("graph-up"),
    title = "Visualizations",
    plotOutput("plot")
  ),
  accordion_panel(
    icon = bsicons::bs_icon("table"),
    title = "Data Table",
    tableOutput("table")
  )
)
```

**Control initial state:**
```r
accordion(
  id = "acc",
  open = c("Panel 1", "Panel 2"),  # Initially open panels
  accordion_panel("Panel 1", "..."),
  accordion_panel("Panel 2", "..."),
  accordion_panel("Panel 3", "...")
)
```

**Multiple open panels:**
```r
accordion(
  multiple = TRUE,  # Allow multiple panels open simultaneously
  accordion_panel("Panel 1", "..."),
  accordion_panel("Panel 2", "..."),
  accordion_panel("Panel 3", "...")
)
```

## Accordions in Sidebars

When an `accordion()` appears as an immediate child of `sidebar()`, panels render flush to the sidebar for clean organization:

```r
page_sidebar(
  sidebar = sidebar(
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
        "Advanced Settings",
        checkboxInput("show_outliers", "Show outliers"),
        numericInput("smooth_span", "Smoothing span", ...),
        selectInput("theme", "ggplot2 theme", ...)
      )
    )
  ),
  card(plotOutput("plot"))
)
```

**Benefits:**
- Groups related inputs
- Reduces sidebar scrolling
- Helps users focus on relevant controls
- Provides clear organizational structure

**Gotcha:** Accordion must be an immediate child of `sidebar()` for flush rendering. Wrapping it in another element adds extra padding.

## Dynamic Accordion Control

Programmatically control accordion state (requires `id` on the accordion):

**Open/close specific panels:**
```r
observeEvent(input$show_advanced, {
  accordion_panel_open("acc", "Advanced Settings")
})

observeEvent(input$hide_advanced, {
  accordion_panel_close("acc", "Advanced Settings")
})
```

**Set which panels are open:**
```r
observeEvent(input$reset, {
  accordion_panel_set("acc", c("Panel 1"))  # Only Panel 1 open
})
```

**Insert new panels dynamically:**
```r
observeEvent(input$add_panel, {
  accordion_panel_insert(
    "acc",
    accordion_panel("New Panel", "Dynamic content"),
    target = "Panel 2",
    position = "after"
  )
})
```

**Remove panels:**
```r
observeEvent(input$remove, {
  accordion_panel_remove("acc", "Panel to Remove")
})
```

**Update panel content:**
```r
observeEvent(input$update, {
  accordion_panel_update(
    "acc",
    "Panel 1",
    "Updated content"
  )
})
```

## Best Practices

**Provide clear panel titles:**
```r
accordion(
  accordion_panel("Data Filters", ...),     # Clear
  accordion_panel("Plot Options", ...),     # Clear
  # Not: accordion_panel("Options", ...)    # Too vague
)
```

**Group logically:**
- Related inputs in same panel
- Order by importance or workflow
- 3-6 panels is ideal; more than 8 becomes unwieldy

**Set appropriate initial state:**
```r
accordion(
  open = "Essential Filters",  # Most important panel open
  accordion_panel("Essential Filters", ...),
  accordion_panel("Advanced Filters", ...),
  accordion_panel("Export Options", ...)
)
```

**Accessibility:** Keyboard navigation (arrow keys, Enter) and ARIA attributes are automatic.
