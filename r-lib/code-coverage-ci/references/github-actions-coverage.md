# GitHub Actions coverage job (practical)

This reference shows a practical GitHub Actions workflow for computing coverage with covr and (optionally) uploading it to Codecov.

In many cases, the best starting point is:

```r
usethis::use_github_action("test-coverage")
```

## Example workflow

Create `.github/workflows/test-coverage.yaml`:

```yaml
name: test-coverage

on:
  push:
    branches: [main, master]
  pull_request:

permissions: read-all

jobs:
  test-coverage:
    runs-on: ubuntu-latest
    env:
      GITHUB_PAT: ${{ secrets.GITHUB_TOKEN }}

    steps:
      - uses: actions/checkout@v4

      - uses: r-lib/actions/setup-r@v2
        with:
          use-public-rspm: true

      - uses: r-lib/actions/setup-r-dependencies@v2
        with:
          extra-packages: any::covr, any::xml2
          needs: coverage

      - name: Test coverage
        run: |
          cov <- covr::package_coverage(
            quiet = FALSE,
            clean = FALSE,
            install_path = file.path(
              normalizePath(Sys.getenv("RUNNER_TEMP"), winslash = "/"),
              "package"
            )
          )
          covr::to_cobertura(cov)
        shell: Rscript {0}

      - uses: codecov/codecov-action@v5
        with:
          fail_ci_if_error: ${{ github.event_name != 'pull_request' || secrets.CODECOV_TOKEN }}
          files: ./cobertura.xml
          plugins: noop
          disable_search: true
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Notes and common gotchas

- If your package needs system dependencies, install them before `setup-r-dependencies`.
- Codecov upload _often_ works without a token for public repos, but in practice it can fail unless `CODECOV_TOKEN` is set.
- The workflow above generates a Cobertura file (`cobertura.xml`) via `covr::to_cobertura()`.

For the most up-to-date template, see the r-lib/actions examples.
