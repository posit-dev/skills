---
name: shiny-py-optimize
description: >
  Diagnose and fix performance problems in Shiny for Python apps — slow
  startup, sluggish interactions, blocking operations, and apps that struggle
  beyond a handful of concurrent users. Use when a Shiny for Python app is
  slow, hangs, recomputes too much, times out, or must support more users;
  when the user asks to "speed up", "optimize", or "make faster" a Python
  Shiny app; or when preparing a prototyped app for real-world traffic.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# Optimizing Shiny for Python App Performance

Make an existing Shiny for Python app faster without changing what it does.
The typical user has an app that worked fine for one or two developers and is
now too slow or must support more users. Keep all app logic intact; prefer
code changes over deployment tuning; resist rewrites.

Order of preference for every fix:

1. **Eliminate** work that isn't needed (don't compute outputs nobody is
   looking at; don't compute with inputs that aren't ready).
2. **Reuse** work that repeats (shared `@reactive.calc`, module-level caches).
3. **Accelerate** unavoidable work (faster data formats, polars, push-down).
4. **Relocate** work that blocks (`@reactive.extended_task`) — last resort; it
   buys concurrency, not raw speed.

One fact drives most Python-specific advice: **Shiny runs reactive functions
serially on a single asyncio event loop — never concurrently, even when they
are `async def`, even across sessions in the same process.** One blocking call
in any reactive function freezes every session in the process. `async`/
`await` alone never fixes this; only `@reactive.extended_task` does.

## Workflow

### 1. Understand the complaint

Pin down what "slow" means and write it as a benchmark to beat:

- **What feels slow?** First page load? Every interaction? One specific
  action? Only when several people use it at once?
- **How many concurrent users** must it support? (1–5, ~20, hundreds?)
- **Where does it run?** Locally, Posit Connect, Posit Connect Cloud,
  self-hosted (uvicorn behind nginx)?
- **How big is the data**, where does it live, and how often does it change?
- **Core or Express?** (`from shiny import ...` vs `from shiny.express import
  ...`). Express top-level code runs once **per session** — a common silent
  trap (data-loading.md).

### 2. Scan the source for smells — and fix them now

Read the app code (`app.py`, modules) and look for the classic smells. Every
smell in this table has a **safe, behavior-preserving fix**: apply each fix
you find *immediately*, before measuring. These changes fix the large majority
of slow Shiny for Python apps.

| Smell (search for) | Why it hurts | Fix |
|---|---|---|
| `pd.read_csv`/DB queries **inside** `server()` or render functions | Re-runs per session or per invalidation | Load once per process: module scope (Core), imported module (Express) → [data-loading.md](references/data-loading.md) |
| Data loads at **top level of an Express `app.py`** | Top-level Express code runs once **per session** | Move loads into an imported module (`shared.py`) → [data-loading.md](references/data-loading.md) |
| Same subsetting/aggregation repeated in several outputs | Duplicate computation on every change | Extract one shared `@reactive.calc` → [reactive-graph.md](references/reactive-graph.md) |
| Expensive `@render.*` with no `req()` guard | Computes on empty/half-ready inputs at startup | `req()` at the top of the body → [reactive-graph.md](references/reactive-graph.md) |
| Many heavy outputs on the landing view | All must compute before the page is usable | Move to tabs/navs — hidden outputs are suspended → [rendering-ui.md](references/rendering-ui.md) |
| Identical expensive work repeated across sessions | Every user re-pays the same cost | Module-level cache (`functools.lru_cache`, `diskcache`) — there is no built-in `bindCache` equivalent → [caching.md](references/caching.md) |
| Sliders/text inputs feeding expensive chains directly | One drag = dozens of recomputations | `@reactive.event()` button gating; debounce helper → [reactive-graph.md](references/reactive-graph.md) |
| `time.sleep`, sync `requests`, heavy pandas/DuckDB calls inline in calcs/effects/renders | Blocks the event loop for **every user in the process** | `@reactive.extended_task` → [async-tasks.md](references/async-tasks.md) |
| `async def` reactives added expecting a speedup | Shiny runs reactive code serially even when async | Async only for async-only APIs; `ExtendedTask` for non-blocking → [async-tasks.md](references/async-tasks.md) |
| `@render.ui` used for routine value updates | DOM rebuild + input re-binding per update | `ui.update_*()` → [rendering-ui.md](references/rendering-ui.md) |
| `@render.table` on large data frames | pandas Styler → full HTML serialization | `@render.data_frame` with `render.DataGrid` → [rendering-ui.md](references/rendering-ui.md) |

