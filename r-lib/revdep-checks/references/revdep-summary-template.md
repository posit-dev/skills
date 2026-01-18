# Revdep summary template

Use this template in a release PR description, a GitHub release, or `cran-comments.md`.

Keep it short and factual.

## Option A: Release PR summary

```text
## Revdeps
Checked: <N> reverse dependencies (via revdepcheck)
New problems: <N> (listed below)

### Summary
- <1–3 bullets describing the impact>

### New failures
- <pkg>: <one-line summary + link to issue/PR if you opened one>
- <pkg>: ...

### Notes
- <any important caveats, e.g. known flaky downstream tests>
```

## Option B: CRAN comments summary

```text
## Reverse dependencies
I ran revdep checks on <N> reverse dependencies.
There were <N> new failures compared to the CRAN version of this package.

- <pkg>: <one-line summary>
- <pkg>: <one-line summary>

(Any failures appear unrelated to changes in this update / were pre-existing / were investigated as described above.)
```

## What to include (and what to omit)

Include:

- how many revdeps you checked
- whether failures are new vs existing
- high-level cause for any new failures

Omit:

- long stack traces
- speculation
- detailed logs (link them if needed)
