---
name: shiny-optimize
description: >
  Diagnose and fix performance problems in Shiny for R apps — slow startup,
  sluggish interactions, long-running blocking operations, and apps that
  struggle beyond a handful of concurrent users. Use when a Shiny app is slow,
  hangs, recomputes too much, times out, or needs to support more users; when
  the user asks to "speed up", "optimize", or "make faster" an existing Shiny
  app; or when preparing a prototyped app for real-world traffic.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "0.1"
license: MIT
---

# Optimizing Shiny App Performance

Help Shiny for R app authors find and fix performance bottlenecks in **existing
apps** — without changing what the app does. The typical user has an app that
worked fine for one or two developers during prototyping and is now too slow,
too fragile, or unable to support the number of users who actually need it.

Two principles govern everything in this skill:

1. **Measure before changing anything.** Human intuition is a notoriously bad
   profiler. A "slow app" is usually slow because of one or two specific
   operations, and they are rarely the ones the user suspects. Profile first,
   then fix what the profile shows, then re-profile to confirm.
2. **Do less work before doing work faster.** The cheapest computation is the
   one that never runs. In order of preference:
   1. **Eliminate** work that isn't needed (don't compute outputs nobody is
      looking at; don't compute with inputs that aren't ready).
   2. **Reuse** work that repeats (share reactives, cache results).
   3. **Accelerate** unavoidable work (faster data access, vectorized code).
   4. **Relocate** work that blocks others (async / background tasks) — this is
      the last resort and mostly buys *concurrency*, not raw speed.

The goal is surgical: keep all app logic and behavior the same, make the app
perceptibly faster and able to handle more users. Resist rewrites.

## The workflow

Follow these steps in order. Don't skip measurement — most "obvious" fixes
turn out to be aimed at the wrong target.

### Step 1 — Understand the complaint

Before touching code, pin down what "slow" means. Ask the user (or infer from
context) and write it down as a benchmark to beat:

- **What feels slow?** Initial page load? Every interaction? One specific
  action (e.g. clicking "Run analysis")? Everything, once more than N people
  use it at once?
- **How many concurrent users** does it need to support? (1–5, ~20, hundreds?)
- **Where does it run?** Locally, shinyapps.io, Posit Connect, Shiny Server?
  (Deployment matters for multi-user problems, less for single-user slowness.)
- **How big is the data?** Where does it live (CSV, database, API) and how
  often does it change?

Each answer selects a different diagnosis path — see the symptom table below.

### Step 2 — Read the app with performance eyes

Read the app source (`app.R` / `server.R` / `ui.R` / modules) before running
anything. Look for the classic smells:

| Smell (search for) | Why it hurts | Fix |
|---|---|---|
| `read.csv`/`read_csv`/DB queries **inside** `server()` or render functions | Re-runs per session or per invalidation | Load once in global scope; see [data-loading.md](references/data-loading.md) |
| The same subsetting/aggregation repeated in several outputs/reactives | Duplicate computation on every change | Extract one shared `reactive()`; see [reactive-graph.md](references/reactive-graph.md) |
| Renderers defined **inside** `observeEvent()`/`observe()` | Re-creates outputs; fights the reactive model | Define once at server top level; see [reactive-graph.md](references/reactive-graph.md) |
| Expensive `render*` expressions with no `req()`/guard | Computes on empty or half-ready inputs at startup | Gate with `req()`; see [reactive-graph.md](references/reactive-graph.md) |
| Many heavy outputs on the landing view | All must compute to load the page | Tabs/navs/conditional gating; see [rendering-ui.md](references/rendering-ui.md) |
| No `bindCache()` anywhere, but repeated identical expensive calls | Everyone re-pays the same cost | See [caching.md](references/caching.md) |
| Sliders/text inputs feeding expensive chains directly | One drag = dozens of recomputations | `debounce()`/`throttle()`/`bindEvent()`; see [reactive-graph.md](references/reactive-graph.md) |
| `Sys.sleep`, long model fits, slow API/DB calls inline in reactives/renders | Blocks the whole R process for all users | `ExtendedTask`; see [async-tasks.md](references/async-tasks.md) |
| `renderUI()` used for routine value updates | DOM rebuild + input rebinding per update | `update*Input()`; see [rendering-ui.md](references/rendering-ui.md) |
| `eventReactive`/`observeEvent` containing `isolate()`-free wide reads | Invalidates more than necessary | Narrow dependencies; see [reactive-graph.md](references/reactive-graph.md) |

