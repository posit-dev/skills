# Data Loading and Access: Get the Right Bytes, Once

Data movement is the most common root cause of slow Shiny apps: data read per
session (or per invalidation), re-read in renderers, or loaded wholesale when
only a slice is needed.

## Rule 1: Load once per process, not per session

Code **outside** `server()` (`app.R` top level, `global.R`) runs **once per R
process**, shared by every session; code inside `server()` runs **once per
session**; code inside renderers runs **on every invalidation**.

```r
# BAD: re-reads the CSV for every session
server <- function(input, output, session) {
  scorecard <- read_csv("scorecard.csv")
}

# GOOD: loaded once at process start, shared across sessions
scorecard <- read_csv("scorecard.csv")

server <- function(input, output, session) { ... }
```

- Anything **session-invariant** (reference data, lookup tables, model
  objects) belongs in global scope; user-specific data stays in `server()`.
- Diagnose with profvis: expensive work in the "Start session" phase is
  per-session work that should move up.
- Caveat: global data is **read-only shared state**. Don't let sessions mutate
  it (`<<-` works in one process but breaks across processes and risks
  cross-user corruption). For writable shared state use a database or an
  app-level cache (caching.md).

## Rule 2: Never read data inside render functions

Reading/processing data inside `render*` re-runs on every invalidation. Load
once (Rule 1), derive in a `reactive()`, let renderers consume it. If the
derivation is expensive and repeats, cache it (caching.md).

## Rule 3: Choose formats that are fast to read

Benchmarks for a 338 MB CSV:

| Format | On disk | Read time | Notes |
|---|---|---|---|
| `readr::read_csv()` | 338 MB | ~1.55 s | 674 MB allocated |
| `readr::read_rds()` | 668 MB | ~0.94 s | general R objects |
| `data.table::fread()` | 338 MB | ~3× faster than read_csv | drop-in for most CSVs |
| `vroom::vroom()` | 338 MB | lazy, columns on demand | great when only some columns are used |
| `arrow::read_feather()` | — | very fast for data frames | columnar, cross-language |
| `arrow::read_parquet()` | — | very fast for data frames | columnar, cross-language, compressed on disk; the best long-term storage format |
| `qs::qread()` | — | ~3–5× faster than readRDS | general R objects |
| `fst` | — | 457 ms vs 1577 ms readRDS (10M rows) | also ~3× smaller |
| DuckDB over CSV | 338 MB | **~51 ms** (lazy `tbl_file`) | 52 KB allocated |
| DuckDB over parquet | 120 MB | **~5.8 ms** | the biggest win available |

Practical ladder for a slow-loading file:

1. `fread()`/`vroom()` — one-line change, no pipeline change.
2. Convert to **parquet** + **DuckDB** for anything bigger than tens of MB or
   used by many sessions:
   ```r
   library(duckdb)
   con <- DBI::dbConnect(duckdb(), ":memory:")
   scorecard <- duckdb::tbl_file(con, "scorecard.csv")   # lazy over the CSV
   # better: write once to parquet, then
   scorecard <- dplyr::tbl(con, "read_parquet('scorecard.parquet')")
   ```
   Normal dplyr verbs run **lazily** via **dbplyr** — `filter()`/`summarise()`
   compile to SQL and only the small result crosses into R, and every session
   against the same `con` shares the work.

   Decide deliberately **where to `collect()`** the query into R memory. If
   several outputs reuse the same heavy query, realize it once into a shared
   (ideally cached) reactive — the download happens once and the small
   downstream calculations run in memory. If each consumer needs only a small
   slice, keep the whole pipeline lazy and collect at the very end. Time the
   query either way: a lazy pipeline that compiles to an expensive query can
   be slower than one smart `collect()`.

3. Precompute the exact analysis artifact offline (Rule 4).

Ask before adding heavy dependencies — but for large-data apps, DuckDB+parquet
is usually the single biggest win. Parquet also pairs well with object
storage: with DuckDB's `httpfs` extension, parquet files can be queried
directly from S3 (`read_parquet('s3://bucket/data.parquet')`) without copying
them to the app server first.

## Rule 4: Precompute offline what doesn't need computing online

Anything deterministic — joins, cleaning, derived columns, pre-aggregated
summaries — should be computed **before the app runs** (a script, a scheduled
job), with the app reading the finished artifact. This also removes the "slow
for the first user after each restart" problem.

For artifacts that aren't tidy data frames — fitted models, nested lists, any
kind of R object — serialize with `saveRDS()` and load with `readRDS()` rather
than forcing a CSV round-trip (`qs::qsave()`/`qread()` are the faster
equivalents, and plain `readRDS()` works fine for data frames too).

## Databases: `pool` + `dbplyr`

```r
# Use pool for real database servers (Postgres, MySQL, SQL Server, ...)
pool <- pool::dbPool(RPostgres::Postgres(),
                     dbname = "appdb", host = "db.internal",
                     user = "app", password = Sys.getenv("DB_PWD"))
onStop(function() pool::poolClose(pool))    # clean shutdown

output$tbl <- renderTable({
  pool |> dplyr::tbl("mtcars") |>
    dplyr::filter(cyl == .env$input$cyl) |>
    dplyr::head(input$nrows)
})

# File-backed local databases (SQLite file, in-memory DuckDB) need no pool:
# one connection, opened once, is simpler and equivalent
con <- DBI::dbConnect(duckdb(), ":memory:")
```

- **Use `pool` only for databases with a server**: pool exists to open and
  return connections per query across sessions, preventing the leaked
  connections that crash long-running apps with server databases. A SQLite
  file or in-memory DuckDB connection has nothing to pool — open a single
  connection once and share it. Either way it works transparently with
  `tbl()`.
- **Push filtering/aggregation to the database**: keep verbs lazy (no
  `collect()` until the end) so only the small result crosses into R.
- Cache frequent identical queries with `memoise()` or `bindCache()`.
- For data that changes while the app runs, poll with a **cheap check query**
  (`SELECT MAX(updated_at)`) via `reactivePoll()` (reactive-graph.md).
- Data too big for RAM: compute in the database, DuckDB-over-parquet, or arrow
  datasets.

## `downloadHandler` shouldn't recompute the dataset

`content(file)` runs on **every download click**. Precompute in a reactive;
only serialize inside `content`:

```r
filtered_data <- reactive({ prep_data(input$year, input$region) })

output$download <- downloadHandler(
  filename = function() "data.csv",
  content  = function(file) write.csv(filtered_data(), file, row.names = FALSE)
)
```

For expensive artifacts (big Excel workbooks, zips), `bindCache()` the data
reactive or generate the file in an ExtendedTask (async-tasks.md).

## Uploads: the 5 MB cap

Uploads silently fail above **5 MB** by default:

```r
options(shiny.maxRequestSize = 30 * 1024^2)   # 30 MB — set at app top level
```

Parse uploads **once** into a cached reactive, not inside renderers; heavy
parsing of large uploads belongs in an ExtendedTask.

## Startup experience

- Keep `server()` bodies cheap — they should mostly *define* the reactive
  graph; expensive eager work belongs in globals or lazily-triggered reactives.
- Let the UI appear before heavy work streams in (rendering-ui.md) rather than
  showing a grey screen.
- On multi-process deployments, **every** R process repeats global-scope loads
  — lean startup and shared disk caches pay off there (diagnosis.md,
  caching.md).

## Further reading

- Mastering Shiny, "Scaling": <https://mastering-shiny.org/scaling-general.html>
- DuckDB R client: <https://r.duckdb.org/>
- pool: <https://rstudio.github.io/pool/>
