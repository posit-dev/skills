# Building and previewing pkgdown locally

Local builds are the fastest way to iterate on `_pkgdown.yml`, navigation, and reference grouping.

## Typical workflow

1. Update docs:

```r
devtools::document()
```

2. Build the site:

```r
pkgdown::build_site()
```

3. Preview:

```r
pkgdown::preview_site()
```

## Faster iterations

- If you are only working on reference grouping, try `pkgdown::build_reference()`.
- If you are only working on articles, try `pkgdown::build_articles()`.

## Common “why is this missing?” checks

- Is the function exported (in `NAMESPACE`)?
- Did you re-run `devtools::document()` after editing roxygen?
- Is the vignette in the right place and declared correctly?

## References

- pkgdown: https://pkgdown.r-lib.org/
