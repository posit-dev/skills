````skill
---
name: shiny-python-dashboard
description: Best practices for building polished dashboards in Shiny for Python. Covers Core and Express APIs, proper icon usage (faicons/Bootstrap Icons — never emojis), value box layout, responsive grids, charts, and reactive patterns.
---

## Critical rules — ALWAYS follow these

1. **NEVER use emoji characters as icons.** No emojis anywhere — not in value box showcase, not in nav panel titles, not in card headers. Use `faicons.icon_svg()` or Bootstrap Icons SVG instead. Emojis render inconsistently and look unprofessional.
2. **Limit value boxes to 3-4 per row.** More causes text overlap and cramped layouts.
3. **Always set `fill=False`** on the row wrapping value boxes (`layout_columns` or `layout_column_wrap`) to prevent vertical stretching.
4. **Always set `fillable=True`** on `page_sidebar` / `page_opts`.
5. **Always add `full_screen=True`** on cards containing charts or tables.
6. **Always add `ui.card_header("Title")`** to every card — never leave cards untitled.
7. **Use `ui.layout_columns(col_widths=[...])`** for grid layouts.
8. **Set explicit chart dimensions** — `fig.update_layout(height=400)` for Plotly, `plt.subplots(figsize=(8, 4))` for Matplotlib.
9. **Handle NaN/missing data gracefully** — some columns have blanks. Use `df.dropna(subset=[col])` before plotting, `pd.to_numeric(col, errors="coerce")` for mixed-type columns, and guard with `req()` for empty inputs.
10. **Use named Bootstrap theme colors** for value boxes: `"primary"`, `"success"`, `"info"`, `"warning"`, `"danger"`. Avoid `bg-gradient-*`.
11. **Place ALL imports at the top of the file.** Never import inside functions, reactive calcs, or render blocks — except `matplotlib.pyplot` which must be imported inside `@render.plot` to avoid backend conflicts.
12. **Format all numbers for readability.** Never display raw floats or unformatted integers. Use comma separators, currency symbols, and percentage formatting.
13. **Follow the standard dashboard layout hierarchy**: value boxes (KPIs) at top → charts in middle → data table at bottom.
14. **Use responsive `col_widths` with breakpoints** for layouts that work on mobile: `col_widths={"sm": 12, "md": [6, 6]}`.

## Number formatting

Always format numbers for professional display:

```python
# Integers — comma separator
f"{count:,}"                    # "12,345"

# Currency
f"${amount:,.2f}"               # "$1,234.56"
f"${amount:,.0f}"               # "$1,235"

# Percentages
f"{ratio:.1%}"                  # "78.3%"
f"{ratio:.0%}"                  # "78%"

# Decimals — control precision
f"{value:,.1f}"                 # "1,234.6"
f"{value:.2f}"                  # "1234.57"

# Large numbers — abbreviate
def fmt_large(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000: return f"{n/1_000:.1f}K"
    return f"{n:,.0f}"
```

Never display raw floats like `0.7834523123` or unformatted integers like `12345`.

## Icons — ONLY faicons or Bootstrap Icons

```python
# CORRECT: faicons (Font Awesome SVGs) — preferred
from faicons import icon_svg
icon = icon_svg("chart-line")        # solid style (default)
icon = icon_svg("user", "regular")   # outlined style
```

```python
# WRONG — NEVER do this:
showcase="\U0001F4CA"         # emoji is NOT an icon
showcase="\U0001F3E5"         # emoji is NOT an icon
```

### Common faicons for dashboards

| Icon name           | Use case                    |
|---------------------|-----------------------------|
| `"chart-line"`      | Trends, time series         |
| `"chart-bar"`       | Bar charts, distributions   |
| `"users"`           | People count                |
| `"user"`            | Individual person           |
| `"dollar-sign"`     | Currency, revenue           |
| `"wallet"`          | Money, tips                 |
| `"clipboard-check"` | Completed tasks             |
| `"calendar"`        | Dates, scheduling           |
| `"flask"`           | Science, experiments        |
| `"stethoscope"`     | Healthcare                  |
| `"heart-pulse"`     | Health metrics              |
| `"arrow-up"`        | Positive change             |
| `"arrow-down"`      | Negative change             |
| `"percent"`         | Percentages                 |
| `"database"`        | Data, records               |
| `"filter"`          | Filtering                   |
| `"table"`           | Tabular data                |
| `"magnifying-glass"`| Search                      |
| `"globe"`           | Geographic data             |
| `"building"`        | Organizations               |
| `"pills"`           | Medications, pharma         |
| `"vial"`            | Lab samples                 |
| `"truck"`           | Shipping, logistics         |
| `"circle-check"`    | Success, completion         |
| `"clock"`           | Time, duration              |
| `"hospital"`        | Healthcare facility         |

## Quick start — Core dashboard

