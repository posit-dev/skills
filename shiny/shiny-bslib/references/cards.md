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

Top section of the card, useful for titles and controls. The header is a flex container by default, so child elements are laid out horizontally. Use Bootstrap utility classes (e.g., `class = "bg-primary text-white"`) to style it, and the `gap` argument to control spacing between child elements.

**With icons or buttons (flex layout):**
```r
card(
  card_header(
    gap = "0.5rem",  # Space between header elements
    "Settings",
    tooltip(bsicons::bs_icon("info-circle"), "Configure options"),
    popover(bsicons::bs_icon("gear"), title = "Options", selectInput("opt", "Option", ...))
  ),
  ...
)
```

### card_body()

Main content area. Usually implicit, but useful for adding multiple body sections, controlling padding and styling, or setting min/max heights for filling behavior. Use `class = "p-0"` to remove padding for edge-to-edge content like maps.

### card_footer()

Bottom section for metadata, actions, or links.

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

Styled title element that can be used within `card_body()` or `card_header()`.

## Height Control & Scrolling

Cards grow by default to fit their contents. Control sizing with `height` (fixed), `min_height` (floor), and `max_height` (ceiling) arguments. When content exceeds the card's height, scrolling is automatically enabled.

- Use `min_height` to prevent cards from becoming too small in filling layouts.
- Use `max_height` on cards with potentially long scrollable content.
- Use fixed `height` sparingly — `min_height` is usually more flexible.

## Full-Screen Expansion

Add `full_screen = TRUE` to enable an expand icon that shows the card in full browser window size. Enable this for all cards containing plots, maps, or detailed tables — it is highly valued by users. When expanded, `max_height` and `height` constraints are ignored.

**Tracking full-screen state in Shiny:** Provide an `id` to the card to observe its full-screen state:
```r
card(
  id = "my_card",
  full_screen = TRUE,
  card_header("Plot"),
  plotOutput("plot")
)

# Server: input$my_card_full_screen is TRUE/FALSE
observe({
  if (isTRUE(input$my_card_full_screen)) {
    # Render higher-resolution plot when expanded
  }
})
```

**Combining with scrolling:** `max_height` and `full_screen = TRUE` work well together — the card scrolls at normal size and expands to show all content at full screen.

## Filling Outputs

Cards are optimized for filling layouts. When a **fill item** (like plotly, leaflet, or most htmlwidgets) is a direct child of `card_body()`, it resizes to match the card's specified height. Fill items by default include most htmlwidgets (plotly, leaflet, DT, etc.), `plotOutput()`, and `imageOutput()`.

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

Use `min_height` on `card_body()` to prevent excessive shrinking when multiple fill outputs share a body:

```r
card_body(
  min_height = 250,
  plotlyOutput("plot1"),
  plotlyOutput("plot2")
)
```

## Multiple card_body() Sections

A single card can contain several `card_body()` elements, useful for combining resizable and fixed-size content. Set `fill = FALSE` on body sections that should maintain their natural size and not participate in filling behavior.

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

## Multi-Column Layouts Within Cards

Use `layout_column_wrap()` for responsive multi-column arrangements inside cards:

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
- Each `nav_panel()` behaves like a card body — do **not** wrap panel content in `card()`; the navset already provides the card container

See [navigation.md](navigation.md) for more details on navset functions.

## Sidebar Integration

`layout_sidebar()` works inside cards to create component-level sidebars. Set `fillable = TRUE` on `layout_sidebar()` to preserve fill behavior for outputs.

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

See [sidebars.md](sidebars.md) for more sidebar patterns.

## Static Images

`card_image()` embeds pre-generated images. Key arguments: `file` (path to image), `alt` (accessibility text), `href` (optional URL to make the image a clickable link), and `border_radius` (corner rounding).

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

## Flexbox Behavior

Both `card()` and `card_body()` default to `fillable = TRUE`, making them CSS flexbox containers. This enables fill behavior but changes how inline elements render — inline tags like `span()` and `a()` appear on separate lines.

**Solution for inline content:** Set `fillable = FALSE` to restore normal inline flow:

```r
card(
  card_body(
    fillable = FALSE,
    "Text with ", tags$a("inline link", href = "#"), " and more text."
  )
)
```

### Flexbox Utilities

Use Bootstrap flex utility classes and the `gap` argument for precise layout control. For example, `class = "d-flex justify-content-between"` on `card_header()` spaces title and action elements to opposite ends, `class = "d-flex align-items-center"` on `card_body()` vertically centers content, and `gap = 10` sets pixel spacing between children.

## Shiny-Specific Features

### Dynamic Content Based on Card Size

Use `shiny::getCurrentOutputInfo()` to render different content based on whether the card is expanded:

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

### Use Appropriate Heights

- Set `min_height` to prevent cards from becoming too small in filling layouts
- Set `max_height` on cards with potentially long scrollable content
- Set fixed `height` sparingly — usually `min_height` is more flexible

### Remove Padding for Edge-to-Edge Content

Use `class = "p-0"` on `card_body()` for full-bleed maps and visualizations.

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
