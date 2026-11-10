---
name: r-mizu
description: >
  Write correct R code for async and parallel computing with mizu: task pools,
  parallel map, channels and promises over shared memory on one machine. Use
  when running R code in parallel or in the background, speeding up a loop or
  lapply, using promises or Shiny ExtendedTask, sharing data with R or Python
  processes, or converting from future, parallel or mirai. Defer to the r-mirai
  skill for work spanning more than one machine (SSH, HPC).
metadata:
  author: Charlie Gao (@shikokuchuo)
  version: "1.0"
license: MIT
---

# mizu: async and parallel R over shared memory

mizu runs R code on worker processes on the same machine and moves data between
processes through shared memory. A task round trip costs under a microsecond
(about 100 µs over sockets), so work can be divided as finely as with threads,
and large vectors and data frames arrive as zero-copy views instead of copies.

Requirements: R >= 4.3, 64-bit; Linux kernel >= 5.3. Install with
`install.packages("mizu")`. The package is experimental: where an
installed version disagrees with this skill, its help page is the authority.

## mizu or mirai?

Shared memory stops at the machine boundary, so the decision is where the
workers run:

- **One machine** (laptop, server, one container, a single HPC node, a Shiny
  server): mizu, for everything async and parallel on it.
- **More than one machine** (SSH workers, Slurm/SGE/PBS/LSF clusters, cloud or
  Posit Workbench launchers, anything "distributed"): the **r-mirai** skill —
  mizu has no remote launcher and cannot reach another host.
- **Both**: mirai fans out across nodes; a mizu pool inside each mirai daemon
  is ordinary R code.

## Quickstart

```r
library(mizu)

p <- mizu_pool(n_workers = 4L)

t <- mizu_submit(p, sum(x) + y, x = 1:10, y = 100)   # returns a handle at once
mizu_collect(t)                                       # 155

m <- mizu_map(p, 1:5, \(i) i * 2L, .template = integer(1))
mizu_collect(m)                                       # 2 4 6 8 10

mizu_pool_stop(p)
```

## Core principle: a task carries everything it needs

`mizu_submit()` captures its expression unevaluated. A worker evaluates it in a
fresh environment that holds only the named arguments from `...`, whose parent
is the worker's global environment (base packages and mizu attached, nothing
else). Nothing from your session is visible and there is no automatic globals
detection: what crosses is exactly what you name, which keeps payloads small and
behaviour predictable. A missing object errors on the worker and is re-raised
at `mizu_collect()`, not at submit.

### Rule 1: pass every object by name, under the name the expression uses

```r
# WRONG: fit and df live in your session, not on the worker
t <- mizu_submit(p, predict(fit, df))

# CORRECT
t <- mizu_submit(p, predict(fit, df), fit = fit, df = df)
```

Every argument must be named; an unnamed one is an error.

### Rule 2: qualify package functions, or load the package in the expression

Workers attach only the base packages and mizu, and tasks are stolen between
workers, so a `library()` call in one task does not prepare the worker that runs
the next. There is no `everywhere()`.

```r
# WRONG
t <- mizu_submit(p, filter(df, x > 5), df = df)

# CORRECT: qualify
t <- mizu_submit(p, dplyr::filter(df, x > 5), df = df)

# CORRECT: load inside the expression (free once that worker has it loaded)
t <- mizu_submit(p, { library(dplyr); filter(df, x > 5) }, df = df)
```

### Rule 3: a function sees its own environment, not the task's arguments

A function defined at top level carries a *reference* to the global
environment. On the worker that resolves to the worker's own global environment,
which holds nothing of yours, so a helper the function calls is not found there,
even when the helper was passed through `...`: the arguments sit in the task
environment, which is not on the function's scope chain.

```r
helper <- function(x) x * 2
g <- function(x) helper(x)

# WRONG: could not find function "helper"
t <- mizu_submit(p, g(1), g = g, helper = helper)

# CORRECT: make the dependency a parameter
g <- function(x, helper) helper(x)
t <- mizu_submit(p, g(1, helper), g = g, helper = helper)

# CORRECT: define what the task needs inside the expression
t <- mizu_submit(p, {
  helper <- function(x) x * 2
  helper(1)
})
```

