# The Reactive Graph: Computing Less Without Changing Behavior

Most "slow everywhere" Shiny apps are slow because the reactive graph does far
more work than the user's actions require. This file explains *why* Shiny
recomputes, then gives every tool for narrowing the graph. All of these fixes
preserve app logic — they change when and how often code runs, not what it
computes.

## The mental model (why over-recomputation happens)

Shiny's reactive engine works in **flush cycles**: receive changed inputs →
invalidate everything downstream (following dependency arrows) → re-execute
invalidated consumers → send results. Three consequences drive most
performance problems:

1. Every read of a reactive source creates a dependency arrow; when the source
   invalidates, everything downstream must re-execute — **even if the result
   would be identical**. Invalidation is all-or-nothing per node.
2. Dependency arrows are discovered at execution time and erased after firing.
   Conditional reads (`if (input$x) ...`) create conditional edges, so the
   graph changes shape over time and can hide dependencies from you.
3. Reactives are **lazy**: nothing downstream of an unexecuted reactive runs.
   An output that isn't requested (hidden, `req()`-failed) pulls nothing.

The reactive graph has three atoms: **reactive values** (inputs, `reactiveVal`),
**reactive expressions** (derived, cached, lazy), and **observers/output
renderers** (eager, side effects). Performance work is mostly about shaping
this graph so expensive nodes sit downstream of narrow dependencies.

## Compute once, consume twice: shared reactive expressions

The single most common structural fix. When two outputs each re-derive the
same thing, every input change pays for the derivation twice:

```r
# Before: duplicated computation, runs on every relevant input change
output$earnings <- renderText({
  scorecard |>
    filter(state == input$state, score_sat_avg >= input$sat) |>
    pull(amnt_earnings_med_10y) |> mean(na.rm = TRUE) |>
    scales::dollar(accuracy = 10)
})
output$earnings_plot <- renderPlot({
  scorecard |>
    filter(state == input$state, score_sat_avg >= input$sat) |>   # again!
    ggplot(aes(amnt_earnings_med_10y)) + geom_histogram()
})
```

```r
# After: one shared reactive, computed once per change, cached between changes
filtered_data <- reactive({
  scorecard |>
    filter(state == input$state, score_sat_avg >= input$sat)
})

output$earnings <- renderText({
  filtered_data() |> pull(amnt_earnings_med_10y) |> mean(na.rm = TRUE) |>
    scales::dollar(accuracy = 10)
})
output$earnings_plot <- renderPlot({
  filtered_data() |> ggplot(aes(amnt_earnings_med_10y)) + geom_histogram()
})
```

A plain `reactive()` remembers only its **latest** value (it re-computes when
invalidated, but caches between reads); with `bindCache()` it also remembers
*previous* values (see caching.md). When a downstream consumer needs several
different slices, either have each consumer `filter()` the shared reactive
cheaply, or create multiple fine-grained reactives — the goal is that each
expensive step has exactly one graph node.

## Gate with `req()`: don't compute on not-ready inputs

`req(input$x)` raises a *silent* exception that stops the current expression
and leaves the output blank until the condition holds. It is the standard fix
for "everything computes at startup with empty inputs":

```r
output$plot <- renderPlot({
  req(input$state)          # blank until a state is chosen — nothing runs
  filtered_data() |> ...
})
```

- `req()` on a **false-y** value (`NULL`, `""`, `FALSE`, empty vector) halts;
  anything else passes through as its value.
- `req(cond, cancelOutput = TRUE)` keeps the **last valid output** visible
  instead of blanking it — often the better UX for transient invalid states.
- Common startup bug class: an output renders before an observer has populated
  its input choices via `updateSelectInput()`, computes on `NULL`, throws, and
  (in the worst case) triggers error-handling overhead per flush. A `req()`
  makes the whole chain a no-op until choices exist.

## `isolate()`: read a value without depending on it

```r
observe({
  r$x                                  # dependency — should re-run when x changes
  r$count <- isolate(r$count) + 1      # no dependency — avoids self-triggering loop
})
```

