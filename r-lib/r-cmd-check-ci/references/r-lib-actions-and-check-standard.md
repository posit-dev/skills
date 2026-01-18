# GitHub Actions CI with r-lib/actions (`check-standard`)

## Table of Contents

- [Scope](#scope)
- [Practical guidance](#practical-guidance)
- [Quick start](#quick-start)
- [What `check-standard` gives you](#what-check-standard-gives-you)
- [Common customizations (and when to do them)](#common-customizations-and-when-to-do-them)
- [Debugging workflow failures](#debugging-workflow-failures)
- [Canonical references](#canonical-references)

## Scope

How to set up CI to run `R CMD check` on GitHub using the standard r-lib/actions
workflow(s), especially `check-standard`.

This page is intentionally pragmatic: it explains what you get by default, what
people commonly customize, and how to debug failures without guesswork.

## Practical guidance

- Use `usethis::use_github_action("check-standard")` to add the standard `R CMD check` workflow.
- Treat CI as enforcing the same quality bar as local `devtools::check()`.

## Quick start

1. In your package root, scaffold the workflow:

```r
usethis::use_github_action("check-standard")
```

2. Commit the generated files (usually `.github/workflows/R-CMD-check.yaml`).
3. Push to GitHub and inspect the Actions run.

If the first CI run fails, your job is to reproduce locally and fix the root
cause, not to keep tweaking the workflow until it passes.

For local reproduction strategy, see:

- [r-cmd-check-mental-model.md](r-cmd-check-mental-model.md)
- [installing-check-deps.md](installing-check-deps.md)

## What `check-standard` gives you

At a high level, `check-standard` is the “sensible default” workflow for R
packages:

- Runs `R CMD check` in clean environments.
- Uses a cross-platform matrix (commonly Linux/macOS/Windows).
- Installs dependencies reproducibly.
- Uploads check results when failures occur (so you can read the `.Rcheck` logs).

The exact matrix and setup evolve over time; treat the workflow as a maintained
default rather than a file you copy once and never revisit.

## Common customizations (and when to do them)

### 1) Adjust the check matrix

Common reasons:

- Package uses OS-specific code (you need Windows/macOS coverage).
- You want to test multiple R versions.
- You want a faster default (e.g., Linux-only for internal packages).

Rule of thumb: don’t drop Windows/macOS just to make a flaky test “go away”.
Fix the portability issue instead.

### 2) Install system dependencies

If CI fails with compilation errors or missing system libraries, this is usually
about system deps, not R deps.

Typical signals:

- Errors mention headers/libraries not found (e.g., `-l…` / `…/include`).
- A package fails to install from source.

Approach:

- Identify the system dependency.
- Add explicit installation steps for the runner OS.
- Keep these steps minimal and documented.

### 3) Split website builds from check

If you use pkgdown, keep “build and deploy website” as a separate workflow.

Reasons:

- Website builds often need extra tooling/dependencies.
- You don’t want check to depend on GitHub Pages configuration.
- It keeps your CI signal clean: check failures mean package failures.

### 4) Handle optional dependencies cleanly

If your package has optional features:

- Declare optional runtime deps in `Suggests`.
- Guard usage with `requireNamespace("pkg", quietly = TRUE)`.
- Use conditional examples (`@examplesIf`) and conditional tests.

Avoid turning CI into “whatever happens to be installed”. Make optionality
explicit.

See: [dependencies-mindset.md](dependencies-mindset.md)

## Debugging workflow failures

### Find the actionable log

When the workflow fails, open the job logs and locate the `.Rcheck` output.
The first meaningful error in the relevant log file is usually the root cause;
later messages are often cascading.

### Classify the failure

Fast classification tends to narrow the fix:

- Install/build failure → system deps, toolchain, or DESCRIPTION/NAMESPACE.
- Load/namespace failure → missing imports, bad `.onLoad()`, relying on attached packages.
- Example failure → undeclared deps, side effects, slow examples.
- Test failure → hidden state, ordering dependence, file paths.

Then reproduce locally with `devtools::check()` before making changes.

## Canonical references

- R Packages (2e), “Software development practices” (CI): https://r-pkgs.org/software-development-practices.html
- r-lib/actions: https://github.com/r-lib/actions
- usethis: `use_github_action()`: https://usethis.r-lib.org/reference/use_github_action.html
