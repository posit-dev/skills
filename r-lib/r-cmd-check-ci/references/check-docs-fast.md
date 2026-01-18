# Faster doc iteration with `devtools::check_man()`

When you’re actively editing roxygen/Rd, you usually want fast feedback on:

- Rd syntax and cross-references
- examples that error, hang, or leave side effects
- “unstated dependency” problems in examples

`devtools::check_man()` runs the documentation-focused subset of `R CMD check` so
you can iterate quickly, then finish with a full `devtools::check()`.

Key mental model:

- `devtools::document()` regenerates `man/` and `NAMESPACE` from roxygen.
- `devtools::check_man()` validates docs (including running examples).
- `devtools::check()` is the full integration gate.

## Table of Contents

- [When to use it](#when-to-use-it)
- [What it runs (and what it skips)](#what-it-runs-and-what-it-skips)
- [Fast loop](#fast-loop)
- [Common failures and fixes](#common-failures-and-fixes)
- [When you must switch to `devtools::check()`](#when-you-must-switch-to-devtoolscheck)
- [References](#references)

## When to use it

Use `devtools::check_man()` when you are working on:

- roxygen blocks (`@param`, `@returns`, `@examples`, `@seealso`, etc.)
- generated `man/*.Rd`
- examples, especially those that interact with files, options, or external services

It is especially useful when `devtools::check()` is “too slow” for the edit → run
→ fix cadence you want while writing docs.

## What it runs (and what it skips)

`check_man()` tries to run the documentation-related checks in a similar way to
`R CMD check`, including running examples.

It is not a replacement for `devtools::check()`.

Two practical reasons:

- `R CMD check` also validates installation, namespace loading/unloading, tests,
  and vignettes.
- Some documentation checks interact with package loading/installation in ways
  that `check_man()` cannot fully replicate.

## Fast loop

Use this loop while you’re editing docs:

1. Make your roxygen/Rd changes.
2. If your changes affect generated `.Rd` or `NAMESPACE`, regenerate:

```r
devtools::document()
```

3. Run:

```r
devtools::check_man()
```

4. Fix failures until `check_man()` is clean.
5. Run `devtools::check()` before you consider the change “done”.

If it seems like your edits are not showing up:

- confirm that you regenerated Rd via `devtools::document()` (sometimes you’ll
  call this explicitly while iterating)
- confirm you’re viewing development docs (after `devtools::load_all()`, `?foo`
  should say “Rendering development documentation …”)

## Common failures and fixes

### Missing / mismatched argument documentation

Symptoms:

- “Documented arguments not in \usage”
- “Undocumented arguments”

Fix:

- update the roxygen block to match the function signature
- re-run `devtools::document()` (explicitly or via your normal workflow)

Prevention: when you change a signature, update `@param` in the same commit.

### Rd cross-reference errors

Symptoms:

- “Rd cross-references” failures
- broken `\link{}` or markdown links

Fix:

- fix typos in links
- ensure the referenced topic exists and is exported under that alias

Common causes:

- you renamed an exported function but didn’t update `@seealso`/links
- you linked to a function that is not exported
- you used the wrong link syntax for roxygen markdown

### Examples that error

Examples must not error during check.

If you need to show a failure mode for teaching, prefer `try()` so readers can
see the error, but the example continues:

```r
try(your_function_that_errors())
```

If examples should only run in specific circumstances (token available,
interactive session, etc.), prefer `@examplesIf` so users see realistic code and
pkgdown can still render the examples fully.

Decision rule for conditional examples:

- If it’s safe and fast, make it unconditional.
- If it requires a dependency or environment condition, prefer `@examplesIf`.
- Avoid hiding large parts of your docs behind `if (requireNamespace(...))` unless
  you truly want sparse rendered examples.

### Examples with side effects

Examples are run in constrained environments during `R CMD check`.

Avoid:

- changing the working directory
- writing outside of `tempdir()`
- leaving modified `options()` or environment variables behind

If you must change something, undo it explicitly in the example code.

If your example changes process state (wd/options/env vars), prefer `withr`
helpers or explicit `on.exit()` patterns to ensure cleanup.

### Example uses an unstated dependency

If examples use functions from another package:

- record that dependency in `DESCRIPTION` (often in `Suggests`)
- in the example, call functions with `pkg::fun()` or `library(pkg)` so it’s
  clear where they come from

If you add or move a dependency, reinstall locally so your environment matches
what check expects:

```r
devtools::install_deps(dependencies = TRUE)
```

## When you must switch to `devtools::check()`

Switch to `devtools::check()` when you:

- changed package code, NAMESPACE/imports, or compiled code
- touched tests or vignettes
- need to validate the full install/load/unload surface
- are preparing for a PR merge or a release

Also switch when `check_man()` is clean but CI still fails: the failure is
likely in install/load/tests/vignettes rather than docs.

## References

- devtools: `check_man()`: https://devtools.r-lib.org/reference/check_man.html
- R Packages (2e): Function documentation + examples guidance: https://r-pkgs.org/man.html
- R Packages (2e), Appendix A — documentation checks inside `R CMD check`: https://r-pkgs.org/R-CMD-check.html
