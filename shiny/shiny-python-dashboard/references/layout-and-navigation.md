# Layout and Navigation in Shiny for Python

This reference covers the page-level and section-level layout patterns for Shiny for Python dashboards. The goal is the same as a modern bslib dashboard in R: keep high-level structure explicit, use cards as the main content containers, and let the layout primitives handle responsive behavior instead of wiring grids by hand with `ui.div()`.

## Page Layouts

### `ui.page_sidebar()`

Use `ui.page_sidebar()` for single-page dashboards where one sidebar controls the whole page.

**Core API:**

```python
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize("ticker", "Stock", choices=stocks),
        ui.input_date_range("dates", "Dates", start=start, end=end),
        open="desktop",
    ),
    ui.card(ui.card_header("Price history"), ui.output_plot("price"), full_screen=True),
    title="Market Dashboard",
    fillable=True,
)
```

**Express API:**

```python
ui.page_opts(title="Market Dashboard", fillable=True)

with ui.sidebar(open="desktop"):
    ui.input_selectize("ticker", "Stock", choices=stocks)
    ui.input_date_range("dates", "Dates", start=start, end=end)
```

Best practices:

- Keep inputs in `ui.sidebar()` and outputs in the main page body.
- Use `open="desktop"` so the sidebar is visible on large screens and collapses on mobile.
- Treat the page body as a sequence of value-box rows, chart cards, and table cards.

### `ui.page_navbar()`

Use `ui.page_navbar()` for multi-page apps with distinct sections.

**Core API:**

```python
overview = ui.layout_columns(
    ui.card(ui.card_header("Overview"), ui.output_plot("overview_plot"), full_screen=True),
    ui.card(ui.card_header("Summary"), ui.output_data_frame("overview_table"), full_screen=True),
    col_widths=[6, 6],
)

app_ui = ui.page_navbar(
    ui.nav_panel("Overview", overview),
    ui.nav_panel("Details", ui.output_data_frame("details")),
    title="Analytics Platform",
    fillable=True,
)
```

**Express API:**

```python
ui.page_opts(title="Analytics Platform", fillable=True)
ui.nav_spacer()

with ui.nav_panel("Overview"):
    with ui.layout_columns(col_widths=[6, 6]):
        with ui.card(full_screen=True):
            ui.card_header("Overview")
            @render.plot
            def overview_plot():
                ...

with ui.nav_panel("Details"):
    with ui.card(full_screen=True):
        ui.card_header("Details")
        @render.data_frame
        def details():
            ...
```

Best practices:

- Use a navbar when pages serve different workflows, not just because there is a lot of content.
- `ui.nav_spacer()` is useful when you want later nav items aligned to the right.
- Do not force one shared sidebar onto every page if the pages need different filters.

## Grid Layouts

### `ui.layout_column_wrap()`

Use `ui.layout_column_wrap()` for uniform cards or KPI boxes.

```python
ui.layout_column_wrap(
    ui.value_box("Users", ui.output_text("users"), showcase=icon_svg("users")),
    ui.value_box("Revenue", ui.output_text("revenue"), showcase=icon_svg("dollar-sign")),
    ui.value_box("Growth", ui.output_text("growth"), showcase=icon_svg("chart-line")),
    width=1 / 3,
    fill=False,
)
```

Use a CSS width like `"280px"` when you want the column count to adapt to screen size automatically.

```python
ui.layout_column_wrap(card_a, card_b, card_c, width="280px")
```

Guidelines:

- Prefer `width=1 / 3` or `width="280px"` instead of hand-calculated percent strings.
- Use `fill=False` for KPI rows so value boxes keep natural height.
- Use `ui.layout_column_wrap()` when you want a clean, even dashboard rhythm.

### `ui.layout_columns()`

Use `ui.layout_columns()` when you need explicit control over width proportions or breakpoints.

```python
ui.layout_columns(
    ui.card(ui.card_header("Sidebar summary"), ui.output_text_verbatim("summary")),
    ui.card(ui.card_header("Main chart"), ui.output_plot("plot"), full_screen=True),
    col_widths=[4, 8],
)
```

Responsive layouts use breakpoint dictionaries:

```python
ui.layout_columns(
    chart_card,
    table_card,
    col_widths={"sm": 12, "md": [6, 6], "lg": [7, 5]},
)
```

Negative values create gaps when needed:

```python
ui.layout_columns(card_a, card_b, col_widths=[5, -2, 5])
```

Use `ui.layout_columns()` when the proportions matter more than uniformity.

## Navigation Containers

Use `ui.nav_panel()` to group related content into tabs or pages.

### `ui.navset_card_underline()`

This is the most useful section-level navigation container for dashboards: it creates a tabbed card with a header and shared footer controls.

**Core API:**

```python
analysis = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("plot")),
    ui.nav_panel("Table", ui.output_data_frame("table")),
    title="Analysis",
    footer=ui.input_select("metric", "Metric", choices=metrics),
)
```

**Express API:**

```python
footer = ui.input_select("metric", "Metric", choices=metrics)

with ui.navset_card_underline(title="Analysis", footer=footer):
    with ui.nav_panel("Plot"):
        @render.plot
        def plot():
            ...

    with ui.nav_panel("Table"):
        @render.data_frame
        def table():
            ...
```

Do not wrap `ui.nav_panel()` content in another `ui.card()` when the container is already `ui.navset_card_*()`.

## Sidebars

### Page-level sidebars

Use page-level sidebars when the controls affect the whole page or the whole app section.

```python
ui.page_sidebar(
    ui.sidebar(
        ui.input_checkbox_group("region", "Region", regions),
        ui.input_action_button("reset", "Reset"),
        open="desktop",
    ),
    ...,
)
```

For navbar apps, only use a single shared sidebar if every page really uses the same controls.

### Component-level sidebars

Use `ui.layout_sidebar()` inside a card when one chart or module needs local controls.

```python
ui.card(
    ui.card_header("Custom chart"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("color", "Color by", choices=color_vars),
            position="right",
            width="240px",
        ),
        ui.output_plot("custom_chart"),
        fillable=True,
    ),
    full_screen=True,
)
```

This keeps advanced controls close to the output they affect and avoids overloading the global sidebar.

## Fill Behavior

The same rule from bslib still applies conceptually: fill behavior only works when the surrounding container has a meaningful height.

- Use `fillable=True` on dashboard pages.
- Use `full_screen=True` when users may need more space.
- Use fixed `height`, `min_height`, or chart-specific dimensions when a card would otherwise collapse too far.
- Avoid putting non-filling KPI rows inside layouts that should donate space to charts.

A common hybrid pattern is a non-filling KPI row followed by cards that can grow:

```python
ui.page_sidebar(
    ui.sidebar(...),
    ui.layout_columns(kpi_a, kpi_b, kpi_c, fill=False),
    ui.layout_columns(chart_a, chart_b, col_widths=[6, 6]),
    fillable=True,
)
```

## Best Practices

1. Start with `ui.page_sidebar()` unless the app clearly needs multiple pages.
2. Use `ui.page_navbar()` for separate workflows, not just to hide content overflow.
3. Prefer `ui.layout_column_wrap()` for evenly sized cards and `ui.layout_columns()` for asymmetric layouts.
4. Keep KPI rows near the top and mark them `fill=False`.
5. Put page-specific controls in page-specific sidebars rather than forcing one global sidebar everywhere.
6. Use `ui.navset_card_underline()` to organize plots, tables, and notes within a single card-sized region.
