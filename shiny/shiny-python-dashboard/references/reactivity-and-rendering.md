# Reactivity and Rendering

## Contents

- `@reactive.calc` — the primary primitive
- `@reactive.effect` and `@reactive.event`
- `req()` — guarding against empty inputs
- Rendering Plotly charts
- Rendering Matplotlib/Seaborn plots
- Rendering data tables
- Rendering value box content
- Interactive Plotly click events

---

## `@reactive.calc` — The primary primitive

Use for all filtered/derived data. Chain calcs for multi-step transformations:

```python
@reactive.calc
def get_ticker():
    return yf.Ticker(input.ticker())

@reactive.calc
def get_data():
    return get_ticker().history(start=input.dates()[0], end=input.dates()[1])

@reactive.calc
def get_change():
    close = get_data()["Close"]
    if len(close) < 2:
        return 0.0
    return close.iloc[-1] - close.iloc[-2]
```

Filtering pattern with Polars:

```python
@reactive.calc
def tips_data():
    bill = input.total_bill()
    return tips.filter(
        pl.col("total_bill").is_between(bill[0], bill[1]),
        pl.col("time").is_in(input.time()),
    )
```

Filtering pattern with Pandas:

```python
@reactive.calc
def careers():
    games = input.games()
    idx = (careers_df["GP"] >= games[0]) & (careers_df["GP"] <= games[1])
    return careers_df[idx]
```

### Core rule: No global state mutation

All reactivity flows one direction through `@reactive.calc` chains. Never mutate
module-level variables inside reactive functions.

---

## `@reactive.effect` and `@reactive.event`

### Reset buttons

Use `@reactive.effect` + `@reactive.event(input.reset)` to reset inputs to defaults:

```python
@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_slider("total_bill", value=bill_rng)
    ui.update_checkbox_group("time", selected=["Lunch", "Dinner"])
```

### Cascading UI updates

Use `@reactive.effect` (without `@reactive.event`) to update dependent inputs
when upstream data changes:

```python
@reactive.effect
def _():
    players = dict(zip(careers()["person_id"], careers()["player_name"]))
    ui.update_selectize("players", choices=players, selected=input.players())
```

This re-runs whenever `careers()` changes, keeping the selectize choices in sync.

---

## `req()` — Guarding against empty inputs

```python
from shiny import req

@reactive.calc
def player_stats():
    players = req(input.players())  # stops execution if None/empty
    return careers()[careers()["person_id"].isin(players)]
```

`req()` silently stops reactive execution when the value is falsy, preventing
downstream errors from empty selections.

---

## Rendering Plotly charts

Use `@render_plotly` from `shinywidgets`. Always set explicit `height` on the figure:

```python
from shinywidgets import output_widget, render_plotly

# Core — requires output_widget("scatterplot") in UI tree
@render_plotly
def scatterplot():
    color = input.scatter_color()
    fig = px.scatter(tips_data(), x="total_bill", y="tip",
        color=None if color == "none" else color, trendline="lowess")
    fig.update_layout(height=400, margin=dict(l=40, r=20, t=40, b=40))
    return fig
```

```python
# Express — place inline inside card
with ui.card(full_screen=True):
    ui.card_header("Scatter Plot")
    @render_plotly
    def scatterplot(): ...
```

In Core, always pair `@render_plotly` with `output_widget("id")` in the UI tree.
In Express, place the decorator inline inside `with ui.card():`.

---

## Rendering Matplotlib/Seaborn plots

Use `@render.plot` — returns a matplotlib figure or axes.
Always set `figsize` explicitly to prevent tiny charts:

```python
@render.plot
def hist():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df[input.var()].dropna(), bins=20,
        color="#0d6efd", edgecolor="white")
    ax.set_xlabel(input.var())
    ax.set_ylabel("Count")
    return fig
```

Combine `sns.kdeplot` + `sns.rugplot` for density with rug marks:

```python
@render.plot
def density():
    hue = "species" if input.species() else None
    sns.kdeplot(df, x=input.var(), hue=hue)
    if input.show_rug():
        sns.rugplot(df, x=input.var(), hue=hue, color="black", alpha=0.25)
```

In Core, use `ui.output_plot("id")` in the UI tree.

---

## Rendering data tables

```python
@render.data_frame
def table():
    return render.DataGrid(tips_data())
```

Add `filters=True` for column-level filtering: `render.DataGrid(df, filters=True)`.

In Core, use `ui.output_data_frame("table")` in the UI tree.

---

## Rendering value box content

```python
# Core — @render.ui returning a formatted string
@render.ui
def average_tip():
    d = tips_data().select((pl.col("tip") / pl.col("total_bill")).mean()).item()
    return f"{d:.1%}" if d else "N/A"
```

```python
# Express — @render.express (prints value, no return needed)
@render.express
def average_tip():
    d = tips_data().select((pl.col("tip") / pl.col("total_bill")).mean()).item()
    f"{d:.1%}" if d else "N/A"
```

---

## Interactive Plotly click events

Convert a plotly Figure to `go.FigureWidget` and attach `.on_click()`:

```python
import plotly.graph_objects as go

fig = go.FigureWidget(fig.data, fig.layout)
fig.data[1].on_click(on_rug_click)
return fig

def on_rug_click(trace, points, state):
    player_id = trace.customdata[points.point_inds[0]]
    selected = list(input.players()) + [player_id]
    ui.update_selectize("players", selected=selected)
```

This enables click-to-select interactions on plotly rug plots or scatter traces.
