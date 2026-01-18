---
name: r-lib/package-development-workflow
description: >
  Modern R package development workflow using the r-lib ecosystem (usethis/devtools)
  and the core edit → load → test-drive → document → check loop. Use this skill when
  working with an R package that needs to:
  (1) Create a new package with `usethis::create_package()` and select a good package name,
  (2) Set up Git and common project files (e.g., `.gitignore`, `.Rbuildignore`),
  (3) Iterate safely with `devtools::load_all()` instead of repeatedly installing,
  (4) Regenerate documentation and `NAMESPACE` with `devtools::document()`,
  (5) Run `devtools::check()` early and often and respond to failures,
  (6) Add README scaffolding and connect the repository to GitHub.
  Also use when adopting the devtools/usethis workflow in an existing package,
  standardizing day-to-day practices across a team, or diagnosing common workflow
  pitfalls (stale docs, wrong working directory, “works on my machine”).
---

# R Package Development Workflow

This skill is intentionally opinionated: it favors workflows that behave the same
locally, on CI, and on other developers’ machines.

If you’re debugging something that “works for me” but fails in check/CI, assume a
workflow discipline issue first (stale docs, hidden dependency, wrong working dir).

## When to Use What

| Task                                         | Use                                            |
| -------------------------------------------- | ---------------------------------------------- |
| Create a new R package                       | `usethis::create_package()`                    |
| Initialize Git for a package                 | `usethis::use_git()`                           |
| Add a new R source file                      | `usethis::use_r("topic")`                      |
| Test-drive functions without reinstalling    | `devtools::load_all()`                         |
| Run package tests                            | `devtools::test()`                             |
| Update `.Rd` docs and regenerate `NAMESPACE` | `devtools::document()`                         |
| Run a full package quality gate              | `devtools::check()`                            |
| Diagnose doc/example problems quickly        | `devtools::check_man()`                        |
| Add an executable README source              | `usethis::use_readme_rmd()`                    |
| Connect local repo to GitHub                 | `usethis::use_github()` (requires credentials) |

## Quick Start (New Package Checklist)

This checklist mirrors the canonical devtools/usethis workflow.

1. Create the package with `usethis::create_package()`.
2. Initialize Git with `usethis::use_git()`.
3. Create your first function file with `usethis::use_r()` and write a simple function.
4. Load the package for interactive iteration with `devtools::load_all()`.
5. Add roxygen comments and regenerate docs with `devtools::document()`.
6. Run `devtools::check()` and keep it clean as you develop.
7. Add `README.Rmd` with `usethis::use_readme_rmd()` and keep it rendered.
8. (Optional) Connect to GitHub with `usethis::use_github()`.

Practical “keep it green” habit:

- Commit early and often.
- Keep `devtools::check()` clean at all times (or at least at the end of every work session).

## The Daily Development Loop

The core loop:

1. Edit source code under `R/`.
2. Reload with `devtools::load_all()`.
3. Try a minimal example interactively.
4. Update docs + `NAMESPACE` as needed via `devtools::document()`.
5. Run `devtools::check()` regularly to catch issues early.

Notes:

- `load_all()` is the normal way to iterate during development; `library()` loads only an installed package.
- Running `check()` frequently is the most reliable way to avoid “big-bang” failure triage late in development.

Practical rhythm:

- Use `devtools::load_all()` constantly while coding.
- Use `devtools::document()` whenever you touch roxygen, imports/exports, or help topics.
- Use `devtools::test()` when a change should be protected.
- Use `devtools::check()` before pushing or opening a PR.

## A minimal interactive session pattern

When you’re test-driving a change, prefer an explicit sequence over “whatever is in my session”:

```r
devtools::load_all()

# Try the change
my_fun(1)

# If you touched roxygen/imports/exports
devtools::document()

# If you touched behavior
devtools::test()
```

Then run `devtools::check()` before you consider the change done.

## Common “mystery failures” and what they usually mean

### Docs are out of date / CI fails on NAMESPACE

- You changed roxygen tags or imports/exports but didn’t run `devtools::document()`.
- You committed code changes without committing the regenerated `NAMESPACE`/`man/*.Rd`.

Fix: run `devtools::document()` and commit the generated diffs.

### Tests pass locally but fail on CI

Common causes:

- Hidden dependency (you have the package installed locally, CI doesn’t).
- Files/paths outside the package.
- Global state leakage (options/env vars/working directory).

Fix: make tests self-sufficient; see [r-lib/testing-r-packages](../testing-r-packages/) and the dependency guidance in [r-lib/r-cmd-check-ci](../r-cmd-check-ci/).

### “It works in load_all() but fails in check()”

That’s expected when check is exercising install/load/unload behavior.

Fix: trust `devtools::check()`; reproduce and fix the underlying portability/dependency issue.

## Project Discipline (Working Directory and Paths)

- Prefer running R with the package root as the working directory.
- Avoid workflows that require changing the working directory frequently.
- Prefer package-aware path helpers in tests and vignettes (see references).

## Git and GitHub for Packages

Adopt Git early so you can:

- Review diffs as your package evolves.
- Collaborate via pull requests.
- Distribute development versions via GitHub.
- Integrate with GitHub Actions and pkgdown later.

## Resources & Advanced Topics

### Reference Files

- **[references/the-whole-game.md](references/the-whole-game.md)** - End-to-end walkthrough of the devtools/usethis workflow
- **[references/workflow101-create-package.md](references/workflow101-create-package.md)** - Package creation, naming, and where to create a package
- **[references/workflow101-rstudio-projects.md](references/workflow101-rstudio-projects.md)** - RStudio Project support for packages
- **[references/workflow101-path-discipline.md](references/workflow101-path-discipline.md)** - Working directory and path discipline guidelines
- **[references/workflow101-load-all.md](references/workflow101-load-all.md)** - Why `load_all()` is central and how to use it
- **[references/workflow101-check.md](references/workflow101-check.md)** - What `devtools::check()` does and how to use it
- **[references/usethis-scaffolding-playbook.md](references/usethis-scaffolding-playbook.md)** - Which `use_*()` helpers to call once vs often
- **[references/git-github-for-packages.md](references/git-github-for-packages.md)** - Git/GitHub practices for R package development

### External Resources

- R Packages (2e): The Whole Game: https://r-pkgs.org/whole-game.html
- R Packages (2e): Fundamental workflows: https://r-pkgs.org/workflow101.html
- usethis reference index: https://usethis.r-lib.org/reference/index.html
- devtools reference index: https://devtools.r-lib.org/reference/index.html

### Related Skills

- [r-lib/testing-r-packages](../testing-r-packages/) - Unit testing best practices and advanced techniques
- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/) - Documentation workflows and pkgdown
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - Interpreting check results and configuring CI
