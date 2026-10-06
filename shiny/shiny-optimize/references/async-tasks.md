# Non-Blocking Operations: ExtendedTask, future, mirai

This is the **last** tool to reach for, not the first. Async doesn't make any
single computation faster — it changes *who waits*. Its two real benefits:
(1) the R process can keep serving **other sessions** while a long task runs,
and (2) with `ExtendedTask`, the **same session** stays interactive while the
user's own task runs. Before anything in this file, make sure elimination
(reactive-graph.md) and caching (caching.md) are exhausted: caching often gives
10–100×; async gives concurrency at the cost of serialization overhead, harder
debugging, and invisible profiling.

## Why blocking hurts: the flush cycle

Shiny's event loop per R process is, roughly:

```
while (TRUE) {
  changes <- get_output_changes()
  changed_outputs <- recompute_all_affected_things(changes)
  send_outputs(changed_outputs)
}
```

- While a session's outputs are executing, **no new input is processed for that
  session**.
- **No output is sent until all outputs in the flush complete** — one slow
  output delays every output in that flush, so the page "hangs" even if only
  one panel is slow.
- R is single-threaded per process: without async, one session's 5-second
  computation blocks **every other user on the same R process** — their clicks
  queue behind it. This is why an app can be fine in dev (one user) and fall
  apart with three.

## The decision path

1. Can the operation be **eliminated** (don't compute what isn't shown)?
2. Can it be **cached** (`bindCache`/`memoise`) so it runs at most once per
   unique input?
3. Can it be **precomputed** offline (data-loading.md)?
4. Is it genuinely a request-time, multi-second, user-specific computation
   (e.g. fitting a model on user-uploaded data, querying an external API)?
   → **Then** async is appropriate.

Rule of thumb: async pays off for "a few big hotspots" — heavy API downloads,
slow DB queries, long model fits. Diffuse small slowness gets *worse* with
async (every task has fixed communication/serialization overhead).

## `ExtendedTask` (Shiny ≥ 1.8.1): the recommended pattern

`ExtendedTask` splits a reactive computation into "decide when to run with what
parameters" and "receive the result", running the work in a background process
so the reactive graph reaches equilibrium each tick and the session stays
responsive.

The complete pattern (with `bslib::input_task_button`):

```r
library(shiny)
library(bslib)
library(future)      # or library(mirai) — see backends below

future::plan(multisession)    # REQUIRED: promises without workers still block

ui <- page_fluid(
  input_task_button("fetch", "Fetch data"),
  plotOutput("plot")
)

server <- function(input, output, session) {
  # 1. Declare the task: a function that RETURNS a promise.
  #    Nothing reactive can happen inside the worker body!
  task_fetch <- ExtendedTask$new(function(data_type) {
    future_promise({
      fetch_from_slow_api(data_type)     # runs in a worker process
    })
  }) |>
    bind_task_button("fetch")            # 3. bind to the task button

  # 2. Invoke from an observer — values are snapshotted here, at invoke time
  observeEvent(input$fetch, {
    task_fetch$invoke(input$data_type)
  })

  # 3. Consume the result reactively — re-executes when the task finishes
  data <- reactive({
    task_fetch$result()
  })

  output$plot <- renderPlot({ plot(data()) })
}
```

Semantics worth knowing cold:

- `ExtendedTask$new(fn)` — `fn` must **return a promise** and must **not read
  reactive values** (Shiny throws if it tries). Everything the task needs is
  passed to `$invoke(...)` and eagerly snapshotted at that moment — inputs may
  have changed by the time the worker starts.
- `$invoke()` does **not** overlap with itself: invoking while running
  **queues** the second call. `input_task_button` prevents accidental
  double-clicks (it disables itself while running); plain `actionButton` does
  not integrate with `bind_task_button()`.