Apply the fixes in this rough order (cheapest first): data loads to module
scope (or imported module in Express) → `req()` guards → shared
`@reactive.calc`s → tabs for heavy outputs → module-level caches →
`@reactive.event()` gating for chatty inputs → `ui.update_*()` over
`@render.ui` → faster data formats (polars, parquet, DuckDB) →
`@reactive.extended_task` for multi-second operations → busy indicators
(`ui.busy_indicators`) for remaining waits.

### 3. Measure — to confirm, not to gate

Measurement is for confirming fixes and for finding what the scan can't see.
**It must never crowd out action.** If the app is hard to run, tracing is
slow, or results are ambiguous, apply the scan fixes anyway and say what
couldn't be verified.

Shiny (≥ 1.6) has built-in OpenTelemetry tracing of reactive execution — the
primary "which code is slow" tool:

```bash
uv pip install "shiny[otel]"
SHINY_OTEL_COLLECT=reactivity \
opentelemetry-instrument --traces_exporter console --logs_exporter console \
    --metrics_exporter none shiny run app.py
```

Interact with the app, then read the span hierarchy: every slow
`reactive.calc` / output / extended task appears with its source file and
line. Use `py-spy` to sample a live process when you need a CPU flame graph,
and `timeit` to compare two implementations. For "how many users can this
app support", load test the deployed app with `shinyloadtest` (record →
replay with N workers → report). Tool selection and reading guides:
[diagnosis.md](references/diagnosis.md).

### 4. Diagnose what the scan didn't catch

| Symptom | Most likely causes | Start here |
|---|---|---|
| First page load is slow (every session) | Per-session data loading (especially Express top-level); outputs computing at startup on empty inputs; heavy per-session setup | [data-loading.md](references/data-loading.md), [reactive-graph.md](references/reactive-graph.md) |
| One interaction recomputes far too much | Over-broad dependencies; duplicate computation; chatty inputs | [reactive-graph.md](references/reactive-graph.md), [caching.md](references/caching.md) |
| A specific action takes seconds and the app freezes — for **everyone** | Blocking operation on the shared event loop | [async-tasks.md](references/async-tasks.md) |
| Fast for one user, degrades with several | Blocking operations; repeated identical computation; per-user reloads; too few processes | [caching.md](references/caching.md), [async-tasks.md](references/async-tasks.md), [diagnosis.md](references/diagnosis.md) |
| Plots/tables slow to appear or update | Heavy rendering; `@render.table`; full redraws; un-aggregated Plotly | [rendering-ui.md](references/rendering-ui.md) |
| Downloads/uploads misbehave or recompute | Download handler recomputing per click; uploads parsed in renderers | [data-loading.md](references/data-loading.md) |
| Slower only when deployed | Per-process globals and caches; process/connection limits | [diagnosis.md](references/diagnosis.md) |

### 5. Fix, cheapest change first

Work the ladder for the diagnosed category; stop when measurements say it's
fast enough. Every rung preserves app behavior.

**Reactive recomputation** → [reactive-graph.md](references/reactive-graph.md)
1. `req()` guards — nothing computes on not-ready inputs.
2. Shared `@reactive.calc`s — each derived value computed once per change.
3. Narrow dependencies: `@reactive.event()`, `reactive.isolate()`,
   `reactive.value.freeze()` for update loops.
4. Debounce chatty inputs (helper — not built in as of Shiny 1.8).
5. Fix timers: `invalidate_later()` scheduled **last**, `@reactive.poll()`
   with a cheap check function.

**Repeated identical work** → [caching.md](references/caching.md)
1. `@reactive.calc` memoizes its latest value per session — for free.
2. `@functools.lru_cache` on module-level pure functions (DB queries, model
   fits) — keys must cover **every** input that affects the result.
3. `diskcache`/`cachetools.TTLCache` when results must be shared across
   processes or survive restarts, or the data changes over time.
4. Treat cached results as read-only shared state — return copies before
   mutation.

