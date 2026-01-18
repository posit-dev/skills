# Release checklist

Use this checklist for a routine release.

## 1) Update versions and notes

- Choose a version bump.
- Update `NEWS.md`.

Practical approach:

- use `usethis::use_version("patch"|"minor"|"major")` to standardize the version bump
- then edit `NEWS.md` so it’s user-facing and complete

## 2) Quality gate

- `devtools::check()` is clean.
- If relevant, run revdeps.

If you plan to submit to CRAN:

- run `R CMD check --as-cran` on the source tarball at least once
- ensure any NOTE is either fixed or explained crisply in `cran-comments.md`

## 3) Release

- Tag the release (and create a GitHub release if that’s your workflow).
- If you submit to CRAN, prepare `cran-comments.md`.

If your workflow includes a release PR:

- put the checklist + revdep summary in the PR description
- ensure CI is green on the release commit

## 4) Post-release

- Bump to a development version if that’s your convention.
- Start a new empty NEWS section for the next cycle.

If you use dev versions, a common pattern is:

- release `x.y.z`
- immediately bump to `x.y.z.9000`
