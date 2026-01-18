# Code Coverage and CI

A practical playbook for measuring R package test coverage and integrating coverage runs into CI.

## Overview

Coverage is a feedback tool:

- it shows which lines were (and weren’t) executed by tests
- it helps you find untested error paths and edge cases
- it should not replace thoughtful tests

This skill focuses on:

- running coverage locally with `covr`
- adding a coverage job to GitHub Actions
- interpreting coverage results without gaming the metric

## When This Skill Activates

Use this skill when you need to:

- measure coverage for an R package test suite
- add CI coverage reporting for pull requests
- decide what to test next based on uncovered code
- troubleshoot coverage failures in CI

## File Organization

- [SKILL.md](SKILL.md) - Task mapping + workflows
- [references/](references/) - Local coverage, exclusions, GitHub Actions setup, Codecov notes, and coverage strategy

```
code-coverage-ci/
├── README.md
├── SKILL.md
└── references/
    ├── ci-and-codecov.md
    ├── covr-local.md
    ├── exclusions-and-nocov.md
    ├── github-actions-coverage.md
    └── coverage-strategy.md
```

## Related skills

- [r-lib/testing-r-packages](../testing-r-packages/) - Improving tests is the main lever
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - CI patterns and dependency discipline
