# Vignettes vs pkgdown articles

This is a decision guide for whether a piece of long-form documentation should
be a vignette (ships + checked) or a pkgdown article (published, but can be
excluded from package checks).

The goal is to keep your **package** lean and check-friendly while still publishing
high-value tutorials on the **website**.

## Table of Contents

- [Core differences](#core-differences)
- [Decision rules](#decision-rules)
- [Dependency implications](#dependency-implications)
- [A pattern that scales](#common-pattern-that-scales)
- [Operational notes](#operational-notes)
- [Concrete workflows](#concrete-workflows)
- [CI and dependency patterns](#ci-and-dependency-patterns)
- [References](#references)

## Core differences

- **Vignette**

  - Ships with the package
  - Contributes to the `R CMD check` surface
  - Must be reproducible, reasonably fast, and dependency-disciplined

- **Article (pkgdown-only)**
  - Published on the website
  - Can be kept out of package build/check
  - Useful for heavier tutorials and integrations

## Decision rules

Choose a **vignette** when:

- Users should have it available offline with the installed package.
- The content is stable and can be run quickly in automated checks.
- Dependencies are appropriate to declare in `Suggests`.

Choose a **pkgdown article** when:

- Content is valuable but too slow/fragile for check (long runtimes, network, large data).
- It depends on heavy optional tooling you do not want to pull into checks.
- It’s more of a tutorial/integration guide than package “core usage”.

Two practical tie-breakers:

- If you’d be unhappy if it failed in CI/CRAN, don’t ship it as a vignette.
- If it needs heavy deps (Java, databases, browsers, large data), prefer article.

## Dependency implications

- Vignettes: any packages used must be recorded in `DESCRIPTION` (often in `Suggests`).
- Articles: can rely on additional packages that are not appropriate as formal
  dependencies, but you should ensure your site build environment installs what
  it needs (often via `Config/Needs/website` + CI config).

Remember: even if an article doesn’t ship, users copy/paste from it.
Make dependencies explicit in the narrative.

## Common pattern that scales

- Keep a small, focused set of vignettes that represent the “official” package guides.
- Publish longer tutorials and integrations as articles.

This pattern keeps check time and dependency footprint predictable while letting your
site be richer.

## Operational notes

### pkgdown builds vignettes into “articles”

pkgdown will build vignettes found in `vignettes/` and publish them as HTML under
`articles/` on the website.

Operational implication: a vignette is simultaneously “package docs” and “website
content”, so any fragility shows up in both places.

### Creating a pkgdown article that does not ship with the package

If you want to publish long-form content on the website but keep it out of the
package bundle (and therefore out of `R CMD check`), use:

```r
usethis::use_article("your-topic")
```

This creates an article source file under `vignettes/` but adds it to
`.Rbuildignore` automatically, so it is not included in the built package.

Quick check: `usethis::use_article()` is ideal when you want Quarto/Rmd content on the
site but you do _not_ want it to be part of the `R CMD check` surface.

## Concrete workflows

### Make it a vignette (ships + checked)

1. Create a vignette:

```r
usethis::use_vignette("topic")
```

2. Develop it efficiently (avoid repeated full installs):

```r
devtools::load_all()
devtools::build_rmd("vignettes/topic.Rmd")
```

3. Keep it check-friendly:

- Make it fast.
- Avoid network calls.
- Keep dependencies intentional (often `Suggests`).

If the vignette uses a package, add it to `Suggests`.
If it uses system requirements, reconsider shipping it.

4. Verify with a real check periodically:

```r
devtools::check()
```

### Make it a pkgdown article (published, not shipped)

1. Create an article:

```r
usethis::use_article("topic")
```

This creates a source file under `vignettes/` _and_ ensures it does not ship with
the package (via `.Rbuildignore`).

2. Build the website:

```r
pkgdown::build_site()
```

3. Decide how it will be built for users:

- Locally only (you run `pkgdown::build_site()` and commit/publish output).
- In CI (GitHub Actions builds and deploys).

Add a “how to run this” section in the article (even if brief):

- what packages to install
- what system requirements exist
- what output to expect

## CI and dependency patterns

Articles are attractive when content needs heavier dependencies.
If you take this route, make your website build environment reproducible.

### Recommended pattern: `Config/Needs/website`

1. Record website-only packages in `DESCRIPTION`, e.g.:

`Config/Needs/website: pkgdown, downlit, xml2`

2. In CI, install those needs for the site build step.

This keeps runtime dependencies lean while still making the site build reliable.

If you have article-only dependencies that are not suitable even as `Suggests`, this
pattern is the cleanest boundary.

### What still matters even for articles

Even though pkgdown articles don’t ship with the package, you still want:

- Examples in help topics to be check-friendly.
- Vignettes (if any) to be reproducible.
- A clear boundary: “core package docs” (vignettes) vs “extended tutorials” (articles).

Also keep in mind: pkgdown may still evaluate code in articles depending on how you
write them. Treat articles as “build artifacts” and make the site build environment
reproducible.

## References

- R Packages (2e), “Vignettes”: https://r-pkgs.org/vignettes.html
- pkgdown site: https://pkgdown.r-lib.org/
- usethis: `use_article()` / `use_vignette()`: https://usethis.r-lib.org/reference/use_vignette.html
- pkgdown: “Introduction to pkgdown” (Articles section): https://pkgdown.r-lib.org/articles/pkgdown.html
