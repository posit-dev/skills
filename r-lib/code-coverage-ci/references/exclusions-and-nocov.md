# Exclusions and `# nocov`

Sometimes code is intentionally hard to test (e.g., interactive glue, defensive fallbacks, platform-specific branches). covr supports several exclusion mechanisms.

Use exclusions sparingly: prefer tests for important behavior.

## 1) `.covrignore`

A `.covrignore` file at the package root can exclude files/directories from coverage.

- Lines are interpreted as file globs (using `Sys.glob()` rules).
- If you don’t want to distribute `.covrignore`, add it to `.RBuildignore`.

You can also set an alternate location via:

- env var `COVR_COVRIGNORE`, or
- option `covr.covrignore`

## 2) Exclusion comments

Exclude a single line:

```r
f1 <- function(x) {
  x + 1 # nocov
}
```

Exclude a range:

```r
f2 <- function(x) { # nocov start
  x + 2
} # nocov end
```

Notes:

- covr’s exclusion comments also apply in `src/`.
- For C/C++ code, a typical pattern is `// # nocov`.

## 3) package_coverage() exclusion arguments

covr also supports exclusion arguments like:

- `function_exclusions`
- `line_exclusions`

These can be useful when you want exclusions without inline comments.

## References

- covr exclusions docs: https://covr.r-lib.org/
