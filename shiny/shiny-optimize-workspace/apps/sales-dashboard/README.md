# Sales Dashboard (deliberately slow)

A regional sales dashboard used as the *before* fixture for shiny-optimize
evals. It is intentionally full of common performance problems; do not "fix"
the fixture itself — eval runs are supposed to find and fix them.

Regenerate the data with: `Rscript generate-data.R` (deterministic seed).

Known planted problems (for graders/reviewers, not for the agent under test):

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
