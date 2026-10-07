# Model Explorer (deliberately slow under multi-user load)

A modeling app used as the *before* fixture for shiny-optimize evals focused
on blocking operations and multi-user capacity. Planted problems:

1. `Simulated "model fit" (`Sys.sleep(4)`) runs inline inside an
   `eventReactive` — blocks the whole R process for every session
2. Data read with `read.csv()` inside `server()` — once per session
3. Three outputs each independently re-derive expensive summaries from the fit
4. No caching anywhere
5. No `req()` — outputs attempt to compute before "Fit model" is clicked

Regenerate data: `Rscript generate-data.R`.
