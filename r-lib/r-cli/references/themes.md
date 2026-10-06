# CLI Themes and Styling

## Table of Contents

- [Theme Basics](#theme-basics)
- [Container Functions](#container-functions)
- [Selector Types](#selector-types)
- [Theme Properties](#theme-properties)
- [Built-in Themes](#built-in-themes)
- [Custom Themes](#custom-themes)
- [App and Package Themes](#app-and-package-themes)
- [Color Palettes](#color-palettes)
- [Accessibility](#accessibility)
- [Debugging Themes](#debugging-themes)

## Theme Basics

CLI uses a CSS-like theming system to style console output. Themes consist of selectors that match elements and properties that define their appearance.

### How Themes Work

1. Elements are identified by selectors (like `.alert-success` or `.code`)
2. Selectors are matched against the element hierarchy
3. Properties are applied to matched elements
4. Properties cascade through the element tree

### Basic Theme Structure

```r
my_theme <- list(
  ".alert-success" = list(
    "color" = "green",
    "font-weight" = "bold"
  ),
  ".code" = list(
    "color" = "blue",
    "background-color" = "grey90"
  )
)

cli_div(theme = my_theme)
cli_alert_success("Operation completed")
cli_code("result <- compute()")
cli_end()
```

## Container Functions

Containers create themed regions and manage element hierarchy. They auto-close when the function exits or can be closed explicitly with `cli_end()`.

### General Containers

**`cli_div()`** - Generic container for applying themes:

```r
cli_div(theme = list(".emph" = list(color = "red")))
cli_text("This is {.emph emphasized} text")
cli_end()
```

With classes:

```r
cli_div(class = "my-section", theme = list(
  ".my-section" = list("margin-left" = 2),
  ".my-section .code" = list(color = "blue")
))
cli_text("Code: {.code mean(x)}")
cli_end()
```

**`cli_par()`** - Paragraph container:

```r
cli_par()
cli_text("First line")
cli_text("Second line")
cli_end()
```

### List Containers

**`cli_ul()` / `cli_ol()` / `cli_dl()`** - List containers:

```r
# Unordered list
cli_ul()
cli_li("First item")
cli_li("Second item")
cli_end()

# Ordered list
cli_ol()
cli_li("Step one")
cli_li("Step two")
cli_end()

# Definition list
cli_dl()
cli_li(c(term = "Definition of term"))
cli_end()
```

### Auto-closing Behavior

Containers automatically close when the calling function exits:

```r
my_function <- function() {
  cli_div(theme = list(".alert" = list(color = "red")))
  cli_alert("Alert message")
  # No need to call cli_end() - auto-closes here
}
```

Explicit closing with `cli_end()`:

```r
id <- cli_div(theme = my_theme)
cli_text("Themed content")
cli_end(id)  # Close specific container
```

### Theme Scoping and Inheritance

Themes inherit from parent containers and can be overridden:

```r
# Outer theme
cli_div(theme = list(".code" = list(color = "blue")))

# Inner theme overrides
cli_div(theme = list(".code" = list(color = "red")))
cli_text("Code is {.code red} here")
cli_end()

cli_text("Code is {.code blue} here")
cli_end()
```

## Selector Types

### Simple Selectors

Match elements by class:

```r
list(
  ".code" = list(color = "blue"),       # Matches {.code ...}
  ".file" = list(color = "magenta"),    # Matches {.file ...}
  ".pkg" = list(color = "cyan")         # Matches {.pkg ...}
)
```

### Element Type Selectors

Match by element type:

```r
list(
  "h1" = list(color = "blue", "font-weight" = "bold"),
  "ul" = list("margin-left" = 2),
  "li" = list(before = "* ")
)
```

### Descendant Selectors

Match elements within other elements:

```r
list(
  ".my-section .code" = list(color = "blue"),
  ".alert .emph" = list(color = "red")
)
```

### Multiple Selectors

Apply same styles to multiple selectors:

```r
list(
  ".code, .fun, .fn" = list(color = "blue")
)
```

### Pseudo-selectors

Match specific states or positions:

```r
list(
  "li:before" = list(content = "-> "),
  "ul li:first-child" = list("margin-top" = 0)
)
```

## Theme Properties

### Color Properties

**`color`** - Text color:

```r
list(".alert" = list(color = "red"))
```

**`background-color`** - Background color:

```r
list(".code" = list("background-color" = "grey90"))
```

Color formats:
- Named colors: `"red"`, `"blue"`, `"green"`
- ANSI colors: `"ansi_red"`, `"ansi_bright_blue"`
- RGB hex: `"#FF5733"`
- RGB function: `rgb(255, 87, 51)`

### Text Formatting

**`font-weight`** - Text weight:

```r
list(".strong" = list("font-weight" = "bold"))
```

**`font-style`** - Text style:

```r
list(".emph" = list("font-style" = "italic"))
```

**`text-decoration`** - Text decoration:

```r
list(".url" = list("text-decoration" = "underline"))
```

### Spacing Properties

**`margin-left`** - Left margin (in characters):

```r
list(".par" = list("margin-left" = 2))
```

**`margin-right`** - Right margin:

```r
list(".par" = list("margin-right" = 2))
```

**`margin-top`** - Top margin (in lines):

```r
list("h1" = list("margin-top" = 1, "margin-bottom" = 1))
```

**`padding-left`** - Left padding:

```r
list(".alert" = list("padding-left" = 2))
```

### Content Properties

**`before`** - Content before element:

```r
list(
  ".alert-success:before" = list(content = "[OK] "),
  "ul li:before" = list(content = "* ")
)
```

**`after`** - Content after element:

```r
list(".code:after" = list(content = " }"))
```

### List Properties

**`list-style-type`** - List marker style:

```r
list(
  "ul" = list("list-style-type" = "bullet"),
  "ol" = list("list-style-type" = "decimal")
)
```

Values: `"bullet"`, `"circle"`, `"square"`, `"decimal"`, `"lower-alpha"`, `"upper-alpha"`

**`start`** - Ordered list start number:

```r
list("ol" = list(start = 5))
```

### Line Properties

**`line-type`** - Line drawing style:

```r
list(".rule" = list("line-type" = "double"))
```

Values: `"single"`, `"double"`, `"bar1"` through `"bar8"`

### Format Control

**`fmt`** - Custom format function:

```r
list(
  ".timestamp" = list(
    fmt = function(x) format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  )
)
```

**`transform`** - Transform function:

```r
list(
  ".upper" = list(transform = toupper)
)
```

## Built-in Themes

### Default Theme

The standard cli theme with semantic colors and spacing:

```r
# View built-in theme structure
str(builtin_theme(), max.level = 2)
```

Key elements:
- Blue for code, functions, arguments
- Magenta for files and paths
- Cyan for packages
- Green for success
- Red for errors
- Yellow for warnings

### Simple Theme

A minimal theme without colors:

```r
options(cli.theme = simple_theme())
```

Useful for:
- Terminals without color support
- Logging to files
- Screen readers
- Testing

### Dark Theme

Optimized for dark terminal backgrounds (included in default theme with automatic detection).

## Custom Themes

### Creating a Custom Theme

Build themes incrementally:

```r
my_theme <- list(
  # Headers
  "h1" = list(
    color = "blue",
    "font-weight" = "bold",
    "margin-top" = 1,
    "margin-bottom" = 1,
    before = "== ",
    after = " =="
  ),

  # Code elements
  ".code" = list(
    color = "cyan",
    "background-color" = "grey10"
  ),

  ".fn" = list(
    color = "blue",
    after = "()"
  ),

  # Alerts
  ".alert-success" = list(
    before = "[OK] ",
    color = "green"
  ),

  ".alert-danger" = list(
    before = "[ERROR] ",
    color = "red",
    "font-weight" = "bold"
  ),

  # Lists
  "ul li" = list(
    before = "• "
  ),

  "ol li" = list(
    "list-style-type" = "decimal"
  )
)
```

### Extending Built-in Themes

Merge your theme with the built-in theme:

```r
my_theme <- utils::modifyList(
  builtin_theme(),
  list(
    ".code" = list(color = "magenta"),
    ".custom" = list(color = "cyan")
  )
)

cli_div(theme = my_theme)
```

### Theme Functions

Create reusable theme functions:

```r
create_brand_theme <- function(primary_color = "blue") {
  list(
    "h1" = list(color = primary_color, "font-weight" = "bold"),
    "h2" = list(color = primary_color),
    ".code" = list(color = primary_color),
    ".alert-success" = list(color = "green"),
    ".alert-danger" = list(color = "red")
  )
}

cli_div(theme = create_brand_theme("purple"))
```

## App and Package Themes

### Setting Package Theme

Define a package-level theme in your `.onLoad()`:

```r
.onLoad <- function(libname, pkgname) {
  my_theme <- list(
    ".code" = list(color = "blue"),
    ".pkg" = list(color = "cyan")
  )

  options(cli.theme = my_theme)
}
```

### User Configuration

Users can override package themes via options:

```r
# In .Rprofile
options(cli.theme = list(
  ".code" = list(color = "magenta")
))
```

### Conditional Themes

Apply themes based on environment:

```r
.onLoad <- function(libname, pkgname) {
  theme <- if (cli::num_ansi_colors() >= 256) {
    rich_theme()  # Full color theme
  } else {
    simple_theme()  # Basic theme
  }

  options(cli.theme = theme)
}
```

### Theme Precedence

Themes are applied in this order (highest to lowest):
1. Inline theme in `cli_div(theme = ...)`
2. User's `cli.theme` option
3. Package's default theme
4. Built-in theme

## Color Palettes

### Configuring Palettes

Set the ANSI color palette with the `cli.palette` option:

```r
options(cli.palette = "vscode")
```

### Built-in Palettes

**`dichro`** - Dichromat-friendly palette:
```r
options(cli.palette = "dichro")
```

**`vscode`** - VS Code color scheme:
```r
options(cli.palette = "vscode")
```

**`iterm`** - iTerm2 default colors:
```r
options(cli.palette = "iterm")
```

### Custom 16-Color Palettes

Define custom ANSI colors:

```r
my_palette <- c(
  # Normal colors (0-7)
  "#000000",  # black
  "#CD0000",  # red
  "#00CD00",  # green
  "#CDCD00",  # yellow
  "#0000EE",  # blue
  "#CD00CD",  # magenta
  "#00CDCD",  # cyan
  "#E5E5E5",  # white

  # Bright colors (8-15)
  "#7F7F7F",  # bright black (grey)
  "#FF0000",  # bright red
  "#00FF00",  # bright green
  "#FFFF00",  # bright yellow
  "#5C5CFF",  # bright blue
  "#FF00FF",  # bright magenta
  "#00FFFF",  # bright cyan
  "#FFFFFF"   # bright white
)

options(cli.palette = my_palette)
```

### Truecolor Support

Check for truecolor support:

```r
cli::num_ansi_colors()
# Returns:
#   1 - no color
#   8 - 8 colors
#   256 - 256 colors
#   16777216 - truecolor (24-bit)
```

Use truecolor when available:

```r
if (cli::num_ansi_colors() >= 16777216) {
  # Use RGB hex colors
  list(".code" = list(color = "#6A9FB5"))
} else {
  # Fall back to named colors
  list(".code" = list(color = "blue"))
}
```

### Color Detection

CLI automatically detects color support from:
- `NO_COLOR` environment variable (disables color)
- `TERM` environment variable
- System capabilities
- RStudio version

Force color support:

```r
options(cli.num_colors = 256)  # Force 256 colors
```

Disable colors:

```r
options(cli.num_colors = 1)
# Or set environment variable
Sys.setenv(NO_COLOR = "1")
```

## Accessibility

### Color Contrast

Ensure sufficient contrast for readability:

```r
# Good contrast
list(
  ".code" = list(color = "blue"),        # Dark on light
  ".emph" = list(color = "ansi_red")     # High contrast
)

# Poor contrast (avoid)
list(
  ".code" = list(color = "grey80"),      # Low contrast on white
  ".emph" = list(color = "#EEEEEE")      # Nearly invisible on white
)
```

### Unicode Fallbacks

Provide ASCII alternatives for Unicode symbols:

```r
bullet <- if (cli::is_utf8_output()) "\u2022" else "*"

list(
  "ul li:before" = list(content = bullet)
)
```

Built-in Unicode detection:

```r
cli::is_utf8_output()  # TRUE if UTF-8 is supported
```

### Color-blind Friendly Themes

Use the dichromat palette or ensure patterns work without color:

```r
color_blind_theme <- list(
  ".alert-success" = list(
    before = "[OK] ",
    color = "green"
  ),
  ".alert-danger" = list(
    before = "[ERROR] ",
    color = "red",
    "font-weight" = "bold"
  )
)
```

Benefits:
- Symbols provide meaning without color
- Bold text adds emphasis
- Works for colorblind users

### Screen Reader Compatibility

Keep semantic meaning in text, not just styling:

```r
# Good: Meaning is in text
cli_alert_success("File saved successfully")

# Poor: Meaning only in style
cli_text("{.green File saved}")
```

## Debugging Themes

### Using cli_debug_doc()

Visualize document structure and applied themes:

```r
# Enable debug mode
withr::local_options(cli.debug = TRUE)

cli_div(class = "my-section")
cli_h1("Header")
cli_text("Text with {.code code}")
cli_end()
```

Debug output shows:
- Element hierarchy
- Applied selectors
- Computed properties
- Theme inheritance

### Inspecting Theme Application

Check which theme properties are applied:

```r
# Create a test container
cli_div(theme = my_theme, class = "test")

# Debug output will show:
# - Matched selectors
# - Applied properties
# - Inherited values

cli_text("Test content")
cli_end()
```

### Theme Testing Strategy

Test themes across different environments:

```r
test_theme <- function(theme) {
  old_colors <- options(cli.num_colors = 256)
  on.exit(options(old_colors))

  cli_div(theme = theme)
  cli_h1("Header")
  cli_alert_success("Success message")
  cli_text("Code: {.code mean(x)}")
  cli_end()
}

# Test with different color depths
test_colors <- c(1, 8, 256, 16777216)
for (n in test_colors) {
  options(cli.num_colors = n)
  test_theme(my_theme)
}
```

### Common Theme Issues

**Colors not appearing:**
- Check `cli::num_ansi_colors()` output
- Verify terminal supports colors
- Check for `NO_COLOR` environment variable

**Spacing incorrect:**
- Use `cli.debug = TRUE` to see computed margins
- Check for inherited spacing properties
- Verify units (characters vs. lines)

**Selectors not matching:**
- Use `cli.debug = TRUE` to see selector matching
- Check selector syntax (spaces for descendants)
- Verify class names match inline markup
