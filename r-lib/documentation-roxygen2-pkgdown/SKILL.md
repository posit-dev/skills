---
name: r-lib/documentation-roxygen2-pkgdown
description: >
  R package documentation workflows with roxygen2, vignettes, and pkgdown.
  Use this skill when working on an R package that needs to:
  (1) Write, regenerate, and preview function documentation using roxygen2,
  (2) Keep `NAMESPACE` and `.Rd` files in sync via `devtools::document()`,
  (3) Write examples that run under `R CMD check` and follow current best practices,
  (4) Add package-level documentation via `"_PACKAGE"` and `usethis::use_package_doc()`,
  (5) Create and maintain vignettes, and decide when to use pkgdown articles instead,
  (6) Understand pkgdown basics (site build and linking); use `r-lib/pkgdown-site-craft` for curation + deployment.
  Also use when debugging documentation failures in `R CMD check`, migrating older
  docs to modern roxygen + markdown conventions, or improving documentation quality.
---

# Documentation for R Packages (roxygen2 + pkgdown)

Documentation is part of the package contract: it must be readable, runnable, and
portable across machines.

If you only remember one thing: roxygen comments are the source of truth, and
`R CMD check` executes your examples.

## When to Use What

| Task                                                  | Use                                                                     |
| ----------------------------------------------------- | ----------------------------------------------------------------------- |
| Regenerate `.Rd` docs and `NAMESPACE`                 | `devtools::document()`                                                  |
| Iterate quickly on documentation failures             | `devtools::check_man()` (focuses on Rd + examples)                      |
| Preview documentation during development              | `devtools::load_all()` then `?your_function`                            |
| Create package-level help topic                       | `usethis::use_package_doc()` (creates `"_PACKAGE"` sentinel)            |
| Write examples that pass checks                       | Follow `references/examples-policy.md` (no errors, fast, restore state) |
| Create a vignette                                     | `usethis::use_vignette("topic")`                                        |
| Build a vignette against a development install        | `devtools::build_rmd("vignettes/topic.Rmd")`                            |
| Create an article that does not ship with the package | `usethis::use_article("topic")` (pkgdown-only)                          |
| Decide vignette vs pkgdown article                    | Criteria in `references/vignettes-vs-articles.md`                       |
| Build a pkgdown website                               | pkgdown workflow (see `references/pkgdown-overview.md`)                 |
| Set up pkgdown + GitHub Pages deployment              | `usethis::use_pkgdown_github_pages()`                                   |

## The Roxygen Workflow (4 Steps)

1. Add roxygen comments above the function.
2. Run `devtools::document()` to regenerate `man/*.Rd` and `NAMESPACE`.
3. Preview with `?function` (ensure you have run `devtools::load_all()` recently).
4. Repeat until the docs read well and examples run.

When the problem is “`R CMD check` fails on docs/examples”, tighten the loop with:

```r
devtools::document()
devtools::check_man()
```

Then confirm with a full check before you ship:

```r
devtools::check()
```

## A high-quality roxygen block (template)

This is a practical shape that works well in real packages:

```r
#' Title: short and specific
#'
#' @description
#' 1–3 sentences: what is this for, and when do I use it?
#'
#' @param x What `x` means (type, constraints, units).
#' @param na.rm Whether to remove missing values.
#' @returns A numeric scalar.
#'
#' @examples
#' x <- c(1, 2, NA)
#' my_fun(x)
#' my_fun(x, na.rm = TRUE)
#'
#' @examplesIf requireNamespace("ggplot2", quietly = TRUE)
#' ggplot2::qplot(x, my_fun(x, na.rm = TRUE))
my_fun <- function(x, na.rm = FALSE) {
  # ...
}
```

Key properties:

- Minimal successful call first.
- One common option next.
- Optional “power” example is conditional via `@examplesIf`.
- External calls are explicit (`pkg::fun()`).

## Writing High-Quality Help Topics

- Use a strong title and a concise description that helps in reference indexes.
- Document arguments and return value clearly (prefer `@returns` over `@return`).
- Prefer roxygen2 markdown (ensure `Roxygen: list(markdown = TRUE)` in `DESCRIPTION`).
- Use links like `[otherpkg::fun()]` and `vignette("topic")` for automatic cross-linking.

