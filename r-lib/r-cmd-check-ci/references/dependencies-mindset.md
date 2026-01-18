# Dependency mindset (Imports vs Suggests vs Depends)

This reference helps you decide:

- When to take a dependency at all.
- Whether it belongs in `Imports`, `Suggests`, or (rarely) `Depends`.
- How to think about dependency _cost_, not just dependency _count_.

## Table of Contents

- [Dependencies are not equal](#dependencies-are-not-equal)
- [Practical decision rules](#practical-decision-rules)
- [A quick classification table](#a-quick-classification-table)
- [Optional dependencies (feature-gating)](#optional-dependencies-feature-gating)
- [Version constraints (including minimum R)](#version-constraints-including-minimum-r)
- [Anti-patterns to avoid](#anti-patterns-to-avoid)
- [A dependency cost checklist](#a-dependency-cost-checklist)
- [Development-only dependencies (Config/Needs)](#development-only-dependencies-configneeds)
- [Related pages](#related-pages)
- [References](#references)

## Dependencies are not equal

R Packages (2e) emphasizes that dependencies differ materially in:

- Installation burden (system requirements, compile time, binary size).
- Recursive dependency footprint.
- Stability/maintenance capacity.
- Whether it’s “almost always present” (base/recommended) vs third-party.

So “minimize number of deps” is usually the wrong objective.

Better objective: take dependencies deliberately, and make optionality explicit.

## Practical decision rules

### Use `Imports` when

- Your package needs the dependency to work at runtime.
- You call functions from that package inside functions under `R/`.

Remember: putting a package in `Imports` ensures it is installed. It does _not_
automatically make its functions available to you.

Recommended default usage in code:

- Prefer `pkg::fun()` in package code and tests.
- Import only what you need (typically via roxygen `@importFrom`) when `::` can’t
  be used or when imports materially improve readability.

### Use `Suggests` when

- The dependency is optional (feature gates).
- The dependency is only used for tests, examples, vignettes, or development tasks.
- The dependency is hard to install on some platforms and you want a reasonable
  base installation experience.

If the package is in `Suggests`, you generally still design your automated
checks to install it. `Suggests` is about optionality at runtime, not “don’t ever
install this”.

In other words:

- `Suggests` is compatible with “installed on CI”.
- `Suggests` is not a strategy for avoiding dependency declarations.

### Use `Depends` sparingly

`Depends` causes the dependency to be attached when your package is attached.
This increases the chance of search-path conflicts and makes code harder to reason about.
Reserve it for special cases where the dependency is a fundamental extension point.

If you are unsure: do not use `Depends`.

`Depends` is usually the wrong tool for:

- making functions available without `pkg::fun()` (prefer explicit calls or imports)
- depending on “convenience” meta-packages

## A quick classification table

Use this when you’re unsure where a dependency belongs.

| You use the dependency for…             | Put it in…       | Notes                                        |
| --------------------------------------- | ---------------- | -------------------------------------------- |
| runtime code under `R/`                 | `Imports`        | Prefer `pkg::fun()`; import only when needed |
| tests under `tests/testthat/`           | `Suggests`       | keep skips narrow; don’t skip whole suite    |
| examples / vignettes                    | `Suggests`       | still needs to be check-friendly             |
| compilation headers                     | `LinkingTo`      | plus `Imports` if used at runtime            |
| tool-only tasks (website/coverage/lint) | `Config/Needs/*` | installed only in relevant CI jobs           |

Where `Depends` fits: only when you deliberately want the dependency attached when
your package is attached (rare).

## Optional dependencies (feature-gating)

When a dependency is truly optional, design for a clear “feature missing” path.

Patterns that scale:

- Gate optional features at runtime with a small check at the boundary (inside
  the function that needs it), and give a helpful error message.
- Keep the dependency explicit in examples (`pkg::fun()`) and declare it in
  `Suggests` if examples/vignettes/tests use it.

Avoid:

- Putting `library(optionalpkg)` inside your package functions.
- Making the entire package behavior depend on what happens to be installed on
  the developer’s machine.

Recommended shape for optional features:

- Put the dependency check at the feature boundary (inside the function that needs it).
- Fail with a helpful error message that tells the user how to install the package.
- Keep the rest of the package usable without the optional dependency.

If the optional dependency is used in examples/tests/vignettes, declare it in
`Suggests` so CI can install it and your docs remain reproducible.

## Version constraints (including minimum R)

Version constraints are part of dependency cost.

Rules of thumb:

- Only add a version constraint when you need a feature/bugfix.
- Prefer the smallest minimum version that supports your needs.
- If you require a minimum R version (e.g. `Depends: R (>= 4.1)`), make sure you
  actually rely on it; increasing minimum R can exclude users.

When you bump a minimum version, consider:

- CI matrix: do you still test the minimum you claim?
- downstream impact: does this break users or reverse dependencies?

## A dependency cost checklist

Before adding a dependency, ask:

- Does it bring system requirements (C libraries, compilers, external tooling)?
- Is it heavy recursively (large dependency graph)?
- Does it change check behavior (vignette/documentation tooling, test helpers)?
- Is it stable and maintained?
- Do you need it at runtime, or only for development tasks?

If it’s development-only, don’t inflate your runtime surface.

## Development-only dependencies (`Config/Needs`)

Some packages are useful for _tasks_ (pkgdown site builds, coverage, linting) but
are not appropriate as runtime dependencies.

A scalable pattern is:

- Record task-only deps in `DESCRIPTION` under `Config/Needs/*`, for example:
  - `Config/Needs/website: pkgdown, downlit`
  - `Config/Needs/coverage: covr`
- Configure CI to install those needs only in the relevant workflow.

This keeps `Imports` focused on runtime needs, while keeping CI reproducible.

## Anti-patterns to avoid

- Depending on meta-packages like `tidyverse` or `devtools` in `Imports`.
  Prefer depending on the specific packages that provide the functionality.

- Using `Suggests` to “hide” required runtime dependencies.
- Importing whole namespaces by default (`@import pkg`) when targeted imports
  are sufficient.

- Using `Depends` as a shortcut to avoid explicit dependency usage.
- Adding a dependency “because it’s convenient” when base R is sufficient.

## Related pages

- [dependencies-in-practice.md](dependencies-in-practice.md)
- [installing-check-deps.md](installing-check-deps.md)
- [description-fields-that-affect-check.md](description-fields-that-affect-check.md)

## References

- R Packages (2e), “Dependencies: Mindset and Background”: https://r-pkgs.org/dependencies-mindset-background.html
- R Packages (2e), “Dependencies: In Practice”: https://r-pkgs.org/dependencies-in-practice.html
