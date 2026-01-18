# CRAN submission checklist

This is a practical checklist you can use as a release gate.

## 1) Local quality gate

- `devtools::check()` is clean.
- `devtools::check(args = "--as-cran")` is clean.
- Prefer a tarball check at least once per submission:

  - `R CMD build` (from a clean checkout)
  - `R CMD check --as-cran pkg_x.y.z.tar.gz`

- If check is not clean, fix the root cause (don’t paper over).

## 2) Dependencies and clean-session behavior

- Package code (`R/`) does not rely on packages that are only in `Suggests`.
- Examples and vignettes either:
  - only use packages in `Imports`, or
  - are guarded so they don’t run without the suggested package.

Common guard patterns:

- Use conditional examples (roxygen2) when a suggested package is required.
- For vignettes, ensure suggested packages are declared and installed in the check environment.

## 3) Examples, tests, vignettes

- Examples:
  - avoid network access
  - avoid writing outside temp dirs
  - keep runtime reasonable
- Tests:
  - do not depend on your personal library state
  - clean up files/options/env vars
- Vignettes:
  - build reliably in a clean library
  - avoid huge intermediate artifacts

If examples/vignettes need optional packages:

- add them to `Suggests`
- use conditional code paths (`requireNamespace()` guards)
- ensure vignettes build in CI / clean environments

## 4) DESCRIPTION and metadata

- `Title` is in title case; `Description` is a real paragraph (not a fragment).
- `URL` and `BugReports` are correct.
- License fields are correct and included files (if any) are present.
- Authors/maintainers are correct.

If you changed licensing or the maintainer email, highlight this in the submission.

## 5) `cran-comments.md`

Include:

- Summary of changes since last release
- Check environments you used (OS/R versions; local/CI)
- Any NOTE and why it is safe
- Responses to any CRAN reviewer feedback (for resubmissions)

Keep it plain text and factual.

## 6) Pre-submit “incoming checks” sanity

- Read the first real failure in `.Rcheck` logs (avoid cascades).
- Assume CRAN will see a clean, minimal environment.
- If you can’t reproduce locally, run checks in a fresh environment (e.g., CI, a new library, or a container).

## 7) Platform preflight (recommended)

- Use GitHub Actions to check Linux/macOS/Windows where possible.
- If you don’t have access to Windows/macOS locally, use hosted services:
  - win-builder: https://win-builder.r-project.org/
  - macbuilder: https://mac.r-project.org/macbuilder/submit.html

CRAN also recommends checking with a current R-devel build when feasible.
