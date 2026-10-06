# Caching: Stop Paying Twice for the Same Work

Caching is the highest-leverage code-level fix for Shiny apps that serve
repeated identical computations — dashboards where many users look at the same
data, or one user toggling between the same few views. It matters because a
plain `reactive()` remembers only its **latest** value: revisit a previous
state and the expensive computation runs again. Scaling an app means either
adding compute or reducing the compute needed — caching reduces it, often by
10–100× ("a few lines of precomputation or caching logic can often lead to
10X–100X better performance" — Joe Cheng). Profile first (diagnosis.md) and
aim caches at computations the profile shows repeating.

## `bindCache()`: cache any reactive or renderer

Shiny ≥ 1.6.0. Works on `reactive()` and on `renderTable`, `renderPlot`,
`renderText`, `renderUI`, `renderPlotly`, etc.:

```r
# Before
city_data <- reactive({ fetchData(input$city) })

# After
city_data <- reactive({ fetchData(input$city) }) |>
  bindCache(input$city)
```

```r
# Renderers work the same way — list every reactive value the body reads
output$slow_plot <- renderPlot({
  data() |>
    why_does_this_take_so_long(input$plot_type)
}) |>
  bindCache(data(), input$plot_type)
```

How it works, and why the keys matter:

- The **cache-key expressions become the reactive dependencies**; the original
  body runs inside `isolate()`. When an input changes, Shiny re-runs only the
  cheap key expressions, hashes their values, and looks them up — the expensive
  body runs **only on a miss**.
- Shiny automatically appends the function body + result type to the key, so
  `reactive({input$x * 2})`, `reactive({input$x * 4})`, and
  `renderText({input$x * 4})` with the same `bindCache(input$x)` never collide.
- **The keys must capture everything the body reads.** A missing key = wrong
  results served from cache (not an error!). When the body reads `data()`,
  either include `data()` as a key or key on the upstream inputs that uniquely
  determine `data()` — only if they truly do.
- First request computes and stores; same-key requests (from **any session**
  with `cache = "app"`) return instantly. "It's still slow, but at least it's
  only slow once."

Key hygiene:

- Keys must be **cheap to hash**: scalars, short strings, small vectors.
  Hashing a 500k-row data frame takes ~1 ms (`system.time(rlang::hash(x))` —
  measure before assuming it matters); avoid making big data frames keys when
  a scalar surrogate exists:
  ```r
  # Surrogate key: still takes the dependency on bigData(), hashes cheaply
  reactive({ summarize(bigData(), x = mean(x)) }) |>
    bindCache({ max(bigData()$time) })
  ```
- Reference-semantics objects (environments, R6, external pointers, functions,
  reactive expressions) may not survive the round-trip. `cache_disk(warn_ref_objects
  = TRUE)` warns on these — it catches the classic bug `bindCache(r)` (caching
  the *reactive object*) where `bindCache(r())` (its value) was meant.

## What to cache: data vs. plots

- Cache the **data** (the shared reactive) when multiple outputs derive from
  it — one cache entry serves many outputs, and downstream cheap steps stay
  uncached and flexible.
- Cache the **plot** (the renderer) when the rendering itself is the expensive
  part (big ggplot builds, plotly serialization) and the plot is what users
  request repeatedly.
- Caching data is usually the better default; cache plots when profiling shows
  render time dominating or when the same plot is re-requested across sessions.

## Cache scopes

`bindCache(x, ..., cache = "app")`:

- **`cache = "app"`** (default): shared across all sessions in the R process.
  This is what makes caching a *scaling* tool — the first user computes,
  everyone else hits the cache. Caveat: values can **leak information between
  sessions** if keys are incomplete or via timing side channels. Don't cache
  user-private computations app-level.
- **`cache = "session"`**: private per session; no cross-session benefit, no
  leakage. Use for user-specific data.
- **A cache object** (see below) for custom size/expiry/backends.

Defaults and configuration (cachem-backed, LRU eviction):

- Default app-level *and* session-level caches: `cachem::cache_mem(max_size =
  200e6)` — 200 MB each.
- Configure globally: `shinyOptions(cache = cachem::cache_mem(max_size = 500e6))`
  at the top of `app.R`/`global.R`.
- Per-session: `session$cache <- cachem::cache_mem(max_size = 100e6)` inside
  the server function.
- Expiry: `cachem::cache_mem(max_size = Inf, max_age = 300)` (5 minutes), or
  per-object `max_age`/`max_n`.

## Backends: `cachem`, and when disk/Redis matter

- `cachem::cache_mem()` — in-process memory (the default).
- `cachem::cache_disk("./app_cache/cache/")` — shared across R processes on
  the machine and persists across restarts. This is how a **multi-process
  deployment** (Connect, Shiny Server Pro) still gets cross-session cache hits:
  `shinyOptions(cache = cachem::cache_disk("./app_cache/cache/"))` at the top
  of the app. rsconnect excludes `app_cache/` from deployments; keep a `cache/`
  subdir to avoid colliding with `app_cache/sass/`. **Clear it when you redeploy
  the app or upgrade R/packages** — stale caches outlive code changes, and
  Connect redeploys otherwise start empty anyway.
- shinyapps.io: disk caches are shareable within an instance only; nothing
  persists past instance shutdown.
- Multiple machines / huge shared caches: implement a custom backend — any
  object with `$get(key)` (missing key returns `structure(list(), class =
  "key_missing")`) and `$set(key, value)`. The caching article includes full
  Redis (`redux::hiredis`) and `storr` examples with a 20 MB `allkeys-lru`
  Redis config.

## `memoise()`: cache plain functions outside the reactive system

For expensive **pure functions** — DB queries, model fits, API calls with
stable parameters — memoise works at the function level, independent of
reactivity:

```r
library(memoise)
m_get_query <- memoise(DBI::dbGetQuery)                            # in-memory
m_get_query <- memoise(DBI::dbGetQuery,
                       cache = cachem::cache_disk("app_cache/q"))  # persistent
```

- Cache key = function identity + argument values. Repeat calls are instant
  (real example: a repeated SQL query 1.25 s → 0.005 s).
- Call the memoised function from inside reactives/renderers as usual. Because
  memoise ignores reactivity, **include data-version information in the
  arguments** (a timestamp, a max(id), a config value) or the result goes stale
  when the underlying data changes; memoise also supports `timeout` and manual
  `cache$prune()`/`drop_cache()`.
- To share Shiny's cache with memoised functions:
  `memoise(fn, cache = getShinyOption("cache"))`, or per-session
  `memoise(fn, cache = session$cache)`.
- Only memoise *pure* functions — memoising a function that reads `input$`
  doesn't work (inputs aren't serializable keys) and memoising one with side
  effects is a correctness bug.

## Plot caching specifics

`renderPlot(...) |> bindCache(...)` keys plots on their **pixel size** as well
as your keys, so two users with slightly different window sizes don't share
entries. Widths are rounded to ~20% growth steps (400, 480, 576, 691…) and the
browser scales the delivered image down — a 450 px div gets the 480 px plot.
This is controlled by `sizePolicy` (`sizeGrowthRatio(width = 400, height =
400, growthRate = 1.2)` is the default) and inherited from `renderCachedPlot()`
(Shiny 1.2.0, superseded by `bindCache()` in 1.6.0 but still the source of the
mental model and the `cacheKeyExpr`/`sizePolicy` vocabulary).

## Checklist before adding a cache

1. Did the profile show this computation repeating? (Don't cache speculatively.)
2. Do the keys capture **every** reactive read in the body?
3. Are the keys cheap to hash?
4. Is the result serializable (no environments/R6/live connections)?
5. Is `cache = "app"` safe here — could one user's result leak to another?
6. Does the underlying data change? If yes, the key needs a version/timestamp
   component, or use `max_age`.
7. On Connect/Shiny Server Pro with `cache_disk`: is the cache directory
   excluded from deployment and cleared on upgrades?
