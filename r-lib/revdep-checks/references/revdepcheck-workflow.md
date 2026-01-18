# revdepcheck workflow

This reference outlines a minimal, repeatable workflow using the revdepcheck package.

## Install

```r
# revdepcheck may not always be available on CRAN.
# This is the installation approach recommended by the revdepcheck docs:
pak::pkg_install("r-lib/revdepcheck")
```

If you don’t use pak, an alternative is:

```r
remotes::install_github("r-lib/revdepcheck")
```

## Run

From your package root:

```r
library(revdepcheck)

revdepcheck::revdep_reset()
revdepcheck::revdep_check(num_workers = 4)
revdepcheck::revdep_report()
```

Notes:

- Revdep checks can take a long time.
- Prefer running on a clean machine/library when possible.
- Keep the release candidate commit stable while you triage.
- If a run fails to complete, running `revdepcheck::revdep_check()` again will typically pick up where it left off.

## Monitor while checks run

Run these in a separate R process to see progress and inspect failures:

```r
revdepcheck::revdep_summary()
revdepcheck::revdep_details(".", "someDownstreamPkg")
```

## Outputs

revdepcheck writes results under `revdep/` (by default), including:

- per-package check logs
- summary tables
- a rendered report (`revdepcheck::revdep_report()` writes `revdep/README.md`, `revdep/problems.md`, and `revdep/failures.md`)

## Status flags (quick mental model)

revdepcheck uses short status flags to highlight what changed. Common ones include:

- `+` no new failures
- `-` new failures
- `i-` install newly fails
- `t-` install/check newly timeouts

See the revdepcheck docs for the full set of flags.
