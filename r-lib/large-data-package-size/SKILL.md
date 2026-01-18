---
name: r-lib/large-data-package-size
description: >
  Handling large files and data in R packages: `inst/extdata`, `data/`, and
  package size discipline (especially for CRAN-bound packages).
  Use this skill when you need to:
  (1) Decide whether data/files should ship in the package or be external,
  (2) Store files for examples via `inst/extdata` and locate them with `system.file()`,
  (3) Produce compact internal datasets (`data/*.rda`) via a `data-raw/` workflow,
  (4) Keep source tarballs and documentation within CRAN expectations,
  (5) Implement user-managed caching and optional downloads safely.
---

# Large Data & Package Size Discipline

## When to Use What

| Task                                               | Use                                                            |
| -------------------------------------------------- | -------------------------------------------------------------- |
| Include a file for examples (CSV, template, image) | Put it in `inst/extdata/` and locate with `system.file()`      |
| Ship a small dataset as `.rda`                     | `usethis::use_data()` (created from scripts under `data-raw/`) |
| Keep large derived artifacts out of the tarball    | `.Rbuildignore` and a build script                             |
| Check package size like CRAN sees it               | Build a tarball and inspect sizes (see references)             |
| Provide large datasets without bundling            | Separate data package or optional downloads + caching          |

## The disciplined workflow

1. **Decide what must ship**

- If users need it offline and it’s small → ship it.
- If it’s large or updates often → prefer an external strategy.

2. **Choose the right place**

- `inst/extdata/` for example files that are accessed by path.
- `data/` for internal datasets users load via `data()` (keep small).

3. **Make access portable**

Use:

```r
path <- system.file("extdata", "example.csv", package = "yourpkg")
```

Never assume a working directory or relative paths.

4. **Keep CRAN expectations in mind**

CRAN policy emphasizes “minimum necessary size” and highlights practical size guidance for data and documentation.

5. **When data is large: design the external path intentionally**

- If it’s static and broadly useful → consider a data-only package.
- If it’s user-specific or cache-like → store under `tools::R_user_dir()` (R >= 4.0) and actively manage size.

## References

- [references/deciding-what-ships.md](references/deciding-what-ships.md)
- [references/inst-extdata-patterns.md](references/inst-extdata-patterns.md)
- [references/data-raw-workflow.md](references/data-raw-workflow.md)
- [references/package-size-checklist.md](references/package-size-checklist.md)
- [references/compression-and-rda.md](references/compression-and-rda.md)
- [references/caching-and-user-dirs.md](references/caching-and-user-dirs.md)
- [references/external-data-strategies.md](references/external-data-strategies.md)

## Related skills

- [r-lib/cran-submission](../cran-submission/)
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/)
