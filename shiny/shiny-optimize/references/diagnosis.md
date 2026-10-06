# Diagnosing Shiny Performance: Profiling and Measurement

Every optimization in this skill starts and ends with measurement. This file is
the how-to for the four measurement tools and how to interpret what they show.
Rule of thumb for choosing: **profvis** answers "which code is slow", **reactlog**
answers "why does so much code run", **bench** answers "which implementation of
one step is faster", and **shinyloadtest** answers "how many users can this
app support".

Intuition is a bad profiler: the code that *looks* expensive is often fine,
while an innocent-looking loop or an over-broad reactive invalidation dominates.
Measure, fix, re-measure, one change at a time.

## profvis — profile where the time goes

`profvis` wraps R's sampling profiler (stop execution every ~10 ms, record the
call stack) in an interactive flame graph. It is Shiny-aware: internal Shiny
functions are hidden and each output's re-execution is colored blue, which
makes it excellent for *seeing reactive dependencies in action*.

```r
library(shiny)
profvis::profvis(
  shiny::runApp("app.R")   # runApp() must be explicit inside profvis()
)
```

Interact with the app to reproduce the slowness, then close it — the flame
graph appears. Reading it:

- **Bar width = time**, stack depth = height. Your code appears nested under
  `eventReactiveHandler()` / render-function internals under `runApp()`.
- Ignore tall narrow "towers" (byte-code compilation, one-time setup) — they
  cost little wall-clock time.
- Find the **widest blocks** and the repeated blocks — those are the targets.
- Gray `<GC>` blocks = garbage collection pressure, usually a symptom of
  allocating-and-discarding large objects in a loop.
- Click a bar to see the source line (needs source refs; packages installed
  with `--with-keep.source` or `R_KEEP_PKG_SOURCE=yes`).

**Classifying the slowness from the profile timeline:**

- "Start session" phase dominates → expensive work in the server function body
  or global scope runs per session. Move it out (see data-loading.md).
- "Calculate" phases dominate → a reactive/observer/output is the bottleneck;
  the flame graph shows which.

**Classic R-level findings** (worth knowing because they show up constantly):

- `df[i, "col"] <- value` / `$<-.data.frame` in a loop copies the whole data
  frame each iteration — one real case went from 2.5 s to 10 ms (~250×) by
  restructuring. Pre-allocate (`x <- numeric(n)`) instead of growing `x <- c(x, ...)`.
- Growing a **vector** is cheap since R 3.4 (with a single reference); growing
  a **data frame** still copies everything.
- `apply(df, 2, mean)` pays for `as.matrix` + `aperm`; `colMeans()` is ~3×
  faster, `vapply`/`lapply` over columns ~10×, restructuring the data ~6× total.

**Limitations:** sampling below ~5 ms is unreliable; it can't see inside C
functions that don't check interrupts, `Sys.sleep()` (use `profvis::pause()` in
test code), or work in other processes — **profvis cannot see inside async
workers (futures/mirai)**, so profile *before* converting code to async.

**Profiling a deployed app:** add the profvis module (UI:
`profvis_ui("profiler")`, server: `profvis_server("profiler")`) to get
start/stop buttons and downloadable `.Rprof` files, or profile manually with
`Rprof("out.Rprof", interval = 0.01, line.profiling = TRUE, gc.profiling = TRUE,
memory.profiling = TRUE)` … `Rprof(NULL)` … `profvis(prof_input = "out.Rprof")`.

## reactlog — inspect the reactive graph

reactlog records every reactive event and renders the graph as an interactive
timeline. Use it when outputs recompute more than they should, when you suspect
hidden/accidental dependencies, or when a small input change causes a big storm.

```r
reactlog::reactlog_enable()   # before the app starts; or options(shiny.reactlog = TRUE)
shiny::runApp("app.R")
```

- **Cmd/Ctrl + F3** (or Cmd/Ctrl + Shift + F3 for a marked time point) opens
  the graph while the app runs; **Cmd/Ctrl + F4** drops a "user mark" so you can
  jump straight to an interesting interaction. After closing the app,
  `shiny::reactlogShow()` renders the full timeline.
