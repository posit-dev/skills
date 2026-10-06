# Rendering, Layout, and Perceived Performance

What the app *renders* and *when* is both a real performance cost (server work,
serialization, browser work) and a perceived one (spinners, tabs). This file
covers both. Layout changes are among the cheapest fixes available because
Shiny already has the machinery — hidden outputs don't compute.

## Output suspension: hidden outputs don't run (use tabs!)

By default, every output has `suspendWhenHidden = TRUE`: when it's not
visible — on an unselected tab, inside a hidden `conditionalPanel`, or
`display: none` — Shiny **suspends** it and it does not execute. Because
reactives are lazy, a suspended output's entire upstream reactive chain stays
unevaluated too. Mastering Shiny's advice is simply: "Split your app up into
tabs, using `tabsetPanel()`. Only outputs on the current tab are recomputed."

Practical consequences:

- **Put expensive outputs behind tabs/navs.** A landing page with 8 heavy
  plots computes all 8 before the app is usable; the same 8 plots across
  `navset_tab()`/`tabsetPanel()` tabs compute only the visible one. This is a
  pure layout change — same outputs, same logic.
- This applies to `tabsetPanel()`, bslib's `nav_panel()`/`navset_tab()`, and
  `conditionalPanel()` (client-side JS condition — no server round trip to
  hide/show).
- **Escape hatch**: if a hidden output must stay warm (e.g. it feeds another
  output), `outputOptions(output, "x", suspendWhenHidden = FALSE)` forces
  evaluation. Use sparingly — it removes the free win.
- Note: suspension gates the *output*, not shared reactives. A reactive that
  several visible outputs use still runs; that's what shared-reactive + cache
  fixes are for (reactive-graph.md, caching.md).

## Gate speculative outputs

- **`req()` at the top** keeps outputs silent (and cheap) until inputs are
  meaningful — the standard fix for "everything computes at startup with empty
  inputs" (reactive-graph.md).
- **Button/checkbox gating**: for expensive results users only sometimes want,
  require an explicit trigger (`actionButton` + `bindEvent(input$go)`) instead
  of computing speculatively on every input change.
- **Remove dead outputs**: every `output$` that nothing displays still costs
  server execution per invalidation and websocket traffic per flush. Search
  the UI for outputs that were disconnected during development.

## `renderUI()` vs `update*Input()`

`renderUI()`/`uiOutput()` rebuild DOM and re-bind inputs on every regeneration
— flicker on reload and real overhead as dynamic elements multiply. For
routine updates:

```r
# Instead of renderUI-ing a new selectInput each time choices change:
updateSelectInput(session, "city", choices = cities_for(input$country))
```

- Prefer `update*Input()` functions, which patch the existing input in place.
- Move pure display toggles to CSS/shinyjs (client-side) to avoid server round
  trips entirely.
- Keep `renderUI` for genuinely structural UI, and remember outputs inside
  dynamically-rendered UI don't exist until the UI renders.

## Plots: choose the right renderer for the data size

Two cost classes for interactive graphics: **build time** (R serializes the
object to JSON/HTML) and **run time** (the browser renders it).

**`renderPlot()` (static PNG)** — cheap in the browser regardless of point
count; cost is server-side rendering + PNG transfer. Composes with
`bindCache()` so repeated identical plots are served from cache. The default
choice for dashboards; it also can't be slowed down by the client's machine.

**plotly (`renderPlotly()`)** — pays JSON serialization of *all* data at build
time plus browser rendering at run time. Worth it for interactivity, costly at
scale. When you must use plotly with big data:

- `plotly::toWebGL(p)` (or `type = "scattergl"` traces) — render via
  WebGL/canvas instead of SVG, which "doesn't scale in the number of vectors".
  Rule of thumb: **> ~10k points → WebGL**.
- `plotly::partial_bundle()` — shrink the ~3 MB plotly.js bundle to < 1 MB for
  scatter/bar/pie pages. One bundle per page; multiple bundles on one page can
  conflict.
- **Proxies instead of redraws**: `plotlyProxy("id", session) |>
  plotlyProxyInvoke("restyle"|"addTraces"|"relayout", ...)` updates an existing
  plot client-side instead of re-executing `renderPlotly()` — avoiding both
  build and full run-time cost.
- Pre-aggregate large data before plotting (hexbin instead of scatter points,
  summarization for huge series).

**`renderImage()`** for pre-rendered images avoids server-side rendering
entirely when figures can be generated ahead of time.

Real-world order of magnitude: one app swapped 15 Plotly charts for
echarts4r and cut load time 30 s → 6 s — canvas-class libraries dramatically
outperform SVG rendering on large data. (echarts4r is a dependency decision —
ask before introducing it.)

## Tables: DT server-side processing

- `DT::renderDT()` defaults to **server-side processing** — keep it for large
  tables. `server = FALSE` ships the entire dataset to the browser: "when the
  data object is relatively large, do not use `server = FALSE`, otherwise it
  will be too slow to render the table in the web browser".
- Update without a full redraw: `dataTableProxy()` + `DT::replaceData(proxy,
  newData)` replaces values while **preserving sort/filter/page state** — much
  cheaper than re-rendering the table and better UX.
- Pagination + server-side processing means the browser only ever holds the
  visible page.

## Perceived performance: make waiting feel shorter

When computation genuinely takes time, the *experience* of waiting is a
performance problem you can fix without touching the computation:

- **`bslib::useBusyIndicators()`** — automatic spinners while Shiny recalculates.
  Customize with `busyIndicatorOptions(spinner_type = ..., spinner_color = ...)`,
  or target specific cards with `spinner_selector = ".my-card-class"`.
- **`input_task_button()`** for triggered long operations (pairs with
  ExtendedTask, async-tasks.md) — disabled + "Processing…" state while running.
- **`withProgress()` / `Progress`** for multi-step operations — incremental
  progress bars "make operations feel faster".
- **Let the UI render first**: if startup work is unavoidable, render the
  shell immediately and stream results in, rather than blocking on data before
  first paint.
- A spinner demo worth internalizing: a 3 s task with a spinner (appearing
  after ~500 ms) feels *faster* than the same task without one.

## Quick reference: output cost levers

| Lever | Effect | Cost |
|---|---|---|
| Tabs/navs (`navset_tab`, `tabsetPanel`) | Hidden outputs don't compute | Pure layout change |
| `req()` gating | Nothing computes until inputs ready | One line per output |
| `bindEvent(input$go)` | Compute only on explicit trigger | Small refactor |
| `suspendWhenHidden = FALSE` | Keeps hidden output warm | Deliberate opt-*out* |
| `update*Input()` over `renderUI` | No DOM rebuild/rebind per update | Small refactor |
| `DT` server-side + `replaceData()` | Browser holds one page; no full redraws | Small refactor |
| WebGL/bundles/proxies for plotly | Big data interactive plots stay usable | Small refactor |
| Busy indicators/task buttons/progress | Waiting feels shorter | Trivial |