This static read gives hypotheses — not conclusions. The next step confirms
which smells actually cost time.

### Step 3 — Measure

Run the app and measure the complaint. Details, commands, and how to read the
output are in [diagnosis.md](references/diagnosis.md); the short version:

```r
# Where does the time go? (CPU/memory profile)
profvis::profvis(shiny::runApp("app.R"))

# Why do outputs keep recomputing? (reactive graph)
reactlog::reactlog_enable()
shiny::runApp("app.R")   # interact, then shiny::reactlogShow()

# Is implementation A faster than B? (micro-benchmark)
bench::mark(A(x), B(x), check = FALSE)

# Does it hold up with N simultaneous users? (load test)
shinyloadtest::record_session("http://localhost:8100/")
# then replay with shinycannon at 1 user and N users
```

Use **profvis** when the question is "which code is slow" and **reactlog** when
the question is "why does so much code run". Use **bench** to compare two
implementations of one step. Use **shinyloadtest** only when the problem is
multi-user capacity, not single-session speed.

Record concrete numbers (seconds per load, per interaction, evaluations per
slider move). You will need them to prove each fix worked.

### Step 4 — Diagnose: classify the bottleneck

| Symptom | Most likely causes | Start here |
|---|---|---|
| First page load is slow (every session) | Data loading or prep inside `server()`; outputs computing at startup on empty inputs; heavy `library()`/setup per session | [data-loading.md](references/data-loading.md), [reactive-graph.md](references/reactive-graph.md) |
| One interaction recomputes far too much | Over-broad reactive dependencies; duplicate computation; no caching; chatty inputs | [reactive-graph.md](references/reactive-graph.md), [caching.md](references/caching.md) |
| A specific action takes seconds and the app freezes | Long synchronous operation inside the flush cycle | [async-tasks.md](references/async-tasks.md) |
| Fast for one user, degrades with several | Blocking operations tie up the R process; repeated identical computation; per-user data reloads | [caching.md](references/caching.md), [async-tasks.md](references/async-tasks.md), [scaling-users.md](references/scaling-users.md) |
| Plots/tables are slow to appear or update | Heavy rendering; full redraws; `server = FALSE` DT on big data | [rendering-ui.md](references/rendering-ui.md) |
| Downloads/uploads misbehave or recompute | `downloadHandler` recomputing; `maxRequestSize` cap | [data-loading.md](references/data-loading.md) |
| Slower only when deployed | Multi-process behavior (globals, caches); scheduler settings | [scaling-users.md](references/scaling-users.md) |

### Step 5 — Fix, cheapest change first

Work through the fix ladder for the diagnosed category. Each ladder is ordered
from least to most invasive; stop as soon as measurements say you're fast
enough. All ladders keep app logic intact.

**Reactive recomputation** → [reactive-graph.md](references/reactive-graph.md)
1. Add `req()` guards so nothing computes on not-ready inputs.
2. Extract shared `reactive()`s so each derived value is computed once.
3. Narrow dependencies: `bindEvent()`/`eventReactive()`, `isolate()`,
   `freezeReactiveValue()` for update loops.
4. Rate-limit chatty inputs with `debounce()`/`throttle()`.
5. Fix timer patterns (`on.exit(invalidateLater(...))`, `reactivePoll()`).

**Repeated identical work** → [caching.md](references/caching.md)
1. `bindCache()` the expensive reactive or renderer (keys must cover all
   reactive reads in the body).
2. Prefer caching data over caching plots when downstream work benefits.
3. `memoise()` expensive pure functions (DB queries, model fits).
4. Choose cache scope deliberately: `"app"` to share across users (mind
   information leakage), `"session"` for user-specific data, `cachem::cache_disk()`
   to persist across restarts.

**Blocking operations** → [async-tasks.md](references/async-tasks.md)
1. Only after caching/elimination are exhausted: move the operation into an
   `ExtendedTask` with `future_promise()` (or `mirai`), `bind_task_button()`.
2. `future::plan(multisession)` (or mirai daemons) is required — a promise
   without workers still blocks.
3. No reactive reads inside the worker; pass values as arguments to `invoke()`.

**Data access** → [data-loading.md](references/data-loading.md)
1. Move loads to global scope; never read data inside render functions.
2. Faster formats: `fread`/`vroom` over `read.csv`; `feather`/`qs`/`fst` over
   CSV/RDS round-trips.
3. DuckDB (+ parquet) or push-down-to-database (`pool` + `dbplyr`) when data
   outgrows RAM or only slices are needed.

