# pkgdown troubleshooting

This reference is a checklist for diagnosing pkgdown build/deploy problems.

## 1) Reproduce locally first

Run a local build:

```r
pkgdown::build_site()
```

If local build fails, fix that before chasing CI.

## 2) Docs and missing topics

Symptoms:

- functions missing from reference
- broken links to help topics

Checks:

- run `devtools::document()` and rebuild
- confirm exports (NAMESPACE) match what you expect
- confirm `_pkgdown.yml` reference groups list valid topics

## 3) CI builds fail but local builds succeed

Common causes:

- undeclared dependencies used in examples
- vignettes that require suggested packages not installed in CI
- system dependencies missing on CI runner

Mitigations:

- ensure dependencies are declared correctly in DESCRIPTION
- ensure optional dependencies are used conditionally
- install required system libs before `setup-r-dependencies`

## 4) Deployment succeeds but Pages site is blank

Common cause:

- GitHub Pages is not configured to publish from the branch/folder your workflow deploys.

If your workflow deploys `docs/` to `gh-pages`, set GitHub Pages to:

- branch: `gh-pages`
- folder: `/`

## 5) CI-friendly build function

The r-lib/actions `pkgdown` workflow uses:

```r
pkgdown::build_site_github_pages(new_process = FALSE, install = FALSE)
```

If you want to debug CI parity locally, run this in a clean session.

## References

- pkgdown: https://pkgdown.r-lib.org/
- r-lib/actions pkgdown example: https://github.com/r-lib/actions/tree/v2/examples
