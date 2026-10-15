---
name: r-cran-status
description: Look up an R package's live status on cran.r-project.org - submission/review state (queue, human review, waiting, archived, past version's fate) or R CMD check results (OK/NOTE/WARN/ERROR per platform). Use for "what's the CRAN status of X", "did X get accepted/rejected", "is X passing CRAN checks", "when was version Y archived", "did win-builder get my package", "is win-builder processing my submission".
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0.1"
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

CRAN's servers are a shared, unpaid resource. Never issue requests in
parallel or in a tight loop — pause briefly (e.g. `sleep 1`) between
requests, stop looping as soon as a match is found, and avoid re-fetching a
page you've already checked in this session.

## Workflow

1. Ask for the package name if not provided. A version may also be given
   (e.g. `btw v1.4.0` or `btw 1.4.0`); strip any leading `v`.
2. Decide which question is being asked:
   - Version given, or request mentions submission, review, the queue, or
     rejection/archival → **Submission Status**.
   - Request mentions checks, `R CMD check`, WARN/ERROR/NOTE, or
     platforms/flavors → **Check Results**.
   - Request mentions win-builder, `check_win_devel()`, or whether a
     submission arrived → **Win-Builder**.
   - If genuinely ambiguous (e.g. just "check the CRAN status of x"), ask
     which is meant, or check both and report both.
3. Follow the relevant section below and report the result.

## Submission Status

1. Check the currently published version first (see below).
2. If no version was requested, or it matches the current version: report it
   as the current, published release. Skip to step 5 unless it's absent from
   `PACKAGES`, in which case continue to step 3.
3. If a prior check this conversation already located the package in a
   stage or reviewer folder, check that folder first, then forward from it
   in the pipeline order (see "CRAN Review Stages") — don't re-sweep from
   the start. Otherwise, sweep all stage and reviewer folders.
4. Search the `incoming/` stage folders (see below).
5. Search the reviewer-assigned folders (see below).
6. If a specific version was requested and doesn't match the current
   published version (or the package isn't published at all), check the
   CRAN Archive for that version (see below).
7. Report the result (see "Reporting Submission Status Results").

## CRAN Review Stages

Listed in typical pipeline order — a package usually moves top to bottom,
though not every package passes through every stage:

- `inspect` / `newbies`: awaiting initial manual inspection (`newbies` is for
  first-time submitters)
- `pending`: awaiting closer review
- `human/<initials>`: assigned to a CRAN reviewer
- `pretest`: automated checks (re)running
- `waiting`: CRAN is waiting for a maintainer response (loops back to
  `pretest` once the maintainer responds)
- `recheck`: reverse-dependency checks
- `publish`: approved and awaiting publication
- `archive`: rejected

## Checking Incoming Stage Folders

Replace `{package}` with the actual package name. Start at the last-known
stage if one exists (see Submission Status step 3), else at `inspect`:

```sh
for stage in inspect newbies pending pretest waiting recheck publish archive; do
  curl -Ls "https://cran.r-project.org/incoming/$stage/" |
    grep -Eio '[^"]*{package}[^"]*' &&
    echo "Stage: $stage" && break
  sleep 1
done
```

## Checking Reviewer-Assigned Folders

Reviewer-initials folders (e.g. `human/KH`) change as CRAN's team changes,
so discover them from the `incoming/` listing instead of a fixed set: any
folder there that isn't one of the stage names above is a reviewer folder.

```sh
reviewer_folders=$(
  curl -Ls "https://cran.r-project.org/incoming/" |
    grep -Eio '<a href="[^"]+/">' |
    sed -E 's/<a href="([^"]+)\/">/\1/' |
    grep -Ev '^(inspect|newbies|pending|pretest|publish|recheck|archive|waiting|special)$'
)

for stage in $reviewer_folders; do
  curl -Ls "https://cran.r-project.org/incoming/$stage/" |
    grep -Eio '[^"]*{package}[^"]*' &&
    echo "Stage: human/$stage" && break
  sleep 1
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

## Win-Builder

Win-builder (win-builder.r-project.org) runs `R CMD check` on Windows for
packages submitted via `devtools::check_win_devel()` (or
`check_win_release()` / `check_win_oldrelease()`): the tarball is uploaded
by anonymous FTP to `ftp://win-builder.r-project.org/<flavor>/` (`R-devel`,
`R-release`, or `R-oldrelease`), and results are emailed to the maintainer
address in `DESCRIPTION`, usually within 15-30 minutes. A local success
message only means the upload command finished — verify receipt on the
server.

1. **Upload receipt (authoritative).** The tarball should be listed in the
   flavor's FTP folder:

   ```sh
   curl ftp://win-builder.r-project.org/R-devel/
   ```

   Listed = uploaded and queued. Server timestamps are European time
   (CEST/CET) — offset them when comparing to local submission time.

2. **Progress.** Once win-builder picks the file up, it appears in the
   pretest listing:

   ```sh
   curl -Ls https://win-builder.r-project.org/incoming_pretest/ |
     grep -i {package}
   ```

   Entries look like `{package}_{version}_{yyyymmdd}_{hhmmss}` and appear
   only once checking starts; logs live inside each entry (e.g.
   `00check.log`). Entries linger for months — match version and date,
   not just the package name.

Gotchas:

- A missing `incoming_pretest` entry ≠ failed upload — entries lag behind
  the FTP listing, which is the authoritative arrival check; queues can
  jam for hours, and the listing's backlog shows it.
- Don't advise resubmitting while the tarball is still listed — it's
  queued, and a duplicate won't speed it up.
- Tarball gone but no email? The run likely finished; check the
  maintainer's spam folder and `incoming_pretest/` for a recent entry
  matching the version. Nothing after several hours → ask R-package-devel
  rather than resubmit.
