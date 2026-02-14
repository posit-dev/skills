# Toast Notifications in bslib

Toasts are lightweight, temporary notification messages that appear in a corner of the screen. Based on [Bootstrap 5.3's toast component](https://getbootstrap.com/docs/5.3/components/toasts/). Try `shiny::runExample("toast", package = "bslib")` for a complete demo.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Key Parameters](#key-parameters)
- [Showing and Hiding Toasts](#showing-and-hiding-toasts)
- [Common Patterns](#common-patterns)
- [Best Practices](#best-practices)

## Basic Usage

**Simple toast (string shorthand):**
```r
# Server
show_toast("Operation completed!")
```

**Create a toast with `toast()`:**
```r
show_toast(
  toast(
    "Your results are ready to view.",
    header = "Analysis Complete",
    type = "success"
  )
)
```

**Using semantic types** for automatic background coloring:
```r
# Success
toast("Saved successfully.", header = "Success", type = "success")

# Warning
toast("Disk space low.", header = "Warning", type = "warning")

# Error
toast("Failed to connect.", header = "Error", type = "danger")

# Info
toast("New data available.", header = "Info", type = "info")
```

**Structured header with status text:**
```r
toast(
  "Your settings have been saved.",
  header = toast_header(
    title = "Settings Updated",
    icon = bsicons::bs_icon("gear"),
    status = "just now"
  ),
  type = "success"
)
```

## Key Parameters

### toast()

| Parameter | Default | Description |
|---|---|---|
| `header` | `NULL` | String or `toast_header()` object |
| `icon` | `NULL` | Icon element (when not using `toast_header()`) |
| `id` | auto | Stable ID for `hide_toast()` or replacing visible toasts |
| `type` | `NULL` | `"success"`, `"danger"`, `"warning"`, `"info"`, `"primary"`, etc. |
| `duration_s` | `5` | Seconds before auto-hide. Use `0` or `NA` to disable auto-hide |
| `position` | `"top-right"` | e.g. `"bottom-right"`, `"top-center"`, `"middle-center"` |
| `closable` | `TRUE` | Show close button |

### toast_header()

| Parameter | Description |
|---|---|
| `title` | Header text (required) |
| `icon` | Optional icon element |
| `status` | Optional small muted text on right side (e.g. "just now") |

## Showing and Hiding Toasts

**`show_toast()`** displays a toast and returns its ID:
```r
observeEvent(input$analyze, {
  result <- run_analysis()

  show_toast(
    toast(
      "Results are now available in the table below.",
      header = "Analysis Complete",
      type = "success"
    )
  )
})
```

**`hide_toast()`** dismisses a toast by ID:
```r
observeEvent(input$start, {
  # Show persistent toast (no auto-hide)
  show_toast(
    toast(
      "Processing...",
      id = "progress_toast",
      duration_s = NA,
      closable = FALSE
    )
  )

  result <- expensive_computation()

  hide_toast("progress_toast")
})
```

**Replacing toasts:** If a toast with the same `id` is already visible, showing a new one with that `id` automatically hides the old one first.

## Common Patterns

### Success/Error Feedback

```r
observeEvent(input$save, {
  tryCatch({
    save_data(data())
    show_toast(
      toast("Data saved successfully.", header = "Saved", type = "success")
    )
  }, error = function(e) {
    show_toast(
      toast(
        paste("Failed to save:", e$message),
        header = "Error",
        type = "danger",
        duration_s = NA  # Don't auto-hide errors
      )
    )
  })
})
```

### Progress then Completion

```r
observeEvent(input$export, {
  show_toast(
    toast("Exporting data...", id = "export", duration_s = NA, closable = FALSE)
  )

  export_data()

  hide_toast("export")
  show_toast(
    toast("File downloaded.", header = "Export Complete", type = "success")
  )
})
```

### Toast with Interactive Content

```r
show_toast(
  toast(
    actionLink("undo_delete", "Undo"),
    header = "Item Deleted",
    id = "undo_toast",
    duration_s = 10,
    closable = FALSE
  )
)

observeEvent(input$undo_delete, {
  restore_item()
  hide_toast("undo_toast")
})
```

## Best Practices

**Be specific:**
```r
# Good
show_toast(toast("Results saved to output.csv", header = "Analysis Complete", type = "success"))

# Too vague
show_toast("Done")
```

**Set appropriate durations:**
- Success messages: 3-5 seconds (default `duration_s = 5`)
- Error messages: `duration_s = NA` (let user read and dismiss)
- Progress updates: `duration_s = NA` + `closable = FALSE` until complete

**Use sparingly:** Don't toast every minor action. Combine related events. Avoid overload.

**Position consistently:** Use the same `position` throughout your app (default: `"top-right"`).

**Accessibility:** ARIA live regions are automatic. Don't rely solely on color for meaning.
