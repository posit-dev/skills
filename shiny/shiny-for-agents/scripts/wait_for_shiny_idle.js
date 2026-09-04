// wait_for_shiny_idle.js — wait on Shiny's own settle signals; NEVER sleep.
//
// Shiny adds class `shiny-busy` to <html> while the server is working and removes
// it when idle; each recalculating output carries class `.recalculating` until it
// re-renders. We wait until BOTH are clear and have *stayed* clear for `stableMs`,
// which absorbs (a) the race where we check before `shiny-busy` is added, and
// (b) multi-step reactive cascades.
//
// Works with any Playwright `page` (Playwright MCP, agent-browser, raw Playwright,
// or Shiny for Python — same client JS). For the Python `sync_api`, call
// page.wait_for_function(...) with the same body.

/**
 * Wait for the app to connect to the Shiny server.
 * @param {import('playwright').Page} page
 */
async function waitForShinyConnected(page, { timeout = 30000 } = {}) {
  await page.waitForFunction(
    () =>
      typeof window.Shiny !== "undefined" &&
      window.Shiny.shinyapp &&
      typeof window.Shiny.shinyapp.isConnected === "function" &&
      window.Shiny.shinyapp.isConnected(),
    undefined,
    { timeout }
  );
}

/**
 * Wait until Shiny has been idle for `stableMs` continuous milliseconds.
 *
 * The GLOBAL idle signal is the `shiny-busy` class on <html> (added while the
 * server is working, removed when idle) — this is what shinytest2's
 * wait_for_idle() keys on. Do NOT gate global idle on the `.recalculating`
 * class: outputs on hidden tabs / suspended outputs keep `.recalculating`
 * indefinitely (they never render until shown — see rstudio/shiny#4114), so a
 * global `.recalculating === 0` check can hang forever.
 *
 * To wait for a SPECIFIC output to finish, pass `selector` — we additionally
 * require that element to drop its `.recalculating` class. Scope it to a
 * visible output, never use it as a global gate.
 *
 * CAVEAT: `window.__shinyLastBusy` persists on the page across calls and is
 * never reset, so a bare second call right after an action can read a stale
 * timestamp and report idle before the new round-trip even starts. For the
 * "act, then read" pattern use `actAndSettle` (it waits for busy to appear
 * first); for "assert it changed" use `assertOutputChanged`.
 *
 * @param {import('playwright').Page} page
 * @param {{ stableMs?: number, timeout?: number, selector?: string }} [opts]
 */
async function waitForShinyIdle(page, { stableMs = 250, timeout = 30000, selector = null } = {}) {
  await page.waitForFunction(
    ({ stableMs, selector }) => {
      const serverBusy = document.documentElement.classList.contains("shiny-busy");
      // Only consider .recalculating for an explicitly-scoped, visible output.
      const targetBusy =
        selector && document.querySelector(selector)
          ? document.querySelector(selector).classList.contains("recalculating")
          : false;
      if (serverBusy || targetBusy) {
        window.__shinyLastBusy = Date.now();
        return false;
      }
      if (window.__shinyLastBusy === undefined) return true; // never went busy => already idle
      return Date.now() - window.__shinyLastBusy >= stableMs; // idle long enough to be settled
    },
    { stableMs, selector },
    { polling: 50, timeout }
  );
}

/**
 * Install error/console recorders right after connect, so server-propagated
 * output errors (otherwise invisible to the browser) can be read after an action.
 * @param {import('playwright').Page} page
 */
async function installShinyErrorRecorder(page) {
  await page.evaluate(() => {
    if (window.__shinyErrors) return; // idempotent
    window.__shinyErrors = [];
    // jQuery is always present in a Shiny page.
    $(document).on("shiny:error", (e) =>
      window.__shinyErrors.push({
        output: e.name,
        message: e.error && e.error.message,
      })
    );
  });
}

/** Read any errors captured since installShinyErrorRecorder(). */
async function getShinyErrors(page) {
  return page.evaluate(() => window.__shinyErrors || []);
}

/**
 * Act, then settle — robust against the premature-idle race.
 *
 * `waitForShinyIdle` alone can return BEFORE a slow round-trip even starts (the
 * stable window elapses against the pre-action quiet period), so a read taken
 * right after can be stale. This first waits for the server to actually BECOME
 * busy (or any output to enter `.recalculating`), then waits for idle. If no
 * work starts within `busyTimeout`, that's fine — the action triggered nothing.
 * @param {import('playwright').Page} page
 * @param {() => Promise<void>} action
 */
async function actAndSettle(page, action, { busyTimeout = 4000, stableMs = 400, timeout = 30000 } = {}) {
  await action();
  await page
    .waitForFunction(
      () =>
        document.documentElement.classList.contains("shiny-busy") ||
        document.querySelectorAll(".recalculating").length > 0,
      undefined,
      { timeout: busyTimeout }
    )
    .catch(() => {}); // no work started — not an error
  await waitForShinyIdle(page, { stableMs, timeout });
}

/**
 * When you assert that an action CHANGES an output, wait for the change itself —
 * don't settle-then-compare (that races the render). Snapshots the output's
 * text/`src`, runs `action`, and resolves true once it differs (false on timeout).
 * The most reliable "did this output update?" oracle. `attr` is "src" for plots
 * (an <img>), omit for text outputs.
 * @param {import('playwright').Page} page
 * @param {string} selector  e.g. "#myplot img" or "#summary"
 * @param {() => Promise<void>} action
 */
async function assertOutputChanged(page, selector, action, { attr = null, timeout = 15000 } = {}) {
  await page.evaluate(
    ([sel, attr]) => {
      const el = document.querySelector(sel);
      window.__before = el ? (attr ? el.getAttribute(attr) : el.textContent) : null;
    },
    [selector, attr]
  );
  await action();
  return page
    .waitForFunction(
      ([sel, attr]) => {
        const el = document.querySelector(sel);
        const now = el ? (attr ? el.getAttribute(attr) : el.textContent) : null;
        return now != null && now !== window.__before;
      },
      [selector, attr],
      { polling: 100, timeout }
    )
    .then(() => true)
    .catch(() => false);
}

// --- Typical usage -----------------------------------------------------------
// await page.goto("http://127.0.0.1:7654");
// await waitForShinyConnected(page);
// await installShinyErrorRecorder(page);
// await page.fill("#country_filter", "Canada");   // ACT
// await waitForShinyIdle(page);                    // SETTLE
// const txt = await page.textContent("#summary");  // ASSERT
// console.log(await getShinyErrors(page));          // any server-side output errors

module.exports = {
  waitForShinyConnected,
  waitForShinyIdle,
  actAndSettle,
  assertOutputChanged,
  installShinyErrorRecorder,
  getShinyErrors,
};
