---
name: r-lib/code-coverage-ci
description: >
  Measuring R package test coverage with covr and integrating coverage checks
  into CI. Use this skill when you need to:
  (1) Run coverage locally and generate reports,
  (2) Interpret uncovered code paths and decide what tests to add,
  (3) Add a GitHub Actions job to compute coverage on pushes/PRs,
  (4) Diagnose coverage job failures (dependencies, system libs, auth).
  Also use when coverage numbers are being used as a target instead of a signal.
---

# Code Coverage and CI

## When to Use What

| Task                            | Use                                                   |
| ------------------------------- | ----------------------------------------------------- |
| Run package tests               | `devtools::test()`                                    |
| Compute coverage locally        | `covr::package_coverage()`                            |
| View an interactive report      | `covr::report()`                                      |
| Find uncovered lines quickly    | `covr::zero_coverage()`                               |
| Add a coverage workflow quickly | `usethis::use_github_action("test-coverage")`         |
| Run coverage in CI              | GitHub Actions job that installs deps and runs `covr` |

## Local workflow (fast)

```r
# install.packages("covr")

cov <- covr::package_coverage()
cov

# Optional: open an HTML report
covr::report(cov)

# Show only uncovered lines (handy for triage)
covr::zero_coverage(cov)
```

Notes:

- Coverage is a _signal_, not a score.
- Coverage changes should be interpreted in terms of behavior: new code paths should usually have tests.
- Don’t fight covr when code is intentionally untestable; use supported exclusion mechanisms.

## CI workflow (practical)

- Prefer the r-lib/actions template installed by `usethis::use_github_action("test-coverage")`.
- Under the hood, the workflow typically either calls `covr::codecov()` directly, or computes coverage with `covr::package_coverage()` and writes a Cobertura XML report via `covr::to_cobertura()`.
- The exact shape can change across r-lib/actions versions; inspect the generated `.github/workflows/test-coverage.yaml` in your repo.
- Uploading to Codecov often works without extra configuration, but in practice you may need a `CODECOV_TOKEN` secret (especially for private repos and some org setups).

If you need general CI and `R CMD check` setup (beyond coverage), use: [r-lib/r-cmd-check-ci](../r-cmd-check-ci/).

See the GitHub Actions reference for a minimal workflow snippet.

## References

- [references/covr-local.md](references/covr-local.md)
- [references/github-actions-coverage.md](references/github-actions-coverage.md)
- [references/coverage-strategy.md](references/coverage-strategy.md)
- [references/exclusions-and-nocov.md](references/exclusions-and-nocov.md)
- [references/ci-and-codecov.md](references/ci-and-codecov.md)

## External resources

- covr: https://covr.r-lib.org/
- r-lib/actions examples (test-coverage): https://github.com/r-lib/actions/tree/v2/examples
