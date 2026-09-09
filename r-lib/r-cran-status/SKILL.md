---
name: r-cran-status
description: Look up an R package's live status on cran.r-project.org - submission/review state (queue, human review, waiting, archived, past version's fate) or R CMD check results (OK/NOTE/WARN/ERROR per platform). Use for "what's the CRAN status of X", "did X get accepted/rejected", "is X passing CRAN checks", "when was version Y archived".
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# CRAN Package Status

Check a package's submission/review state, a specific historical version's
fate (e.g. `{package} {version}`, as in `btw v1.4.0`), or its current
`R CMD check` results across CRAN's test platforms.

"CRAN status" is ambiguous between two questions:

- **Submission status**: is/was this package (or version) in review,
  published, archived, or rejected? See "Submission Status".
- **Check results**: is the published version passing `R CMD check` on all
  platforms, or does it have WARN/ERROR/NOTE flags risking removal? See
  "Check Results".

## Workflow

1. Ask for the package name if not provided. A version may also be given
   (e.g. `btw v1.4.0` or `btw 1.4.0`); strip any leading `v`.
2. Decide which question is being asked:
   - Version given, or request mentions submission, review, the queue, or
     rejection/archival → **Submission Status**.
   - Request mentions checks, `R CMD check`, WARN/ERROR/NOTE, or
     platforms/flavors → **Check Results**.
   - If genuinely ambiguous (e.g. just "check the CRAN status of x"), ask
     which is meant, or check both and report both.
3. Follow the relevant section below and report the result.

## Submission Status

1. Check the currently published version first (see below).
2. If no version was requested, or it matches the current version: report it
   as the current, published release. Skip to step 5 unless it's absent from
   `PACKAGES`, in which case continue to step 3.
3. Search the `incoming/` stage folders (see below).
4. Search the reviewer-assigned folders (see below).
5. If a specific version was requested and doesn't match the current
   published version (or the package isn't published at all), check the
   CRAN Archive for that version (see below).
6. Report the result (see "Reporting Submission Status Results").

## CRAN Review Stages

- `inspect`: awaiting manual inspection
- `newbies`: first-time submission inspection queue
- `pending`: awaiting closer review
- `human/<initials>`: assigned to a CRAN reviewer
- `waiting`: CRAN is waiting for a maintainer response
- `pretest`: automated checks rerunning after a fix
- `archive`: rejected
- `recheck`: reverse-dependency checks
- `publish`: approved and awaiting publication

## Checking Incoming Stage Folders

Replace `{package}` with the actual package name:

```sh
for stage in inspect newbies pending pretest publish recheck waiting archive; do
  curl -Ls "https://cran.r-project.org/incoming/$stage/" |
    grep -Eio '[^"]*{package}[^"]*' &&
    echo "Stage: $stage"
done
```

## Checking Reviewer-Assigned Folders

```sh
for stage in BA KH KL LH SU Tyagi UL VW; do
  curl -Ls "https://cran.r-project.org/incoming/$stage/" |
    grep -Eio '[^"]*{package}[^"]*' &&
    echo "Stage: $stage"
done
```

## Checking Whether the Package Is Already Published

```sh
curl -Ls https://cran.r-project.org/src/contrib/PACKAGES |
  awk -v pkg="{package}" '
    $0 == "Package: " pkg { found=1 }
    found && /^Version:/ { print; exit }
  '
```

A printed `Version:` line is the current CRAN version. Remember it — needed
later to say whether a requested older version was "superseded by" it.

## Checking a Specific Version in the CRAN Archive

Superseded versions move out of `src/contrib/` into a per-package archive
folder. This `Archive` is unrelated to the `archive` `incoming/` stage above
(that means "rejected"; this means "an older version, since superseded").

```sh
curl -Ls "https://cran.r-project.org/src/contrib/Archive/{package}/" |
  grep -Eio '[^"]*{package}_{version}\.tar\.gz[^"]*'
```

A matching `.tar.gz` filename means that exact version was published and has
since been superseded.

## Reporting Submission Status Results

- **No version requested:**
  - Present in `PACKAGES`: report as published, with current version.
  - Else found in an `incoming/` or reviewer folder: report the folder name
    and meaning from the stage list above.
  - Else: report it wasn't found in CRAN's submission queue or index.
- **Specific version requested:**
  - Matches current version in `PACKAGES`: report as the current release.
  - Else found in the CRAN Archive: report it was published and has been
    superseded by the current version (from `PACKAGES`), e.g. "available in
    the archive, superseded by v1.5.0".
  - Else the package (any version) is found in an `incoming/` or reviewer
    folder: report that stage, noting the requested version wasn't a past
    release.
  - Else: report the requested version wasn't found (current, archived, or
    in-review).

## Check Results

CRAN publishes per-platform `R CMD check` results for every published
package at `https://cran.r-project.org/web/checks/check_results_{package}.html`.
WARN or ERROR results persisting more than ~2-4 weeks risk archival by CRAN.

Fetch and simplify the results table:

```sh
curl -Ls "https://cran.r-project.org/web/checks/check_results_{package}.html" |
  grep '<tr> <td>' |
  sed -E 's/<[^>]+>/ /g' |
  awk '{print $1": "$NF}'
```

Prints one `flavor: STATUS` line per row, e.g.:

```
r-devel-linux-x86_64-debian-clang: OK
r-oldrel-windows-x86_64: ERROR
```

Status is `OK`, `NOTE`, `WARN`, or `ERROR`. For any non-`OK` flavor, full
failure output is further down the same page under "Check Details" — fetch
again without stripping tags and read the `<pre>`-formatted section after
the failing flavor's `Version:` / `Check:` / `Result:` lines.

A 404 means no CRAN check history — likely not currently published. Check
submission status instead.

### Reporting Check Results

- Every flavor `OK`: report the package passes checks on all platforms.
- Any flavor `NOTE`/`WARN`/`ERROR`: list affected flavors and status,
  summarize failure reason(s) from "Check Details", and note that
  persistent WARN/ERROR can lead to archival.
- Page 404s: report no check results exist; check/report submission status
  instead.
