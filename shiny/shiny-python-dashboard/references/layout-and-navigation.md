# Layout, Sidebar, and Navigation

## Contents
- Choosing the right page layout
- Sidebar patterns
- Navigation between panels
- Two-level navigation hierarchy

---

## Choosing the right page layout

### `ui.page_sidebar` — Global sidebar controlling all content

Use when a single sidebar of filters drives all outputs on one page.
**Always set `fillable=True`** so content fills the viewport.

```python
# Core
app_ui = ui.page_sidebar(ui.sidebar(...), title="My Dashboard", fillable=True)
# Express
ui.page_opts(title="My Dashboard", fillable=True)
with ui.sidebar(): ...
```

### `ui.page_navbar` — Multi-page navigation via top navbar

Use when the app has distinct pages/sections the user switches between.
**Never use emojis in nav panel titles** — use plain text only.

```python
# Core
app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_panel("Overview", page1),
    ui.nav_panel("Details", page2),
    title="My App",
    fillable=True,
)
```

```python
# Express
ui.page_opts(title="My App", fillable=True)
ui.nav_spacer()
with ui.nav_panel("Overview"): ...
with ui.nav_panel("Details"): ...
```

`ui.nav_spacer()` pushes subsequent nav items to the right in the navbar.

---

## Sidebar patterns

Place all primary filter inputs inside `ui.sidebar()`.

```python
# Core
ui.sidebar(
    ui.input_selectize("ticker", "Stock", choices=stocks, selected="AAPL"),
    ui.input_slider("bill", "Amount", min=0, max=100, value=[10, 90], pre="$"),
    ui.input_checkbox_group("time", "Service", ["Lunch", "Dinner"],
        selected=["Lunch", "Dinner"], inline=True),
    ui.input_date_range("dates", "Dates", start=start, end=end),
    ui.input_switch("group", "Group by species", value=True),
    ui.input_action_button("reset", "Reset filter"),
    open="desktop",  # auto-collapse on mobile
)
```

```python
# Express
with ui.sidebar(open="desktop"):
    ui.input_selectize("ticker", "Stock", choices=stocks, selected="AAPL")
    ui.input_slider("bill", "Amount", min=0, max=100, value=[10, 90], pre="$")
    ui.input_action_button("reset", "Reset filter")
```

### Key rules

- Use `open="desktop"` to auto-collapse the sidebar on mobile viewports.
- Group filters logically — filters first, reset button last.
- Sidebar inputs drive `@reactive.calc` functions that filter/transform data.
- Common input types in sidebars: `input_select`, `input_selectize`, `input_slider`,
  `input_checkbox_group`, `input_date_range`, `input_switch`, `input_action_button`.

---

## Navigation between panels

### Two-level navigation hierarchy

Combine `page_navbar` (top-level pages) with `navset_card_underline` (sub-tabs within a page):

```python
# Core — nested navigation
page1 = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("hist")),
    ui.nav_panel("Table", ui.output_data_frame("data")),
    footer=ui.input_select("var", "Variable", choices=["col_a", "col_b"]),
    title="Data explorer",
)

app_ui = ui.page_navbar(
    ui.nav_panel("Page 1", page1),
    ui.nav_panel("Page 2", "Second page content."),
    title="My App",
)
```

```python
# Express — nested navigation
with ui.nav_panel("Page 1"):
    footer = ui.input_select("var", "Variable", choices=["col_a", "col_b"])
    with ui.navset_card_underline(title="Data explorer", footer=footer):
        with ui.nav_panel("Plot"):
            @render.plot
            def hist(): ...
        with ui.nav_panel("Table"):
            @render.data_frame
            def data(): ...

with ui.nav_panel("Page 2"):
    "Second page content."
```

### Key rules

- The `footer` kwarg on `navset_card_underline` places shared inputs **below all
  sub-tabs**, keeping them visible regardless of which tab is active.
- In Core, define navset content as a variable (e.g., `page1`), then pass into
  `ui.nav_panel()`.
- In Express, define the `footer` input widget **before** the
  `with ui.navset_card_underline(...)` block so it can be passed as a kwarg.
- `ui.nav_spacer()` pushes navbar items to the right for visual alignment.
- No sidebar is used in basic-navigation apps — inputs live in the navset card's footer.
