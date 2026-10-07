# Data Loading and Access: Get the Right Bytes, Once

Data movement is the most common root cause of slow Shiny for Python apps:
data read per session (or per invalidation), re-read in renderers, or loaded
wholesale when only a slice is needed.

## Rule 1: Load once per process, not per session

Python scoping rules decide how often code runs — and they differ by mode:

| Where the code lives | Shiny Core | Shiny Express |
|---|---|---|
| Module scope of an imported module | Once per process | Once per process |
| `server()` body | Once per session | — (no server function) |
| **Top level of `app.py`** | Once per process* | **Once per session** |

\* In Core, `app.py` module scope runs at import; `server()` runs per
connection. In **Express, the whole top level of `app.py` is re-executed once
per session** (it's wrapped in an implicit server function) — `df =
pd.read_csv(...)` at the top of an Express app re-reads the file for *every
user*. This is the most common silent trap in Python Shiny apps.

```python
# BAD (Express): re-reads the CSV for every session
# app.py
import pandas as pd
scorecard = pd.read_csv("scorecard.csv")   # runs per session!

# GOOD (Express): loaded once per process, shared across sessions
# shared.py
import pandas as pd
scorecard = pd.read_csv("scorecard.csv")

# app.py
import shared                             # first import wins; cached after
from shiny.express import render

@render.data_frame
def table():
    return shared.scorecard
```

- Anything **session-invariant** (reference data, lookup tables, model
  objects, DB engines, executor pools) belongs in an imported module;
  user-specific data (connections, auth state, per-user selections) stays in
  `server()` / Express top level.
- **Verify scope with a stderr timestamp**: a load-time `print()` that
  appears on *every page open* is per-session work in the wrong place.
- Caveat: shared module data is **read-only shared state**. Don't let
  sessions mutate it (in-place mutation also fails to notify anyone —
  reactive-graph.md). For writable shared state use a database or a cache
  (caching.md).

## Rule 2: Never read data inside render functions

Reading/processing data inside a `@render.*` re-runs on every invalidation.
Load once (Rule 1), derive in a `@reactive.calc`, let renderers consume it.
If the derivation is expensive and repeats across sessions, cache it
(caching.md).

## Rule 3: Choose engines and formats that are fast

Recommended ladder (per the official reading-data guide):

1. **polars** is the recommended default for data work in Shiny apps —
   multithreaded, generally faster and lighter than pandas for large frames.
   pandas remains fine for small-to-medium data and anything already built on
   it.
2. **Parquet over CSV** — columnar, compressed, typed, much faster to read;
   convert once in preprocessing, don't convert at startup.
3. **DuckDB** — an embedded analytical database; query parquet (local or on
   S3) with SQL push-down and pull back only the result slice.
4. **Lazy loading** when data outgrows RAM or only slices are needed — see
   below.

Lazy patterns that push work to the engine:

```python
# polars Lazy API: filter before collect — only the needed slice downloads
# (works with local files and s3:// paths)
import polars as pl

@reactive.calc
def sales_slice():
    return (
        pl.scan_parquet("s3://bucket/sales.parquet")
        .filter(
            (pl.col("region") == input.region())
            & (pl.col("year") == input.year())
        )
        .group_by("product")
        .agg(pl.col("amount").sum())
        .collect()
    )
```

```python
# DuckDB: a view over parquet; each query reads only what it needs
import duckdb

con = duckdb.connect()   # module scope, one connection, shared (read-only use)

@reactive.calc
def sales_slice():
    return con.sql(
        "SELECT product, SUM(amount) AS total"
        " FROM read_parquet('sales.parquet')"
        " WHERE region = ?"
        " GROUP BY product",
        [input.region()],            # pass parameters — never interpolate
    ).pl()                          # or .df() / .arrow()
```

- Decide deliberately **where to materialize** (`.collect()` / `.execute()`).
  If several outputs reuse the same heavy slice, realize it once into a
  shared (ideally cached) calc. If each consumer needs a different small
  slice, stay lazy to the end. Time both — a lazy pipeline that compiles to
  an expensive query can lose to one smart collect.
- Sync DuckDB/pandas queries longer than ~100 ms don't belong inline in a
  calc — move them to `asyncio.to_thread` or an extended task
  (async-tasks.md).
- **Ibis** (or SQLAlchemy with SQL) is the lazy path for database servers:
  build lazy tables, filter/aggregate, `.execute()` at the end so only the
  small result crosses the wire.

## Rule 4: Precompute offline what doesn't need computing online

Anything deterministic — joins, cleaning, derived columns, pre-aggregated
summaries — should be computed **before the app runs** (a script, a scheduled
job), with the app reading the finished artifact. This also removes the "slow
for the first user after each restart" problem.

## Databases

```python
def server(input, output, session):
    con = connect_db()                      # per session for server databases

    @session.on_ended                       # clean shutdown per user — REQUIRED
    def _():
        con.disconnect()

    @reactive.calc
    def rows():
        return query(con, input.region())   # keep queries lazy/push-down
```

- **Open a per-session connection and close it with `@session.on_ended`.**
  Leaked connections are the classic way long-running apps die under load.
  (File-backed DuckDB/SQLite: one module-level connection, read-only use,
  is simpler and shared.)
- **Push filtering/aggregation to the database** — don't fetch a table and
  filter in pandas.
- **Cache frequent identical queries** (caching.md) and **poll changing data
  with a cheap check** (`@reactive.poll(lambda: SELECT MAX(updated_at)...)`)
  instead of re-reading on a timer.
- Use async drivers (`asyncpg`, `aiosqlite`) only where you'd otherwise block
  the loop — and remember async reactive code still runs serially
  (async-tasks.md); extended tasks remain the responsiveness mechanism.

## Downloads shouldn't recompute the dataset

The `@render.download_button` handler runs on **every click**. Precompute in
a calc; only serialize inside the handler:

```python
@reactive.calc
def filtered_data():
    return prep_data(input.year(), input.region())

@render.download_button(filename="data.csv")
def download():
    yield filtered_data().to_csv(index=False)
```

For expensive artifacts (big Excel workbooks, zips), generate the file in an
extended task (async-tasks.md) or cache the computation (caching.md).

## Uploads: parse once

Uploads arrive as temp files (`fileinfo["datapath"]`) that **may be deleted
when the next upload arrives** — parse immediately into a `@reactive.calc`
(guarded with `req`), never inside renderers. Heavy parsing of large uploads
belongs in an extended task.

```python
@reactive.calc
def uploaded_df():
    files = req(input.file1())
    return pd.read_csv(files[0]["datapath"])
```

## Startup experience

- Keep `server()` bodies and Express top level cheap — they should mostly
  *define* the reactive graph; expensive eager work belongs in imported
  modules or lazily-triggered calcs.
- Let the UI shell render before heavy work streams in (rendering-ui.md).
- On multi-process deployments **every process repeats module-scope loads** —
  lean startup and shared disk caches pay off there (caching.md,
  diagnosis.md).

## Further reading

- Reading data (the canonical guide):
  <https://shiny.posit.co/py/docs/reading-data.html>
- polars: <https://docs.pola.rs/>
- DuckDB: <https://duckdb.org/>
