# Workflow 101: `devtools::check()`

## Table of Contents

1. [What `check()` Does](#what-check-does)
2. [How Often to Run It](#how-often-to-run-it)
3. [Interpreting Results](#interpreting-results)
4. [Fast Iteration Helpers](#fast-iteration-helpers)
5. [Common Failure Sources](#common-failure-sources)
6. [Reading check output (logs)](#reading-check-output-logs)
7. [A practical triage flow](#a-practical-triage-flow)
8. [Common messages → likely fixes](#common-messages--likely-fixes)
9. [Related pages](#related-pages)
10. [References](#references)

## What `check()` Does

`devtools::check()` runs `R CMD check` for your package and reports the results
in a developer-friendly way. Conceptually, it is your integration-quality gate:
it exercises package metadata, namespace, documentation, examples, tests, and
vignettes together.

Because `R CMD check` runs in a more controlled context than an interactive
session, it catches "works for me" problems early.

## How Often to Run It

- Run `check()` early (once you have a minimal working skeleton).
- Run `check()` regularly as you develop, especially before pushing changes or
  opening a PR.

A good working rhythm is:

- `devtools::load_all()` many times per hour
- `devtools::document()` whenever you change roxygen or exports
- `devtools::check()` at least once per work session (more for larger changes)

## Interpreting Results

`R CMD check` reports outcomes as:

- **ERROR**: must be fixed.
- **WARNING**: treat as serious, especially if you care about CRAN.
- **NOTE**: investigate; some are fine, but many are actionable.

Triage order:

1. Fix ERRORs.
2. Fix WARNINGs.
3. Review NOTEs; remove where possible or document rationale.

## Fast Iteration Helpers

When you are actively editing documentation or examples, you can often tighten
the loop:

- Use `devtools::check_man()` to focus on documentation-related checks.

Once those are clean, return to full `devtools::check()`.

## Common Failure Sources

These are recurring buckets that `check()` surfaces:

- **Documentation/examples**: examples are too slow, rely on missing packages, or
  leave global state changed.
- **NAMESPACE**: missing imports/exports due to stale `document()` results.
- **Dependencies**: packages used in code/tests/examples not declared correctly.
- **Platform differences**: line endings, file paths, encoding, timezone, locale.

For deeper triage patterns and CI guidance, see the `r-lib/r-cmd-check-ci` skill.

If you’re aiming for CRAN-level strictness locally, consider:

```r
devtools::check(args = "--as-cran")
```

## Reading check output (logs)

When check fails, don’t guess from the summary.
Open the log that contains the first meaningful error:

- `00check.log` (phase ordering)
- `00install.out` (build/install failures)
- `tests/testthat.Rout` (test failures)

If you’re using CI, those same logs exist inside the `.Rcheck` directory produced
by the workflow.

Practical habit: always locate the `.Rcheck` directory first.

- In local `devtools::check()`, devtools prints the check directory path.
- In CI, download artifacts (if configured) or read the log output.

Once you have the directory, identify the _first meaningful error_ in the most
relevant log file. Many failures cascade.

## A practical triage flow

1. Fix install/load failures first (they block everything else).
2. Fix docs/examples next (they often hide dependency and state issues).
3. Fix tests and vignettes next.
4. Work through NOTEs and remove as many as practical.

When something passes interactively but fails in check, trust check: it is the
closest thing you have to “portable package behavior”.

## Common messages → likely fixes

These are not exact rules, but they cover a large fraction of real failures.

### “there is no package called …”

Likely causes:

- The package is used but not declared in `DESCRIPTION`.
- The package is in `Suggests` but your code/examples/tests aren’t gated.

Fix:

- Declare the dependency (usually `Imports` for runtime, `Suggests` for tests/examples/vignettes).
- Use `pkg::fun()` in code.
- Use conditional patterns for optional deps.

### “object ‘x’ not found” in examples/tests

Likely causes:

- Example relies on objects from your global environment.
- Test relies on state from a previous test.

Fix:

- Make examples/tests self-contained.
- Restart R and re-run to confirm it’s not session leakage.

### “no visible binding for global variable”

Likely causes:

- Non-standard evaluation (common with dplyr/tidy evaluation).

Fix:

- Use the package-recommended pattern for registering globals (depends on the ecosystem).
- If it’s truly a false positive, document why and keep it stable.

### “non-standard file/directory found” NOTE

Likely causes:

- Extra files are included in the build.

Fix:

- Move files to `inst/` (if they belong in the package) or add to `.Rbuildignore`.

## Related pages

- [r-cmd-check-mental-model.md](../../r-cmd-check-ci/references/r-cmd-check-mental-model.md)
- [r-cmd-check-appendix-playbook.md](../../r-cmd-check-ci/references/r-cmd-check-appendix-playbook.md)

## References

- R Packages (2e), “Fundamental workflows”: https://r-pkgs.org/workflow101.html
- R Packages (2e), “R CMD check”: https://r-pkgs.org/R-CMD-check.html
- devtools reference: https://devtools.r-lib.org/reference/check.html
