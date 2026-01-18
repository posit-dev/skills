# Memory profiling and allocations

Performance problems are often memory problems:

- large allocations
- repeated allocation in tight loops
- excessive garbage collection (GC)

This reference focuses on tools that help you see allocation behavior.

## Base R: Rprofmem

`utils::Rprofmem()` records memory allocations above a threshold.

Example:

```r
# Record allocations > 1MB to a file
utils::Rprofmem("Rprofmem.out", threshold = 1e6)

# Run a representative workload
result <- my_fun(x)

# Stop profiling
utils::Rprofmem(NULL)

# Inspect the results
readLines("Rprofmem.out", n = 50)
```

Tips:

- Start with a higher threshold (e.g., 1MB) to reduce noise.
- Then lower the threshold once you know where the big allocations occur.

## Bench: allocations + GC

If you use `bench::mark()`, you get allocation and GC metrics alongside timing.

This is often the easiest way to validate that an “optimization” didn’t just move the cost into memory churn.

## Object size helpers

- `lobstr::obj_size(x)` gives a more accurate estimate of memory usage than `utils::object.size()` in many cases.

## References

- Writing memory-friendly code (general): focus on reducing allocations and copies.
- bench: https://bench.r-lib.org/
