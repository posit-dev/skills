# Tooltips and Popovers in bslib

Tooltips and popovers add contextual information and secondary controls to your UI. Tooltips are hover-triggered read-only messages; popovers are click-triggered containers that can hold interactive content.

## Table of Contents

- [Tooltips](#tooltips)
- [Popovers](#popovers)
- [Choosing Between Tooltips and Popovers](#choosing-between-tooltips-and-popovers)
- [Best Practices](#best-practices)

## Tooltips

### Basic Usage

Wrap any UI element in `tooltip()` to add a hover message:

```r
tooltip(
  actionButton("analyze", "Analyze"),
  "Run the analysis on the selected data"
)
```

**Key insight:** `tooltip()` uses the **last HTML element** in its first argument as the trigger. This means you can place an icon next to text using `span()` or `tagList()`, and only the icon becomes the trigger.

Common placements: wrap an `bsicons::bs_icon("info-circle")` inside `card_header()`, use `span("Label", bsicons::bs_icon("info-circle"))` as an input label, or nest inside a `value_box()` `title`.

### Dynamic Tooltips

**`toggle_tooltip()`** shows or hides a tooltip programmatically. **`update_tooltip()`** changes its content:

```r
# UI
tooltip(id = "help_tip", actionButton("analyze", "Analyze"), "Click to run analysis")

# Server
observe({
  toggle_tooltip("help_tip", show = TRUE)
}) |> bindEvent(once = TRUE)

observeEvent(input$update_status, {
  update_tooltip("status_tip", paste("Last updated:", Sys.time()))
})
```

## Popovers

### Basic Usage

`popover()` accepts any content as additional arguments and an optional `title`:

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

### Dynamic Popovers

**`toggle_popover()`** and **`update_popover()`** work like their tooltip counterparts:

```r
# UI
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

observeEvent(input$run, {
  update_popover("progress_pop", "Running analysis...")
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
