# Reverse Dependency Checks

A workflow playbook for running reverse dependency (revdep) checks before releases and interpreting results.

## Overview

Reverse dependency checks answer: “If I release this change, what will it break?”

This skill focuses on:

- running revdep checks with minimal ceremony
- separating your breakage from downstream/environmental noise
- producing an actionable summary (what to fix vs what to document)

## When This Skill Activates

Use this skill when you need to:

- run reverse dependency checks for an upcoming release
- interpret failures in downstream packages
- decide whether a change is release-safe
- prepare a release PR with a revdep summary

## File Organization

- [SKILL.md](SKILL.md) - Task mapping + core workflow
- [references/](references/) - Deep dives and templates

```
revdep-checks/
├── README.md
├── SKILL.md
└── references/
    ├── downstream-triage-playbook.md
    ├── revdepcheck-workflow.md
    ├── interpreting-revdep-results.md
    ├── release-readiness-and-revdeps.md
    └── revdep-summary-template.md
```

## Related skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - Understanding check surfaces that revdeps often expose
- [r-lib/cran-submission](../cran-submission/) - Releases and CRAN submissions often require revdep evidence
