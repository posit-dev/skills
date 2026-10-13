---
name: shiny-for-agents
description: Drive, inspect, and debug a running Shiny app (R and Python) with a browser tool (Playwright or agent-browser). Use when launching a Shiny app for inspection, driving its UI without flaky sleeps, reading server-side errors the browser can't see, or authoring an app to be legible to agents. Triggers on driving or screenshotting a Shiny app, the shiny:busy/idle/error JS events, and server errors invisible to the browser.
metadata:
  author: Samuel Bharti (@samuelbharti)
  version: "1.0"
license: MIT
---

# Shiny for Agents

Shiny is **split-runtime**: the UI (DOM, inputs/outputs) runs in the browser, but the reactive graph, all state, and the logic run in a separate R/Python **server process** over a websocket. Driving the browser (Playwright/agent-browser) shows you only the client half — the half that is *not* the source of truth.

**What you can see today, and what you can't:**

| Readable from the browser | NOT readable (lives in the server) |
|---|---|
| DOM, rendered output, input values (`Shiny.shinyapp.$inputValues`) | Current value of any reactive/expression/scoped variable |
| Busy/idle state, the `shiny:*` JS events | Why a reactive fired, the invalidation trace |
| Errors *if* devmode is on (see below) | Server errors/warnings (unless surfaced) |

So: drive and assert from the browser, but get errors from the **server process output**, and design the app so its logic is testable without a browser at all. The deepest introspection (reading reactive values, tracing invalidation) needs Shiny-side support that doesn't exist yet — see the last section.

## 0. Setup — install the best-practice tooling

Install the recommended packages first; the no-install/manual path is a **fallback, not the default**. Use the project's env manager (`renv`, `uv`/`venv`), not global installs; confirm before system/sudo-level steps.

- **R (install these):** `install.packages(c("shinytest2", "reactlog"))` — `shinytest2` is the official E2E tool (drives real Chrome via `chromote` with idle-waiting built in); `reactlog` is the reactive-graph debugger. See **`shiny-testing`** / **`shiny-reactivity`**.
- **Python (install these):** `uv add --dev pytest playwright pytest-playwright` then `uv run playwright install chromium`; use the `shiny.playwright` controllers for E2E.
- **Browser driver:** Playwright is JS/Python; **R has no Playwright** — drive R apps from `chromote` (which `shinytest2` already uses) or from a Playwright/agent-browser process pointed at the running app over HTTP. The `shiny-busy` idle signal (below) is identical either way.
- **Interactive driving:** prefer the **Playwright MCP or agent-browser** tool when present (no install). *Alternate* — raw Playwright (Python) / `chromote` (R) + the idle helper below.
- **Fallback only** (can't install / locked-down env): drive an already-running app and scrape server stdout for errors (see *Read errors the browser can't show*). On restricted Linux, the official `mcr.microsoft.com/playwright` image ships browsers + OS libs.

## 1. Authoring for legibility

Habits that make an app driveable and debuggable without instrumentation:

- **Stable, explicit IDs.** Hand-write every `inputId`/`outputId` (e.g. `id = "country_filter"`). Never auto-generate them — your selectors and assertions depend on them.
- **Consistent modules.** One `moduleServer(id, ...)` per module, every child ID wrapped in `ns()`, so the DOM id is predictable: `#<moduleId>-<inputId>`.
- **Logic in named reactives / pure functions, not inside `render*`** — so it's testable without a browser. See **`shiny-reactivity`** for reactive design and **`shiny-testing`** for the headless test layers.

## 2. Run for inspection

Launch once, fixed port, dev features on, randomness pinned. Use [scripts/launch_app_dev.R](scripts/launch_app_dev.R) or:

```r
options(shiny.port = 7654, shiny.host = "127.0.0.1", shiny.fullstacktrace = TRUE)
shiny::devmode(TRUE)             # client-side error console + dev defaults
set.seed(1); Sys.setenv(TZ = "UTC")
shiny::runApp("path/to/app", launch.browser = FALSE)
```

- Run it in the **background and capture stdout/stderr** — that stream is your source of truth for server errors.
- `launch.browser = FALSE` — *your* browser attaches, at `http://127.0.0.1:7654`.
- Determinism: fixed seed/timezone/fixtures so assertions don't flap.

## 3. Drive the app — never `sleep`, wait on `shiny-busy`

> Act → wait for the server to go idle → assert. **Never** `waitForTimeout`/`sleep`.

This section is for **live interactive driving** (Playwright MCP / agent-browser against a running app). For anything you'd *commit as a test*, use `shinytest2` (R) or the `shiny.playwright` controllers (Python) — they encapsulate all of this; see **`shiny-testing`**. The helper below is the fallback for the no-wrapper case.

