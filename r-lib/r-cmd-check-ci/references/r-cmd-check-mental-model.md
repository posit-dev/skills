# R CMD check: a practical mental model

This reference explains what `R CMD check` is validating, why it catches “works
on my machine”, and how to read the output in a way that gets you to a fix
quickly.

## Table of Contents

- [What `devtools::check()` does](#what-devtoolscheck-does)
- [What `R CMD check` is testing](#what-r-cmd-check-is-testing)
- [The check pipeline (build → install → validate)](#the-check-pipeline-build--install--validate)
- [Where the real error lives (logs)](#where-the-real-error-lives-logs)
- [Why failures differ from interactive runs](#why-failures-differ-from-interactive-runs)
- [A reliable triage order](#a-reliable-triage-order)
- [How to reproduce a CI failure locally](#how-to-reproduce-a-ci-failure-locally)
- [Fast inner loops (docs, tests, deps)](#fast-inner-loops-docs-tests-deps)
- [Common check outcomes (and what they usually mean)](#common-check-outcomes-and-what-they-usually-mean)
- [Related pages](#related-pages)
- [References](#references)

## What `devtools::check()` does

`devtools::check()` is the recommended way to run `R CMD check` during development.
It deliberately checks a _built source package_ in a clean-ish environment.

At a high level:

1. Optionally regenerates docs (see `document` argument in the devtools docs).
2. Builds a source package.
3. Runs `R CMD check` in a separate R session.
4. Collects ERROR/WARNING/NOTE results.

Key implications:

- Your global environment objects are irrelevant.
- Your interactive search path is irrelevant.
- “It worked after `devtools::load_all()`” is not evidence it will pass check.

## What `R CMD check` is testing

Think of `R CMD check` as an integration test across multiple surfaces:

- Package structure and build process (`R CMD build`, `R CMD INSTALL`).
- `DESCRIPTION` validity, dependency declarations, and minimum versions.
- Namespace correctness: exports, imports, load/unload behavior.
- R code analysis (including missing dependencies, suspicious usage patterns).
- Documentation: Rd syntax, xrefs, examples, and manual build.
- Tests and vignettes in a fresh session.

This is why check tends to catch:

- Missing packages that you happened to have installed locally.
- Missing imports you “got away with” because something was attached.
- Files and paths that work on your OS but not Windows/macOS.
- State leakage (options/env vars/working directory) that only appears in clean runs.

## The check pipeline (build → install → validate)

It’s useful to think of check as a pipeline where each stage can fail for
different reasons:

1. **Build** a source package (what would be submitted/distributed).
2. **Install** that package into a temporary library.
3. **Load/unload** the namespace in a clean session.
4. **Validate** surfaces: DESCRIPTION, NAMESPACE, Rd, examples, tests, vignettes.

This pipeline model explains why “my function works interactively” is not the
same claim as “my package installs and checks cleanly”. Check is mostly about
**package correctness**, not “does one function run in my current session”.

## Where the real error lives (logs)

The headline output in the console is often not the most actionable part.
When something fails, locate the `.Rcheck` directory and open the relevant log:

- `00check.log` (overall orchestration)
- `00install.out` / `00pkg_src` logs (install/build failures)
- `tests/testthat.Rout` (test failures)
- vignette build logs under `vignettes/`-related outputs

Quick map (most common):

- Fails before “checking installed package” → look at `00install.out`.
- Mentions “Rd cross-references” / “running examples” → Documentation phase logs.
- Mentions “Running ‘testthat.R’” → `tests/testthat.Rout`.
- Mentions “building vignettes” → vignette logs (and confirm vignette deps).

If you’re using `devtools::check()`, it prints the check directory path near the top.

If you want a “message → fix” map, see `r-cmd-check-appendix-playbook.md`.

If you’re debugging a CI failure, your goal is to find the _first_ meaningful
error line in the corresponding log (the rest is often cascading).

## Why failures differ from interactive runs

Many checks run with `R_DEFAULT_PACKAGES=NULL`, which means common packages
that are usually attached (like stats, utils, methods) are not attached.
This exposes code that incorrectly assumes packages are on the search path.

Your package should:

- Use `pkg::fun()` (or explicit imports) for dependencies.
- Avoid `library()`/`require()` in package code under `R/`.

Also remember: check often runs with different locale/timezone/encoding than
your dev machine, and Windows path semantics can surface latent assumptions.

## A reliable triage order

1. Fix **ERROR**.
2. Fix **WARNING** (treat as release-blocking if CRAN-bound).
3. Work through **NOTE** (prefer eliminating, or have a clear rationale).

Within a single category, start with failures that prevent installation.

## How to reproduce a CI failure locally

Reproducing locally is the fastest way to fix CI problems without guessing.

1. **Run a clean check**:

```r
devtools::check()
```

2. If the failure is CRAN-policy-ish (notes/warnings, incoming checks), try:

```r
devtools::check(args = "--as-cran")
```

3. If the failure is “package X missing” or “works on my machine”, ensure your
   dependency state resembles CI:

- reinstall deps: `devtools::install_deps(dependencies = TRUE)`
- avoid relying on attached packages in your dev session

4. If the CI log shows it fails only on Windows/macOS:

- look for paths/encoding/line-ending assumptions
- confirm you’re not reading files that are outside the package

5. When the failure is in docs/examples, tighten the loop with
   `devtools::check_man()` (see [check-docs-fast.md](check-docs-fast.md)).

If CI fails only on one OS:

- Windows-only: suspect path handling, line endings, encoding, and file locks.
- macOS-only: suspect system libraries and locale differences.
- Linux-only: suspect system libraries and missing system deps.

## Fast inner loops (docs, tests, deps)

Use the smallest tool that exercises the failing surface:

- **Docs/examples**: `devtools::check_man()`
- **Tests**: `devtools::test()` (and reproduce the specific failing file)
- **Deps**: re-run dependency installation (devtools or pak), then re-check

Decision rule: if the failure prevents install/load, you can’t meaningfully debug
docs/tests yet. Fix install/load first.

The rule: always return to `devtools::check()` before you call it “fixed”.

## Common check outcomes (and what they usually mean)

- **Installation failure**: missing system dependency, compilation toolchain,
  or a DESCRIPTION/NAMESPACE issue.
- **Namespace/load failure**: missing imports, bad `.onLoad()` behavior, relying
  on attached packages.
- **Example failure**: undeclared dependency, side effects not restored, network
  call, or a slow example.
- **Test failure**: hidden global state, ordering dependence, file path issues.
- **NOTE about “non-standard files”**: extra files in the package bundle; move
  to `inst/`, ignore via `.Rbuildignore`, or delete.

If you see “it works locally but not in CI”, your default suspects should be:

- a missing declared dependency (present locally)
- a system dependency not installed on the runner
- a file/path assumption
- reliance on interactive session state

## Related pages

- [r-cmd-check-appendix-playbook.md](r-cmd-check-appendix-playbook.md)
- [installing-check-deps.md](installing-check-deps.md)
- [dependencies-in-practice.md](dependencies-in-practice.md)
- [description-fields-that-affect-check.md](description-fields-that-affect-check.md)

## References

- R Packages (2e), Appendix A — `R CMD check`: https://r-pkgs.org/R-CMD-check.html
- devtools: `check()`: https://devtools.r-lib.org/reference/check.html
