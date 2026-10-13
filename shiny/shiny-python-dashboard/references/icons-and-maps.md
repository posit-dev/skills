# Icons and Maps in Shiny for Python Dashboards

This reference covers two dashboard details that strongly affect quality: icon usage and geographic views. Both should feel intentional, readable, and easy to expand.

## Icons

Use `faicons.icon_svg()` for dashboard icons.

```python
from faicons import icon_svg

icon_svg("chart-line")
icon_svg("users")
icon_svg("dollar-sign")
icon_svg("globe")
```

Guidelines:

- Never use emoji characters as icons.
- Use icons to reinforce a metric or action, not to decorate every label.
- Keep icon choice semantically close to the content.
- Reuse a small icon vocabulary across the app.

### Accessible icon-only triggers

When an icon is the only visible trigger for a tooltip, popover, or action, mark it as semantic and provide a meaningful title.

```python
ui.tooltip(
    icon_svg("circle-info", title="More information", a11y="sem"),
    "Explains how this value is calculated",
)
```

The title should describe the purpose of the trigger, not the icon itself.

### Common dashboard icons

- `"chart-line"` for trends and time series
- `"chart-bar"` for comparisons
- `"users"` or `"user"` for people counts
- `"dollar-sign"` or `"wallet"` for money metrics
- `"percent"` for ratios and conversion
- `"globe"` or `"map"` for geographic views
- `"table"` for tabular drill-downs
- `"filter"` for filter controls

## Maps

The repo already contains Python dashboard examples with geographic outputs, so the guidance here should be concrete: maps belong in full-screen cards, need explicit height, and depend on clean numeric coordinates.

### Clean coordinates first

```python
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
map_data = df.dropna(subset=["latitude", "longitude"])
```

Do not defer coordinate cleanup to the rendering function if the whole dashboard depends on the map.

### Put maps in full-screen cards

```python
ui.card(
    ui.card_header("Market map"),
    output_widget("market_map", height="540px"),
    full_screen=True,
)
```

Guidelines:

- Give the map an explicit height.
- Use `full_screen=True` so users can inspect dense point layers.
- Keep map controls in the sidebar or a small popover, not spread across the page.
- Remove extra padding when the visual should run edge to edge.

### Match the map to the question

Use the map when users need to answer geographic questions such as:

- where listings cluster
- which neighborhoods command higher prices
- how a filtered subset changes by location
- which points deserve drill-down inspection

If the geography is incidental, use a ranked table or bar chart instead.

### Widget choices

Shiny for Python dashboards in this repo use widget-style geographic outputs, so keep the guidance library-agnostic:

- if the map library returns an interactive widget or figure, place it in a card with explicit height
- if the map shares filters with charts, drive all of them from the same `@reactive.calc` dataset
- keep legends, color scales, and marker size encodings simple enough to read at dashboard scale

## Best Practices

1. Use icons sparingly and consistently.
2. Add `a11y="sem"` and a useful `title` for icon-only triggers.
3. Clean latitude and longitude before building map outputs.
4. Put maps in full-screen cards with explicit height.
5. Use maps only when location materially changes the analysis.
