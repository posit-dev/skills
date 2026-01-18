# Release readiness and revdeps

Reverse dependency checks are most valuable when they’re tied to a specific release candidate.

## Suggested release gate

- Clean `devtools::check()` for your package.
- Run revdeps for the release candidate.
- If you introduced a breaking change:
  - decide whether to restore backward compatibility, or
  - ship the break with clear communication.

If your change is likely to disrupt important reverse dependencies, consider coordinating ahead of time (or at least allowing time) before releasing.

## CRAN interplay

If CRAN reviewers ask about impact, a short revdep summary in `cran-comments.md` can be useful.

## A good PR note

Include a short section in the release PR:

- “Revdeps: checked N packages; failures: M; analysis: …”
