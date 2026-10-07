---
name: shiny-r-optimize
description: >
  Diagnose and fix performance problems in Shiny for R apps — slow startup,
  sluggish interactions, long-running blocking operations, and apps that
  struggle beyond a handful of concurrent users. Use when a Shiny app is slow,
  hangs, recomputes too much, times out, or needs to support more users; when
  the user asks to "speed up", "optimize", or "make faster" an existing Shiny
  app; or when preparing a prototyped app for real-world traffic.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# Optimizing Shiny App Performance

Make an existing Shiny for R app faster without changing what it does. The
typical user has an app that worked fine for one or two developers and is now
too slow or must support more users. Keep all app logic intact; prefer code
changes over deployment tuning; resist rewrites.

Order of preference for every fix:

1. **Eliminate** work that isn't needed (don't compute outputs nobody is
   looking at; don't compute with inputs that aren't ready).
2. **Reuse** work that repeats (shared reactives, caching).
3. **Accelerate** unavoidable work (faster data formats, vectorized code).
4. **Relocate** work that blocks (async / background tasks) — last resort; it
   buys concurrency, not raw speed.

## Workflow

### 1. Understand the complaint

Pin down what "slow" means and write it as a benchmark to beat:

- **What feels slow?** First page load? Every interaction? One specific
  action? Only when several people use it at once?
- **How many concurrent users** must it support? (1–5, ~20, hundreds?)
- **Where does it run?** Locally, Posit Connect, Posit Connect Cloud, Shiny
  Server?
- **How big is the data**, where does it live, and how often does it change?

### 2. Scan the source for smells — and fix them now

Read the app code (`app.R` / `server.R` / `ui.R` / modules) and look for the
classic smells. Every smell in this table has a **safe, behavior-preserving
fix**: apply each fix you find *immediately*, before measuring. These ten
changes fix the large majority of slow Shiny apps.

| Smell (search for) | Why it hurts | Fix |
|---|---|---|
| `read.csv`/`read_csv`/DB queries **inside** `server()` or render functions | Re-runs per session or per invalidation | Load once in global scope → [data-loading.md](references/data-loading.md) |
| Same subsetting/aggregation repeated in several outputs | Duplicate computation on every change | Extract one shared `reactive()` → [reactive-graph.md](references/reactive-graph.md) |
| Renderers defined **inside** `observeEvent()`/`observe()` | Re-creates outputs; fights the reactive model | Define once at server top level, gate with `bindEvent()`/`req()` → [reactive-graph.md](references/reactive-graph.md) |
| Expensive `render*` with no `req()` guard | Computes on empty/half-ready inputs at startup | `req()` at the top of the body → [reactive-graph.md](references/reactive-graph.md) |
| Many heavy outputs on the landing view | All must compute before the page is usable | Move to tabs/navs — hidden outputs don't compute → [rendering-ui.md](references/rendering-ui.md) |
| No `bindCache()` on repeated identical expensive calls | Everyone re-pays the same cost | `bindCache()` → [caching.md](references/caching.md) |
| Sliders/text inputs feeding expensive chains directly | One drag = dozens of recomputations | `debounce()`/`throttle()`/`bindEvent()` → [reactive-graph.md](references/reactive-graph.md) |
| `Sys.sleep`, long model fits, slow API/DB calls inline in reactives/renders | Blocks the whole R process for all users | `ExtendedTask` → [async-tasks.md](references/async-tasks.md) |
| `renderUI()` used for routine value updates | DOM rebuild + input rebinding per update | `update*Input()` → [rendering-ui.md](references/rendering-ui.md) |
| Wide `isolate()`-free reads in `eventReactive`/`observeEvent` | Invalidates more than necessary | Narrow dependencies → [reactive-graph.md](references/reactive-graph.md) |

Apply the fixes in this rough order (cheapest first): data loads to global
scope → `req()` guards → shared reactives → tabs for heavy outputs →
`bindCache()` → debounce chatty inputs → `update*Input()` over `renderUI` →
faster data formats (`fread`/feather/DuckDB) → `ExtendedTask` for multi-second
operations → busy indicators (`bslib::useBusyIndicators()`) for remaining
waits.