`isolate(expr)` evaluates `expr` immediately with *no* dependency registration.
Primary uses:

- **Button-gated computation**: read the current filter values only when the
  user clicks Go, so typing into a filter costs nothing:
  ```r
  results <- eventReactive(input$go, {
    expensive_filter(isolate(input$state), isolate(input$sat))
  })
  ```
  (With `eventReactive`/`bindEvent` the event expression is already isolated —
  see below — so plain `isolate()` is for observers and mixed cases.)
- **Breaking read/write loops**: an observer that reads and writes the same
  `reactiveVal` loops forever without it.

Cost of `isolate()`: the reader stops being notified of changes, so use it
only where staleness-until-event is intended (buttons, save actions), never to
silently paper over a dependency you don't understand.

## Event-driven execution: `eventReactive()`, `observeEvent()`, `bindEvent()`

Event helpers make *one* expression the trigger and `isolate()` everything
else. `eventReactive(input$go, {...})` is equivalent to
`reactive(isolate({...}))` keyed on `input$go`.

```r
# Trigger on the button only — typing in x/y is now free
results <- eventReactive(input$go, {
  expensive(input$x, input$y)
})
```

Options: `ignoreNULL = TRUE` (default; also treats `actionButton` value 0 as
NULL), `ignoreInit = FALSE` (TRUE skips the initial run), `once = TRUE`
(`observeEvent` only; auto-unsubscribes after first fire — good for expensive
one-time setup).

**`bindEvent()`** (Shiny ≥ 1.6.0) is the modern, composable equivalent — it
works on reactives, observers, *and render functions*, which `eventReactive`
cannot decorate:

```r
output$plot <- renderPlot({
  plot(cars[seq_len(input$nrows), ])
}) |>
  bindEvent(input$go)          # plot only when the button is clicked
```

Signature: `bindEvent(x, ..., ignoreNULL = TRUE, ignoreInit = FALSE, once =
FALSE)`. Caveat: on `observe()` it mutates in place and only works on observers
that haven't executed yet.

Anti-pattern to remove when you see it — defining renderers inside observers
to "control when they run":

```r
# Wrong: re-creates the output binding on every click; fights the reactive model
observeEvent(input$go, {
  output$plot <- renderPlot({ ... })
})
```
The right tool is exactly this section: define the renderer once at server top
level and use `bindEvent()`/`eventReactive()`/`req()` to control execution.

## `freezeReactiveValue()`: break update-fires-update loops

When an observer updates an input (`updateSelectInput(...)`) that downstream
reactives read, the update itself triggers a cascade — often recomputing
expensive outputs with an *intermediate* value. Freezing makes the next read of
that input raise the same silent exception as `req(FALSE)` until the flush ends:

```r
observeEvent(input$country, {
  freezeReactiveValue(input, "city")     # downstream stays quiet this flush
  updateSelectInput(session, "city", choices = cities_for(input$country))
})
```

Official caveat: `freezeReactiveVal()` and `freezeReactiveValue()` are being
considered for deprecation *except* when `x` is `input` — treat it as an
input-only escape hatch. Alternative loop-breakers: `bindEvent(...,
ignoreInit = TRUE)`, or gate with a `reactiveVal` "initialized" flag.

Related real-world case: filters initialized empty → server populates choices
→ the population update re-renders 15 plots with unchanged data (6 s → 3 s
after gating the first-change case with a `reactiveVal` detector).

## Rate-limit chatty inputs: `debounce()` and `throttle()`

Sliders and text boxes fire dozens of invalidations per interaction; an
expensive chain downstream turns each into full recomputation.

```r
search_term <- reactive(input$search) |> debounce(500)   # fire 500 ms after typing stops
cursor     <- reactive(input$hover) |> throttle(250)     # fire at most every 250 ms
```

Semantics that matter (easy to get wrong):

- These rate-limit the **invalidation signal**, not execution. The wrapped
  reactive still runs on every change — so only wrap a **cheap** reactive
  (usually a direct input read) when the *downstream* work is expensive.
  Debouncing an already-expensive reactive does nothing.
