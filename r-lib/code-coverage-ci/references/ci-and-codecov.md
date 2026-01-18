# CI coverage and Codecov notes

This reference collects practical notes for running coverage in CI and uploading results to Codecov.

## Preferred approach: use the template

The easiest way to get a well-maintained workflow is:

```r
usethis::use_github_action("test-coverage")
```

This installs a workflow derived from the r-lib/actions examples.

## Why CI coverage is structured differently than local

In CI, covr is commonly run in a way that:

- installs your package into a temporary location
- writes a Cobertura XML file via `covr::to_cobertura()`

This is designed to work well with CI upload steps.

## About `CODECOV_TOKEN`

Codecov upload can fail unless you set a token:

- repository token (per repo), or
- organization token (stored as an org secret, often also named `CODECOV_TOKEN`)

This can matter even for public repositories depending on org settings and the upload approach.

If you see unexplained upload failures, start by adding `CODECOV_TOKEN` as a GitHub Secret.

## Failing vs non-failing uploads

A common pattern is:

- allow failures on PRs without a token
- fail the workflow on push/main if upload fails

The r-lib/actions template uses this approach via `fail_ci_if_error`.

## References

- covr: https://covr.r-lib.org/
- r-lib/actions examples: https://github.com/r-lib/actions/tree/v2/examples
