# ANSI Operations and Advanced Features

## Table of Contents

1. [ANSI String Operations](#ansi-string-operations)
   - [Character Counting](#character-counting)
   - [Text Alignment](#text-alignment)
   - [String Splitting](#string-splitting)
   - [Substring Operations](#substring-operations)
   - [Text Wrapping](#text-wrapping)
   - [Case Conversion](#case-conversion)
   - [Whitespace Handling](#whitespace-handling)
   - [Columnar Layout](#columnar-layout)
   - [Removing ANSI Codes](#removing-ansi-codes)
2. [Hyperlinks](#hyperlinks)
3. [Advanced Colors](#advanced-colors)
4. [Symbol Sets](#symbol-sets)
5. [Testing CLI Output](#testing-cli-output)
6. [Performance](#performance)
7. [Debugging](#debugging)

## ANSI String Operations

All base R string functions break when applied to ANSI-formatted text because they count escape codes as characters. The cli package provides ANSI-aware versions of common string operations.

### Character Counting

Use `ansi_nchar()` instead of `nchar()` to count visible characters:

```r
# Problem with base R
text <- col_red("hello")
nchar(text)
#> [1] 15  # Includes ANSI codes

# Solution with cli
ansi_nchar(text)
#> [1] 5  # Counts only visible characters

# Works with vectors
texts <- c(col_blue("short"), col_green("longer text"))
ansi_nchar(texts)
#> [1]  5 11

# type argument works like base nchar()
ansi_nchar(text, type = "width")  # Display width
ansi_nchar(text, type = "chars")  # Character count
ansi_nchar(text, type = "bytes")  # Byte count
```

### Text Alignment

Use `ansi_align()` to align formatted text while accounting for ANSI codes:

```r
# Left alignment (default)
texts <- c(col_red("Error"), col_yellow("Warning"), col_green("OK"))
ansi_align(texts, width = 10)
#> [1] "Error     " "Warning   " "OK        "

# Right alignment
ansi_align(texts, width = 10, align = "right")
#> [1] "     Error" "   Warning" "        OK"

# Center alignment
ansi_align(texts, width = 10, align = "center")
#> [1] "  Error   " " Warning  " "    OK    "

# Practical example: aligned status messages
statuses <- c(col_green("Success"), col_red("Failed"), col_yellow("Pending"))
labels <- c("Database", "API", "Cache")
paste0(labels, ": ", ansi_align(statuses, width = 10))
#> [1] "Database: Success   " "API: Failed     " "Cache: Pending   "
```

### String Splitting

Use `ansi_strsplit()` instead of `strsplit()`:

```r
# Split colored text
text <- paste0(col_red("hello"), " ", col_blue("world"))
ansi_strsplit(text, " ")
#> [[1]]
#> [1] "\033[31mhello\033[39m" "\033[34mworld\033[39m"

# Fixed strings
ansi_strsplit(col_green("a-b-c"), "-", fixed = TRUE)
#> [[1]]
#> [1] "\033[32ma\033[39m" "\033[32mb\033[39m" "\033[32mc\033[39m"

# Regular expressions
text <- col_red("one123two456three")
ansi_strsplit(text, "[0-9]+")
#> [[1]]
#> [1] "\033[31mone\033[39m"   "\033[31mtwo\033[39m"   "\033[31mthree\033[39m"
```

### Substring Operations

Use `ansi_substr()` and `ansi_substring()` for extracting substrings:

```r
# Extract substring
text <- col_red("hello world")
ansi_substr(text, 1, 5)
#> [1] "\033[31mhello\033[39m"  # Preserves color

ansi_substr(text, 7, 11)
#> [1] "\033[31mworld\033[39m"

# Negative indices work like base R
ansi_substring(text, 7)  # From position 7 to end
#> [1] "\033[31mworld\033[39m"

# Substring replacement
text <- col_blue("hello world")
ansi_substr(text, 1, 5) <- "HELLO"
text
#> [1] "\033[34mHELLO world\033[39m"

# Multiple strings
texts <- c(col_red("abcdef"), col_green("123456"))
ansi_substr(texts, 2, 4)
#> [1] "\033[31mbcd\033[39m" "\033[32m234\033[39m"
```

### Text Wrapping

Use `ansi_strwrap()` for wrapping formatted text:

```r
# Basic wrapping
long_text <- paste0(
  col_blue("This is a long piece of text "),
  col_red("that needs to be wrapped "),
  col_green("across multiple lines")
)
ansi_strwrap(long_text, width = 30)
#> [1] "This is a long piece of text"
#> [2] "that needs to be wrapped"
#> [3] "across multiple lines"

# Custom indent and exdent
ansi_strwrap(long_text, width = 40, indent = 2, exdent = 4)
#> First line indented by 2, subsequent by 4

# Simplify option
ansi_strwrap(c(col_red("short"), col_blue("text")), simplify = FALSE)
#> Returns a list

# Practical example: formatted help text
help_text <- paste0(
  col_bold("--verbose"), " ",
  "Enable verbose output with detailed logging information"
)
cat(ansi_strwrap(help_text, width = 60), sep = "\n")
```

### Case Conversion

Use `ansi_toupper()`, `ansi_tolower()`, and `ansi_chartr()`:

```r
# Convert to uppercase
text <- col_red("hello world")
ansi_toupper(text)
#> [1] "\033[31mHELLO WORLD\033[39m"

# Convert to lowercase
text <- col_blue("HELLO WORLD")
ansi_tolower(text)
#> [1] "\033[34mhello world\033[39m"

# Character translation
ansi_chartr("aeiou", "AEIOU", col_green("hello world"))
#> [1] "\033[32mhEllO wOrld\033[39m"

# Preserves all formatting
text <- paste0(col_red(style_bold("error")), ": ", col_blue("message"))
ansi_toupper(text)
#> Colors and styles preserved
```

### Whitespace Handling

Use `ansi_trimws()` to trim whitespace from ANSI strings:

```r
# Trim both sides (default)
text <- col_red("  hello world  ")
ansi_trimws(text)
#> [1] "\033[31mhello world\033[39m"

# Trim left only
ansi_trimws(text, which = "left")
#> [1] "\033[31mhello world  \033[39m"

# Trim right only
ansi_trimws(text, which = "right")
#> [1] "\033[31m  hello world\033[39m"

# Custom whitespace definition
ansi_trimws(col_blue("..hello.."), whitespace = ".")
#> [1] "\033[34mhello\033[39m"
```

### Columnar Layout

Use `ansi_columns()` to create column layouts with ANSI-formatted text:

```r
# Simple two-column layout
items <- paste0(col_blue(letters[1:10]), " = ", col_green(1:10))
ansi_columns(items, width = 40)
#> Arranges items in columns that fit in 40 characters

# Custom number of columns
ansi_columns(items, width = 60, fill = "cols")
#> fill = "cols" fills by columns, "rows" fills by rows

# Practical example: displaying options
options <- paste0(
  col_yellow(sprintf("--option%d", 1:20)),
  " ",
  col_grey("Description text")
)
ansi_columns(options, width = 80)
```

### Removing ANSI Codes

Use `ansi_strip()` to remove all ANSI formatting:

```r
# Remove all ANSI codes
text <- col_red(style_bold("error"))
ansi_strip(text)
#> [1] "error"

# Works with complex formatting
text <- paste0(
  col_blue("Status: "),
  col_green(style_underline("OK"))
)
ansi_strip(text)
#> [1] "Status: OK"

# Essential for testing (see Testing CLI Output section)
expect_equal(ansi_strip(my_output()), "expected plain text")
```

## Hyperlinks

Modern terminals support hyperlinks via ANSI escape codes. The cli package provides several link types through inline markup.

### Terminal Support Detection

Check if the current terminal supports hyperlinks:

```r
# Check for hyperlink support
style_hyperlink_supported()
#> [1] TRUE or FALSE

# Hyperlinks are auto-disabled when not supported
# Always safe to use in code
```

### Link Types Overview

```r
# URL links - external websites
cli_text("See {.url https://example.com}")

# URL with custom text
cli_text("Visit our {.href [website](https://example.com)}")

# File links
cli_text("Check {.file /path/to/file.R}")

# File with line and column
cli_text("Error at {.file /path/to/file.R:42:10}")

# Function documentation
cli_text("Use {.fun package::function}")

# Help topic
cli_text("See {.help topic}")

# Topic in package
cli_text("Read {.topic stats::lm}")

# Vignette
cli_text("Tutorial: {.vignette dplyr::introduction}")

# Executable code
cli_text("Try {.run code_to_execute()}")
```

### .url vs .href - When to Use Each

**Use `.url` when:**
- The URL is the meaningful content
- Showing the full URL is important
- The link destination should be visible

```r
cli_text("Documentation: {.url https://cli.r-lib.org}")
cli_text("API endpoint: {.url https://api.example.com/v1}")
```

**Use `.href` when:**
- The link text should differ from the URL
- Creating natural prose with embedded links
- The URL is long or technical

```r
cli_text("Read the {.href [complete guide](https://very-long-url.com/path)}")
cli_text("See {.href [issue #123](https://github.com/org/repo/issues/123)}")
```

### .file with Line and Column Syntax

```r
# Just the file
cli_text("Modified {.file script.R}")

# File with line number
cli_text("Error in {.file script.R:42}")

# File with line and column
cli_text("Syntax error at {.file script.R:42:10}")

# Full path with line numbers
cli_text("See {.file /home/user/project/R/utils.R:100:5}")

# Practical example in error messages
check_syntax <- function(file, line, col) {
  cli_abort(c(
    "Syntax error detected",
    "x" = "Unexpected token at {.file {file}:{line}:{col}}",
    "i" = "Check for matching braces"
  ))
}
```

### Documentation Links

```r
# Function help - opens help page
cli_text("Calculate mean with {.fun mean}")
cli_text("Join tables using {.fun dplyr::left_join}")

# Help topic
cli_text("Learn about {.help vectors}")

# Topic from specific package
cli_text("Read about {.topic dplyr::mutate}")

# Vignette
cli_text("Tutorial: {.vignette dplyr::window-functions}")
cli_text("Guide: {.vignette tidyr::pivot}")

# Practical example: suggesting functions
suggest_function <- function() {
  cli_inform(c(
    "i" = "For string manipulation, try {.fun stringr::str_replace}",
    "i" = "See {.topic stringr::str_replace} for examples",
    "i" = "Learn more: {.vignette stringr::stringr}"
  ))
}
```

### .run Links - Executable Code

**Security Warning:** `.run` links execute arbitrary code when clicked. Use with extreme caution.

```r
# Simple command
cli_text("Install with {.run install.packages('cli')}")

# Multiple statements
cli_text("Setup: {.run source('setup.R'); init_project()}")

# Display differs from execution
cli_text("{.run [reset database](drop_all_tables(); rebuild())}")

# Safe use cases only:
# - Your own diagnostic commands
# - Read-only operations
# - Well-understood helper functions

# NEVER use .run with:
# - User-supplied input
# - File system modifications from untrusted sources
# - Network operations
# - Data deletion
```

### Practical Hyperlink Examples

```r
# Error with file link
file_error <- function(path, line) {
  cli_abort(c(
    "Parse error in configuration file",
    "x" = "Invalid syntax at {.file {path}:{line}}",
    "i" = "Check the {.href [YAML specification](https://yaml.org/spec/)}"
  ))
}

# Function suggestion with documentation
suggest_alternative <- function(old_fn, new_fn) {
  cli_warn(c(
    "{.fun {old_fn}} is deprecated",
    "!" = "Use {.fun {new_fn}} instead",
    "i" = "See {.topic {new_fn}} for details"
  ))
}

# Help message with links
show_resources <- function() {
  cli_inform(c(
    "v" = "Package installed successfully",
    "i" = "Documentation: {.url https://pkg.example.com}",
    "i" = "Quick start: {.vignette mypkg::quickstart}",
    "i" = "Get help: {.run help('mypkg')}"
  ))
}
```

## Advanced Colors

### Color Palette Customization

Beyond basic colors, cli supports extensive palette customization:

```r
# Create custom color palette
my_palette <- list(
  error = "#FF5555",
  warn = "#FFB86C",
  success = "#50FA7B",
  info = "#8BE9FD"
)

# Apply custom theme
my_theme <- list(
  span.error = list(color = my_palette$error),
  span.warn = list(color = my_palette$warn),
  span.success = list(color = my_palette$success),
  span.info = list(color = my_palette$info)
)

cli_div(theme = my_theme)
```

### Terminal Capability Detection

```r
# Detect number of colors supported
num_ansi_colors()
#> Returns: 1 (no colors), 8, 256, or 16777216 (truecolor)

# Check capabilities
if (num_ansi_colors() >= 256) {
  # Use 256-color palette
  style_rgb(100, 150, 200)
} else if (num_ansi_colors() >= 8) {
  # Fall back to 8-color palette
  col_blue()
} else {
  # No colors, use plain text
  identity()
}
```

### Color Mode Details

**Truecolor (16.7M colors):**
```r
# num_ansi_colors() returns 16777216
# Full RGB color space available
make_ansi_style("#FF5733")  # Hex colors
style_rgb(255, 87, 51)       # RGB values
```

**256-color mode:**
```r
# num_ansi_colors() returns 256
# 216 colors + 24 grayscale
# Colors approximated from truecolor
```

**8-color mode:**
```r
# num_ansi_colors() returns 8
# Basic ANSI colors only: black, red, green, yellow,
# blue, magenta, cyan, white
```

**No color (1):**
```r
# num_ansi_colors() returns 1
# All styling removed
# Useful for piping to files or non-terminal output
```

### Custom Color Functions

```r
# Define reusable color functions
error_color <- make_ansi_style("#FF5555", bg = FALSE)
success_color <- make_ansi_style("#50FA7B", bg = FALSE)
highlight_bg <- make_ansi_style("#FFFF00", bg = TRUE)

# Use in messages
cli_text("Status: {error_color('Failed')}")
cli_text("Result: {success_color('Success')}")
cli_text("{highlight_bg('Important')}")

# Combine styles
emphasize <- combine_ansi_styles(
  make_ansi_style("#FF5555"),
  style_bold
)
cli_text("{emphasize('Critical warning')}")
```

## Symbol Sets

The cli package provides Unicode symbols with automatic ASCII fallback.

### Symbol Behavior

```r
# Unicode symbols in capable terminals
symbol$tick           # ✔
symbol$cross          # ✖
symbol$arrow_right    # →
symbol$ellipsis       # …
symbol$warning        # ⚠

# Automatic ASCII fallback when needed
# Environment: NO_UNICODE=1 or incapable terminal
symbol$tick           # v
symbol$cross          # x
symbol$arrow_right    # ->
symbol$ellipsis       # ...
symbol$warning        # !
```

### Available Symbols

```r
# Status indicators
symbol$tick            # ✔ or v
symbol$cross           # ✖ or x
symbol$circle_filled   # ● or (*)
symbol$circle_dotted   # ◌ or ( )

# Arrows
symbol$arrow_right     # → or ->
symbol$arrow_left      # ← or <-
symbol$arrow_up        # ↑ or ^
symbol$arrow_down      # ↓ or v

# UI elements
symbol$ellipsis        # … or ...
symbol$continue        # ⋯ or ...
symbol$warning         # ⚠ or !
symbol$info            # ℹ or i

# Pointers
symbol$pointer         # ❯ or >
symbol$radio_on        # ◉ or (*)
symbol$radio_off       # ◯ or ( )

# Box drawing (for tables/borders)
symbol$line            # ─ or -
symbol$double_line     # ═ or =
```

### Practical Symbol Usage

```r
# Status messages
cli_alert("Processing {symbol$ellipsis}")
cli_text("{symbol$tick} Done")
cli_text("{symbol$cross} Failed")

# Lists with custom bullets
cli_text("{symbol$pointer} Option 1")
cli_text("{symbol$pointer} Option 2")

# Progress indicators
cli_text("Step 1 {symbol$arrow_right} Step 2 {symbol$arrow_right} Step 3")
```

## Testing CLI Output

### Basic Testing with ansi_strip()

```r
test_that("function produces correct message", {
  # Capture output
  output <- capture.output({
    cli_alert_success("Operation complete")
  })

  # Strip ANSI codes for comparison
  plain <- ansi_strip(paste(output, collapse = "\n"))

  expect_match(plain, "Operation complete")
})
```

### Snapshot Testing with testthat

Best practice for testing CLI output:

```r
test_that("error message is correct", {
  # Snapshot the entire formatted output
  expect_snapshot(error = TRUE, {
    my_function_that_errors()
  })
})

test_that("progress output is correct", {
  # Use local options for reproducible output
  withr::local_options(cli.width = 80)

  expect_snapshot({
    my_function_with_progress()
  })
})
```

### Testing in Non-Interactive Mode

```r
test_that("cli works non-interactively", {
  # Simulate non-interactive environment
  withr::local_options(cli.dynamic = FALSE)

  output <- capture.output({
    cli_progress_bar("Working", total = 100)
    for (i in 1:100) cli_progress_update()
  })

  # No progress bar in non-interactive mode
  expect_length(output, 0)
})
```

### Using test_that_cli()

Special testing helper for CLI output:

```r
test_that_cli("formatted message appears", {
  # Automatically sets up CLI testing environment
  # - Fixed width (80 columns)
  # - ANSI colors enabled
  # - Unicode symbols enabled

  expect_snapshot({
    cli_h1("Header")
    cli_alert_success("Done")
  })
})

# Equivalent to:
test_that("formatted message appears", {
  withr::local_options(
    cli.width = 80,
    cli.num_colors = 256,
    cli.unicode = TRUE
  )

  expect_snapshot({
    cli_h1("Header")
    cli_alert_success("Done")
  })
})
```

### Transform for Reproducible Tests

```r
test_that("output is stable", {
  expect_snapshot(
    my_function_with_timestamps(),
    transform = function(output) {
      # Remove variable elements
      output <- ansi_strip(output)
      output <- gsub("\\d{4}-\\d{2}-\\d{2}", "[DATE]", output)
      output <- gsub("\\d+\\.\\d+ seconds", "[TIME]", output)
      output
    }
  )
})
```

## Performance

### When CLI Adds Overhead

CLI has minimal overhead in most cases, but be aware of:

**High-frequency operations:**
```r
# Avoid CLI in tight loops
for (i in 1:1000000) {
  cli_alert("Iteration {i}")  # Very slow!
}

# Instead: use progress bar
cli_progress_bar("Processing", total = 1000000)
for (i in 1:1000000) {
  # work
  if (i %% 1000 == 0) cli_progress_update()
}
```

**String interpolation cost:**
```r
# Expensive: interpolation on every call
for (i in 1:10000) {
  msg <- cli::cli_fmt(cli::cli_text("Value: {i}"))
}

# Cheaper: use sprintf or paste for simple cases
for (i in 1:10000) {
  msg <- sprintf("Value: %d", i)
}
```

### Optimization Strategies

**Disable in production:**
```r
# Option to disable all CLI output
options(cli.default_handler = function(...) NULL)

# Or use environment variable
Sys.setenv(CLI_NO_OUTPUT = "true")
```

**Batch updates:**
```r
# Bad: update on every item
cli_progress_bar("Processing", total = 1000000)
for (i in 1:1000000) {
  process(i)
  cli_progress_update()  # Too frequent
}

# Good: batch updates
cli_progress_bar("Processing", total = 1000000)
for (i in 1:1000000) {
  process(i)
  if (i %% 100 == 0) cli_progress_update(inc = 100)
}
```

**Conditional verbosity:**
```r
process_data <- function(data, verbose = TRUE) {
  if (verbose) {
    cli_progress_bar("Processing", total = nrow(data))
  }

  for (i in seq_len(nrow(data))) {
    # work
    if (verbose) cli_progress_update()
  }
}
```

## Debugging

### CLI Internal State

```r
# Check current CLI state
cli::cli_status()
#> Shows active containers, progress bars, themes

# Debug theme application
options(cli.debug = TRUE)
cli_alert("Test")
#> Shows theme resolution and style application
```

### Troubleshooting Techniques

**Colors not appearing:**
```r
# Check color support
cli::num_ansi_colors()
#> Should be > 1

# Force colors on
options(cli.num_colors = 256)

# Check if output is to terminal
isatty(stdout())
#> Should be TRUE for interactive colors
```

**Hyperlinks not working:**
```r
# Check hyperlink support
cli::style_hyperlink_supported()

# Force enable for testing
options(cli.hyperlink = TRUE)

# Test with explicit hyperlink
writeLines(style_hyperlink("test", "https://example.com"))
```

**Unicode symbols showing as boxes:**
```r
# Check Unicode support
l10n_info()$`UTF-8`
#> Should be TRUE

# Force ASCII fallback
options(cli.unicode = FALSE)

# Or use environment variable
Sys.setenv(CLI_NO_UNICODE = "true")
```

**Progress bars not updating:**
```r
# Check if output is buffered
# Progress requires unbuffered output
flush.console()  # Force output after updates

# Check for interactive mode
interactive()
#> Should be TRUE for dynamic progress

# Test with forced dynamic mode
options(cli.dynamic = TRUE)
```

**Debugging custom themes:**
```r
# Validate theme structure
my_theme <- list(
  span.error = list(color = "red", "font-weight" = "bold")
)

cli_div(theme = my_theme)
cli_text("Test {.error message}")

# Check resolved styles
options(cli.debug = TRUE)
# Shows which selectors match and final styles
```
