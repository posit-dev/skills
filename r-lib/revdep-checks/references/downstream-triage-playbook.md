# Downstream triage playbook

This reference is an opinionated triage workflow for reverse dependency failures.

Goal: efficiently determine whether a revdep failure is caused by your change, and what you should do about it.

## Step 0: Focus on _new_ failures

revdepcheck is designed to surface differences between:

- the CRAN version of your package
- your local release candidate

Prioritize packages flagged as having new failures.

## Step 1: Find the first real error

Within a downstream log:

- skip past installation noise
- locate the first “ERROR” (or failing test)
- treat later failures as possibly cascading

## Step 2: Classify the failure

### A) Compile/install failures

Common causes:

- you changed or removed exported symbols used in compiled code
- you tightened C/C++ headers, registration, or linking behavior

Common actions:

- restore backward-compatible entry points when feasible
- provide a deprecation window
- coordinate with maintainers if removal is unavoidable

### B) Check/test failures

Common causes:

- changed return values/types
- changed error messages or error classes
- stricter input validation

Common actions:

- decide whether the old behavior was part of the intended API
- document behavior changes in NEWS
- add compatibility shims where justified

### C) Environmental failures

Common causes:

- network calls
- timeouts
- external services
- OS-specific system libraries

Common actions:

- treat as downstream noise unless your change plausibly triggers it
- if your change increases runtime, treat timeouts as a signal

## Step 3: Reproduce one representative failure

Pick at least one “high signal” failure (new, clearly related to your package).

Reproduction strategy:

- install your release candidate in a clean library
- install the downstream package
- run its tests or `R CMD check`

## Step 4: Choose a response strategy

### Fix in your package

Prefer this when:

- the downstream usage is reasonable
- the change was accidental
- you can maintain compatibility cheaply

### Coordinate

Prefer this when:

- the downstream package is relying on behavior you intentionally changed
- you need to remove an API surface

Provide maintainers:

- a minimal reproducible example
- a suggested patch or workaround
- a timeframe (especially if you submit to CRAN)

### Document and proceed

Prefer this when:

- failures are clearly pre-existing or unrelated
- the change is intentional and acceptable

In this case, ensure you have:

- NEWS entries that describe the impact
- a revdep summary for your release PR / cran-comments (if relevant)
