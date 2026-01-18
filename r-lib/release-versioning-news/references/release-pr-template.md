# Release PR template

Use this as a starting point for a release pull request description.

The goal is to make the release auditable: version, checks, and impact are clear.

```text
## Release
Version: x.y.z

## Summary
- <1–5 bullets describing user-visible changes>

## Checks
- devtools::check(): ✅
- R CMD check --as-cran (tarball): ✅ / N/A
- CI (linux/mac/windows): ✅ / N/A

## Revdeps
Checked: <N>
New failures: <N>
Notes: <short explanation>

## CRAN
- Submitting to CRAN: yes/no
- cran-comments.md: prepared / N/A

## Post-release
- Bump to dev version: yes/no
- Opened follow-up issues: <links>
```
