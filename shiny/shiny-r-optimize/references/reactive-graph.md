# The Reactive Graph: Computing Less Without Changing Behavior

Most "slow everywhere" apps are slow because the reactive graph does more work
than the user's actions require. Everything here changes *when* and *how
often* code runs, never what it computes.

## Why over-recomputation happens

Shiny works in **flush cycles**: receive changed inputs → invalidate
everything downstream → re-execute → send results. Three consequences:

1. Every read of a reactive source creates a dependency; when the source
   invalidates, everything downstream re-executes — **even if the result would
   be identical**. Invalidation is all-or-nothing per node.
2. Dependencies are discovered at execution time, so conditional reads
   (`if (input$x) ...`) create conditional edges that can hide from you.
3. Reactives are **lazy**: an output that isn't requested (hidden,
   `req()`-failed) pulls nothing upstream.

## Compute once, consume twice: shared reactives

The single most common structural fix. Two outputs that each re-derive the
same thing pay for the derivation on every input change — twice.

```r
# Before: duplicated computation
output$earnings <- renderText({
  scorecard |>
    filter(state == input$state, score_sat_avg >= input$sat) |>
    pull(amnt_earnings_med_10y) |> mean(na.rm = TRUE) |> scales::dollar()
})
output$earnings_plot <- renderPlot({
  scorecard |>
    filter(state == input$state, score_sat_avg >= input$sat) |>   # again!
    ggplot(aes(amnt_earnings_med_10y)) + geom_histogram()
})

# After: one shared reactive, computed once per change
filtered_data <- reactive({
  scorecard |> filter(state == input$state, score_sat_avg >= input$sat)
})
output$earnings <- renderText({
  filtered_data() |> pull(amnt_earnings_med_10y) |> mean(na.rm = TRUE) |> scales::dollar()
})
output$earnings_plot <- renderPlot({
  filtered_data() |> ggplot(aes(amnt_earnings_med_10y)) + geom_histogram()
})
```

A plain `reactive()` remembers only its **latest** value; add `bindCache()` to
remember previous ones (caching.md). Each expensive step should have exactly
one graph node.

## Gate with `req()`

`req(input$x)` raises a *silent* exception that stops the current expression
until the condition holds — the standard fix for "everything computes at
startup with empty inputs":

```r
output$plot <- renderPlot({
  req(input$state)          # blank until a state is chosen — nothing runs
  filtered_data() |> ...
})
```

- False-y values (`NULL`, `""`, `FALSE`, empty vector) halt; anything else
  passes through as its value.
- `req(cond, cancelOutput = TRUE)` keeps the **last valid output** visible
  instead of blanking it — often the better UX for transient invalid states.

## `isolate()`: read without depending

`isolate(expr)` evaluates immediately with no dependency registration. Uses:

- **Breaking read/write loops**: an observer that reads and writes the same
  `reactiveVal` loops forever without it.
- Reading values inside observers where staleness-until-next-event is
  intended. Never use it to paper over a dependency you don't understand.

(Inside `eventReactive`/`bindEvent` the non-event reads are already isolated —
see below.)

## Event-driven execution: `bindEvent()`, `eventReactive()`, `observeEvent()`

Event helpers make one expression the trigger and isolate everything else.

```r
# Modern form (Shiny ≥ 1.6.0): works on reactives, observers, AND renderers
output$plot <- renderPlot({
  plot(cars[seq_len(input$nrows), ])
}) |>
  bindEvent(input$go)          # plot only when the button is clicked

# Equivalent for reactives
results <- eventReactive(input$go, {
  expensive(input$x, input$y)   # input$x/y are isolated
})
```

Signature: `bindEvent(x, ..., ignoreNULL = TRUE, ignoreInit = FALSE, once =
FALSE)`. `ignoreInit = TRUE` skips the initial run; `once = TRUE`
(`observeEvent` only) auto-unsubscribes after the first fire.

Anti-pattern to remove when you see it — defining renderers inside observers:

```r
# Wrong: re-creates the output binding on every click
observeEvent(input$go, {
  output$plot <- renderPlot({ ... })
})
```

Define the renderer once at server top level; control execution with
`bindEvent()`/`req()`.

## `freezeReactiveValue()`: break update-fires-update loops

When an observer updates an input that downstream reactives read, the update
retriggers them — often recomputing expensive outputs with an *intermediate*
value. Freezing makes reads of that input raise the silent exception until the
flush ends:

```r
observeEvent(input$country, {
  freezeReactiveValue(input, "city")   # downstream stays quiet this flush
  updateSelectInput(session, "city", choices = cities_for(input$country))
})
```

