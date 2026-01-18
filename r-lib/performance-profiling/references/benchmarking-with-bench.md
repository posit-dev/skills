# Benchmarking with bench

This reference documents a practical approach to benchmarking performance changes in R code.

## Why bench

`bench::mark()` is a good default because it:

- measures time with high precision
- tracks memory allocations and garbage collections
- checks that expressions return equivalent results by default (so you don’t benchmark different behavior)

## A practical benchmarking template

```r
# install.packages("bench")

library(bench)

# Ensure expressions are equivalent, then compare performance.
res <- bench::mark(
  old = old_impl(x),
  new = new_impl(x),
  check = TRUE,
  relative = TRUE
)

res
```

Notes:

- Use a representative `x` (size and shape similar to real usage).
- If you need to benchmark across multiple input sizes, use `bench::press()`.

## Common benchmarking mistakes

- Benchmarking setup work (file IO, downloads, printing) instead of the hot path.
- Using unrealistically small inputs.
- Ignoring garbage collection and allocations (a “faster” method that allocates heavily may be worse in real workloads).

## How to interpret results

- Look at both time (e.g., median) and memory allocation.
- If one method triggers lots of GC and the other doesn’t, the “real-world” winner might depend on your workload.

## References

- bench: https://bench.r-lib.org/