**Blocking operations** → [async-tasks.md](references/async-tasks.md)
1. Only after elimination/caching are exhausted: `@reactive.extended_task`
   with `ui.input_task_button` + `@ui.bind_task_button`.
2. Sync I/O inside the task → `asyncio.to_thread(...)`; CPU-bound work → a
   module-level `ProcessPoolExecutor` (plain threads won't help CPU work).
3. No reactive reads inside the task body; pass values via `.invoke()`.

**Data access** → [data-loading.md](references/data-loading.md)
1. Loads to process scope (module scope in Core; an imported module in
   Express); never read data in render functions.
2. polars over pandas for anything sizable; parquet over CSV.
3. DuckDB over parquet, or lazy `pl.scan_parquet(...).filter(...).collect()`,
   when data outgrows RAM or only slices are needed.

**Rendering & UI** → [rendering-ui.md](references/rendering-ui.md)
1. Heavy outputs on tabs/navs so hidden outputs stay suspended.
2. Gate speculative outputs behind buttons (`req()` + `@reactive.event()`).
3. `@render.data_frame` + `update_data()` for tables; WebGL/aggregation for
   big Plotly; busy indicators while work runs.

### 6. Verify and iterate

Re-measure after each change, one change at a time, and compare against your
baseline numbers. Keep observable behavior identical — a "faster" app that
dropped a feature is not faster. Before finishing, recompute one
representative output's value from the original and modified apps (or from
the raw data) and confirm they match — this catches silent behavior drift
cheaply.

Report integrity: save every measurement you cite (trace output, timing log)
under `outputs/measurements/`, and check each number and mechanism claimed
in the final report against those saved artifacts. If a claim can't be
verified against an artifact, say so in the report instead of asserting it.

## Ground rules

- **Batch the obvious; isolate the uncertain.** Safe fixes with predictable
  effects — moving a data load to module scope, consolidating duplicated
  filtering, replacing a `@render.ui` — can be applied together and
  re-measured once. Reach for one-change-at-a-time only when it's genuinely
  unclear which change helped, or a change didn't deliver its expected
  effect; that's the only situation where attribution is worth the extra
  measurement rounds.
- **Preserve behavior.** UI changes are limited to perceived-performance aids
  (spinners, task buttons, tabs) and must be flagged to the user — as must
  changes that alter *timing semantics* even when outputs are identical
  (debouncing adds intentional latency; caches share results across
  sessions).
- **`async` is not a performance fix.** `async def` reactives exist so you can
  call async-only APIs. They do not run concurrently and do not make the app
  responsive. Non-blocking means `@reactive.extended_task`.
- **Caching before async.** Caching often yields 10–100×; async only adds
  concurrency and carries serialization and debugging costs.
- **Never scale with multi-worker servers.** `uvicorn --workers >1`, the
  `WEB_CONCURRENCY` env var, and multi-worker Gunicorn silently break Shiny
  (sticky-session requirement, [diagnosis.md](references/diagnosis.md)).
  Scale with multiple single-worker processes behind sticky-session load
  balancing.
- **Ask before adding dependencies** (polars, duckdb, diskcache, py-spy...).

## References

Read **only** the reference your diagnosis points to, when you need it — do
not read all of them up front.

- [diagnosis.md](references/diagnosis.md) — OpenTelemetry tracing, py-spy,
  timing checks, load testing with shinyloadtest; the single-process asyncio
  model; sticky sessions and deployment capacity knobs.
- [reactive-graph.md](references/reactive-graph.md) — shared calcs, `req()`,
  `reactive.isolate()`, `@reactive.event()`, update loops and
  `reactive.value.freeze()`, the debounce helper, timers and polling.
- [caching.md](references/caching.md) — what `@reactive.calc` does and
  doesn't cache; module-level `lru_cache`/`diskcache`/`cachetools` patterns
  and their hard rules.
- [async-tasks.md](references/async-tasks.md) — why blocking hurts everyone,
  the `@reactive.extended_task` pattern and its hard rules, threads vs
  process pools.
- [data-loading.md](references/data-loading.md) — process-scope loading
  (Core and Express), polars/parquet/DuckDB lazy loading, databases,
  downloads and uploads.
- [rendering-ui.md](references/rendering-ui.md) — output suspension via tabs,
  `@render.ui` alternatives, plot/table rendering costs, perceived
  performance.
