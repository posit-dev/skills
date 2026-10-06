# Non-Blocking Operations: ExtendedTask, future, mirai

Async is the **last** tool to reach for. It doesn't make any computation
faster — it changes *who waits*: the R process keeps serving **other
sessions**, and with `ExtendedTask` the **same session** stays interactive.
Exhaust elimination (reactive-graph.md) and caching (caching.md) first: caching
gives 10–100×; async gives concurrency at the cost of serialization overhead,
harder debugging, and invisible profiling.

## Why blocking hurts

R is single-threaded per process, and **no output is sent until all outputs in
a flush complete** — one session's 5-second computation blocks every other
user on the same R process. This is why an app can be fine in dev and fall
apart with three users.

## The decision path

1. Can the operation be **eliminated** (not computed when not shown)?
2. **Cached** (`bindCache`/`memoise`), so it runs at most once per unique input?
3. **Precomputed** offline (data-loading.md)?
4. Genuinely a request-time, multi-second, user-specific computation (model
   fit on uploaded data, slow external API)? → **Then** async is appropriate.

Async pays off for a few big hotspots. Diffuse small slowness gets *worse*
with async (fixed per-task serialization overhead).

## `ExtendedTask` (Shiny ≥ 1.8.1): the recommended pattern

`ExtendedTask` splits a computation into "decide when to run with what
parameters" and "receive the result", running the work in a background process
so the session stays responsive. The complete pattern:

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
- `$invoke()` does not overlap with itself: invoking while running **queues**
  the second call. `input_task_button` disables itself while running; plain
  `actionButton` does not integrate with `bind_task_button()`.
- `$status()` — reactive read: `"initial" | "running" | "success" | "error"`.
- `$result()` — reactive read for consumers: blank before the first run; a
  special "in progress" state while running (this drives busy indicators); the
  resolved **value** on success (not a promise); the error re-raised in the
  consuming output on failure. **Don't wrap `result()` in
  `observeEvent`/`bindEvent`/`isolate()`** — its invalidations are the
  mechanism.
- Declare the task at **server top level** → one instance per session. Declare
  at `app.R` top level → shared across all visitors (rarely what you want).
- Multiple distinct ExtendedTasks run concurrently with each other and with
  reactive code.

## Worker backends: `future` and `mirai`

- **future + promises** (classic): `future::plan(multisession)` spawns worker
  R processes; `future_promise({...})` runs the body there. Worker count =
  concurrent long tasks; each worker is a full R process (RAM!). The default
  `plan(sequential)` runs tasks synchronously — fake async, everything still
  blocks.
- **mirai** (recommended for new work): event-driven promises resolve
  immediately on completion instead of being polled — lower latency, much
  higher scalability. Drop-in where `future_promise()` is accepted:
  ```r
  library(mirai)
  daemons(4)                              # 4 local workers, top of app.R
  onStop(function() mirai::daemons(0))    # clean shutdown

  task <- ExtendedTask$new(function(x) mirai({ slow(x) }, x = x)) |>
    bind_task_button("go")
  ```
  Daemons can be remote hosts for horizontal scaling. **crew** adds managed,
  auto-scaling worker pools on top of mirai.

## Hard rules for worker code

1. **No reactive reads inside the worker body.** Read reactives in the main
   process; pass values as named arguments:
   ```r
   # Wrong: reactive reads can't cross processes
   future_promise({ filter(data(), state == input$state) })
   # Right
   st <- input$state
   future_promise({ filter(data(), state == st) }, st = st, data = data)
   ```
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
   reactive/observer/render body — that's how Shiny knows when work is done.
5. **Observers mutate reactive values inside handlers**:
   `mirai(...) |> then(\(d) rv$done(d))`, never inside the worker.
6. **Serialization costs are real**: arguments and results are copied to/from
   workers. Don't ship a 2 GB data frame to a worker to add a column.
7. profvis can't see inside workers — profile synchronous code first, convert
   the proven hotspot after.

## Raw async reactives (pre-ExtendedTask style)

`reactive({ future_promise({...}) |> then(...) })` (Shiny ≥ 1.1.0) unblocks
**other sessions** but not the current one — the session's flush still waits
for its dependent outputs. ExtendedTask is the better default; use raw
promises only when ExtendedTask can't express the flow.

## UI expectations

- `input_task_button` shows a busy state and disables itself — feedback
  instead of a frozen app.
- While a task runs, the rest of the app stays live (verify with an
  `invalidateLater(1000)` ticking-clock output if unsure).
- Busy indicators for *outputs* (rendering-ui.md) complement task buttons:
  buttons for triggered work, spinners for render-time work.

## Further reading

- ExtendedTask / async: <https://shiny.posit.co/r/articles/improve/nonblocking/>
- mirai: <https://mirai.r-lib.org/>
- crew: <https://wlandau.github.io/crew/>
