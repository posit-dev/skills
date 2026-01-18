# Workflow 101: RStudio Projects (packages)

## Table of Contents

1. [What a Project Buys You](#what-a-project-buys-you)
2. [How to Set It Up](#how-to-set-it-up)
3. [Working Directory Expectations](#working-directory-expectations)
4. [What to Commit (and Ignore)](#what-to-commit-and-ignore)
5. [Common Pitfalls](#common-pitfalls)
6. [A practical checklist](#a-practical-checklist)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

## What a Project Buys You

RStudio Projects are a reliable way to:

- Anchor your work in the **package root**.
- Avoid “mystery working directory” problems.
- Keep package development tasks predictable across sessions.

In a package workflow, the best default is: **package root = project root**.

Practical benefits for packages:

- RStudio can treat the project as a package, which makes build/test/check
  commands more predictable.
- File navigation and relative paths become stable (especially across restarts).

## How to Set It Up

- Create/open the project in the package directory.
- Keep all package work (code, docs, tests) inside that project.

If you create a package with `usethis::create_package()`, you typically end up in
the right place to treat that directory as your project root.

Practical benefit: you stop fighting file paths and tool defaults.

If you inherit an existing package folder without a project file, it’s usually
fine to create/open an RStudio Project rooted at the package directory.

Recommended defaults:

- One `.Rproj` file at the package root.
- Treat the `.Rproj` as a convenience for humans; the package must still work in
  non-RStudio contexts (CI, command line).

## Working Directory Expectations

The canonical workflow assumes:

- You run interactive code with the package root as working directory.
- Functions/tests/examples do not rely on your personal machine paths.

If you regularly need to `setwd()` during development, that’s usually a smell.

Instead of changing working directory, prefer organizing files so they live under
package-controlled locations (and are included/excluded appropriately during build).

If you must refer to files, prefer package-aware patterns:

- shipped files: `system.file("extdata", "file.csv", package = "yourpkg")`
- tests: `testthat::test_path("fixtures", "file.csv")`
- examples/tests temporary output: `tempdir()`

If you want one “anchor” rule that scales: every interactive session should start
from the package root.

## What to Commit (and Ignore)

Typical git defaults for packages:

- Commit the `.Rproj` file (it’s lightweight and helpful for contributors).
- Ignore `.Rproj.user/` (RStudio’s per-user state).

If you see `.Rproj.user` in git status, add it to `.gitignore`.

Related pages in this skill:

- [workflow101-path-discipline.md](workflow101-path-discipline.md)
- [workflow101-load-all.md](workflow101-load-all.md)

## Common Pitfalls

- **Multiple active projects:** you run code in the wrong package without
  realizing.
- **Hard-coded paths in examples/tests:** they pass locally but fail on CI.
- **Treating the project root as optional:** it’s the foundation for stable
  relative paths and predictable tooling.

More pitfalls that show up in real workflows:

- **Running `library(yourpkg)` out of habit** instead of using `devtools::load_all()`.
- **Editing outside the package root** (e.g. opening a parent folder and then creating
  files that are not part of the package).
- **Keeping lots of global state** in your session and blaming the package for it.

Practical check:

- If you’re unsure “where you are”, confirm you are working in the package root
  before running `devtools::load_all()` / `devtools::document()` / `devtools::check()`.

## A practical checklist

Use this checklist when a workflow feels “mysterious”:

- The active project root is the package root (the folder that contains `DESCRIPTION`).
- You can run `devtools::load_all()` without errors.
- After changing roxygen/imports/exports, you ran `devtools::document()`.
- Before pushing, you ran `devtools::check()`.
- Tests/examples don’t rely on a specific working directory.

If any item is false, fix it before chasing deeper debugging.

If you want a “minimal clean session” practice:

- restart R
- open the package project
- run `devtools::load_all()`
- run `devtools::test()`

## Troubleshooting

### “RStudio says this isn’t a package”

- You opened the wrong folder (not the one containing `DESCRIPTION`).
- You’re in a parent folder that contains multiple projects.

Fix: open the package root as the project.

### “I keep running code in the wrong repo / wrong package”

- You likely have multiple projects open, or you’re switching between repos.

Fix: adopt a habit of starting each session by confirming the working directory
is the package root before running devtools commands.

### “CI fails but it works in RStudio”

Common causes:

- hidden dependency (installed locally, missing in CI)
- reliance on local files outside the package
- reliance on session state (attached packages, options, env vars)

Fix: reproduce with `devtools::check()` and use the `r-lib/r-cmd-check-ci` playbooks.

## References

- R Packages (2e), “Fundamental workflows”: https://r-pkgs.org/workflow101.html