### 3. Measure — to confirm, not to gate

Measurement is for confirming fixes and for finding what the scan can't see.
**It must never crowd out action.** If the app is hard to run, profiling is
slow, or results are ambiguous, apply the scan fixes anyway and say what
couldn't be verified.

```r
# Where does the time go? (CPU/memory profile)
p <- profvis::profvis(shiny::runApp("app.R"))
debrief::pv_print_debrief(p)   # debrief turns the profvis output into text
                               # summaries — hot functions/lines, call paths,
                               # memory, suggestions — much easier to act on
                               # than the interactive flame graph. Follow up
                               # with pv_focus(), pv_hot_lines(),
                               # pv_suggestions(); compare before/after runs
                               # with pv_print_compare().

# Is implementation A faster than B?
bench::mark(A(x), B(x), check = FALSE)
```

Two tools in the ecosystem are for the **user**, not for you to run: **reactlog**
has the user interact with their own app and explore the reactive-graph
visualization to understand how their reactives interact — you can usually get
the same insight (and more cheaply) by reading the code and reconstructing the
reactive graph yourself. **shinyloadtest** is a load test of a *deployed* app,
run at the end of an optimization when the user wants to verify their
infrastructure will handle the number of users they intend to support.

Tool selection, how to read each tool's output, and load-test interpretation:
[diagnosis.md](references/diagnosis.md). Use profvis/debrief for "which code is
slow" and bench to compare two implementations; leave reactlog to the user,
and shinyloadtest for deployed-app capacity.

### 4. Diagnose what the scan didn't catch

| Symptom | Most likely causes | Start here |
|---|---|---|
| First page load is slow (every session) | Data loading/prep inside `server()`; outputs computing at startup on empty inputs; heavy setup per session | [data-loading.md](references/data-loading.md), [reactive-graph.md](references/reactive-graph.md) |
| One interaction recomputes far too much | Over-broad dependencies; duplicate computation; no caching; chatty inputs | [reactive-graph.md](references/reactive-graph.md), [caching.md](references/caching.md) |
| A specific action takes seconds and the app freezes | Long synchronous operation in the flush cycle | [async-tasks.md](references/async-tasks.md) |
| Fast for one user, degrades with several | Blocking operations tie up the process; repeated identical computation; per-user reloads | [caching.md](references/caching.md), [async-tasks.md](references/async-tasks.md), [diagnosis.md](references/diagnosis.md) |
| Plots/tables slow to appear or update | Heavy rendering; full redraws; `server = FALSE` DT on big data | [rendering-ui.md](references/rendering-ui.md) |
| Downloads/uploads misbehave or recompute | `downloadHandler` recomputing; `maxRequestSize` cap | [data-loading.md](references/data-loading.md) |
| Slower only when deployed | Per-process globals and caches; scheduler settings | [diagnosis.md](references/diagnosis.md) |

### 5. Fix, cheapest change first

Work the ladder for the diagnosed category; stop when measurements say it's
fast enough. Every rung preserves app behavior.

**Reactive recomputation** → [reactive-graph.md](references/reactive-graph.md)
1. `req()` guards — nothing computes on not-ready inputs.
2. Shared `reactive()`s — each derived value computed once.
3. Narrow dependencies: `bindEvent()`/`eventReactive()`, `isolate()`,
   `freezeReactiveValue()` for update loops.
4. `debounce()`/`throttle()` chatty inputs; when updates compound, gate
   the batch behind `bslib::input_task_button()` (drop-in for
   `actionButton()`).
5. Fix timers: `on.exit(invalidateLater(...))`, `reactivePoll()` with a cheap
   `checkFunc`.

**Repeated identical work** → [caching.md](references/caching.md)
1. `bindCache()` the expensive reactive or renderer — keys must cover every
   reactive read in the body.
2. Cache data over plots when downstream work benefits.
3. `memoise()` expensive pure functions (DB queries, model fits).
4. Choose scope deliberately: `"app"` to share across users (mind information
   leakage), `"session"` for user-specific data, `cachem::cache_disk()` to
   share across processes and restarts.

