# Rendering, Layout, and Perceived Performance

What the app renders and when is both a real cost (server work, serialization,
browser work) and a perceived one. Layout changes are among the cheapest fixes
because hidden outputs are suspended.

## Output suspension: hidden outputs don't run (use tabs!)

Every output is suspended while not visible — unselected tab, hidden
container. Because calcs and outputs are lazy, a suspended output's entire
upstream chain stays unevaluated.

- **Put expensive outputs behind tabs/navs** (`ui.navset_tab()`,
  `ui.navset_pill()`/`navset_card_tab()` with `ui.nav_panel()`, or
  `ui.panel_conditional()` for client-side toggles with no server round
  trip). A landing page with 8 heavy plots computes all 8 before the app is
  usable; the same plots across tabs compute only the visible one. Pure
  layout change — same outputs, same logic.
- Suspension gates the *output*, not shared calcs — a calc used by several
  visible outputs still runs; that's what shared-calc + cache fixes are for
  (reactive-graph.md, caching.md).

## Gate speculative outputs

- `req()` at the top keeps outputs silent until inputs are meaningful
  (reactive-graph.md).
- For expensive results users only sometimes want, require an explicit
  trigger: `ui.input_action_button("go", "Compute")` + `@reactive.event(input.go)`.
- **Remove dead outputs**: a `@render.*` with no visible placeholder still
  costs server execution and websocket traffic per flush.

## `@render.ui` vs `ui.update_*()`

`@render.ui` rebuilds DOM and re-binds inputs on every regeneration —
flicker plus real overhead. For routine updates, patch the existing input:

```python
# Instead of render.ui-ing a new ui.input_select each time choices change:
@reactive.effect
def _():
    ui.update_select("city", choices=cities_for(input.country()))
```

Move pure display toggles to client-side CSS/`ui.panel_conditional` to avoid
server round trips. Keep `@render.ui` for genuinely structural UI.

## Plots: choose the right renderer for the data size

Two cost classes: **build time** (server serializes to PNG or JSON) and
**run time** (browser rendering).

**`@render.plot` (static PNG)** — matplotlib/seaborn/plotnine figures are
rendered server-side and shipped as an image; cheap in the browser regardless
of point count. The default for dashboards. Build and return a `Figure`
object (the pyplot global interface is unsafe in async renderers); set
display size with `ui.output_plot(width=, height=)` (CSS) and avoid forcing
pixel sizes on the renderer unless caching sizes.

**Plotly via shinywidgets** — pays JSON serialization of *all* data at build
time plus browser rendering. With big data:

- Prefer WebGL traces (`Scattergl` / `"mode": "markers"` with `scattergl`)
  — rule of thumb **> ~10k points → WebGL**.
- **Pre-aggregate before plotting** (hexbin/bins instead of raw points) —
  aggregation is cheaper than shipping points.
- Plotly re-renders the whole chart on each invalidation; prefer updating
  what the user sees over re-plotting everything, and cache the underlying
  data so the plot function is cheap.

**`@render.image`** for pre-rendered image files avoids server-side rendering
entirely.

## Tables: `@render.data_frame`, not `@render.table`

- **`@render.table`** renders through pandas' Styler to full HTML — heavy
  serialization and slow browser layout for more than a few hundred rows.
- **`@render.data_frame` with `render.DataGrid`/`render.DataTable`**
  virtualizes rows in the browser and is the right tool for anything sizable.
- Only return the columns the user needs (select before returning; wide
  frames serialize slowly).
- Update without a full re-render: from an effect,
  `await grid.update_data(new_df)` replaces the data while keeping
  sort/filter state.

## Perceived performance: make waiting feel shorter

- **`ui.busy_indicators.use()` / `.options()`** — automatic spinners on
  recalculating outputs and a busy pulse banner; on by default, configurable
  in the UI (not the server).
- **`ui.input_task_button`** for triggered long operations (pairs with
  `@reactive.extended_task`, async-tasks.md).
- **`ui.Progress`** for multi-step operations — progress bars make
  operations feel faster.
- **Let the UI render first**: render the shell immediately and stream
  results in, rather than blocking on data before first paint.
- One slow output holds up the flush that delivers *all* outputs of an
  interaction — gate slow computes behind buttons or extended tasks so fast
  outputs aren't held hostage.

## Quick reference

| Lever | Effect | Cost |
|---|---|---|
| Tabs/navs (`ui.navset_*`, `ui.nav_panel`) | Hidden outputs stay suspended | Pure layout change |
| `req()` gating | Nothing computes until inputs ready | One line per output |
| `@reactive.event(input.go)` | Compute only on explicit trigger | Two lines per output |
| `ui.update_*()` over `@render.ui` | No DOM rebuild/rebind per update | Small refactor |
| `@render.data_frame` over `@render.table` | Virtualized rows, lighter payloads | Small refactor |
| WebGL + pre-aggregation for Plotly | Big interactive plots stay usable | Small refactor |
| Busy indicators/task buttons/progress | Waiting feels shorter | Trivial |
