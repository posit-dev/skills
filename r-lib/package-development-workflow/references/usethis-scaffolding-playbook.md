# usethis scaffolding playbook (`use_*()`)

This page is a practical guide to using `usethis` as your “project scaffolding
tool”: it helps you create and modify files consistently so you can focus on
the daily dev loop (`load_all()` / `document()` / `test()` / `check()`).

## Table of Contents

1. [How to Think About `use_*()`](#how-to-think-about-use_)
2. [One-time Setup (Usually)](#one-time-setup-usually)
3. [Repeatable Helpers](#repeatable-helpers)
4. [A Minimal “New Package” Sequence](#a-minimal-new-package-sequence)
5. [Decision Rules (When to Use What)](#decision-rules-when-to-use-what)
6. [A practical mapping (task → helper)](#a-practical-mapping-task--helper)
7. [Common Pitfalls](#common-pitfalls)
8. [Troubleshooting](#troubleshooting)
9. [References](#references)

## How to Think About `use_*()`

`usethis` exists to make “the right thing” easy and consistent. In practice,
most `use_*()` functions:

- create or modify files in the package
- use sensible defaults aligned with modern package practice
- are designed to be **idempotent** (re-running is usually safe)

The key mental split:

- **Setup helpers**: run once per package (or rarely)
- **Workflow helpers**: run repeatedly during development

## One-time Setup (Usually)

Common early calls (not exhaustive):

- `usethis::create_package()` (start the package)
- `usethis::use_git()` (version control)
- `usethis::use_readme_rmd()` (README source)
- `usethis::use_license_*()` (licensing)
- `usethis::use_github()` (collaboration / remote)
- `usethis::use_github_action()` (CI workflow scaffolding)

The exact set depends on whether the package is internal vs public/CRAN-bound,
but the intent is the same: establish repeatable structure early.

Practical advice: keep your “setup” commits boring and reviewable.
If you scaffold many things at once, do it in small, themed commits (e.g.
“initial package skeleton”, “add testthat”, “add CI”).

## Repeatable Helpers

These are often used repeatedly as the package evolves:

- `usethis::use_r("topic")` (create new `R/` files)
- `usethis::use_testthat()` and `usethis::use_test("topic")` (test scaffolding)
- `usethis::use_vignette("topic")` (new vignette)

Many setup-like helpers are also safe to re-run when you want to restore default
structure (e.g., updating ignore files) — `usethis` typically detects existing
state.

That said, there are a few helpers where re-running changes semantics (e.g.
renaming the package or changing licensing). Treat those as “deliberate changes”.

## A Minimal “New Package” Sequence

This is a practical starting point for most packages:

1. `usethis::create_package()`
2. `usethis::use_git()`
3. `usethis::use_readme_rmd()`
4. Add initial code under `R/` (create files via `usethis::use_r()`)
5. Iterate with `devtools::load_all()`
6. Keep docs current with `devtools::document()`
7. Keep checks clean with `devtools::check()`

Then add GitHub + CI when collaboration begins.

Related pages in this skill:

- [workflow101-create-package.md](workflow101-create-package.md)
- [workflow101-load-all.md](workflow101-load-all.md)
- [workflow101-check.md](workflow101-check.md)

Related skills:

- `r-lib/documentation-roxygen2-pkgdown` for roxygen + pkgdown workflows.
- `r-lib/r-cmd-check-ci` for check/CI debugging and dependency triage.

## Decision Rules (When to Use What)

These rules prevent most “why did this file change?” confusion.

- Want to create/modify package files with good defaults → `usethis::use_*()`
- Want to run the daily dev loop quickly → `devtools::load_all()`
- Want to update `man/` + `NAMESPACE` from roxygen → `devtools::document()`
- Want a fast docs-only check loop → `devtools::check_man()`
- Want the real integration gate → `devtools::check()`

Idempotence rule: before running a `use_*()` helper, read its docs once.
Most are safe to re-run, but if a helper changes important identifiers
(package name, repo settings, licensing), treat it like a refactor.

## Common Pitfalls

- **Treating `usethis` as a daily driver for everything:** you still need the
  dev loop (`load_all()`/`document()`/`check()`), tests, and disciplined check runs.
- **Skipping Git until later:** you lose history and make collaboration harder.
- **Assuming setup is “done forever”:** project scaffolding evolves; re-running
  helpers to update structure is sometimes appropriate.

## A practical mapping (task → helper)

This is a “what do I run?” map you can use without searching:

- Create package: `usethis::create_package()`
- Start Git: `usethis::use_git()`
- Add README source: `usethis::use_readme_rmd()`
- Add testthat: `usethis::use_testthat(3)`
- Add a test file: `usethis::use_test("topic")`
- Add a vignette: `usethis::use_vignette("topic")`
- Add a pkgdown site scaffold: `usethis::use_pkgdown()` / GitHub Pages helper

Rule of thumb:

- Use usethis to _create/modify files consistently_.
- Use devtools to _run the daily loop_ (`load_all()`, `document()`, `test()`, `check()`).

## Common Pitfalls

- **Treating `usethis` as a daily driver for everything:** you still need the
  dev loop (`load_all()`/`document()`/`check()`), tests, and disciplined check runs.
- **Running scaffolding on a dirty working tree:** it becomes hard to review what changed.
- **Confusing `.Rbuildignore` vs `.gitignore`:**
  - `.Rbuildignore` controls what ships in the package tarball
  - `.gitignore` controls what is committed to git
- **Assuming setup is “done forever”:** project scaffolding evolves; re-running
  helpers to update structure is sometimes appropriate.

## Troubleshooting

### “I ran a `use_*()` helper and now check fails”

1. Inspect what changed (keep scaffolding in its own commit).
2. Run `devtools::check()` and read the first failure.
3. If the failure is dependency-related, confirm `DESCRIPTION` updated the way you expect.

### “I don’t know which helper I need”

Search the usethis reference index for your noun/verb:
https://usethis.r-lib.org/reference/index.html

Then prefer the helper that does the smallest scoped change.

## References

- usethis reference index: https://usethis.r-lib.org/reference/index.html
- R Packages (2e), “The whole game”: https://r-pkgs.org/whole-game.html
