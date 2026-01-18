# DESCRIPTION fields that affect check

This is a practical list of `DESCRIPTION` fields that commonly cause
`R CMD check` problems, with notes on why they matter.

## Table of Contents

- [Metadata fields that are strictly validated](#metadata-fields-that-are-strictly-validated)
- [High-frequency field cheat sheet](#high-frequency-field-cheat-sheet)
- [Dependency fields](#dependency-fields)
- [Build and check integration fields](#build-and-check-integration-fields)
- [Tooling and conventions](#tooling-and-conventions)
- [Fields that influence CRAN review norms](#fields-that-influence-cran-review-norms)
- [Quick triage: error message → likely field](#quick-triage-error-message--likely-field)
- [References](#references)

## Metadata fields that are strictly validated

- `Package`, `Version`: must be valid; version must increase for CRAN updates.
- `Title`, `Description`: checked for common CRAN style issues.
- `License`: must be a recognized license string or `file LICENSE`.
- `Encoding`: required when using non-ASCII; UTF-8 is the common recommendation.
- `Type`: almost always `Package`.
- `Authors@R`: increasingly preferred over legacy `Author`/`Maintainer`; must parse.

Other fields that are frequently implicated in check or review:

- `Language`: relevant if you use translations.
- `Collate`: only if you rely on source file ordering (avoid if possible).
- `ByteCompile`: can change warning surfacing; usually leave default.

When in doubt, validate these fields first: they can cause “fail fast” errors
before check gets to the rest of your package.

Formatting rule (often the real problem):

- Each field is `Name: value`.
- Continuation lines must be indented by at least one space.

If you see “cannot open compressed file 'DESCRIPTION'” or parsing failures, check
for malformed formatting (missing colon, bad indentation, or stray tabs).

## High-frequency field cheat sheet

This is the short list of fields that show up most often in practical failures.

- `Authors@R`: must parse; use `person()` objects.
- `Depends` / `Imports` / `Suggests`: must match how you use packages.
- `Encoding: UTF-8`: required when non-ASCII appears.
- `Roxygen` / `RoxygenNote`: roxygen2-managed; don’t hand-edit `RoxygenNote`.
- `VignetteBuilder`: required when you ship vignettes.
- `URL` / `BugReports`: rarely break check, but often become CRAN notes if missing or invalid.
- `Config/Needs/*`: keeps task-only deps reproducible (website, coverage, lint).

## Dependency fields

- `Depends`, `Imports`, `Suggests`, `LinkingTo`: determine what must be installed.
- Version requirements are enforced for hard deps.

Key check rule:

- Any package referenced in `NAMESPACE` must also appear in `Imports` or `Depends`.

Practical rule: a dependency can be “mentioned” in many places, and you need to
declare it in the right place:

- used in runtime code (`R/`) → `Imports`
- used only in tests/examples/vignettes → `Suggests`
- used only for website/coverage tooling → `Config/Needs/*`

Practical rule of thumb:

- Put packages you call in functions (at runtime) in `Imports`.
- Put packages you use only in examples/tests/vignettes in `Suggests`.

Version constraints: only add `pkg (>= x.y.z)` when you need a feature/bugfix.
Unnecessary version constraints increase the chance of install failures.

Related reference pages:

- [dependencies-mindset.md](dependencies-mindset.md)
- [dependencies-in-practice.md](dependencies-in-practice.md)
- [installing-check-deps.md](installing-check-deps.md)

## Build and check integration fields

- `VignetteBuilder`: required when you ship vignettes.
- `SystemRequirements`: doesn’t directly affect check mechanics, but becomes
  relevant when installation depends on external system libraries/tooling.

If vignettes fail to build in CI but work locally, check:

- the vignette dependencies are declared (often in `Suggests`)
- CI is actually installing suggests (it usually should)
- the vignette isn’t relying on local files/network

If you have compiled code:

- `LinkingTo`: header-only dependencies for compilation.
- `NeedsCompilation`: informational, but check/install will reflect compiled code requirements.

Other build-related fields you may encounter:

- `LazyData`: affects how data objects are stored/loaded; can surface size/encoding
  problems.
- `ByteCompile`: can change warning/error surfacing (rarely needed in modern packages).
- `NeedsCompilation`: mainly informational but can affect user expectations.

## Tooling and conventions

- `Roxygen`: often `list(markdown = TRUE)` for roxygen2 markdown.
- `RoxygenNote`: maintained by roxygen2; don’t hand-edit.
- `Config/testthat/edition`: used by testthat 3+ to select edition behavior.

Useful conventions:

- `Config/Needs/website`: pkgdown + site tooling dependencies
- `Config/Needs/coverage`: covr
- `Config/Needs/lint`: lintr

These keep runtime dependencies lean while making CI reproducible.

If you use pkgdown/CI conventions:

- `Config/Needs/*`: task-only dependency groups (e.g. website, coverage, lint).
- `Config/Needs/website`: commonly used to keep pkgdown deps out of core deps.

Other commonly-used conventions:

- `URL`, `BugReports`: not required for check success, but strongly recommended.
- `Config/Needs/*`: commonly used with r-lib/actions to install task-specific deps
  (e.g. `Config/Needs/website`).

## Fields that influence CRAN review norms

These don’t always fail check, but they affect how smooth CRAN submission tends to be:

- `URL`, `BugReports`: provide a clear home and issue tracker.
- `Description`: avoid boilerplate and ensure it reads as a real description of the package.
- `License`: ensure it matches your repository LICENSE file and contents.

URL fields are a common source of NOTES:

- Use `https://`.
- Multiple URLs should be comma-separated (common convention: `URL: https://a, https://b`).
- Fix redirects and dead links; CRAN checks URLs.

## Quick triage: error message → likely field

- “_Package required but not available_” during examples/tests/vignettes: often a
  missing entry in `Suggests`.
- “_Namespace dependency not required_” / imports mismatch: `NAMESPACE` references
  a package not listed in `Imports`/`Depends`.
- Vignette build failures: confirm `VignetteBuilder`, and that vignette-only deps
  are declared (often in `Suggests`).
- System dependency failures (e.g. `libcurl`, `openssl`): document in
  `SystemRequirements` and ensure CI installs system libs.

Other common mappings:

- “_Malformed package name_” / “_Invalid Version_”: `Package` / `Version`.
- “_Non-ASCII characters in …_”: `Encoding` (and file contents).
- “_cannot open compressed file 'DESCRIPTION'_” / parsing failures: malformed field formatting.

More common mappings:

- “Invalid 'Authors@R' field” / parse error: malformed `Authors@R` syntax.
- “URL … invalid” / “possibly invalid URLs”: `URL` / `BugReports` formatting or dead links.
- “Non-standard file/directory found at top level”: often a build-ignore issue
  (not a DESCRIPTION field), but review `.Rbuildignore`.

## References

- R Packages (2e), “DESCRIPTION”: https://r-pkgs.org/description.html
- R Packages (2e), Appendix A — `R CMD check` (DESCRIPTION section): https://r-pkgs.org/R-CMD-check.html
