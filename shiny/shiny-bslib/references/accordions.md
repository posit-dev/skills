# Accordions in bslib

Accordions provide collapsible sections for organizing content vertically. Especially useful for grouping inputs in sidebars and providing progressive disclosure.

## Table of Contents

- [Basic Usage](#basic-usage)
- [In Sidebars](#accordions-in-sidebars)
- [Dynamic Control](#dynamic-accordion-control)
- [Best Practices](#best-practices)

## Basic Usage

Use `accordion()` and `accordion_panel()` to create collapsible sections. Pass `icon` to `accordion_panel()` to add a leading icon. Use `open` to specify which panels start open (by title), and `multiple = TRUE` to allow more than one panel open at a time (default is `FALSE`).

```r
accordion(
  id = "acc",
  open = c("Visualizations"),
  multiple = TRUE,
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

- `accordion_panel_open("acc", "Panel Title")` — opens a panel
- `accordion_panel_close("acc", "Panel Title")` — closes a panel
- `accordion_panel_set("acc", c("Panel 1"))` — sets exactly which panels are open
- `accordion_panel_remove("acc", "Panel Title")` — removes a panel
- `accordion_panel_update("acc", "Panel Title", "New content")` — replaces panel body content

**Insert a new panel** at a specific position:

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

## Best Practices

**Group logically:**
- Related inputs in same panel
- Order by importance or workflow
- 3-6 panels is ideal; more than 8 becomes unwieldy

**Set appropriate initial state:** Open the most important panel by default, and leave secondary or advanced panels closed:

```r
accordion(
  open = "Essential Filters",
  accordion_panel("Essential Filters", ...),
  accordion_panel("Advanced Filters", ...),
  accordion_panel("Export Options", ...)
)
```

**Accessibility:** Keyboard navigation (arrow keys, Enter) and ARIA attributes are automatic.