- Embedding live in an app for demos: `reactlog::reactlog_module_ui()` in the
  UI and `reactlog::reactlog_module_server()` in the server.

Reading the graph:

- Nodes: inputs (left), reactive expressions (middle), observers/outputs
  (right). Green = up to date, gray = invalidated, orange = executing.
- Step through one user interaction with the arrow keys and **count the steps
  until the app is idle again**. A single slider move should invalidate a narrow
  slice. If large swaths go gray, dependencies are too broad.
- The graph shows **evaluation counts per node** — a reactive evaluated many
  times per interaction signals duplicated work (often two outputs independently
  re-deriving the same value instead of sharing one reactive).
- Dependency arrows are discovered at execution time and erased on
  invalidation, so the graph shows *actual* dependencies — which is exactly why
  it reveals accidental ones (e.g. a conditional `input$x` read that only
  registers when a switch is on).

What you're hunting for, concretely: outputs or observers that re-execute
without their inputs having changed meaning; reactives evaluated several times
per interaction; invalidations cascading into graph regions unrelated to the
user's action. Every finding here maps to a fix in reactive-graph.md.

## bench — compare two implementations

When the profile says "this one function", benchmark alternatives before
rewriting:

```r
res <- bench::mark(
  first_try(1e4),
  second_try(1e4),
  check = FALSE   # needed when results differ (random, timestamps, row names)
)
plot(res)          # visual comparison of time + memory
```

- `check = FALSE` silences the "each result must equal the first result" error
  for stochastic code.
- Read **memory allocation** alongside time — `bench::mark` reports both, and a
  version that allocates 100× less is usually both faster and more scalable.
- Typical wins, in order of size: do the operation once instead of N times
  (hoist out of loops/reactives) > vectorize > pre-allocate > micro-optimize.

## In-app timers and regression tracking

- **shiny.tictoc** (Appsilon): one `<script>` tag in the UI measures server-side
  calc time and output recalc time from the browser;
  `showAllMeasurements()` / `exportMeasurements()` / `exportHtmlReport()` from
  the devtools console. Nice for before/after numbers on real interactions.
- **shiny.benchmark** (Appsilon): runs shinytest2/Cypress interaction scripts
  against multiple git refs and reports elapsed-time changes — use it to catch
  performance regressions in CI once the app is fast.

## shinyloadtest — capacity, not single-session speed

Only relevant when the complaint is "it dies with N users". A load test
replays a recorded realistic session with simulated concurrent users and
reports latency. The loop: **benchmark → analyze → recommend → optimize → re-benchmark**.

```r
# 1. Record one realistic session (opens a proxy browser; click through the app)
shinyloadtest::record_session("http://localhost:8100/")
#    -> recording.log  (plus recording.log.post.N for uploads/DT POST traffic)

# 2. Replay: 1-user baseline, then the target load
#    (run shinycannon from a DIFFERENT machine on the same network, not the
#    same box — resource contention distorts results; requires Java)
# shinycannon recording.log http://... --workers 1  --loaded-duration-minutes 5 --output-dir run1
# shinycannon recording.log http://... --workers 20 --loaded-duration-minutes 5 --output-dir run20

# 3. Analyze
df <- shinyloadtest::load_runs("1 user" = "run1", "20 users" = "run20")
shinyloadtest::shinyloadtest_report(df, "report.html")
```

Reading the report:

- **Session Duration tab**: if loaded sessions take about as long as the
  recording (the red line), the app handles that many users without
  degradation; session times 2×+ the recording mean users are queuing behind
  each other on the R process.
- **Latency tab**: histograms of page-load and per-interaction latency at each
  load level.

Each worker loops the recording, so workers ≠ unique sessions. If the load
test shows degradation, the fix ladder in scaling-users.md (and the code fixes
in caching.md/async-tasks.md) comes next — load tests quantify the problem;
code changes usually solve it.

## Recording results

Whatever the tool, end every diagnosis with numbers someone can re-check:
- seconds to first usable page,
- seconds per key interaction (name the interaction),
- evaluations per interaction (reactlog),
- workers × users the load test sustains at < 2× baseline latency.

These are the acceptance criteria for every fix you propose next.
