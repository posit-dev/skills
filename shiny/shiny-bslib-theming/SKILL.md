---
name: shiny-bslib-theming
description: Comprehensive theming for Shiny apps using bslib and Bootstrap 5. Use when customizing app appearance with bs_theme(), Bootswatch themes, custom colors, typography (font_google, font_face, font_link, font_collection), brand.yml integration, Bootstrap Sass variables, custom Sass/CSS rules (bs_add_rules), dark mode (input_dark_mode, session$setCurrentTheme), real-time theming (bs_themer), or making R plots match the app theme (thematic package). Covers everything from quick Bootswatch theming to advanced Sass customization and dynamic theme switching.
---

# Theming Shiny Apps with bslib

Customize Shiny app appearance using bslib's Bootstrap 5 theming system. From quick Bootswatch themes to advanced Sass customization and dynamic theme switching.

## Quick Start

**Bootswatch theme (fastest):**
```r
page_sidebar(
  theme = bs_theme(bootswatch = "flatly"),
  ...
)
```

**Custom colors and fonts:**
```r
page_sidebar(
  theme = bs_theme(
    version = 5,
    bg = "#FFFFFF",
    fg = "#333333",
    primary = "#2c3e50",
    base_font = font_google("Lato"),
    heading_font = font_google("Montserrat")
  ),
  ...
)
```

**Auto-brand from `_brand.yml`:**
If a `_brand.yml` file exists in your app directory, `bs_theme()` automatically applies its settings. No code changes needed. Requires the `brand.yml` R package. Disable with `bs_theme(brand = FALSE)`.

## Theming Workflow

1. Start with a Bootswatch theme close to your desired look
2. Customize main colors (`bg`, `fg`, `primary`)
3. Adjust fonts with `font_google()` or other font helpers
4. Fine-tune with Bootstrap Sass variables
5. Add custom Sass rules if needed
6. Enable `thematic::thematic_shiny()` so plots match the theme

**Example:**
```r
theme <- bs_theme(
  bootswatch = "minty"
) |>
  bs_theme_update(
    primary = "#1a9a7f",
    base_font = font_google("Lato")
  ) |>
  bs_add_rules("
    .card { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  ")
```

## Core Theming: bs_theme()

### Main Colors

The most influential colors — changing these affects **hundreds** of CSS rules:

- `bg`: Background color
- `fg`: Foreground (text) color
- `primary`: Primary brand color (links, nav active states, input focus)

Additional semantic colors: `secondary`, `success`, `info`, `warning`, `danger`.

```r
bs_theme(
  bg = "#FFFFFF",
  fg = "#212529",
  primary = "#2c3e50",
  secondary = "#95a5a6",
  success = "#27ae60",
  danger = "#e74c3c"
)
```

**Color selection tips:**
- `bg` and `fg` should have similar hue but large luminance difference
- `primary` should contrast well with both `bg` and `fg`
- `secondary` is the default color for action buttons

### Bootswatch Themes

Pre-packaged professional themes. List available themes with `bootswatch_themes()`.

Popular options: `"flatly"` (flat design), `"minty"` (fresh green), `"cosmo"` (modern), `"litera"` (crisp), `"darkly"` (dark), `"cyborg"` (dark), `"simplex"` (minimalist), `"zephyr"` (modern).

```r
page_navbar(
  title = "My App",
  theme = bs_theme(bootswatch = "flatly"),
  ...
)
```

### Typography

Three font arguments: `base_font`, `heading_font`, `code_font`.

#### font_google()

Downloads and caches Google Fonts locally. Internet needed only on first use.

```r
bs_theme(
  base_font = font_google("Roboto"),
  heading_font = font_google("Montserrat"),
  code_font = font_google("Fira Code")
)
```

With weights: `font_google("Raleway", wght = c(300, 400, 700))`

Font pairing resource: fontpair.co

#### font_link()

For custom font URLs:
```r
bs_theme(
  base_font = font_link("Custom Font", href = "https://fonts.example.com/font.css")
)
```

#### font_face()

For locally hosted font files:
```r
bs_theme(
  base_font = font_face(family = "Custom Font", src = "url('fonts/custom.woff2')")
)
```

#### font_collection()

