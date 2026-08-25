# Toolbars in bslib

Toolbars are compact horizontal strips of controls — buttons, selects, and dividers — designed for card headers and footers. Toolbar inputs are visually compact and integrate with the card's header/footer styling, unlike full-width sidebar controls.

## Table of Contents

- [Basic Usage](#basic-usage)
- [toolbar()](#toolbar)
- [toolbar_input_button()](#toolbar_input_button)
- [toolbar_input_select()](#toolbar_input_select)
- [toolbar_divider()](#toolbar_divider)
- [Server-Side Updates](#server-side-updates)
- [Placement Patterns](#placement-patterns)
- [Info Icon Labels](#info-icon-labels)

## Basic Usage

A toolbar in a card header with a select and a button:

```r
card(
  full_screen = TRUE,
  card_header(
    "Sales Trend",
    toolbar(
      toolbar_input_select("period", "Period",
        choices = c("Daily", "Weekly", "Monthly"),
        selected = "Monthly"
      ),
      toolbar_divider(),
      toolbar_input_button("download", "Download",
        icon = bsicons::bs_icon("download")
      )
    )
  ),
  plotOutput("trend_plot")
)
```

## toolbar()

```r
toolbar(..., align = c("right", "left"), gap = NULL, width = NULL)
```

Container for toolbar elements. Defaults to right-aligned within its parent (e.g., pushed to the right end of a card header).

| Parameter | Default | Description |
|---|---|---|
| `...` | | Toolbar elements: buttons, selects, dividers, or arbitrary HTML |
| `align` | `"right"` | Alignment within the parent: `"right"` or `"left"` |
| `gap` | `NULL` | CSS length unit for spacing between elements (e.g., `"0.5rem"`) |
| `width` | `NULL` | CSS width; defaults to `100%` |

## toolbar_input_button()

```r
toolbar_input_button(
  id,
  label,
  icon = NULL,
  show_label = is.null(icon),
  tooltip = !show_label,
  ...,
  disabled = FALSE,
  border = FALSE
)
```

A compact button for use inside `toolbar()`. When an icon is provided, the label is hidden by default and shown as a tooltip instead — keeping the toolbar visually tight while remaining accessible.

| Parameter | Default | Description |
|---|---|---|
| `id` | | Input ID. Behaves like `actionButton()` — increments on click |
| `label` | | Button label (shown or used as tooltip text) |
| `icon` | `NULL` | Icon element, e.g. `bsicons::bs_icon("download")` |
| `show_label` | `is.null(icon)` | Show label text; defaults to `TRUE` when no icon |
| `tooltip` | `!show_label` | Show label as hover tooltip when label is hidden |
| `disabled` | `FALSE` | Prevent clicks |
| `border` | `FALSE` | Show a border around the button |

**Reading the value:** `input$id` increments like `actionButton()`. Use `observeEvent(input$id, ...)`.

**Accessibility:** When `show_label = FALSE`, the label is still used as tooltip text (`tooltip = TRUE` by default) so screen reader and keyboard users can identify the button.

## toolbar_input_select()

```r
toolbar_input_select(
  id,
  label,
  choices,
  ...,
  selected = NULL,
  icon = NULL,
  show_label = FALSE,
  tooltip = !show_label
)
```

A compact select input for use inside `toolbar()`. The label is hidden by default (`show_label = FALSE`) and shown as a tooltip, keeping the toolbar uncluttered when context makes the purpose obvious.

| Parameter | Default | Description |
|---|---|---|
| `id` | | Input ID. `input$id` returns the selected value |
| `label` | | Label (used as tooltip when `show_label = FALSE`) |
| `choices` | | Character vector or named list of choices |
| `selected` | `NULL` | Initially selected value (defaults to first choice) |
| `icon` | `NULL` | Optional icon shown alongside the select |
| `show_label` | `FALSE` | Show label text inline |
| `tooltip` | `!show_label` | Show label as tooltip when hidden |

**Reading the value:** `input$id` returns the selected value as a string.

## toolbar_divider()

```r
toolbar_divider(..., width = NULL, gap = NULL)
```

A thin vertical rule for visually grouping toolbar elements.

| Parameter | Default | Description |
|---|---|---|
| `width` | `"2px"` | CSS width of the divider line |
| `gap` | `"1rem"` | CSS spacing on either side of the divider |

## Server-Side Updates

### update_toolbar_input_button()

```r
update_toolbar_input_button(
  id,
  label = NULL,
  show_label = NULL,
  icon = NULL,
  disabled = NULL,
  session = get_current_session()
)
```

Update button appearance or state from the server. Pass only the parameters you want to change; `NULL` leaves them unchanged.

**Example — toggle icon on click:**
```r
chart_type <- reactiveVal("bar")
observeEvent(input$toggle_type, {
  new_type <- if (chart_type() == "bar") "line" else "bar"
  chart_type(new_type)
  update_toolbar_input_button("toggle_type",
    icon = bsicons::bs_icon(if (new_type == "bar") "bar-chart" else "graph-up")
  )
})
```

**Example — conditionally disable:**
```r
observe({
  update_toolbar_input_button("export",
    disabled = nrow(filtered_data()) == 0
  )
})
```

### update_toolbar_input_select()

```r
update_toolbar_input_select(
  id,
  label = NULL,
  show_label = NULL,
  choices = NULL,
  selected = NULL,
  icon = NULL,
  session = get_current_session()
)
```

Update select choices, selection, or label from the server.

**Example — cascading selects:**
```r
observeEvent(input$region, {
  update_toolbar_input_select("store",
    choices = stores_for_region(input$region)
  )
})
```

## Placement Patterns

### Card Footer

```r
card(
  card_header("Plot"),
  plotOutput("plot"),
  card_footer(
    toolbar(
      toolbar_input_button("save", "Save",
        icon = bsicons::bs_icon("floppy")
      ),
      toolbar_input_button("share", "Share",
        icon = bsicons::bs_icon("share")
      ),
      toolbar_divider(),
      toolbar_input_button("fullscreen", "Expand",
        icon = bsicons::bs_icon("arrows-fullscreen")
      )
    )
  )
)
```

## Info Icon Labels

A toolbar is the cleanest way to add a help tooltip to an input label. Wrap the label text and an info icon together in a `toolbar()` as the `label` argument:

```r
selectInput(
  "metric",
  label = toolbar(
    align = "left",
    gap = "0.25rem",
    "Metric",
    tooltip(
      bsicons::bs_icon("info-circle", title = "About this metric"),
      "Revenue includes all recognized sales net of returns and discounts."
    )
  ),
  choices = c("Revenue", "Units", "Margin")
)
```

This works with any Shiny input that takes an HTML `label` argument. The `title` on `bs_icon()` provides accessible text for screen readers — see the main skill's Icons section for accessibility guidance on icon-only triggers.