Shiny adds the **`shiny-busy` class to `<html>`** while the server works and removes it when idle — the same signal `shinytest2` waits on internally. Wait on that. Full helper (connect, idle-wait, error recorder): [scripts/wait_for_shiny_idle.js](scripts/wait_for_shiny_idle.js).

```js
// idle = no `shiny-busy` on <html>, stable for 250ms (absorbs the busy-not-yet-set race)
await page.waitForFunction((stableMs) => {
  if (document.documentElement.classList.contains('shiny-busy')) {
    window.__lastBusy = Date.now(); return false;
  }
  if (window.__lastBusy === undefined) return true;
  return Date.now() - window.__lastBusy >= stableMs;
}, 250, { polling: 50, timeout: 30000 });
```

The act → settle → assert loop:

```js
await page.fill('#country_filter', 'Canada');   // ACT
await waitForShinyIdle(page);                    // SETTLE
const txt = await page.textContent('#summary');  // ASSERT
```

**Don't** gate idle on the `.recalculating` class globally — suspended/hidden outputs can keep it indefinitely (they don't render until shown), and some hide/`removeUI` sequences leave it stuck (rstudio/shiny#4114), so a global `.recalculating === 0` check can hang. Use it only scoped to one visible output: `page.waitForSelector('#plot:not(.recalculating)')`.

**Settling races (important).** `waitForShinyIdle` can return *before* a slow round-trip even starts — the stable window elapses against the pre-action quiet period — so a read taken right after may be stale. Two robust fixes (both in the helper):
- **Asserting a change?** Wait for the change itself, not a fixed settle: `assertOutputChanged(page, '#plot img', action, {attr:'src'})` snapshots, acts, and resolves once the output differs. This is the reliable "did it update?" oracle and immune to render nondeterminism.
- **Need to settle, then read?** Use `actAndSettle(page, action)` — it waits for the server to *become busy* (or an output to enter `.recalculating`) before waiting for idle, closing the race.

## 4. Read errors the browser can't show

The real traceback is in the **server process stdout/stderr** (`shiny.fullstacktrace = TRUE`) — read it there first. With `devmode(TRUE)` the client also shows the error; catch *which* output failed via the `shiny:error` event (`e.name`, `e.error`). By default client errors are sanitized to "An error has occurred"; the real text is server-side.

To go beyond observing — reproducing a server error or asserting on a reactive's value — reach for the headless test layers in **`shiny-testing`** (`testServer` for reactive logic, `shinytest2` for end-to-end), and **`shiny-reactivity`** for diagnosing *why* a reactive did or didn't fire.

## 5. Shiny for Python

The client JS is identical, so the idle-waiting approach (wait on `shiny-busy`) and the `shiny:*` events apply unchanged. Differences: launch with `shiny run --port 7654 --reload app.py`; server errors go to the `shiny run` process output; there is **no `testServer`** — write logic as pure Python functions and unit-test them; E2E uses `pytest` + `shiny.playwright` controllers (`from shiny.playwright import controller`), which wait on Shiny state for you.

## 6. The wall, and how to work with it

You **can** expose chosen reactive values for inspection by opting in: under `shiny.testmode`, `exportTestValues()` (R) registers internals that `shinytest2` reads via `app$get_value(export=)` (Shiny for Python is gaining an equivalent — posit-dev/py-shiny#2270). What there's still **no** API for is reading *arbitrary* reactive state without that opt-in, or getting a machine-readable invalidation trace (not even a `shiny:invalidated` JS event; `shiny:recalculating` lags invalidation). So the most reliable way to inspect server state today is to design for it: put logic in named reactives / pure functions and exercise it headlessly (see *Authoring for legibility* above and **`shiny-testing`**) rather than trying to read it through the browser.

## See also

- **`shiny-reactivity`** — design and debug the reactive graph (reactlog, tracebacks, "why didn't this update").
- **`shiny-testing`** — the headless test layers (`testServer`, `shinytest2`).
- **`shiny-bslib`** — building the UI.

## References

Fetch only for an edge case or to confirm a current API signature:

- [Shiny JS events](https://shiny.posit.co/r/articles/build/js-events/) — full `shiny:*` event list + properties.
- [Shiny for Python: end-to-end testing](https://shiny.posit.co/py/docs/end-to-end-testing.html) — `shiny.playwright` controllers + pytest fixtures.
- [Playwright](https://playwright.dev/docs/intro) · [Playwright MCP](https://github.com/microsoft/playwright-mcp) — driving APIs and the MCP server setup.