Combine fonts with fallbacks:
```r
bs_theme(
  base_font = font_collection(font_google("Lato"), "Helvetica Neue", "Arial", "sans-serif")
)
```

## Bootstrap Sass Variables

Pass any Bootstrap Sass variable through `...` for fine-grained control:

```r
bs_theme(
  bg = "#002B36",
  fg = "#EEE8D5",
  "card-border-radius" = "1rem",
  "btn-border-radius" = "0.25rem"
)
```

Values can be Sass expressions:
```r
bs_theme(
  "progress-bar-bg" = "mix(white, orange, 20%)",
  "card-bg" = "lighten($bg, 5%)"
)
```

**Referencing existing Bootstrap variables** requires `bs_add_variables()` because variables aren't yet defined at `bs_theme()` time:
```r
bs_theme() |>
  bs_add_variables("progress-bar-bg" = "$secondary", .where = "declarations")
```

**Finding variable names:** Visit https://rstudio.github.io/bslib/articles/bs5-variables/ for a comprehensive list.

Common variables: `"border-radius"`, `"link-color"`, `"font-size-base"`, `"spacer"`, `"card-bg"`, `"navbar-bg"`, `"btn-padding-y"`, `"btn-padding-x"`.

## Custom Sass/CSS Rules

Use `bs_add_rules()` to add Sass/CSS that references Bootstrap variables and mixins:

```r
theme <- bs_theme(primary = "#007bff") |>
  bs_add_rules("
    .custom-card {
      background: mix($bg, $primary, 95%);
      border: 1px solid $primary;
      border-radius: $border-radius;
      padding: $spacer;
    }

    .my-component {
      @include media-breakpoint-up(md) {
        padding: $spacer * 2;
      }
    }
  ")
```

From external file: `bs_add_rules(sass::sass_file("custom.scss"))`

Available Sass functions: `lighten()`, `darken()`, `mix()`, `rgba()`, `color-contrast()`.
Available Bootstrap mixins: `@include media-breakpoint-up()`, `@include box-shadow()`, `@include border-radius()`.

## Theming R Plots

Since `bs_theme()` affects CSS only, R plot output (rendered server-side as images) won't auto-match. Use the `thematic` package:

```r
library(thematic)
thematic_shiny(font = "auto")  # Call before shinyApp()
shinyApp(ui, server)
```

Works with base R, ggplot2, and lattice. Auto-matches theme colors and fonts.

Set global ggplot2 theme for further consistency:
```r
library(ggplot2)
theme_set(theme_minimal())
```

## Dark Mode and Dynamic Theming

See [advanced-theming.md](references/advanced-theming.md) for:

- Runtime theme switching with `session$setCurrentTheme()`
- `input_dark_mode()` integration
- Ensuring custom Sass works across light/dark themes
- Component compatibility (what responds to theming, what doesn't)

## Real-Time Theming Tools

**`bs_themer()`** -- Interactive overlay for live experimentation during development:
```r
server <- function(input, output, session) {
  bs_themer()  # Add during development, remove for production
}
```

**`bs_theme_preview()`** -- Standalone demo app for exploring themes:
```r
bslib::bs_theme_preview()
```

## Best Practices

1. **Prefer `bs_theme()` over custom CSS** -- variables cascade to all related components automatically
2. **Pin Bootstrap version**: `bs_theme(version = 5)` prevents breakage if defaults change
3. **Test across components**: inputs, buttons, cards, navs, plots, tables, modals, toasts, mobile
4. **Check accessibility**: aim for WCAG AA (4.5:1 normal text, 3:1 large text). Use `bs_get_contrast(theme, "bg", "fg")`
5. **Use CSS utility classes** for one-off styling: `"bg-primary"`, `"text-muted"`, `"p-3"`, `"d-flex"`, `"fw-bold"`
6. **Organize theme code** in a separate `theme.R` for complex themes:

```r
# theme.R
app_theme <- function() {
  bs_theme(
    version = 5,
    bootswatch = "flatly",
    primary = "#2c3e50",
    base_font = font_google("Lato"),
    heading_font = font_google("Montserrat", wght = c(400, 700))
  ) |>
    bs_add_rules(sass::sass_file("www/custom.scss"))
}
```

## Reference Files

- **[advanced-theming.md](references/advanced-theming.md)** -- Dynamic theme switching, dark mode, component compatibility
