# CLI Conditions Reference

## Table of Contents

1. [CLI Conditions Overview](#cli-conditions-overview)
2. [Error Design Principles](#error-design-principles)
3. [cli_abort() Deep Dive](#cli_abort-deep-dive)
4. [cli_warn() Patterns](#cli_warn-patterns)
5. [cli_inform() Patterns](#cli_inform-patterns)
6. [Testing CLI Conditions](#testing-cli-conditions)
7. [Migration Guide](#migration-guide)
8. [Real-World Examples](#real-world-examples)
9. [Anti-Patterns](#anti-patterns)

## CLI Conditions Overview

CLI conditions (cli_abort(), cli_warn(), cli_inform()) provide formatted alternatives to base R's stop(), warning(), and message(). They offer:

**Key Benefits:**

- **Inline markup** - Format code, paths, variables, and values with semantic meaning
- **Structured output** - Use bullet lists to organize problem statements, context, and solutions
- **Automatic styling** - Colors, icons, and formatting are applied consistently
- **Better readability** - Multi-line messages are easier to scan and understand
- **rlang integration** - Seamless integration with structured error handling via rlang

**When to Use CLI Conditions:**

```r
# Use cli_abort() for errors that stop execution
cli_abort("Cannot proceed: {.file {path}} is missing")

# Use cli_warn() for warnings about potential issues
cli_warn("Column {.field {col}} has {n} missing value{?s}")

# Use cli_inform() for informative messages
cli_inform("Successfully processed {n} record{?s}")
```

## Error Design Principles

Good error messages follow these principles:

### 1. Clear Problem Statement

State what went wrong in plain language:

```r
# Bad - Technical jargon
cli_abort("NULL pointer in slot `data`")

# Good - Clear statement
cli_abort("Dataset is missing")
```

### 2. Actionable Solutions

Tell users how to fix the problem:

```r
validate_email <- function(email) {
  if (!grepl("@", email)) {
    cli_abort(c(
      "Invalid email address",
      "x" = "{.val {email}} is not a valid email",
      "i" = "Email must contain an @ symbol"
    ))
  }
}
```

### 3. Context via Bullet Lists

Use bullets to structure information hierarchically:

```r
check_dimensions <- function(x, y) {
  if (length(x) != length(y)) {
    cli_abort(c(
      "Incompatible vector lengths",
      "x" = "{.arg x} has length {length(x)}",
      "x" = "{.arg y} has length {length(y)}",
      "i" = "Both vectors must have the same length"
    ))
  }
}
```

### 4. Caller Information

Use the `call` argument to show where the error occurred:

```r
# Default - shows the function where cli_abort() is called
validate <- function(x) {
  cli_abort("Invalid input")  # Error in: validate(x)
}

# Explicit - control the call shown in error
validate <- function(x) {
  cli_abort("Invalid input", call = caller_env())
}

# Suppress - don't show any call
validate <- function(x) {
  cli_abort("Invalid input", call = NULL)
}
```

## cli_abort() Deep Dive

### Basic Usage

```r
# Simple message
cli_abort("Something went wrong")

# With inline markup
cli_abort("Cannot find file {.file {path}}")

# With multiple elements
cli_abort(c(
  "Operation failed",
  "i" = "Additional context here"
))
```

### Bullet Types

Each bullet type has semantic meaning and visual styling:

**`"x"` - Error/Problem (red X):**

```r
cli_abort(c(
  "Validation failed",
  "x" = "File {.file data.csv} does not exist",
  "x" = "Directory {.path /tmp/output} is not writable"
))
```

**`"i"` - Information (blue i):**

```r
cli_abort(c(
  "Invalid argument type",
  "x" = "{.arg x} must be numeric",
  "i" = "You supplied a {.cls {class(x)}} object",
  "i" = "Use {.fn as.numeric} to convert"
))
```

**`"v"` - Success context (green checkmark):**

```r
cli_abort(c(
  "Partial operation failure",
  "v" = "Successfully processed {n_success} file{?s}",
  "x" = "Failed to process {n_failed} file{?s}",
  "i" = "See {.file error.log} for details"
))
```

**`"*"` - Bullet point:**

```r
cli_abort(c(
  "Invalid configuration",
  "x" = "Missing required fields in config file",
  "i" = "Required fields:",
  "*" = "{.field name}",
  "*" = "{.field version}",
  "*" = "{.field author}"
))
```

**`">"` - Arrow/Pointer:**

```r
cli_abort(c(
  "Database connection failed",
  "x" = "Cannot connect to {.val {host}}:{.val {port}}",
  "i" = "Troubleshooting steps:",
  ">" = "Check that the server is running",
  ">" = "Verify credentials in {.file .env}",
  ">" = "Ensure firewall allows port {.val {port}}"
))
```

### Named vs Unnamed Elements

**Unnamed elements** are treated as headers or main messages:

```r
cli_abort(c(
  "This is the main error message",
  "This is a second header line"
))
```

**Named elements** get bullet icons:

```r
cli_abort(c(
  "Main message",
  "x" = "Problem description",
  "i" = "Helpful information"
))
```

### rlang Integration

CLI works seamlessly with rlang's structured error handling:

**Error Classes:**

```r
validate_user <- function(user) {
  if (is.null(user$id)) {
    cli_abort(
      "User ID is required",
      class = "validation_error"
    )
  }
}

# Catch specific error class
tryCatch(
  validate_user(list()),
  validation_error = function(e) {
    # Handle validation errors specifically
  }
)
```

**Parent Errors (Error Chaining):**

```r
load_data <- function(path) {
  tryCatch(
    read.csv(path),
    error = function(e) {
      cli_abort(
        c(
          "Failed to load data",
          "i" = "Attempted to read from {.file {path}}"
        ),
        parent = e
      )
    }
  )
}
```

**Multiple Error Classes:**

```r
cli_abort(
  "Invalid input",
  class = c("invalid_input", "user_error")
)
```

### Call Specification Patterns

**Pattern 1: Default behavior (show internal function):**

```r
helper <- function(x) {
  cli_abort("Invalid x")
}

my_function <- function(x) {
  helper(x)
}

# Error: in `helper()`
my_function(NULL)
```

**Pattern 2: Show caller's context:**

```r
helper <- function(x, call = caller_env()) {
  cli_abort("Invalid x", call = call)
}

my_function <- function(x) {
  helper(x)
}

# Error: in `my_function()`
my_function(NULL)
```

**Pattern 3: Suppress call entirely:**

```r
helper <- function(x) {
  cli_abort("Invalid x", call = NULL)
}

# Error: (no function context shown)
helper(NULL)
```

**Pattern 4: Custom call:**

```r
validate <- function(x) {
  cli_abort("Invalid", call = quote(custom_function()))
}

# Error: in `custom_function()`
```

### Interpolation and Evaluation

CLI evaluates expressions in the calling environment:

```r
check_file <- function(path) {
  size <- file.size(path)

  cli_abort(c(
    "File too large",
    "x" = "{.file {path}} is {size} bytes",
    "i" = "Maximum size is {.val {1e6}} bytes"
  ))
}
```

**Escaping braces:**

```r
# Use double braces to show literal braces
cli_abort("Use {{variable}} syntax in glue")
#> Error: Use {variable} syntax in glue
```

## cli_warn() Patterns

Warnings indicate potential problems that don't stop execution:

### Basic Warnings

```r
# Simple warning
cli_warn("Deprecated function")

# With context
cli_warn(c(
  "Deprecated function",
  "!" = "{.fn old_function} is deprecated",
  "i" = "Use {.fn new_function} instead"
))
```

### Deprecation Warnings

```r
old_function <- function(x) {
  cli_warn(c(
    "{.fn old_function} is deprecated",
    "i" = "Use {.fn new_function} instead",
    "i" = "See {.url https://example.com/migration} for migration guide"
  ))

  # Function implementation
}
```

### Data Quality Warnings

```r
clean_data <- function(data) {
  missing_counts <- sapply(data, function(x) sum(is.na(x)))
  cols_with_missing <- names(missing_counts[missing_counts > 0])

  if (length(cols_with_missing) > 0) {
    cli_warn(c(
      "Missing values detected",
      "!" = "Column{?s} with missing values: {.field {cols_with_missing}}",
      "i" = "Consider using {.fn tidyr::drop_na} or {.fn tidyr::fill}"
    ))
  }

  data
}
```

### Configuration Warnings

```r
load_config <- function(path) {
  config <- read_config(path)

  if (is.null(config$timeout)) {
    cli_warn(c(
      "Missing configuration value",
      "!" = "{.field timeout} not specified in {.file {path}}",
      "i" = "Using default value of {.val 30} seconds"
    ))
    config$timeout <- 30
  }

  config
}
```

### Once Per Session Warnings

```r
experimental_feature <- function() {
  cli_warn(
    c(
      "Experimental feature",
      "!" = "This function is experimental and may change",
      "i" = "Use at your own risk"
    ),
    .frequency = "once",
    .frequency_id = "experimental_feature_warning"
  )

  # Implementation
}
```

## cli_inform() Patterns

Informative messages provide feedback without indicating problems:

### Progress Updates

```r
process_data <- function(data) {
  cli_inform("Starting data processing")

  # Processing steps...

  cli_inform(c(
    "v" = "Successfully processed {nrow(data)} row{?s}",
    "i" = "Output saved to {.file results.csv}"
  ))
}
```

### Startup Messages

```r
.onAttach <- function(libname, pkgname) {
  cli_inform(c(
    "v" = "Loaded {.pkg mypackage} version {packageVersion('mypackage')}",
    "i" = "Use {.fn ?mypackage} for help"
  ))
}
```

### Verbose Mode Information

```r
analyze <- function(data, verbose = TRUE) {
  if (verbose) {
    cli_inform("Analyzing {nrow(data)} observation{?s}")
  }

  result <- expensive_computation(data)

  if (verbose) {
    cli_inform(c(
      "v" = "Analysis complete",
      "i" = "Found {result$n_groups} group{?s}",
      "i" = "Mean value: {.val {round(result$mean, 2)}}"
    ))
  }

  result
}
```

### Informative vs Progress

**Use cli_inform() for:**
- One-time status updates
- Package startup messages
- Final results or summaries
- Debug/verbose output

**Use cli_progress_*() for:**
- Loops or iterations
- Long-running operations
- Operations with known total count
- Real-time progress tracking

```r
# Good - use inform for one-time messages
process <- function(data) {
  cli_inform("Preprocessing data")
  data <- preprocess(data)

  # Good - use progress for iteration
  cli_progress_bar("Processing rows", total = nrow(data))
  for (i in seq_len(nrow(data))) {
    process_row(data[i, ])
    cli_progress_update()
  }

  cli_inform("v" = "Processing complete")
}
```

## Testing CLI Conditions

### Snapshot Testing

Use testthat's snapshot tests to verify condition messages:

```r
test_that("validation errors are clear", {
  expect_snapshot(error = TRUE, {
    validate_email("")
    validate_email("not-an-email")
    validate_email("user@example.com@extra")
  })
})
```

Snapshot file (`tests/testthat/_snaps/validation.md`):

```md
# validation errors are clear

    Code
      validate_email("")
    Error <rlang_error>
      Invalid email address
      x "" is not a valid email
      i Email must contain an @ symbol

    Code
      validate_email("not-an-email")
    Error <rlang_error>
      Invalid email address
      x "not-an-email" is not a valid email
      i Email must contain an @ symbol
```

### Testing Bullet Formatting

```r
test_that("error messages show proper context", {
  expect_snapshot(error = TRUE, {
    check_dimensions(1:3, 1:5)
  })
})
```

### Testing Pluralization

```r
test_that("pluralization works in errors", {
  expect_snapshot(error = TRUE, {
    report_missing(c("file1.txt"))          # singular
    report_missing(c("file1.txt", "file2.txt"))  # plural
  })
})
```

### Testing Warning Frequency

```r
test_that("deprecation warning shown once per session", {
  # Clear warning registry
  assign("last_shown", NULL, envir = rlang::ns_env("cli"))

  # First call shows warning
  expect_warning(old_function(1), "deprecated")

  # Second call does not (with frequency = "once")
  expect_no_warning(old_function(2))
})
```

### Testing Condition Classes

```r
test_that("errors have correct classes", {
  expect_error(
    validate_user(list()),
    class = "validation_error"
  )

  err <- tryCatch(
    validate_user(list()),
    error = function(e) e
  )

  expect_s3_class(err, c("validation_error", "rlang_error"))
})
```

### Mocking for Error Testing

```r
test_that("handles missing file gracefully", {
  local_mocked_bindings(
    file.exists = function(path) FALSE
  )

  expect_snapshot(error = TRUE, {
    load_dataset("missing.csv")
  })
})
```

## Migration Guide

### Base R to CLI: stop() to cli_abort()

**Before:**

```r
validate <- function(x, y) {
  if (!is.numeric(x)) {
    stop("x must be numeric")
  }
  if (length(x) != length(y)) {
    stop("x and y must have the same length")
  }
}
```

**After:**

```r
validate <- function(x, y) {
  if (!is.numeric(x)) {
    cli_abort(c(
      "{.arg x} must be numeric",
      "x" = "You supplied a {.cls {class(x)}} object"
    ))
  }

  if (length(x) != length(y)) {
    cli_abort(c(
      "{.arg x} and {.arg y} must have the same length",
      "x" = "{.arg x} has length {length(x)}",
      "x" = "{.arg y} has length {length(y)}"
    ))
  }
}
```

### Base R to CLI: warning() to cli_warn()

**Before:**

```r
process <- function(data) {
  if (any(is.na(data))) {
    warning("Data contains missing values")
  }
}
```

**After:**

```r
process <- function(data) {
  if (any(is.na(data))) {
    n_missing <- sum(is.na(data))
    cli_warn(c(
      "Data contains missing values",
      "!" = "Found {n_missing} missing value{?s}",
      "i" = "Consider imputation or removal"
    ))
  }
}
```

### Base R to CLI: message() to cli_inform()

**Before:**

```r
load_data <- function(path) {
  message("Loading data from ", path)
  data <- read.csv(path)
  message("Loaded ", nrow(data), " rows")
  data
}
```

**After:**

```r
load_data <- function(path) {
  cli_inform("Loading data from {.file {path}}")
  data <- read.csv(path)
  cli_inform("v" = "Loaded {nrow(data)} row{?s}")
  data
}
```

### sprintf() to Inline Markup

**Before:**

```r
stop(sprintf(
  "File '%s' not found. Expected path: %s",
  basename(path),
  dirname(path)
))
```

**After:**

```r
cli_abort(c(
  "File not found",
  "x" = "Cannot find {.file {basename(path)}}",
  "i" = "Expected location: {.path {dirname(path)}}"
))
```

### paste() Concatenation to Glue Syntax

**Before:**

```r
msg <- paste0(
  "Processing ",
  n,
  " files",
  if (n > 1) "s" else "",
  " from ",
  dirname
)
message(msg)
```

**After:**

```r
cli_inform("Processing {n} file{?s} from {.path {dirname}}")
```

## Real-World Examples

### usethis-Style Error Messages

The usethis package provides excellent examples of clear, actionable errors:

```r
use_github <- function() {
  if (!uses_git()) {
    cli_abort(c(
      "Cannot use GitHub without Git",
      "x" = "This project is not a Git repository",
      "i" = "Use {.fn usethis::use_git} to initialize Git first"
    ))
  }

  if (is.null(github_token())) {
    cli_abort(c(
      "GitHub token not found",
      "x" = "No GitHub personal access token (PAT) found",
      "i" = "Create a token at {.url https://github.com/settings/tokens}",
      "i" = "Store it with {.fn gitcreds::gitcreds_set}"
    ))
  }

  # Implementation
}
```

### devtools-Style Validation

```r
check_package <- function(path = ".") {
  errors <- character()
  warnings <- character()

  # Collect issues
  if (!file.exists(file.path(path, "DESCRIPTION"))) {
    errors <- c(errors, "Missing {.file DESCRIPTION} file")
  }

  if (!file.exists(file.path(path, "NAMESPACE"))) {
    warnings <- c(warnings, "Missing {.file NAMESPACE} file")
  }

  # Report
  if (length(errors) > 0) {
    cli_abort(c(
      "Package structure invalid",
      set_names(errors, rep("x", length(errors))),
      "i" = "Use {.fn usethis::create_package} to create proper structure"
    ))
  }

  if (length(warnings) > 0) {
    cli_warn(c(
      "Package structure issues",
      set_names(warnings, rep("!", length(warnings)))
    ))
  }
}
```

### Database Connection with Rich Context

```r
connect_db <- function(host, port, database, user, password) {
  tryCatch(
    {
      conn <- DBI::dbConnect(
        RPostgres::Postgres(),
        host = host,
        port = port,
        dbname = database,
        user = user,
        password = password
      )

      cli_inform("v" = "Connected to {.field {database}} at {.val {host}}")
      conn
    },
    error = function(e) {
      cli_abort(
        c(
          "Database connection failed",
          "x" = "Cannot connect to {.val {host}}:{.val {port}}",
          "i" = "Connection details:",
          "*" = "Host: {.val {host}}",
          "*" = "Port: {.val {port}}",
          "*" = "Database: {.val {database}}",
          "*" = "User: {.val {user}}",
          "i" = "Troubleshooting:",
          ">" = "Verify server is running",
          ">" = "Check firewall settings",
          ">" = "Confirm credentials"
        ),
        parent = e
      )
    }
  )
}
```

## Anti-Patterns

### Don't Mix Base R and CLI

**Bad:**

```r
validate <- function(x) {
  if (!is.numeric(x)) {
    stop("x must be numeric")  # base R
  }
  if (length(x) == 0) {
    cli_abort("{.arg x} cannot be empty")  # cli
  }
}
```

**Good:**

```r
validate <- function(x) {
  if (!is.numeric(x)) {
    cli_abort("{.arg x} must be numeric")
  }
  if (length(x) == 0) {
    cli_abort("{.arg x} cannot be empty")
  }
}
```

### Don't Overuse Bullets

**Bad - Too many bullets:**

```r
cli_abort(c(
  "Error",
  "x" = "Problem 1",
  "i" = "Info 1",
  "x" = "Problem 2",
  "i" = "Info 2",
  "x" = "Problem 3",
  "i" = "Info 3",
  "x" = "Problem 4"
  # ... too much information
))
```

**Good - Focused message:**

```r
cli_abort(c(
  "Validation failed",
  "x" = "Found {n_errors} error{?s} in configuration",
  "i" = "See {.file validation.log} for details"
))
```

### Don't Repeat Information

**Bad:**

```r
cli_abort(c(
  "File data.csv not found",
  "x" = "Cannot read data.csv",
  "i" = "The file data.csv does not exist"
))
```

**Good:**

```r
cli_abort(c(
  "File not found",
  "x" = "Cannot read {.file data.csv}",
  "i" = "Check that the file exists in the working directory"
))
```

### Don't Use Technical Jargon

**Bad:**

```r
cli_abort("NULL pointer in slot `data` of S4 object")
```

**Good:**

```r
cli_abort(c(
  "Dataset is missing",
  "x" = "The {.field data} slot is empty",
  "i" = "Use {.fn set_data} to provide a dataset"
))
```

### Don't Forget Pluralization

**Bad:**

```r
cli_inform("Found {n} files")  # "Found 1 files" looks wrong
```

**Good:**

```r
cli_inform("Found {n} file{?s}")  # "Found 1 file", "Found 2 files"
```

### Don't Use Bare Errors in Package Code

**Bad:**

```r
# Package function with no context
compute <- function(x) {
  cli_abort("Invalid input")
  # Which function failed? What's invalid?
}
```

**Good:**

```r
compute <- function(x) {
  if (!is.numeric(x)) {
    cli_abort(
      c(
        "{.arg x} must be numeric",
        "x" = "You supplied a {.cls {class(x)}} object"
      ),
      call = caller_env()  # Show caller's context
    )
  }
}
```
