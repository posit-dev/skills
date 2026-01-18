# cran-comments.md and reviewer responses

CRAN submissions usually go smoother when `cran-comments.md` is crisp, factual, and minimal.

Treat `cran-comments.md` as a release artifact:

- it helps you submit confidently
- it helps CRAN reviewers understand what changed
- it gives you a stable place to record the exact rationale for any remaining NOTE

## A good default template

```text
## Test environments
* local R installation, R X.Y.Z
* GitHub Actions (ubuntu-latest, macos-latest, windows-latest)
* (optional) win-builder / macbuilder

## R CMD check results
0 errors | 0 warnings | 0 notes

## Reverse dependencies
(If you ran them, summarize briefly; otherwise omit.)

## Comments
- Summary of changes (1–5 bullets).
- Any NOTE(s): what they are and why they are expected.

## Resubmission
(Only include this section for resubmissions.)

* Reviewer comment 1:
	- Action taken:
	- Where to see it (file/function):

* Reviewer comment 2:
	- Action taken:
	- Where to see it (file/function):
```

## How to write responses

- Quote the reviewer request briefly.
- State what you changed.
- Point to the exact file(s) affected (e.g., `DESCRIPTION`, `man/*`, `R/*`).
- Avoid arguing; prefer adapting.

If CRAN says something is a problem, your goal is usually to either:

- remove the issue entirely, or
- make the behavior explicitly conditional / robust, with a clear explanation.

## Handling NOTES

Only keep a NOTE if:

- it’s genuinely unavoidable, and
- you can justify it clearly.

If a NOTE indicates a potential policy violation (e.g., long-running examples), treat it as a fix request, not a documentation exercise.
