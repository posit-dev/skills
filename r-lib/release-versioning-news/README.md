# Release Versioning and NEWS

A practical workflow for bumping versions, maintaining `NEWS.md`, and preparing releases for R packages.

## Overview

This skill focuses on the mechanics that keep releases predictable:

- choosing a version bump
- keeping `NEWS.md` actionable and user-facing
- preparing a release branch/PR
- tagging and post-release cleanup

## When This Skill Activates

Use this skill when you need to:

- bump a package version correctly
- start or update `NEWS.md`
- write release notes that map to user-visible change
- run the right checks before release

## File Organization

- [SKILL.md](SKILL.md) - Task mapping + practical workflow
- [references/](references/) - Versioning guidance, NEWS conventions, and a release checklist

```
release-versioning-news/
├── README.md
├── SKILL.md
└── references/
    ├── versioning.md
    ├── news-md-conventions.md
    ├── release-checklist.md
    └── release-pr-template.md
```

## Related skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - The release quality gate
- [r-lib/cran-submission](../cran-submission/) - If you’re releasing to CRAN
- [r-lib/revdep-checks](../revdep-checks/) - If changes might impact downstream users