**Blocking operations** → [async-tasks.md](references/async-tasks.md)
1. Only after elimination/caching are exhausted: `ExtendedTask` with
   `mirai()` (or `future_promise()`), plus `bind_task_button()`.
2. Worker backends are **required** — set up mirai `daemons()` or
   `future::plan(multisession)`; with future's default `plan(sequential)`
   everything still blocks.
3. No reactive reads inside the worker; pass values via `invoke()`.

**Data access** → [data-loading.md](references/data-loading.md)
1. Loads to global scope; never read data in render functions.
2. `fread`/`read_csv` (vroom-powered) over `read.csv`; `feather`/`qs`/`fst`
   over CSV/RDS round-trips.
3. DuckDB + parquet, or `pool` + `dbplyr` push-down, when data outgrows RAM
   or only slices are needed.

**Rendering & UI** → [rendering-ui.md](references/rendering-ui.md)
1. Heavy outputs on tabs/navs so hidden outputs don't compute.
2. Gate speculative outputs behind buttons (`req()` + `bindEvent()`).
3. DT server-side processing + `replaceData()`; WebGL/bundles for big plotly;
   busy indicators while work runs.

### 6. Verify and iterate

Re-measure after each change, one change at a time, and compare against your
baseline numbers. Keep observable behavior identical — a "faster" app that
dropped a feature is not faster. Before finishing, recompute one
representative output's value from the original and modified apps (or from
the raw data) and confirm they match — this catches silent behavior drift
cheaply.

Report integrity: save every measurement you cite (script output, timing log)
under `outputs/measurements/` in the app's project — create the folder if it
doesn't exist — and check each number and mechanism claimed in the final
report against those saved artifacts. If a claim can't be verified against an
artifact, say so in the report instead of asserting it.

```
<app-project>/
  outputs/
    measurements/    # the audit trail for the final report: one file per
                     # measurement (profvis output, bench results, timings),
                     # named for the fix or code path it measured
```

## Ground rules

- **Batch the obvious; isolate the uncertain.** Safe fixes with predictable
  effects — moving a data load to global scope, consolidating duplicated
  filtering, replacing a `renderUI` — can be applied together and re-measured
  once. Reach for one-change-at-a-time only when it's genuinely unclear which
  change helped, or a change didn't deliver its expected effect; that's the
  only situation where attribution is worth the extra measurement rounds.
- **Preserve behavior.** UI changes are limited to perceived-performance aids
  (spinners, task buttons, tabs) and must be flagged to the user — as must
  changes that alter *timing semantics* even when outputs are identical
  (`debounce()` adds intentional latency; `bindCache()`/`memoise()` share
  results across sessions).
- **Prefer modern APIs**: `bindCache()`/`bindEvent()` over `renderCachedPlot()`
  and raw `eventReactive` composition; `ExtendedTask` over hand-rolled
  promises. Mention legacy equivalents only when the app already uses them.
- **Caching before async.** Caching often yields 10–100×; async only adds
  concurrency and carries serialization and debugging costs.
- **Ask before adding dependencies** (duckdb, data.table, mirai, ...).

## References

Read **only** the reference your diagnosis points to, when you need it — do
not read all of them up front.

- [diagnosis.md](references/diagnosis.md) — profvis/debrief, bench, and
  load testing (shinyloadtest/shinycannon) with reading guides; multi-user
  process model; Connect and Posit Connect Cloud capacity knobs.
- [reactive-graph.md](references/reactive-graph.md) — shared reactives,
  `req()`, `isolate()`, `bindEvent()`, `freezeReactiveValue()`,
  `debounce()`/`throttle()`, timers, and dependency-storm fixes.
- [caching.md](references/caching.md) — `bindCache()` key rules and scopes,
  cache backends, `memoise()`, pre-cache checklist.
- [async-tasks.md](references/async-tasks.md) — why blocking hurts, the
  `ExtendedTask`/`mirai`/`future_promise` pattern and its hard rules.
- [data-loading.md](references/data-loading.md) — load-once patterns, file
  format benchmarks, DuckDB/parquet, `pool`/`dbplyr`, downloads and uploads.
- [rendering-ui.md](references/rendering-ui.md) — output suspension via tabs,
  `renderUI` alternatives, plot/table rendering costs, perceived performance.
