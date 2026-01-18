# Dependencies in practice (code, tests, examples, vignettes)

How to _use_ dependencies correctly in each place they show up:

- Package code under `R/`
- Tests under `tests/testthat/`
- Examples under `man/` (roxygen)
- Vignettes under `vignettes/`

This is where most “missing dependency” check failures originate.

Related pages in this skill:

- [dependencies-mindset.md](dependencies-mindset.md)
- [description-fields-that-affect-check.md](description-fields-that-affect-check.md)
- [installing-check-deps.md](installing-check-deps.md)

## Table of Contents

- [Two key facts to internalize](#two-key-facts-to-internalize)
- [The dependency triangle (DESCRIPTION, NAMESPACE, code)](#the-dependency-triangle-description-namespace-code)
- [Recommended defaults by context](#recommended-defaults-by-context)
- [Cookbook (common patterns)](#cookbook-common-patterns)
- [S3 generics and methods](#s3-generics-and-methods)
- [NSE and “no visible binding” NOTES](#nse-and-no-visible-binding-notes)
- [Development-only dependencies (`Config/Needs/*`)](#development-only-dependencies-configneeds)
- [Common failure messages → likely cause](#common-failure-messages--likely-cause)
- [References](#references)

## Two key facts to internalize

1. Listing a package in `Imports` ensures it gets installed, but does **not**
   automatically attach it or import its functions.
2. `R CMD check` tries hard to detect code that relies on packages being attached.

## The dependency triangle (DESCRIPTION, NAMESPACE, code)

Most dependency problems are a mismatch between these three layers:

- **Code**: how you reference external functions (explicit `pkg::fun()` vs relying on imports/search path).
- **NAMESPACE**: what gets imported/exported (usually generated from roxygen).
- **DESCRIPTION**: what must be installed (`Imports`/`Depends`) vs optional (`Suggests`).

Rules that prevent many failures:

- If `NAMESPACE` references a package, that package must be listed in `Imports` or `Depends`.
- If code uses `pkg::fun()`, you usually do _not_ need an import for `fun()`.
- If code uses an operator or unqualified symbol that can’t be written as `pkg::op`, you likely need an import.

## Recommended defaults by context

### In package code under `R/`

Default recommendation:

- Call external functions with `pkg::fun()`.

Import exceptions (when you _must_ import):

- Operators can’t be called with `::` (e.g. `%||%`, `%>%`), so you need an import.
- High-frequency or readability-sensitive calls may justify importing a function.

If you import:

- Add roxygen namespace tags and regenerate with `devtools::document()`.
- Keep imports centralized (often via the `"_PACKAGE"` file / package doc sentinel).

### In `NAMESPACE` / roxygen imports

Prefer generating NAMESPACE via roxygen, not hand editing.

Typical patterns:

- Use `pkg::fun()` in code (no import needed).
- Use `@importFrom pkg fun` when you must import (operators, S3 generics, or
  deliberate readability improvements).

After changes:

```r
devtools::document()
devtools::check()
```

### In tests

- Prefer `pkg::fun()` for external calls (same reasoning as in package code).
- Avoid `library()`/`require()` which changes the search path and can mask problems.
- If a suggested dependency is genuinely hard to install, use
  `testthat::skip_if_not_installed("pkg")` around the small set of tests that need it.

Keep skips narrow: don’t skip the whole test suite because one optional package
is hard to install.

### In examples

Examples are executed during check.

Recommended defaults:

- Record any package used in examples in `DESCRIPTION` (often in `Suggests`).
- Prefer `pkg::fun()` so the dependency is explicit.

If examples should only run in specific circumstances (token available, network
allowed, interactive session), prefer `@examplesIf` so readers see realistic code
and pkgdown can still render the examples.

Avoid putting large swaths of example code behind `if (requireNamespace(...))`
blocks unless you truly want the rendered examples to be sparse.

Prefer making examples _explicit_ and _conditionally runnable_:

- explicit: `otherpkg::fun()`
- conditional: `@examplesIf` (so pkgdown and readers see real code)

### In vignettes

Vignettes are checked and should be reproducible:

- Ensure vignette-only dependencies are in `Suggests`.
- Prefer deterministic, offline execution.
- If content would require heavy or non-portable dependencies, prefer a pkgdown
  article instead of a vignette.

Vignette-specific habit: if the vignette uses a package, declare it (often in
`Suggests`) and make sure the vignette is still reproducible in a clean session.

See: [vignettes-workflow.md](../../documentation-roxygen2-pkgdown/references/vignettes-workflow.md)

## Cookbook (common patterns)

### Calling external functions

Default:

```r
otherpkg::fun(x)
```

Benefits:

- dependency is obvious in code review
- no surprise search-path reliance

### Operators from other packages

You can’t call most operators with `::`.

Recipe:

1. Add the package to `Imports`.
2. Add an import for the operator (typically via roxygen):

```r
#' @importFrom rlang %||%
NULL
```

3. Run `devtools::document()`.

### Optional feature with an optional dependency

Make the “requires X” boundary explicit:

```r
if (!requireNamespace("optionalpkg", quietly = TRUE)) {
  stop("This feature requires 'optionalpkg'. Install it with install.packages('optionalpkg').")
}
```

Then declare `optionalpkg` in `Suggests` (if it’s truly optional at runtime).

### Tests that require an optional package

```r
testthat::skip_if_not_installed("optionalpkg")
```

### Examples that require special environment (token/network)

Prefer `@examplesIf` in roxygen instead of hiding code behind
`if (requireNamespace(...))` blocks.

### Website / docs tooling deps

If you need extra packages only for website builds, record them under a
`Config/Needs/*` field in `DESCRIPTION` and have CI install them via r-lib/actions.

See: [installing-check-deps.md](installing-check-deps.md)

## S3 generics and methods

If you implement S3 methods for generics owned by another package, dependency problems
can show up as namespace/load failures.

Recommended defaults:

- Be explicit about which package owns the generic.
- Prefer explicit imports for generics when needed (often via roxygen `@importFrom`).
- Re-run `devtools::document()` after changing imports/exports.

Recipe (generic import via roxygen, often in `"_PACKAGE"`):

```r
#' @importFrom stats predict
NULL
```

Then:

```r
devtools::document()
devtools::check()
```

## Common failure messages → likely cause

- “there is no package called …”: missing `Imports`/`Suggests`, or a dep not being
  installed in the current environment.
- “could not find function …”: relying on attached packages instead of `pkg::fun()`
  or an explicit import.
- “Namespace dependency not required”: NAMESPACE references a package that isn’t
  listed in `Imports`/`Depends`.
- Examples fail on CI but pass locally: hidden dependency on local state, file
  path, network, or a package you happen to have installed.

## NSE and “no visible binding” NOTES

Some non-standard evaluation (NSE) workflows can trigger NOTES like:
“no visible binding for global variable …”.

Guidance:

- Prefer standard evaluation where practical.
- If the NOTE is a known false positive, declare the symbols narrowly with
  `utils::globalVariables()`.

Treat this as a last resort: don’t silence warnings you haven’t understood.

## Development-only dependencies (`Config/Needs/*`)

For dependencies that are not appropriate as formal runtime deps (e.g. website tooling):

- Record them in a `Config/Needs/*` field in `DESCRIPTION`.
- Install them in CI via r-lib/actions `setup-r-dependencies@v2` using `needs:`.

Decision rule: if something is only used in one CI job (website, coverage), record it
under `Config/Needs/*` and install it only for that job.

## References

- R Packages (2e), “Dependencies: In Practice”: https://r-pkgs.org/dependencies-in-practice.html
- R Packages (2e), “Dependencies: Mindset and Background”: https://r-pkgs.org/dependencies-mindset-background.html
