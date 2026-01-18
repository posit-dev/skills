# Local coverage with covr

## Install

```r
install.packages("covr")
```

## Compute coverage

From your package root:

```r
cov <- covr::package_coverage()
print(cov)
```

## Inspect uncovered code

A quick way to explore:

```r
covr::report(cov)
```

If you want a “what is uncovered?” view:

```r
covr::zero_coverage(cov)
```

Notes:

- Coverage is affected by which tests run and what code paths are exercised.
- Snapshot tests and conditional tests may change coverage results.

## Excluding code intentionally

If some code is intentionally untestable (e.g., interactive UI glue, error recovery that’s hard to trigger safely), use supported exclusion mechanisms:

- `.covrignore` to ignore files/directories (globs via `Sys.glob()` rules)
- `# nocov` comments to exclude a line or region

See [exclusions-and-nocov.md](exclusions-and-nocov.md) for details.
