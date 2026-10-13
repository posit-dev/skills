---
name: shiny-reactivity
description: Design and debug Shiny's reactive graph in R. Use when choosing between reactive(), observe(), observeEvent(), and eventReactive(); managing state with reactiveValues; controlling when things run with req(), bindEvent(), bindCache(), or debounce(); or debugging reactivity with reactlog, tracebacks, and profvis. Triggers on reactive bugs, outputs not updating, reactives firing too often, invalidation, infinite loops, and the observer-writes-reactiveValues anti-pattern.
metadata:
  author: Samuel Bharti (@samuelbharti)
  version: "1.0"
license: MIT
---

# Reactive Design & Debugging in Shiny

Most Shiny bugs are reactive-graph bugs: the wrong things run, run too often, or don't run at all. Write reactivity so the graph is obvious, then debug by inspecting the graph — not by reading code top to bottom.

## The mental model

Shiny builds a **dependency graph**: inputs → reactive expressions → outputs/observers. When an input changes, everything downstream is **invalidated** and lazily recomputed. You don't call reactives in order; you declare dependencies and Shiny schedules them.

## The building blocks — pick the right one

| Construct | Purpose | Eager/lazy | Returns a value? |
|---|---|---|---|
| `reactiveVal()` / `reactiveValues()` | **Mutable state** you set explicitly | — | get/set |
| `reactive(expr)` | **Compute a value** from inputs/other reactives | lazy + cached | yes — call it like `x()` |
| `eventReactive(event, expr)` | Computed value that updates **only** when `event` fires | lazy | yes |
| `observeEvent(event, handler)` | **Side effect** in response to an event | eager | no |
| `observe(expr)` | Side effect tracking all reactive reads in `expr` | eager | no |

**Rules of thumb:**
- Use `reactive()` to *compute*; use `observe`/`observeEvent` only for *side effects* (writing files, updating inputs, showing notifications). A construct that returns a value you use elsewhere should almost always be a `reactive()`.
- To inspect a module's reactive state, have the module **return** a `reactive()` (or a list of reactives), never a plain value.
- Prefer a **list of `reactiveVal()`** over a single `reactiveValues()` object for explicit state. Get/set on a `reactiveVal()` is visibly a function call (`state$count()` to read, `state$count(n)` to set), whereas `rv$count <- n` reads like ordinary R assignment and hides that it's reactive — easy to misread.
- Keep reactives small and single-purpose — one job each makes the graph legible and avoids over-broad invalidation.

## The #1 anti-pattern: observers that write state

Writing to `reactiveValues` from an `observe` to feed a render **hides the dependency** from the graph — the thing this whole framework exists to make visible:

```r
# BAD — the nrows -> data edge is invisible; harder to trace, test, and reason about
data <- reactiveVal()
observe({ data(head(cars, input$nrows)) })
output$plot <- renderPlot(plot(data()))

# GOOD — the dependency is explicit in the graph
data <- reactive(head(cars, input$nrows))
output$plot <- renderPlot(plot(data()))
```

Use `reactiveVal()`/`reactiveValues()` only when you genuinely need mutable state that several events update (accumulators, "either button sets this", pause/resume). When an observer must update a value it also reads, wrap the read in `isolate()` to avoid an infinite invalidation loop.

`isolate(x())` reads a reactive's current value **without** taking a dependency on it — the tool for "use this value but don't re-run when it changes."

## Control when things run

- **`req(x)`** — stop silently (no output, no error) until `x` is truthy. The right gate for "don't compute until the user has chosen something." A stray `req()` is the most common cause of "output never appears."
- **`validate(need(cond, "message"))`** — like `req()` but shows the user a message. For richer, field-level validation install **`shinyvalidate`** (`install.packages("shinyvalidate")`) and use its `InputValidator`.
- **`x |> bindEvent(input$go)`** — make a reactive/render/observer respond **only** to `input$go` (the modern, composable replacement for `eventReactive`/`observeEvent`'s event arg). Pair with `ignoreInit`/`ignoreNULL` as needed.
- **`x |> bindCache(input$a, input$b)`** — cache results by key; huge speedups for slow computations, shareable across sessions. **Caveat:** the cache key determines dependencies — `reactive({input$x + input$y}) |> bindCache(input$x)` will *not* recompute when only `input$y` changes. Pair `bindCache()` then `bindEvent()` for slow, on-demand work.
- **`debounce()` / `throttle()`** — rate-limit a fast-changing reactive (typing, sliders) so downstream work doesn't fire on every keystroke.

## Debug the reactive graph

**See the graph — `reactlog`** (the canonical tool — install it: `install.packages("reactlog")`):

```r
reactlog::reactlog_enable()   # or options(shiny.reactlog = TRUE), before launching
shiny::runApp("app")
# In the running app press Ctrl+F3 (Cmd+F3 on Mac), or after stopping:
shiny::reactlogShow()
```

It shows every reactive, its dependencies, and what invalidated what — the direct answer to "why did this (not) update." Dev-only: it exposes reactive source and grows unbounded; never enable in production.

**See the error — tracebacks:**

```r
options(shiny.fullstacktrace = TRUE)    # full traceback to the console on error
options(shiny.sanitize.errors = FALSE)  # show real error text (dev only)
```

The real traceback is in the **R console / server stdout**, not the browser (the browser shows a sanitized "An error has occurred"). Drop `browser()` into a reactive to step through it; use `message()`/`cat(file = stderr())` for lightweight tracing without perturbing the graph.

**Find the slow part — `profvis`:**

```r
profvis::profvis(shiny::runApp("app"))  # interact, then read the flame graph
```

## Symptom → fix

**"Output didn't update."**
1. Is there a `req()`/`validate()` short-circuiting it? Check the gate.
2. Open `reactlog` — does the output actually depend on the input you changed? A missing edge means the value was read in `isolate()`, via the observer-write anti-pattern, or under the wrong ID.
3. Frozen by `freezeReactiveValue()` / an `eventReactive` waiting on a different trigger?

**"Reactive fires too often / app is slow."**
1. In `reactlog`, find the over-broad dependency — a reactive reading a whole `input`/`reactiveValues` object instead of one field.
2. Split the reactive; depend only on what's needed; gate with `bindEvent()`; rate-limit with `debounce()`; cache with `bindCache()`.
3. Confirm with `profvis`.

**"An error has occurred."**
1. Read the **console traceback** (`shiny.fullstacktrace = TRUE`) — the browser message is sanitized.
2. Reproduce the failing reactive in `testServer` (see `shiny-testing`) to get a plain R traceback.

## See also

- **`shiny-testing`** — test reactives headlessly (`testServer`) and end-to-end (`shinytest2`).
- **`shiny-for-agents`** — drive/inspect a running app from a browser without flaky sleeps.
- **`shiny-bslib`** — building the UI.

## References

Fetch only for an edge case or to confirm a signature:

- [Mastering Shiny — Reactivity](https://mastering-shiny.org/reactivity-intro.html) and [The reactive graph](https://mastering-shiny.org/reactive-graph.html).
- [`bindEvent` / `bindCache`](https://rstudio.github.io/shiny/reference/bindEvent.html) and [caching guide](https://shiny.posit.co/r/articles/improve/caching/).
- [shinyvalidate](https://rstudio.github.io/shinyvalidate/) — input validation.
- [reactlog](https://rstudio.github.io/reactlog/) — reactive graph visualizer.