A function created inside another function carries its enclosing environment
by value, so a closure and the helpers defined beside it travel together. Keep
that environment small: all of it is serialized with every task.

The same rules apply to `.f` in `mizu_map()`: constants and helpers go through
`...` and arrive as extra arguments to `.f`.

### Other traps

- `mizu_submit()` returns a handle, never a value; `mizu_collect()` yields the
  value, exactly once ("task handle already collected" on a second call).
- A loop of tiny `mizu_submit()` calls: use `mizu_map()`, which stages once.

## Pools

```r
p <- mizu_pool(n_workers = 4L)       # spawns 4 R workers
mizu_pool_stop(p)                    # cancels pending tasks, waits for workers, releases shm
```

Stop every pool you create: in a function with `on.exit(mizu_pool_stop(p))`,
in a Shiny app with `onStop(function() mizu_pool_stop(p))`; otherwise the
workers linger until the handle is garbage-collected or R exits. Two arguments
matter early:

- `result_slots` (default 4096): bounds uncollected tasks per submitter;
  past it `mizu_submit()` raises `mizu_error_slots_exhausted`, so collect or
  cancel before submitting more.
- `launcher`: `mizu_launcher(stdout = , stderr = )` redirects worker output;
  `mizu_py_launcher()` spawns Python workers.

Sizing and growth (`max_workers`, `max_submitters` for nested fan-outs,
`slot_size` spill tuning, `mizu_spawn_workers()` / `mizu_retire_worker()`) are
covered by `?mizu_pool`.

### Submit and collect

```r
t <- mizu_submit(p, slow(x), x = x)
r <- mizu_collect(t, timeout = 30)    # blocks; mizu_timeout sentinel on expiry
if (mizu_is_sentinel(r)) ...          # the task keeps running; collect again later
```

A task that errors re-raises its original condition, classes intact, at
`mizu_collect()`; a dead worker raises `mizu_error_worker_died`.
`mizu_cancel(t)` skips a queued task, lets a running one finish and discards its
result; the collect then raises `mizu_error_cancelled`.

### Several tasks

```r
ts <- list(a = mizu_submit(p, f(1), f = f), b = mizu_submit(p, g(2), g = g))
mizu_collect_all(ts, timeout = 60)    # list in input order, names kept
mizu_collect_any(ts, timeout = 60)    # list(index =, value =) of the first done
```

A raised outcome in a collective wait carries an `index` field; only that handle
is consumed, the others stay collectible. A timeout consumes nothing.
`mizu_submit_batch(p, list(quote(a()), quote(b())))` submits pre-quoted
expressions in one call.

### Nested tasks

Inside a task, `mizu_current_pool()` is the running worker's own handle. Nested
submits go onto that worker's deque, and a worker blocked in a nested collect
executes other work instead of sleeping, so divide-and-conquer cannot deadlock.

### A default pool for package code

`mizu_set_default_pool(p)` registers a process-wide default (`mizu_with_pool()`
/ `mizu_local_pool()` scope it); `pool = mizu_default_pool()` resolves: the
explicit argument, `mizu_current_pool()` inside a task, the default, then a
fallback such as `lapply()`.

## Parallel map

`mizu_map()` stages `.f`, its constant arguments and `.x` into shared memory
once, then workers claim contiguous ranges of elements from a shared cursor and
balance by stealing. The per-element cost approaches `lapply()`.

```r
m <- mizu_map(p, 1:100, \(i, k) i * k, k = 3)                  # constants via ...
mizu_collect(m)                                                # list; names of .x kept

m <- mizu_map(p, rnorm(1e5), abs, .template = numeric(1))      # atomic result, unserialized
m <- mizu_map(p, 1:3, \(i) c(i, i^2), .template = numeric(2))  # a 2 x 3 matrix

m <- mizu_map(p, 1:4, \(i) rnorm(i), .seed = 123L)             # reproducible streams
```

- `.template` works like `vapply()`'s `FUN.VALUE`: results are written straight
  into a shared output area, so use it for large results of one shape.
- `.seed` gives every element its own L'Ecuyer-CMRG stream; results are then
  identical for any worker count or steal order. Without it draws are
  independent but not reproducible, and nothing is paid for the option.
