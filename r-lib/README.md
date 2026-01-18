# R Package Development Skills

Skills for R package developers working with the r-lib ecosystem and modern R package development workflows.

## Available Skills

- **[cli](./cli/)** - Command-line interface styling, semantic messaging, progress reporting, and inline markup for user-facing R output.
- **[testing-r-packages](./testing-r-packages/)** - Best practices for writing R package tests using testthat 3+ (structure, expectations, fixtures, snapshots, mocking).
- **[package-development-workflow](./package-development-workflow/)** - The modern edit → load → test-drive → document → check workflow using usethis/devtools.
- **[documentation-roxygen2-pkgdown](./documentation-roxygen2-pkgdown/)** - R package documentation workflows with roxygen2 and pkgdown (examples policy, vignettes vs articles, package-level docs).
- **[r-cmd-check-ci](./r-cmd-check-ci/)** - A practical playbook for `R CMD check` triage and CI with GitHub Actions (r-lib/actions).
- **[compiled-code-workflows](./compiled-code-workflows/)** - Building and shipping packages with compiled code (C/C++/Fortran), including Rcpp usage, toolchains, and external system dependencies.
- **[cran-submission](./cran-submission/)** - Preparing a package for CRAN submission (check-as-CRAN discipline, common gotchas, `cran-comments.md`).
- **[large-data-package-size](./large-data-package-size/)** - Handling large files and data in packages (`inst/extdata`, `data-raw/`, caching) and keeping package size within CRAN expectations.
- **[revdep-checks](./revdep-checks/)** - Running reverse dependency checks prior to release and interpreting downstream failures.
- **[performance-profiling](./performance-profiling/)** - Profiling and benchmarking package code to improve runtime and memory use.
- **[code-coverage-ci](./code-coverage-ci/)** - Measuring test coverage with covr and integrating coverage runs into GitHub Actions.
- **[release-versioning-news](./release-versioning-news/)** - Version bumps and `NEWS.md` workflow for predictable releases.
- **[pkgdown-site-craft](./pkgdown-site-craft/)** - Configuring, curating, and deploying pkgdown sites (reference index, navigation, GitHub Pages).

## Where to Go Next

Pick the skill that matches what you’re trying to do:

- Starting (or standardizing) day-to-day package work → **[package-development-workflow](./package-development-workflow/)**
- A check or CI run failed and you need to triage it → **[r-cmd-check-ci](./r-cmd-check-ci/)**
- You’re preparing a CRAN submission or responding to CRAN feedback → **[cran-submission](./cran-submission/)**
- You’re about to release and need version + NEWS discipline → **[release-versioning-news](./release-versioning-news/)**
- You need revdep evidence for release/CRAN risk management → **[revdep-checks](./revdep-checks/)**
- You want to understand/improve test coverage or add a coverage workflow → **[code-coverage-ci](./code-coverage-ci/)**
- You’re writing docs/examples/vignettes or debugging doc-related check failures → **[documentation-roxygen2-pkgdown](./documentation-roxygen2-pkgdown/)**
- You’re curating/deploying a pkgdown site (nav, reference index, GitHub Pages) → **[pkgdown-site-craft](./pkgdown-site-craft/)**
- You’re chasing runtime/memory performance regressions → **[performance-profiling](./performance-profiling/)**
- You’re improving test structure, snapshots, fixtures, or mocking → **[testing-r-packages](./testing-r-packages/)**
- You’re making user-facing CLI output nicer (messages, progress, styling) → **[cli](./cli/)**
- You’re adding compiled code (Rcpp/C/C++/Fortran) or debugging platform toolchains → **[compiled-code-workflows](./compiled-code-workflows/)**
- Your package is too big, needs `inst/extdata`, or needs caching/optional downloads → **[large-data-package-size](./large-data-package-size/)**

## Overview

These skills focus on the “r-lib way” of building packages:

- Tight feedback loops (`devtools::load_all()`, `devtools::document()`, `devtools::check()`)
- Explicit dependencies and predictable behavior in clean sessions
- Documentation and tests that are runnable under `R CMD check`
- CI that confirms local discipline (not a surprise discovery tool)

## Potential Skills

This category could also include future skills for:

- Bioconductor submission workflows
- Internationalization and translations (i18n)

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new skills to this category. We encourage you to use [Anthropic's skill-creator](https://github.com/anthropics/skills) when building new skills.
