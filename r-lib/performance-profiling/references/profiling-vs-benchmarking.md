# Profiling vs benchmarking

## Profiling answers “where is the time going?”

Use profiling when you don’t know what to change.

- A profiler samples call stacks while code runs.
- Output helps you find hotspots.

## Benchmarking answers “is change A faster than change B?”

Use benchmarking after you have candidate changes.

- Benchmark the smallest unit that reflects the real cost.
- Include enough iterations to smooth noise.

## Practical sequence

1. Profile the real workload.
2. Identify 1–2 hotspots.
3. Implement a small change.
4. Benchmark the exact hotspot path.
5. Repeat.
