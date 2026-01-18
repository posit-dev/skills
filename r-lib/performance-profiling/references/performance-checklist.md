# Performance checklist

Use this checklist to keep performance work evidence-driven.

## Reproducibility

- Can you reproduce the slowdown locally?
- Do you have a stable input that triggers the problem?

If the report is “sometimes slow”, try to capture:

- input sizes
- platform (OS/R version)
- whether caches or warm starts matter

## Measurement

- Profile first.
- Benchmark after.
- Measure with realistic inputs.

If memory is suspected:

- measure allocations / memory growth
- confirm whether GC is dominating runtime

## Correctness and maintenance

- Add a regression test when feasible.
- Keep changes simple; avoid cleverness unless the benefit is large and proven.
- Re-run `devtools::check()` and (if relevant) revdeps.

Finally, sanity check the “win”:

- does it speed up the end-user workload, or just a micro-benchmark?
