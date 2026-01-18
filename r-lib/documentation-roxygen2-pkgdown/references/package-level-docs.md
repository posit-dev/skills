# Package-level documentation (`"_PACKAGE"`)

## Table of Contents

- [What Package-level Docs Are](#what-package-level-docs-are)
- [Creating Them with `usethis`](#creating-them-with-usethis)
- [A practical template (recommended shape)](#a-practical-template-recommended-shape)
- [What to Put There](#what-to-put-there)
- [Package-wide roxygen tags (imports, reuse, keywords)](#package-wide-roxygen-tags-imports-reuse-keywords)
- [How It Relates to pkgdown](#how-it-relates-to-pkgdown)
- [Migrating older packages (legacy patterns)](#migrating-older-packages-legacy-patterns)
- [Gotchas](#gotchas)
- [Keeping it in sync](#keeping-it-in-sync)
- [What not to put there](#what-not-to-put-there)
- [References](#references)

## What Package-level Docs Are

Package-level documentation is the help topic you get when you run `?pkgname`.
In modern roxygen workflows, roxygen2 uses the `"_PACKAGE"` sentinel to define
this “package” help topic.

## Creating Them with `usethis`

The recommended workflow is to scaffold and maintain the package-level doc with:

```r
usethis::use_package_doc()
```

This creates a home for the package help topic and sets up the sentinel.

Typical outcomes:

- A new file under `R/` that roxygen processes into the package help topic.
- A clear, stable place to put package-wide documentation and (optionally)
  package-wide roxygen tags.

If you’re starting a new package, it’s worth creating package-level docs early
because it gives you a stable “home” for entry-point links and package-wide
conventions.

## A practical template (recommended shape)

The goal is that `?pkgname` answers:

- What is this package for?
- What are the top entry points?
- Where do I go next?

This template is intentionally short, navigational, and check-friendly:

```r
#' Package Title
#'
#' @description
#' One paragraph: what the package does and who it is for.
#'
#' @section Key functions:
#' - [foo()] for ...
#' - [bar()] for ...
#'
#' @section Articles and vignettes:
#' - `vignette("getting-started")` for ...
#'
#' @seealso
#' - [foo()]
#' - [bar()]
#'
"_PACKAGE"
```

Notes:

- Use roxygen markdown links (`[foo()]`, `[otherpkg::fun()]`) for robust linking.
- Prefer “map” content over “tutorial” content. Tutorials belong in vignettes/articles.
- Keep examples minimal or omit them entirely from the package help topic.

## What to Put There

Good content often includes:

- a short overview of what the package does
- key user-facing concepts or entry points
- links to important topics/vignettes

If you use `usethis` to manage namespace tags centrally, the package doc file is
also a common place where `usethis` maintains a dedicated import block.

Practical writing guidance:

- Keep it short and skimmable (it’s a help topic, not a tutorial).
- Put longer narrative material in a vignette or article.
- Prefer explicit links to the “next place to go” (e.g., a vignette title) so
  `?pkgname` is a navigational entry point.

Additional high-value content that often belongs here:

- A short “design contract” statement if it helps users reason about behavior.
  Example: “All functions return tibbles” or “File paths are always relative to the package root”.
- A pointer to “How to report bugs” or a URL to the issue tracker (if appropriate).

Keep it ruthlessly skimmable: if users need to scroll for multiple screens,
you’ve probably put tutorial content in the wrong place.

## Package-wide roxygen tags (imports, reuse, keywords)

The package doc file is sometimes used as a central place for roxygen tags that
apply broadly.

Common, legitimate uses:

- Package-wide imports maintained by tooling.
- A package-level `@keywords` choice.

Rules of thumb:

- Prefer targeted imports near the functions that need them (`@importFrom`).
- Avoid `@import pkg` unless you truly need broad imports.

On `@keywords internal`:

- Use it when the package help topic is mainly for developers.
- Avoid it when `?pkgname` is meant as a user entry point.

On reuse:

- Use `@inheritParams` and `@inheritSection` on function docs, not in the package
  help topic.

Related pages in this skill:

- [rd-intro-quality.md](rd-intro-quality.md)
- [examples-policy.md](examples-policy.md)
- [roxygen-tags-and-structure.md](roxygen-tags-and-structure.md)
- [pkgdown-overview.md](pkgdown-overview.md)

## How It Relates to pkgdown

Package-level docs and pkgdown serve different roles:

- The package help topic is what users see in R via `?pkgname`.
- Pkgdown’s home page typically comes from README (or a pkgdown home template),
  while reference pages come from `.Rd`.

Treat the package help topic as the “in-R entry point”, and treat pkgdown as the
“web entry point”. They should link to each other conceptually, but they don’t
need to duplicate content.

Practical implication: don’t try to make the package help topic do the job of
the pkgdown home page. Let README + articles do the narrative; let `?pkgname`
be the in-R map.

## Migrating older packages (legacy patterns)

Older roxygen2 patterns you may see:

- `@docType package`
- `@name pkgname-package`

Modern guidance is to prefer the `"_PACKAGE"` sentinel.

When migrating:

1. Add a package doc file with `usethis::use_package_doc()`.
2. Run `devtools::document()`.
3. Ensure `?pkgname` resolves to exactly one topic (avoid duplicates).
4. Remove the legacy package doc block once the sentinel version is correct.

## Keeping it in sync

Treat the package help topic as derived from roxygen like everything else:

1. Edit the roxygen source file created by `usethis::use_package_doc()`.
2. Regenerate:

```r
devtools::document()
```

3. Preview in a development session:

```r
devtools::load_all()
?yourpkg
```

If you see stale content, you’re usually previewing an installed copy rather
than your development version.

Fast “am I reading the dev version?” check:

```r
devtools::load_all()
?yourpkg
```

If it still looks wrong:

- restart R
- run `devtools::document()`
- try again

## What not to put there

Common mistakes:

- Long tutorials or narratives (use a vignette/article).
- Slow or fragile examples.
- Content that must be conditional on optional dependencies (keep package help topic robust).

The package help topic should be a map: “what this package is” and “where to go next”.

## Gotchas

- If `NAMESPACE`/`man/` are stale, re-run `devtools::document()`.
- Package-level docs are part of the check surface; keep them robust.
- Don’t put long-running examples here; keep examples check-friendly.
- If you’re migrating older packages, you may see legacy patterns like
  `@docType package` / `@name pkgname-package`. Prefer the modern `"_PACKAGE"`
  sentinel going forward.

- If you accidentally create _two_ package help topics, you’ll see confusing
  behavior (wrong content for `?pkgname`, duplicate topics). Fix by removing the
  legacy pattern or consolidating to a single package doc file.

## References

- R Packages (2e), “Function documentation” (package-level docs): https://r-pkgs.org/man.html
- usethis: `use_package_doc()`: https://usethis.r-lib.org/reference/use_package_doc.html
