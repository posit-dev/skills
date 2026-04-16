# Components for Shiny for Python Dashboards

This reference covers the card-level building blocks of a Shiny for Python dashboard: cards, value boxes, accordions, and lightweight contextual UI such as tooltips and popovers.

## Cards

Cards are the default container for dashboard content.

```python
ui.card(
    ui.card_header("Revenue by month"),
    ui.output_plot("revenue_plot"),
    ui.card_footer("Updated daily at 6am"),
    full_screen=True,
)
```

Use cards for:

- charts
- tables
- maps
- summaries that need supporting text
- module-like dashboard sections

Guidelines:

- Add `ui.card_header()` to every card.
- Default to `full_screen=True` for charts, maps, and tables.
- Use `ui.card_footer()` for provenance, notes, or small actions.
- Keep static text cards shorter than plot cards; large paragraphs belong in scrolling pages, not dashboard grids.

### Card headers with inline controls

Card headers can hold small secondary controls.

```python
ui.card_header(
    "Bill vs tip",
    ui.popover(
        icon_svg("ellipsis"),
        ui.input_radio_buttons("color_var", None, ["none", "sex", "day"], inline=True),
        title="Color by",
        placement="top",
    ),
    class_="d-flex justify-content-between align-items-center",
)
```

Use this for secondary options that do not deserve a full sidebar section.

## Value Boxes

Use `ui.value_box()` for KPIs and headline metrics.

**Core API:**

```python
ui.layout_columns(
    ui.value_box(
        "Total users",
        ui.output_ui("total_users"),
        showcase=icon_svg("users"),
        theme="primary",
    ),
    ui.value_box(
        "Average order",
        ui.output_ui("avg_order"),
        showcase=icon_svg("wallet"),
        theme="success",
    ),
    fill=False,
)
```

**Express API:**

```python
with ui.layout_columns(fill=False):
    with ui.value_box(showcase=icon_svg("users"), theme="primary"):
        "Total users"

        @render.express
        def total_users():
            f"{len(df):,}"
```

Guidelines:

- Keep the row to 3 or 4 boxes.
- Use named themes like `"primary"`, `"success"`, `"info"`, `"warning"`, and `"danger"`.
- Use icons that reinforce the metric; do not use emojis.
- Format the displayed value instead of passing a raw float or integer.

### Dynamic showcase icons

Use `@render.ui` when the icon depends on the data.

```python
@render.ui
def change_icon():
    icon = icon_svg("arrow-up" if get_change() >= 0 else "arrow-down")
    icon.add_class("text-success" if get_change() >= 0 else "text-danger")
    return icon
```

In Express, `with ui.hold():` is useful when an output is referenced before it is defined.

## Accordions

Accordions are most useful in sidebars with many controls.

```python
ui.sidebar(
    ui.accordion(
        ui.accordion_panel(
            "Filters",
            ui.input_selectize("species", "Species", choices=species),
            ui.input_date_range("dates", "Dates", start=start, end=end),
        ),
        ui.accordion_panel(
            "Display",
            ui.input_switch("show_trend", "Show trend", value=True),
            ui.input_slider("bins", "Bins", min=5, max=50, value=20),
        ),
        open=["Filters"],
    ),
    open="desktop",
)
```

Use accordions when:

- the sidebar has more than a handful of inputs
- some controls are clearly advanced or optional
- you want to reduce visual clutter on smaller screens

Keep related inputs together and leave only the most important panel open by default.

## Tooltips and Popovers

Tooltips provide quick read-only help. Popovers hold small interactive controls.

```python
ui.tooltip(
    icon_svg("circle-info", title="More information", a11y="sem"),
    "Shows how the metric is calculated",
)
```

```python
ui.popover(
    icon_svg("gear", title="Chart options", a11y="sem"),
    ui.input_select("palette", "Palette", choices=palettes),
    ui.input_switch("show_trend", "Show trend line", value=True),
    title="Chart options",
)
```

Guidelines:

- Use tooltips for one short explanation.
- Use popovers for 2 to 4 small controls.
- Give icon-only triggers accessible titles so screen readers have a useful label.
- Do not use popovers as a substitute for a real form or a full advanced-settings workflow.

## Toast-like Feedback

Use the framework's notification helpers for lightweight success, warning, or error feedback instead of permanently allocating screen space to ephemeral status messages.

Guidelines:

- Use notifications for completion, failure, or "export started" states.
- Keep them specific instead of saying only "Done".
- Reserve persistent on-page status areas for information users need to keep reading.

## Best Practices

1. Treat cards as the default dashboard container.
2. Use value boxes for headline metrics, not for long explanations.
3. Keep chart options in card-header popovers when they are secondary.
4. Group busy sidebars with accordions.
5. Give icon-only triggers accessible titles.
6. Avoid card-within-card compositions unless you are intentionally creating a nested layout.
