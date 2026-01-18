# Troubleshooting compiled build failures

This is a pragmatic checklist for “it builds on my machine but fails on CI/CRAN”.

## 1) Reproduce in a clean environment

- Restart R.
- Run `devtools::check()`.
- If possible, run on another OS (CI is usually the fastest path).

## 2) Classify the failure

### Compile-time

- Missing headers
- C++ standard mismatch
- Warnings treated as errors (some toolchains)

### Link-time

- Missing libraries
- Wrong order of `PKG_LIBS`
- ABI mismatch

### Load-time

- Missing runtime dependency
- Symbol not found due to platform differences

## 3) Reduce

- Reduce to a small example in `src/`.
- Temporarily remove optional features to isolate the break.

## 4) Fix with portability in mind

- Don’t hard-code absolute paths.
- Prefer `LinkingTo` when the dependency can be shipped as an R package.
- Keep platform-specific logic explicit and small.

## 5) Re-run the quality gates

- `devtools::check()`
- CI across at least Linux + one of Windows/macOS.

## References

- [toolchains-and-ci.md](toolchains-and-ci.md)
- [src-layout-and-makevars.md](src-layout-and-makevars.md)
