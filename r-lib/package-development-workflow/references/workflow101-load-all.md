# Workflow 101: `devtools::load_all()`

## Table of Contents

1. [What `load_all()` Does](#what-load_all-does)
2. [Why It’s Central](#why-its-central)
3. [The Fast Dev Loop](#the-fast-dev-loop)
4. [When You Still Need Install or Restart](#when-you-still-need-install-or-restart)
5. [Common Pitfalls](#common-pitfalls)
6. [What `load_all()` Does _Not_ Do](#what-load_all-does-not-do)
7. [Related Tools](#related-tools)
8. [Troubleshooting](#troubleshooting)
9. [References](#references)

## What `load_all()` Does

`devtools::load_all()` loads your package directly from the source tree (the
working directory) instead of from an installed copy in a library. The goal is
to make iteration cheap: you edit files under `R/` and then re-load.

It is conceptually similar to repeatedly calling `source()` on all your R files,
plus the extra work needed to approximate a “real” package load.

Practical mental model:

- `load_all()` is for _developer speed_.
- `R CMD check` is for _integration truth_.

## Why It’s Central

The r-lib development workflow assumes you will iterate many times before you
run a full `R CMD check`. `load_all()` is the core mechanism that keeps those
iterations fast.

Use `load_all()` when you want to:

- Try a new function immediately after editing.
- Sanity-check edge cases interactively.
- Develop documentation/examples alongside code (paired with `document()`).

## The Fast Dev Loop

This is the intended daily loop:

1. Edit code under `R/`.
2. Reload with `devtools::load_all()`.
3. Try a minimal example.
4. If you changed exports or roxygen, run `devtools::document()`.
5. Periodically run `devtools::check()`.

Example pattern:

```r
devtools::load_all()

# Test-drive the change
my_fun(1)

# If you edited roxygen blocks / exports
devtools::document()

# When ready for a fuller gate
devtools::check()
```

Decision rule: if you edited roxygen tags/exports/imports, run `document()` first
or immediately after (and expect `NAMESPACE` to change).

## When You Still Need Install or Restart

`load_all()` is ideal for most R-level code changes, but there are situations
where you should do something heavier:

- You changed compiled code (C/C++/Fortran) and need a rebuild.
- You are debugging behavior that depends on the installed state.
- You are seeing confusing symptoms that look like stale objects lingering.

When in doubt, prefer to validate with `devtools::check()` (which runs in a
cleaner, more package-like context).

Also consider restarting your R session when:

- you removed or renamed functions and old objects are still hanging around
- you changed options/env vars and can’t tell what state you’re in
- you suspect a loaded dependency is masking/overriding behavior

## Common Pitfalls

- **Forgetting to re-load:** You edit code, but you’re still running an old definition.
- **Stale documentation / exports:** You changed roxygen tags but didn’t run `devtools::document()`, so `NAMESPACE` and `man/` are out of sync.
- **Assuming interactive success implies check success:** interactive testing is necessary but not sufficient; check exercises more surfaces.

Other common pitfalls:

- **Relying on attached packages**: `load_all()` + your session may have lots of packages
  attached; `check()` runs in a clean session. Prefer explicit `pkg::fun()` calls.
- **State leakage**: objects in `.GlobalEnv`, options, temp files, caches.
- **Not noticing masked functions**: your dev session may mask base/other-package symbols.

## What `load_all()` Does _Not_ Do

`load_all()` is not a replacement for these:

- `devtools::document()` (regenerating `man/` and `NAMESPACE`)
- `devtools::test()` (running tests in a controlled way)
- `devtools::check()` (the check surface: examples, tests, vignettes, Rd validity)

It also won’t reliably catch:

- missing `DESCRIPTION` dependencies that happen to be installed locally
- file/path assumptions that only fail in a clean checkout
- problems that only show up when the package is installed

## Troubleshooting

### “My changes aren’t showing up”

- You forgot to re-run `devtools::load_all()` after editing.
- You’re testing an installed copy (via `library()`) instead of your dev version.

Fix: run `devtools::load_all()` and re-test.

If you are still seeing old behavior:

- restart your R session
- confirm you are not calling `library(yourpkg)` (installed version) by habit

### “Docs / NAMESPACE look stale”

`load_all()` doesn’t regenerate derived docs.

Fix:

```r
devtools::document()
```

Then reload and preview.

### “Works in load_all(), fails in check()”

This often indicates:

- hidden dependency
- reliance on attached packages
- a path/state assumption

Fix: reproduce with `devtools::check()` and use the `r-lib/r-cmd-check-ci` playbooks.

If you want to narrow it down:

- docs/examples failures → `devtools::check_man()`
- test failures → `devtools::test()`

## Related Tools

- `devtools::document()` (keep `man/*.Rd` and `NAMESPACE` up to date)
- `devtools::check()` (integration-quality gate)

## References

- R Packages (2e), “Fundamental workflows”: https://r-pkgs.org/workflow101.html
- devtools reference: https://devtools.r-lib.org/reference/load_all.html
