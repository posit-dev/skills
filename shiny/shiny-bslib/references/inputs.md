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

A specialized switch for toggling between light and dark themes, built on [Bootstrap 5.3 color modes](https://getbootstrap.com/docs/5.3/customize/color-modes/). This toggle automatically switches the Bootstrap color mode attribute on the page.

**Important:** `input_dark_mode()` relies on Bootstrap 5.3+ color mode support. For full dark mode theming with custom colors, combine it with `session$setCurrentTheme()` to switch between custom light and dark `bs_theme()` objects. See [theming.md](theming.md) for details.

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
      toggle_dark_mode(mode = saved_mode)
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

For truly long-running tasks, combine with `ExtendedTask` and `bind_task_button()`. The button stays in "busy" state for as long as the extended task is running.

**Example:**
```r
library(shiny)
library(bslib)
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
  # Define extended task and bind to button
  long_task <- ExtendedTask$new(function() {
    future({
      Sys.sleep(10)  # Simulate long operation
      "Task complete!"
    }, seed = TRUE)
  }) |> bind_task_button("run")

  # Trigger task on button click
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

Binds a task button to an `ExtendedTask` so the button reflects the task's state. The first argument is the task, the second is the button ID:

```r
# Piped style (recommended)
my_task <- ExtendedTask$new(...) |> bind_task_button("my_button")

# Or explicit call
bind_task_button(my_task, "my_button")
```

**Note:** `bind_task_button()` does NOT trigger the task on click -- you still need `observeEvent()` to invoke it.

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

  show_toast(toast("Export complete!", type = "success"))
})
```

## input_code_editor()

A lightweight code editor with syntax highlighting, powered by [prism-code-editor](https://prism-code-editor.netlify.app/). Supports 20+ languages and automatic light/dark mode switching. Try `shiny::runExample("code-editor", package = "bslib")` for a complete demo.

**Important:** The editor value is not sent on every keystroke. Updates reach the server when the user moves focus away from the editor or presses `Ctrl/Cmd+Enter`. Not designed for large files (1000+ lines may have performance issues).

### Basic Usage

**Simple code editor:**
```r
input_code_editor(
  id = "user_code",
  language = "r",
  value = "# Enter your R code here\n"
)
```

**Supported languages:** `"r"`, `"python"`, `"julia"`, `"sql"`, `"javascript"`, `"typescript"`, `"html"`, `"css"`, `"scss"`, `"sass"`, `"json"`, `"markdown"`, `"yaml"`, `"xml"`, `"toml"`, `"ini"`, `"bash"`, `"docker"`, `"latex"`, `"cpp"`, `"rust"`, `"diff"`, `"plain"`.

**With dynamic language switching:**
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
  height = "400px"  # Default is "auto"
)
```

**Themes (auto-switches with dark mode):**
```r
input_code_editor(
  id = "code",
  language = "r",
  theme_light = "github-light",  # Default
  theme_dark = "github-dark"     # Default
)
```

Available themes: `"atom-one-dark"`, `"dracula"`, `"github-dark-dimmed"`, `"github-dark"`, `"github-light"`, `"night-owl-light"`, `"night-owl"`, `"prism-okaidia"`, `"prism-solarized-light"`, `"prism-tomorrow"`, `"prism-twilight"`, `"prism"`, `"vs-code-dark"`, `"vs-code-light"`.

**Read-only mode:**
```r
input_code_editor(
  id = "code",
  language = "r",
  value = "# Read-only code example",
  read_only = TRUE
)
```

**Other options:** `line_numbers` (default TRUE), `word_wrap`, `tab_size` (default 2), `indentation` (`"space"` or `"tab"`), `fill` (default TRUE for filling containers).

### Keyboard Shortcuts

- `Ctrl/Cmd+Enter`: Submit current code to R
- `Ctrl/Cmd+Z`: Undo
- `Ctrl/Cmd+Shift+Z`: Redo
- `Tab`: Indent selection
- `Shift+Tab`: Dedent selection

### Common Patterns

#### SQL Query Builder

```r
# UI
page_sidebar(
  sidebar = sidebar(
    selectInput("table", "Table", c("users", "orders", "products")),
    input_task_button("run_query", "Run Query")
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
    run_query(input$sql_query)
  })
})
```

### When to Use

**Use `input_code_editor()` when:**
- Users need to write code snippets with syntax highlighting
- Building SQL query builders, expression editors, or config editors
- Displaying read-only code with highlighting

## input_submit_textarea()

A textarea with explicit submission, preventing reactive updates on every keystroke. Ideal for chat boxes, comments, or any input where users compose and review text before submitting. The textarea auto-grows as the user types.

**Important:** The initial server value is always `""` (empty string), regardless of the `value` parameter. The server value only updates when the user explicitly submits (via button click or keyboard shortcut).

### Basic Usage

**Simple submit textarea:**
```r
input_submit_textarea(
  id = "user_input",
  label = "Enter text:",
  placeholder = "Type your text here..."
)
```

**With more rows and custom width:**
```r
input_submit_textarea(
  id = "comments",
  label = "Comments:",
  rows = 6,
  width = "100%"
)
```

### Submission Behavior

**Default (`submit_key = "enter+modifier"`):** User holds `Ctrl` (or `Cmd` on Mac) and presses `Enter` to submit. This prevents accidental submissions.

**Enter-only submission:**
```r
input_submit_textarea(
  id = "chat_input",
  placeholder = "Type a message...",
  submit_key = "enter"  # Submit with Enter, Shift+Enter for new lines
)
```

### Custom Submit Button

The `button` parameter accepts any HTML element. Using `input_task_button()` is recommended for built-in busy state:

```r
input_submit_textarea(
  id = "query",
  placeholder = "Ask a question...",
  button = input_task_button("submit_query", "Send", icon = bsicons::bs_icon("send"))
)
```

### Toolbar Items

Add extra UI elements next to the submit button with `toolbar`:

```r
input_submit_textarea(
  id = "message",
  placeholder = "Write a message...",
  toolbar = list(
    actionLink("attach", bsicons::bs_icon("paperclip")),
    actionLink("emoji", bsicons::bs_icon("emoji-smile"))
  )
)
```

### Update Submit Textarea

```r
# Server
observeEvent(input$load_template, {
  update_submit_textarea("user_input", value = "Template text here...")
})

# Submit programmatically
update_submit_textarea("user_input", value = "Auto text", submit = TRUE)

# Move focus to the textarea
update_submit_textarea("user_input", focus = TRUE)
```

### Common Patterns

#### Chat Interface

```r
# UI
card(
  card_header("Chat"),
  card_body(uiOutput("chat_messages"), fillable = FALSE, fill = TRUE),
  card_footer(
    input_submit_textarea(
      id = "chat_input",
      placeholder = "Type a message...",
      submit_key = "enter"
    )
  )
)

# Server
observeEvent(input$chat_input, {
  req(nchar(input$chat_input) > 0)
  add_message(input$chat_input)
  update_submit_textarea("chat_input", value = "")
})
```

### When to Use

**Use `input_submit_textarea()` when:**
- Downstream computations are expensive (API calls, model inference)
- Users need to compose and review before submitting
- Building chat or comment interfaces

**Use regular `textAreaInput()` when:**
- Live preview of changes is desired
- Downstream computations are cheap

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
  result <- process_data()

  show_toast(
    toast("Processing finished successfully", header = "Complete", type = "success")
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
      toast(e$message, header = "Error", type = "danger", duration_s = NA)
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
