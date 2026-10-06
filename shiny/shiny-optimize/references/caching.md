# Caching: Stop Paying Twice for the Same Work

A plain `reactive()` remembers only its **latest** value — revisit a previous
state and the computation runs again. Caching is the highest-leverage fix for
repeated identical work (dashboards where many users view the same data, one
user toggling between a few views) and often yields 10–100×.

## `bindCache()`: cache any reactive or renderer

Shiny ≥ 1.6.0; works on `reactive()` and on `renderPlot`, `renderTable`,
`renderText`, `renderUI`, `renderPlotly`, etc.:

```r
city_data <- reactive({ fetchData(input$city) }) |>
  bindCache(input$city)

output$slow_plot <- renderPlot({
  data() |> why_does_this_take_so_long(input$plot_type)
}) |>
  bindCache(data(), input$plot_type)
```

How it works — and why the keys matter:

- The **cache-key expressions become the reactive dependencies**; the original
  body runs inside `isolate()`. On input change, Shiny re-runs only the cheap
  key expressions, hashes them, and looks up the result — the expensive body
  runs **only on a miss**.
- Shiny automatically appends the function body + result type to the key, so
  different reactives/renderers with the same `bindCache(input$x)` never
  collide.
- **The keys must capture every reactive read in the body.** A missing key =
  wrong results served from cache (not an error!). When the body reads
  `data()`, either include `data()` as a key or key on upstream inputs that
  truly determine it.

Key hygiene:

- Keys must be **cheap to hash**: scalars, short strings, small vectors. Avoid
  big data frames as keys — use a scalar surrogate that still takes the
  dependency:
  ```r
  reactive({ summarize(bigData(), x = mean(x)) }) |>
    bindCache({ max(bigData()$time) })
  ```
- Reference-semantics objects (environments, R6, external pointers) may not
  survive the round-trip. `cache_disk(warn_ref_objects = TRUE)` warns on these
  — it catches the classic bug `bindCache(r)` (caching the *reactive object*)
  where `bindCache(r())` (its value) was meant.

## What to cache: data vs. plots

- Cache the **data** (shared reactive) when multiple outputs derive from it —
  one entry serves many outputs. The better default.
- Cache the **plot** (renderer) when rendering itself dominates (big ggplot
  builds, plotly serialization) or the same plot is re-requested across
  sessions.
- Plot caches also key on **pixel size**: widths are rounded to ~20% growth
  steps (400, 480, 576, …) and the browser scales down, so users with slightly
  different window sizes still share entries (`sizeGrowthRatio()` controls
  this).

## Cache scopes

`bindCache(x, ..., cache = "app")`:

- **`cache = "app"`** (default): shared across all sessions in the R process —
  what makes caching a *scaling* tool. Caveat: values can **leak information
  between sessions** if keys are incomplete; never cache user-private
  computations app-level.
- **`cache = "session"`**: private per session; no cross-session benefit, no
  leakage.
- **A cachem object** for custom size/expiry/backend.

Defaults: `cachem::cache_mem(max_size = 200e6)` (200 MB) at both app and
session level. Configure:

```r
# App-wide, at the top of app.R/global.R
shinyOptions(cache = cachem::cache_mem(max_size = 500e6))
# Per session, inside server()
session$cache <- cachem::cache_mem(max_size = 100e6)
# With expiry
cachem::cache_mem(max_size = Inf, max_age = 300)   # 5 minutes
```

## Backends

- `cachem::cache_mem()` — in-process memory (default).
- `cachem::cache_disk("./app_cache/cache/")` — shared across R processes on
  the machine and persists across restarts. This is how a **multi-process
  deployment** (Connect, Shiny Server) still gets cross-session cache hits.
  Keep a `cache/` subdir (rsconnect excludes `app_cache/`), and **clear the
  cache when you redeploy the app or upgrade R/packages** — stale caches
  outlive code changes.
- shinyapps.io: disk caches are shareable within an instance only; nothing
  persists past instance shutdown.
- Multiple machines / very large shared caches: implement a custom backend
  (`$get(key)` / `$set(key, value)` — e.g. Redis via `redux`).

## `memoise()`: cache plain functions

For expensive **pure functions** — DB queries, model fits, API calls with
stable parameters:

```r
library(memoise)
m_get_query <- memoise(DBI::dbGetQuery)                            # in-memory
m_get_query <- memoise(DBI::dbGetQuery,
                       cache = cachem::cache_disk("app_cache/q"))  # persistent
```

- Key = function identity + argument values; repeat calls are instant (real
  example: repeated SQL query 1.25 s → 0.005 s).
- Memoise ignores reactivity: **include data-version information in the
  arguments** (timestamp, `max(id)`, config value) or results go stale when
  the underlying data changes. `timeout` and `drop_cache()` also exist.
- Only memoise *pure* functions — a function reading `input$` can't be keyed,
  and memoising side effects is a correctness bug.

## Checklist before adding a cache

1. Does the computation actually repeat? (Scan or profile — don't cache
   speculatively.)
2. Do the keys capture **every** reactive read in the body?
3. Are the keys cheap to hash?
4. Is the result serializable (no environments/R6/live connections)?
5. Is `cache = "app"` safe — could one user's result leak to another?
6. Does the underlying data change? Then the key needs a version/timestamp, or
   use `max_age`.
7. Multi-process deployment with `cache_disk`: is the cache directory cleared
   on redeploy?

## Further reading

- bindCache: <https://shiny.posit.co/r/articles/improve/caching/>
- cachem: <https://cachem.r-lib.org/>
- memoise: <https://memoise.r-lib.org/>
