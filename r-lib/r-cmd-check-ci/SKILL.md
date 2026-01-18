---
name: r-lib/r-cmd-check-ci
description: >
  Running, interpreting, and fixing `R CMD check` locally and in continuous
  integration, with a focus on modern r-lib tooling and GitHub Actions.
  Use this skill when working with an R package that needs to:
  (1) Run `devtools::check()` and understand what it does,
  (2) Triage ERROR/WARNING/NOTE results and map them to concrete fixes,
  (3) Diagnose failures related to DESCRIPTION, dependencies, namespace, docs,
      tests, or vignettes,
  (4) Apply dependency best practices (Imports vs Suggests vs Depends) and
      correct usage patterns in code/examples/tests,
  (5) Set up CI with GitHub Actions, especially the `check-standard` workflow,
  (6) Debug “works locally but fails on CI/Windows/macOS” issues.
  Also use when installing check dependencies, handling suggested packages,
  or reviewing dependency weight with pak where appropriate.
---

# R CMD check and CI for R Packages

## When to Use What

| Task                                                 | Use                                                                         |
| ---------------------------------------------------- | --------------------------------------------------------------------------- |
| Run the full package check locally                   | `devtools::check()`                                                         |
| Iterate faster on documentation-related failures     | `devtools::check_man()`                                                     |
| Install/update package dependencies for checks       | `devtools::install_deps(dependencies = TRUE)`                               |
| Install dependencies with pak (alternative workflow) | `pak::local_install_deps()` / `pak::local_install_dev_deps()`               |
| Analyze dependency weight or chains                  | `pak::pkg_deps_tree()` / `pak::pkg_deps_explain()`                          |
| Decide Imports vs Suggests vs Depends                | Dependency mindset rules (see references)                                   |
| Use dependencies correctly in package code           | Default to `pkg::fun()`; use roxygen + `devtools::document()` for NAMESPACE |
| Configure CI for R CMD check on GitHub               | `usethis::use_github_action("check-standard")`                              |

## The Check Discipline

- Use `devtools::check()` early and often.
- Read the output; treat a clean check as a core quality bar.

## Triage: ERROR / WARNING / NOTE

1. Start with ERRORs.
2. Fix WARNINGs next (especially for CRAN-bound packages).
3. Read each NOTE; eliminate where possible or document rationale.

## Common Failure Buckets

- Package structure and stray files
- DESCRIPTION metadata and dependencies
- Namespace and imports/exports
- Documentation and examples
- Tests and snapshots
- Vignettes

(Use the appendix playbook reference for section-by-section detail.)

## Dependencies and NAMESPACE Practices

Key defaults:

- Declare dependencies in `DESCRIPTION` (usually `Imports` or `Suggests`).
- In package code under `R/`, default to `pkg::fun()` for external calls.
- Use roxygen comments + `devtools::document()` to generate `NAMESPACE`.

## CI with GitHub Actions (check-standard)

If you only configure one CI workflow, use `check-standard` to run `R CMD check`
across platforms.

## Resources & Advanced Topics

### Reference Files

- **[references/r-cmd-check-mental-model.md](references/r-cmd-check-mental-model.md)** - What check is and why `devtools::check()` is recommended
- **[references/r-cmd-check-appendix-playbook.md](references/r-cmd-check-appendix-playbook.md)** - Appendix-style breakdown of check phases and fixes
- **[references/check-docs-fast.md](references/check-docs-fast.md)** - Faster doc iteration with `check_man()`
- **[references/description-fields-that-affect-check.md](references/description-fields-that-affect-check.md)** - DESCRIPTION fields and check implications
- **[references/dependencies-mindset.md](references/dependencies-mindset.md)** - When to take dependencies and Imports/Suggests/Depends choices
- **[references/dependencies-in-practice.md](references/dependencies-in-practice.md)** - Using deps in R code/tests/examples/vignettes; NAMESPACE workflow
- **[references/r-lib-actions-and-check-standard.md](references/r-lib-actions-and-check-standard.md)** - `use_github_action()` and `check-standard`
- **[references/installing-check-deps.md](references/installing-check-deps.md)** - Installing deps; FORCE_SUGGESTS; devtools vs pak options

### External Resources

- R Packages (2e): Fundamental workflows (check): https://r-pkgs.org/workflow101.html
- R Packages (2e): Appendix A — R CMD check: https://r-pkgs.org/R-CMD-check.html
- R Packages (2e): DESCRIPTION: https://r-pkgs.org/description.html
- R Packages (2e): Dependencies (mindset): https://r-pkgs.org/dependencies-mindset-background.html
- R Packages (2e): Dependencies (in practice): https://r-pkgs.org/dependencies-in-practice.html
- R Packages (2e): CI with GitHub Actions: https://r-pkgs.org/software-development-practices.html
- r-lib/actions: https://github.com/r-lib/actions

### Related Skills

- [r-lib/package-development-workflow](../package-development-workflow/) - Where check/CI fits in the daily loop
- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/) - Documentation causes many check failures
- [r-lib/testing-r-packages](../testing-r-packages/) - Tests and snapshots in check/CI
