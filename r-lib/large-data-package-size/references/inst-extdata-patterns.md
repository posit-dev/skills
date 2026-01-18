# `inst/extdata` patterns

`inst/extdata/` is the right place for example files that users (or your examples/tests) access by file path.

## How it works

Everything under `inst/` is installed with the package.

At runtime, locate files using `system.file()`:

```r
path <- system.file("extdata", "example.csv", package = "yourpkg")
stopifnot(nzchar(path))

x <- utils::read.csv(path)
```

## Common good uses

- small CSV/TSV files for examples
- templates (e.g., YAML, LaTeX)
- small images used in vignettes

## Common mistakes

- assuming `inst/extdata` exists relative to the current working directory
- using `setwd()` to “find” files
- shipping very large files

## Check/CI considerations

- Examples should run quickly and not require network access.
- If a file is optional, make examples conditional.

## Related

- [package-size-checklist.md](package-size-checklist.md)
