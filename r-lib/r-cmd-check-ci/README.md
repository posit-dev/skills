# R CMD check and CI

A practical playbook for running, interpreting, and fixing `R CMD check` results,
plus setting up CI with GitHub Actions using modern r-lib tooling.

## Overview

This skill treats `R CMD check` as an integration pipeline:

- build a clean package bundle
- install it into a temporary library
- load/unload it in a clean session
- validate DESCRIPTION, NAMESPACE, docs/examples, tests, and vignettes

That’s why check catches “works on my machine”. The goal here is to turn check
output into a fix, quickly and reliably.

## When This Skill Activates

Use this skill when you need to:

- Run `devtools::check()` and understand the results
- Triage and fix ERROR/WARNING/NOTE outcomes
- Diagnose failures in DESCRIPTION, dependencies, namespace, docs, tests, or vignettes
- Apply dependency best practices (Imports vs Suggests vs Depends)
- Set up GitHub Actions CI (especially `check-standard`)
- Debug failures that show up only on CI/Windows/macOS

## The fast triage loop

When check fails, do this (in order):

1. Find the first real error in the `.Rcheck` logs (don’t chase cascades).
2. Classify the failure surface: install/load, docs/examples, tests, vignettes, or metadata/deps.
3. Reproduce locally with `devtools::check()`.
4. Tighten the loop with the smallest tool that still exercises the failing surface:
   - docs/examples: `devtools::check_man()`
   - tests: `devtools::test()`
5. Re-run `devtools::check()` before you consider it fixed.

If CI is your first failure signal, the local discipline loop in `r-lib/package-development-workflow` is too loose.

## File Organization

- [SKILL.md](SKILL.md) - Core triage workflow and task→tool mapping
- [references/](references/) - Deep dives organized around canonical check phases and policies

```
r-cmd-check-ci/
├── README.md
├── SKILL.md
└── references/
	├── r-cmd-check-mental-model.md
	├── r-cmd-check-appendix-playbook.md
	├── check-docs-fast.md
	├── description-fields-that-affect-check.md
	├── dependencies-mindset.md
	├── dependencies-in-practice.md
	├── installing-check-deps.md
	└── r-lib-actions-and-check-standard.md
```

### Reference Files

- [references/r-cmd-check-mental-model.md](references/r-cmd-check-mental-model.md)
- [references/r-cmd-check-appendix-playbook.md](references/r-cmd-check-appendix-playbook.md)
- [references/check-docs-fast.md](references/check-docs-fast.md)
- [references/description-fields-that-affect-check.md](references/description-fields-that-affect-check.md)
- [references/dependencies-mindset.md](references/dependencies-mindset.md)
- [references/dependencies-in-practice.md](references/dependencies-in-practice.md)
- [references/r-lib-actions-and-check-standard.md](references/r-lib-actions-and-check-standard.md)
- [references/installing-check-deps.md](references/installing-check-deps.md)

## Related skills

- [r-lib/package-development-workflow](../package-development-workflow/)
- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/)
