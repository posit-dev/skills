---
name: r-lib/performance-profiling
description: >
  Profiling and benchmarking R package code to improve runtime and memory use.
  Use this skill when you need to:
  (1) Identify performance bottlenecks with profiling tools,
  (2) Benchmark alternative implementations correctly,
  (3) Reduce allocations and memory pressure,
  (4) Validate improvements and prevent regressions.
  Also use when performance discussions are speculative and you need evidence.
---

# Performance Profiling

## When to Use What

| Task                                | Use                                                                 |
| ----------------------------------- | ------------------------------------------------------------------- |
| Profile interactive code            | `profvis::profvis({ ... })`                                         |
| Profile CPU hotspots (base R)       | `Rprof()` / `summaryRprof()`                                        |
| Profile memory allocations (base R) | `utils::Rprofmem()`                                                 |
| Benchmark alternatives              | `bench::mark()` (or `microbenchmark::microbenchmark()`)             |
| Measure object size                 | `lobstr::obj_size()` (or `utils::object.size()`)                    |
| Confirm correctness while iterating | Add tests (`testthat`)                                              |
| Prevent regressions over time       | A lightweight benchmark + CI gating (only when the signal is clean) |

## The disciplined loop

1. **Write a minimal reproducer** for the slow path.
2. **Profile first** (don’t benchmark guesses).
3. **Change one thing**.
4. **Benchmark** the before/after with realistic inputs.
5. **Add a regression test** when feasible (and rerun `devtools::check()`).

If the problem is memory pressure (OOMs, huge allocations, GC churn), include a memory profiling step before you rewrite code.

## Common pitfalls

- Benchmarking code that includes setup/IO/network (measure the wrong thing).
- Using tiny inputs that don’t reflect real costs.
- Ignoring variability (run multiple iterations).
- “Optimizing” code that’s not on the hot path.
- Improving speed while breaking correctness.
- Measuring a different workload than users actually run.

## References

- [references/profiling-vs-benchmarking.md](references/profiling-vs-benchmarking.md)
- [references/profvis-workflow.md](references/profvis-workflow.md)
- [references/performance-checklist.md](references/performance-checklist.md)
- [references/benchmarking-with-bench.md](references/benchmarking-with-bench.md)
- [references/memory-profiling.md](references/memory-profiling.md)

## External resources

- profvis: https://rstudio.github.io/profvis/
- bench: https://bench.r-lib.org/
