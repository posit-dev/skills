# Progress Indicators

## Table of Contents

1. [Choosing Progress Style](#choosing-progress-style)
2. [cli_progress_bar() Deep Dive](#cli_progress_bar-deep-dive)
3. [cli_progress_step() Advanced](#cli_progress_step-advanced)
4. [cli_progress_message()](#cli_progress_message)
5. [Progress Variables Reference](#progress-variables-reference)
6. [Format Strings](#format-strings)
7. [Progress Styles](#progress-styles)
8. [Advanced Scenarios](#advanced-scenarios)
9. [Shiny Integration](#shiny-integration)
10. [C-Level Progress](#c-level-progress)
11. [Debugging Progress](#debugging-progress)
12. [Performance Considerations](#performance-considerations)

## Choosing Progress Style

cli offers three progress indicator functions, each suited for different scenarios:

### cli_progress_bar()

Use when:
- You know the total number of iterations upfront
- Progress can be measured as a percentage
- Operation involves loops or iterating over collections
- Users need ETA and completion estimates

```r
# Good use case
process_files <- function(files) {
  cli_progress_bar("Processing", total = length(files))
  for (file in files) {
    process(file)
    cli_progress_update()
  }
}
```

### cli_progress_step()

Use when:
- Progress happens in discrete named steps
- Total work is unknown or variable
- Steps have different durations
- You want automatic success/failure indicators

```r
# Good use case
deploy_app <- function() {
  cli_progress_step("Building assets")
  build_assets()

  cli_progress_step("Running tests")
  run_tests()

  cli_progress_step("Deploying to server")
  deploy()
}
```

### cli_progress_message()

Use when:
- Showing a simple status message
- No quantifiable progress to track
- Operation duration is uncertain
- Want a spinner without step semantics

```r
# Good use case
cli_progress_message("Waiting for API response...")
response <- long_running_api_call()
```

## cli_progress_bar() Deep Dive

### Basic Parameters

```r
cli_progress_bar(
  name = NULL,           # Progress bar name/label
  status = NULL,         # Additional status text
  type = "iterator",     # Bar type: "iterator", "tasks", "download", "custom"
  total = NA,            # Total number of items (NA for unknown)
  format = NULL,         # Custom format string
  format_done = NULL,    # Format when complete
  format_failed = NULL,  # Format when failed
  clear = TRUE,          # Clear bar when done
  current = TRUE,        # Show current position
  auto_terminate = TRUE, # Auto-close when function exits
  .auto_close = TRUE     # Deprecated, use auto_terminate
)
```

### Type Parameter Examples

```r
# Iterator (default) - for loops
cli_progress_bar("Processing items", total = 100, type = "iterator")

# Tasks - for discrete tasks
cli_progress_bar("Completing tasks", total = 5, type = "tasks")

# Download - for file downloads
cli_progress_bar("Downloading", total = file_size, type = "download")

# Custom - for user-defined formats
cli_progress_bar(
  format = "Working {cli::pb_bar} {cli::pb_percent}",
  total = 100,
  type = "custom"
)
```

### Auto-Termination Behavior

Progress bars automatically close when the calling function exits:

```r
process_data <- function(data) {
  cli_progress_bar("Processing", total = nrow(data))

  for (i in seq_len(nrow(data))) {
    process_row(data[i, ])
    cli_progress_update()
  }

  # Bar automatically closes here when function returns
}

# Manual control if needed
process_data_manual <- function(data) {
  id <- cli_progress_bar("Processing", total = nrow(data))

  for (i in seq_len(nrow(data))) {
    process_row(data[i, ])
    cli_progress_update(id = id)
  }

  cli_progress_done(id = id)  # Explicit close
}
```

### Clearing Behavior

Control whether progress bars remain visible after completion:

```r
# Clear after completion (default)
cli_progress_bar("Working", total = 100, clear = TRUE)
for (i in 1:100) {
  Sys.sleep(0.01)
  cli_progress_update()
}
# Bar disappears when done

# Keep visible after completion
cli_progress_bar("Working", total = 100, clear = FALSE)
for (i in 1:100) {
  Sys.sleep(0.01)
  cli_progress_update()
}
# Bar remains showing 100% completion
```

### Dynamic Updates

Update progress with optional status messages:

```r
process_files <- function(files) {
  cli_progress_bar("Processing files", total = length(files))

  for (i in seq_along(files)) {
    file <- files[[i]]

    # Update with status
    cli_progress_update(
      status = sprintf("Current: %s", basename(file))
    )

    process_file(file)
  }
}

# Update multiple items at once
cli_progress_update(inc = 5)  # Increment by 5
cli_progress_update(set = 50) # Set to specific value
```

## Format Strings

### Default Formats

```r
# Iterator format (default)
# "{cli::pb_spin} {cli::pb_name} {cli::pb_bar} {cli::pb_percent} | ETA: {cli::pb_eta}"

# Download format
# "Downloaded {cli::pb_current_bytes}/{cli::pb_total_bytes} ({cli::pb_rate_bytes}/s) | ETA: {cli::pb_eta}"

# Tasks format
# "{cli::pb_name} {cli::pb_current}/{cli::pb_total} | ETA: {cli::pb_eta}"
```

### Custom Format Examples

```r
# Simple percentage only
cli_progress_bar(
  "Working",
  total = 100,
  format = "{cli::pb_name} {cli::pb_percent}"
)

# With ETA and rate
cli_progress_bar(
  "Processing",
  total = 1000,
  format = "{cli::pb_bar} {cli::pb_current}/{cli::pb_total} [{cli::pb_eta} @ {cli::pb_rate}]"
)

# With elapsed time
cli_progress_bar(
  "Running",
  total = 50,
  format = "{cli::pb_spin} {cli::pb_name} {cli::pb_percent} | Elapsed: {cli::pb_elapsed}"
)

# Download-style with bytes
cli_progress_bar(
  "Downloading data.zip",
  total = 1024^3,  # 1 GB
  format = paste0(
    "{cli::pb_current_bytes}/{cli::pb_total_bytes} ",
    "({cli::pb_percent}) | ",
    "{cli::pb_rate_bytes}/s | ",
    "ETA: {cli::pb_eta}"
  )
)

# Custom status display
cli_progress_bar(
  format = "{cli::pb_bar} {cli::pb_status}"
)
```

### Completion and Failure Formats

```r
cli_progress_bar(
  "Processing",
  total = 100,
  format = "Working: {cli::pb_bar} {cli::pb_percent}",
  format_done = "Completed {cli::pb_total} items in {cli::pb_elapsed}",
  format_failed = "Failed after processing {cli::pb_current} items"
)

# Trigger failure
for (i in 1:50) {
  if (i == 30) {
    cli_progress_done(result = "failed")
    break
  }
  cli_progress_update()
}
```

## Progress Variables Reference

### Basic Progress Variables

```r
# Current position
cli::pb_current       # Current iteration number (e.g., 45)

# Total work
cli::pb_total         # Total iterations (e.g., 100)

# Percentage
cli::pb_percent       # Completion percentage (e.g., "45%")

# Visual bar
cli::pb_bar           # Progress bar visualization (e.g., "=========>    ")

# Spinner
cli::pb_spin          # Animated spinner character

# Name and status
cli::pb_name          # Progress bar name
cli::pb_status        # Current status message
```

### Timing Variables

```r
# Time elapsed
cli::pb_elapsed       # Time since start (e.g., "2m 30s")
cli::pb_elapsed_raw   # Elapsed time in seconds (e.g., 150.234)
cli::pb_elapsed_clock # Clock time format (e.g., "02:30")

# Time remaining
cli::pb_eta           # Estimated time remaining (e.g., "1m 15s")
cli::pb_eta_raw       # ETA in seconds (e.g., 75.0)
cli::pb_eta_str       # ETA as string (e.g., "ETA: 1m 15s")

# Rate
cli::pb_rate          # Items per second (e.g., "0.6/s")
cli::pb_rate_raw      # Raw rate value (e.g., 0.6)
```

### Byte-Based Variables

For download/upload progress bars:

```r
# Current bytes
cli::pb_current_bytes # Formatted current (e.g., "45.2 MB")

# Total bytes
cli::pb_total_bytes   # Formatted total (e.g., "100 MB")

# Rate
cli::pb_rate_bytes    # Bytes per second (e.g., "2.1 MB/s")
```

### Advanced Variables

```r
# Tick information
cli::pb_tick          # Current tick number
cli::pb_tick_rate     # Ticks per second

# Timestamps
cli::pb_start         # Start timestamp (POSIXct)
cli::pb_timestamp     # Current timestamp (POSIXct)

# Extra data
cli::pb_extra         # User-defined extra data
```

## cli_progress_step() Advanced

### Basic Usage

```r
deploy_package <- function() {
  cli_progress_step("Checking package")
  check_result <- check_package()

  cli_progress_step("Building package")
  build_result <- build_package()

  cli_progress_step("Uploading to CRAN")
  upload_result <- upload_package()
}
```

### Spinner Customization

```r
# Use different spinner style
options(cli.spinner = "dots")
cli_progress_step("Processing")

# Available spinners
options(cli.spinner = "line")      # Classic line spinner
options(cli.spinner = "dots")      # Dots
options(cli.spinner = "dots2")     # Alternative dots
options(cli.spinner = "dots3")     # More dots
options(cli.spinner = "dots12")    # 12-frame dots
options(cli.spinner = "arrow")     # Rotating arrow
options(cli.spinner = "bouncingBar") # Bouncing bar
options(cli.spinner = "clock")     # Clock hands

# Custom spinner frames
options(cli.spinner = list(
  interval = 100,
  frames = c("◐", "◓", "◑", "◒")
))
```

### Multiple Concurrent Steps

Progress steps can be nested:

```r
process_projects <- function(projects) {
  cli_progress_step("Processing {length(projects)} projects")

  for (proj in projects) {
    cli_progress_step("Building {proj}")
    build_project(proj)

    cli_progress_step("Testing {proj}")
    test_project(proj)

    cli_progress_step("Deploying {proj}")
    deploy_project(proj)
  }
}
```

### Dynamic Message Updates

Update step messages while they're running:

```r
process_with_details <- function(files) {
  id <- cli_progress_step("Processing files")

  for (i in seq_along(files)) {
    cli_progress_update(
      id = id,
      status = sprintf("File %d/%d: %s", i, length(files), basename(files[i]))
    )

    process_file(files[i])
  }

  cli_progress_done(id = id)
}
```

### Success/Failure Termination

```r
deploy_with_status <- function() {
  tryCatch({
    cli_progress_step("Building application")
    build_app()

    cli_progress_step("Running tests")
    test_result <- run_tests()

    if (!test_result$passed) {
      cli_progress_done(result = "failed", msg_failed = "Tests failed!")
      return(FALSE)
    }

    cli_progress_step("Deploying")
    deploy()

    cli_progress_done(result = "done", msg_done = "Deployment successful!")
    TRUE

  }, error = function(e) {
    cli_progress_done(result = "failed", msg_failed = "Deployment failed: {e$message}")
    FALSE
  })
}
```

### Custom Success/Failure Messages

```r
id <- cli_progress_step(
  "Processing data",
  msg_done = "Data processed successfully",
  msg_failed = "Data processing failed"
)

# Mark as done
cli_progress_done(id = id, result = "done")

# Or mark as failed
cli_progress_done(id = id, result = "failed")
```

## cli_progress_message()

Simple progress messages with automatic spinners:

```r
# Basic usage
cli_progress_message("Loading configuration...")
config <- load_config()

# With explicit cleanup
id <- cli_progress_message("Waiting for server...")
wait_for_server()
cli_progress_done(id = id)

# Updating message
id <- cli_progress_message("Connecting...")
cli_progress_update(id = id, status = "Authenticating...")
cli_progress_update(id = id, status = "Connected!")
cli_progress_done(id = id)
```

## Progress Styles

cli includes several built-in progress bar styles:

```r
# Classic style (default)
options(cli.progress_bar_style = "classic")

# Unicode style (requires Unicode support)
options(cli.progress_bar_style = "unicode")

# ASCII style (for limited terminals)
options(cli.progress_bar_style = "ascii")

# Custom style
options(cli.progress_bar_style = list(
  complete = "=",
  incomplete = " ",
  current = ">",
  width = 40
))
```

## Advanced Scenarios

### Nested Progress Bars

```r
process_datasets <- function(datasets) {
  cli_progress_bar("Processing datasets", total = length(datasets))

  for (dataset in datasets) {
    # Outer progress updates
    cli_progress_update()

    # Inner progress bar
    n_rows <- nrow(dataset)
    cli_progress_bar("Processing rows", total = n_rows)

    for (i in seq_len(n_rows)) {
      process_row(dataset[i, ])
      cli_progress_update()  # Updates inner bar
    }
    # Inner bar auto-closes
  }
  # Outer bar auto-closes
}
```

### Progress with Parallel Code

Progress bars in parallel contexts require special handling:

```r
library(foreach)
library(doParallel)

# Not recommended - doesn't work well
process_parallel_bad <- function(items) {
  cli_progress_bar("Processing", total = length(items))

  foreach(item = items) %dopar% {
    result <- process_item(item)
    cli_progress_update()  # Won't work across processes
    result
  }
}

# Better approach - update after each completion
process_parallel_better <- function(items) {
  cli_progress_bar("Processing", total = length(items))

  results <- foreach(item = items) %dopar% {
    process_item(item)
  }

  # Update in main thread
  for (i in seq_along(results)) {
    cli_progress_update()
  }

  results
}

# Best approach - use progress updates between parallel batches
process_parallel_best <- function(items, batch_size = 10) {
  batches <- split(items, ceiling(seq_along(items) / batch_size))
  cli_progress_bar("Processing", total = length(items))

  results <- list()
  for (batch in batches) {
    batch_results <- foreach(item = batch) %dopar% {
      process_item(item)
    }
    results <- c(results, batch_results)
    cli_progress_update(inc = length(batch))
  }

  results
}
```

### Progress in Loops vs Mapping

```r
# Traditional loop with progress
process_loop <- function(items) {
  cli_progress_bar("Processing", total = length(items))

  results <- vector("list", length(items))
  for (i in seq_along(items)) {
    results[[i]] <- process_item(items[[i]])
    cli_progress_update()
  }

  results
}

# Using cli_progress_along()
process_along <- function(items) {
  results <- lapply(cli_progress_along(items, "Processing"), function(i) {
    process_item(items[[i]])
  })

  results
}

# Using purrr with progress
library(purrr)
process_purrr <- function(items) {
  cli_progress_bar("Processing", total = length(items))

  map(items, function(item) {
    result <- process_item(item)
    cli_progress_update()
    result
  })
}
```

### Progress Output vs Regular CLI Output

Progress bars interact with other cli output:

```r
process_with_messages <- function(items) {
  cli_progress_bar("Processing", total = length(items))

  for (i in seq_along(items)) {
    result <- process_item(items[[i]])

    # Regular cli messages work alongside progress
    if (result$warnings) {
      cli_alert_warning("Item {i} had warnings")
    }

    cli_progress_update()
  }

  cli_alert_success("Processing complete")
}

# Progress-aware output functions
process_with_progress_output <- function(items) {
  cli_progress_bar("Processing", total = length(items))

  for (item in items) {
    # These respect progress bars
    cli_progress_output(cli_text("Processing {item}"))
    process_item(item)
    cli_progress_update()
  }
}
```

### Unknown Total

Progress bars can run without knowing the total:

```r
process_stream <- function(conn) {
  cli_progress_bar("Processing stream", total = NA)

  while (length(line <- readLines(conn, n = 1)) > 0) {
    process_line(line)
    cli_progress_update()
  }

  # Shows spinner and count, no percentage
}

# Update total when it becomes known
process_dynamic <- function() {
  cli_progress_bar("Discovering files", total = NA)

  files <- find_files()

  # Update total
  cli_progress_update(total = length(files))

  for (file in files) {
    process_file(file)
    cli_progress_update()
  }
}
```

## Shiny Integration

Progress indicators in Shiny applications require special consideration:

```r
library(shiny)

ui <- fluidPage(
  actionButton("process", "Process Data")
)

server <- function(input, output, session) {
  observeEvent(input$process, {
    # Use Shiny's progress API
    withProgress(message = "Processing", {

      # cli progress works but won't show in Shiny UI
      cli_progress_bar("Internal progress", total = 100)

      for (i in 1:100) {
        Sys.sleep(0.01)

        # Update Shiny progress
        incProgress(1/100)

        # cli progress (for logs)
        cli_progress_update()
      }
    })
  })
}

# Better: Use cli in Shiny with proper output
server <- function(input, output, session) {
  observeEvent(input$process, {
    # Redirect cli output to console
    withProgress(message = "Processing", {
      # cli progress shows in R console, not Shiny UI
      process_data()
    })
  })
}
```

## C-Level Progress

For package developers using C/C++:

```r
# In R
process_with_c <- function(data) {
  cli_progress_bar("Processing in C", total = nrow(data))
  .Call(C_process_data, data, environment())
}

# In C code (using cli's C API)
# #include <cli/progress.h>
#
# SEXP C_process_data(SEXP data, SEXP progress_env) {
#   R_xlen_t n = Rf_xlength(data);
#
#   for (R_xlen_t i = 0; i < n; i++) {
#     // Process data[i]
#
#     // Update progress from C
#     cli_progress_update(progress_env);
#   }
#
#   return R_NilValue;
# }
```

Note: C-level progress requires the cli package C headers and proper linking.

## Debugging Progress

### Common Issues

```r
# Issue: Progress bar not updating
# Problem: Not calling cli_progress_update()
for (i in 1:100) {
  process(i)
  # Missing: cli_progress_update()
}

# Issue: Multiple progress bars interfering
# Solution: Store IDs and update correct bar
id1 <- cli_progress_bar("Task 1", total = 10)
id2 <- cli_progress_bar("Task 2", total = 20)

cli_progress_update(id = id1)
cli_progress_update(id = id2)

# Issue: Progress bar not visible
# Check: Is stderr redirected? Is output captured?
# Progress bars use stderr by default

# Issue: Progress bar flickers
# Problem: Output mixing with progress
# Solution: Use cli_progress_output()
cli_progress_output(cli_alert_info("Status update"))
```

### Testing Progress Bars

```r
test_that("progress bar updates correctly", {
  # Mock progress to test without output
  mockery::stub(my_function, "cli_progress_bar", NULL)
  mockery::stub(my_function, "cli_progress_update", NULL)

  result <- my_function()
  expect_true(result)
})

# Test with captured output
test_that("progress messages are correct", {
  output <- capture.output({
    process_data(test_data)
  })

  # Note: Progress bars may not appear in captured output
  # Consider testing function logic separately
})
```

### Disabling Progress

```r
# Disable all progress indicators
options(cli.progress_show_after = Inf)

# Or use show_after parameter
cli_progress_bar("Working", total = 100, show_after = Inf)

# Conditional progress
process_data <- function(data, verbose = TRUE) {
  if (verbose) {
    cli_progress_bar("Processing", total = nrow(data))
  }

  for (i in seq_len(nrow(data))) {
    process_row(data[i, ])
    if (verbose) cli_progress_update()
  }
}
```

## Performance Considerations

### Update Frequency

```r
# Bad: Update too frequently (slows down loop)
for (i in 1:1e6) {
  fast_operation(i)
  cli_progress_update()  # 1 million updates!
}

# Better: Update periodically
cli_progress_bar("Processing", total = 1e6)
for (i in 1:1e6) {
  fast_operation(i)
  if (i %% 1000 == 0) cli_progress_update(set = i)
}

# Best: Use show_after to delay display
cli_progress_bar(
  "Processing",
  total = 1e6,
  show_after = 2  # Only show if takes >2 seconds
)
```

### Overhead

Progress bars add minimal overhead, but consider:

```r
# Negligible overhead for slow operations
process_files <- function(files) {
  cli_progress_bar("Processing", total = length(files))
  for (file in files) {
    slow_operation(file)  # 1 second per file
    cli_progress_update()  # <1ms overhead
  }
}

# Noticeable overhead for fast operations
process_numbers <- function(n = 1e6) {
  cli_progress_bar("Processing", total = n)
  for (i in 1:n) {
    fast_operation(i)  # 1μs per operation
    cli_progress_update()  # 1ms overhead - 1000x slower!
  }
}

# Solution: Batch updates
process_numbers_fast <- function(n = 1e6, update_every = 1000) {
  cli_progress_bar("Processing", total = n)
  for (i in 1:n) {
    fast_operation(i)
    if (i %% update_every == 0) {
      cli_progress_update(set = i)
    }
  }
}
```

### Terminal Performance

```r
# Progress bars can be slow on Windows
# Use ASCII style for better performance
if (.Platform$OS.type == "windows") {
  options(cli.progress_bar_style = "ascii")
}

# Disable Unicode for remote sessions
if (Sys.getenv("SSH_CONNECTION") != "") {
  options(cli.unicode = FALSE)
}
```
