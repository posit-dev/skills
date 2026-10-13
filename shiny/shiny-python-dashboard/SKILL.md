---
name: shiny-python-dashboard
description: Build polished Shiny for Python dashboards and analytical apps. Use when creating or refactoring Shiny for Python apps, dashboards, KPI layouts, sidebar or navbar navigation, cards, value boxes, responsive grids, reactive filtering, charts, data tables, or when choosing between Core and Express APIs.
---

# Modern Shiny for Python Dashboards

Build professional dashboards with Shiny for Python's layout primitives, reactive graph, and card-based composition patterns. This skill is the Python equivalent of a modern bslib dashboard workflow: use `ui.page_sidebar()` or `ui.page_navbar()` for page structure, `ui.layout_columns()` or `ui.layout_column_wrap()` for responsive grids, `ui.card()` and `ui.value_box()` for content containers, and `@reactive.calc` plus render decorators for data flow.

## Critical rules

1. Never use emoji characters as icons. Use `faicons.icon_svg()` or Bootstrap Icons SVG instead.
2. Keep value boxes to 3 to 4 per row and wrap their container with `fill=False` so they do not stretch vertically.
3. Use `fillable=True` on dashboard page layouts and `full_screen=True` on chart or table cards.
4. Give every card a title with `ui.card_header("Title")`.
5. Prefer `ui.layout_column_wrap()` for uniform cards and `ui.layout_columns()` when you need explicit proportions.
6. Handle missing data explicitly with `dropna()`, `pd.to_numeric(..., errors="coerce")`, and `req()`.
7. Keep imports at module scope except `matplotlib.pyplot`, which should be imported inside `@render.plot` to avoid backend issues.
8. Format all displayed numbers for readability with commas, currency symbols, percentages, or compact abbreviations.
9. Keep the default dashboard hierarchy: value boxes at the top, charts in the middle, and the detailed table below.
10. Use breakpoint-aware `col_widths` so the layout still works on mobile.

## Quick Start

**Single-page dashboard with a shared sidebar:**

```python
from pathlib import Path

import pandas as pd
from faicons import icon_svg
from shiny import App, reactive, render, ui

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "data.csv")

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("metric", "Metric", choices=list(df.columns)),
        open="desktop",
    ),
    ui.layout_columns(
        ui.value_box(
            "Rows",
            ui.output_text("row_count"),
            showcase=icon_svg("database"),
            theme="primary",
        ),
        ui.value_box(
            "Average",
            ui.output_text("avg_value"),
            showcase=icon_svg("chart-line"),
            theme="info",
        ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Distribution"),
            ui.output_plot("distribution"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Preview"),
            ui.output_data_frame("preview"),
            full_screen=True,
        ),
        col_widths=[6, 6],
    ),
    title="Dashboard",
    fillable=True,
)


def server(input, output, session):
    @reactive.calc
    def series():
        return pd.to_numeric(df[input.metric()], errors="coerce").dropna()

    @render.text
    def row_count():
        return f"{len(df):,}"

    @render.text
    def avg_value():
        return f"{series().mean():,.1f}"

    @render.plot
    def distribution():
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(series(), bins=20, color="#0d6efd", edgecolor="white")
        ax.set_xlabel(input.metric())
        ax.set_ylabel("Count")
        fig.tight_layout()
        return fig

    @render.data_frame
    def preview():
        return render.DataGrid(df.head(20), filters=True)


app = App(app_ui, server)
```

**Multi-page dashboard with a navbar:**

```python
from shiny import App, ui

overview = ui.layout_columns(
    ui.card(ui.card_header("Summary"), "Overview content", full_screen=True),
    ui.card(ui.card_header("Recent activity"), "More content", full_screen=True),
    col_widths=[6, 6],
)

details = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("plot")),
    ui.nav_panel("Table", ui.output_data_frame("table")),
    title="Analysis",
)

app_ui = ui.page_navbar(
    ui.nav_panel("Overview", overview),
    ui.nav_panel("Analysis", details),
    title="Analytics Platform",
    fillable=True,
)
```

## Core Concepts

### Page layouts

- `ui.page_sidebar()` is the default for single-page dashboards with one shared set of controls.
- `ui.page_navbar()` is the default for multi-page apps with distinct sections.
- In Express, use `ui.page_opts(title=..., fillable=True)` and then declare `with ui.nav_panel(...):` blocks.

See [references/layout-and-navigation.md](references/layout-and-navigation.md) for layout, sidebar, navigation, and responsive grid patterns.

### Grids

- `ui.layout_column_wrap()` is the simplest way to build uniform KPI rows or evenly sized cards.
- `ui.layout_columns()` gives you a 12-column grid with breakpoint-aware `col_widths`.
- Negative column widths create intentional gaps when needed.

See [references/layout-and-navigation.md](references/layout-and-navigation.md) and [references/components.md](references/components.md) for detailed layout guidance.

### Cards

Cards are the primary dashboard container. Use `ui.card_header()` for titles, `ui.card_footer()` for context, and `full_screen=True` for plots, maps, and tables.

See [references/components.md](references/components.md) for card composition, tabbed card patterns, and inline controls.

### Value boxes

Use `ui.value_box()` for KPIs, summaries, and status indicators. Place them in a non-filling row so they stay compact and scannable.

See [references/components.md](references/components.md) for showcase icons, layouts, and dynamic output patterns.

### Reactivity

