# The Whole Game: an end-to-end package workflow

## Table of Contents

1. [What “The Whole Game” Covers](#what-the-whole-game-covers)
2. [A Minimal Working Loop](#a-minimal-working-loop)
3. [Milestones and When to Do Them](#milestones-and-when-to-do-them)
4. [What Changes Require Which Step](#what-changes-require-which-step)
5. [Keeping the Loop Healthy](#keeping-the-loop-healthy)
6. [Common failure modes (and the fastest fixes)](#common-failure-modes-and-the-fastest-fixes)
7. [A release/PR readiness checklist](#a-releasepr-readiness-checklist)
8. [References](#references)

## What “The Whole Game” Covers

This reference is an opinionated, end-to-end workflow for R package development
using the modern r-lib toolchain. It connects:

- The **daily loop** (edit → load → try → document → check)
- The **project milestones** (create package, Git/GitHub, README, tests,
  documentation, CI readiness)

It is not a replacement for the canonical book chapters; it is a condensed map
you can use repeatedly.

## A Minimal Working Loop

In practice, you want a loop that is both fast and honest:

1. **Edit** files under `R/`.
2. **Reload** with `devtools::load_all()`.
3. **Try** a minimal example (one or two calls, not a full script).
4. **Document** with `devtools::document()` when roxygen/exports changed.
5. **Check** with `devtools::check()` regularly.

The reason this works is that each step exercises a distinct surface:

- `load_all()` makes iteration cheap and catches “does it run?” issues.
- `document()` keeps `NAMESPACE` + `man/` deterministic and aligned.
- `check()` is the integration test: it runs in a controlled context and
  exercises more than interactive use.

A concrete “start a session” recipe that avoids stale state:

```r
# Start from a clean session
devtools::load_all()

# Try the change minimally
# my_fun(...)

# Keep derived files in sync
devtools::document()

# Protect behavior
devtools::test()

# Integration gate
devtools::check()
```

Not every change needs every step every time, but the sequence is a reliable default.

## Milestones and When to Do Them

### 1) Package creation and initial structure

Do this once at the start:

- Create the package with `usethis::create_package()`.
- Establish a consistent project root (RStudio Project / stable working dir).

Practical rule: always know what directory you are in, and run package commands
from the package root.

### 2) Version control and collaboration

As early as possible:

- Initialize Git (`usethis::use_git()`).
- Connect to GitHub when you are ready to collaborate (`usethis::use_github()`).

### 3) Documentation surface (README + help topics)

Early, but after the package has a minimal point:

- Add `README.Rmd` (`usethis::use_readme_rmd()`) and keep it rendered.
- Add roxygen docs and keep them in sync with `devtools::document()`.

Derived-file discipline is the usual failure point:

- If you edit roxygen, run `devtools::document()`.
- Commit `NAMESPACE` and `man/*.Rd` changes.

### 4) Tests and checks

Once you have stable behavior worth protecting:

- Add tests (see `r-lib/testing-r-packages`).
- Keep `devtools::check()` clean as you grow features.

Treat a clean check as a habit, not a milestone.

## What Changes Require Which Step

Use this as a quick mapping:

- **Changed R code**: `devtools::load_all()`.
- **Changed exports / roxygen tags**: `devtools::document()`.
- **Changed README/vignettes/tests/deps**: `devtools::check()` sooner rather than later.

More detailed decision rules:

- **Changed imports/exports** (added `@importFrom`, `@export`, `@rawNamespace`):
  run `devtools::document()` immediately.
- **Changed examples**: run `devtools::check_man()` while iterating, then `devtools::check()`.
- **Changed tests**: run `devtools::test()` frequently, then `devtools::check()`.
- **Changed DESCRIPTION dependencies**: reinstall deps if needed, then `devtools::check()`.

If you’re not sure, choose the more conservative option: run `devtools::check()`.

If interactive behavior and `check()` disagree, trust `check()` and triage why.

## Keeping the Loop Healthy

Common practices that prevent “mysterious” failures:

- Treat the package root as the working directory.
- Avoid relying on undeclared packages (in code, examples, tests, vignettes).
- Keep documentation generation (`document()`) part of the habit.
- Run checks before pushing so CI is confirming, not discovering.

If you do one “health” practice: regularly restart R.
Many workflow issues are just session state.

If you do two: restart R and run `devtools::check()` before pushing.

## Common failure modes (and the fastest fixes)

### “It works in `load_all()` but fails in check/CI”

Almost always one of:

- missing dependency declaration
- relying on attached packages (`library()`/search path)
- docs out of sync (`NAMESPACE`/`man/`)
- file path assumptions

Fast fix loop:

1. Restart R.
2. `devtools::document()`.
3. `devtools::check()`.

### CI-only failures (Windows/macOS)

Treat these as portability issues, not “CI being weird”.

Common culprits:

- case-sensitive paths
- encoding/locale/timezone assumptions
- missing system dependencies

Use the `r-lib/r-cmd-check-ci` references to reproduce locally and find the first real error.

### Docs and examples fail

Typical causes:

- example uses a package you happen to have installed
- example writes files outside `tempdir()`
- example modifies global state without restoring

Fix:

- make deps explicit (`pkg::fun()`, `Suggests`, `@examplesIf`)
- restore state (`on.exit(...)`)
- tighten the loop with `devtools::check_man()`

## A release/PR readiness checklist

Use this checklist before you open a PR or cut a release:

- `devtools::check()` is clean locally.
- If you touched roxygen/imports/exports: `devtools::document()` was run and generated diffs are committed.
- If you changed behavior: tests exist and are meaningful.
- No hidden dependencies: everything used in code/examples/tests/vignettes is declared.
- Any non-portable workflows (network, credentials, heavy tooling) are moved to
  pkgdown-only articles or guarded appropriately.

If CI finds issues anyway, treat that as signal: your local workflow is missing
one of the surfaces CI exercises.

## References

- R Packages (2e), “The whole game”: https://r-pkgs.org/whole-game.html
- R Packages (2e), “Fundamental workflows”: https://r-pkgs.org/workflow101.html
