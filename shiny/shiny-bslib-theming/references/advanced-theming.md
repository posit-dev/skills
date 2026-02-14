# Advanced Theming

Dynamic theme switching, dark mode, and component compatibility details.

## Table of Contents

- [Dynamic Theme Switching](#dynamic-theme-switching)
- [Dark Mode](#dark-mode)
- [Component Compatibility](#component-compatibility)
- [Performance](#performance)

## Dynamic Theme Switching

Use `session$setCurrentTheme()` to change themes at runtime:

```r
ui <- page_sidebar(
  title = "Dynamic Theming",
  sidebar = sidebar(
    input_dark_mode(id = "dark_mode")
  ),
  ...
)

server <- function(input, output, session) {
  light_theme <- bs_theme(bg = "#FFFFFF", fg = "#212529", primary = "#007bff")
  dark_theme <- bs_theme(bg = "#1a1a1a", fg = "#f8f9fa", primary = "#375a7f")

  observe({
    if (input$dark_mode) {
      session$setCurrentTheme(dark_theme)
    } else {
      session$setCurrentTheme(light_theme)
    }
  })
}
```

### input_dark_mode()

Convenient dark mode toggle widget:

```r
# UI
sidebar(
  input_dark_mode(id = "mode", mode = "light")
)

# Access state
input$mode  # "light" or "dark"
```

## Dark Mode

When offering dark mode, ensure custom Sass rules work in both themes by using Sass variables instead of hardcoded colors:

```r
# Both themes share the same custom rules via Sass variables
custom_rules <- "
  .custom-card {
    background: mix($bg, $primary, 95%);
    border: 1px solid $primary;
  }
"

light_theme <- bs_theme(bg = "#FFFFFF", fg = "#212529", primary = "#007bff") |>
  bs_add_rules(custom_rules)

dark_theme <- bs_theme(bg = "#1a1a1a", fg = "#f8f9fa", primary = "#375a7f") |>
  bs_add_rules(custom_rules)
```

Using `$bg`, `$primary`, etc. ensures styles adapt automatically to each theme.

## Component Compatibility

### Themeable

**Core Shiny UI:** All inputs, buttons, tables, text, links.

**bslib components:** Cards, value boxes, navs/navsets, sidebars, accordions, tooltips, popovers, toasts.

**HTML widgets (partial):**
- `DT::datatable()` -- via CSS
- `plotly` -- partially via `ggplotly()` + thematic
- Others vary

**R Markdown:** `html_document()`, `flexdashboard`, unstyled HTML.

### Not Themeable

- `renderPlot()` without the `thematic` package
- HTML widgets with baked-in styles
- External iframes
- Custom HTML with hardcoded inline styles

## Performance

Heavy theming with many custom rules can impact load time:

- Minimize custom Sass/CSS
- Pre-compile Sass when possible (`sass::sass()` to a CSS file)
- Use browser dev tools to profile CSS load time
- Consider caching strategies for production