**Rendering & UI** → [rendering-ui.md](references/rendering-ui.md)
1. Put heavy outputs on tabs/navs so hidden outputs don't compute.
2. Gate speculative outputs behind buttons/checkboxes (`req()` + `bindEvent`).
3. Use `DT` server-side processing, `replaceData()` updates, WebGL/bundles for
   big plotly, busy indicators while work runs.

### Step 6 — Verify and iterate

Re-measure after **each** change, one change at a time, and compare against the
numbers from step 3. Performance work done blind tends to shuffle
complexity around instead of removing it. Keep the app's observable behavior
identical — a "faster" app that dropped a feature is not faster.

## Quick-wins scan

When the user wants immediate improvements and the app is small-to-medium, run
this triage first. These ten changes fix the large majority of slow Shiny apps
and rarely require refactoring:

1. **Load data once, globally** — not in `server()`, never in renderers.
2. **Share one `reactive()`** among outputs that need the same derived data.
3. **`req()` at the top of expensive outputs** — no computing on empty inputs.
4. **Put heavy outputs on separate tabs** — hidden outputs don't compute.
5. **`bindCache()` the most expensive repeated computation.**
6. **`debounce()` sliders and search boxes** that drive expensive chains.
7. **Move multi-second operations into an `ExtendedTask`.**
8. **Switch slow data reads** to `fread`/`feather`/DuckDB.
9. **Replace `renderUI` updates with `update*Input()`.**
10. **Add busy indicators** (`bslib::useBusyIndicators()`) so remaining waits
    feel shorter.

## Ground rules

- **One change at a time, then re-measure.** Batching changes makes it
  impossible to know what helped.
- **Preserve behavior.** The user wants the same app, faster — not a redesign.
  UI changes are limited to perceived-performance aids (spinners, task buttons,
  tabs) and must be flagged to the user.
- **Prefer modern APIs**: `bindCache()`/`bindEvent()` over `renderCachedPlot()`
  and raw `eventReactive` composition; `ExtendedTask` over hand-rolled promises;
  `mirai`/`future` for workers. Mention legacy equivalents only when the app
  already uses them.
- **Caching before async.** Caching often yields 10–100× improvements;
  async only adds concurrency and carries serialization and debugging costs.
- **Profile before and after.** Capture timings in the issue/PR so the
  improvement is provable.
- **Ask before adding dependencies** (duckdb, data.table, mirai, ...). Each new
  package is a real cost for the user.

## Reference map

Read a reference only when the workflow points there:

- [diagnosis.md](references/diagnosis.md) — profiling (profvis), reactive-graph
  inspection (reactlog), micro-benchmarks (bench), and load testing
  (shinyloadtest/shinycannon) with reading guides for each tool's output.
- [reactive-graph.md](references/reactive-graph.md) — why Shiny recomputes,
  and every tool for narrowing the graph: shared reactives, `req()`,
  `isolate()`, `bindEvent()`, `freezeReactiveValue()`, `debounce()`/`throttle()`,
  timers, and circular-dependency fixes.
- [caching.md](references/caching.md) — `bindCache()` keys and scopes, caching
  data vs. plots, `memoise()`, `cachem` backends, deployment caveats.
- [async-tasks.md](references/async-tasks.md) — the flush cycle, why blocking
  hurts every user on the process, and the `ExtendedTask`/`future_promise`/`mirai`
  patterns with their hard rules and pitfalls.
- [data-loading.md](references/data-loading.md) — load-once patterns, file
  format choices (with benchmark numbers), DuckDB/parquet, databases with
  `pool`/`dbplyr`, downloads and uploads.
- [rendering-ui.md](references/rendering-ui.md) — output suspension via
  tabs/conditional panels, `outputOptions`, `renderUI` alternatives, plot and
  table rendering costs, and perceived performance.
- [scaling-users.md](references/scaling-users.md) — brief: what changes when
  multiple R processes serve the app, load-factor knobs on Connect and
  shinyapps.io, and when to hand off to deployment tuning.

**Shiny for Python:** this skill targets Shiny for R. If the app is Python,
translate concepts rather than code: `@reactive.extended_task` ≈ `ExtendedTask`,
`@reactive.event` ≈ `bindEvent`, `reactive.isolate()` ≈ `isolate()`,
`reactive.poll` ≈ `reactivePoll`, `functools.lru_cache` ≈ `memoise()`. There is
no `bindCache()` in Python — caching is DIY with `lru_cache`/`diskcache`. Note
that `async def` reactives do **not** make Python Shiny faster; use extended
tasks for background work.