Treat it as an **input-only** escape hatch (other uses are being considered
for deprecation). Alternative loop-breakers: `bindEvent(..., ignoreInit =
TRUE)` or a `reactiveVal` "initialized" flag.

## Rate-limit chatty inputs: `debounce()` / `throttle()`

Shiny already debounces slider and text-input updates internally, so most
changes arrive as a single invalidation. But bursts still happen — a slow drag
or a long edit can outlast the internal debounce window, and they're
guaranteed to pile up when each invalidation's downstream computation takes
longer than the gaps between changes. High-frequency client events are the
clear-cut case:

```r
# plotly brushing fires continuously while the user drags a selection box
brush <- reactive(plotly::event_data("plotly_brushing")) |>
  debounce(500)   # wait for quiet — compute once when dragging stops
# hover/pointer positions: emit at most every 250 ms
cursor <- reactive(input$hover) |> throttle(250)
```

Semantics that matter (easy to get wrong):

- These rate-limit the **invalidation signal**, not execution — the wrapped
  reactive still runs on every change. Wrap only a **cheap** reactive (usually
  a direct input read) when the *downstream* work is expensive. Debouncing an
  expensive reactive does nothing.
- `debounce()` waits for quiet — text search, brushing. `throttle()` emits at
  a steady rate — hover/pointer positions.
- Single-threaded R makes timings **minimums, not guarantees**; if one
  downstream computation exceeds the window, use a button or `ExtendedTask`
  instead.
- These matter most for high-frequency client events (plotly brushing/hover
  today, more as client-driven patterns like shinyreact catch on) — for
  ordinary sliders and text inputs, rely on Shiny's built-in debouncing first
  and add these only when profiling shows a storm.

### When smoothing isn't enough: gate behind a button

Rate-limiting loses once changes compound — cascading `update*Input()` chains,
a long batch of settings, or downstream compute that outlasts every window.
Then stop smoothing the stream and make the expensive update wait for a
deliberate trigger:

- Gate the heavy work with `bindEvent(input$go)` and use
  **`bslib::input_task_button()`** in place of `actionButton()`: same click
  semantics, a **direct drop-in with no server-side changes and no
  `ExtendedTask` required**. On click it disables itself and shows a busy
  state until the server finishes dealing with the triggered reactivity, then
  reverts on its own — exactly the feedback a long or compounding update
  cycle needs (the shorter the cycle, the less it has to show). Users batch
  their input changes, click once, and the expensive update runs once.

## Timers

- **`invalidateLater()` at the *start* of a slow reactive is an infinite
  busy-loop**: the timer is scheduled immediately and re-fires the moment the
  reactive finishes. Schedule on exit so the timer starts *after* completion:
  ```r
  x <- reactive({
    on.exit(invalidateLater(500), add = TRUE)
    slow_step(); another_step()
  })
  ```
- **Polling external data on a timer invalidates all consumers on every tick,
  even when nothing changed.** `reactivePoll()` runs an expensive `valueFunc`
  only when a *cheap* `checkFunc` value changes:
  ```r
  live_data <- reactivePoll(
    10000, session,
    checkFunc = function() DBI::dbGetQuery(con, "SELECT MAX(updated_at) FROM sales"),
    valueFunc = function() DBI::dbReadTable(con, "sales")
  )
  ```
  `reactiveFileReader(millis, session, filePath, readFunc)` is the file-mtime
  special case.
- Several consumers needing the same cadence should share **one**
  `reactiveTimer()` instead of many `invalidateLater()` calls.

## Granularity: splitting state limits the blast radius

- Prefer `reactive()` for derived values — cached, lazy, read-only.
- `reactiveValues()` slots **each invalidate independently** — reading `r$a`
  does not depend on `r$b`. One monolithic `reactiveValues()` written from
  many observers is a common storm source; split it.
- Observers that write reactive values they also (transitively) read are where
  most loops originate. Prefer `reactive()`-derived data over "observer
  computes and stores into a reactiveVal".

## Conditional and accidental dependencies

Two subtle shapes to check with reactlog:

1. **Conditional reads**: `if (input$by_bracket) input$bracket else ...`
   depends on `input$bracket` *only in flushes where the switch is on*. If an
   expensive consumer shouldn't re-run when a cosmetic input changes, move
   that read out of the shared path or `isolate()` it.
2. **Accidental dependencies** via functions that read inputs deep in a call
   stack. The reactlog shows the real graph — trust it over your mental model.
