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
