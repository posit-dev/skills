# Workflow 101: path discipline and working directory

## Table of Contents

1. [Why Path Discipline Matters](#why-path-discipline-matters)
2. [Working Directory Rule of Thumb](#working-directory-rule-of-thumb)
3. [Patterns That Scale](#patterns-that-scale)
4. [Common Pitfalls](#common-pitfalls)
5. [Cookbook (common file/path jobs)](#cookbook-common-filepath-jobs)
6. [Troubleshooting](#troubleshooting)
7. [References](#references)

## Why Path Discipline Matters

Packages are intended to run on other machines (and in CI). If your development
workflow relies on your personal working directory layout, `R CMD check` can
fail in ways that are hard to debug.

You want a setup where your package works regardless of where it is cloned.

## Working Directory Rule of Thumb

- During development, treat the **package root** as the default working directory.
- Avoid frequent `setwd()` calls.

This aligns with the standard workflow and makes relative paths predictable.

## Patterns That Scale

Good defaults that work locally, in CI, and on other machines:

- Keep any files the package needs inside the package (often under `inst/`).
- Prefer temporary files/directories for tests and examples.
- Assume CI runs from a clean checkout and a clean R session.

Useful boundary concepts:

- **What ships** is controlled by `R CMD build` and `.Rbuildignore`.
- **What is committed** is controlled by git and `.gitignore`.
- Your package code should only rely on files that ship (or that it creates at runtime).

Concrete patterns:

- Read package-shipped files via `system.file()`:

```r
path <- system.file("extdata", "example.csv", package = "yourpkg")
read.csv(path)
```

- Create ephemeral files in examples/tests under `tempdir()`:

```r
path <- file.path(tempdir(), "example.csv")
write.csv(data.frame(x = 1), path, row.names = FALSE)
```

- When you temporarily change process state, restore it:

```r
old <- getwd()
on.exit(setwd(old), add = TRUE)
setwd(tempdir())
```

If you use `withr`, prefer local “scope” helpers for state changes:

- `withr::local_dir()`
- `withr::local_options()`
- `withr::local_envvar()`

If you need to exclude dev-only files from the package build, add them to
`.Rbuildignore` (often via `usethis::use_build_ignore()`).

Decision rules for file placement:

- If users need the file at runtime → ship it under `inst/`.
- If only tests need it → keep it under `tests/testthat/fixtures/`.
- If only you need it (scratch data, notes) → keep it out of the package build via
  `.Rbuildignore` (and usually out of git via `.gitignore`).

## Cookbook (common file/path jobs)

### Ship a small file with the package

Put it under `inst/extdata/`.

Keep files small and stable. If the file is large or frequently changing, consider:

- generating it during tests
- downloading it in examples/vignettes (but only if check-safe)
- moving it to an article that doesn’t ship

Then read it with:

```r
path <- system.file("extdata", "example.csv", package = "yourpkg")
stopifnot(nzchar(path))
```

### Use a static file in tests

Put it under `tests/testthat/fixtures/` and access it with:

```r
path <- testthat::test_path("fixtures", "example.csv")
```

### Write temporary output

Write under `tempdir()` and clean up if needed:

```r
path <- file.path(tempdir(), "example.csv")
on.exit(unlink(path), add = TRUE)
```

### Exclude a dev-only file from the package bundle

Add it to `.Rbuildignore` (often via usethis):

```r
usethis::use_build_ignore("^scratch/")
```

Remember: `.Rbuildignore` is a _build_ boundary, not a _git_ boundary.

## Troubleshooting

### “cannot open file …” on CI

Common cause: the file is outside the package or not included in the build.

Fix:

- If the file should ship, move it under `inst/` and use `system.file()`.
- If it’s test-only, move it under `tests/testthat/fixtures/` and use `test_path()`.
- If it’s dev-only, don’t rely on it in code/tests that run in check.

### “Works interactively, fails in examples/tests”

Typical causes:

- working directory assumptions
- reliance on attached packages
- reliance on user-level caches or environment variables

Fix:

- make paths relative to shipped files (`system.file()`)
- use explicit `pkg::fun()` calls
- use `tempdir()` (and clean up) for generated files

### “It works when I run a script from my project”

That’s a smell: packages are not analysis projects.

Fix: remove reliance on project-root helpers and use package-aware paths.

For more advanced patterns (fixtures, temp dirs, snapshot file locations), see
`r-lib/testing-r-packages`.

## Common Pitfalls

- **Absolute paths** in code/tests/examples.
- **Depending on the interactive session state** (working dir, options, env vars).
- **Reading files that aren’t in the package**.

One strong smell: relying on project helpers intended for analysis projects
(e.g. `here::here()`). In packages, prefer package-aware paths and
`system.file()`.

Other strong smells:

- `setwd()` in package code
- reading `~/Downloads/...` or other user-specific locations
- writing into the package source tree during examples/tests

Related pages in this skill:

- [workflow101-rstudio-projects.md](workflow101-rstudio-projects.md)
- [workflow101-load-all.md](workflow101-load-all.md)

## References

- R Packages (2e), “Fundamental workflows”: https://r-pkgs.org/workflow101.html
