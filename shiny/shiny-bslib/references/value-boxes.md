# Value Boxes in bslib

Value boxes are specialized card-like components designed for displaying key metrics, KPIs, and statistics in dashboards. They provide a focused, scannable way to communicate important numbers.

## Table of Contents

- [Core Components](#core-components)
- [Basic Usage](#basic-usage)
- [Showcase Options](#showcase-options)
- [Theming](#theming)
- [Dashboard Layouts](#dashboard-layouts)
- [Dynamic Rendering in Shiny](#dynamic-rendering-in-shiny)
- [Expandable Sparklines](#expandable-sparklines)
- [Best Practices](#best-practices)

## Core Components

A `value_box()` has five main parts:

1. **`title`** — descriptive label (e.g., "Total Users", "Revenue", "Growth Rate")
2. **`value`** — the primary metric displayed prominently (e.g., "1,234", "$56K", "+12%")
3. **`showcase`** — optional icon or plot displayed alongside the value
4. **`theme`** — optional appearance customization
5. **`...`** (additional arguments) — extra text/UI elements rendered below the value

## Basic Usage

**Simple value box:**
```r
value_box(
  title = "Total Users",
  value = "1,234"
)
```

**With additional context:**
```r
value_box(
  title = "Monthly Revenue",
  value = "$56,789",
  "Up 12% from last month"
)
```

**Multiple value boxes in a layout:**
```r
layout_column_wrap(
  width = 1/3,
  value_box(title = "Users", value = "1,234", theme = "primary"),
  value_box(title = "Sessions", value = "5,678", theme = "info"),
  value_box(title = "Conversion", value = "4.5%", theme = "success")
)
```

## Showcase Options

The `showcase` parameter accepts icons or small plots. Three layout functions control positioning:

### Showcase Layouts

Pass `showcase_layout` one of three options: `showcase_left_center()` (default), `showcase_top_right()`, or `showcase_bottom()`. String shorthands `"left center"`, `"top right"`, and `"bottom"` also work. Each function accepts optional `width` and `max_height` parameters for fine-grained control over the showcase area dimensions.

```r
value_box(
  title = "New Users",
  value = "487",
  showcase = bsicons::bs_icon("person-plus"),
  showcase_layout = showcase_left_center()
)
```

### Icons

Use `bsicons::bs_icon()` (designed for Bootstrap) or `fontawesome::fa()` as the `showcase` value. Common dashboard icons:

- Users: `bs_icon("people")`, `bs_icon("person")`
- Money: `bs_icon("currency-dollar")`, `bs_icon("cash")`
- Trends: `bs_icon("graph-up")`, `bs_icon("graph-down")`, `bs_icon("arrow-up")`
- Status: `bs_icon("check-circle")`, `bs_icon("x-circle")`, `bs_icon("exclamation-triangle")`
- Activity: `bs_icon("activity")`, `bs_icon("clock")`, `bs_icon("calendar")`

### Plots as Showcase

Small sparkline plots work well in the showcase:

```r
library(sparkline)

value_box(
  title = "Daily Users",
  value = "1,234",
  showcase = sparkline::sparkline(daily_users_vector),
  showcase_layout = "left center"
)
```

See [Expandable Sparklines](#expandable-sparklines) for advanced patterns.

## Theming

The `theme` argument accepts a string class name or `value_box_theme()` for custom colors.

**Background themes** set a solid colored background. Strings without a `bg-` or `text-` prefix get `bg-` prepended automatically, so `"success"` and `"bg-success"` are equivalent. Semantic options: `"primary"`, `"secondary"`, `"success"`, `"danger"`, `"warning"`, `"info"`. Named color options: `"blue"`, `"indigo"`, `"purple"`, `"pink"`, `"red"`, `"orange"`, `"yellow"`, `"green"`, `"teal"`, `"cyan"`.

**Foreground themes** (`text-*`) use a white/light background with colored text — less visually dominant than solid backgrounds. Examples: `"text-success"`, `"text-primary"`, `"text-purple"`, `"text-danger"`.

**Gradient themes** use Bootstrap 5's named colors. Every non-identical pair is available as `"bg-gradient-{from}-{to}"`, e.g. `"bg-gradient-blue-purple"`, `"bg-gradient-orange-red"`, `"bg-gradient-teal-cyan"`. Gradient themes require Bootstrap 5 and are not available with Bootstrap 3/4 themes.

**Custom theme** with `value_box_theme()`:

```r
theme = value_box_theme(bg = "#1f77b4", fg = "#ffffff")
```

Omit `fg` to auto-compute a contrasting foreground color.

**Interactive builder:** Visit bslib.shinyapps.io/build-a-box to explore all theme options and copy generated code.

## Dashboard Layouts

### With layout_column_wrap()

**Fixed columns:**
```r
layout_column_wrap(
  width = 1/4,  # 4 columns
  value_box(title = "Metric 1", value = "1,234"),
  value_box(title = "Metric 2", value = "5,678"),
  value_box(title = "Metric 3", value = "9,012"),
  value_box(title = "Metric 4", value = "3,456")
)
```

**Responsive columns:**
```r
layout_column_wrap(
  width = "250px",  # Auto-wraps based on screen size
  value_box(title = "Users", value = "1,234"),
  value_box(title = "Revenue", value = "$56K"),
  value_box(title = "Growth", value = "+12%")
)
```

### With layout_columns()

**Custom proportions:**
```r
layout_columns(
  col_widths = c(6, 3, 3),
  card(
    card_header("Main Content"),
    plotOutput("main_plot")
  ),
  value_box(title = "KPI 1", value = "123"),
  value_box(title = "KPI 2", value = "456")
)
```

### In Filling Layouts

When embedding value boxes within a larger filling layout, set `fill = FALSE` on the layout container to prevent boxes from consuming excess vertical space:

```r
page_fillable(
  # Value boxes at top - don't fill
  layout_column_wrap(
    width = 1/3,
    fill = FALSE,  # Important!
    value_box(title = "Users", value = "1,234"),
    value_box(title = "Sessions", value = "5,678"),
    value_box(title = "Revenue", value = "$90K")
  ),
  # Main content fills remaining space
  card(
    card_header("Detailed Analysis"),
    plotlyOutput("analysis")
  )
)
```

This allows the card below to fill the remaining vertical space.

## Dynamic Rendering in Shiny

**Best practice:** Wrap dynamic content in `textOutput()` as a placeholder to reduce layout shift:

**Good:**
```r
# UI
value_box(
  title = "Active Users",
  value = textOutput("user_count"),
  showcase = bs_icon("people")
)

# Server
output$user_count <- renderText({
  # Calculate value
  nrow(filtered_data())
})
```

**With additional dynamic content:**
```r
# UI
value_box(
  title = "Revenue",
  value = textOutput("revenue_value"),
  textOutput("revenue_change"),
  showcase = bs_icon("currency-dollar"),
  theme = "success"
)

# Server
output$revenue_value <- renderText({
  paste0("$", format(sum(data$revenue), big.mark = ","))
})

output$revenue_change <- renderText({
  change <- calculate_change()
  paste0(ifelse(change > 0, "+", ""), round(change * 100, 1), "% vs last month")
})
```

## Expandable Sparklines

Since `value_box()` is implemented using `card()`, it inherits `full_screen` capabilities. This is particularly useful for sparklines:

**Basic expandable sparkline:**
```r
value_box(
  title = "Daily Traffic",
  value = textOutput("current_traffic"),
  showcase = plotOutput("traffic_sparkline", height = "100%"),
  showcase_layout = "left center",
  full_screen = TRUE
)
```

### Responsive Sparkline Rendering

**With Shiny - different plots for different sizes:**
```r
# Server
output$traffic_sparkline <- renderPlot({
  info <- getCurrentOutputInfo()

  if (info$height() > 200) {
    # Expanded view: full chart with axes and labels
    ggplot(traffic_data, aes(date, visits)) +
      geom_line(color = "steelblue", linewidth = 1) +
      geom_area(fill = "steelblue", alpha = 0.2) +
      labs(x = "Date", y = "Visits", title = "Traffic Over Time") +
      theme_minimal()
  } else {
    # Compact view: minimal sparkline
    ggplot(traffic_data, aes(date, visits)) +
      geom_line(color = "steelblue") +
      theme_void()
  }
})
```

**Without Shiny - JavaScript approach:**
```r
library(htmlwidgets)

sparkline_widget <- htmlwidgets::createWidget(...)

sparkline_widget |>
  htmlwidgets::onRender(
    "function(el) {
      el.closest('.bslib-value-box')
        .addEventListener('bslib.card', function(ev) {
          if (ev.detail.fullScreen) {
            // modify plot for full screen appearance
          } else {
            // trim plot for small style in value box
          }
        })
    }"
  )
```

## Best Practices

### Keep Values Concise

Value boxes work best with short, scannable values:

**Good:**
- "1.2K", "$56K", "+18%", "98.5%"

**Avoid:**
- "1,234 active users in the last 30 days"
- Very long numbers without abbreviation

### Use Appropriate Number Formatting

```r
# In server
output$revenue <- renderText({
  scales::dollar(sum(data$revenue), scale = 1e-3, suffix = "K")
})

output$users <- renderText({
  scales::comma(nrow(users_data))
})

output$rate <- renderText({
  scales::percent(success_rate, accuracy = 1)
})
```

### Choose Meaningful Themes

Match theme to context:
- `"success"` for positive metrics (growth, success rate)
- `"danger"` for alerts or problems
- `"warning"` for cautionary metrics
- `"primary"` for neutral key metrics
- `"info"` for informational metrics

### Group Related Metrics

Use `layout_column_wrap()` to group related value boxes:

```r
layout_column_wrap(
  width = 1/3,
  value_box(title = "New Users", value = "487", theme = "primary"),
  value_box(title = "Returning Users", value = "1,234", theme = "info"),
  value_box(title = "Total Sessions", value = "5,678", theme = "secondary")
)
```

### Position Value Boxes Appropriately

**Top of dashboard:** Most common placement for KPIs
```r
page_sidebar(
  title = "Dashboard",
  sidebar = sidebar(...),
  # Value boxes at top
  layout_column_wrap(width = 1/4, fill = FALSE, ...),
  # Detailed content below
  card(...)
)
```

**Within sections:** Group with related content
```r
card(
  card_header("Sales Performance"),
  layout_column_wrap(
    width = 1/3,
    value_box(title = "Revenue", value = "$125K"),
    value_box(title = "Orders", value = "487"),
    value_box(title = "AOV", value = "$256")
  ),
  plotOutput("sales_trend")
)
```

### Use Showcase Strategically

**Icons:** Use for quick visual identification
**Sparklines:** Use when trends matter as much as current values
**No showcase:** Valid choice for clean, minimal design

### Test Responsive Behavior

Always check how value boxes look at different screen widths:
- Desktop (4+ columns)
- Tablet (2-3 columns)
- Mobile (1 column)

### Consider Accessibility

- Use clear, descriptive titles
- Ensure sufficient color contrast (handled automatically by themes)
- Don't rely solely on color to convey meaning
- Test with screen readers if building public-facing apps
