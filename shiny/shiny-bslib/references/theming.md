# Theming in bslib

bslib provides powerful theming capabilities that allow you to customize the appearance of Shiny apps using Bootstrap 5 variables, Bootswatch themes, custom fonts, and dynamic theming. This reference covers comprehensive theming strategies.

## Table of Contents

- [Core Theming Function](#core-theming-function)
- [Bootswatch Themes](#bootswatch-themes)
- [Main Colors](#main-colors)
- [Typography](#typography)
- [Bootstrap Sass Variables](#bootstrap-sass-variables)
- [Real-Time Theming](#real-time-theming)
- [Custom Sass/CSS Rules](#custom-sasscss-rules)
- [Dynamic Theming](#dynamic-theming)
- [Theming R Plots](#theming-r-plots)
- [Component Compatibility](#component-compatibility)
- [Best Practices](#best-practices)

## Core Theming Function

### bs_theme()

The `bs_theme()` function is the central mechanism for customizing Bootstrap-based themes in Shiny apps and R Markdown documents.

**Basic usage:**
```r
page_sidebar(
  theme = bs_theme(
    version = 5,  # Bootstrap version
    bootswatch = "minty"  # Optional Bootswatch theme
  ),
  ...
)
```

**Key insight:** Changing only a few colors and fonts can impact **hundreds** of Bootstrap CSS rules due to variable cascading.

## Bootswatch Themes

Pre-packaged professional themes from Bootswatch provide instant polish.

**Available themes (Bootstrap 5):**
```r
bootswatch_themes()
```

Popular options include:
- `"cerulean"` - Calm blue
- `"cosmo"` - Flatly inspired
- `"cyborg"` - Dark theme
- `"darkly"` - Dark theme variant
- `"flatly"` - Flat design
- `"litera"` - Crisp and clean
- `"lumen"` - Light and friendly
- `"minty"` - Fresh green/mint
- `"pulse"` - Purple tones
- `"sandstone"` - Earthy tones
- `"simplex"` - Minimalist
- `"sketchy"` - Hand-drawn style
- `"slate"` - Dark with blue accents
- `"solar"` - Dark with yellow
- `"spacelab"` - Blue space theme
- `"superhero"` - Dark hero theme
- `"united"` - Orange accents
- `"yeti"` - Clean and modern
- `"zephyr"` - Modern and clean

**Example:**
```r
page_navbar(
  title = "My App",
  theme = bs_theme(bootswatch = "flatly"),
  ...
)
```

**Note:** Unlike the older `shinythemes` package (Bootstrap 3), bslib supports modern Bootstrap 5 Bootswatch themes.

## Main Colors

### Core Color Variables

**The most influential colors:**
- `bg`: Background color
- `fg`: Foreground (text) color
- `primary`: Primary brand color

These three variables affect **nearly every color on the page**.

**Example:**
```r
theme <- bs_theme(
  bg = "#FFFFFF",
  fg = "#333333",
  primary = "#007bff"
)
```

### Accent Colors

Additional semantic colors:
- `secondary`: Default for secondary actions
- `success`: For positive/success states
- `info`: For informational content
- `warning`: For warnings
- `danger`: For errors/destructive actions

**Example:**
```r
theme <- bs_theme(
  primary = "#2c3e50",
  secondary = "#95a5a6",
  success = "#27ae60",
  info = "#3498db",
  warning = "#f39c12",
  danger = "#e74c3c"
)
```

### Color Selection Guidelines

**bg and fg:**
- Pick colors with **similar hue** but **large difference in luminance**
- Ensure sufficient contrast for readability
- Light background = dark foreground, dark background = light foreground

**Good combinations:**
```r
# Light theme
bs_theme(bg = "#FFFFFF", fg = "#212529")

# Dark theme
bs_theme(bg = "#1a1a1a", fg = "#f8f9fa")

# Colored theme
bs_theme(bg = "#002B36", fg = "#EEE8D5")  # Solarized dark
```

**primary:**
- Used for hyperlinks, navigation active states, input focus colors
- Should contrast well with both bg and fg
- Consider brand colors

**secondary:**
- Default color for action buttons
- Should be visually distinct from primary

## Typography

### Font Variables

Three font arguments control typography:
- `base_font`: Body text font
- `heading_font`: Headings font
- `code_font`: Code/monospace font

**Best practice:** "Put serif fonts in `base_font`, sans-serif fonts in `heading_font`, and monospace fonts in `code_font`."

### Font Helpers

#### font_google()

Downloads and caches Google Fonts locally. Internet needed only on first use.

**Example:**
```r
theme <- bs_theme(
  base_font = font_google("Roboto"),
  heading_font = font_google("Montserrat"),
  code_font = font_google("Fira Code")
)
```

**With weights:**
```r
theme <- bs_theme(
  heading_font = font_google("Raleway", wght = c(300, 400, 700))
)
```

**Font pairing resource:** Visit fontpair.co for discovering harmonious Google Font combinations.

#### font_link()

Low-level CSS web font interface for custom font URLs:

**Example:**
```r
theme <- bs_theme(
  base_font = font_link(
    "Custom Font",
    href = "https://fonts.example.com/custom-font.css"
  )
)
```

#### font_face()

For locally hosted font files:

**Example:**
```r
theme <- bs_theme(
  base_font = font_face(
    family = "Custom Font",
    src = "url('fonts/custom-font.woff2')"
  )
)
```

#### font_collection()

Combine multiple fonts with fallbacks:

**Example:**
```r
theme <- bs_theme(
  base_font = font_collection(
    font_google("Lato"),
    "Helvetica Neue",
    "Arial",
    "sans-serif"
  )
)
```

## Bootstrap Sass Variables

### Advanced Customization

Pass any Bootstrap Sass variable through the `...` argument to customize specific aspects beyond the main parameters.

**Example:**
```r
theme <- bs_theme(
  bg = "#002B36",
  fg = "#EEE8D5",
  "progress-bar-bg" = "orange",
  "card-border-radius" = "1rem",
  "btn-border-radius" = "0.25rem"
)
```

**Values can be Sass expressions:**
```r
theme <- bs_theme(
  "progress-bar-bg" = "mix(white, orange, 20%)",
  "card-bg" = "lighten($bg, 5%)"
)
```

### How Variables Work

`bs_theme()` places Sass variable defaults **before** Bootstrap's variable defaults, enabling cascading.

**Example:**
```r
bs_theme(primary = "red")
```

This sets `$primary: red` before Bootstrap processes its files, affecting all variables that reference `$primary` (buttons, links, focus states, etc.).

### Referencing Bootstrap Variables

Direct references to Bootstrap variables (like `$secondary`) in `bs_theme()` will fail because those variables aren't yet defined.

**Workaround using bs_add_variables():**
```r
theme <- bs_theme() |>
  bs_add_variables(
    "progress-bar-bg" = "$secondary",
    .where = "declarations"
  )
```

The `.where = "declarations"` places the definition after Bootstrap's variables are available.

### Finding Variable Names

**Bootstrap 5 variables:**
- See [references/bs5-variables.md](bs5-variables.md) for comprehensive list
- Or visit https://rstudio.github.io/bslib/articles/bs5-variables/

**Common useful variables:**
- `"border-radius"` - Global border radius
- `"link-color"` - Hyperlink color
- `"font-size-base"` - Base font size
- `"spacer"` - Base spacing unit
- `"card-bg"` - Card background
- `"navbar-bg"` - Navbar background
- `"btn-padding-y"` / `"btn-padding-x"` - Button padding

## Real-Time Theming

### bs_themer()

Interactive widget that overlays on running Shiny apps for live experimentation.

**Usage:**
```r
ui <- page_sidebar(...)

server <- function(input, output, session) {
  bs_themer()  # Add this line

  # Rest of server logic
  ...
}

shinyApp(ui, server)
```

**Features:**
- Try different Bootswatch themes
- Adjust main colors
- Change fonts
- Modify variables
- See changes instantly
- Copy final theme code

**Best practice:** Use during development, remove before production deployment.

### bs_theme_preview()

Standalone demo app for exploring themes without a specific app:

```r
bslib::bs_theme_preview()
```

Opens an interactive app where you can experiment with all theming options and preview how they affect various UI components.

## Custom Sass/CSS Rules

### bs_add_rules()

Add custom Sass or CSS rules that can reference Bootstrap variables and mixins.

**Example:**
```r
theme <- bs_theme(
  bg = "#f8f9fa",
  primary = "#007bff"
) |>
  bs_add_rules("
    .custom-card {
      background: mix($bg, $primary, 95%);
      border: 1px solid $primary;
      border-radius: $border-radius;
      padding: $spacer;
    }

    .highlight {
      background: lighten($primary, 40%);
      color: $primary;
    }
  ")
```

**Benefits:**
- Reference Bootstrap Sass variables (like `$primary`, `$spacer`)
- Use Sass functions (like `mix()`, `lighten()`, `darken()`)
- Use Bootstrap mixins (like `@include media-breakpoint-up()`)
- Ensures styles are theme-aware

**With external file:**
```r
theme <- bs_theme() |>
  bs_add_rules(sass::sass_file("custom.scss"))
```

### Sass Functions and Mixins

**Available Sass functions:**
- `lighten($color, $amount)` - Lighten a color
- `darken($color, $amount)` - Darken a color
- `mix($color1, $color2, $weight)` - Mix two colors
- `rgba($color, $alpha)` - Add transparency
- `color-contrast($color)` - Get contrasting color

**Available Bootstrap mixins:**
- `@include media-breakpoint-up(md)` - Responsive breakpoints
- `@include box-shadow($shadow)` - Box shadows
- `@include border-radius($radius)` - Border radius

**Example:**
```r
theme <- bs_theme(primary = "#007bff") |>
  bs_add_rules("
    .my-component {
      background: lighten($primary, 45%);
      border: 1px solid $primary;

      @include media-breakpoint-up(md) {
        padding: $spacer * 2;
      }
    }
  ")
```

## Dynamic Theming

### Runtime Theme Switching

Use `session$setCurrentTheme()` to change themes dynamically (e.g., light/dark mode toggle):

**Example:**
```r
ui <- page_sidebar(
  title = "Dynamic Theming",
  sidebar = sidebar(
    input_dark_mode(id = "dark_mode")
  ),
  ...
)

server <- function(input, output, session) {
  # Define themes
  light_theme <- bs_theme(
    bg = "#FFFFFF",
    fg = "#212529",
    primary = "#007bff"
  )

  dark_theme <- bs_theme(
    bg = "#1a1a1a",
    fg = "#f8f9fa",
    primary = "#375a7f"
  )

  # Switch themes reactively
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

## Theming R Plots

### The thematic Package

Since `bs_theme()` operates on CSS, it can't directly affect `renderPlot()` (which generates images server-side). The `thematic` package solves this.

**Basic usage:**
```r
library(thematic)

# Call before running app
thematic_shiny()

shinyApp(ui, server)
```

**How it works:**
- Translates CSS colors into R plotting defaults
- Affects base R plots, ggplot2, and lattice
- Plots automatically match theme colors

**With auto fonts:**
```r
thematic_shiny(font = "auto")
```

This also matches fonts from `bs_theme()`.

**For real-time theming:**
```r
# Enable thematic
thematic_shiny(font = "auto")

# Use renderPlot for auto-theming
output$plot <- renderPlot({
  ggplot(data, aes(x, y)) + geom_point()
})
```

**Set global ggplot2 theme:**
```r
library(ggplot2)

# Use complete themes for consistent styling
theme_set(theme_minimal())

# Or customize
theme_update(
  plot.title = element_text(size = 16, face = "bold"),
  axis.title = element_text(size = 12)
)
```

## Component Compatibility

### Themeable Components

**Core Shiny UI:**
- All inputs (text, select, slider, checkbox, etc.)
- Buttons
- Tables
- Text (headings, paragraphs)
- Links

**bslib components:**
- Cards
- Value boxes
- Navs and navsets
- Sidebars
- Accordions
- Tooltips and popovers

**HTML widgets (select):**
- `DT::datatable()` - Via CSS
- `plotly` - Partially via `ggplotly()` + thematic
- Others vary

**R Markdown:**
- `rmarkdown::html_document()`
- `flexdashboard`
- Unstyled HTML content

### Non-Themeable Components

Some components don't respond to `bs_theme()`:
- `renderPlot()` without thematic package
- Some HTML widgets with baked-in styles
- External iframes
- Custom HTML with hardcoded styles

## Best Practices

### Use bs_theme() Over Custom CSS

**Prefer:**
```r
bs_theme(
  primary = "#2c3e50",
  "card-border-radius" = "0.5rem"
)
```

**Over:**
```css
/* custom.css */
.btn-primary { background: #2c3e50; }
.card { border-radius: 0.5rem; }
```

**Why:** `bs_theme()` affects all related variables and components automatically.

### Pin Bootstrap Version for Production

```r
theme <- bs_theme(
  version = 5,  # Pin to Bootstrap 5
  bootswatch = "flatly"
)
```

This prevents breakage if bslib's default version changes.

### Start with Bootswatch, Then Customize

**Good workflow:**
1. Start with a Bootswatch theme close to your desired look
2. Customize main colors
3. Adjust fonts
4. Fine-tune specific variables
5. Add custom rules if needed

**Example:**
```r
theme <- bs_theme(
  bootswatch = "minty"
) |>
  bs_theme_update(
    primary = "#1a9a7f",  # Adjust minty's primary
    base_font = font_google("Lato")
  ) |>
  bs_add_rules("
    .card { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  ")
```

### Test Accessibility

Ensure sufficient color contrast:

**Use contrast checking tools:**
- WebAIM Contrast Checker
- Browser dev tools
- `bslib::bs_get_contrast()` function

**Example:**
```r
theme <- bs_theme(bg = "#1a1a1a", fg = "#f0f0f0")

# Check if contrast is sufficient
bs_get_contrast(theme, "bg", "fg")
```

Aim for WCAG AA compliance (4.5:1 for normal text, 3:1 for large text).

### Use CSS Utility Classes

Complement theming with Bootstrap utility classes:

```r
card(
  card_header(class = "bg-primary text-white", "Header"),
  card_body(class = "p-4", "Content"),
  card_footer(class = "text-muted text-end", "Footer")
)
```

Common utilities:
- Colors: `"bg-primary"`, `"text-secondary"`, `"text-muted"`
- Spacing: `"p-3"`, `"m-4"`, `"px-2"`, `"mt-3"`
- Display: `"d-flex"`, `"d-none"`, `"d-md-block"`
- Text: `"text-center"`, `"fw-bold"`, `"fs-5"`

### Organize Theme Code

For complex themes, organize in a separate file:

**theme.R:**
```r
app_theme <- function() {
  bs_theme(
    version = 5,
    bootswatch = "flatly",
    primary = "#2c3e50",
    base_font = font_google("Lato"),
    heading_font = font_google("Montserrat", wght = c(400, 700)),
    code_font = font_google("Fira Code")
  ) |>
    bs_add_rules(sass::sass_file("www/custom.scss"))
}
```

**app.R:**
```r
source("theme.R")

ui <- page_navbar(
  theme = app_theme(),
  ...
)
```

### Document Theme Decisions

For team projects or handoff, document theme rationale:

```r
# Theme aligned with brand guidelines
theme <- bs_theme(
  primary = "#007bff",    # Company brand blue
  secondary = "#6c757d",  # Neutral gray for secondary actions
  success = "#28a745",    # Kept default green for universal success color
  base_font = font_google("Open Sans"),  # Brand font per style guide
  heading_font = font_google("Montserrat", wght = c(400, 700))  # Brand heading font
)
```

### Test Themes Across Components

When customizing, test how your theme affects:
- All input types
- Buttons (primary, secondary, success, etc.)
- Cards with various content
- Navigation elements
- Plots (with thematic)
- Tables
- Modals and toasts
- Mobile view

### Consider Dark Mode

If offering dark mode, ensure all custom styles work in both:

```r
# Define both themes
light_theme <- bs_theme(
  bg = "#FFFFFF",
  fg = "#212529",
  primary = "#007bff"
) |>
  bs_add_rules("
    .custom-card {
      background: mix($bg, $primary, 95%);
      border: 1px solid $primary;
    }
  ")

dark_theme <- bs_theme(
  bg = "#1a1a1a",
  fg = "#f8f9fa",
  primary = "#375a7f"
) |>
  bs_add_rules("
    .custom-card {
      background: mix($bg, $primary, 95%);
      border: 1px solid $primary;
    }
  ")
```

Using Sass variables ensures custom styles adapt to theme changes.

### Profile Performance

Heavy theming with many custom rules can impact load time:
- Minimize custom Sass/CSS
- Pre-compile Sass when possible
- Use browser dev tools to profile CSS load time
- Consider caching strategies for production

### Version Control Theme Files

Track theme changes in version control:
- Commit `theme.R` or theme configuration
- Track custom Sass/CSS files
- Document breaking changes in themes
- Consider theme versioning for major changes
