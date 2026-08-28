# Reactivity and Rendering in Shiny for Python

This reference covers the reactive graph and output rendering patterns that make a Shiny for Python dashboard predictable and maintainable.

## Reactive Graph Design

### `@reactive.calc`

Use `@reactive.calc` for filtered data, derived metrics, and reusable intermediate objects.

```python
@reactive.calc
def filtered_data():
    frame = df.copy()
    if input.region():
        frame = frame[frame["region"].isin(input.region())]
    return frame


@reactive.calc
def metric_series():
    return pd.to_numeric(filtered_data()[input.metric()], errors="coerce").dropna()
```

Chain reactive calcs instead of repeating the same filtering logic in every output.

### `req()`

Use `req()` to stop the reactive pipeline when an input or intermediate result is empty.

```python
from shiny import req


@reactive.calc
def selected_players():
    players = req(input.players())
    return careers()[careers()["person_id"].isin(players)]
```

This keeps render functions simple and avoids error-prone empty-state code in every output.

### `@reactive.effect` and `@reactive.event`

Use `@reactive.effect` for imperative updates such as resetting inputs or synchronizing dependent controls. Add `@reactive.event(...)` when the effect should only run in response to a specific trigger.

```python
@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_slider("amount", value=[10, 90])
    ui.update_checkbox_group("service", selected=["Lunch", "Dinner"])
```

Without `@reactive.event`, the effect will rerun whenever one of its reactive dependencies changes.

### No global mutation

Do not mutate module-level globals inside reactive functions. Compute new values and return them through the reactive graph instead.

## Rendering Patterns

### Matplotlib and Seaborn with `@render.plot`

Import `matplotlib.pyplot` inside the render function.

```python
@render.plot
def histogram():
    import matplotlib.pyplot as plt

    series = req(metric_series())
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(series, bins=20, color="#0d6efd", edgecolor="white")
    ax.set_xlabel(input.metric())
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig
```

Rules:

- use `figsize=(8, 4)` as a strong default
- label axes
- call `fig.tight_layout()` before returning
- drop missing values before plotting

### Plotly with `shinywidgets`

Use `output_widget()` in Core apps and `@render_plotly` in the server or Express block.

```python
from shinywidgets import output_widget, render_plotly

app_ui = ui.card(
    ui.card_header("Scatterplot"),
    output_widget("scatterplot"),
    full_screen=True,
)


@render_plotly
def scatterplot():
    return px.scatter(filtered_data(), x="total_bill", y="tip", color=input.color())
```

Avoid duplicate keys when you merge Plotly layout dictionaries:

```python
axis_style = {"gridcolor": "#d0d7de", "showline": False}
fig.update_layout(yaxis={**axis_style, "tickfont": {"size": 11}})
```

Do not write `dict(**axis_style, tickfont=...)` if `axis_style` already contains `tickfont`.

### Tables with `@render.data_frame`

Use `render.DataGrid(...)` for sortable, filterable tables.

```python
@render.data_frame
def summary_table():
    return render.DataGrid(filtered_data(), filters=True)
```

Treat the data table as the detailed layer beneath charts and KPIs.

### Dynamic UI with `@render.ui`

Use `@render.ui` for small dynamic fragments such as icons, badges, or conditional helper text.

```python
@render.ui
def growth_note():
    if get_change() >= 0:
        return ui.span("Up vs prior period", class_="text-success")
    return ui.span("Down vs prior period", class_="text-danger")
```

Do not build major page sections with `@render.ui` if a regular static layout plus reactive outputs would be simpler.

## Core and Express Equivalents

Core API keeps outputs explicit in the UI tree:

```python
ui.card(ui.card_header("Data"), ui.output_data_frame("table"), full_screen=True)


@render.data_frame
def table():
    return render.DataGrid(filtered_data())
```

Express colocates the UI block and renderer:

```python
with ui.card(full_screen=True):
    ui.card_header("Data")

    @render.data_frame
    def table():
        return render.DataGrid(filtered_data())
```

Both are valid. Choose the style that fits the codebase and keep it consistent.

## Common Patterns

### Reset buttons

Use `@reactive.effect` with `@reactive.event` and the appropriate `ui.update_*()` helpers.

### Cascading inputs

Use a plain `@reactive.effect` when one input's choices depend on the current filtered data.

```python
@reactive.effect
def _():
    choices = dict(zip(filtered_data()["id"], filtered_data()["label"]))
    ui.update_selectize("item", choices=choices)
```

### Derived KPI values

Create one calc per reusable business metric instead of recalculating inside each value box renderer.

## Common Errors

1. Repeating filtering logic in every render function instead of centralizing it in `@reactive.calc`.
2. Forgetting `req()` before indexing into empty selections.
3. Importing `matplotlib.pyplot` at module scope.
4. Building large layouts with `@render.ui` instead of static UI plus small reactive outputs.
5. Duplicating Plotly layout keys during dict unpacking.
