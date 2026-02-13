# UI Components in bslib

This reference covers additional UI components in bslib beyond cards and navigation: accordions, tooltips, popovers, and toasts.

## Table of Contents

- [Accordions](#accordions)
  - [Basic Usage](#basic-usage)
  - [In Sidebars](#accordions-in-sidebars)
  - [Dynamic Control](#dynamic-accordion-control)
- [Tooltips](#tooltips)
  - [Basic Usage](#tooltip-basic-usage)
  - [Common Patterns](#tooltip-patterns)
  - [Dynamic Tooltips](#dynamic-tooltips)
- [Popovers](#popovers)
  - [Basic Usage](#popover-basic-usage)
  - [Common Patterns](#popover-patterns)
  - [Dynamic Popovers](#dynamic-popovers)
- [Tooltips vs Popovers](#tooltips-vs-popovers)
- [Toasts](#toasts)
  - [Basic Usage](#toast-basic-usage)
  - [Showing and Hiding Toasts](#showing-and-hiding-toasts)
- [Best Practices](#best-practices)

## Accordions

Accordions provide collapsible sections for organizing content vertically. They're useful for grouping information, reducing visual clutter, and providing progressive disclosure.

### Basic Usage

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

### Accordions in Sidebars

When an `accordion()` appears as an immediate child of `sidebar()`, panels render flush to the sidebar for clean organization:

**Example:**
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

### Dynamic Accordion Control

Programmatically control accordion state with these functions:

#### accordion_panel_open()

Open specific panels:

```r
# Server
observeEvent(input$show_advanced, {
  accordion_panel_open("acc", "Advanced Settings")
})
```

#### accordion_panel_close()

Close specific panels:

```r
# Server
observeEvent(input$hide_advanced, {
  accordion_panel_close("acc", "Advanced Settings")
})
```

#### accordion_panel_set()

Set which panels are open:

```r
# Server
observeEvent(input$reset, {
  accordion_panel_set("acc", c("Panel 1"))  # Only Panel 1 open
})
```

#### accordion_panel_insert()

Add new panels dynamically:

```r
# Server
observeEvent(input$add_panel, {
  accordion_panel_insert(
    "acc",
    accordion_panel("New Panel", "Dynamic content"),
    target = "Panel 2",
    position = "after"
  )
})
```

#### accordion_panel_remove()

Remove panels dynamically:

```r
# Server
observeEvent(input$remove, {
  accordion_panel_remove("acc", "Panel to Remove")
})
```

#### accordion_panel_update()

Update panel content:

```r
# Server
observeEvent(input$update, {
  accordion_panel_update(
    "acc",
    "Panel 1",
    "Updated content"
  )
})
```

## Tooltips

Tooltips are small, hover-triggered messages that provide additional context without cluttering the UI. They're perfect for "read-only" supplementary information.

### Tooltip Basic Usage

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

**Multiple elements as trigger:**
```r
# Entire span is trigger
span(
  "Revenue ",
  bsicons::bs_icon("question-circle"),
  tooltip("Total revenue from all sources")
)
```

**Icon-only trigger:**
```r
# Only icon is trigger (using list or tagList)
tagList(
  "Revenue ",
  tooltip(
    bsicons::bs_icon("question-circle"),
    "Total revenue from all sources"
  )
)
```

**Key insight:** `tooltip()` uses the **last HTML element** in its first argument as the trigger.

### Tooltip Patterns

#### Input Labels

Add tooltips to input labels for contextual help:

**Example:**
```r
textInput(
  "username",
  tooltip(
    span("Username", bsicons::bs_icon("info-circle")),
    "Your username must be 3-20 characters"
  )
)
```

#### Card Headers

Provide context about card content:

**Example:**
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

#### Value Boxes

Explain metrics:

**Example:**
```r
value_box(
  title = tooltip(
    span("MRR", bsicons::bs_icon("question-circle")),
    "Monthly Recurring Revenue"
  ),
  value = "$45,678"
)
```

#### Tables and Plots

Provide legend or methodology information:

**Example:**
```r
card(
  card_header(
    "Sales Trend",
    tooltip(
      bsicons::bs_icon("info-circle"),
      "Smoothed using LOESS with span=0.3"
    )
  ),
  plotOutput("sales_trend")
)
```

### Dynamic Tooltips

#### toggle_tooltip()

Show or hide programmatically:

**Example:**
```r
# UI
tooltip(
  id = "help_tip",
  actionButton("analyze", "Analyze"),
  "Click to run analysis"
)

# Server
# Show tooltip on page load
observe({
  toggle_tooltip("help_tip", show = TRUE)
}) |> bindEvent(once = TRUE)
```

#### update_tooltip()

Change tooltip content dynamically:

**Example:**
```r
# UI
tooltip(
  id = "status_tip",
  textOutput("status"),
  "Status information"
)

# Server
observeEvent(input$update_status, {
  update_tooltip(
    "status_tip",
    paste("Last updated:", Sys.time())
  )
})
```

## Popovers

Popovers are click-triggered containers that can hold interactive content. They're more "persistent" than tooltips and support richer content.

### Popover Basic Usage

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

### Popover Patterns

#### Input Toolbars in Card Headers

Place secondary inputs in a popover to save space:

**Example:**
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

**Use case:** Tweaking parameters that don't warrant permanent sidebar space.

#### Hyperlink Context

Provide additional context without leaving the page:

**Example:**
```r
card_footer(
  "Data source: ",
  popover(
    tags$a("National Survey", href = "#"),
    title = "About the Data",
    "This data comes from the 2023 National Survey conducted by...",
    tags$a("Learn more", href = "https://example.com", target = "_blank")
  )
)
```

#### Editable Card Titles

Combine popover with dynamic UI for inline editing:

**Example:**
```r
# UI
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

# Server
card_title <- reactiveVal("My Plot")

output$card_title <- renderUI({
  card_title()
})

observeEvent(input$save_title, {
  card_title(input$new_title)
})
```

#### Help Documentation

Provide contextual help:

**Example:**
```r
sidebar(
  title = "Filters",
  popover(
    bsicons::bs_icon("question-circle"),
    title = "How to Use Filters",
    tags$p("Filters are applied in real-time as you change selections."),
    tags$p("Reset all filters using the button below."),
    tags$p(tags$strong("Tip:"), " Use Shift+Click to select multiple items.")
  ),
  selectInput("category", "Category", ...),
  dateRangeInput("dates", "Date Range", ...)
)
```

### Dynamic Popovers

#### toggle_popover()

Show or hide programmatically:

**Example:**
```r
# UI
popover(
  id = "welcome_pop",
  actionButton("start", "Start"),
  title = "Welcome!",
  "Click Start to begin the analysis."
)

# Server
# Show on page load
observe({
  toggle_popover("welcome_pop", show = TRUE)
}) |> bindEvent(once = TRUE)

# Hide when button clicked
observeEvent(input$start, {
  toggle_popover("welcome_pop", show = FALSE)
})
```

#### update_popover()

Change content dynamically:

**Example:**
```r
# UI
popover(
  id = "progress_pop",
  actionButton("run", "Run"),
  title = "Status",
  "Click to start"
)

# Server
observeEvent(input$run, {
  update_popover("progress_pop", "Running analysis...")

  # Simulate work
  Sys.sleep(2)

  update_popover("progress_pop", "Complete!")
})
```

## Tooltips vs Popovers

### When to Use Tooltips

**Use tooltips for:**
- Short, read-only messages (1-2 sentences)
- Icon explanations
- Input label clarifications
- Quick contextual help
- Non-interactive content

**Triggered by:** Hover or focus (automatic)

**Example:**
```r
tooltip(
  bsicons::bs_icon("info-circle"),
  "This metric updates every 5 minutes"
)
```

### When to Use Popovers

**Use popovers for:**
- Interactive content (inputs, buttons)
- Longer explanations
- Lists or structured content
- Secondary controls
- Content users should actively engage with

**Triggered by:** Click (manual)

**Example:**
```r
popover(
  bsicons::bs_icon("gear"),
  title = "Options",
  selectInput("option1", "Option 1", ...),
  checkboxInput("option2", "Option 2")
)
```

### Key Differences

| Feature | Tooltip | Popover |
|---------|---------|---------|
| **Trigger** | Hover/focus | Click |
| **Persistence** | Disappears quickly | Remains until dismissed |
| **Content** | Text only (read-only) | Rich content (interactive) |
| **Use case** | Quick help | Secondary UI |
| **User effort** | Passive | Active |

**Guidance:** "Use tooltips for small 'read-only' messages, and popovers when the user should be able to interact with the message itself."

### Popovers vs Modals

**Popovers:** Non-blocking - users can interact with other UI while popover is open

**Modals:** Blocking - users must address modal before continuing

**Use modal when:** User must complete an action (confirm deletion, submit form)

**Use popover when:** User can continue working while referencing popover content

## Toasts

Toasts are temporary notification messages that appear (typically in a corner) to provide feedback without interrupting workflow.

### Toast Basic Usage

**Create a toast:**

```r
my_toast <- toast(
  "Analysis complete!",
  "Your results are ready to view."
)
```

**With title:**
```r
my_toast <- toast(
  toast_header("Success"),
  "Analysis completed successfully."
)
```

**Different intent:**
```r
# Success
toast(toast_header("Success", class = "bg-success text-white"), "...")

# Warning
toast(toast_header("Warning", class = "bg-warning"), "...")

# Error
toast(toast_header("Error", class = "bg-danger text-white"), "...")

# Info
toast(toast_header("Info", class = "bg-info text-white"), "...")
```

### Showing and Hiding Toasts

#### show_toast()

Display a toast notification:

**Example:**
```r
# Server
observeEvent(input$analyze, {
  # Run analysis
  result <- run_analysis()

  # Show toast
  show_toast(
    toast(
      toast_header("Analysis Complete", class = "bg-success text-white"),
      "Results are now available in the table below."
    )
  )
})
```

**With options:**
```r
show_toast(
  toast("Message"),
  autohide = TRUE,  # Auto-dismiss
  delay = 5000      # Dismiss after 5 seconds
)
```

#### hide_toast()

Dismiss a toast programmatically:

**Example:**
```r
# UI
my_toast <- toast(
  id = "progress_toast",
  "Processing..."
)

# Server
observeEvent(input$start, {
  show_toast(my_toast, autohide = FALSE)

  # Long-running operation
  result <- expensive_computation()

  # Hide toast when done
  hide_toast("progress_toast")
})
```

### Common Toast Patterns

#### Success Notifications

```r
observeEvent(input$save, {
  tryCatch({
    save_data(data())
    show_toast(
      toast(
        toast_header("Saved", class = "bg-success text-white"),
        "Data saved successfully."
      )
    )
  }, error = function(e) {
    show_toast(
      toast(
        toast_header("Error", class = "bg-danger text-white"),
        paste("Failed to save:", e$message)
      )
    )
  })
})
```

#### Progress Updates

```r
observeEvent(input$export, {
  show_toast(
    toast(id = "export_toast", "Exporting data..."),
    autohide = FALSE
  )

  export_data()

  hide_toast("export_toast")

  show_toast(
    toast(
      toast_header("Export Complete", class = "bg-success text-white"),
      "File downloaded to your Downloads folder."
    )
  )
})
```

#### Multiple Toasts

```r
# Show multiple toasts for different events
observe({
  if (data_updated()) {
    show_toast(toast("Data refreshed"))
  }

  if (new_notifications()) {
    show_toast(toast("You have new notifications"))
  }
})
```

## Best Practices

### Tooltips

**Keep them concise:**
- 1-2 sentences maximum
- Focus on essential information
- Avoid redundancy with visible UI

**Use consistent placement:**
```r
# Prefer icon next to label
tooltip(
  span("Label ", bsicons::bs_icon("info-circle")),
  "Explanation"
)
```

**Test hover interaction:**
- Ensure tooltips don't block important UI
- Verify tooltips are accessible on mobile (consider popovers for mobile)

### Popovers

**Limit interactive elements:**
- 2-4 inputs maximum
- Avoid complex forms
- Consider modal for extensive interaction

**Provide clear titles:**
```r
popover(
  trigger,
  title = "Plot Options",  # Clear, descriptive
  ...
)
```

**Don't use hyperlinks as triggers:**
Conflicts with click behavior. Instead:

```r
# Bad
popover(tags$a("Link"), "Content")

# Good - icon next to link
tagList(
  tags$a("Link", href = "#"),
  popover(bsicons::bs_icon("info-circle"), "Context about link")
)
```

### Accordions

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
- Consider user mental model

**Limit panel count:**
- 3-6 panels is ideal
- More than 8 becomes unwieldy
- Consider alternative organization if needed

**Set appropriate initial state:**
```r
# Most important panel open
accordion(
  open = "Essential Filters",
  accordion_panel("Essential Filters", ...),
  accordion_panel("Advanced Filters", ...),
  accordion_panel("Export Options", ...)
)
```

### Toasts

**Be specific:**
```r
# Good
show_toast(toast("Analysis complete", "Results saved to output.csv"))

# Too vague
show_toast(toast("Done"))
```

**Set appropriate timing:**
- Success messages: 3-5 seconds
- Error messages: No auto-hide (let user read and dismiss)
- Progress updates: No auto-hide until complete

**Use sparingly:**
- Don't toast every minor action
- Combine multiple similar events
- Avoid toast overload

**Position consistently:**
Toasts typically appear in the same corner throughout the app (default: top-right).

### Accessibility

**Tooltips:**
- Ensure keyboard accessible (built-in)
- Provide alt text for icon triggers
- Test with screen readers for public apps

**Popovers:**
- Keyboard dismissible (Esc key)
- Focus management (return focus after close)
- ARIA labels for trigger elements

**Accordions:**
- Keyboard navigation (arrow keys, Enter)
- ARIA attributes (automatic)
- Ensure panel titles are meaningful

**Toasts:**
- Use ARIA live regions (automatic)
- Don't rely solely on color for meaning
- Ensure sufficient contrast
