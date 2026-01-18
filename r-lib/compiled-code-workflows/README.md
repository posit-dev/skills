# Compiled Code Workflows (Rcpp, toolchains, system deps)

A practical playbook for R packages that include compiled code (C/C++/Fortran), use Rcpp, or depend on external system libraries.

## Overview

This skill focuses on:

- making builds reproducible across Linux/macOS/Windows
- understanding the `src/` build pipeline (`Makevars`, `configure`, `LinkingTo`, `SystemRequirements`)
- diagnosing common CI and CRAN failures
- keeping compiled code safe for `R CMD check` (no abort/exit, portable file paths, no surprise downloads)

## When This Skill Activates

Use this skill when you need to:

- add compiled code to an R package (or refactor an existing `src/` layout)
- set up or debug compilation on Windows/macOS/Linux
- add or document external system dependencies
- understand `LinkingTo` vs linking to system libs
- troubleshoot build errors in CI or on CRAN

## File Organization

- [SKILL.md](SKILL.md) - Task mapping + core workflow
- [references/](references/) - Deep dives and troubleshooting

```
compiled-code-workflows/
├── README.md
├── SKILL.md
└── references/
    ├── compiled-code-quality-gates.md
    ├── linkingto-and-systemrequirements.md
    ├── src-layout-and-makevars.md
    ├── configure-and-autoconf.md
    ├── toolchains-and-ci.md
    └── troubleshooting-compiled-builds.md
```

## Related skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - CI discipline and check triage
- [r-lib/cran-submission](../cran-submission/) - CRAN policy expectations (including for compiled code)
- [r-lib/package-development-workflow](../package-development-workflow/) - Where compiled code fits in the daily loop
