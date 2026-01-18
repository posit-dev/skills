# Installing dependencies for checks

The goal is a reproducible “all deps installed” state so you can run
`devtools::check()` locally and CI can do the same.

If your check passes only “sometimes”, treat dependency installation as part of
the debugging process: rebuild the environment, then re-run check.

## Table of Contents

- [Install dependencies locally (devtools)](#install-dependencies-locally-devtools)
- [Install dependencies locally (pak)](#install-dependencies-locally-pak)
- [Which installer should you use?](#which-installer-should-you-use)
- [Suggested packages and `_R_CHECK_FORCE_SUGGESTS_`](#suggested-packages-and-_r_check_force_suggests_)
- [System dependencies](#system-dependencies)
- [CI strategy (GitHub Actions)](#ci-strategy-github-actions)
- [Clean-room reproduction recipe](#clean-room-reproduction-recipe)
- [A practical setup checklist](#a-practical-setup-checklist)
- [Related pages](#related-pages)
- [References](#references)

## Install dependencies locally (devtools)

For most workflows, devtools is the simplest:

```r
devtools::install_deps(dependencies = TRUE)
```

This aims to install:

- hard dependencies (`Depends`, `Imports`, `LinkingTo`)
- and, with `dependencies = TRUE`, also development dependencies like `Suggests`

If you are debugging a check failure, it often helps to reinstall dependencies
from a clean session to reduce “it worked yesterday” confusion.

## Install dependencies locally (pak)

pak is commonly used in CI and can be used locally too:

```r
pak::local_install_deps()
pak::local_install_dev_deps()
```

Use pak when you want fast, dependency-solver-based installs.

If you’re working on multiple packages, pak’s solver often produces more
predictable outcomes than iterative installs.

## Which installer should you use?

Both approaches can work.

- Use **devtools** when you want the simplest default and you’re already using
  devtools for the workflow.
- Use **pak** when you care about a solver-based install (often closer to CI)
  or you’re juggling multiple interdependent packages.

The important part is consistency: pick one, make it reproducible, and use it
to match CI.

## Suggested packages and `_R_CHECK_FORCE_SUGGESTS_`

During `R CMD check`, suggested packages are expected to be present unless you
explicitly relax that.

In devtools, you can relax this locally when a suggested package is hard to
install on your platform:

```r
devtools::check(force_suggests = FALSE)
```

This sets `_R_CHECK_FORCE_SUGGESTS_` to a false value for the check run.

Important: relaxing `force_suggests` is a development convenience, not a substitute
for correct conditional usage of suggested packages in code/examples/tests.

Decision rule:

- If suggested packages are required for your test/doc surface, keep `force_suggests = TRUE`
  and make sure CI installs them.
- If a suggested package is genuinely optional, gate its usage narrowly (feature boundary,
  specific tests) and skip conditionally.

If you find yourself routinely turning off `force_suggests`, that’s often a sign
you should either:

- move the suggested-package usage behind explicit feature-gating and document it
- or reconsider whether the dependency should be a hard dependency

Local-only escape hatch:

- You can use `force_suggests = FALSE` to make progress on a platform where a suggests
  package is hard to install.
- But before merging/releasing, validate in an environment where suggests are installed.

## System dependencies

Some R packages require OS-level system libraries (common for packages that
compile C/C++ code, use curl/ssl/xml, or link to geospatial tooling).

When dependency installation fails, distinguish:

- “R package not available / wrong version” (an R dependency problem)
- “system library missing” (an OS dependency problem)

On CI, r-lib/actions can help manage this (and pak can report system
requirements), but the exact solution is platform-specific.

When you hit a system dependency failure, capture:

- OS and version (Windows/macOS/Linux)
- R version
- The specific system library/tool mentioned

Then add the installation step to CI so it’s repeatable.

If you maintain a package that needs system libraries, treat this as part of the
“definition of done”: the CI workflow should install the system deps.

## CI strategy (GitHub Actions)

In CI (GitHub Actions), the r-lib/actions workflow typically installs dependencies
via `setup-r-dependencies@v2` and then runs `check-r-package@v2`.

If you have task-only dependencies (e.g. website), prefer recording them in
`DESCRIPTION` under `Config/Needs/*` and let CI install them via `needs:`.

Decision rule: keep your CI dependency install explicit.
If CI is green only because “something happened to be installed”, it will break later.

## Clean-room reproduction recipe

When CI fails but local passes, aim to make local look more like CI.

1. Restart R (so you’re not relying on your current session state).
2. Reinstall dependencies (choose one):

```r
devtools::install_deps(dependencies = TRUE)
```

or

```r
pak::local_install_deps()
```

3. Run a clean check:

```r
devtools::check()
```

4. If the failure is CRAN-policy-ish, also try:

```r
devtools::check(args = "--as-cran")
```

If the failure remains CI-only, suspect system deps, OS-specific paths/encoding,
or a missing suggested package.

## A practical setup checklist

When checks are failing due to missing dependencies, walk this list:

1. Confirm dependency is declared in `DESCRIPTION` (usually `Imports` for runtime,
   `Suggests` for tests/examples/vignettes).
2. Ensure usage is explicit (`pkg::fun()` or proper imports), not relying on
   attached packages.
3. Reinstall deps (`devtools::install_deps(dependencies = TRUE)` or pak).
4. Run `devtools::check()` (or `devtools::check(args = "--as-cran")` when relevant).
5. If CI-only failure: ensure system dependencies are installed in the workflow.

If the check fails with “package X not available”, the fastest fix is usually:

- add it to `Imports`/`Suggests` as appropriate
- make usage explicit (`pkg::fun()` or proper imports)
- reinstall deps
- re-run `check()`

## Related pages

- [dependencies-mindset.md](dependencies-mindset.md)
- [dependencies-in-practice.md](dependencies-in-practice.md)
- [r-lib-actions-and-check-standard.md](r-lib-actions-and-check-standard.md)

## References

- R Packages (2e), Appendix A — `R CMD check` (DESCRIPTION/deps): https://r-pkgs.org/R-CMD-check.html
- R Packages (2e), “Dependencies: In Practice”: https://r-pkgs.org/dependencies-in-practice.html
- devtools: `check()`: https://devtools.r-lib.org/reference/check.html
- devtools: `install()` / `install_deps()`: https://devtools.r-lib.org/reference/install.html
