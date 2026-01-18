---
name: r-lib/cran-submission
description: >
  Preparing an R package for CRAN submission (new submissions and updates).
  Use this skill when you need to:
  (1) Run CRAN-style checks (`R CMD check --as-cran` or equivalent via devtools),
  (2) Interpret and resolve CRAN-relevant ERROR/WARNING/NOTE output,
  (3) Verify DESCRIPTION metadata and packaging expectations,
  (4) Write or update `cran-comments.md` for submission/resubmission,
  (5) Handle common CRAN friction points (examples runtime, suggested packages,
  large files, incoming checks, platform-specific issues),
  (6) Prepare a crisp response to CRAN reviewer feedback.
  Also use when deciding whether an issue is safe to ignore, needs mitigation,
  or requires a different implementation strategy.
---

# CRAN Submission

## When to Use What

| Task                                           | Use                                                         |
| ---------------------------------------------- | ----------------------------------------------------------- |
| Run a full local check                         | `devtools::check()`                                         |
| Run CRAN-style checks locally                  | `devtools::check(args = "--as-cran")`                       |
| Run the closest-to-CRAN check (tarball)        | `R CMD build` then `R CMD check --as-cran pkg_x.y.z.tar.gz` |
| Tighten loop on docs/examples                  | `devtools::check_man()`                                     |
| Confirm suggested packages for local checking  | `devtools::install_deps(dependencies = TRUE)`               |
| Record submission notes and reviewer responses | `cran-comments.md`                                          |
| Preflight on platforms you don’t have          | win-builder / macbuilder                                    |

## The CRAN-quality gate (recommended order)

1. **Make `R CMD check` boring**
   - `devtools::check()` is clean.
2. **Make it CRAN-like**
   - Prefer a tarball check: `R CMD build` then `R CMD check --as-cran pkg_x.y.z.tar.gz`.
   - Use `devtools::check(args = "--as-cran")` for a faster iteration loop.
3. **Cross-platform confidence**
   - Run CI on Linux/macOS/Windows if feasible.
   - Use hosted check services when you don’t have local access.
4. **Policy + metadata sanity**
   - DESCRIPTION fields are correct and complete.
   - Any remaining NOTE is either fixed or explained crisply in `cran-comments.md`.
5. **Submission hygiene**
   - Changes are summarized for humans (NEWS/release notes).
   - You’re ready to respond point-by-point if CRAN asks.

## The CRAN submission mindset

- Assume checks run in a minimal environment with no hidden dependencies.
- Anything slow, flaky, networked, interactive, or that writes outside tempdirs will eventually fail.
- Prefer fixes that make checks green everywhere over explanations that justify fragility.

## Typical triage patterns

- **ERRORs**: treat as blockers.
- **WARNINGs**: almost always treat as blockers.
- **NOTEs**: split into:
  - _actionable_ (e.g., undeclared dependency, broken URL checks, too-long examples)
  - _contextual_ (e.g., incoming feasibility NOTE for new submission)

When you keep a NOTE, `cran-comments.md` should answer:

1. What is the NOTE?
2. Why does it happen?
3. Why is it safe/expected?
4. What did you do to minimize it?

## Common CRAN failure surfaces (high frequency)

- **Undeclared dependencies**: code/examples/tests call packages not in DESCRIPTION.
- **Examples too slow / unreliable**: network calls, randomness, external services.
- **Non-portable paths**: writing to the working directory; assuming files exist.
- **Package size / long-running vignettes**: large PDFs/data, heavy computations.
- **Policy gotchas**: writing to user directories, using `:::` on base packages, downloading on install.

## References

- [references/as-cran-checks.md](references/as-cran-checks.md)
- [references/cran-submission-checklist.md](references/cran-submission-checklist.md)
- [references/common-cran-notes.md](references/common-cran-notes.md)
- [references/cran-comments-and-responses.md](references/cran-comments-and-responses.md)
- [references/cran-policy-gotchas.md](references/cran-policy-gotchas.md)

## Related skills

- [r-lib/r-cmd-check-ci](../r-cmd-check-ci/)
- [r-lib/testing-r-packages](../testing-r-packages/)
- [r-lib/documentation-roxygen2-pkgdown](../documentation-roxygen2-pkgdown/)
- [r-lib/release-versioning-news](../release-versioning-news/) - Version bumps + NEWS, often needed for submissions/resubmissions
- [r-lib/revdep-checks](../revdep-checks/) - Revdeps as a release/CRAN-risk signal for widely used packages

## External resources

- CRAN repository policy: https://cran.r-project.org/web/packages/policies.html
- CRAN submission checklist: https://cran.r-project.org/web/packages/submission_checklist.html
- Writing R Extensions (R CMD check): https://cran.r-project.org/doc/manuals/r-release/R-exts.html
- R Packages (2e): Appendix A — R CMD check: https://r-pkgs.org/R-CMD-check.html
- R Packages (2e): DESCRIPTION: https://r-pkgs.org/description.html

Common pre-submission check services:

- win-builder: https://win-builder.r-project.org/
- macbuilder: https://mac.r-project.org/macbuilder/submit.html
