# Package Development Workflow (r-lib)

Modern, practical workflows for developing R packages using the r-lib ecosystem
(usethis/devtools) and the core edit → load → test-drive → document → check loop.

## Overview

This skill is about keeping package development boring and repeatable.

It focuses on:

- Fast iteration (`devtools::load_all()`)
- Keeping derived files in sync (`devtools::document()` for `NAMESPACE` + `man/`)
- Catching portability/dependency issues early (`devtools::check()`)
- Using usethis for scaffolding once, and devtools for the daily loop

## When This Skill Activates

Use this skill when you need to:

- Create a new package and set it up with modern defaults
- Iterate quickly with `devtools::load_all()` (without reinstalling constantly)
- Keep `.Rd` docs and `NAMESPACE` up-to-date with `devtools::document()`
- Run `devtools::check()` early and often and respond to failures
- Adopt Git/GitHub workflows for package development

## The daily loop (80/20)

For day-to-day development, this is the core:

```r
devtools::load_all()

# test-drive the change
# my_fun(...)

devtools::document()  # whenever roxygen/exports/imports changed
devtools::test()      # when behavior should be protected
devtools::check()     # before pushing / opening a PR
```

If CI is regularly the first place you discover failures, this loop isn’t tight enough.

## File Organization

- [SKILL.md](SKILL.md) - The core playbook and task→tool mapping
- [references/](references/) - Deep dives mapped to canonical sources

```
package-development-workflow/
├── README.md
├── SKILL.md
└── references/
	├── the-whole-game.md
	├── workflow101-create-package.md
	├── workflow101-rstudio-projects.md
	├── workflow101-path-discipline.md
	├── workflow101-load-all.md
	├── workflow101-check.md
	├── usethis-scaffolding-playbook.md
	└── git-github-for-packages.md
```

### Reference Files

- [references/the-whole-game.md](references/the-whole-game.md)
- [references/workflow101-create-package.md](references/workflow101-create-package.md)
- [references/workflow101-rstudio-projects.md](references/workflow101-rstudio-projects.md)
- [references/workflow101-path-discipline.md](references/workflow101-path-discipline.md)
- [references/workflow101-load-all.md](references/workflow101-load-all.md)
- [references/workflow101-check.md](references/workflow101-check.md)
- [references/usethis-scaffolding-playbook.md](references/usethis-scaffolding-playbook.md)
- [references/git-github-for-packages.md](references/git-github-for-packages.md)

## Related skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/)
- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/)
