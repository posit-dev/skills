# Rendering, Layout, and Perceived Performance

What the app renders and when is both a real cost (server work, serialization,
browser work) and a perceived one. Layout changes are among the cheapest fixes
because hidden outputs don't compute.

## Output suspension: hidden outputs don't run (use tabs!)

Every output defaults to `suspendWhenHidden = TRUE`: when not visible —
unselected tab, hidden `conditionalPanel`, `display: none` — Shiny suspends it
and, because reactives are lazy, its entire upstream chain stays unevaluated.

- **Put expensive outputs behind tabs/navs** (`tabsetPanel()`, bslib's
  `nav_panel()`/`navset_tab()`, or `conditionalPanel()` — a client-side
  condition with no server round trip). A landing page with 8 heavy plots
  computes all 8 before the app is usable; the same plots across tabs compute
  only the visible one. Pure layout change — same outputs, same logic.
- **Escape hatch**: `outputOptions(output, "x", suspendWhenHidden = FALSE)`
  keeps a hidden output warm (e.g. it feeds another output). Use sparingly.
- Suspension gates the *output*, not shared reactives — a reactive used by
  several visible outputs still runs; that's what shared-reactive + cache
  fixes are for.

## Gate speculative outputs

- `req()` at the top keeps outputs silent until inputs are meaningful
  (reactive-graph.md).
- For expensive results users only sometimes want, require an explicit
  trigger: `actionButton` + `bindEvent(input$go)`.
- **Remove dead outputs**: an `output$` nothing displays still costs server
  execution and websocket traffic per flush.

## `renderUI()` vs `update*Input()`

`renderUI()`/`uiOutput()` rebuild DOM and re-bind inputs on every regeneration
— flicker plus real overhead. For routine updates, patch the existing input:

```r
# Instead of renderUI-ing a new selectInput each time choices change:
updateSelectInput(session, "city", choices = cities_for(input$country))
```

Move pure display toggles to CSS/shinyjs (client-side) to avoid server round
trips. Keep `renderUI` for genuinely structural UI.

## Plots: choose the right renderer for the data size

Two cost classes: **build time** (R serializes to JSON/HTML) and **run time**
(browser rendering).

**`renderPlot()` (static PNG)** — cheap in the browser regardless of point
count; cost is server-side rendering + PNG transfer. Composes with
`bindCache()`. The default for dashboards.

**plotly (`renderPlotly()`)** — pays JSON serialization of *all* data at build
time plus browser rendering. With big data:

- `plotly::toWebGL(p)` (or `type = "scattergl"`) — WebGL/canvas instead of
  SVG. Rule of thumb: **> ~10k points → WebGL**.
- `plotly::partial_bundle()` — shrink the ~3 MB plotly.js bundle under 1 MB
  for scatter/bar/pie pages (one bundle per page).
- **Proxies instead of redraws**: `plotlyProxy("id", session) |>
  plotlyProxyInvoke("restyle"|"addTraces"|"relayout", ...)` updates the
  existing plot client-side instead of re-executing `renderPlotly()`.
- Pre-aggregate before plotting (hexbin instead of scatter points).

**`renderImage()`** for pre-rendered images avoids server-side rendering
entirely.

## Tables: DT server-side processing

- `DT::renderDT()` defaults to **server-side processing** — keep it for large
  tables. `server = FALSE` ships the entire dataset to the browser and renders
  slowly.
- Update without a full redraw: `dataTableProxy()` +
  `DT::replaceData(proxy, newData)` replaces values while **preserving
  sort/filter/page state** — cheaper and better UX than re-rendering.

## Perceived performance: make waiting feel shorter

- **`bslib::useBusyIndicators()`** — automatic spinners while Shiny
  recalculates; customize with `busyIndicatorOptions()`.
- **`input_task_button()`** for triggered long operations — pairs with
  ExtendedTask (async-tasks.md), which runs the work off the R process so a
  slow-to-compute output no longer blocks the rest of the app.
- **`withProgress()` / `Progress`** for multi-step operations — progress bars
  make operations feel faster.
- **Let the UI render first**: render the shell immediately and stream results
  in, rather than blocking on data before first paint.

## Quick reference

| Lever | Effect | Cost |
|---|---|---|
| Tabs/navs (`navset_tab`, `tabsetPanel`) | Hidden outputs don't compute | Pure layout change |
| `req()` gating | Nothing computes until inputs ready | One line per output |
| `bindEvent(input$go)` | Compute only on explicit trigger | Small refactor |
| `update*Input()` over `renderUI` | No DOM rebuild/rebind per update | Small refactor |
| `DT` server-side + `replaceData()` | Browser holds one page; no full redraws | Small refactor |
| WebGL/bundles/proxies for plotly | Big-data interactive plots stay usable | Small refactor |
| Busy indicators/task buttons/progress | Waiting feels shorter | Trivial |
| Task button + `ExtendedTask` | Slow compute no longer blocks the rest of the app | Medium refactor (async-tasks.md) |