The primary reactive primitive is `@reactive.calc`. Chain calculations for derived data, and pair `@reactive.effect` with `@reactive.event` for reset buttons or imperative updates.

See [references/reactivity-and-rendering.md](references/reactivity-and-rendering.md) for reactive graph patterns and guardrails.

### Rendering outputs

- Use `@render.plot` for Matplotlib or Seaborn.
- Use `@render.data_frame` with `render.DataGrid(...)` for tables.
- Use `shinywidgets.output_widget()` plus `@render_plotly` for Plotly outputs.
- Use `@render.ui` for small dynamic UI fragments, including dynamic icons.

See [references/reactivity-and-rendering.md](references/reactivity-and-rendering.md) for output-specific guidance.

### Styling and data

Use a `shared.py` module or top-level data-loading block to keep data access, constants, and app directory logic out of reactive code. Pair this with a small `styles.css` file rather than inline styling everywhere.

See [references/styling-and-data.md](references/styling-and-data.md) for project structure, formatting, and styling guidance.

### Icons and maps

Use `faicons.icon_svg()` for dashboard icons and treat map widgets as full-screen cards with clear loading and empty-state behavior.

See [references/icons-and-maps.md](references/icons-and-maps.md) for icon, accessibility, and map patterns.

### Core and Express APIs

Both APIs are first-class. Pick one style for the app and keep it consistent. Core is explicit and easy to factor; Express is concise and works well for smaller apps.

See [references/core-vs-express.md](references/core-vs-express.md) for side-by-side equivalents and selection guidance.

## Common Workflows

### Building a dashboard

1. Choose `ui.page_sidebar()` for one-page analytics or `ui.page_navbar()` for multiple sections.
2. Load the data once at module scope or in `shared.py`, then compute reusable constants for inputs.
3. Put primary filters in a sidebar with `open="desktop"` so mobile starts collapsed.
4. Add KPI value boxes in a `fill=False` row near the top.
5. Arrange cards with `ui.layout_column_wrap()` or `ui.layout_columns()`.
6. Enable `full_screen=True` on visualizations and detailed tables.
7. Build the data pipeline through `@reactive.calc` functions, not mutated globals.
8. Finish with a `render.DataGrid(...)` card and minimal CSS overrides.

### Translating or modernizing an existing app

If you are replacing an older Shiny for Python layout or translating an R bslib design into Python:

1. Replace ad hoc `ui.div()` grid wiring with `ui.page_sidebar()`, `ui.page_navbar()`, `ui.layout_columns()`, or `ui.layout_column_wrap()`.
2. Wrap charts and tables in cards with headers and full-screen support.
3. Convert top-line metrics into `ui.value_box()` components.
4. Move repeated data transformations into `@reactive.calc` or `shared.py`.
5. Replace emoji icons with `faicons.icon_svg()`.
6. Audit charts for explicit sizes, axis labels, and missing-data handling.

## Guidelines

1. Prefer Shiny's page and layout primitives over raw `ui.div()` composition when building dashboards.
2. Keep one API style per app unless you have a compelling reason to mix Core and Express.
3. Use `ui.layout_column_wrap()` for uniform groups and `ui.layout_columns()` for precise layout control.
4. Wrap dashboard outputs in cards and default to `full_screen=True` on charts, maps, and tables.
5. Set `fill=False` on KPI rows so value boxes do not consume spare vertical space.
6. Use responsive `col_widths` such as `{"sm": 12, "md": [6, 6]}` for mobile-safe layouts.
7. Use named Bootstrap theme colors like `"primary"`, `"success"`, `"info"`, `"warning"`, and `"danger"` for value boxes.
8. Place imports at the top of the file, except `matplotlib.pyplot` inside `@render.plot`.
9. Never display raw numbers when a formatted value is more readable.
10. Guard empty selections and filtered datasets with `req()` before rendering.
11. Never pass duplicate keys when unpacking Plotly dicts; merge overrides with `{**base, "key": value}` instead.

## Avoid Common Errors

1. Do not omit `fill=False` on KPI rows; otherwise value boxes stretch awkwardly.
2. Do not wrap `ui.navset_card_*()` content in another `ui.card()`; the navset is already the card container.
3. Do not import `matplotlib.pyplot` at module scope in dashboard apps.
4. Do not pass the same key through both `**base_dict` and a keyword override in Plotly layout dictionaries.
5. Do not assume a sidebar on `ui.page_navbar()` should drive every page; use page-specific controls when sections need different filters.
6. Do not leave cards untitled or charts unlabeled.

## Number formatting

Always format numbers for display:

```python
f"{count:,}"            # 12,345
f"${amount:,.2f}"       # $1,234.56
f"{ratio:.1%}"          # 78.3%
f"{value:,.1f}"         # 1,234.6


def fmt_large(number):
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return f"{number:,.0f}"
```

## Reference Files

- [references/layout-and-navigation.md](references/layout-and-navigation.md) — page layouts, grids, nav panels, sidebars, and fill behavior
- [references/components.md](references/components.md) — cards, value boxes, accordions, tooltips, popovers, and inline controls
- [references/reactivity-and-rendering.md](references/reactivity-and-rendering.md) — reactive graph design and output rendering patterns
- [references/styling-and-data.md](references/styling-and-data.md) — project structure, data loading, formatting, styling, and themes
- [references/icons-and-maps.md](references/icons-and-maps.md) — icon rules, accessibility, and map container patterns
- [references/core-vs-express.md](references/core-vs-express.md) — API selection and side-by-side equivalents
