# Core vs Express — Full Comparison

## Contents

- Side-by-side quick reference
- Import differences
- Page setup
- UI construction
- Server function vs module-level
- Output placement
- Value box rendering
- Forward references

---

## Side-by-side quick reference

| Aspect | Core | Express |
| --- | --- | --- |
| **Imports** | `from shiny import App, reactive, render, ui` | `from shiny.express import input, render, ui` |
| **Page setup** | `app_ui = ui.page_sidebar(title=...)` | `ui.page_opts(title=..., fillable=True)` |
| **Sidebar** | `ui.sidebar(...)` as arg | `with ui.sidebar():` |
| **Layout** | Nested function calls | `with` context managers |
| **Server** | `def server(input, output, session):` | Module-level decorators |
| **Output placement** | `output_widget("id")` / `ui.output_*("id")` | Decorator inline in `with` block |
| **Value boxes** | `@render.ui` + `return` | `@render.express` (no `return`) |
| **Forward refs** | N/A | `with ui.hold():` |
| **App creation** | `app = App(app_ui, server)` | Not needed |
| **Nav panels** | `ui.nav_panel("Name", content)` as arg | `with ui.nav_panel("Name"):` |

---

## Import differences

```python
# Core
from shiny import App, reactive, render, req, ui
from shinywidgets import output_widget, render_plotly

# Express
from shiny import reactive, req
from shiny.express import input, render, ui
from shinywidgets import render_plotly
```

In Express, `input` is imported from `shiny.express`, not `shiny`.
`output_widget` is not needed in Express — `@render_plotly` is placed inline.

---

## Page setup

```python
# Core — declarative, assigned to a variable
app_ui = ui.page_sidebar(
    ui.sidebar(...),
    # ... layout content ...
    title="Dashboard",
    fillable=True,
)
```

```python
# Express — imperative, called at module level
ui.page_opts(title="Dashboard", fillable=True)
with ui.sidebar():
    ...
```

---

## UI construction

Core builds the entire UI tree as nested function calls:

```python
# Core
ui.layout_columns(
    ui.card(ui.card_header("Plot"), output_widget("plot"), full_screen=True),
    ui.card(ui.card_header("Table"), ui.output_data_frame("table")),
    col_widths=[8, 4],
)
```

Express uses `with` context managers:

```python
# Express
with ui.layout_columns(col_widths=[8, 4]):
    with ui.card(full_screen=True):
        ui.card_header("Plot")
        @render_plotly
        def plot(): ...
    with ui.card():
        ui.card_header("Table")
        @render.data_frame
        def table(): ...
```

---

## Server function vs module-level

Core wraps all reactive logic in an explicit server function:

```python
# Core
def server(input, output, session):
    @reactive.calc
    def filtered(): ...

    @render.plot
    def plot(): ...

app = App(app_ui, server)
```

Express places reactive logic at module level — no `server` function, no `App()`:

```python
# Express
@reactive.calc
def filtered(): ...

# Render decorators placed inline within with-blocks (see UI construction above)
```

---

## Output placement

In Core, outputs must be placed in the UI tree using explicit placeholder functions:

- `output_widget("id")` for Plotly charts (from `shinywidgets`)
- `ui.output_ui("id")` for dynamic UI / value box content
- `ui.output_plot("id")` for matplotlib/seaborn
- `ui.output_data_frame("id")` for data tables

In Express, render decorators are placed inline where the output should appear:

```python
with ui.card():
    @render_plotly
    def chart(): ...  # output appears here in the card
```

---

## Value box rendering

```python
# Core — @render.ui with explicit return
@render.ui
def average_tip():
    d = tips_data().select((pl.col("tip") / pl.col("total_bill")).mean()).item()
    return f"{d:.1%}" if d else "N/A"
```

```python
# Express — @render.express, value printed implicitly (no return)
with ui.value_box(showcase=icon_svg("wallet")):
    "Average tip"
    @render.express
    def average_tip():
        d = tips_data().select((pl.col("tip") / pl.col("total_bill")).mean()).item()
        f"{d:.1%}" if d else "N/A"
```

---

## Forward references

Core has no forward-reference issue — the UI tree and server are separate.

In Express, if an output is used as a parameter (e.g., `showcase=output_ui("icon")`)
before the render function is defined, wrap the definition in `with ui.hold()`:

```python
# The value_box references "change_icon" before it exists
with ui.value_box(showcase=output_ui("change_icon")):
    "Change"
    @render.ui
    def change(): return f"${get_change():.2f}"

# Define the forward-referenced output later
with ui.hold():
    @render.ui
    def change_icon():
        icon = icon_svg("arrow-up" if get_change() >= 0 else "arrow-down")
        icon.add_class(f"text-{'success' if get_change() >= 0 else 'danger'}")
        return icon
```
