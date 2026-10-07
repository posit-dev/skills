# Grader notes: planted problems in the eval fixture apps

**For graders and reviewers only — never place this file (or its contents)
inside `apps/` or in any directory given to the agent under test.** Reads
`RUNNING.md` in this directory for the isolation protocol that keeps it that
way.

## `apps/sales-dashboard` (eval 0: dashboard-broad-slowness)

A regional sales dashboard, intentionally full of common performance
problems; do not "fix" the fixture itself — eval runs are supposed to find
and fix them.

1. `sales.csv` read with `read.csv()` **inside `server()`** — once per session
2. Expensive prep (date parsing) also per session
3. `renderUI()` for the city filter instead of `updateSelectInput()`
4. Two outputs each re-filter the full data independently (duplicate work)
5. No `req()` — outputs compute on `NULL`/empty selections at startup
6. Six heavy outputs all visible on the landing page (no tabs)
7. Year slider feeds expensive chains directly (no debounce)
8. Simulated slow API (`Sys.sleep(1.5)`) inline in a reactive — uncached
9. `DT::renderDT(..., server = FALSE)` with the full detail table (client-side
   processing; note: in DT ≥ 0.34 the `server` argument lives on `renderDT()`,
   not `datatable()`)
10. 30k-point scatter rendered raw, no aggregation
11. No caching anywhere

## `apps/model-explorer` (eval 1: multiuser-blocking-freeze)

A modeling app, intentionally slow under multi-user load.

1. Simulated "model fit" (`Sys.sleep(4)`) runs inline inside an
   `eventReactive` — blocks the whole R process for every session
2. Data read with `read.csv()` inside `server()` — once per session
3. Three outputs each independently re-derive expensive summaries from the fit
4. No caching anywhere
5. No `req()` — outputs attempt to compute before "Fit model" is clicked
