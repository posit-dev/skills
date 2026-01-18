# The roxygen workflow (write → document → preview)

This page is about keeping documentation changes in the same “tight loop” as code
changes: iterate fast locally, then validate with check-oriented commands.

## Table of Contents

1. [The 3-step Loop](#the-3-step-loop)
2. [What `document()` Actually Does](#what-document-actually-does)
3. [Previewing Docs Reliably](#previewing-docs-reliably)
4. [Common Failure Modes](#common-failure-modes)
5. [Recommended Habits](#recommended-habits)
6. [Fast loops for specific problems](#fast-loops-for-specific-problems)
7. [Related pages](#related-pages)
8. [References](#references)

## The 3-step Loop

The intended roxygen workflow is a tight loop:

1. **Write** roxygen blocks above the relevant object (functions, datasets, etc.).
2. **Generate** docs with `devtools::document()`.
3. **Preview** locally (typically after a `devtools::load_all()`): `?pkg::fun`.

This is intentionally similar to “edit → reload → try” in code development: you
want documentation changes to be fast and repeatable.

Recommended minimal loop:

```r
devtools::load_all()
devtools::document()
?your_function
```

Notes on ordering:

- If you changed roxygen (docs/exports/imports), run `devtools::document()`.
- If you changed code behavior used in examples, run `devtools::load_all()`.
- If you changed both (very common), do both, then re-open the topic.

If you are repeatedly editing roxygen blocks and want a slightly faster-feeling loop,
this often works well:

```r
devtools::document()
devtools::load_all()
?your_function
```

The key idea: **preview the docs for the code you are actually editing**.
If you preview docs without loading your dev version, you can easily end up
reading the installed package docs and chasing ghosts.

## What `document()` Actually Does

`devtools::document()` is the canonical way (in the r-lib workflow) to regenerate:

- `man/*.Rd` help files
- the `NAMESPACE` file

The key practice is to treat documentation generation as **derived output**
from roxygen comments, not something edited by hand.

Under the hood, devtools is calling into roxygen2 (roughly equivalent to
`roxygen2::roxygenize()`), with some extra conveniences.

## Previewing Docs Reliably

Documentation previews can be misleading if you’re not loading the current source.
A reliable pattern is:

```r
devtools::load_all()
devtools::document()

?your_function
```

Notes:

- Prefer `?your_function` while developing inside the package.
- Outside the package, use `?pkg::your_function`.

Avoid a common trap: without `devtools::load_all()`, you may be reading docs from the
installed package rather than your development checkout.

If you’re iterating on failures seen in `R CMD check`, use `devtools::check_man()`
to tighten the loop while staying closer to how examples are actually executed.

Decision rule: which command should you run?

- You changed roxygen tags, `@export`, or imports → `devtools::document()`.
- You changed examples and want doc-only speed → `devtools::check_man()`.
- You’re close to done (or CI failed) → `devtools::check()` (optionally `args = "--as-cran"`).

If your goal is “make docs look good on pkgdown”, you still want the same loop,
but you also need to confirm:

- your `.Rd` renders correctly
- your examples run and don’t have side effects

Pkgdown amplifies doc quality issues because it publishes everything.

## Common Failure Modes

- **Stale docs**: roxygen block changed but `document()` not re-run.
- **Stale namespace**: missing imports/exports because `NAMESPACE` didn’t regen.
- **Example failures**: examples run in `R CMD check`; they must be fast and safe.

Two other high-frequency failures:

- **Rd parse errors**: roxygen generated invalid `.Rd` (unbalanced braces, bad
  `\\link{}` syntax, illegal markup).
- **Topic mismatch**: you expect function A’s docs, but are reading function B’s
  topic via `@rdname` or a stale alias.

Two common sources of confusion:

- You changed code but didn’t re-run `load_all()`, so examples/preview reflect
  old behavior.
- You changed roxygen but didn’t re-run `document()`, so `.Rd`/`NAMESPACE` are stale.

If `R CMD check` is failing on docs, use the `r-lib/r-cmd-check-ci` skill to
triage, and consider `devtools::check_man()` for faster iterations.

### Debug checklist: “Why did this doc change not show up?”

1. Confirm `devtools::document()` ran without errors.
2. Confirm you are previewing development docs:

- inside package: `?your_function`
- outside package: reinstall, or use a dev install, then `?pkg::your_function`

3. Search for topic-sharing tags:

- are you using `@name`, `@rdname`, or `@aliases` elsewhere?

4. If you changed exports/imports, confirm `NAMESPACE` changed as expected.

## Recommended Habits

- Run `devtools::document()` whenever you change roxygen tags, exports, or imports.
- Keep examples minimal and robust (see `examples-policy.md`).
- Validate with `devtools::check()` regularly; interactive preview is not enough.

Add these if you want fewer “doc-only CI surprises”:

- Run `devtools::check_man()` early and often when editing docs.
- Don’t hand-edit `man/*.Rd` or `NAMESPACE` (treat them as derived output).
- When refactoring signatures, update `@param` immediately and regenerate.

## Fast loops for specific problems

### “I’m changing docs and examples and want speed”

```r
devtools::document()
devtools::check_man()
```

Then confirm with `devtools::check()` before you’re done.

### “Docs look wrong / out of date”

Checklist:

1. `devtools::document()` ran successfully.
2. `devtools::load_all()` ran successfully.
3. `?your_function` shows development docs (it should say it’s rendering
   development documentation).

If the doc is still “wrong”, look for:

- `@rdname` causing multiple objects to share a topic.
- `@inheritParams` pulling docs from an unexpected source.
- `@aliases` collisions.

### “CI fails on docs”

- Open the `.Rcheck` logs (see the `r-lib/r-cmd-check-ci` mental model).
- Reproduce locally with `devtools::check()`.

If the failure is only in CI:

- Check whether an example depends on a suggested package that isn’t installed.
- Check whether an example depends on system deps / external data.
- Confirm you didn’t accidentally rely on a user-level cache or global option.

See: [../../r-cmd-check-ci/references/r-cmd-check-mental-model.md](../../r-cmd-check-ci/references/r-cmd-check-mental-model.md)

## Related pages

- [roxygen-tags-and-structure.md](roxygen-tags-and-structure.md)
- [examples-policy.md](examples-policy.md)
- [pkgdown-overview.md](pkgdown-overview.md)
- [check-docs-fast.md](../../r-cmd-check-ci/references/check-docs-fast.md)

If your docs problem is actually a dependency problem (imports/suggests/examples), see:
[dependencies-in-practice.md](../../r-cmd-check-ci/references/dependencies-in-practice.md)

## References

- R Packages (2e), “Function documentation”: https://r-pkgs.org/man.html
- roxygen2 site: https://roxygen2.r-lib.org/
- devtools: `document()`: https://devtools.r-lib.org/reference/document.html
