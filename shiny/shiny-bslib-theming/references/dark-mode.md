# Dark Mode and Color Modes

Bootstrap 5.3 introduced client-side color modes that switch CSS custom properties without Sass recompilation. bslib integrates this via `input_dark_mode()` and `toggle_dark_mode()`.

## Table of Contents

- [How Bootstrap Color Modes Work](#how-bootstrap-color-modes-work)
- [input_dark_mode()](#input_dark_mode)
- [toggle_dark_mode()](#toggle_dark_mode)
- [Server-Side Theme Switching](#server-side-theme-switching)
- [Client-Side vs Server-Side](#client-side-vs-server-side)
- [Custom Styles Across Modes](#custom-styles-across-modes)
- [Component Compatibility](#component-compatibility)
- [Performance](#performance)

## How Bootstrap Color Modes Work

Bootstrap 5.3 uses the `data-bs-theme` attribute on HTML elements to switch color modes. When toggled, Bootstrap overrides a set of CSS custom properties (`--bs-body-bg`, `--bs-body-color`, `--bs-emphasis-color`, etc.) without any Sass recompilation.

**Global mode** (set on `<html>`):
```html
<html data-bs-theme="light">  <!-- or "dark" -->
```

**Per-element override** (scoped to a component):
```r
# This card is always dark, regardless of global mode
tags$div(
  `data-bs-theme` = "dark",
  card(card_header("Settings"), "Always dark card")
)
```

**Default behavior:** If no `data-bs-theme` is set, Bootstrap respects the user's OS-level `prefers-color-scheme` preference.

## input_dark_mode()

A toggle button that switches between Bootstrap 5.3's light and dark color modes client-side.

```r
input_dark_mode(
  ...,           # Additional HTML attributes (class, style, etc.)
  id = NULL,     # Input ID to reactively read current mode
  mode = NULL    # Initial mode: NULL (follow OS), "light", or "dark"
)
```

**Basic usage:**
```r
# UI — place in navbar, sidebar, or anywhere
page_navbar(
  title = "My App",
  nav_spacer(),
  nav_item(input_dark_mode(id = "color_mode")),
  nav_panel("Dashboard", ...)
)

# Server — read current mode
output$mode_text <- renderText({
  paste("Current mode:", input$color_mode)  # "light" or "dark"
})
```

**How it works under the hood:**
1. User clicks the toggle
2. `input_dark_mode()` sets `data-bs-theme="dark"` (or `"light"`) on `<html>`
3. Bootstrap's pre-compiled CSS variable overrides take effect immediately
4. All Bootstrap components and utilities update their colors
5. If `id` is provided, the server receives `"light"` or `"dark"`

**No Sass recompilation happens** — this is purely a CSS variable switch, making it instantaneous.

## toggle_dark_mode()

Programmatically set or toggle the color mode from the server:

```r
toggle_dark_mode(
  mode = NULL,   # "light", "dark", or NULL to toggle
  session = get_current_session()
)
```

**Examples:**
```r
# Toggle between modes
observeEvent(input$toggle_btn, {
  toggle_dark_mode()
})

# Force a specific mode
observeEvent(input$force_light, {
  toggle_dark_mode("light")
})
```

## Server-Side Theme Switching

For more extensive theme changes beyond light/dark (different color palettes, fonts, etc.), use `session$setCurrentTheme()`:

```r
server <- function(input, output, session) {
  corporate_theme <- bs_theme(
    bg = "#FFFFFF", fg = "#212529",
    primary = "#003366",
    base_font = font_google("Open Sans")
  )

  playful_theme <- bs_theme(
    bg = "#FFF8E7", fg = "#333333",
    primary = "#FF6B35",
    base_font = font_google("Nunito")
  )

  observeEvent(input$theme_choice, {
    theme <- switch(input$theme_choice,
      "corporate" = corporate_theme,
      "playful" = playful_theme
    )
    session$setCurrentTheme(theme)
  })
}
```

This triggers a full Sass recompilation and CSS replacement via Shiny's connection.

## Client-Side vs Server-Side

| Aspect | `input_dark_mode()` / `toggle_dark_mode()` | `session$setCurrentTheme()` |
|---|---|---|
| **Mechanism** | Sets `data-bs-theme` attribute (CSS variable swap) | Full Sass recompilation + CSS replacement |
| **Speed** | Instantaneous | Noticeable delay |
| **Scope** | Light/dark mode only (same Sass, different CSS vars) | Any theme change (colors, fonts, variables) |
| **Custom Sass** | Only works if styles use CSS custom properties | Custom Sass is recompiled with new values |
| **3rd-party widgets** | Only if they use Bootstrap CSS variables | Only if they use `bs_dependency_defer()` |

**Recommendation:** Use `input_dark_mode()` for simple light/dark toggling (faster, no server round-trip). Use `session$setCurrentTheme()` when you need fundamentally different themes.

## Custom Styles Across Modes

### Using Sass Variables (recompiled themes)

When using `session$setCurrentTheme()`, Sass variables adapt automatically:

```r
custom_rules <- "
  .custom-card {
    background: mix($bg, $primary, 95%);
    border: 1px solid $primary;
  }
"
light_theme <- bs_theme(bg = "#FFFFFF", fg = "#212529") |> bs_add_rules(custom_rules)
dark_theme <- bs_theme(bg = "#1a1a1a", fg = "#f8f9fa") |> bs_add_rules(custom_rules)
```

### Using CSS Custom Properties (client-side color modes)

When using `input_dark_mode()` (no recompilation), custom CSS must reference CSS custom properties, not Sass variables:

```r
bs_theme() |>
  bs_add_rules("
    .custom-card {
      /* These update automatically when data-bs-theme changes */
      background: var(--bs-secondary-bg);
      color: var(--bs-body-color);
      border: 1px solid var(--bs-border-color);
    }
  ")
```

**Important:** Sass variables like `$bg` and `$primary` are resolved at compile time. They don't change when `data-bs-theme` toggles. Use `var(--bs-*)` properties for styles that should respond to client-side color mode changes.

### Mode-Specific Overrides

Target specific modes in custom CSS:

```r
bs_theme() |>
  bs_add_rules("
    [data-bs-theme='dark'] .custom-card {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }
    [data-bs-theme='light'] .custom-card {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  ")
```

## Component Compatibility

### Responds to bs_theme() and Color Modes

**Core Shiny UI:** All inputs, buttons, tables, text, links.

**bslib components:** Cards, value boxes, navs/navsets, sidebars, accordions, tooltips, popovers, toasts.

### Partially Compatible

- **`DT::datatable()`** -- Responds to color mode via CSS; filter controls adapt to dark mode (since bslib 0.6.0)
- **`plotly`** -- Partially via `ggplotly()` + thematic; may need explicit dark mode layout config
- **Other HTML widgets** -- Varies by widget

### Not Themeable

- **`renderPlot()`** without the `thematic` package (images are rendered server-side, unaffected by CSS)
- **HTML widgets with baked-in styles** (hardcoded CSS overrides Bootstrap)
- **External iframes**
- **Custom HTML with hardcoded inline styles**

### R Plots with Dark Mode

The `thematic` package responds to `session$setCurrentTheme()` but **not** to client-side `data-bs-theme` toggles. For apps using `input_dark_mode()`, you may need to re-render plots when the mode changes:

```r
output$plot <- renderPlot({
  # Re-render when color mode changes
  mode <- input$color_mode
  bg <- if (identical(mode, "dark")) "#212529" else "#ffffff"
  fg <- if (identical(mode, "dark")) "#dee2e6" else "#212529"

  ggplot(data, aes(x, y)) +
    geom_point(color = fg) +
    theme_minimal(base_size = 14) +
    theme(
      plot.background = element_rect(fill = bg, color = NA),
      panel.background = element_rect(fill = bg, color = NA),
      text = element_text(color = fg),
      axis.text = element_text(color = fg)
    )
})
```

## Performance

- **Client-side color modes** (`input_dark_mode()`) are instantaneous — just a CSS variable swap
- **Server-side theme switching** (`session$setCurrentTheme()`) triggers Sass recompilation, which can take a noticeable moment for complex themes
- Minimize custom Sass/CSS rules to reduce compilation time
- Pre-compile Sass when possible (`sass::sass()` to a CSS file)
- Consider caching strategies for production apps with multiple themes
