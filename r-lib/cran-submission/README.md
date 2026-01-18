# CRAN Submission

A practical, opinionated workflow for preparing an R package for CRAN submission (new submissions and updates).

## Overview

This skill treats CRAN submission as an extension of `R CMD check` discipline:

- run checks in clean environments (not your interactive dev session)
- address ERROR/WARNING/NOTE issues with CRAN expectations in mind
- document any unavoidable NOTE in `cran-comments.md`
- be ready to respond quickly and precisely to CRAN feedback

## When This Skill Activates

Use this skill when you need to:

- prepare a package for CRAN (first submission or update)
- run checks “as CRAN” and interpret typical NOTEs
- write or review `cran-comments.md`
- verify DESCRIPTION metadata for CRAN
- triage issues related to examples, vignettes, large files, or suggested packages
- plan a resubmission response

## File Organization

- [SKILL.md](SKILL.md) - Core checklist and tool mapping
- [references/](references/) - Deep dives (CRAN comments, common gotchas, and a submission checklist)

```
cran-submission/
├── README.md
├── SKILL.md
└── references/
    ├── as-cran-checks.md
    ├── common-cran-notes.md
    ├── cran-submission-checklist.md
    ├── cran-comments-and-responses.md
    └── cran-policy-gotchas.md
```

## Related skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - Understanding and triaging `R CMD check`
- [r-lib/package-development-workflow](../package-development-workflow/) - Keeping check green during development
- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/) - Docs/examples/vignettes are frequent CRAN friction points
