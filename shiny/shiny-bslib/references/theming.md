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

```r
page_sidebar(
  theme = bs_theme(
    version = 5,
    preset = "flatly"
  ),
  ...
)
```

## Preset Themes

Pre-packaged professional themes. List all with `bootswatch_themes()`. The `bootswatch` argument is an alias for `preset`.

Popular options: `"flatly"`, `"minty"`, `"cosmo"`, `"litera"`, `"darkly"`, `"cyborg"`, `"simplex"`, `"zephyr"`.

```r
page_navbar(
  title = "My App",
  theme = bs_theme(preset = "flatly"),
  ...
)
```

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

Three font arguments: `base_font`, `heading_font`, `code_font`.

**Google Fonts (most common):**
```r
bs_theme(
  base_font = font_google("Roboto"),
  heading_font = font_google("Montserrat"),
  code_font = font_google("Fira Code")
)
```

Also available: `font_link()` (custom URL), `font_face()` (local files), `font_collection()` (fallback stacks).

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
