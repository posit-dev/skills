# Diagnosis: Measurement Tools and Multi-User Scaling

Read this when you need to profile, load-test, or reason about multi-user
capacity. Choose the tool by question: **profvis** — "which code is slow";
**reactlog** — "why does so much code run"; **bench** — "which implementation
is faster"; **shinyloadtest** — "how many users can this app support".

Remember: measurement confirms and discovers — it is not a prerequisite for
applying the safe fixes from the smell scan. If tooling is slow or ambiguous,
fix what the scan found and record what couldn't be verified.

## profvis — where the time goes

`profvis` wraps R's sampling profiler in an interactive flame graph; Shiny
output re-executions are colored blue.

```r
profvis::profvis(
  shiny::runApp("app.R")   # runApp() must be explicit inside profvis()
)
```

Interact to reproduce the slowness, then close the app. Reading the graph:

- **Bar width = time**, height = stack depth. Your code appears under
  `eventReactiveHandler()` / render internals under `runApp()`.
- Ignore tall narrow towers (one-time setup); find the **widest** and
  **repeated** blocks.
- Gray `<GC>` blocks = allocation pressure from creating-and-discarding large
  objects in a loop.
- "Start session" phase dominating → per-session work that belongs in global
  scope (see data-loading.md). "Calculate" phases dominating → a reactive or
  output is the bottleneck.

Classic R-level findings that show up constantly:

- `df[i, "col"] <- value` in a loop copies the whole data frame each iteration
  (one real case: 2.5 s → 10 ms by restructuring). Pre-allocate vectors
  instead of growing them.
- Growing a vector is cheap (single reference, R ≥ 3.4); growing a data frame
  still copies everything.
- `apply(df, 2, mean)` pays for `as.matrix`; use `colMeans()` or `vapply()`
  over columns.

**Limitations:** unreliable below ~5 ms; **cannot see inside async workers
(futures/mirai)** — profile synchronous code *before* converting it to async.

## reactlog — inspect the reactive graph

Use when outputs recompute more than they should or a small input change
causes a storm.

```r
reactlog::reactlog_enable()   # before the app starts
shiny::runApp("app.R")
# Cmd/Ctrl+F3 opens the graph live; Cmd/Ctrl+F4 drops a user mark
# After closing: shiny::reactlogShow()
```

Reading the graph:

- Nodes: inputs (left), reactive expressions (middle), observers/outputs
  (right). Green = up to date, gray = invalidated, orange = executing.
- Step through one interaction and **count steps until idle**. A slider move
  should invalidate a narrow slice; large gray swaths mean dependencies are
  too broad.
- **Evaluation counts per node** reveal duplicated work (two outputs
  independently re-deriving the same value instead of sharing a reactive).
- Dependency arrows are discovered at execution time, so the graph shows
  *actual* dependencies — trust it over your mental model; it exposes
  accidental ones (e.g. conditional `input$x` reads).

Every finding here maps to a fix in reactive-graph.md.

## bench — compare two implementations

```r
res <- bench::mark(first_try(1e4), second_try(1e4), check = FALSE)
plot(res)
```

- `check = FALSE` allows differing results (random, timestamps, row names).
- Read **memory allocation** alongside time — a version allocating 100× less
  is usually both faster and more scalable.
- Wins, ordered by size: do it once instead of N times (hoist out of
  loops/reactives) > vectorize > pre-allocate > micro-optimize.

## shinyloadtest — capacity, not single-session speed

Only when the complaint is "dies with N users". Replay a recorded session
with simulated concurrent users:

```r
# 1. Record one realistic session (proxy browser; click through the app)
shinyloadtest::record_session("http://localhost:8100/")   # -> recording.log

# 2. Replay with shinycannon from a DIFFERENT machine on the same network
#    (requires Java): 1-user baseline, then target load
# shinycannon recording.log http://... --workers 1  --loaded-duration-minutes 5 --output-dir run1
# shinycannon recording.log http://... --workers 20 --loaded-duration-minutes 5 --output-dir run20

# 3. Analyze
df <- shinyloadtest::load_runs("1 user" = "run1", "20 users" = "run20")
shinyloadtest::shinyloadtest_report(df, "report.html")
```

Reading the report:

- **Session Duration tab**: loaded sessions ≈ the recording length (red line)
  means the app handles that load; 2×+ means users are queuing on the R
  process.
- Workers loop the recording, so workers ≠ unique sessions. Sessions are
  sticky per browser — don't fake a load test by opening 5 tabs.

If the load test shows degradation, the code fixes in caching.md and
async-tasks.md come before the infrastructure knobs below.

## Recording results

End every diagnosis with re-checkable numbers: seconds to first usable page,
seconds per key interaction, evaluations per interaction (reactlog), and
workers × users sustained at < 2× baseline latency. These are the acceptance
criteria for every fix.

## The multi-user process model

One Shiny R process is **single-threaded**; apps scale by running multiple
processes (workers), each with its own memory, globals, and caches. Implications:

- **Blocking operations tie up the whole process** — every user on it queues.
  This is why code fixes come first.
- **Globals and app-level caches are per-process**: 3 workers = 3 independent
  `bindCache(cache = "app")` stores. Use `cachem::cache_disk()` to share a
  cache across processes (caching.md).
- **Global data loads repeat per process**: 3 workers = 3 copies of the 2 GB
  data frame in RAM and 3 cold starts. Many processes × big globals is the
  most common OOM.

## Deployment knobs (last resort, after code fixes)

**Posit Connect** (content's Runtime tab):

| Setting | Default | Meaning |
|---|---|---|
| Max processes | 3 | Upper bound of R workers |
| Max connections per process | 20 | Concurrent connections per worker |
| Load factor | 0.5 | Fraction of capacity that triggers a new process; lower = spawn sooner |
| Min processes | 0 | Keep workers warm — raise toward Max when the app preloads data at process start (avoids cold starts) |

Capacity ≈ Max processes × Max connections per process.

**shinyapps.io**: instance RAM 256 MB–8 GB (1 GB default); tunables include
workers per instance, max/min instances, idle timeout, max connections per
worker (default 50), and load factors. **OOM shows up as a grey screen and
"killed" in logs** — fix with a bigger instance or *fewer* workers.

More processes is the easy, costly fix; code optimization is the durable one.
When recommending infrastructure changes, hand the user the load-test numbers
that justify them.

## Further reading

- profvis: <https://rstudio.github.io/profvis/>
- reactlog: <https://rstudio.github.io/reactlog/>
- shinyloadtest: <https://rstudio.github.io/shinyloadtest/>
- Connect scaling: <https://docs.posit.co/connect/admin/appendix/off-host-scheduler/>
