---
name: r-lib/revdep-checks
description: >
  Running reverse dependency checks for R packages and interpreting the results.
  Use this skill when you need to:
  (1) Run revdep checks prior to a release,
  (2) Classify downstream failures (your change vs downstream fragility),
  (3) Produce a concise revdep summary for release notes or CRAN comments,
  (4) Decide whether to patch, revert, or coordinate with downstream maintainers.
  Also use when you need a repeatable, low-drama revdep workflow.
---

# Reverse Dependency Checks

## When to Use What

| Task                                 | Use                            |
| ------------------------------------ | ------------------------------ |
| Confirm your package itself is clean | `devtools::check()`            |
| Run reverse dependency checks        | `revdepcheck::revdep_check()`  |
| Produce an HTML report               | `revdepcheck::revdep_report()` |
| Reset the revdep library/state       | `revdepcheck::revdep_reset()`  |
| Summarize revdep results for a PR    | Use the template in references |

## What revdepcheck is doing (why it’s useful)

revdepcheck is designed to reduce false positives by checking each reverse dependency twice:

- once against the CRAN version of your package
- once against your local development version

It then reports the _differences_, so you can focus on problems introduced by your change.

## Practical workflow

1. **Get your package clean first**
   - `devtools::check()`
2. **Create a release candidate**
   - Make one commit/branch that represents “what you intend to ship”.
3. **Run revdeps in a separate process**
   - revdep checks are long-running; run them in a separate R session/terminal.
   - (Re)start from a clean state: `revdepcheck::revdep_reset()`.
   - Run checks: `revdepcheck::revdep_check(num_workers = 4)`.
4. **Monitor and triage**
   - While checks run, use `revdepcheck::revdep_summary()` and `revdepcheck::revdep_details()`.
   - Generate a human report: `revdepcheck::revdep_report()`.
5. **Decide and act**
   - fix with backward compatibility
   - coordinate downstream patches (and allow time)
   - document expected impact clearly (NEWS / cran-comments)

## How to interpret failures

- If many downstream packages fail in the same way, assume your change is the trigger.
- If failures are flaky, network-related, or clearly unrelated to your package’s surface area, treat as downstream noise.
- Always reproduce at least one representative failure locally before drawing conclusions.

Triage heuristics that work well:

- **New failures are the priority** (revdepcheck marks new problems vs existing failures).
- Prefer looking at the _first_ error in a failing downstream log.
- If a downstream failure is a strict check on behavior you changed intentionally, treat it like a coordination problem (not necessarily a “bug”).

## References

- [references/revdepcheck-workflow.md](references/revdepcheck-workflow.md)
- [references/interpreting-revdep-results.md](references/interpreting-revdep-results.md)
- [references/release-readiness-and-revdeps.md](references/release-readiness-and-revdeps.md)
- [references/downstream-triage-playbook.md](references/downstream-triage-playbook.md)
- [references/revdep-summary-template.md](references/revdep-summary-template.md)

## External resources

- revdepcheck package: https://r-lib.github.io/revdepcheck/
- R Packages (2e): Releasing a package: https://r-pkgs.org/release.html
