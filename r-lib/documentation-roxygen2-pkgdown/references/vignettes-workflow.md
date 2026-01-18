# Vignettes workflow

## Table of Contents

- [What Vignettes Are (and Aren’t)](#what-vignettes-are-and-arent)
- [Creating a Vignette](#creating-a-vignette)
- [Mental model: build vs check](#mental-model-build-vs-check)
- [Developing Vignettes Efficiently](#developing-vignettes-efficiently)
- [Keeping Vignettes Check-friendly](#keeping-vignettes-check-friendly)
- [Dependencies and Suggests](#dependencies-and-suggests)
- [Vignette vs pkgdown article](#vignette-vs-pkgdown-article)
- [Common failure modes](#common-failure-modes)
- [References](#references)

## What Vignettes Are (and Aren’t)

Vignettes are long-form guides that ship with your package. They are part of the
check surface: they are built and executed (depending on configuration) during
`R CMD check`.

That means vignette code must be:

- reasonably fast
- robust across machines
- explicit about its dependencies

Vignettes are not a great place for:

- slow analysis pipelines
- network-bound workflows
- tutorials that require non-trivial system setup

If the content is valuable but too heavy for check, publish it as a pkgdown-only
article instead.

## Creating a Vignette

Create a new vignette skeleton:

```r
usethis::use_vignette("topic")
```

This scaffolds a new vignette and updates `DESCRIPTION` as needed.

Quick `DESCRIPTION` sanity checks when you ship vignettes:

- `Suggests:` includes `knitr` and `rmarkdown` (and any packages used in the vignette)
- `VignetteBuilder:` is present (commonly `knitr`)

If you commit vignettes, also ensure they build in a clean session via
`devtools::check()` (or at least `R CMD check`) before you consider the vignette
“done”.

## Mental model: build vs check

Vignettes have three “surfaces” you care about:

1. **Local iteration** (fast): knit one vignette while developing.
2. **Package build**: `R CMD build` may (depending on settings) include/build vignettes.
3. **Package check**: `R CMD check` will validate the built package and can (again,
   depending on configuration) run vignette code.

The operational point: something that “knits on my machine” can still fail in CI/CRAN
because check runs in a clean session with only declared dependencies.

## Developing Vignettes Efficiently

During development, you often want to build a single vignette against your
current dev state:

```r
devtools::build_rmd("vignettes/topic.Rmd")
```

This pattern helps you iterate without running a full check each time.

If your vignette depends on recent changes in package code, remember that
vignettes are typically built against an installed package. Installing a dev
version (or using `build_rmd()` with an up-to-date dev install) prevents “why is
my vignette using old behavior?” confusion.

Practical loop:

```r
devtools::load_all()
devtools::document()
devtools::check()
```

More surgical loops:

- Iterate on _one_ vignette: `devtools::build_rmd("vignettes/topic.Rmd")`
- Validate vignettes + examples more like check: `devtools::check_man()` and a full
  `devtools::check()` periodically

Use `build_rmd()` for quick iteration, but trust `check()` for the integration
surface.

## Keeping Vignettes Check-friendly

- Prefer small, illustrative examples over long-running analyses.
- Avoid network calls and system-specific paths.
- If you need expensive computations, consider whether the content belongs in a
  pkgdown article instead.

Chunk options are policy tools. Use them intentionally:

- Prefer to keep code runnable with `eval = TRUE`.
- If you must show code that is not run, say why and use `eval = FALSE`.
- If you must show expected output without running, use `eval = FALSE` + a precomputed
  output snippet (and make sure it stays correct).
- If you are demonstrating failure modes, use `error = TRUE` so the behavior is explicit
  without breaking the build.

Avoid relying on user state:

- don’t write into the package directory
- don’t rely on a user’s global options
- use temporary directories and clean up after yourself

If you must show failing behavior, use knitr chunk options deliberately (e.g.
`error = TRUE`) so check outcomes are intentional.

If the vignette needs a long-running computation, treat it as a publishing
artifact instead of a package artifact.

## Dependencies and Suggests

If a vignette uses a package, that relationship needs to be declared in
`DESCRIPTION` (often `Suggests`).

Also confirm `DESCRIPTION` has an appropriate `VignetteBuilder` entry when
shipping vignettes.

Decision rules that prevent most CI failures:

- If a vignette calls `library(foo)` or uses `foo::bar()`, add `foo` to `Suggests`.
- If a vignette needs system dependencies, reconsider whether it should ship.
- If a vignette is “optional content”, prefer a pkgdown article + website-only deps.

## Vignette vs pkgdown article

Use a vignette when:

- it is part of the package deliverable
- you expect it to build reliably on CRAN/CI

Prefer a pkgdown-only article when:

- the content is valuable, but too heavy or too environment-specific for check
- you want to avoid forcing users/CI to install expensive dependencies

See also: [vignettes-vs-articles.md](vignettes-vs-articles.md) and
[pkgdown-overview.md](pkgdown-overview.md).

## Common failure modes

- Vignette knits locally but fails on CI: missing declared dependency or hidden
  reliance on local files/paths.
- Vignette uses the “old” version of your code: it’s being built against an
  installed package; install or use a dev build loop.
- Vignette is too slow: move expensive work out of the vignette or convert to a
  pkgdown article.

Common error messages and what they usually mean:

- “there is no package called ‘X’”
  - add `X` to `Suggests` (or `Imports` if it’s runtime code)
  - ensure CI installs suggests (or gate the vignette/article appropriately)
- “cannot open the connection” / missing file
  - you relied on a local file path; make paths relative to the vignette or use
    package-installed files via `system.file()`
- “object ‘x’ not found” in a later chunk
  - chunk ordering or conditional execution differs; ensure all required setup
    happens in the vignette itself

## References

- R Packages (2e), “Vignettes”: https://r-pkgs.org/vignettes.html
- usethis: `use_vignette()`: https://usethis.r-lib.org/reference/use_vignette.html
- devtools: `build_rmd()`: https://devtools.r-lib.org/reference/build_rmd.html
