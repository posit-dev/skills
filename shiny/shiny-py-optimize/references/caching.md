# Caching: Stop Paying Twice for the Same Work

A plain `@reactive.calc` remembers only its **latest** value **within one
session** — revisit a previous state or open a second browser tab and the
computation runs again. Caching is the highest-leverage fix for repeated
identical work (dashboards where many users view the same data, one user
toggling between a few views) and often yields 10–100×.

**There is no built-in equivalent of R Shiny's `bindCache()` in Shiny for
Python** (verified against the Shiny 1.8 API). Cross-session and
cross-invalidation caching is manual: ordinary Python caches at module scope,
wrapped in reactive code.

## What caches what — decision table

| Situation | Tool |
|---|---|
| No reactive reads at all (constant dataset, one-time model load) | Module scope (Core) / an imported module (Express) — data-loading.md. A cache adds nothing to key on. |
| Expensive reactive computation, several consumers in one session | `@reactive.calc` — already memoized per invalidation. Free; use it first. |
| Pure function with stable arguments (DB query, model fit, API call) repeated across sessions | `@functools.lru_cache` at module scope |
| Same, but the underlying data changes | Add a **version/timestamp** to the key, or `cachetools.TTLCache` |
| Results must be shared across processes on one machine, or survive restarts | `diskcache` (on-disk) |
| Results too big for RAM, or shared across machines | Cache the *query*, not the data (DuckDB/parquet, data-loading.md); or a shared store (Redis/valkey) |

## The core pattern: module-level cache + reactive wrapper

```python
# shared.py — module scope, loaded once per process, shared by every session
import functools
import pandas as pd

@functools.lru_cache(maxsize=128)
def get_sales(region: str, year: int, version: str) -> pd.DataFrame:
    return fetch_and_aggregate(region, year, version)   # expensive
```

```python
# app.py (Express shown; same idea in Core inside server())
from shiny import reactive, render
import shared

@reactive.calc
def sales_version():
    # Cheap query whose value changes when the data does — part of the key,
    # so stale entries are never served when upstream data changes.
    return db.scalar("SELECT MAX(updated_at) FROM sales")

@reactive.calc
def sales_data():
    return shared.get_sales(
        input.region(), int(input.year()), sales_version()
    )

@render.data_frame
def table():
    return sales_data()          # second user with same filters: instant
```

Every session shares the same `lru_cache` entries because the *function* is
module-level. The `@reactive.calc`s exist to (a) memoize within a session and
(b) feed reactive values into the cache keys.

## Hard rules

1. **The key must capture every input that affects the result.** A missing
   input means silently *stale or wrong* results served from cache — not an
   error. When the wrapped function reads several values, every one must be
   an argument (pass them from the wrapping calc).
2. **Only cache pure functions.** A function that reads `input.x()`, uses
   `session`, writes files, or logs can't be keyed correctly.
3. **Include a data version in the key when the underlying data changes** —
   `SELECT MAX(updated_at)`, a file mtime, an S3 ETag — or use a TTL
   (`cachetools.TTLCache(maxsize=..., ttl=300)`), or accept staleness
   explicitly.
4. **Cached results are shared, mutable state.** `lru_cache` returns the
   *same object* to every caller. In-place mutation (sorting a cached
   DataFrame, appending to a cached list) silently corrupts every other
   consumer. Treat cached results as read-only, or return copies
   (`df.copy()`) at the cache boundary.
5. **Keys must be hashable and cheap**: scalars, strings, small tuples.
   DataFrames aren't hashable — use a scalar surrogate (a fingerprint like
   `len(df)`, `max(df["ts"])`, or a content hash) as the key.
6. **Bound memory.** `functools.cache` is *unbounded* — prefer
   `functools.lru_cache(maxsize=...)`. Each entry holds a full DataFrame;
   128 big frames can exhaust RAM faster than no cache at all.
7. **Caches are per-process.** With N app processes (Connect, self-hosted
   scaling) every process has its own in-memory cache: N cold misses per
   key, and N copies in RAM. `diskcache` shares one store across processes
   on the same machine; multi-machine deployments need a shared store.
8. **Clear caches when code or data schema changes.** An in-memory cache
   lives as long as the process; a disk cache outlives a redeploy. Include
   the app/schema version in the key or the cache directory when in doubt.

## Disk cache for cross-process sharing

```python
# shared.py
import diskcache

cache = diskcache.Cache("app_cache/queries")   # relative to the app directory

def get_sales(region: str, year: int, version: str):
    key = f"sales/{region}/{year}/{version}"
    hit = cache.get(key)
    if hit is not None:
        return hit
    result = fetch_and_aggregate(region, year, version)
    cache.set(key, result, expire=3600)        # 1 hour, belt and suspenders
    return result
```

- Values are pickled to disk — they must be serializable (no live DB
  connections, no lambdas). pandas/polars/numpy objects serialize fine.
- One entry serves every process on the machine; delete the directory when
  the data or code changes (add it to the deploy checklist).

## Caching data vs. rendered artifacts

- Cache the **data** (shared calc around a cached function) when multiple
  outputs derive from it — one entry serves many outputs. The better default.
- Cache the **artifact** (the rendered plot bytes, the serialized table)
  only when rendering itself dominates. Shiny for Python has no built-in
  plot cache (R's `renderCachedPlot`/`bindCache` have no equivalent), so this
  means your own keying — rarely worth it; cache the data instead.

## Checklist before adding a cache

1. Does the computation actually repeat? (Trace or time it — don't cache
   speculatively.)
2. Does the key capture **every** input that affects the result?
3. Are the keys cheap and hashable?
4. Is the result treatable as read-only (or copied at the boundary)?
5. Could one user's data leak to another via a shared key? Never cache
   user-private computations at module scope.
6. Does the underlying data change? Then the key needs a version, or a TTL,
   or both.
7. Multi-process deployment: is the in-memory duplication acceptable, or do
   you need diskcache?

## Further reading

- `functools`:
  <https://docs.python.org/3/library/functools.html#functools.lru_cache>
- `cachetools`: <https://cachetools.readthedocs.io/>
- `diskcache`: <https://grantjenks.com/docs/diskcache/>
- R Shiny's `bindCache()` (for contrast — no Python equivalent):
  <https://shiny.posit.co/r/articles/improve/caching/>
