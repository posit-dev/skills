# Workflow 101: create a package (naming and location)

## Table of Contents

1. [Create the Package](#create-the-package)
2. [Where to Put It](#where-to-put-it)
3. [Naming: Why It Matters](#naming-why-it-matters)
4. [First-minute Setup](#first-minute-setup)
5. [A practical naming checklist](#a-practical-naming-checklist)
6. [A “first hour” workflow](#a-first-hour-workflow)
7. [Common Pitfalls](#common-pitfalls)
8. [Troubleshooting](#troubleshooting)
9. [References](#references)

## Create the Package

For a modern default setup, create the package with:

```r
usethis::create_package("path/to/pkg")
```

`usethis` scaffolds the baseline package structure and is designed to set you up
for the edit → load → document → check workflow.

## Where to Put It

Choose a location that makes “package root = working directory” natural:

- Prefer a dedicated directory for the package.
- Avoid nesting one package inside another.
- Avoid developing from within a synced/managed directory that causes file locks
  or unusual path behavior.

The most important outcome is that your tools and paths behave consistently
across machines.

Practical decision rules:

- Prefer a short-ish path without spaces or special characters if you frequently
  work across Windows/macOS/Linux or use tooling that shells out.
- Avoid directories with aggressive syncing/locking (some cloud folders can cause
  intermittent file-lock issues during install/check).
- Keep “one repo = one package” as the default. Multi-package repos are possible,
  but they require more discipline.

## Naming: Why It Matters

Package names show up everywhere: the project directory, DESCRIPTION, help topics,
URLs, and often the GitHub repo. Renaming after the fact tends to be expensive.

Choose a name early, then treat it as stable.

Naming decision rule: if you can’t imagine saying it out loud in a code review,
pick a different name.

Practical note: the package name becomes the default repo name when you push to
GitHub. Keeping them aligned reduces confusion.

## First-minute Setup

A minimal “first-minute” sequence:

1. `usethis::create_package()`
2. `usethis::use_git()`
3. Create your first `R/` file with `usethis::use_r("topic")`
4. Start iterating with `devtools::load_all()`

Then, as soon as there is something real to protect and document:

5. Add roxygen docs + run `devtools::document()`.
6. Add tests (see `r-lib/testing-r-packages`).
7. Keep `devtools::check()` clean as you grow features.

Then add README/testing/CI as the package gains substance.

If you plan to collaborate (even with just one other person), add GitHub early.
It’s cheaper to set it up before you have lots of history and branches.

## A practical naming checklist

Use this checklist before you commit to a name:

- valid R package name (letters/numbers, starts with a letter)
- not already taken on CRAN (if public)
- easy to pronounce and type
- not likely to conflict with common objects/functions
- stable enough that you won’t want to rename it in a month

If renaming feels likely, pause: renaming later touches DESCRIPTION, docs, URLs,
badges, pkgdown, and often external references.

## A “first hour” workflow

Once the package exists, get to a minimal working state quickly:

1. Create a small function file:

```r
usethis::use_r("core")
```

2. Write one simple exported function with roxygen.
3. Regenerate docs:

```r
devtools::document()
```

4. Load and test-drive interactively:

```r
devtools::load_all()
your_fun(1)
```

5. Run an early check:

```r
devtools::check()
```

The point is not “finish everything in an hour”. The point is to establish the
loop and ensure the scaffolding behaves on your machine.

Strong “first hour” outcome checklist:

- `devtools::load_all()` works
- `devtools::document()` runs cleanly
- `devtools::check()` has no errors
- one exported function has a minimal help topic + example
- tests run (even if there is only one)

Related pages in this skill:

- [workflow101-rstudio-projects.md](workflow101-rstudio-projects.md)
- [workflow101-path-discipline.md](workflow101-path-discipline.md)
- [workflow101-load-all.md](workflow101-load-all.md)
- [workflow101-check.md](workflow101-check.md)

## Common Pitfalls

- **Creating a package in a messy working directory:** it becomes hard to reason
  about paths and project roots.
- **Delaying Git:** you lose history and make review harder.
- **Treating interactive success as enough:** use `devtools::check()` as the
  recurring quality bar.

- **Choosing a name you’ll want to change later:** renaming touches DESCRIPTION,
  pkgdown, badges, URLs, and often external references.
- **Starting without a clear repo boundary:** mixing package code with analysis
  files leads to path + build problems unless you’re disciplined with ignores.

## Troubleshooting

### “It created the package but tools don’t recognize it”

You are probably not in the package root (the directory containing `DESCRIPTION`).

Fix:

- Open the package directory as your project.
- Then run `devtools::load_all()`.

### “Paths work locally but fail on CI”

This is usually a path discipline issue.

Fix: follow [workflow101-path-discipline.md](workflow101-path-discipline.md).

## References

- R Packages (2e), “Fundamental workflows”: https://r-pkgs.org/workflow101.html
- usethis: `create_package()`: https://usethis.r-lib.org/reference/create_package.html
