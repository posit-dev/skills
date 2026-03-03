# Icons with faicons and Interactive Maps

## Contents

- Using faicons for icons
- Icon patterns: static, dictionary, dynamic
- Icons as popover triggers
- Interactive maps with ipyleaflet
- Map markers, layers, and basemaps
- Draggable markers with reactive updates

---

## Using faicons

The `faicons` package provides Font Awesome SVG icons for Shiny for Python.
Add `faicons` to `requirements.txt`.

### CRITICAL: Never use emoji characters as icons

Emojis are NOT icons. They render differently across platforms, cannot be styled
with CSS, and look unprofessional in dashboards. ALWAYS use `icon_svg()` from
faicons or Bootstrap Icons via `ui.HTML()`.

```python
# CORRECT
from faicons import icon_svg
showcase = icon_svg("chart-line")
showcase = icon_svg("hospital")
showcase = icon_svg("users")

# WRONG — never do this
showcase = "\U0001F4CA"   # chart emoji — NO
showcase = "\U0001F3E5"   # hospital emoji — NO
showcase = "\U0001F465"   # people emoji — NO
```

### Import styles

```python
# Option A: namespace import (dashboard-tips pattern)
import faicons as fa
icon = fa.icon_svg("user", "regular")

# Option B: direct import (stock-app, map-distance pattern)
from faicons import icon_svg
icon = icon_svg("dollar-sign")
```

### Static icons in value boxes

Pass `icon_svg()` directly to the `showcase` parameter:

```python
# Core
ui.value_box("Current Price", ui.output_ui("price"),
    showcase=icon_svg("dollar-sign"))

# Express
with ui.value_box(showcase=icon_svg("dollar-sign")):
    "Current Price"
    @render.ui
    def price(): return f"{close.iloc[-1]:.2f}"
```

### Icon dictionary pattern

Pre-build icons in a dict when reusing across multiple components (value boxes + popovers).
This avoids repeated `icon_svg()` calls:

```python
ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "wallet": fa.icon_svg("wallet"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),
}
```

Then reference by key:

```python
ui.value_box("Total tippers", ui.output_ui("total_tippers"),
    showcase=ICONS["user"])
```

### Dynamic / conditional icons

Render icons conditionally via `@render.ui`. Use `.add_class()` to style with
Bootstrap text-color utilities:

```python
# Core
ui.value_box("Change", ui.output_ui("change"),
    showcase=ui.output_ui("change_icon"))

@render.ui
def change_icon():
    icon = icon_svg("arrow-up" if get_change() >= 0 else "arrow-down")
    icon.add_class(f"text-{'success' if get_change() >= 0 else 'danger'}")
    return icon
```

In Express, use `ui.hold()` for the forward-referenced output:

```python
from shiny.ui import output_ui

with ui.value_box(showcase=output_ui("change_icon")):
    "Change"
    @render.ui
    def change(): return f"${get_change():.2f}"

with ui.hold():
    @render.ui
    def change_icon():
        icon = icon_svg("arrow-up" if get_change() >= 0 else "arrow-down")
        icon.add_class(f"text-{'success' if get_change() >= 0 else 'danger'}")
        return icon
```

### Icons as popover triggers

Use an icon (typically `"ellipsis"`) as the trigger for a popover containing
secondary inputs:

```python
ui.card_header(
    "Total bill vs tip",
    ui.popover(
        ICONS["ellipsis"],  # trigger icon
        ui.input_radio_buttons("color", None, ["none", "sex", "day"], inline=True),
        title="Add a color variable",
        placement="top",
    ),
    class_="d-flex justify-content-between align-items-center",
)
```

### Common icon names

| Icon name            | Typical use                 |
|----------------------|-----------------------------|
| `"user"`             | Count / people metrics      |
| `"users"`            | Groups / team size          |
| `"wallet"`           | Money / tip metrics         |
| `"dollar-sign"`      | Currency / price            |
| `"percent"`          | Percentage values           |
| `"ellipsis"`         | Popover / settings trigger  |
| `"arrow-up"`         | Positive change indicator   |
| `"arrow-down"`       | Negative change indicator   |
| `"chart-line"`       | Trends / time series        |
| `"chart-bar"`        | Bar charts / distributions  |
| `"globe"`            | Geographic / distance       |
| `"ruler"`            | Measurement                 |
| `"mountain"`         | Altitude / elevation        |
| `"database"`         | Data / records              |
| `"clipboard-check"`  | Completed tasks             |
| `"calendar"`         | Dates / scheduling          |
| `"flask"`            | Science / experiments       |
| `"stethoscope"`      | Healthcare                  |
| `"heart-pulse"`      | Health metrics              |
| `"hospital"`         | Healthcare facility         |
| `"pills"`            | Medications / pharma        |
| `"vial"`             | Lab samples                 |
| `"building"`         | Organizations               |
| `"truck"`            | Shipping / logistics        |
| `"filter"`           | Filtering                   |
| `"table"`            | Tabular data                |
| `"magnifying-glass"` | Search                      |
| `"circle-check"`     | Success / completion        |
| `"clock"`            | Time / duration             |

