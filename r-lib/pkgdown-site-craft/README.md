# pkgdown Site Craft

A practical playbook for configuring, curating, and deploying pkgdown sites for R packages.

## Overview

This skill focuses on turning a “generated site” into a usable documentation surface:

- curated reference index and navigation
- predictable URLs via `_pkgdown.yml` `url`
- articles/vignettes structure
- GitHub Pages deployment

## When This Skill Activates

Use this skill when you need to:

- configure `_pkgdown.yml`
- curate reference topics and ordering
- build a site locally (`pkgdown::build_site()`)
- deploy to GitHub Pages
- troubleshoot broken links, missing articles, or site build failures

## File Organization

- [SKILL.md](SKILL.md) - Task mapping + workflow
- [references/](references/) - Config, reference index curation, and deployment details

```
pkgdown-site-craft/
├── README.md
├── SKILL.md
└── references/
    ├── pkgdown-config.md
    ├── pkgdown-reference-index.md
    ├── pkgdown-local-preview.md
    ├── pkgdown-deploy-gh-pages.md
    └── pkgdown-troubleshooting.md
```

## Related skills

- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/) - roxygen and articles/vignettes foundations
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - CI discipline and dependency setup
