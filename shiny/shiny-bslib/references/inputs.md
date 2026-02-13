# Special Inputs in bslib

bslib provides several specialized input widgets that enhance standard Shiny inputs with modern features. This reference covers these bslib-specific inputs.

## Table of Contents

- [input_switch()](#input_switch)
- [input_dark_mode()](#input_dark_mode)
- [input_task_button()](#input_task_button)
- [input_code_editor()](#input_code_editor)
- [input_submit_textarea()](#input_submit_textarea)

## input_switch()

A modern toggle switch input, an alternative to `checkboxInput()` with better visual design.

### Basic Usage

**Simple switch:**
```r
input_switch(
  id = "enable_feature",
  label = "Enable advanced features"
)
```

**With initial value:**
```r
input_switch(
  id = "notifications",
  label = "Enable notifications",
  value = TRUE
)
```

**Example in sidebar:**
```r
page_sidebar(
  sidebar = sidebar(
    input_switch("show_trend", "Show trend line"),
    input_switch("show_outliers", "Show outliers", value = FALSE),
    input_switch("log_scale", "Log scale")
  ),
  card(plotOutput("plot"))
)
```

### Update and Toggle

**update_switch():**
```r
# Server
observeEvent(input$reset, {
  update_switch("enable_feature", value = FALSE)
})
```

**toggle_switch():**
```r
# Server
observeEvent(input$toggle_all, {
  toggle_switch("feature1")
  toggle_switch("feature2")
  toggle_switch("feature3")
})
```

### When to Use

**Prefer `input_switch()` over `checkboxInput()` when:**
- Representing an on/off or enable/disable state
- The change takes immediate effect
- You want modern, mobile-friendly UI
- Space is limited

**Use `checkboxInput()` when:**
- Representing selection/agreement (e.g., "I agree to terms")
- The change requires form submission
- You need multiple checkboxes in a group

**Example - good switch usage:**
```r
sidebar(
  title = "Plot Options",
  input_switch("show_grid", "Show grid lines", value = TRUE),
  input_switch("show_legend", "Show legend", value = TRUE),
  input_switch("dark_bg", "Dark background")
)
```

## input_dark_mode()

A specialized switch for toggling between light and dark themes, with built-in theme switching logic.

### Basic Usage

**Simple dark mode toggle:**
```r
# UI
page_sidebar(
  sidebar = sidebar(
    input_dark_mode(id = "mode")
  ),
  ...
)
```

**With initial mode:**
```r
input_dark_mode(
  id = "mode",
  mode = "dark"  # Start in dark mode
)
```

### Accessing Mode

**In server logic:**
```r
# Server
observe({
  current_mode <- input$mode
  # "light" or "dark"
})
```

### With Custom Themes

Combine with `session$setCurrentTheme()` for full control:

**Example:**
```r
# UI
ui <- page_navbar(
  title = "My App",
  sidebar = sidebar(
    input_dark_mode(id = "theme_mode", mode = "light")
  ),
  nav_panel("Home", ...)
)

# Server
server <- function(input, output, session) {
  # Define themes
  light_theme <- bs_theme(
    bg = "#FFFFFF",
    fg = "#212529",
    primary = "#007bff",
    base_font = font_google("Lato")
  )

  dark_theme <- bs_theme(
    bg = "#1a1a1a",
    fg = "#f8f9fa",
    primary = "#375a7f",
    base_font = font_google("Lato")
  )

  # Switch themes based on input
  observe({
    if (input$theme_mode == "dark") {
      session$setCurrentTheme(dark_theme)
    } else {
      session$setCurrentTheme(light_theme)
    }
  })
}
```

### User Preference Persistence

Store user preference using browser storage or cookies:

**Example with cookies:**
```r
library(cookies)

server <- function(input, output, session) {
  # Read saved preference on start
  observe({
    saved_mode <- get_cookie("theme_mode")
    if (!is.null(saved_mode)) {
      update_dark_mode("mode", mode = saved_mode)
    }
  }) |> bindEvent(once = TRUE)

  # Save preference when changed
  observeEvent(input$mode, {
    set_cookie("theme_mode", input$mode)
  })
}
```

### When to Use

**Use `input_dark_mode()` when:**
- Offering light/dark theme switching
- You want automatic icon and label handling
- Building apps for extended viewing sessions
- Following modern UI patterns

**Features:**
- Automatic moon/sun icons
- Clear visual indication of current mode
- Integrates naturally with bslib themes
- Mobile-friendly

## input_task_button()

A specialized action button designed for longer-running operations, with built-in loading state indication.

### Basic Usage

**Simple task button:**
```r
# UI
input_task_button(
  id = "run_analysis",
  label = "Run Analysis"
)

# Server
observeEvent(input$run_analysis, {
  # Long-running operation
  result <- expensive_computation()
  output$result <- renderText(result)
})
```

**With auto-disable:**
The button automatically disables while the task runs, providing visual feedback.

### With Extended Tasks

For truly long-running tasks, combine with `ExtendedTask`:

**Example:**
```r
library(shiny)
library(bslib)
library(promises)
library(future)
plan(multisession)

# UI
ui <- page_sidebar(
  sidebar = sidebar(
    input_task_button("run", "Run Long Task")
  ),
  card(textOutput("result"))
)

# Server
server <- function(input, output, session) {
  # Define extended task
  long_task <- ExtendedTask$new(function() {
    future_promise({
      Sys.sleep(10)  # Simulate long operation
      "Task complete!"
    })
  })

  # Bind button to task
  observeEvent(input$run, {
    long_task$invoke()
  })

  # Display result
  output$result <- renderText({
    long_task$result()
  })
}
```

### bind_task_button()

Explicitly bind a task button to an ExtendedTask:

**Example:**
```r
# UI
ui <- page_sidebar(
  sidebar = sidebar(
    input_task_button("analyze", "Analyze Data")
  ),
  card(
    plotOutput("plot"),
    textOutput("status")
  )
)

# Server
server <- function(input, output, session) {
  analysis_task <- ExtendedTask$new(function(data) {
    future_promise({
      # Complex analysis
      expensive_analysis(data)
    })
  })

  # Bind button to task
  bind_task_button("analyze", analysis_task)

  observeEvent(input$analyze, {
    analysis_task$invoke(filtered_data())
  })

  output$plot <- renderPlot({
    req(analysis_task$result())
    plot(analysis_task$result())
  })

  output$status <- renderText({
    if (analysis_task$is_running()) {
      "Analysis in progress..."
    } else {
      "Analysis complete"
    }
  })
}
```

### Update Button

**update_task_button():**
```r
# Server
observeEvent(input$complete, {
  update_task_button(
    "run_analysis",
    label = "Analysis Complete",
    icon = bsicons::bs_icon("check")
  )
})
```

### When to Use

**Use `input_task_button()` when:**
- Operations take more than ~2 seconds
- Users should wait for completion before continuing
- You want built-in loading indication
- Preventing duplicate submissions is important

**Prefer `actionButton()` when:**
- Operations are near-instantaneous
- Multiple rapid clicks are acceptable
- You have custom loading indicators

**Example - good task button usage:**
```r
sidebar(
  title = "Export",
  selectInput("format", "Format", c("CSV", "Excel", "PDF")),
  input_task_button("export", "Export Data", icon = bsicons::bs_icon("download"))
)

# Server
observeEvent(input$export, {
  # Long export operation
  export_data(data(), format = input$format)

  show_toast(toast("Export complete!"))
})
```

## input_code_editor()

A code editor input widget with syntax highlighting, perfect for allowing users to input code snippets.

### Basic Usage

**Simple code editor:**
```r
input_code_editor(
  id = "user_code",
  language = "r",
  value = "# Enter your R code here\n"
)
```

**With multiple languages:**
```r
page_sidebar(
  sidebar = sidebar(
    selectInput("language", "Language", c("r", "python", "sql", "javascript"))
  ),
  card(
    card_header("Code Editor"),
    input_code_editor(
      id = "code",
      language = "r",
      value = "# Code here"
    )
  )
)

# Server
observeEvent(input$language, {
  update_code_editor("code", language = input$language)
})
```

### Configuration Options

**Height control:**
```r
input_code_editor(
  id = "code",
  language = "r",
  height = "400px"
)
```

**Theme:**
```r
input_code_editor(
  id = "code",
  language = "r",
  theme = "vs-dark"  # Dark theme for the editor
)
```

**Read-only mode:**
```r
input_code_editor(
  id = "code",
  language = "r",
  value = "# Read-only code example",
  readonly = TRUE
)
```

### Update Code Editor

**update_code_editor():**
```r
# Server
observeEvent(input$load_example, {
  update_code_editor(
    "user_code",
    value = "ggplot(data, aes(x, y)) +\n  geom_point()"
  )
})
```

### Common Patterns

#### Code Evaluation

```r
# UI
card(
  card_header("R Code Editor"),
  input_code_editor(
    id = "r_code",
    language = "r",
    value = "# Write R code\n1 + 1"
  ),
  actionButton("eval", "Evaluate"),
  card_footer(
    verbatimTextOutput("result")
  )
)

# Server
observeEvent(input$eval, {
  result <- tryCatch({
    eval(parse(text = input$r_code))
  }, error = function(e) {
    paste("Error:", e$message)
  })

  output$result <- renderPrint({
    result
  })
})
```

#### Query Builder

```r
# UI
page_sidebar(
  sidebar = sidebar(
    selectInput("table", "Table", c("users", "orders", "products")),
    actionButton("run_query", "Run Query", class = "btn-primary w-100")
  ),
  card(
    card_header("SQL Query"),
    input_code_editor(
      id = "sql_query",
      language = "sql",
      value = "SELECT * FROM users\nLIMIT 10;"
    )
  ),
  card(
    card_header("Results"),
    tableOutput("query_results")
  )
)

# Server
observeEvent(input$run_query, {
  output$query_results <- renderTable({
    # Execute query (safely!)
    run_query(input$sql_query)
  })
})
```

### When to Use

**Use `input_code_editor()` when:**
- Users need to write code snippets
- Syntax highlighting improves usability
- Code validation/linting would help users
- Building developer-focused tools

**Examples:**
- SQL query builders
- R/Python code notebooks
- API request builders
- Configuration file editors
- Custom formula/expression inputs

## input_submit_textarea()

A textarea with explicit submission control, preventing reactive updates on every keystroke.

### Basic Usage

**Basic submit textarea:**
```r
input_submit_textarea(
  id = "long_text",
  label = "Enter text:",
  placeholder = "Type your text here...",
  submit_label = "Submit"
)
```

**With rows:**
```r
input_submit_textarea(
  id = "comments",
  label = "Comments:",
  rows = 10,
  submit_label = "Post Comment"
)
```

### Behavior

Unlike regular `textAreaInput()`, this doesn't trigger reactive updates on every keystroke. It only updates when the user explicitly submits.

**Example:**
```r
# UI
page_sidebar(
  sidebar = sidebar(
    input_submit_textarea(
      id = "analysis_notes",
      label = "Analysis Notes:",
      placeholder = "Enter notes about the analysis...",
      rows = 8,
      submit_label = "Save Notes"
    )
  ),
  card(
    card_header("Saved Notes"),
    verbatimTextOutput("notes_display")
  )
)

# Server
output$notes_display <- renderText({
  # Only updates when submitted
  input$analysis_notes
})
```

### Update Submit Textarea

**update_submit_textarea():**
```r
# Server
observeEvent(input$load_template, {
  update_submit_textarea(
    "long_text",
    value = "Template text here..."
  )
})
```

### When to Use

**Use `input_submit_textarea()` when:**
- Long-form text input is needed
- Expensive computations triggered by input changes
- Users should explicitly save/submit their input
- Preventing accidental triggering is important

**Use regular `textAreaInput()` when:**
- Live preview of changes is desired
- Downstream computations are cheap
- Immediate feedback enhances UX

**Example - comments system:**
```r
card(
  card_header("Add Comment"),
  input_submit_textarea(
    id = "new_comment",
    label = NULL,
    placeholder = "Write your comment...",
    rows = 4,
    submit_label = "Post Comment"
  )
)

# Server
observeEvent(input$new_comment, {
  # Only triggers when "Post Comment" is clicked
  save_comment(input$new_comment)

  # Clear the textarea
  update_submit_textarea("new_comment", value = "")

  show_toast(toast("Comment posted!"))
})
```

## Best Practices

### Choose the Right Input

**input_switch() vs checkboxInput():**
- Switch: on/off states, immediate effect
- Checkbox: selection/agreement, form submission

**input_task_button() vs actionButton():**
- Task button: long operations (>2 seconds), prevent duplicates
- Action button: quick operations, custom loading logic

**input_code_editor() vs textAreaInput():**
- Code editor: code snippets, syntax highlighting valuable
- Text area: plain text, notes, comments

**input_submit_textarea() vs textAreaInput():**
- Submit textarea: expensive downstream operations
- Text area: cheap operations, live preview

### Consistent Placement

Group similar inputs:
```r
sidebar(
  title = "Display Options",
  # All switches together
  input_switch("show_grid", "Show grid"),
  input_switch("show_legend", "Show legend"),
  input_switch("show_labels", "Show labels"),
  hr(),
  # Dark mode separate
  input_dark_mode("theme")
)
```

### Clear Labels

Use descriptive labels:
```r
# Good
input_switch("enable_caching", "Enable result caching")
input_task_button("export_csv", "Export to CSV")

# Avoid
input_switch("cache", "Cache")
input_task_button("export", "Export")
```

### Provide Feedback

For task buttons, show completion feedback:
```r
observeEvent(input$process, {
  # Long operation
  result <- process_data()

  # Show feedback
  show_toast(
    toast(
      toast_header("Complete", class = "bg-success text-white"),
      "Processing finished successfully"
    )
  )
})
```

### Handle Errors Gracefully

Especially with code editor:
```r
observeEvent(input$run_code, {
  result <- tryCatch({
    eval(parse(text = input$code))
  }, error = function(e) {
    show_toast(
      toast(
        toast_header("Error", class = "bg-danger text-white"),
        e$message
      )
    )
    NULL
  })

  if (!is.null(result)) {
    output$result <- renderPrint(result)
  }
})
```

### Test Accessibility

- Ensure all inputs are keyboard accessible (built-in)
- Provide clear labels for screen readers
- Test with keyboard-only navigation
- Verify focus indicators are visible

### Mobile Considerations

- Switches work well on mobile (large touch targets)
- Code editors may be challenging on small screens
- Consider responsive alternatives for mobile users
- Test task buttons on slower connections

### Responsive Design

Adjust input layouts for different screen sizes:
```r
layout_columns(
  col_widths = breakpoints(
    sm = 12,  # Full width on mobile
    md = 6,   # Half width on tablet
    lg = 4    # Third width on desktop
  ),
  input_switch("option1", "Option 1"),
  input_switch("option2", "Option 2"),
  input_switch("option3", "Option 3")
)
```
