# Tooltips and Popovers in bslib

Tooltips and popovers add contextual information and secondary controls to your UI. Tooltips are hover-triggered read-only messages; popovers are click-triggered containers that can hold interactive content.

## Table of Contents

- [Tooltips](#tooltips)
- [Popovers](#popovers)
- [Choosing Between Tooltips and Popovers](#choosing-between-tooltips-and-popovers)
- [Best Practices](#best-practices)

## Tooltips

### Basic Usage

**Wrap any UI element:**
```r
tooltip(
  actionButton("analyze", "Analyze"),
  "Run the analysis on the selected data"
)
```

**With icons:**
```r
card_header(
  "Sales Dashboard",
  tooltip(
    bsicons::bs_icon("info-circle"),
    "Shows sales data for the selected time period"
  )
)
```

**Key insight:** `tooltip()` uses the **last HTML element** in its first argument as the trigger.

**Icon-only trigger (using tagList):**
```r
tagList(
  "Revenue ",
  tooltip(
    bsicons::bs_icon("question-circle"),
    "Total revenue from all sources"
  )
)
```

### Common Patterns

**Input labels:**
```r
textInput(
  "username",
  tooltip(
    span("Username", bsicons::bs_icon("info-circle")),
    "Your username must be 3-20 characters"
  )
)
```

**Card headers:**
```r
card(
  card_header(
    "Key Metrics",
    tooltip(
      bsicons::bs_icon("info-circle"),
      "Metrics are updated every hour"
    )
  ),
  value_box(title = "Users", value = "1,234")
)
```

**Value boxes:**
```r
value_box(
  title = tooltip(
    span("MRR", bsicons::bs_icon("question-circle")),
    "Monthly Recurring Revenue"
  ),
  value = "$45,678"
)
```

### Dynamic Tooltips

**toggle_tooltip()** -- show or hide programmatically:
```r
tooltip(
  id = "help_tip",
  actionButton("analyze", "Analyze"),
  "Click to run analysis"
)

# Server
observe({
  toggle_tooltip("help_tip", show = TRUE)
}) |> bindEvent(once = TRUE)
```

**update_tooltip()** -- change content dynamically:
```r
observeEvent(input$update_status, {
  update_tooltip("status_tip", paste("Last updated:", Sys.time()))
})
```

## Popovers

### Basic Usage

**Basic popover:**
```r
popover(
  actionButton("info", "More Info"),
  "Additional details go here"
)
```

**With title:**
```r
popover(
  bsicons::bs_icon("gear"),
  title = "Settings",
  "Configuration options..."
)
```

**With HTML content:**
```r
popover(
  actionButton("help", "Help"),
  title = "Getting Started",
  tags$ul(
    tags$li("Step 1: Select data"),
    tags$li("Step 2: Choose parameters"),
    tags$li("Step 3: Run analysis")
  )
)
```

### Common Patterns

**Input toolbars in card headers** -- secondary controls that don't warrant sidebar space:
```r
card(
  full_screen = TRUE,
  card_header(
    "Sales Analysis",
    popover(
      bsicons::bs_icon("gear"),
      title = "Plot Options",
      selectInput("color_scheme", "Colors", c("default", "viridis", "plasma")),
      checkboxInput("show_trend", "Show trend line"),
      sliderInput("alpha", "Transparency", min = 0, max = 1, value = 0.8)
    )
  ),
  plotOutput("sales_plot")
)
```

**Editable card titles:**
```r
card(
  card_header(
    uiOutput("card_title"),
    popover(
      bsicons::bs_icon("pencil"),
      title = "Edit Title",
      textInput("new_title", "Title", value = "My Plot"),
      actionButton("save_title", "Save")
    )
  ),
  plotOutput("plot")
)
```

**Contextual help in sidebar:**
```r
sidebar(
  title = "Filters",
  popover(
    bsicons::bs_icon("question-circle"),
    title = "How to Use Filters",
    tags$p("Filters are applied in real-time as you change selections."),
    tags$p(tags$strong("Tip:"), " Use Shift+Click to select multiple items.")
  ),
  selectInput("category", "Category", ...),
  dateRangeInput("dates", "Date Range", ...)
)
```

### Dynamic Popovers

**toggle_popover():**
```r
popover(
  id = "welcome_pop",
  actionButton("start", "Start"),
  title = "Welcome!",
  "Click Start to begin the analysis."
)

# Server
observe({
  toggle_popover("welcome_pop", show = TRUE)
}) |> bindEvent(once = TRUE)

observeEvent(input$start, {
  toggle_popover("welcome_pop", show = FALSE)
})
```

**update_popover():**
```r
observeEvent(input$run, {
  update_popover("progress_pop", "Running analysis...")
  Sys.sleep(2)
  update_popover("progress_pop", "Complete!")
})
```

## Choosing Between Tooltips and Popovers

| Feature | Tooltip | Popover |
|---------|---------|---------|
| **Trigger** | Hover/focus | Click |
| **Persistence** | Disappears quickly | Remains until dismissed |
| **Content** | Text only (read-only) | Rich content (interactive) |
| **Use case** | Quick help | Secondary UI |
| **User effort** | Passive | Active |

**Rule of thumb:** Use tooltips for small read-only messages, and popovers when the user should interact with the content.

### Popovers vs Modals

- **Popovers:** Non-blocking -- users can interact with other UI while open
- **Modals:** Blocking -- users must address modal before continuing
- Use modals when users must complete an action (confirm deletion, submit form)

## Best Practices

### Tooltips
- Keep concise: 1-2 sentences maximum
- Use consistent icon placement (prefer info-circle next to label)
- Test on mobile (consider popovers as mobile alternative)

### Popovers
- Limit to 2-4 inputs; use modal for complex forms
- Always provide clear titles
- Don't use hyperlinks as triggers (conflicts with click behavior):

```r
# Bad
popover(tags$a("Link"), "Content")

# Good - icon next to link
tagList(
  tags$a("Link", href = "#"),
  popover(bsicons::bs_icon("info-circle"), "Context about link")
)
```

### Accessibility
- **Tooltips:** Keyboard accessible (built-in), provide alt text for icon triggers
- **Popovers:** Keyboard dismissible (Esc key), focus management automatic
