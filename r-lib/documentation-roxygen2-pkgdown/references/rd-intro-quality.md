# `.Rd` help topics: quality essentials

High-quality help topics are a product feature: they help users succeed quickly and
reduce support burden. In the r-lib workflow, they also have a hard constraint:
**they must be `R CMD check`-safe**.

This page is a practical checklist + pattern library for writing and reviewing
help topics (as generated from roxygen).

## Table of Contents

1. [What a Help Topic Needs to Do](#what-a-help-topic-needs-to-do)
2. [A Quality Checklist](#a-quality-checklist)
3. [Title/Description Patterns](#titledescription-patterns)
4. [Argument and Return Docs](#argument-and-return-docs)
5. [Examples as Part of Docs](#examples-as-part-of-docs)
6. [Cross-linking and Navigation](#cross-linking-and-navigation)
7. [When to Move Content Elsewhere](#when-to-move-content-elsewhere)
8. [Common Pitfalls](#common-pitfalls)
9. [Related Pages](#related-pages)
10. [References](#references)

## What a Help Topic Needs to Do

A high-quality help topic helps a user answer, quickly:

- What is this for?
- What inputs does it take?
- What does it return?
- What does a minimal successful usage look like?

In package development, help topics also need to be check-friendly: examples
must run, and the generated `.Rd` must be valid.

## A Quality Checklist

Use this checklist when reviewing docs:

- **Title**: short, descriptive.
- **Description**: 1–3 sentences that explain the purpose.
- **Args**: each argument documented; meaning and units clear.
- **Return**: class/shape described.
- **Examples**: minimal, fast, robust.

If you can’t check every item quickly, the help topic is probably trying to do
too much. Move the narrative to a vignette or article.

Also verify:

- **Signature matches docs**: no undocumented or documented-but-missing args.
- **Dependencies are explicit**: no hidden packages used in examples.
- **Error messages are readable** (if you mention them): do they match actual behavior?

Fast review trick: skim the topic as if you were a new user.
If you can’t answer “what do I do next?” within 10 seconds, add a minimal example
and a `@seealso` path.

## Title/description patterns

Help topic titles and descriptions drive discoverability (search + scanning).

Good defaults:

- **Title**: short, purpose-first. Start with a verb (“Read…”, “Compute…”, “Parse…”) or
  a concrete noun phrase (“HTTP request”, “XYZ parser”).
- **Description**: 1–3 sentences that answer: what is this for, and what does it return/do?
- **Details**: constraints, edge cases, and “why” (not the full tutorial).

Common upgrade patterns:

- Replace “Tools” / “Helpers” titles with the actual job.
- Replace “Creates an object” with shape + intent (“Creates a `foo` object used to …”).

If your Description needs multiple paragraphs to be correct, it probably belongs
in a vignette/article.

## Argument and Return Docs

Keep argument docs concrete:

- expected type/class
- length/dimensions if relevant
- constraints (must be non-empty, must be increasing, etc.)

Return docs should explain structure, not just “returns a result”.

If the return value is a data structure, specify what matters to a user:

- class/type (e.g. tibble, data frame, character vector)
- key columns/names
- important invariants (sorted? unique? one row per input?)

Decision rules:

- If an argument is “the hard one”, document it first and be specific about
  constraints.
- If an argument accepts multiple types, list them and what changes (e.g.
  “character vector or `NULL`; `NULL` means …”).
- If you validate inputs, document the invariant you enforce.

## Examples as Part of Docs

Examples are part of the help topic UX.
They should also satisfy check constraints (see `examples-policy.md`).

Good example shape:

- Start with a minimal successful call.
- Show one common option/variant.
- Avoid teaching the entire problem domain in `@examples`.

Most topics benefit from an examples “ladder”:

1. **Minimal success**: the smallest realistic call.
2. **One common variant**: a frequent option or common pattern.
3. **Edge case (optional)**: only if it prevents common misuse.

Keep examples self-contained:

- Provide inputs in the example.
- Avoid reading/writing files unless that is the point (and then clean up).
- Avoid network access.

If you need a longer narrative, move it to a vignette or article:

- Vignettes: [vignettes-workflow.md](vignettes-workflow.md)
- Choosing formats: [vignettes-vs-articles.md](vignettes-vs-articles.md)

When you do move content out:

- keep a minimal example in `@examples`
- link to the vignette/article from `@seealso` or a short sentence in Details

For rules and mechanisms (`@examplesIf`, `\\donttest`, `\\dontrun`, cleanup), use:
[examples-policy.md](examples-policy.md)

## Cross-linking and navigation

Good help topics are navigational.

Prefer linking patterns that are robust in both R and pkgdown:

- Link to functions with `[pkg::fun()]`.
- Link to vignettes with `vignette("topic")`.
- Use `@seealso` for “where do I go next?”.

Patterns that work well in practice:

- Provide a “next step” link for workflows (parse → validate → write).
- Use `@family` when you have a set of siblings; then ensure the pkgdown reference
  page uses those families in a useful way.

If your package has a natural “start here” guide, make it easy to find from:

- the package help topic (`?pkgname`)
- the most common exported functions

## When to Move Content Elsewhere

Use this decision rule (fast and practical):

- Keep **interface** + **minimal usage** + **one common variant** in the help topic.
- Move **tutorial narrative**, **multiple scenarios**, and **plots/figures** to a vignette/article.

Signals you should move content:

- Examples take noticeable time.
- The help page is longer than what a user will scan.
- You need package-level state or many dependencies to explain the concept.

## Common Pitfalls

- **Vague argument docs** (“a vector”) without constraints.
- **Return docs that don’t describe shape** (“returns a result”).
- **Examples that rely on undeclared packages**.
- **Examples that modify state** without restoring.
- **Overlong examples** that become mini-tutorials (move those to vignettes).
- **Docs don’t match the function signature** after refactors.
- **Broken links in `@seealso`** (especially after renames).

## Related pages

- [roxygen-tags-and-structure.md](roxygen-tags-and-structure.md)
- [roxygen-workflow.md](roxygen-workflow.md)
- [examples-policy.md](examples-policy.md)
- [package-level-docs.md](package-level-docs.md)
- [pkgdown-overview.md](pkgdown-overview.md)

## References

- R Packages (2e), “Function documentation”: https://r-pkgs.org/man.html