- `.x` is indexed with `[[`, so a data frame maps over its columns. For rows,
  map over `seq_len(nrow(df))` and pass `df` as a constant.
- An error in `.f` re-raises with a `mizu_map_index` field naming the element;
  the map is fail-fast, other runners stop within about a batch.
- Nested: `mizu_map(mizu_current_pool(), ...)` inside a task.
- Repeated simulation: `pm <- mizu_map_prepare(p, x, f, ...)` stages once, and
  each `mizu_map_run(pm, .seed = s)` costs only submission and collection.
- `.n_chunks = length(.x)` suits extremely skewed element times;
  `.stream = TRUE` streams slices when `.x` must not be staged whole;
  `.collect = "view"` returns the shared output area as a copy-on-write view.

## Outcomes: sentinels for transport states, conditions for failures

The functions that move data and wait with a bound (`mizu_send()`,
`mizu_recv()`, `mizu_collect()`) return class-tagged **sentinel values** for
the normal states of a loop, never errors: `mizu_timeout` (nothing yet),
`mizu_full` (ring full), `mizu_closed` (orderly close), `mizu_peer_gone` (peer
died). Test with `mizu_is_sentinel(x)` (identity, safe with untrusted payloads)
or `inherits(x, "mizu_timeout")`. Nothing is signalled, so `tryCatch()` cannot
see them.

Failures that cannot resolve raise **classed conditions** inheriting
`mizu_error` — `mizu_error_cancelled`, `mizu_error_worker_died`,
`mizu_error_slots_exhausted`, and the rest in `?mizu_error`. A task's own error
re-raises with its original classes and fields. Dispatch on class, never on
message text:

```r
r <- tryCatch(
  mizu_collect(t),
  mizu_error_worker_died = \(e) retry(),
  mizu_error_cancelled = \(e) NULL,
  error = \(e) e                     # the task's own error, classes intact
)
```

A peer's error on a channel arrives as a *value* (`mizu_is_remote_error(x)`;
raise it yourself with `stop(x)`), and a Python worker's error is raised at
collect as a `mizu_error_remote` condition.

## Promises and Shiny

Task and map handles are promise-like: `then(t, fn)` or `as.promise(t)`
resolves with the value `mizu_collect()` would return and rejects with the
classed condition it would raise. One promise stands per task;
`mizu_collect_async(t, timeout = )` is the explicit form (its timeout rejects
with `mizu_timeout` and leaves the task collectible), and
`mizu_collect_all_async()` / `mizu_collect_any_async()` make one promise per
collection. Needs the later and promises packages.

```r
library(promises)
then(mizu_submit(p, slow(x), x = x), onFulfilled = print, onRejected = warning)
as.promise(mizu_map(p, 1:100, f, .template = numeric(1))) %...>% sum() %...>% print()
```

In a script, drive the event loop with `later::run_now()`; Shiny and httpuv run
it for you. A result has exactly one consumer: a handle with a pending promise
refuses a blocking `mizu_collect()` and a second promise. `mizu_cancel()` is
always allowed and rejects the pending promise.

### Shiny `ExtendedTask`

```r
library(shiny)
library(bslib)
library(mizu)

p <- mizu_pool(n_workers = 4L)         # one pool serves every session
onStop(function() mizu_pool_stop(p))

ui <- page_fluid(
  numericInput("n", "n", 1e6),
  input_task_button("run", "Run"),
  verbatimTextOutput("result")
)

server <- function(input, output, session) {
  task <- ExtendedTask$new(
    function(n) mizu_submit(p, mean(rnorm(n)), n = n)   # invoke args, by name
  ) |> bind_task_button("run")
  observeEvent(input$run, task$invoke(input$n))
  output$result <- renderPrint(task$result())
}

shinyApp(ui, server)
```

Shiny sources app.R into a local environment, so a helper defined there
carries the whole app environment (`ui`, `server`, everything in the file:
about 2 MB per submit for a bslib page) when passed as a task argument. Inline
the body as above, define the helper inside the expression, or give a named
helper a clean enclosure with `environment(f) <- globalenv()` so it crosses by
reference under Rule 3.

Channel messages flow into the event loop too: `mizu_recv_async(ch)` for the
next message, `mizu_recv_handler(ch, fn, batch = TRUE)` for a stream.

