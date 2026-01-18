# Documentation (roxygen2 + pkgdown)

Workflows and best practices for R package documentation using roxygen2,
vignettes/articles, and pkgdown.

## Overview

This skill is built around a simple idea: treat documentation as part of the
package’s quality surface.

- roxygen comments in `R/` are the source of truth
- `man/*.Rd` and `NAMESPACE` are derived outputs
- examples are executable and must be check-friendly
- pkgdown is a publishing layer that amplifies whatever quality you ship

If you keep the feedback loop tight, documentation problems become routine to fix
instead of mysterious CI failures.

## When This Skill Activates

Use this skill when you need to:

- Write or fix function documentation (roxygen2)
- Regenerate `.Rd` files and `NAMESPACE` via `devtools::document()`
- Produce examples that run under `R CMD check`
- Add package-level docs (`"_PACKAGE"`)
- Create and maintain vignettes
- Decide between shipping vignettes vs publishing pkgdown articles
- Build a pkgdown website for cohesive, linked documentation

## The 80/20 workflow

Most doc work fits this loop:

```r
devtools::load_all()
devtools::document()
devtools::check_man()
```

Then confirm with:

```r
devtools::check()
```

Use `check_man()` for speed while iterating; trust `check()` before you ship.

## What “good” docs look like (in practice)

- Help topics teach a minimal successful usage quickly.
- Examples run fast, don’t error, and restore global state.
- Long narrative belongs in vignettes/articles, not `@examples`.
- Users can navigate: `?pkgname` → help topics → vignette/article → pkgdown.

## File Organization

- [SKILL.md](SKILL.md) - Core workflows and task→tool mapping
- [references/](references/) - Deep dives and policies mapped to canonical sources

```
documentation-roxygen2-pkgdown/
├── README.md
├── SKILL.md
└── references/
	├── roxygen-workflow.md
	├── roxygen-tags-and-structure.md
	├── rd-intro-quality.md
	├── examples-policy.md
	├── package-level-docs.md
	├── vignettes-workflow.md
	├── vignettes-vs-articles.md
	└── pkgdown-overview.md
```

### Reference Files

- [references/roxygen-workflow.md](references/roxygen-workflow.md)
- [references/roxygen-tags-and-structure.md](references/roxygen-tags-and-structure.md)
- [references/rd-intro-quality.md](references/rd-intro-quality.md)
- [references/examples-policy.md](references/examples-policy.md)
- [references/package-level-docs.md](references/package-level-docs.md)
- [references/vignettes-workflow.md](references/vignettes-workflow.md)
- [references/vignettes-vs-articles.md](references/vignettes-vs-articles.md)
- [references/pkgdown-overview.md](references/pkgdown-overview.md)

## Related skills

- [r-lib/package-development-workflow](../package-development-workflow/)
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/)