Practical rule: if your help topic can’t teach a correct, minimal use in ~10 lines
of example code, move the longer narrative to a vignette or article.

For check-safe example rules and cleanup recipes, see:

- [references/examples-policy.md](references/examples-policy.md)

## Reusing Documentation

Use roxygen2 reuse features when you have repeated argument docs or shared sections:

- `@inheritParams` for shared arguments.
- `@inheritSection` for shared sections.
- `@rdname` when multiple functions belong in one help topic.

## Examples That Pass `R CMD check`

Examples should:

- Run without errors.
- Be fast.
- Leave the world as you found it.
- Use only declared dependencies.

For optional or environment-dependent examples, prefer `@examplesIf` (see `references/examples-policy.md`).

## Common failures → fastest fixes

### “Rd cross-references” / broken links

- Prefer roxygen markdown links like `[pkg::fun()]`.
- Ensure the linked function/topic is exported and spelled correctly.
- Re-run `devtools::document()` and then `devtools::check_man()`.

### “there is no package called …” from examples

- Add the dependency to `DESCRIPTION` (often `Suggests` for examples).
- Use `@examplesIf requireNamespace("pkg", quietly = TRUE)` for optional packages.
- Prefer `pkg::fun()` calls so dependency usage is explicit.

### Examples change state and fail on CI

Common culprits: `options()`, `Sys.setenv()`, working directory, files.

- Use `on.exit(..., add = TRUE)` (or `withr` in tests) to restore state.
- Write only to `tempdir()`.
- Avoid `setwd()` unless absolutely necessary.

## Package-Level Documentation

Use `usethis::use_package_doc()` to create a package-level help topic using the
`"_PACKAGE"` sentinel, and to establish a natural home for package-wide
housekeeping patterns.

## Vignettes and Articles

- Vignettes ship with the package and are checked.
- Articles are like vignettes, but live only on the pkgdown website (and can be
  useful when you do not want to formalize certain dependencies).

Vignette workflow gotcha: by default, vignettes are built against the installed
package, not your current source. Use `devtools::build_rmd()` or install a dev
version before knitting.

If a vignette is too slow or relies on non-portable dependencies, convert it to a
pkgdown-only article (see [references/vignettes-vs-articles.md](references/vignettes-vs-articles.md)).

## Pkgdown Overview

Pkgdown consolidates function reference, articles/vignettes, and README content
into a cohesive, interlinked website.

If your focus is site configuration, reference index curation, or GitHub Pages deployment, use:

- [r-lib/pkgdown-site-craft](../pkgdown-site-craft/)

## Resources & Advanced Topics

### Reference Files

- **[references/roxygen-workflow.md](references/roxygen-workflow.md)** - The 4-step workflow and preview behavior
- **[references/roxygen-tags-and-structure.md](references/roxygen-tags-and-structure.md)** - Tags, blocks, and markdown features
- **[references/rd-intro-quality.md](references/rd-intro-quality.md)** - Title/description/details guidance
- **[references/examples-policy.md](references/examples-policy.md)** - Examples: errors, dependencies, conditional execution, state
- **[references/package-level-docs.md](references/package-level-docs.md)** - `"_PACKAGE"` and package-level documentation
- **[references/vignettes-workflow.md](references/vignettes-workflow.md)** - Vignette creation and development workflow
- **[references/vignettes-vs-articles.md](references/vignettes-vs-articles.md)** - Choosing vignettes vs pkgdown articles
- **[references/pkgdown-overview.md](references/pkgdown-overview.md)** - What pkgdown provides and how linking works

### External Resources

- R Packages (2e): Function documentation: https://r-pkgs.org/man.html
- R Packages (2e): Vignettes: https://r-pkgs.org/vignettes.html
- roxygen2 site: https://roxygen2.r-lib.org/
- pkgdown site: https://pkgdown.r-lib.org/

### Related Skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - Documentation-related failures in checks and CI
- [r-lib/package-development-workflow](../package-development-workflow/) - Where docs fit into the daily dev loop
- [r-lib/testing-r-packages](../testing-r-packages/) - Testing examples and snapshots that relate to docs output
- [r-lib/pkgdown-site-craft](../pkgdown-site-craft/) - Site configuration, curation, and deployment
