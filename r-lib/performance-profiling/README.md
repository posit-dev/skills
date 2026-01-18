# Performance Profiling

A workflow playbook for finding and fixing performance problems in R packages: profiling, benchmarking, and memory.

## Overview

This skill emphasizes a disciplined sequence:

1. Reproduce the performance issue.
2. Profile to find where time is spent.
3. Make a minimal change.
4. Benchmark to confirm the change helped.
5. Re-run `R CMD check` (performance fixes often touch internals).

## When This Skill Activates

Use this skill when you need to:

- speed up an R package function
- reduce memory usage or allocations
- choose between alternative implementations based on evidence
- interpret profiling output (flame graphs, call stacks)
- avoid common benchmarking mistakes

## File Organization

- [SKILL.md](SKILL.md) - Task mapping + core workflow
- [references/](references/) - Profiling vs benchmarking, profvis workflow, benchmarking patterns, memory profiling, and a checklist

```
performance-profiling/
├── README.md
├── SKILL.md
└── references/
    ├── benchmarking-with-bench.md
    ├── profiling-vs-benchmarking.md
    ├── profvis-workflow.md
    ├── performance-checklist.md
    └── memory-profiling.md
```

## Related skills

- [r-lib/testing-r-packages](../testing-r-packages/) - Regression tests to protect performance fixes
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - Confirm fixes behave under check/CI
