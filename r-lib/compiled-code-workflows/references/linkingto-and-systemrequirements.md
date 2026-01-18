# `LinkingTo` and `SystemRequirements`

This reference explains the dependency split you must get right for compiled code.

## The three common cases

### 1) Pure R dependency

- Add the package to `Imports`/`Depends`/`Suggests`.
- Use `pkg::fun()` in R code.

### 2) Header-only / vendored C/C++ dependency shipped as an R package

- Add the provider package to `LinkingTo`.
- Include its headers in your C/C++ sources.

This is the most portable way to depend on C/C++ code in CRAN packages because the dependency is resolved through R’s package system.

### 3) External system dependency

- Document it in `SystemRequirements`.
- Add platform-specific install instructions (README, pkgdown article).
- Use a robust strategy for include/link flags.

CRAN policy expects packages to be of minimum necessary size, and it has explicit guidance on external libraries (including preferring to use already-installed libraries, and using fixed-version downloads only as a last resort).

## Practical guidance

- Keep `SystemRequirements` user-facing (“Needs libxml2 development headers”).
- In code and build scripts, avoid fragile assumptions about paths.

## References

- CRAN policy: https://cran.r-project.org/web/packages/policies.html
