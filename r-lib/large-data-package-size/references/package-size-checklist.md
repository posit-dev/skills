# Package size checklist

CRAN policy emphasizes packages should be of the minimum necessary size.

## What to check

- Source tarball size (`.tar.gz`)
- Installed size (especially `inst/` payloads)
- Documentation size (PDFs and vignettes)

## Common size offenders

- large PDFs under `inst/doc`
- large raw data files under `inst/extdata`
- generated outputs accidentally committed (cache, rendered artifacts)

## Practical checklist

1. Build a tarball locally.
2. Inspect what dominates size.
3. Compress or reduce what you ship.
4. Move large payloads to an external strategy.

## CRAN guidance to keep in mind

- As a general rule, neither data nor documentation should exceed ~5MB.
- Source tarballs should preferably not exceed ~10MB.
- Consider a separate data-only package for large data.

(These rules are described in the CRAN repository policy; treat them as practical expectations.)

## References

- CRAN policy (package size guidance): https://cran.r-project.org/web/packages/policies.html
