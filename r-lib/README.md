# R Package Development Skills

Skills for R package developers working with the r-lib ecosystem and modern R package development workflows.

## Available Skills

### `testing-r-packages`

Best practices for writing R package tests using testthat version 3+. Use when writing or modifying tests for R packages, organizing test files and fixtures, creating snapshot tests, mocking external dependencies, or following BDD patterns with describe/it.

**Organization**: Uses progressive disclosure with reference files. Core workflows load automatically from SKILL.md, while specialized topics (BDD, snapshots, mocking, fixtures, advanced topics) load only when needed from the `references/` directory.

**Resources**: This skill synthesizes guidance from:
- [R Packages: Testing Basics](https://r-pkgs.org/testing-basics.html)
- [R Packages: Testing Design](https://r-pkgs.org/testing-design.html)
- [R Packages: Testing Advanced](https://r-pkgs.org/testing-advanced.html)
- [testthat 3.0.0 release notes](https://tidyverse.org/blog/2020/10/testthat-3-0-0/)
- [testthat 3.1 release notes](https://tidyverse.org/blog/2021/10/testthat-3-1/)
- [testthat 3.2.0 release notes](https://tidyverse.org/blog/2023/10/testthat-3-2-0/)
- [testthat 3.3.0 release notes](https://tidyverse.org/blog/2025/11/testthat-3-3-0/)
- testthat package documentation

### `cli`

Comprehensive guidance for using the cli R package for command-line interface styling, semantic messaging, and user communication. Use when formatting console output with inline markup, displaying errors/warnings/messages with `cli_abort()`/`cli_warn()`/`cli_inform()`, showing progress indicators, creating semantic CLI elements, applying themes, handling pluralization, or working with ANSI strings and hyperlinks.

**Organization**: Uses progressive disclosure with reference files. Core workflows and inline markup patterns load from SKILL.md, while specialized topics (progress indicators, theming, advanced features, pluralization) load only when needed from the `references/` directory.

**Resources**: This skill synthesizes guidance from:
- [cli package documentation](https://cli.r-lib.org/)
- cli vignettes and function reference

### `cran-extrachecks`

Prepare R packages for CRAN submission by checking for common ad-hoc requirements not caught by `devtools::check()`. Use when preparing a package for first CRAN release, preparing updates for resubmission, reviewing packages for CRAN compliance, or responding to CRAN reviewer feedback.

**Organization**: Single comprehensive SKILL.md file combining standard checklist with detailed guidance. Covers documentation requirements (`@return`, `@examples`), DESCRIPTION field standards (Title/Description formatting, quoting conventions), URL validation, suggested package handling, and administrative requirements (copyright holder, LICENSE year).

**Resources**: This skill synthesizes guidance from:
- [DavisVaughan/extrachecks](https://github.com/DavisVaughan/extrachecks)
- `usethis::use_release_issue()` checklist
- Common CRAN rejection reasons

### `lifecycle`

Guidance for managing R package lifecycle according to tidyverse principles using the lifecycle package. Use when setting up lifecycle infrastructure in a package, deprecating functions or arguments, renaming functions/arguments, superseding functions, or marking functions as experimental.

**Organization**: The `SKILL.md` file provides step-by-step instructions for common lifecycle management tasks, while the `references/` directory includes detailed reference materials on lifecycle stages.

**Resources**: This skill synthesizes guidance from:
- [lifecycle package documentation](https://lifecycle.r-lib.org/)
- lifecycle vignettes: "Stages", "Communicate", and "Manage"
- [R Packages: Lifecycle](https://r-pkgs.org/lifecycle.html)

### `mirai`

Comprehensive guidance for async, parallel, and distributed computing in R using the mirai package. Use when running R code asynchronously or in parallel, fixing dependency-passing mistakes, setting up local or remote daemon pools, converting code from future or parallel, using `mirai_map()` for parallel mapping, integrating async tasks with Shiny via `ExtendedTask`, or configuring cluster/HPC computing.

**Organization**: Single comprehensive SKILL.md file covering all major topics — explicit dependency passing (`.args` vs `...`), daemon setup and compute profiles, `mirai_map`, `everywhere`, error handling, Shiny/promises integration, remote/HPC launchers, RNG, debugging, and nested parallelism.

**Resources**: This skill synthesizes guidance from:
- [mirai package documentation](https://mirai.r-lib.org/)
- [mirai GitHub repository](https://github.com/r-lib/mirai)

## Potential Skills

This category could include skills for:

- Package development workflows (usethis, devtools)
- Documentation with roxygen2 and pkgdown
- Package structure and organization
- Dependencies and NAMESPACE management
- R CMD check and CRAN submission
- Continuous integration setup
- Version control workflows for packages

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new skills to this category. We encourage you to use [Anthropic's skill-creator](https://github.com/anthropics/skills) when building new skills.
