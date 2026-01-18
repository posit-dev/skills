# Interpreting revdep results

The goal is not “zero downstream failures”. The goal is “understand the impact of your change” and act responsibly.

revdepcheck is especially useful because it highlights _new_ problems caused by your local version, compared to the CRAN version.

## Classify each failure

- **Likely your fault**

  - compilation errors due to changed exported functions
  - changed return types or error classes
  - stricter argument validation

- **Likely downstream/environmental**

  - network access failures
  - timeouts
  - flaky tests unrelated to your package’s API

- **Ambiguous / needs investigation**
  - failures that look like “undefined behavior” downstream (tests relied on accidental behavior)
  - failures caused by tightened checks (e.g., you now error earlier)

## Reproduce representative failures

Pick 1–3 failures that look most likely to be triggered by your change and reproduce them locally if feasible.

Practical reproduction strategy:

1. Open the downstream package’s revdepcheck log and find the _first_ failure.
2. Identify whether the failure is:

- compile-time (C/C++/R CMD INSTALL)
- check-time (tests/examples)

3. Try to reproduce in a clean environment:

- install your release candidate
- install the downstream package
- run its tests / check

## Produce a summary

For release PRs and CRAN comments, summarize:

- how many downstream packages you checked
- how many failed
- what you changed (API/behavior)
- what you fixed (if anything)
- any coordinated downstream patches (links)

When possible, separate:

- new failures introduced by your release candidate
- pre-existing downstream failures
