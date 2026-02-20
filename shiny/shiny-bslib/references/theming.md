# Theming in bslib

Basic theming for Shiny apps using `bs_theme()`. For comprehensive theming (Sass variables, custom rules, dark mode, dynamic theming), see the **shiny-bslib-theming** skill.

## Table of Contents

- [Quick Start](#quick-start)
- [Preset Themes](#preset-themes)
- [Main Colors](#main-colors)
- [Typography](#typography)
- [Brand YAML](#brand-yaml)
- [Theming R Plots](#theming-r-plots)

## Quick Start

`bs_theme(version = 5)` uses `preset = "shiny"` by default — a polished theme designed to look good for most Shiny apps. Start here, especially when modernizing a stock Shiny app:

```r
page_sidebar(
  theme = bs_theme(version = 5),  # "shiny" preset by default
  ...
)
```

## Preset Themes

### The "shiny" preset (default)

`bs_theme(version = 5)` defaults to `preset = "shiny"`, which is specifically designed for Shiny apps and looks professional without any extra configuration. Recommend this as the starting point.

### Bootswatch presets

For a different visual style, use a Bootswatch preset via `bs_theme(version = 5, preset = "<name>")`. Popular options include `"minty"` (soft green), `"cosmo"` (clean and modern), `"darkly"` (dark background), and `"zephyr"` (light, airy). List all options with `bootswatch_themes()`. Choose one that fits the app's purpose and audience — don't apply one by default.

The `bootswatch` argument is an alias for `preset`.

## Main Colors

The most influential color parameters — changing these affects hundreds of CSS rules:

| Parameter | Description |
|---|---|
| `bg` | Background color |
| `fg` | Foreground (text) color |
| `primary` | Primary brand color (links, nav active, input focus) |
| `secondary` | Default for action buttons |
| `success` | Positive/success states |
| `info` | Informational content |
| `warning` | Warnings |
| `danger` | Errors/destructive actions |

```r
bs_theme(
  bg = "#FFFFFF",
  fg = "#212529",
  primary = "#2c3e50",
  success = "#27ae60",
  danger = "#e74c3c"
)
```

**Tips:**
- `bg`/`fg`: similar hue, large luminance difference
- `primary`: should contrast well with both `bg` and `fg`

## Typography

Three font arguments: `base_font`, `heading_font`, `code_font`. Each accepts `font_google("Name")` (most common), `font_link()` (custom URL), `font_face()` (local files), or `font_collection()` (fallback stacks).

## Brand YAML

bslib auto-discovers `_brand.yml` in your app directory. No code changes needed.

```r
bs_theme(brand = FALSE)  # Disable auto-discovery
```

Requires the `brand.yml` R package. See the **brand-yml** skill for creating `_brand.yml` files.

## Theming R Plots

`bs_theme()` only affects CSS. Use the `thematic` package to auto-match R plots:

```r
library(thematic)
thematic_shiny(font = "auto")  # Call before shinyApp()
shinyApp(ui, server)
```

Works with base R, ggplot2, and lattice.