Pass `"regular"` as second arg for outlined style: `icon_svg("user", "regular")`.
Default style is `"solid"`.

---

## Interactive maps with ipyleaflet

The `map-distance` app demonstrates interactive maps using `ipyleaflet` rendered
through `shinywidgets`. Add to `requirements.txt`:

```txt
ipyleaflet
shinywidgets
geopy        # for distance calculations
requests     # for elevation API lookups
```

### Basic map rendering

Use `@render_widget` from `shinywidgets` to render an ipyleaflet `Map`:

```python
# Core
from shinywidgets import output_widget, render_widget
import ipyleaflet as L

# In UI
output_widget("map")

# In server
@render_widget
def map():
    m = L.Map(zoom=4, center=(0, 0))
    m.add_layer(L.basemap_to_tiles(BASEMAPS["WorldImagery"]))
    return m
```

```python
# Express
from shinywidgets import render_widget

@render_widget
def map():
    m = L.Map(zoom=4, center=(0, 0))
    m.add_layer(L.basemap_to_tiles(BASEMAPS[input.basemap()]))
    return m
```

### Basemap configuration

Define available basemaps in `shared.py`:

```python
from ipyleaflet import basemaps

BASEMAPS = {
    "WorldImagery": basemaps.Esri.WorldImagery,
    "Mapnik": basemaps.OpenStreetMap.Mapnik,
    "Positron": basemaps.CartoDB.Positron,
    "DarkMatter": basemaps.CartoDB.DarkMatter,
}
```

Let users switch via `ui.input_selectize("basemap", "Choose a basemap", choices=list(BASEMAPS.keys()))`.

### Partial map updates with reactive effects

Render the map **once**, then update layers incrementally via `@reactive.effect`
and helper functions. Access the underlying widget via `map.widget`:

```python
@reactive.effect
def _():
    update_marker(map.widget, loc1xy(), on_move1, "loc1")

@reactive.effect
def _():
    update_marker(map.widget, loc2xy(), on_move2, "loc2")

@reactive.effect
def _():
    update_line(map.widget, loc1xy(), loc2xy())
```

### Layer management helpers

Name layers so they can be found and replaced:

```python
def update_marker(map: L.Map, loc: tuple, on_move: object, name: str):
    remove_layer(map, name)
    m = L.Marker(location=loc, draggable=True, name=name)
    m.on_move(on_move)
    map.add_layer(m)

def update_line(map: L.Map, loc1: tuple, loc2: tuple):
    remove_layer(map, "line")
    map.add_layer(
        L.Polyline(locations=[loc1, loc2], color="blue", weight=2, name="line")
    )

def remove_layer(map: L.Map, name: str):
    for layer in map.layers:
        if layer.name == name:
            map.remove_layer(layer)

def update_basemap(map: L.Map, basemap: str):
    for layer in map.layers:
        if isinstance(layer, L.TileLayer):
            map.remove_layer(layer)
    map.add_layer(L.basemap_to_tiles(BASEMAPS[basemap]))
```

### Draggable markers with input sync

When a marker is dragged, update a `selectize` input so the new coordinates flow
back through the reactive graph:

```python
def on_move1(**kwargs):
    return on_move("loc1", **kwargs)

def on_move(id, **kwargs):
    loc = kwargs["location"]
    loc_str = f"{loc[0]}, {loc[1]}"
    choices = city_names + [loc_str]
    ui.update_selectize(id, selected=loc_str, choices=choices)
```

### Fit bounds reactively

Auto-zoom to show both markers when they move outside the current viewport:

```python
@reactive.effect
def _():
    l1, l2 = loc1xy(), loc2xy()
    lat_rng = [min(l1[0], l2[0]), max(l1[0], l2[0])]
    lon_rng = [min(l1[1], l2[1]), max(l1[1], l2[1])]
    new_bounds = [[lat_rng[0], lon_rng[0]], [lat_rng[1], lon_rng[1]]]

    b = map.widget.bounds
    if len(b) == 0 or (
        lat_rng[0] < b[0][0] or lat_rng[1] > b[1][0] or
        lon_rng[0] < b[0][1] or lon_rng[1] > b[1][1]
    ):
        map.widget.fit_bounds(new_bounds)
```

### Distance calculations with geopy

```python
from geopy.distance import geodesic, great_circle

@render.text
def great_circle_dist():
    circle = great_circle(loc1xy(), loc2xy())
    return f"{circle.kilometers.__round__(1)} km"

@render.text
def geo_dist():
    dist = geodesic(loc1xy(), loc2xy())
    return f"{dist.kilometers.__round__(1)} km"
```

### Value box theming for maps

Use named Bootstrap themes for value boxes — avoid gradient themes:

```python
ui.value_box("Great Circle Distance", ui.output_text("great_circle_dist"),
    theme="primary", showcase=icon_svg("globe"))

ui.value_box("Geodesic Distance", ui.output_text("geo_dist"),
    theme="info", showcase=icon_svg("ruler"))
```

Available themes: `"primary"`, `"success"`, `"info"`, `"warning"`, `"danger"`.
