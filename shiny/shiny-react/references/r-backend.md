# R Backend Reference

Complete guide for building shiny-react apps with R Shiny backends.

## Table of Contents

- [Setup](#setup)
- [shinyreact.R Functions](#shinyreactr-functions)
- [Rendering Patterns](#rendering-patterns)
- [Message Handling](#message-handling)
- [Complete Example](#complete-example)

## Setup

### File Structure

```
myapp/
├── r/
│   ├── app.R           # Main Shiny application
│   ├── shinyreact.R    # Utility functions (copy from template)
│   └── www/            # Built JS/CSS from esbuild
│       ├── main.js
│       └── main.css
```

### Minimal app.R

```r
library(shiny)

source("shinyreact.R", local = TRUE)

server <- function(input, output, session) {
  # Your server logic here
}

shinyApp(ui = page_react(title = "My App"), server = server)
```

## shinyreact.R Functions

These functions are provided in the `shinyreact.R` utility file.

### page_react()

Creates the HTML page shell for React apps.

```r
page_react(
  ...,                    # Additional UI elements
  title = NULL,           # Page title
  js_file = "main.js",    # JavaScript bundle (NULL to skip)
  css_file = "main.css",  # CSS file (NULL to skip)
  lang = "en"             # HTML lang attribute
)
```

**What it does:**
- Creates minimal HTML with jQuery dependency (required by Shiny)
- Includes `<div id="root">` for React mounting
- Links JS/CSS from `www/` directory

**Example:**
```r
ui <- page_react(
  title = "My Dashboard",
  js_file = "main.js",
  css_file = "main.css"
)
```

### render_json()
Renders arbitrary R objects as JSON for React consumption.

```r
render_json(
  expr,                   # R expression to evaluate
  env = parent.frame(),   # Environment for evaluation
  quoted = FALSE,         # Is expr already quoted?
  outputArgs = list()     # Additional output arguments
)
```

**What it does:**
- Evaluates the expression reactively
- Serializes result via `shiny:::toJSON()`
- Sends to React via custom Shiny output binding

**Examples:**

```r
# Simple values
output$greeting <- render_json({
  paste("Hello,", input$name)
})

# Data frames (become column-major JSON)
output$table_data <- render_json({
  mtcars[1:input$num_rows, ]
})

# Lists become JSON objects
output$stats <- render_json({
  list(
    mean = mean(mtcars$mpg),
    sd = sd(mtcars$mpg),
    n = nrow(mtcars)
  )
})

# Nested structures
output$config <- render_json({
  list(
    settings = list(theme = "dark", fontSize = 14),
    data = head(iris, 5)
  )
})
```

### post_message()

Send custom messages from server to React.

```r
post_message(session, type, data)
```

**Parameters:**
- `session`: Shiny session object
- `type`: Message type string (matches `useShinyMessageHandler` type)
- `data`: Any JSON-serializable R object

**Examples:**

```r
# Toast notification
post_message(session, "toast", list(
  text = "File saved successfully",
  type = "success"
))

# Progress update
post_message(session, "progress", list(
  percent = 75,
  message = "Processing..."
))

# Custom event
post_message(session, "dataUpdate", list(
  timestamp = Sys.time(),
  rows = nrow(updated_data)
))
```

## Rendering Patterns

### Reactive Data Processing

```r
server <- function(input, output, session) {
  # Reactive data source
  filtered_data <- reactive({
    mtcars %>%
      filter(cyl >= input$min_cyl) %>%
      filter(mpg >= input$min_mpg)
  })

  # Output uses reactive
  output$table <- render_json({
    filtered_data()
  })

  # Derived statistics
  output$summary <- render_json({
    df <- filtered_data()
    list(
      count = nrow(df),
      avg_mpg = mean(df$mpg),
      avg_hp = mean(df$hp)
    )
  })
}
```

### Multiple Related Outputs

```r
server <- function(input, output, session) {
  output$chart_data <- render_json({
    list(
      x = mtcars$wt,
      y = mtcars$mpg,
      labels = rownames(mtcars)
    )
  })

  output$chart_options <- render_json({
    list(
      title = input$chart_title,
      showLegend = input$show_legend,
      colorScheme = input$color_scheme
    )
  })
}
```

### Plots with renderPlot

Standard Shiny `renderPlot()` works with `ImageOutput` component:

```r
output$myplot <- renderPlot({
  ggplot(mtcars, aes(x = wt, y = mpg)) +
    geom_point(size = input$point_size) +
    theme_minimal()
})
```

React automatically sends plot dimensions via special inputs:
- `.clientdata_output_myplot_width`
- `.clientdata_output_myplot_height`

## Message Handling

### Periodic Updates

```r
server <- function(input, output, session) {
  observe({
    invalidateLater(5000)  # Every 5 seconds

    post_message(session, "heartbeat", list(
      time = Sys.time(),
      status = "connected"
    ))
  })
}
```

### Event-Driven Messages

```r
server <- function(input, output, session) {
  observeEvent(input$submit, {
    # Long computation
    result <- expensive_calculation()

    post_message(session, "complete", list(
      success = TRUE,
      message = "Calculation finished",
      result = result
    ))
  })
}
```

### Streaming Data

```r
server <- function(input, output, session) {
  observeEvent(input$start_stream, {
    for (i in 1:100) {
      post_message(session, "stream", list(
        progress = i,
        data = generate_chunk(i)
      ))
      Sys.sleep(0.1)
    }
    post_message(session, "stream", list(progress = 100, done = TRUE))
  })
}
```

## Complete Example

### app.R

```r
library(shiny)
library(dplyr)

source("shinyreact.R", local = TRUE)

server <- function(input, output, session) {
  # Filtered data reactive
  filtered <- reactive({
    mtcars %>%
      filter(cyl %in% input$cylinders) %>%
      filter(mpg >= input$min_mpg)
  })

  # Table output
  output$car_data <- render_json({
    filtered()
  })

  # Summary statistics
  output$summary <- render_json({
    df <- filtered()
    list(
      total = nrow(df),
      avg_mpg = round(mean(df$mpg), 1),
      avg_hp = round(mean(df$hp), 0)
    )
  })

  # Plot
  output$scatter <- renderPlot({
    ggplot(filtered(), aes(x = wt, y = mpg, color = factor(cyl))) +
      geom_point(size = 3) +
      theme_minimal() +
      labs(title = "Weight vs MPG", color = "Cylinders")
  })

  # Notify when filter changes significantly
  observeEvent(filtered(), {
    if (nrow(filtered()) < 5) {
      post_message(session, "warning", list(
        text = "Very few cars match your filters"
      ))
    }
  })
}

shinyApp(
  ui = page_react(title = "Car Explorer"),
  server = server
)
```

## Running the App

### Development

```bash
# From app directory
R -e "options(shiny.autoreload = TRUE); shiny::runApp('r/app.R', port = 8000)"
```

### With npm scripts (recommended)

```json
{
  "scripts": {
    "shinyapp-r": "Rscript -e \"options(shiny.autoreload = TRUE); shiny::runApp('r/app.R', port=${R_PORT:-8000})\""
  }
}
```

```bash
npm run shinyapp-r
# or
R_PORT=8001 npm run shinyapp-r
```