- `$status()` — reactive read: `"initial" | "running" | "success" | "error"`.
- `$result()` — reactive read for consumers: blank (silent exception) before
  the first run; a special "in progress" state while running (this drives the
  busy indicators); the resolved **value** on success (not a promise); the
  error is re-raised in the consuming output on failure. **Don't wrap
  `result()` in `observeEvent`/`eventReactive`/`bindEvent`/`isolate()`** — its
  invalidations are the mechanism.
- Declare the task at the **top level of the server function** → one task
  instance per session. Declare at the top level of `app.R` → **shared across
  all visitors** (rarely what you want; also means one user's invocation state
  is everyone's).
- Multiple distinct ExtendedTasks run concurrently with each other and with
  reactive code.
- `bind_task_button(task, "btn")` can also drive an arbitrary button's busy
  state; `bslib::busyIndicatorOptions()` styles it.

## Worker backends: `future` and `mirai`

- **future + promises** (classic): `future::plan(multisession)` spawns worker
  R processes; `future_promise({...})` runs the body there and returns a
  promise. Worker count = concurrent long tasks; each worker is a full R
  process (RAM!). `plan(sequential)` (the default if you forget) runs the task
  synchronously — the "async" is fake and everything still blocks.
- **mirai** (newer, recommended for new work): event-driven promises —
  resolution triggers immediately on completion instead of being polled, for
  lower latency and much higher scalability (thousands of simultaneous
  promises). Drop-in where `future_promise()` is accepted:
  ```r
  library(mirai)
  daemons(4)                          # 4 local workers, top of app.R
  onStop(function() mirai::daemons(0))   # clean shutdown

  task <- ExtendedTask$new(function(x) mirai({ slow(x) }, x = x)) |>
    bind_task_button("go")
  ```
  Daemons can also be remote hosts for true horizontal scaling.
- **crew** builds on mirai: managed worker pools with auto-scaling — reach for
  it when tasks need lifecycle management beyond simple daemons.

## Hard rules for worker code

1. **No reactive reads inside the worker body.** Read reactives in the main
   process and pass values as named arguments:
   ```r
   # Wrong: reactive reads can't cross processes
   future_promise({ filter(data(), state == input$state) })
   # Right
   st <- input$state
   future_promise({ filter(data(), state == st) }, st = st, data = data)
   ```
   (In ExtendedTask this is enforced — pass via `$invoke()`.)
2. **`session` is off-limits in workers** for the same reason.
3. **Plotting/printing happens in the main process**, in a `then()` handler —
   graphics devices in workers go nowhere:
   ```r
   output$plot <- renderPlot({
     mirai({ prep_data(df) }, df = df()) |>
       then(\(d) ggplot(d, aes(x, y)) + geom_point())
   })
   ```
4. **The promise (or its pipeline) must be the last expression** of the
   reactive/observer/render body — that's how Shiny knows when the work is done.
5. **Observers mutate reactive values inside handlers**: `mirai(...) |> then(\(d)
   rv$done(d))`, never inside the worker.
6. **Serialization costs are real**: arguments and results are copied
   to/from workers. Don't ship 2 GB data frames to a worker to add a column;
   restructure or use a database instead.
7. **Async reactives cache the promise**; downstream consumers chain `then()`.
8. profvis can't see inside workers — profile synchronous code first, convert
   the proven hotspot after.

## Async reactives/observers (pre-ExtendedTask style)

`reactive({ future_promise({...}) |> then(...) })` still works (Shiny ≥ 1.1.0)
and unblocks **other sessions** — but not the current one, because the
session's flush waits for the promise's dependent outputs. It remains useful
when the result must live in the reactive graph but no user-facing task button
makes sense. ExtendedTask is the better default; go raw-promises only when
ExtendedTask can't express the flow.

## UI expectations to set with the user

- `input_task_button` shows a busy state and disables itself — users get
  feedback instead of a frozen app.
- While a task runs, the rest of the app (sliders, other tabs, even a ticking
  clock output) stays live. Verify with an `invalidateLater(1000)` clock if
  unsure.
- Busy indicators for *outputs* (see rendering-ui.md) complement task buttons:
  buttons for triggered work, spinners for render-time work.