## Channels

A channel is a two-way link to one child process. `mizu_channel()` takes a
*quoted* expression evaluated in the child with `ch` bound to its end, spawns
the child, and returns your end. Use it for streaming or request/response with
one long-lived process; use a pool for computation.

```r
ch <- mizu_channel(quote(repeat {
  x <- mizu_recv(ch, timeout = 30)
  if (mizu_is_sentinel(x)) break
  mizu_send(ch, x * 2)
}))
mizu_send(ch, 21)
mizu_recv(ch, timeout = 5)      # 42
mizu_close(ch)                  # orderly: waits for the peer to drain
```

`mizu_send_batch()` / `mizu_recv_batch()` move a list of messages in one
call; `mizu_alive(ch)` probes the peer. Large payloads arrive as zero-copy
views that pin shared memory until garbage-collected, so do not hoard them.

## Python

Workers and channel peers can be Python processes running pymizu, the Python
binding of the same core. `mizu_py_launcher()` spawns them (it probes `python3`
on the `PATH` for pymizu first; pass `python = ` for a venv). A Python pool
refuses `mizu_submit()`: `mizu_call()` builds a language-neutral task and
`mizu_submit_call()` submits it, and a `mizu_call()` spec as `.f` maps over a
Python pool.

```r
p <- mizu_pool(2L, launcher = mizu_py_launcher())
t <- mizu_submit_call(p, mizu_call("numpy.quantile", faithful$eruptions, q = 0.5))
mizu_collect(t)
m <- mizu_map(p, faithful$eruptions, mizu_call("numpy.log"), .template = numeric(1))
```

Vectors, strings, lists (a dict), data frames (a `pymizu.Frame`), factors,
matrices, dates and Arrow tables cross, zero-copy above a size floor;
`POSIXlt`, S4 objects, data.tables and named character vectors are declined
with `mizu_error_not_portable` (fields `path`, `reason`, `remedy`).
`mizu_as_arrow()` converts a received frame back to Arrow without copying.

## Converting from other frameworks

The step is always the same: list every object the expression uses from the
calling environment and pass it by name. Nothing is inferred.

| Elsewhere | mizu |
|---|---|
| `plan(multisession, workers = 4)` / `makeCluster(4)` / `daemons(4)` | `p <- mizu_pool(4L)` |
| `future(expr)` / `mirai(expr, x = x)` / `future_promise(expr)` | `mizu_submit(p, expr, x = x)` |
| `value(f)` / `m[]` | `mizu_collect(t)` |
| `future_lapply()` / `parLapply()` / `mirai_map()[]` | `mizu_collect(mizu_map(p, X, FUN))` |
| `clusterExport()` / `everywhere()` | pass by name per task; `pkg::fn` for packages |
| `future.seed = TRUE` / `clusterSetRNGStream()` / `daemons(seed = )` | `.seed = 123L` on `mizu_map()` |
| `plan(sequential)` / `stopCluster()` / `daemons(0)` | `mizu_pool_stop(p)` |

`mirai(expr, environment())` has no named-argument form; to splice a frame,
`do.call(mizu_submit, c(list(p, quote(expr)), as.list(environment())))`.

## Debugging and operations

- A task's expression plus its named arguments is all the worker sees, so test
  it locally first: `eval(quote({ expr }), list(x = x))`.
- `mizu_pool_info(p)` is the state snapshot, `mizu_pool_stats(p)` the counters
  (tasks, steals, spills), `mizu_pool_dump(p)` the first tool when a pool
  hangs, `mizu_pool_trace(p, fn)` the lifecycle hook; worker stderr reaches
  your console, or a file via `mizu_launcher(stderr = )`.
- A dead worker fails only the tasks it had claimed; the survivors carry on.
- Handles do not survive `fork()`; Linux containers need `/dev/shm` sized for
  the in-flight payloads (`docker run --shm-size=4g`).

## Where to look next

`?mizu_pool` (sizing), `?mizu_map` (templates, RNG, streaming, cross-language
maps), `?mizu_error` (every condition class and field), `?mizu_default_pool`
(the package-author idiom), `vignette("interop", package = "mizu")` and
`vignette("operations", package = "mizu")`; rendered at
https://shikokuchuo.net/mizu/.
