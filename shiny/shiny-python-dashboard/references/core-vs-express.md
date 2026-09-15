# Core vs Express in Shiny for Python

Both Core and Express are first-class APIs in Shiny for Python. This reference helps you choose between them and translate patterns cleanly from one style to the other.

## High-Level Difference

- Core separates UI declaration from server outputs.
- Express colocates layout blocks and render functions.

Neither is more "correct" for dashboards. Pick the style that matches the app's size, expected complexity, and the team's preference for explicit structure versus local readability.

## When to Choose Core

Choose Core when:

- the app is large or likely to grow
- you want a clearly separated `app_ui` and `server`
- outputs need to be referenced across modules or helper functions
- you want the UI tree to be easy to inspect at a glance

Core is often the safer default for production dashboards with several sections.

## When to Choose Express

Choose Express when:

- the app is small to medium sized
- the main advantage is colocating a card and its renderer
- the team prefers a more linear, notebook-like authoring style
- rapid iteration matters more than strict separation

Express works well for focused dashboards where the layout is easy to read top to bottom.

## Equivalent Patterns

| Pattern | Core | Express |
|---|---|---|
| Page title and fill | `ui.page_sidebar(..., title="App", fillable=True)` | `ui.page_opts(title="App", fillable=True)` |
| Sidebar | `ui.sidebar(...)` inside page layout | `with ui.sidebar(...):` |
| Card output | `ui.card(ui.card_header("Plot"), ui.output_plot("plot"), full_screen=True)` | `with ui.card(full_screen=True): ui.card_header("Plot")` plus `@render.plot` |
| Data table | `ui.output_data_frame("table")` plus `@render.data_frame` | `@render.data_frame` inside the card block |
| Value box | `ui.value_box("Title", ui.output_ui("value"), ...)` | `with ui.value_box(...): "Title"` plus `@render.express` |
| Section tabs | `ui.navset_card_underline(...)` assigned to a variable or inserted directly | `with ui.navset_card_underline(...):` |

## Skeletons

### Core skeleton

```python
from shiny import App, reactive, render, ui

app_ui = ui.page_sidebar(
    ui.sidebar(ui.input_select("metric", "Metric", choices=metrics), open="desktop"),
    ui.card(ui.card_header("Plot"), ui.output_plot("plot"), full_screen=True),
    title="Dashboard",
    fillable=True,
)


def server(input, output, session):
    @reactive.calc
    def filtered():
        return df

    @render.plot
    def plot():
        ...


app = App(app_ui, server)
```

### Express skeleton

```python
from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="Dashboard", fillable=True)

with ui.sidebar(open="desktop"):
    ui.input_select("metric", "Metric", choices=metrics)


@reactive.calc
def filtered():
    return df


with ui.card(full_screen=True):
    ui.card_header("Plot")

    @render.plot
    def plot():
        ...
```

## Important Express Detail

`ui.hold()` exists in the Express namespace and is useful when an output is referenced before it is defined.

```python
from shiny.express import render, ui

with ui.value_box(showcase=ui.output_ui("trend_icon")):
    "Trend"

with ui.hold():
    @render.ui
    def trend_icon():
        return icon_svg("arrow-up")
```

## Rules for Mixing Styles

- Do not casually mix Core and Express in the same file.
- If you need to translate one style into the other, translate the full local pattern: layout block, reactive helpers, and render functions.
- Keep helper modules, data loading, and formatting utilities reusable regardless of API choice.

## Best Practices

1. Pick one API per app file and stay consistent.
2. Use Core when structure and maintainability matter most.
3. Use Express when localized readability matters most.
4. Translate patterns between APIs mechanically rather than inventing a third style.
5. Treat both APIs as equally valid for production dashboards.
