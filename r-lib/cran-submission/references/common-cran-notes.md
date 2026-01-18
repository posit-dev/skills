# Common CRAN NOTEs: what they usually mean

This reference groups common `R CMD check` NOTE patterns that often come up during CRAN submission, along with practical mitigation strategies.

This is not exhaustive and does not override CRAN policy, but it’s a useful triage map.

## “CRAN incoming feasibility … NOTE” (new submissions)

Typical situation:

- New package submissions often produce an “incoming feasibility” NOTE.

What to do:

- Read it carefully.
- If it is purely informational and your checks are otherwise clean, you typically explain it briefly in `cran-comments.md`.
- If it points at something actionable (URLs, size, missing metadata), fix the root cause.

## “Possibly mis-spelled words in DESCRIPTION”

Typical cause:

- DESCRIPTION contains proper nouns, package names, acronyms, or domain-specific terms.

What to do:

- Make sure the Description is well-written and not just a list of keywords.
- If it’s legitimate spelling noise, you can explain briefly in `cran-comments.md`.

## “Found the following (possibly) invalid URLs”

Typical causes:

- A URL redirects unexpectedly.
- A URL is temporarily down.
- A URL includes characters that URL checks dislike.

What to do:

- Prefer stable canonical URLs.
- Avoid URLs that require authentication.
- Replace brittle links (e.g., “latest” URLs) with stable permalinks where possible.

## “Namespace in Imports field not imported from …”

Typical cause:

- A package is listed in `Imports` but nothing is used from it (or it’s only used conditionally).

What to do:

- If it’s a hard runtime dependency, ensure the code actually uses it and it’s imported properly.
- If it’s optional, move to `Suggests` and guard calls with `requireNamespace()`.

## “Package has a ‘License’ field that is not a standard CRAN license”

Typical cause:

- License metadata is incomplete or non-standard.

What to do:

- Prefer a standard license identifier where possible.
- If you use `MIT + file LICENSE`, ensure the LICENSE file is present and correct.
- If you change a license between releases, highlight it in the submission.

## “Package size” / “installed size” notes

Typical causes:

- Large datasets embedded in the package.
- Large PDF vignettes or other documentation artifacts.

What to do:

- Keep data and docs as small as possible.
- Consider separating large datasets into a data-only package or external hosting (if appropriate for your users).

## “Examples … too long” / timeouts

Typical cause:

- Examples/vignettes are doing real work (network calls, long computations).

What to do:

- Make examples fast and deterministic.
- Move heavy content to vignettes (and keep vignettes reasonable too).
- Ensure tests validate correctness without requiring expensive runs.

## References

- CRAN policy: https://cran.r-project.org/web/packages/policies.html
- CRAN submission checklist: https://cran.r-project.org/web/packages/submission_checklist.html
