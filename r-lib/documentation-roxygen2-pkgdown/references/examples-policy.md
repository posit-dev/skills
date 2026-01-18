# Examples policy (R CMD check compatible)

Examples are user-facing documentation and part of the `R CMD check` surface.
Treat them like tiny, runnable tests for your API.

## Table of Contents

- [Non-negotiables](#non-negotiables)
- [Speed and determinism](#speed-and-determinism)
- [State hygiene (cleanup recipes)](#state-hygiene-cleanup-recipes)
- [Dependencies in examples](#dependencies-in-examples)
- [Conditional execution: pick the right tool](#conditional-execution-pick-the-right-tool)
- [Patterns that scale](#patterns-that-scale)
- [Anti-patterns](#anti-patterns)
- [Troubleshooting: common failures](#troubleshooting-common-failures)
- [References](#references)

## Non-negotiables

Every example should:

- **Run without errors**.
- **Be fast** (think seconds, not minutes).
- **Be deterministic** (or explicitly set and restore randomness).
- **Leave no mess** (no changed options/WD/env vars, no lingering files).

If you can’t satisfy these constraints, the content probably belongs in a vignette
or pkgdown article rather than `@examples`.

## Speed and determinism

Prefer examples that:

- Operate on small, in-memory objects.
- Avoid network calls.
- Avoid writing to user locations.
- Avoid randomness; if needed, set a seed (and restore state if you changed it).

If you need an example that demonstrates a slow workflow, make the slow part optional
and keep the core example runnable.

If you must use randomness:

- Prefer removing randomness entirely.
- Otherwise, set a seed and keep it local.

Example pattern:

```r
#' @examples
#' set.seed(1)
#' x <- rnorm(5)
#' my_fun(x)
```

## State hygiene (cleanup recipes)

Examples run in a clean-ish session, but they still share global state _within that
example run_. If you must change state, change it briefly and restore it.

If you already use withr in your package/dev stack, it can make “local + restore”
patterns clearer in examples and tests.

### Options

```r
#' @examples
#' old <- options(width = 60)
#' on.exit(options(old), add = TRUE)
#' options(width = 120)
#' str(1:3)
```

withr alternative (more concise):

```r
#' @examples
#' withr::local_options(list(width = 120))
#' str(1:3)
```

### Working directory

Prefer avoiding `setwd()` entirely. If you must:

```r
#' @examples
#' old <- getwd()
#' on.exit(setwd(old), add = TRUE)
#' setwd(tempdir())
#' file.create("example.txt")
```

Prefer writing to temporary files without changing the working directory:

```r
#' @examples
#' path <- tempfile(fileext = ".txt")
#' on.exit(unlink(path), add = TRUE)
#' writeLines("hello", path)
#' readLines(path)
```

### Environment variables

```r
#' @examples
#' old <- Sys.getenv("MY_PKG_EXAMPLE", unset = NA_character_)
#' on.exit({
#'   if (is.na(old)) Sys.unsetenv("MY_PKG_EXAMPLE") else Sys.setenv(MY_PKG_EXAMPLE = old)
#' }, add = TRUE)
#' Sys.setenv(MY_PKG_EXAMPLE = "1")
#' Sys.getenv("MY_PKG_EXAMPLE")
```

### Files

Write to `tempdir()` and clean up what you create:

```r
#' @examples
#' path <- file.path(tempdir(), "my-pkg-example.txt")
#' on.exit(unlink(path), add = TRUE)
#' writeLines("hello", path)
#' readLines(path)
```

## Dependencies in examples

Rule: examples may only use packages that are correctly declared in `DESCRIPTION`.

- If the example uses `otherpkg::fun()`, decide whether `otherpkg` is a hard dependency
  (`Imports`) or optional (`Suggests`).
- If the package is optional, **guard the example** so checks pass without it.

Prefer explicit namespace calls (`otherpkg::fun()`) in examples. It keeps dependencies
obvious and avoids relying on `library()`.

Practical decision rule:

- If a dependency is needed for core runtime behavior, it’s usually `Imports`.
- If a dependency is used only to enrich examples/plots, it’s usually `Suggests` + `@examplesIf`.

## Conditional execution: pick the right tool

There are three common ways to conditionally skip example code. Use the least-skippy
option that meets the goal.

### Best default: `@examplesIf`

Use `@examplesIf` when the code should run when an optional dependency is present,
and be cleanly omitted when it isn’t:

```r
#' @examplesIf requireNamespace("otherpkg", quietly = TRUE)
#' otherpkg::fun(x)
```

This keeps the rendered examples readable and keeps `R CMD check` happy.

### Acceptable: `\donttest{}` (only for expensive / flaky examples)

Use `\donttest{}` when the example is correct but too expensive or too fragile for
routine checks. It may still run in some configurations, so it must still be valid.

Important nuance: `\donttest{}` is not “never run”; it is “not run in the standard
check configuration”. Keep it minimal and correct.

### Use `\dontshow{}` when you need setup but don’t want it displayed

`\dontshow{}` runs the code but hides it from the printed example output. This is
useful for small setup steps (creating temp files, setting options) that would
otherwise clutter examples.

Use it sparingly; hidden work can confuse readers.

### Last resort: `\dontrun{}` (documentation-only)

Use `\dontrun{}` when code cannot be run automatically (e.g., requires credentials,
interactive authentication, or external systems). Keep `\dontrun{}` blocks small and
surround them with runnable setup code where possible.

When you do use `\dontrun{}`:

- explain why it can’t be run
- keep the snippet small
- prefer placing full workflows in vignettes/articles instead

## Patterns that scale

### “One runnable example + one optional power example”

```r
#' @examples
#' x <- 1:5
#' my_fun(x)
#'
#' @examplesIf requireNamespace("ggplot2", quietly = TRUE)
#' ggplot2::qplot(x, my_fun(x))
```

### “Minimal example + link to longer narrative”

If the real-world workflow is too big for examples, keep `@examples` tiny and
link out:

- A vignette (ships + checked)
- A pkgdown-only article (doesn’t ship; can be heavier)

### “Show the default path”

Examples should demonstrate the _default_ usage path first. Put advanced knobs
behind conditionals or in vignettes/articles.

## Anti-patterns

- Network calls (HTTP, databases, cloud).
- Writing to user directories (home, Documents, project root).
- Changing global state without restoring it.
- Sleeping / waiting / timing-dependent assertions.
- Relying on attached packages (`library(dplyr)` in examples) instead of `pkg::fun()`.

## Troubleshooting: common failures

### “there is no package called …”

The example used an undeclared dependency.

- Add it to `Suggests` (or `Imports` if truly required at runtime).
- Guard with `@examplesIf requireNamespace("pkg", quietly = TRUE)`.

Also check that the example uses `pkg::fun()` rather than `library(pkg)`.

### “Examples must run in \dontrun” / “Examples with side effects”

Your examples are doing non-check-friendly work.

- Remove network/file-system dependencies.
- Move the heavy workflow to a vignette or pkgdown article.

### Works locally, fails on CI

- You may have packages installed locally that are not declared.
- You may be relying on a non-empty working directory.
- You may be relying on system libraries not present on runners.

See related check guidance in the `r-lib/r-cmd-check-ci` skill.

If you want the fastest confirmation that you’re not relying on session state,
restart R before running the example.

## References

- R Packages (2e), “Function documentation”: https://r-pkgs.org/man.html
- R Packages (2e), “R CMD check”: https://r-pkgs.org/R-CMD-check.html
- roxygen2: conditional examples (`@examplesIf`): https://roxygen2.r-lib.org/
