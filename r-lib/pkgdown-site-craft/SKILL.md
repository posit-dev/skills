---
name: r-lib/pkgdown-site-craft
description: >
  Configuring, curating, and deploying pkgdown sites for R packages.
  Use this skill when you need to:
  (1) Set up `_pkgdown.yml` with a stable `url`,
  (2) Curate the reference index and navigation structure,
  (3) Build sites locally and debug missing topics/articles,
  (4) Deploy to GitHub Pages using modern workflows,
  (5) Keep the site aligned with roxygen2 docs and package structure.
---

# pkgdown Site Craft

## When to Use What

| Task                                          | Use                                     |
| --------------------------------------------- | --------------------------------------- |
| Initialize pkgdown GitHub Pages scaffolding   | `usethis::use_pkgdown_github_pages()`   |
| Add a pkgdown GitHub Actions workflow quickly | `usethis::use_github_action("pkgdown")` |
| Build full site locally                       | `pkgdown::build_site()`                 |
| Build just reference index                    | `pkgdown::build_reference()`            |
| Build articles                                | `pkgdown::build_articles()`             |
| Build for GitHub Pages (CI-friendly)          | `pkgdown::build_site_github_pages()`    |
| Debug missing docs                            | Run `devtools::document()` then rebuild |

## Core guidance

- This skill assumes roxygen2 docs and examples are already in good shape (see [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/)).
- Keep `_pkgdown.yml` minimal but explicit.
- Set `url` early (it affects links and metadata).
- Curate reference topics for discoverability.
- Treat site build failures like any other pipeline: reproduce locally, narrow scope, fix root cause.

## Practical workflow

1. **Get documentation into a good state**

- `devtools::document()`
- ensure examples build and vignettes render

2. **Configure pkgdown**

- add `_pkgdown.yml`
- set `url` (especially important for GitHub Pages)

3. **Build locally and preview**

- `pkgdown::build_site()`
- fix missing topics, broken links, and nav/reference organization

4. **Deploy via CI**

- use the r-lib/actions `pkgdown` workflow (via usethis)
- confirm GitHub Pages is configured to publish the `gh-pages` branch (or your chosen target)

5. **Maintain**

- keep `_pkgdown.yml` and your exported API in sync
- treat site build failures as a CI signal (often missing deps or broken examples)

## References

- [references/pkgdown-config.md](references/pkgdown-config.md)
- [references/pkgdown-reference-index.md](references/pkgdown-reference-index.md)
- [references/pkgdown-deploy-gh-pages.md](references/pkgdown-deploy-gh-pages.md)
- [references/pkgdown-troubleshooting.md](references/pkgdown-troubleshooting.md)
- [references/pkgdown-local-preview.md](references/pkgdown-local-preview.md)

## External resources

- pkgdown: https://pkgdown.r-lib.org/
- r-lib/actions examples (pkgdown): https://github.com/r-lib/actions/tree/v2/examples
