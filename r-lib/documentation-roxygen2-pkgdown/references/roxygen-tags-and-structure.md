# Roxygen tags, blocks, and structure

## Table of Contents

1. [How to Think About Roxygen Blocks](#how-to-think-about-roxygen-blocks)
2. [Common Tags by Job](#common-tags-by-job)
3. [Markdown in Roxygen](#markdown-in-roxygen)
4. [NAMESPACE Side-effects](#namespace-side-effects)
5. [Patterns and Anti-patterns](#patterns-and-anti-patterns)
6. [Documenting Common Object Types](#documenting-common-object-types)
7. [Common Check Failures and Fixes](#common-check-failures-and-fixes)
8. [References](#references)

## How to Think About Roxygen Blocks

Roxygen blocks serve two purposes:

- Generate **help topics** (`man/*.Rd`).
- Generate **namespace directives** (`NAMESPACE`).

The key practice is to treat roxygen comments as the source of truth, and to
regenerate derived output with `devtools::document()`.

Practical implication: if something is wrong in `man/` or `NAMESPACE`, fix the
roxygen source and regenerate, rather than patching the generated files.

## Common tags by job

This is a “what tag do I reach for?” map (not exhaustive):

### Help topic content

- **Describe purpose:** `@title`, `@description`, `@details`
- **Document interface:** `@param`, `@returns` (or `@return`), `@value`
- **Examples:** `@examples`, `@examplesIf`
- **Cross-linking:** `@seealso`
- **Grouping/indexing:** `@family`, `@keywords`

Other useful help-topic tags you’ll see in real packages:

- `@inheritParams` and `@inheritSection` to reuse docs across functions.
- `@aliases` when you need extra entry points to the same topic.
- `@noRd` when you intentionally do not want an exported help topic.

### Namespace directives

- **Export a function/method:** `@export`
- **Import specific objects:** `@importFrom pkg fun`
- **Import entire namespace (rare):** `@import pkg`
- **Last resort:** `@rawNamespace` (avoid unless you know you need it)

Rule of thumb: prefer a small number of explicit `@importFrom` tags over broad
imports. It makes dependencies easier to audit and reduces surprises.

Decision rule (simple but effective):

- If you can write `pkg::fun()` in code, you usually _don’t_ need any `@importFrom`.
- If you are using unqualified symbols (common for S3 methods, some tidy-eval patterns,
  or operators), prefer targeted `@importFrom`.
- Avoid `@import pkg` unless the package is designed to be imported wholesale.

## Markdown in Roxygen

Modern roxygen workflows often use markdown features for clarity.
Keep formatting readable, but remember it ultimately becomes `.Rd`.

Enabling markdown is typically done via:

- `Roxygen: list(markdown = TRUE)` in `DESCRIPTION`

Then you can use:

- Backticks for inline code
- Links like `[otherpkg::fun()]` (renders as an Rd link)
- Lists and simple emphasis

Common markdown gotchas:

- Prefer short code examples: long fenced blocks can be hard to read in `?help`.
- Keep link text stable; renames can break `@seealso` navigation.
- When linking to functions, prefer `[pkg::fun()]` over raw URLs.

## NAMESPACE Side-effects

When you add `@export` or `@importFrom`, you are changing the package namespace.
Make that change intentionally, then regenerate with `devtools::document()`.

Common failure mode: you add an import tag, but forget to document, so `NAMESPACE`
does not reflect your intent.

Another common failure mode: you add `@export` during development, but didn’t intend
to make the function part of the public API.

API decision rule:

- Export only what you’re willing to support.
- If a function is “helper-y” but must be exported for S3 dispatch, document that in
  the help topic (or keep it grouped with the primary generic).

Recommended workflow:

```r
devtools::document()
devtools::check()
```

If you’re iterating on doc-related failures, tighten the loop with
`devtools::check_man()` (see [roxygen-workflow.md](roxygen-workflow.md)).

## Patterns and Anti-patterns

### Good: minimal, readable docs

Focus on:

- what the function does
- what inputs mean
- what output looks like
- one or two small examples

Template for an exported function (high-signal, low-noise):

- Title: purpose-first
- Description: one paragraph
- `@param`: constraints + units
- `@return`: class/shape + invariants
- `@examples`: minimal success + one common variant
- `@seealso`: next step links

### Risky: using `@import` broadly

Prefer targeted `@importFrom pkg fun` where possible; broad imports can increase
namespace clutter and make dependencies less explicit.

Also risky:

- Using `@rawNamespace` to work around missing imports (fix the imports instead).
- Using `@noRd` to hide an exported object (if it’s exported, it should usually have docs).

## Two common “structure” patterns

### Reuse argument docs

- `@inheritParams other_fun`
- `@inheritSection other_fun {section name}`

Use these when you have the same parameters across multiple functions.

Reuse decision rule:

- Use `@inheritParams` when the parameters have the same meaning.
- Don’t use inheritance to avoid thinking: if the parameter meaning differs, document it.

### One help topic for multiple functions

Use `@rdname` when several functions belong to the same conceptual topic.

Keep `@rdname` topics coherent:

- One topic should have one “main” function; the others should feel like siblings.
- Use `@family` to group large sets instead of giant shared topics.

## Documenting common object types

### Internal helpers

Default: do not export. If you must keep internal helpers documented (for contributors),
consider:

- `@noRd` (no help topic) + rely on readable code
- or keep a small internal doc topic and link to it from developer docs (but avoid
  shipping lots of internal topics to users)

### S3 methods

Common patterns you’ll see:

- The generic is exported and documented.
- Methods share the generic’s help topic via `@rdname`.
- You may need imports for generics (e.g. `@importFrom stats predict`) if you implement
  methods without qualifying.

If you create methods for generics in other packages, be explicit about which package
owns the generic.

### Data objects

Data documentation often needs:

- `@format` (columns, types, invariants)
- examples that show how to inspect or use the data (but keep them fast)

### Packages

For package-level docs (`?pkgname`), see:
[package-level-docs.md](package-level-docs.md)

## Common Check Failures and Fixes

### “Documented arguments not in \usage” / “Undocumented arguments”

Usually means your function signature changed but the `@param` list did not.

Fix:

- Update the roxygen block.
- Re-run `devtools::document()`.

Prevention: when you change a signature, update the docs in the same commit.

### “Namespace dependencies not required” / missing imports

Usually means you added `pkg::fun()` calls or imports but didn’t declare the
dependency correctly.

Fix:

- Ensure the dependency appears in `DESCRIPTION` (`Imports` for runtime use).
- If you used `@importFrom`, regenerate via `devtools::document()`.

If the dependency is only used in examples/tests, consider `Suggests` instead.

For dependency decision rules, see the `r-lib/r-cmd-check-ci` references:

- [dependencies-mindset.md](../../r-cmd-check-ci/references/dependencies-mindset.md)
- [dependencies-in-practice.md](../../r-cmd-check-ci/references/dependencies-in-practice.md)

### Examples fail in `R CMD check`

Fix:

- Keep examples fast and side-effect-safe.
- Declare any packages used by examples (often in `Suggests`).
- Use `@examplesIf` for conditional execution rather than hiding everything
  behind `requireNamespace()`.

See: [examples-policy.md](examples-policy.md) and
[check-docs-fast.md](../../r-cmd-check-ci/references/check-docs-fast.md).

### “Rd files must have a non-empty title/description”

Usually means you relied on defaults and ended up with empty fields.

Fix:

- Add `@title` and `@description`.
- Regenerate with `devtools::document()`.

Use [rd-intro-quality.md](rd-intro-quality.md) as the checklist.

## References

- R Packages (2e), “Function documentation”: https://r-pkgs.org/man.html
- roxygen2 site: https://roxygen2.r-lib.org/
