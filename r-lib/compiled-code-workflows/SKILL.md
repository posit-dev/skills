---
name: r-lib/compiled-code-workflows
description: >
  Building and shipping R packages with compiled code (C/C++/Fortran), including
  Rcpp usage, toolchains, and external system dependencies.
  Use this skill when you need to:
  (1) Add or maintain code under `src/` and understand how it is built,
  (2) Manage compiler/linker flags via `Makevars` and/or `configure`,
  (3) Declare and document system dependencies (`SystemRequirements`),
  (4) Debug cross-platform and CI failures (especially Windows/macOS),
  (5) Keep compiled code safe under `R CMD check` and CRAN policy.
---

# Compiled Code Workflows

## When to Use What

| Task                                        | Use                                                        |
| ------------------------------------------- | ---------------------------------------------------------- |
| Add compiled code quickly (C++ integration) | `usethis::use_rcpp()` (if using Rcpp)                      |
| Check what fails in a clean build           | `devtools::check()` and CI (`check-standard`)              |
| Understand dependency boundaries            | `Imports`/`LinkingTo` vs `SystemRequirements`              |
| Tune compilation flags                      | `src/Makevars` / `src/Makevars.win`                        |
| Add a configure-time probe                  | `configure` + `configure.win` (only when necessary)        |
| Diagnose build failures                     | Reproduce from a clean session + read full compiler output |

## The reliable workflow

1. **Decide what you’re building against**

- Header-only dependency shipped as an R package → prefer `LinkingTo`.
- External system library (e.g., `libcurl`, `libxml2`, `gdal`) → document in `SystemRequirements` and use a portable detection strategy.

2. **Keep the package build boring**

- Prefer defaults and portable code.
- Treat warnings as errors in your own thinking, even if CRAN doesn’t.

3. **Make cross-platform behavior explicit**

- Use `src/Makevars` for Unix-like platforms.
- Use `src/Makevars.win` for Windows-specific flags.

4. **Add `configure` only if you must**

- `configure` makes builds more complex; only use it when you truly need to detect non-trivial system features.

5. **Reproduce failures in clean environments**

- A local interactive session hides toolchain and dependency problems.
- CI failures are usually real portability problems.

## High-frequency failure surfaces

- Missing toolchain (Windows Rtools, Xcode CLI tools)
- Missing headers / wrong include paths
- Linking errors (library not found, wrong ABI)
- Non-portable code paths or assumptions about filesystem layout
- Compiled code that terminates R (calls to `abort`, `exit`, `assert`, `std::terminate`)

## References

- [references/compiled-code-quality-gates.md](references/compiled-code-quality-gates.md)
- [references/src-layout-and-makevars.md](references/src-layout-and-makevars.md)
- [references/linkingto-and-systemrequirements.md](references/linkingto-and-systemrequirements.md)
- [references/configure-and-autoconf.md](references/configure-and-autoconf.md)
- [references/toolchains-and-ci.md](references/toolchains-and-ci.md)
- [references/troubleshooting-compiled-builds.md](references/troubleshooting-compiled-builds.md)

## Related skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/)
- [r-lib/cran-submission](../cran-submission/)
