# Grader notes: planted problems in the eval fixture apps

**For graders and reviewers only — never place this file (or its contents)
inside `apps/` or in any directory given to the agent under test.** Read
`RUNNING.md` in this directory for the isolation protocol that keeps it that
way.

## `apps/sales-dashboard` (evals 0 and 2)

A regional sales dashboard (Shiny Express), intentionally full of common
performance problems. Do not "fix" the fixture itself — eval runs are
supposed to find and fix them.

1. `sales.csv` (200k rows) read with `pd.read_csv()` at the **top level of the
   Express `app.py`** — Express runs that code once per session
2. Date parsing (`month`, `year` columns) also once per session
3. `@render.ui` for the city filter instead of `ui.update_select()`
4. Every output re-filters the full data independently (duplicate work)
5. No guard for an empty product selection — clearing the selectize makes
   outputs error or do pointless work
6. Seven heavy outputs all visible on the landing page (no tabs)
7. Year slider feeds expensive chains directly (no debounce)
8. Simulated slow API (`time.sleep(1.5)`) in a `@reactive.calc` that reads no
   reactive values — runs once per session, and since the sleep is sync, it
   stalls every session in the process while it runs
9. `@render.table` on the full filtered frame — ~19 MB of HTML from the
   pandas Styler
10. 200k-point scatter rendered raw, no aggregation or sampling
11. No caching anywhere

Known quirk: matplotlib can print a one-off `OverflowError: Exceeded cell
block limit in Agg` for `revenue_plot` while the page is first laid out. The
output then renders correctly. Don't count it against a run unless an output
stays in an error state.

## `apps/model-explorer` (eval 1)

A modeling app (Shiny Core), intentionally slow under multi-user load.

1. Simulated "model fit" (`time.sleep(4)`) runs inline in a
   `@reactive.calc` + `@reactive.event(input.fit)` — blocks the event loop
   for every session, on every shiny version
2. Data read with `pd.read_csv()` inside `server()` — once per session
3. Three outputs each rebuild the design matrix and recompute predictions
   from the fit
4. No caching anywhere
5. The existing `ui.input_task_button` is not bound to anything, so it resets
   as soon as the reactive flush ends

## `apps/ops-monitor` (eval 3)

An ops dashboard (Shiny Core) whose behavior differs between shiny 1.8.0 and
1.9.0, so the right diagnosis depends on the installed version.

1. `@reactive.effect` + `@reactive.event(input.refresh)` that does
   `await fetch_incident_report(...)` (a 5 s `asyncio.sleep`). The session
   stays busy until it finishes: no input changes, no `invalidate_later`
   ticks, no outputs.
   - shiny >= 1.9.0: only the session that clicked freezes; other sessions
     keep ticking.
   - shiny < 1.9.0: reactive functions run one at a time across the process,
     so every session freezes.
   The fix on both versions is `@reactive.extended_task`.
2. A per-session background task feeds `latest_volume` with
   `async with reactive.lock(): ...set(...); await reactive.flush()`.
   - shiny >= 1.9.0: `reactive.lock()` does nothing and emits a
     `ShinyDeprecationWarning`; `.set()` alone schedules the dependents.
   - shiny < 1.9.0: the lock + flush is the documented way to do this and is
     correct.

Measured on the fixtures (Playwright, two tabs): during a refresh, the
clicking tab's clock froze on both versions; the other tab's clock kept
ticking on 1.9.0 and froze on 1.8.0.
