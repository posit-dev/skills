# profvis workflow

`profvis` provides a visual profiler that’s often the fastest way to understand R performance.

## Install

```r
install.packages("profvis")
```

## Basic usage

```r
profvis::profvis({
  # code you want to profile
  result <- my_fun(x)
})
```

For package code, it’s often helpful to:

1. create a minimal repro function (or a script) that sets up realistic inputs
2. profile only the “hot path” (not data loading, printing, or plotting)

## Tips

- Profile a representative input size.
- Remove one-time setup costs from the profiled block if they’re not the target.
- If the code calls C/C++, ensure you’re attributing time correctly (R vs native).

Practical workflow:

1. Start with the slowest user-facing function.
2. Profile once and identify 1–2 hotspots.
3. Make one change.
4. Re-profile to confirm the hotspot moved (or disappeared).

If you are going to benchmark, do it _after_ profiling so you know what to measure.
