---
name: r-lib/release-versioning-news
description: >
  Versioning and release note workflows for R packages, centered on `NEWS.md`
  and usethis helpers. Use this skill when you need to:
  (1) Choose and apply a version bump,
  (2) Create and maintain `NEWS.md` with user-facing entries,
  (3) Prepare a release PR and run appropriate checks,
  (4) Tag a release and do post-release version bumps.
  Also use when release notes are drifting toward implementation detail rather
  than user impact.
---

# Release Versioning and NEWS

## When to Use What

| Task                          | Use                                                           |
| ----------------------------- | ------------------------------------------------------------- |
| Initialize `NEWS.md`          | `usethis::use_news_md()`                                      |
| Bump released version         | `usethis::use_version("patch")` (or `"minor"` / `"major"`)    |
| Bump to a development version | `usethis::use_version("dev")` or `usethis::use_dev_version()` |
| Run the release quality gate  | `devtools::check()`                                           |
| Tighten loop on docs/examples | `devtools::check_man()`                                       |
| Run revdeps when risk is high | `revdepcheck::revdep_check()`                                 |

Revdeps are their own workflow and failure-triage problem; this skill only helps you decide when they’re worth the cost.
For the full revdep playbook, use: [r-lib/revdep-checks](../revdep-checks/).

## Practical workflow

1. **Prepare the release candidate**

- Ensure `main` (or your release branch) is green.
- Decide whether the release includes breaking changes.

2. **Update version + NEWS**

- Use `usethis::use_version("patch"|"minor"|"major")`.
- Write NEWS entries that describe user-visible behavior changes.

3. **Run the quality gate**

- `devtools::check()`
- Run revdeps when the change is risky or widely used.

4. **Release**

- Tag the release (and create a GitHub release if that’s your workflow).
- If submitting to CRAN, prepare `cran-comments.md`.

5. **Post-release**

- If you use dev versions, bump to `x.y.z.9000` via `usethis::use_version("dev")`.
- Start a new empty NEWS section for the next cycle.

## What usethis does (important detail)

`usethis::use_version()` updates the `Version` field in `DESCRIPTION`, adds a new heading to `NEWS.md` (if it exists), and commits those changes if the project uses Git.

## References

- [references/versioning.md](references/versioning.md)
- [references/news-md-conventions.md](references/news-md-conventions.md)
- [references/release-checklist.md](references/release-checklist.md)
- [references/release-pr-template.md](references/release-pr-template.md)

## External resources

- R Packages (2e): Releasing a package: https://r-pkgs.org/release.html
- usethis (versioning): https://usethis.r-lib.org/reference/use_version.html

## Related skills

- [r-lib/revdep-checks](../revdep-checks/) - Running and interpreting reverse dependency checks
- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/) - The release quality gate (`R CMD check`) and CI
- [r-lib/cran-submission](../cran-submission/) - If the release is going to CRAN
