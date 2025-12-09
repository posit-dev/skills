# CLI Inline Markup Reference

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Syntax](#basic-syntax)
3. [Code & Syntax Classes](#code--syntax-classes)
4. [Files & Paths Classes](#files--paths-classes)
5. [Communication Classes](#communication-classes)
6. [Values & Data Classes](#values--data-classes)
7. [Emphasis Classes](#emphasis-classes)
8. [Documentation Classes](#documentation-classes)
9. [Special Classes](#special-classes)
10. [Vector Collapsing](#vector-collapsing)
11. [Advanced Patterns](#advanced-patterns)
12. [Pluralization](#pluralization)
13. [Performance Considerations](#performance-considerations)
14. [Quick Reference Table](#quick-reference-table)

## Introduction

Read this file when you need to:

- Look up the correct inline markup class for specific content types
- Understand how to nest and combine markup classes
- Learn vector collapsing behavior and customization
- Master pluralization patterns beyond basic `{?s}`
- Optimize performance for high-frequency messaging
- Troubleshoot unexpected formatting behavior

Inline markup classes format text within cli messages using `{.class content}` syntax. They integrate with glue string interpolation and work across all cli functions: `cli_text()`, `cli_abort()`, `cli_warn()`, `cli_inform()`, `cli_alert_*()`, etc.

## Basic Syntax

Inline markup uses curly braces with a period-prefixed class name:

```r
cli_text("Function {.fn mean} calculates {.field average}")
#> Function `mean()` calculates average
```

**Key syntax rules:**

- Format: `{.class content}`
- Content is interpolated if it contains `{}`
- Double braces `{{` and `}}` escape literal braces
- Whitespace inside `{}` is preserved in output
- Classes can be nested (see [Advanced Patterns](#advanced-patterns))

## Code & Syntax Classes

### .code

Generic code formatting for expressions, statements, or syntax:

```r
cli_text("Use {.code sum(x, na.rm = TRUE)} to ignore NA values")
cli_text("Set {.code options(width = 120)} in your .Rprofile")
cli_text("The {.code return()} statement exits early")
```

**When to use:**
- Multi-token code expressions
- Syntax examples
- Configuration snippets
- When other code classes are too specific

### .fn and .fun

Function names with automatic parentheses:

```r
cli_text("Call {.fn mean} to calculate average")
#> Call `mean()` to calculate average

cli_text("Use {.fun base::mean} for namespace clarity")
#> Use `base::mean()` for namespace clarity
```

**Automatic formatting:**
- Adds `()` suffix automatically
- Supports `package::function` notation
- Both `.fn` and `.fun` are equivalent

**When to use:**
- Referring to functions by name
- Suggesting which function to call
- Error messages about function usage

### .arg

Function argument names:

```r
cli_abort(c(
  "{.arg x} must be numeric",
  "i" = "Set {.arg na.rm = TRUE} to handle missing values"
))
```

**When to use:**
- Parameter validation errors
- Documenting function arguments
- Explaining argument behavior

### .cls

S3/S4/R6 class names:

```r
cli_abort("Expected {.cls data.frame}, got {.cls {class(x)}}")
cli_text("Object is {.cls tbl_df}, a tibble subclass")
```

**When to use:**
- Type checking errors
- Documenting expected types
- Explaining inheritance

### .type

Broader type descriptions (base types, generic categories):

```r
cli_abort("Input must be {.type integer}, not {.type {typeof(x)}}")
cli_text("Coercing from {.type character} to {.type numeric}")
```

**When to use:**
- Base R types: integer, double, character, logical
- Generic type categories
- Type coercion messages

### .obj_type_friendly

User-friendly type descriptions with indefinite articles:

```r
x <- data.frame()
cli_text("You provided {.obj_type_friendly {x}}")
#> You provided a data frame

y <- 1:10
cli_text("You provided {.obj_type_friendly {y}}")
#> You provided an integer vector
```

**Automatic features:**
- Adds "a"/"an" article automatically
- Uses friendly names ("data frame" not "data.frame")
- Handles pluralization for vectors

## Files & Paths Classes

### .file

File names and paths with appropriate formatting:

```r
cli_text("Reading {.file data/input.csv}")
cli_warn("File {.file ~/.ssh/config} has insecure permissions")
cli_inform("Created {.file output/results.xlsx}")
```

**Best practices:**
- Use for any file reference
- Works with relative and absolute paths
- Handles home directory expansion

### .path

Directory paths and file system locations:

```r
cli_text("Installing to {.path /usr/local/lib/R}")
cli_text("Working directory: {.path {getwd()}}")
cli_abort("Directory {.path {dir}} does not exist")
```

**When to use .file vs .path:**
- `.file` - Files, scripts, documents
- `.path` - Directories, installation locations, system paths

## Communication Classes

### .email

Email addresses:

```r
cli_text("Contact maintainer at {.email user@example.com}")
cli_inform("Send bug reports to {.email bugs@r-project.org}")
```

**Features:**
- Creates `mailto:` links in supported terminals
- Formatted distinctly from regular text

### .url

Web URLs and URIs:

```r
cli_text("Visit {.url https://cli.r-lib.org} for documentation")
cli_text("API endpoint: {.url https://api.example.com/v1}")
```

**Features:**
- Creates clickable hyperlinks in supported terminals
- Formats protocol, domain, and path distinctly

### .href

Custom hyperlinks with separate text and URL:

```r
cli_text("See {.href [documentation](https://cli.r-lib.org)}")
cli_text("Read {.href [vignette](vignette:cli::inline-markup)}")
```

**Syntax:**
- Format: `{.href [text](url)}`
- Markdown-style link syntax
- Text and URL can be styled differently

**Link types:**
- HTTP/HTTPS: `https://example.com`
- Help topics: `help:topic`
- Vignettes: `vignette:package::topic`

## Values & Data Classes

### .val

Data values, constants, and literals:

```r
n <- 42
cli_text("Found {.val {n}} records")
cli_text("Default timeout is {.val 30} seconds")
cli_text("Status: {.val 'complete'}")
```

**Automatic formatting:**
- Quoted for character values
- Unquoted for numeric values
- Handles vectors with collapsing

### .var

Variable names in code or data:

```r
cli_abort("Variable {.var x} must be numeric")
cli_text("Column {.var age} contains missing values")
cli_inform("Using {.var Sepal.Length} as predictor")
```

**When to use:**
- Variable names in R code
- Column names in data frames
- Field names in objects

### .envvar

Environment variable names:

```r
cli_text("Set {.envvar R_LIBS_USER} to customize library location")
cli_abort("{.envvar HOME} is not defined")
cli_inform("Using {.envvar PATH}: {.val {Sys.getenv('PATH')}}")
```

**When to use:**
- System environment variables
- R-specific environment variables
- Configuration via environment

### .field

Object fields, slots, or attributes:

```r
cli_text("The {.field name} field is required")
cli_abort("Invalid {.field status} value")
cli_text("Access {.field @data} slot in S4 object")
```

**When to use:**
- Named list elements
- Data frame columns (prefer `.var` for analysis context)
- S4 slots
- Object attributes

### .str

String literals and text values:

```r
cli_text("Message starts with {.str 'Error:'}")
cli_text("Pattern {.str '^[0-9]+$'} matches digits")
```

**When to use:**
- Literal string values
- Pattern strings
- Format strings
- When `.val` formatting is too generic

## Emphasis Classes

### .emph

Emphasis for important concepts or terms:

```r
cli_text("This function is {.emph deprecated}")
cli_text("The file is {.emph locked} by another process")
cli_inform("{.emph Note}: This may take several minutes")
```

**Rendering:**
- Typically italic or colored
- Lighter emphasis than `.strong`

### .strong

Strong emphasis for critical information:

```r
cli_warn("{.strong Warning}: This action cannot be undone")
cli_text("This parameter is {.strong required}")
cli_abort("{.strong Error}: Database connection failed")
```

**Rendering:**
- Typically bold or brightly colored
- Stronger emphasis than `.emph`

## Documentation Classes

### .help

R help topic references:

```r
cli_text("See {.help stats::lm} for details")
cli_inform("More info: {.help base::sum}")
```

**Features:**
- Creates link to help topic in RStudio
- Supports `package::topic` notation
- Fallback to plain text in terminals

### .topic

Generic topic or section references:

```r
cli_text("See {.topic 'Error Handling'} section")
cli_inform("Refer to {.topic 'Advanced Usage'}")
```

**When to use:**
- Internal documentation sections
- Vignette sections
- General topic references

### .vignette

Vignette references:

```r
cli_text("Read {.vignette cli::semantic-cli} for examples")
cli_inform("See {.vignette dplyr::programming}")
```

**Features:**
- Links to package vignettes
- Format: `package::vignette-name`

### .run

Runnable R code examples:

```r
cli_text("Try: {.run install.packages('cli')}")
cli_inform("Debug with: {.run options(error = recover)}")
```

**Features:**
- Creates executable link in RStudio
- Click to run code in console
- Formatted as code in terminals

## Special Classes

### .kbd

Keyboard keys and shortcuts:

```r
cli_text("Press {.kbd Ctrl+C} to cancel")
cli_text("Use {.kbd Enter} to confirm")
cli_inform("Save with {.kbd Cmd+S} (Mac) or {.kbd Ctrl+S} (Windows)")
```

**Rendering:**
- Typically in keyboard key style
- May show as boxed or distinct formatting

### .key

Alternative to `.kbd` for key names:

```r
cli_text("Press the {.key RETURN} key")
cli_text("Hold {.key SHIFT} while clicking")
```

### .or

Logical OR separator for alternatives:

```r
cli_text("Use {.val 'yes'} {.or} {.val 'no'}")
cli_abort("Type must be {.val 'auto'} {.or} {.val 'manual'}")
```

**Rendering:**
- Formats as " or " with appropriate styling
- Maintains class formatting for surrounding elements

### .pkg

Package names:

```r
cli_text("Install {.pkg dplyr} for data manipulation")
cli_inform("Loading {.pkg ggplot2}")
cli_abort("{.pkg httr2} is required but not installed")
```

**Features:**
- Distinct package name formatting
- May include CRAN/GitHub links in supported environments

### .dt

Definition term in definition lists:

```r
cli_dl(c(
  "{.dt name}" = "User's full name",
  "{.dt email}" = "Contact email address"
))
```

**When to use:**
- Definition list terms
- Glossary entries
- Key-value pair keys

### .dd

Definition description in definition lists:

```r
cli_dl(c(
  "name" = "{.dd User's full name}",
  "email" = "{.dd Contact email address}"
))
```

**When to use:**
- Definition list descriptions
- Glossary definitions
- Key-value pair values

## Vector Collapsing

Vectors are automatically collapsed with appropriate separators:

### Default Behavior

```r
pkgs <- c("dplyr", "tidyr", "ggplot2")
cli_text("Loading packages: {.pkg {pkgs}}")
#> Loading packages: dplyr, tidyr, and ggplot2

files <- c("a.R", "b.R")
cli_text("Modified: {.file {files}}")
#> Modified: a.R and b.R

single <- "data.csv"
cli_text("Found: {.file {single}}")
#> Found: data.csv
```

**Rules:**
- Length 1: no separators
- Length 2: " and " separator
- Length 3+: ", " separators with " and " before last item

### Collapsing Empty Vectors

```r
empty <- character()
cli_text("Files: {.file {empty}}")
#> Files:

cli_text("Files: {?none/one/some}: {.file {empty}}")
#> Files: none:
```

### Custom Collapse Separators

Control collapsing with glue transformers:

```r
items <- c("apple", "banana", "cherry")

# Custom separator
cli_text("Items: {.val {items}}", .transformer = function(text, envir) {
  glue::glue_collapse(text, sep = " | ", last = " | ")
})
#> Items: 'apple' | 'banana' | 'cherry'

# OR separator
cli_text("Choose: {.val {items}}", .transformer = function(text, envir) {
  glue::glue_collapse(text, sep = ", ", last = " or ")
})
#> Choose: 'apple', 'banana' or 'cherry'
```

### Truncating Long Vectors

```r
many <- letters[1:20]

cli_text("Variables: {.var {many}}")
#> Variables: a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, and t

# Truncate with custom transformer
cli_text("Variables: {.var {head(many, 5)}} and {length(many) - 5} more")
#> Variables: a, b, c, d, e and 15 more
```

## Advanced Patterns

### Nested Markup

Classes can be nested for combined formatting:

```r
cli_text("Call {.fn {.pkg dplyr}::filter} to subset data")
cli_abort("File {.file {.path {dir}}/data.csv} not found")
cli_text("Set {.arg timeout} to {.val {default_timeout}} by default")
```

**Nesting guidelines:**
- Outer class determines primary formatting
- Inner classes add semantic meaning
- Keep nesting depth reasonable (2-3 levels max)

### Combining with Glue Expressions

```r
n <- 5
cli_text("Processing {n} file{?s} from {.path {getwd()}}")

status <- "complete"
cli_inform("Status: {.val {toupper(status)}}")

pkg <- "dplyr"
cli_text("Version: {.pkg {pkg}} {.val {packageVersion(pkg)}}")
```

### Custom Glue Transformers

Full control over formatting with transformers:

```r
# Highlight differences
cli_text(
  "Expected {.val {expected}}, got {.val {actual}}",
  .transformer = function(text, envir) {
    # Custom logic here
    text
  }
)

# Add prefixes
my_transformer <- function(text, envir) {
  if (startsWith(text, ".pkg")) {
    paste0("R package: ", glue::glue(text, .envir = envir))
  } else {
    glue::identity_transformer(text, envir)
  }
}

cli_text("Install {.pkg cli}", .transformer = my_transformer)
```

### Conditional Formatting

```r
status <- "error"
cli_text("Status: {.{if(status == 'error') 'strong' else 'emph'} {status}}")

type <- class(x)
cli_text("Type: {if(is.numeric(x)) .val else .cls} {type}")
```

### Multiple Classes on Same Content

Combine semantic classes:

```r
# Package function
cli_text("{.fn {.pkg stats}::median}")

# File in path
cli_text("{.file {.path /usr/local}/script.R}")

# Variable value
cli_text("{.var x} = {.val {x}}")
```

### Working with Lists

```r
config <- list(host = "localhost", port = 8080, ssl = TRUE)

cli_dl(c(
  "{.field host}" = "{.val {config$host}}",
  "{.field port}" = "{.val {config$port}}",
  "{.field ssl}" = "{.val {config$ssl}}"
))
```

### Escaping Markup

Prevent interpretation with double braces:

```r
cli_text("In glue, use {{variable}} syntax")
#> In glue, use {variable} syntax

cli_text("Literal: {{.code not_markup}}")
#> Literal: {.code not_markup}
```

## Pluralization

Pluralization adapts text based on quantities using `{?}` syntax.

### Single Alternative Pattern

Add "s" for plural:

```r
n <- 1
cli_text("{n} file{?s} found")
#> 1 file found

n <- 5
cli_text("{n} file{?s} found")
#> 5 files found
```

### Two Alternative Pattern

Specify singular/plural forms:

```r
n <- 1
cli_text("{n} director{?y/ies}")
#> 1 directory

n <- 3
cli_text("{n} director{?y/ies}")
#> 3 directories
```

**Common patterns:**
- `{?y/ies}` - directory/directories
- `{?/s}` - item/items
- `{?is/are}` - is/are
- `{?/es}` - box/boxes
- `{?ex/ices}` - index/indices

### Three Alternative Pattern

Handle zero/one/many:

```r
n <- 0
cli_text("{?No/One/Some} file{?s} {?is/is/are} ready")
#> No files are ready

n <- 1
cli_text("{?No/One/Some} file{?s} {?is/is/are} ready")
#> One file is ready

n <- 5
cli_text("{?No/One/Some} file{?s} {?is/is/are} ready")
#> Some files are ready
```

### Setting Quantity with qty()

Control pluralization explicitly:

```r
updated <- 3
total <- 10
cli_text("{updated}/{total} {qty(updated)} file{?s} {?needs/need} update{?s}")
#> 3/10 files need updates
```

**When to use qty():**
- When quantity appears elsewhere
- Complex expressions with multiple numbers
- Explicit pluralization control

### no() Helper

Display "no" instead of 0:

```r
n <- 0
cli_text("Found {no(n)} error{?s}")
#> Found no errors

n <- 3
cli_text("Found {no(n)} error{?s}")
#> Found 3 errors
```

### Advanced Pluralization Patterns

**Multiple quantities in one message:**

```r
nerr <- 2
nwarn <- 1
cli_text(
  "{nerr} error{?s} and {nwarn} {qty(nwarn)} warning{?s} found"
)
#> 2 errors and 1 warning found
```

**Conditional articles:**

```r
n <- 1
cli_text("Found {?a /}{n} file{?s}")
#> Found a 1 file

n <- 5
cli_text("Found {?a /}{n} file{?s}")
#> Found 5 files
```

**Complex pluralization:**

```r
nfile <- 3
ndir <- 1
cli_text(
  "{nfile} file{?s} in {ndir} {qty(ndir)} director{?y/ies}"
)
#> 3 files in 1 directory
```

**Verb agreement:**

```r
n <- 1
cli_text("File {?was/were} modified")
#> File was modified

n <- 3
cli_text("Files {?was/were} modified")
#> Files were modified
```

**Possessives:**

```r
n <- 1
cli_text("User{?'s/'s'} setting{?s}")
#> User's setting

n <- 3
cli_text("Users{?'s/'s'} settings")
#> Users' settings
```

## Performance Considerations

### High-Frequency Messages

For loops with many iterations:

```r
# Expensive - creates cli context each iteration
for (i in 1:10000) {
  cli_text("Processing {.val {i}}")
}

# Better - batch messages
if (i %% 1000 == 0) {
  cli_text("Processed {.val {i}} items")
}

# Best - use progress bar
cli_progress_bar("Processing", total = 10000)
for (i in 1:10000) {
  # work here
  cli_progress_update()
}
```

### Expensive Interpolation

Avoid expensive computations in markup:

```r
# Expensive - computes every time
cli_text("Processing {.file {slow_path_computation()}}")

# Better - compute once
path <- slow_path_computation()
cli_text("Processing {.file {path}}")
```

### Conditional Messages

Use conditions to avoid unnecessary formatting:

```r
# Inefficient
if (verbose) cli_text("Status: {.val {expensive_status_check()}}")

# Better
if (verbose) {
  status <- expensive_status_check()
  cli_text("Status: {.val {status}}")
}
```

### Large Vectors

Truncate large vectors before formatting:

```r
# Problematic with huge vectors
vars <- names(huge_dataframe)
cli_text("Variables: {.var {vars}}")

# Better
n_vars <- length(vars)
if (n_vars > 10) {
  cli_text("Variables: {.var {head(vars, 10)}} and {n_vars - 10} more")
} else {
  cli_text("Variables: {.var {vars}}")
}
```

## Quick Reference Table

| Class | Use For | Example | Output |
|-------|---------|---------|--------|
| `.code` | Code expressions | `{.code sum(x)}` | `sum(x)` |
| `.fn`, `.fun` | Functions | `{.fn mean}` | `mean()` |
| `.arg` | Function arguments | `{.arg na.rm}` | `na.rm` |
| `.cls` | Class names | `{.cls data.frame}` | data.frame |
| `.type` | Base types | `{.type integer}` | integer |
| `.obj_type_friendly` | Friendly types | `{.obj_type_friendly {x}}` | an integer vector |
| `.file` | File names | `{.file script.R}` | script.R |
| `.path` | Directory paths | `{.path /usr/local}` | /usr/local |
| `.email` | Email addresses | `{.email user@example.com}` | user@example.com |
| `.url` | Web URLs | `{.url https://example.com}` | https://example.com |
| `.href` | Custom links | `{.href [text](url)}` | text (linked) |
| `.val` | Data values | `{.val {x}}` | 42 or 'text' |
| `.var` | Variable names | `{.var column}` | column |
| `.envvar` | Environment vars | `{.envvar PATH}` | PATH |
| `.field` | Object fields | `{.field name}` | name |
| `.str` | String literals | `{.str 'pattern'}` | 'pattern' |
| `.emph` | Emphasis | `{.emph important}` | *important* |
| `.strong` | Strong emphasis | `{.strong critical}` | **critical** |
| `.help` | Help topics | `{.help stats::lm}` | stats::lm (linked) |
| `.topic` | Topic references | `{.topic 'Intro'}` | 'Intro' |
| `.vignette` | Vignettes | `{.vignette pkg::name}` | pkg::name (linked) |
| `.run` | Runnable code | `{.run code}` | code (executable) |
| `.kbd`, `.key` | Keyboard keys | `{.kbd Ctrl+C}` | Ctrl+C |
| `.or` | Logical OR | `{.val x} {.or} {.val y}` | x or y |
| `.pkg` | Package names | `{.pkg dplyr}` | dplyr |
| `.dt` | Definition term | `{.dt term}` | term (in definition list) |
| `.dd` | Definition desc | `{.dd description}` | description (in definition list) |
