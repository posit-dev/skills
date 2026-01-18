# R CMD check playbook (error → fix mapping)

This is a fast triage map from common `R CMD check` output to concrete fixes.
It’s designed for the “I have a failing check log; what do I do next?” moment.

## Table of Contents

- [First move: find the right log](#first-move-find-the-right-log)
- [Triage order](#triage-order)
- [Reproduce reliably (local + CI)](#reproduce-reliably-local--ci)
- [Phase-by-phase cheat sheet](#phase-by-phase-cheat-sheet)
- [Common NOTES worth fixing](#common-notes-worth-fixing)
- [Related pages](#related-pages)
- [References](#references)

## First move: find the right log

Before changing code, open the log that contains the actual error:

- `00check.log` gives the overall phase ordering.
- Installation/build problems usually show in `00install.out`.
- Test failures show in `tests/testthat.Rout`.
- Example failures are reported under the Documentation phase.

In GitHub Actions, the step output is often enough to start, but the most
actionable detail is still usually in the `.Rcheck` logs (the same files as
above).

## Reproduce reliably (local + CI)

When a check fails, the fastest path to a real fix is a _reproducible_ failure.

### Local reproduction (default)

```r
devtools::check()
```

### Local reproduction (closer to CRAN)

```r
devtools::check(args = "--as-cran")
```

### Narrow the surface area

- Docs/examples: `devtools::check_man()` (see `check-docs-fast.md`)
- Tests only: `devtools::test()`

### CI reproduction mindset

If CI fails but local passes, assume one of:

- undeclared dependency (present locally, absent on runner)
- OS-specific path/encoding issue
- missing system dependency
- reliance on interactive state (working dir, options, attached packages)

## Triage order

1. Fix **ERROR**.
2. Fix **WARNING**.
3. Then fix/justify **NOTE**.

Within that: fix anything that prevents install/load first.

Decision rule: if the package does not install and load cleanly, nothing else is
trustworthy. Fix install/load before chasing docs/tests/vignettes.

## Phase-by-phase cheat sheet

### Check metadata / package structure

Common messages:

- “non-portable file paths / file names”
- “hidden files”
- “executable files”

Typical fixes:

- Rename files to portable names; avoid spaces and non-ASCII in file names.
- Add development-only files to `.Rbuildignore`.
- Remove executables from the package (or follow the CRAN guidance if applicable).

### DESCRIPTION

Common messages:

- malformed `DESCRIPTION` fields
- missing dependency versions
- “packages in Suggests must be installed” (unless `_R_CHECK_FORCE_SUGGESTS_` is false)

Typical fixes:

- Validate `DESCRIPTION` formatting.
- Ensure every package referenced in `NAMESPACE` is also in `Imports` or `Depends`.
- Install deps (see `installing-check-deps.md`) or relax locally with
  `devtools::check(force_suggests = FALSE)` when appropriate.

### Namespace / loading

Common messages:

- package fails to load with `R_DEFAULT_PACKAGES=NULL`
- “namespace cannot be loaded”

Typical fixes:

- Add missing package dependencies to `DESCRIPTION`.
- Ensure you’re not relying on attached packages.
- Regenerate `NAMESPACE` via roxygen + `devtools::document()`.

High-frequency gotcha:

- Code that works interactively because you attached packages in your session.
  Fix by using `pkg::fun()` or explicit imports.

### R code checks

Common messages:

- “Namespace in Imports field not imported from …”
- “no visible binding for global variable …”

Typical fixes:

- Prefer `pkg::fun()` calls in package code.
- If you truly need an import, add it with roxygen/usethis and re-document.
- For false positives in NSE, use `utils::globalVariables()` judiciously.

### Documentation + examples

Common messages:

- Rd syntax / xref errors
- examples failing, hanging, or leaving side effects

Typical fixes:

- Iterate with `devtools::check_man()` while fixing docs (see `check-docs-fast.md`).
- Ensure examples are fast, error-free, and restore global state.

Common messages and fixes:

- “Rd files must have a non-empty title/description”
  - add `@title` / `@description` and re-document
- “Undocumented arguments” / “Documented arguments not in \\usage”
  - align `@param` with the function signature
- “Running examples … ERROR”
  - remove side effects, declare missing suggests, avoid network

### Tests

Common messages:

- testthat failures that only happen in check/CI

Typical fixes:

- Make tests self-sufficient and clean up state (options/env vars/WD).
- Avoid reliance on external services, local files, or user config.

### Vignettes

Common messages:

- vignette fails to build/compile

Typical fixes:

- Ensure vignette dependencies are in `Suggests`.
- Reduce runtime and avoid network access; use cached/recorded artifacts if needed.
- If content is not appropriate as a vignette, consider a pkgdown article instead.

If the vignette uses a package, declare it in `Suggests`.
If the vignette needs heavy system tooling, reconsider shipping it.

## Common NOTES worth fixing

NOTEs can be benign, but many are signals of real portability or CRAN issues.

### "Non-portable file paths" / "non-ASCII"

- Avoid non-ASCII file names.
- Use UTF-8 and declare `Encoding: UTF-8` when needed.
- Use forward slashes in paths inside the package.

### "No visible binding for global variable"

- For NSE-heavy code (e.g. dplyr), declare known symbols via `utils::globalVariables()`.
- Prefer writing code that doesn’t depend on non-standard evaluation where possible.

### "Possibly misspelled words in DESCRIPTION"

- Either fix typos or add legitimate words to the appropriate dictionary/wordlist (project-specific).

### "Found the following (possibly) invalid URLs"

- Ensure URLs in `DESCRIPTION`, docs, and README are correct and use https when available.

Fix patterns:

- replace redirects with the final `https://` URL
- avoid `http://` unless necessary
- keep `URL:` formatting valid (comma-separated list is common)

## Related pages

- [Mental model](r-cmd-check-mental-model.md)
- [DESCRIPTION fields](description-fields-that-affect-check.md)
- [Dependencies in practice](dependencies-in-practice.md)
- [Install check deps](installing-check-deps.md)
- [CI with r-lib/actions](r-lib-actions-and-check-standard.md)

## References

- R Packages (2e), Appendix A — `R CMD check`: https://r-pkgs.org/R-CMD-check.html
- devtools: `check()`: https://devtools.r-lib.org/reference/check.html