```python
from pathlib import Path
import pandas as pd
from faicons import icon_svg
from shiny import App, reactive, render, ui

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "data.csv")

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("var", "Variable", choices=list(df.columns)),
        open="desktop",
    ),
    # Value boxes — fill=False prevents vertical stretching
    ui.layout_columns(
        ui.value_box("Total Records", ui.output_text("total"),
            showcase=icon_svg("database"), theme="primary"),
        ui.value_box("Average", ui.output_text("avg"),
            showcase=icon_svg("chart-line"), theme="info"),
        ui.value_box("Maximum", ui.output_text("max_val"),
            showcase=icon_svg("arrow-up"), theme="success"),
        fill=False,
    ),
    # Charts — col_widths controls the grid
    ui.layout_columns(
        ui.card(ui.card_header("Distribution"),
            ui.output_plot("hist"), full_screen=True),
        ui.card(ui.card_header("Trend"),
            ui.output_plot("trend"), full_screen=True),
        col_widths=[6, 6],
    ),
    # Data table
    ui.card(ui.card_header("Data"), ui.output_data_frame("table"),
        full_screen=True),
    title="Dashboard",
    fillable=True,
)

def server(input, output, session):
    @reactive.calc
    def filtered():
        return df

    @render.text
    def total():
        return f"{len(filtered()):,}"

    @render.text
    def avg():
        return f"{filtered()[input.var()].mean():,.1f}"

    @render.text
    def max_val():
        return f"{filtered()[input.var()].max():,.0f}"

    @render.plot
    def hist():
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(filtered()[input.var()].dropna(), bins=20,
            color="#0d6efd", edgecolor="white")
        ax.set_xlabel(input.var())
        ax.set_ylabel("Count")
        return fig

    @render.plot
    def trend():
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(filtered()[input.var()].dropna().values,
            color="#198754", linewidth=1.5)
        ax.set_ylabel(input.var())
        return fig

    @render.data_frame
    def table():
        return render.DataGrid(filtered(), filters=True)

app = App(app_ui, server)
```

## Quick start — Express dashboard

```python
from pathlib import Path
import pandas as pd
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "data.csv")

ui.page_opts(title="Dashboard", fillable=True)

with ui.sidebar(open="desktop"):
    ui.input_select("var", "Variable", choices=list(df.columns))

@reactive.calc
def filtered():
    return df

# Value boxes — fill=False prevents vertical stretching
with ui.layout_columns(fill=False):
    with ui.value_box(showcase=icon_svg("database"), theme="primary"):
        "Total Records"
        @render.express
        def total():
            f"{len(filtered()):,}"

    with ui.value_box(showcase=icon_svg("chart-line"), theme="info"):
        "Average"
        @render.express
        def avg():
            f"{filtered()[input.var()].mean():,.1f}"

    with ui.value_box(showcase=icon_svg("arrow-up"), theme="success"):
        "Maximum"
        @render.express
        def max_val():
            f"{filtered()[input.var()].max():,.0f}"

# Charts
with ui.layout_columns(col_widths=[6, 6]):
    with ui.card(full_screen=True):
        ui.card_header("Distribution")
        @render.plot
        def hist():
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(filtered()[input.var()].dropna(), bins=20,
                color="#0d6efd", edgecolor="white")
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Trend")
        @render.plot
        def trend():
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(filtered()[input.var()].dropna().values, color="#198754")
            return fig

# Data table
with ui.card(full_screen=True):
    ui.card_header("Data")
    @render.data_frame
    def table():
        return render.DataGrid(filtered(), filters=True)
```

## Dashboard layout hierarchy

Always follow this top-to-bottom structure:

```
1. Value boxes (KPIs)     — fill=False row at the top
2. Charts                 — in cards with full_screen=True
3. Data table             — full-width card at the bottom
```

For multi-page apps with `page_navbar`, apply this hierarchy within each `nav_panel`.

## Responsive design

Use `col_widths` with breakpoint dictionaries so dashboards look good on all screen sizes:

```python
# Stacks on mobile, side-by-side on desktop
ui.layout_columns(
    chart_card_1, chart_card_2,
    col_widths={"sm": 12, "md": [6, 6]},
)

# Three columns on desktop, stacked on mobile
ui.layout_columns(
    card_a, card_b, card_c,
    col_widths={"sm": 12, "md": [6, 6, 12], "lg": [4, 4, 4]},
)

# Use negative values for spacing
ui.layout_columns(
    card_a, card_b,
    col_widths=[5, -2, 5],  # 5-wide cards with 2-unit gap
)
```

For uniform grids (all items same size), use `ui.layout_column_wrap(width=1/3)` instead.

## Chart best practices

- **Plotly**: Set `height=400`, hide modebar, use `margin=dict(l=40, r=20, t=40, b=40)`
- **Matplotlib**: Use `figsize=(8, 4)`, call `fig.tight_layout()` before returning
- **Seaborn**: Build on matplotlib — same `figsize` rules apply
- **Color palette**: Use Bootstrap-aligned colors for consistency:
  - Primary blue: `"#0d6efd"` — main charts
  - Success green: `"#198754"` — positive trends
  - Danger red: `"#dc3545"` — negative trends, alerts
  - Info cyan: `"#0dcaf0"` — secondary charts
  - Warning amber: `"#ffc107"` — caution indicators
- **Always label axes** with `ax.set_xlabel()` / `ax.set_ylabel()`
- **Remove chartjunk**: no unnecessary gridlines, borders, or legends for single-series charts

## Project structure

```
my-dashboard/
+-- app.py               # Main app (Core or Express)
+-- shared.py            # Data loading, constants, app_dir
+-- styles.css           # Minimal CSS overrides
+-- data.csv             # Static data files
+-- requirements.txt     # Must include faicons
```

`shared.py` always exports `app_dir = Path(__file__).parent` and pre-loaded data.
`requirements.txt` must always include `faicons`.

## Reference files

Read these for detailed patterns on specific topics:

**Layout & navigation**: See [references/layout-and-navigation.md](references/layout-and-navigation.md)
**Value boxes, cards & grids**: See [references/components.md](references/components.md)
**Reactivity & rendering**: See [references/reactivity-and-rendering.md](references/reactivity-and-rendering.md)
**Styling & data loading**: See [references/styling-and-data.md](references/styling-and-data.md)
**Icons & maps**: See [references/icons-and-maps.md](references/icons-and-maps.md)
**Core vs Express**: See [references/core-vs-express.md](references/core-vs-express.md)
````