- **`debounce()`** waits for quiet — right for text search boxes, sliders being
  dragged, anything where intermediate values are meaningless.
- **`throttle()`** emits at a steady rate while changes keep arriving — right
  for hover/pointer positions where you want bounded, continuous updates.
- `millis` can itself be a reactive (user-configurable windows). Default
  `priority = 100` is deliberate: the internal timers must run before
  downstream observers.
- Single-threaded R makes timings **minimums, not guarantees**; if one
  downstream computation takes longer than the window, no window helps — use a
  button or `ExtendedTask` instead.

Cheaper alternatives when a control should simply *not* fire until submitted:
an `actionButton` + `bindEvent(input$go)`, or requiring Enter in text inputs.

## Timers: `invalidateLater()`, `reactivePoll()`, `reactiveFileReader()`

- **`invalidateLater()` at the *start* of a slow reactive is an infinite
  busy-loop**: the timer is scheduled immediately and the reactive re-fires the
  moment it finishes. Schedule on exit so the timer starts *after* completion:
  ```r
  x <- reactive({
    on.exit(invalidateLater(500), add = TRUE)
    slow_step(); another_step()
  })
  ```
- **Polling external data invalidates all downstream consumers on every tick,
  even when nothing changed.** `reactivePoll(millis, session, checkFunc,
  valueFunc)` fixes this: `checkFunc` is a *cheap* probe (e.g.
  `file.mtime("data.csv")`, or `SELECT MAX(updated_at) ...`) and `valueFunc`
  (the expensive read) only runs when the probe value changes:
  ```r
  live_data <- reactivePoll(
    10000, session,
    checkFunc = function() DBI::dbGetQuery(con, "SELECT MAX(updated_at) FROM sales"),
    valueFunc = function() DBI::dbReadTable(con, "sales")
  )
  ```
  `reactiveFileReader(millis, session, filePath, readFunc)` is the file-mtime
  special case.
- When several consumers need the same cadence, share **one** `reactiveTimer()`
  instead of many `invalidateLater()` calls.
- Timer accuracy is bounded by the single-threaded event loop — treat intervals
  as minimums.

## Choosing reactive atoms: granularity and style

- `reactive()` — derived computation: cached, lazy, read-only. Prefer it for
  anything downstream of inputs.
- `reactiveVal()` — one settable value; `rv()` reads, `rv(x)` writes.
- `reactiveValues()` — named slots; **each name invalidates independently**.
  Splitting state into separate slots limits the invalidation blast radius:
  reading `r$a` does not depend on `r$b`. One monolithic `reactiveValues()`
  written from many observers is a common storm source.
- Observers that write reactive values they also (transitively) read are where
  most loops and storms originate. Prefer `reactive()`-derived data over
  "observer computes and stores into a reactiveVal" — the store-and-forward
  pattern adds a graph hop and an eager computation that may not be needed.
- For cross-module signaling with explicit triggers, the `gargoyle` package
  (`init()`/`watch()`/`trigger()`) formalizes the pattern and avoids observers
  that listen to too many sources.

## Conditional and hidden dependencies

Two subtle graph shapes to check with reactlog:

1. **Conditional reads**: `cost_var <- if (input$by_bracket) input$bracket else
   "cost_avg"` registers a dependency on `input$bracket` *only in flushes where
   the switch is on*. The graph is correct but shape-shifting; a reactlog
   session with the switch both on and off shows the difference. If an
   expensive downstream consumer shouldn't re-run when a cosmetic input
   changes, move that read out of the shared path or `isolate()` it.
2. **Accidental dependencies** via shared mutable state or functions that read
   inputs deep in a call stack. Because arrows are discovered at runtime, the
   reactlog shows the *real* graph — trust it over your mental model.

## Verification

After each change in this file, re-run reactlog and answer: does one
interaction now invalidate a narrow slice? Do evaluation counts match the
number of *distinct* things being computed? Then re-profile (diagnosis.md) —
fewer executions should show up directly in profvis.
