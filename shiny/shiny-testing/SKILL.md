---
name: shiny-testing
description: Test Shiny apps in R across three layers — pure functions with testthat, reactive logic with shiny::testServer(), and end-to-end with shinytest2 (AppDriver, snapshots). Use when writing or fixing tests for a Shiny app or module, testing reactives without a browser, setting up shinytest2, or deciding what to test where. Triggers on testServer, shinytest2, AppDriver, snapshot tests, testing modules, and flaky Shiny tests.
metadata:
  author: Samuel Bharti (@samuelbharti)
  version: "1.0"
license: MIT
---

# Testing Shiny Apps

Test in three layers, fastest first. Most logic should be covered by the fast lower layers; reserve the slow browser layer for what genuinely needs rendering.

| Layer | Tool | Tests | Speed |
|---|---|---|---|
| 1. Pure functions | `testthat` | computation with no reactivity | fastest |
| 2. Reactive logic | `shiny::testServer()` | reactives, observers, module server logic | fast (no browser) |
| 3. End-to-end | `shinytest2` | rendering, JS, full round-trip, visuals | slow (headless Chrome) |

**Design for testability first:** push computation into plain functions (Layer 1) and named reactives (Layer 2). Logic buried inside `renderPlot({...})` can only be reached through the slow Layer 3.

This skill is **R-specific**. For Shiny for Python there's no `testServer` — unit-test pure functions, and use `pytest` + `shiny.playwright` controllers for E2E (see the *Shiny for Python* section of **`shiny-for-agents`**).

## Layer 1 — pure functions (testthat)

Extract non-reactive computation into ordinary functions and test them directly. No Shiny needed.

```r
test_that("filtering selects the chosen country", {
  out <- filter_country(sample_data, "Canada")
  expect_equal(unique(out$country), "Canada")
})
```

For testthat structure, fixtures, mocking, and snapshots, see the **`testing-r-packages`** skill — it all applies here.

## Layer 2 — reactive logic (testServer)

`testServer()` runs the server function in a simulated session, with no browser. Set inputs, then read reactives and outputs directly.

```r
test_that("summary reacts to the country filter", {
  testServer(myAppServer, {
    session$setInputs(country_filter = "Canada")   # set inputs
    expect_equal(filtered_data()$country[1], "Canada")  # read a named reactive
    expect_match(output$summary, "Canada")              # read an output
    session$setInputs(country_filter = "Brazil")        # multiple steps in one test
    expect_match(output$summary, "Brazil")
  })
})
```

- `session$setInputs()` exists only inside `testServer`; it sets inputs and flushes reactivity synchronously — no idle-waiting needed.
- Test a **module**: pass args to its server. `testServer(myModuleServer, args = list(id = "x", data = reactive(df)), { ... })`.
- **Limitation:** `render*` outputs that need a client (e.g. `renderPlot` sizing) don't fully execute headlessly — test the *named reactive* feeding the render, not the rendered image. That's another reason to keep logic out of `render*`.

### Expose internals for snapshots — `exportTestValues()`

Register an internal reactive so the **end-to-end** layer can assert on it (active only under `shiny.testmode`, which `shinytest2` sets automatically):

```r
exportTestValues(result = filtered_data())   # in the server function
```

Then in `shinytest2`: `app$get_value(export = "result")`, and exports are included in `app$expect_values()`. In `testServer` you usually don't need this — read reactives directly; use `session$getReturned()` to assert a **module's return value**.

## Layer 3 — end-to-end (shinytest2)

**Install it — this is the best-practice E2E path** (prefer it over hand-driving a browser, which is `shiny-for-agents`' fallback): `install.packages("shinytest2")` (pulls `chromote`), then scaffold with `shinytest2::use_shinytest2()`.

`AppDriver` drives a real app in headless Chrome (via chromote), with idle-waiting built in.

```r
library(shinytest2)
test_that("app renders the filtered summary", {
  app <- AppDriver$new("path/to/app", name = "country-filter", seed = 1)
  app$set_inputs(country_filter = "Canada")  # auto-waits for the resulting change
  app$wait_for_idle()                         # extra settle for chained reactives
  app$expect_values()                         # JSON snapshot of inputs/outputs/exports
  app$expect_screenshot()                     # visual snapshot (review on first run)
})
```

Key `AppDriver` methods: `set_inputs()`, `wait_for_idle()`, `wait_for_value()`, `get_value(input=/output=/export=)`, `get_values()`, `get_logs()`, `expect_values()`, `expect_screenshot()`, `run_js()`.

- **Prefer `expect_values()` over `expect_screenshot()`** for data — value snapshots are stable; pixels flap across machines/fonts.
- Review snapshot changes with `testthat::snapshot_review()`.
- The driver waits on Shiny's own busy/idle signal, so you never write sleeps. (For driving a *live* app outside shinytest2, see **`shiny-for-agents`**.)

## Test behavior, not wiring

Tests break when they assert *implementation* (internal IDs, intermediate values, exact HTML) instead of *behavior*. Assert what the user observes — the output value, the visible state — so refactors don't break green tests. Snapshot app author values, not the plumbing.

## Determinism (or tests flake)

- Pass `seed =` to `AppDriver`; `set.seed()` for Layer 1/2.
- Use fixed fixtures, not live data sources; freeze time (`Sys.setenv(TZ=...)`, mock `Sys.time()`).
- One assertion target per behavior; avoid asserting on timing.

## Running tests

- App-as-a-package: `devtools::test()` (tests in `tests/testthat/`).
- App directory: `shiny::runTests()` runs the app's top-level test runners in `tests/` (e.g. `tests/testthat.R`), which in turn run the testthat and shinytest2 tests.
- shinytest2 tests live in `tests/testthat/` as `test-*.R` using `AppDriver`.

## See also

- **`testing-r-packages`** — testthat 3 patterns (structure, fixtures, mocking, snapshots) underlying Layer 1.
- **`shiny-reactivity`** — design reactives so they're testable; debug failures.
- **`shiny-for-agents`** — drive/inspect a running app from a browser.
- **`review-testing`** — review existing tests for quality and coverage.

## References

- [Shiny testing overview](https://shiny.posit.co/r/articles/improve/testing-overview/) and [server-function testing](https://shiny.posit.co/r/articles/improve/server-function-testing/).
- [`testServer`](https://shiny.posit.co/r/reference/shiny/latest/testserver.html) · [shinytest2 `AppDriver`](https://rstudio.github.io/shinytest2/reference/AppDriver.html).
- [Mastering Shiny — Testing](https://mastering-shiny.org/scaling-testing.html).
