# Data Loading and Access: Get the Right Bytes, Once

Data movement is the most common root cause of slow Shiny apps: data read per
session (or per invalidation!), re-read in renderers, or loaded wholesale when
only a slice is needed. The rules in this file preserve app behavior — same
data, same app — while cutting load times by 10–250× in realistic benchmarks.

## Rule 1: Load once per process, not per session

Code in `app.R`/`global.R` **outside** `server()` runs **once per R process**
and is shared by every session; code inside `server()` runs **once per
session**; code inside renderers runs **on every invalidation**.

```r
# BAD: re-reads the CSV for every session
server <- function(input, output, session) {
  scorecard <- read_csv("scorecard.csv")
  # ...
}

# GOOD: loaded once at process start, shared across sessions
scorecard <- read_csv("scorecard.csv")

server <- function(input, output, session) {
  # ...
}
```

- Anything **session-invariant** (reference data, lookup tables, model objects)
  belongs in global scope. Anything user-specific stays in `server()`.
- Watch the console while the app runs: packages attaching or services
  starting *mid-session* mean heavy setup is in the wrong scope.
- Diagnose with profvis: expensive work during the "Start session" phase is
  per-session work that should move up (or be precomputed — below).
- Caveat: global data is **read-only shared state**. Don't let sessions mutate
  it (`<<-` from a session works within one process but breaks under multiple
  processes and risks cross-user corruption). For sharing *writable* state,
  use a database or an app-level cache (caching.md).

## Rule 2: Never read data inside render functions

Reading/processing data inside `render*` re-runs on every invalidation of that
output. Load once (Rule 1), derive in a `reactive()`, and let renderers
consume the reactive. If the derivation is expensive and repeats, that's a
caching.md problem.

## Rule 3: Choose formats that are fast to read

Benchmark numbers for a 338 MB CSV (`bench::mark(..., check = FALSE)`):

| Format | On disk | Read time | Notes |
|---|---|---|---|
| `readr::read_csv()` | 338 MB | ~1.55 s | 674 MB allocated |
| `readr::read_rds()` | 668 MB | ~0.94 s | general R objects |
| `data.table::fread()` | 338 MB | ~3× faster than read_csv | drop-in for most CSVs |
| `vroom::vroom()` | 338 MB | lazy — reads columns on demand | great when only some columns are used |
| `arrow::read_feather()` | — | very fast for data frames | columnar, cross-language |
| `qs::qread()` | — | ~3–5× faster than readRDS | general R objects |
| `fst` | — | 457 ms vs 1577 ms readRDS (10M rows) | also ~3× smaller |
| DuckDB over CSV | 338 MB | **~51 ms** (lazy `tbl_file`) | 52 KB allocated |
| DuckDB over parquet | 120 MB | **~5.8 ms** | "an unbeatable combo" |

Practical ladder for a slow-loading data file:

1. `fread()`/`vroom()` — one-line change, no pipeline change.
2. Convert to **parquet** + **DuckDB** for anything bigger than tens of MB or
   used by many sessions:
   ```r
   library(duckdb)
   con <- DBI::dbConnect(duckdb(), ":memory:")
   scorecard <- duckdb::tbl_file(con, "scorecard.csv")     # lazy over the CSV
   # better: write once to parquet, then
   scorecard <- dplyr::tbl(con, "read_parquet('scorecard.parquet')")
   ```
   Normal dplyr verbs work **lazily** — `filter()`/`summarise()` compile to
   SQL and only the small result crosses into R. One workshop benchmark: full
   CSV read 1.5 s/670 MB vs DuckDB query 51 ms/52 KB — and every session
   against the same `con` shares the work.
3. Precompute the exact analysis artifact offline when the derivation is
   deterministic (next rule).

Don't swap in heavy dependencies without asking — but for large-data apps,
DuckDB+parquet is usually the single biggest win available.

## Rule 4: Precompute offline what doesn't need computing online

Anything deterministic — joins, cleaning, derived columns, pre-aggregated
summaries — should be computed **before the app runs** (a script, a scheduled
job, a scheduled Quarto/report), and the app reads the finished artifact. The
restaurant metaphor from Mastering Shiny: hire a prep chef who comes in at
3am, don't chop vegetables during the dinner rush. This also removes the
"app is slow for the *first* user after each restart" class of problems.

## Databases: `pool` + `dbplyr`, push compute to the data

```r
pool <- pool::dbPool(RSQLite::SQLite(), dbname = "app.db")
onStop(function() pool::poolClose(pool))    # clean shutdown

output$tbl <- renderTable({
  pool |> dplyr::tbl("mtcars") |>
    dplyr::filter(cyl == .env$input$cyl) |>
    dplyr::head(input$nrows)
})
```

- **Why pool**: opens/returns connections per query, preventing the leaked
  connections that crash long-running apps; works transparently with `tbl()`.
- **Push filtering/aggregation to the database**: keep verbs lazy (no
  `collect()` until the end) so `filter()`/`summarise()` become SQL and only
  the small result crosses into R.
- Cache frequent identical queries with `memoise()` or `bindCache()`
  (caching.md).
- For data that changes while the app runs, poll with a **cheap check query**
  (`SELECT MAX(updated_at)`) via `reactivePoll()` rather than re-reading on a
  timer (reactive-graph.md).
- Big data that doesn't fit in RAM: compute in the database, DuckDB-over-
  parquet, or arrow datasets — don't try to swap your way out of it.

## `downloadHandler` shouldn't recompute the dataset

`content(file)` runs on **every download click**. Precompute the data in a
reactive; only serialize inside `content`:

```r
filtered_data <- reactive({ prep_data(input$year, input$region) })

output$download <- downloadHandler(
  filename = function() "data.csv",
  content  = function(file) write.csv(filtered_data(), file, row.names = FALSE)
)
```

If the exported artifact itself is expensive to build (big Excel workbooks,
zip files), consider `bindCache()` on the data reactive, or generate the file
in an ExtendedTask for very large exports (async-tasks.md).

## Uploads: the 5 MB cap

Uploads silently fail above **5 MB** by default. If the app accepts data
files:

```r
options(shiny.maxRequestSize = 30 * 1024^2)   # 30 MB — set at app top level
```

Parse uploads **once** into a cached reactive, not inside renderers; heavy
parsing of large uploads belongs in an ExtendedTask.

## Startup experience

When heavy init is unavoidable (model warm-up, big load at process start):

- Keep `server()` bodies cheap — they should mostly *define* the reactive
  graph; expensive eager work belongs in globals or lazily-triggered reactives.
- Let the UI appear before heavy work streams in (perceived performance:
  rendering-ui.md) rather than showing users a grey screen.
- On multi-process deployments, **every** R process repeats global-scope
  loads — this is where lean startup and shared disk caches pay off
  (scaling-users.md, caching.md).
