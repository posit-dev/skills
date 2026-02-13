# Cards in bslib

Cards are the primary container component in modern bslib dashboards. They group related content with borders and padding, helping users digest, engage with, and navigate through information.

## Table of Contents

- [Core Concept](#core-concept)
- [Card Structure](#card-structure)
- [Card Components](#card-components)
- [Height Control & Scrolling](#height-control--scrolling)
- [Full-Screen Expansion](#full-screen-expansion)
- [Filling Outputs](#filling-outputs)
- [Multiple card_body() Sections](#multiple-card_body-sections)
- [Multi-Column Layouts Within Cards](#multi-column-layouts-within-cards)
- [Tabbed Cards](#tabbed-cards)
- [Sidebar Integration](#sidebar-integration)
- [Static Images](#static-images)
- [Flexbox Behavior](#flexbox-behavior)
- [Shiny-Specific Features](#shiny-specific-features)
- [Best Practices](#best-practices)

## Core Concept

At their core, cards are "just an HTML `div()` with a special Bootstrap class." They serve as rectangular containers that visually group related information.

**Basic card:**
```r
card(
  card_header("My Card"),
  "Card content goes here"
)
```

## Card Structure

The `card()` function accepts "known" card items as unnamed arguments (children):

- **`card_header()`** — top section, supports Bootstrap utility classes
- **`card_body()`** — main content area (often implicit)
- **`card_footer()`** — bottom section
- **`card_image()`** — for embedding static images
- **`card_title()`** — styled title element

### Implicit card_body()

Direct children of `card()` that aren't recognized card items automatically get wrapped in `card_body()`. These are equivalent:

```r
# Explicit
card(
  card_header("Title"),
  card_body("Content")
)

# Implicit (recommended for simple cases)
card(
  card_header("Title"),
  "Content"  # Automatically wrapped in card_body()
)
```

## Card Components

### card_header()

Top section of the card, useful for titles and controls.

**Basic usage:**
```r
card(
  card_header("Sales Dashboard"),
  plotOutput("sales_plot")
)
```

**With styling:**
```r
card(
  card_header(
    class = "bg-primary text-white",
    "Featured Analysis"
  ),
  ...
)
```

**With icons or buttons:**
```r
card(
  card_header(
    tags$span("Settings", tooltip(bsicons::bs_icon("info-circle"), "Configure options"))
  ),
  ...
)
```

### card_body()

Main content area. Usually implicit, but useful for:
- Adding multiple body sections
- Controlling padding and styling
- Setting min/max heights for filling behavior

**Example with custom styling:**
```r
card(
  card_header("Data"),
  card_body(
    class = "p-0",  # Remove padding
    plotlyOutput("plot")
  )
)
```

### card_footer()

Bottom section for metadata, actions, or links.

**Example:**
```r
card(
  card_header("Analysis Results"),
  plotOutput("results"),
  card_footer(
    class = "text-muted",
    "Last updated: ", textOutput("last_update", inline = TRUE)
  )
)
```

### card_title()

Styled title element that can be used within card_body() or card_header().

**Example:**
```r
card(
  card_body(
    card_title("Section Title"),
    p("Content goes here")
  )
)
```

## Height Control & Scrolling

Cards grow by default to fit their contents. Control sizing with named arguments:

**Fixed height:**
```r
card(
  height = 400,
  card_header("Fixed Height Card"),
  lorem::ipsum(paragraphs = 10)  # Will scroll if content exceeds height
)
```

**Maximum height:**
```r
card(
  max_height = 250,
  card_header("Scrollable Card"),
  verbatimTextOutput("long_output")
)
```

**Minimum height:**
```r
card(
  min_height = 300,
  card_header("Flexible Card"),
  plotOutput("plot")  # Won't shrink below 300px
)
```

When content exceeds the card's height, scrolling is automatically enabled.

## Full-Screen Expansion

Add `full_screen = TRUE` to enable an expand icon that shows the card in full browser window size:

**Basic usage:**
```r
card(
  full_screen = TRUE,
  card_header("Expandable Plot"),
  plotlyOutput("plot")
)
```

**Best practice:** Enable full-screen for all cards containing plots, maps, or detailed tables. This is highly valued by users.

**Important:** When expanded to full-screen, `max_height` and `height` constraints are ignored, allowing content to use the full viewport.

**Example with scrolling and full-screen:**
```r
card(
  max_height = 250,
  full_screen = TRUE,
  card_header("Analysis Details"),
  lorem::ipsum(paragraphs = 10)
)
```

## Filling Outputs

Cards are optimized for filling layouts. When a **fill item** (like plotly, leaflet, or most htmlwidgets) is a direct child of `card_body()`, it resizes to match the card's specified height.

**Example:**
```r
card(
  height = 400,
  full_screen = TRUE,
  card_header("Interactive Map"),
  card_body(
    class = "p-0",  # Remove padding for edge-to-edge display
    leafletOutput("map")
  )
)
```

**Fill items by default:**
- Most htmlwidgets (plotly, leaflet, DT, etc.)
- `plotOutput()`
- `imageOutput()`

**Preventing excessive shrinking:**
```r
card_body(
  min_height = 250,
  plotlyOutput("plot1"),
  plotlyOutput("plot2")
)
```

## Multiple card_body() Sections

A single card can contain several `card_body()` elements, useful for combining resizable and fixed-size content.

**Example:**
```r
card(
  full_screen = TRUE,
  card_header("Sales Analysis"),
  # Subtitle section - won't fill or scroll
  card_body(
    fill = FALSE,
    gap = 0,
    card_title("Q4 Results"),
    p(class = "text-muted", "Preliminary data as of Dec 31")
  ),
  # Plot section - fills available space
  card_body(
    min_height = 300,
    plotlyOutput("sales_plot")
  ),
  # Summary section - fixed size
  card_body(
    fill = FALSE,
    verbatimTextOutput("summary_stats")
  )
)
```

**Key insight:** Set `fill = FALSE` on body sections that should maintain their natural size and not participate in filling behavior.

## Multi-Column Layouts Within Cards

Use `layout_column_wrap()` for responsive multi-column arrangements inside cards:

**Example:**
```r
card(
  card_header("Quarterly Metrics"),
  card_body(
    min_height = 200,
    layout_column_wrap(
      width = 1/2,
      plotOutput("q1"),
      plotOutput("q2"),
      plotOutput("q3"),
      plotOutput("q4")
    )
  )
)
```

## Tabbed Cards

Use `navset_card_tab()`, `navset_card_pill()`, or `navset_card_underline()` to create multi-tab cards:

**Example:**
```r
navset_card_underline(
  title = "Analysis",
  full_screen = TRUE,
  nav_panel("Plot", plotOutput("plot")),
  nav_panel("Summary", verbatimTextOutput("summary")),
  nav_panel("Data", tableOutput("data"))
)
```

**Key features:**
- The `title` argument adds a card header
- Full-screen support works with tabbed cards
- Each `nav_panel()` behaves like a card — non-card children get implicitly wrapped in `card_body()`

See [navigation.md](navigation.md) for more details on navset functions.

## Sidebar Integration

`layout_sidebar()` works inside cards to create component-level sidebars:

**Example:**
```r
card(
  full_screen = TRUE,
  card_header("Customizable Plot"),
  layout_sidebar(
    fillable = TRUE,  # Preserve fill behavior
    sidebar = sidebar(
      title = "Plot Options",
      position = "right",
      selectInput("color", "Color scheme", ...),
      sliderInput("bins", "Bins", ...)
    ),
    plotlyOutput("plot")
  )
)
```

**Important:** Set `fillable = TRUE` on `layout_sidebar()` to preserve fill behavior for outputs.

See [sidebars.md](sidebars.md) for more sidebar patterns.

## Static Images

`card_image()` embeds pre-generated images:

**Example:**
```r
card(
  card_header("Project Logo"),
  card_image(
    file = "path/to/image.png",
    alt = "Project logo",
    href = "https://project-website.com"  # Makes image clickable
  ),
  card_body("Project description...")
)
```

**Parameters:**
- `file`: Path to image file
- `alt`: Alt text for accessibility
- `href`: Optional URL to make image a clickable link
- `border_radius`: Control corner rounding

## Flexbox Behavior

Both `card()` and `card_body()` default to `fillable = TRUE`, making them CSS flexbox containers. This enables fill behavior but changes how inline elements render.

**Side effect:** Inline tags (like `span()`, `a()`) appear on separate lines in flexbox containers.

**Solution for inline content:**
Set `fillable = FALSE` to restore normal inline flow:

```r
card(
  card_body(
    fillable = FALSE,
    "Text with ", tags$a("inline link", href = "#"), " and more text."
  )
)
```

### Flexbox Utilities

Use Bootstrap flex utility classes for precise control:

**Horizontal spacing:**
```r
card_header(
  class = "d-flex justify-content-between",
  tags$span("Title"),
  actionButton("refresh", "Refresh")
)
```

**Vertical alignment:**
```r
card_body(
  class = "d-flex align-items-center",
  ...
)
```

**Gap control:**
```r
card_body(
  gap = 10,  # Gap between children in pixels
  ...
)
```

## Shiny-Specific Features

### Dynamic Content Based on Card Size

Use `shiny::getCurrentOutputInfo()` to render different content based on whether the card is expanded:

**Example:**
```r
output$plot <- renderPlot({
  info <- getCurrentOutputInfo()

  if (info$height() > 500) {
    # Full plot with labels when expanded
    ggplot(data, aes(x, y)) +
      geom_point() +
      labs(title = "Detailed Analysis", subtitle = "With annotations")
  } else {
    # Simplified plot in normal view
    ggplot(data, aes(x, y)) + geom_point()
  }
})
```

This is particularly useful with `full_screen = TRUE` to show additional detail when the card is expanded.

## Best Practices

### Always Use Full-Screen for Visualizations

Enable `full_screen = TRUE` on cards containing:
- Plots (ggplot2, base R plots, plotly)
- Maps (leaflet, other mapping libraries)
- Tables with many rows
- Any content that benefits from more space

```r
card(
  full_screen = TRUE,  # Always include for viz cards
  card_header("Key Metrics"),
  plotOutput("metrics_plot")
)
```

### Use Appropriate Heights

- Set `min_height` to prevent cards from becoming too small in filling layouts
- Set `max_height` on cards with potentially long scrollable content
- Set fixed `height` sparingly — usually `min_height` is more flexible

### Remove Padding for Edge-to-Edge Content

Use `class = "p-0"` on `card_body()` for maps and certain visualizations:

```r
card_body(
  class = "p-0",
  leafletOutput("map")
)
```

### Organize Related Content

Use multiple `card_body()` sections to separate concerns:

```r
card(
  card_header("Analysis"),
  card_body(fill = FALSE, "Introduction and context..."),
  card_body(plotOutput("main_plot")),
  card_body(fill = FALSE, "Key findings and conclusions...")
)
```

### Leverage Tabbed Cards

When a card would contain multiple related outputs, use `navset_card_*()`:

```r
navset_card_underline(
  title = "Sales Data",
  full_screen = TRUE,
  nav_panel("Overview", plotOutput("overview")),
  nav_panel("By Region", plotOutput("by_region")),
  nav_panel("By Product", plotOutput("by_product")),
  nav_panel("Raw Data", tableOutput("raw_data"))
)
```

### Test Filling Behavior

Always test your cards in:
- Different viewport sizes
- Full-screen mode
- With varying amounts of content
- On mobile devices (or use browser dev tools)
