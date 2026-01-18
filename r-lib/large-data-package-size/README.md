# Large Data & Package Size Discipline

A practical playbook for handling large data, files under `inst/extdata`, and package size discipline (especially for CRAN-bound packages).

## Overview

This skill focuses on:

- deciding what data should ship inside the package vs outside
- using `inst/extdata` safely and portably via `system.file()`
- keeping packages small enough for CRAN expectations
- avoiding common pitfalls (writing to user directories, downloading on install, huge vignettes)

## When This Skill Activates

Use this skill when you need to:

- include example datasets or files (CSV, images, templates) in your package
- manage a `data-raw/` workflow and produce compact `.rda` artifacts
- reduce package size (tarball size, installed size, docs size)
- design “large data” strategies (separate data packages, optional downloads, caching)

## File Organization

- [SKILL.md](SKILL.md) - Task mapping + core workflow
- [references/](references/) - Deep dives, checklists, and patterns

```
large-data-package-size/
├── README.md
├── SKILL.md
└── references/
    ├── deciding-what-ships.md
    ├── inst-extdata-patterns.md
    ├── data-raw-workflow.md
    ├── package-size-checklist.md
    ├── compression-and-rda.md
    ├── caching-and-user-dirs.md
    └── external-data-strategies.md
```

## Related skills

- [r-lib/cran-submission](../cran-submission/) - CRAN size policy and submission expectations
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - Check surfaces that reveal size/portability problems
- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/) - Vignettes/examples can dominate size and runtime
