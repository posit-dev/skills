# Git and GitHub for package development

## Table of Contents

- [Why Git early](#why-git-early)
- [A minimal Git setup](#a-minimal-git-setup)
- [What goes in .gitignore vs .Rbuildignore](#what-goes-in-gitignore-vs-rbuildignore)
- [Connecting to GitHub](#connecting-to-github)
- [Credentials and authentication (PAT vs SSH)](#credentials-and-authentication-pat-vs-ssh)
- [Branching and pull requests](#branching-and-pull-requests)
- [Keeping your branch up to date](#keeping-your-branch-up-to-date)
- [Working with forks](#working-with-forks)
- [What to commit in an R package](#what-to-commit-in-an-r-package)
- [Commit discipline (small, reviewable steps)](#commit-discipline-small-reviewable-steps)
- [Keeping main green (local vs CI)](#keeping-main-green-local-vs-ci)
- [Release and tagging basics](#release-and-tagging-basics)
- [Recommended GitHub repo settings](#recommended-github-repo-settings)
- [How this connects to CI and pkgdown](#how-this-connects-to-ci-and-pkgdown)
- [Common pitfalls](#common-pitfalls)
- [References](#references)

## Why Git Early

Use Git early so you can:

- Review diffs while you’re still forming APIs.
- Bisect or revert regressions.
- Collaborate safely (branches/PRs).
- Prepare for automation (CI checks, pkgdown deploy).

In package development, Git is part of the quality loop: it makes changes visible
and reviewable.

## A Minimal Git Setup

For most packages:

```r
usethis::use_git()
```

This initializes the repository and sets you up to commit early.

Add ignores early too, especially for local and generated files:

```r
usethis::use_git_ignore(c(
  ".Rproj.user",
  ".Rhistory",
  ".Rdata",
  ".Ruserdata"
))
```

If you use tooling that generates local caches (linters, coverage, pkgdown, etc.),
ignore those too.

## What goes in .gitignore vs .Rbuildignore

These two files solve different problems:

- `.gitignore` controls what _Git tracks_.
- `.Rbuildignore` controls what _goes into the built package tarball_.

Practical consequences:

- It’s normal to commit `.github/` (CI config) to Git _and_ ignore it for builds
  via `.Rbuildignore`.
- It’s normal to commit `README.Rmd` to Git, but ignore it in the build because
  the shipped source-of-truth for users is `README.md`.

Common patterns:

- Git ignores local state: `.Rproj.user/`, `.Rhistory`, `*.Rcheck/`.
- Build ignores non-package assets: `.github/`, `README.Rmd`, `docs/` (if you use
  it only for website publishing).

Use usethis helpers to keep these consistent:

```r
usethis::use_build_ignore(c("^README\\.Rmd$", "^\\.github$"))
```

## Connecting to GitHub

When you want a remote and collaboration:

```r
usethis::use_github()
```

This typically requires credentials to be configured.

If you already created the repo on GitHub, you can connect it manually too (remote + push),
but `usethis::use_github()` is the smooth path when you’re using the r-lib toolchain.

If you’re connecting manually, the workflow is conceptually:

1. Create a GitHub repo.
2. Add it as a remote.
3. Push your local `main`.

The exact commands differ depending on whether you use HTTPS or SSH.

## Credentials and authentication (PAT vs SSH)

Git and GitHub involve two separate interactions:

- **Git operations** (commit, branch, merge) are local.
- **GitHub operations** (push, pull, create PRs, run Actions) require authentication.

Two common approaches:

### Option A: HTTPS + Personal Access Token (PAT)

Best when:

- You’re in corporate environments with restricted SSH.
- You want consistent behavior across machines.

Typical “pitfall signal”:

- You get prompted for a password (GitHub does not accept account passwords for Git over HTTPS).

Fix:

- Use a PAT and a credential manager.

### Option B: SSH keys

Best when:

- You want to avoid typing credentials.
- You already use SSH for Git across repos.

Typical “pitfall signal”:

- You can browse GitHub but `git push` fails with permission/auth errors.

Fix:

- Ensure your SSH key is added to your GitHub account and your remote uses the SSH URL.

No matter which option you choose, aim for one “boring” default across all repos.

## Branching and pull requests

A practical default model:

- `main` stays green (checks pass).
- Work happens on short-lived branches.
- Changes land via PRs.

PR checklist that maps well to package work:

- `devtools::check()` runs clean locally.
- If you touched docs/exports: `devtools::document()` was run and changes are committed.
- If you touched behavior: tests were added/updated.
- The diff is reviewable (small commits, clear intent).

If CI fails, don’t “fight CI”. Reproduce locally and fix the underlying portability/dependency
issue (see the `r-lib/r-cmd-check-ci` skill).

### A practical PR workflow (recipe)

1. Create a branch with a purpose-first name:

- `fix-docs-links`
- `feat-parse-foo`
- `refactor-io-layer`

Example branch creation (Git):

```sh
git switch -c fix-docs-links
```

2. Work in small commits that each make sense in isolation.
3. Open a PR early (draft is fine) so CI and review can start.
4. Keep `main` green: don’t merge when checks fail.

If you created a branch locally and need to publish it:

```sh
git push -u origin fix-docs-links
```

If you’re working on a package with multiple contributors, avoid long-lived
branches that drift from `main`.

## Keeping your branch up to date

Keeping your PR branch close to `main` reduces conflicts and CI surprises.

Two common strategies:

- **Merge `main` into your branch**: preserves history; usually simplest.
- **Rebase your branch onto `main`**: keeps a linear history; requires more care.

Rules of thumb:

- If you’re not comfortable resolving conflicts, prefer merge.
- If your team requires rebase, do it before you request final review.

Whatever you do: avoid rewriting history on a branch that other people are actively using.

## Working with forks

Forks are common for open-source contributions (and sometimes internal workflows).

Practical model:

- **Upstream**: the “real” repo you ultimately want changes merged into.
- **Origin**: your fork (where you have push access).

Use a fork when:

- You don’t have direct push permission to the upstream repo.
- You want to isolate experimental work.

Typical fork pitfalls:

- The fork drifts far behind upstream (hard merges).
- CI behavior differs because secrets are not available on forks.

When secrets are required (deployments, API keys), expect fork PR workflows to have limits.

## What to commit in an R package

Package repos have some “generated” files that you generally _do_ commit because they are
part of the source bundle users and CRAN see:

- `DESCRIPTION`, `NAMESPACE`
- `man/*.Rd` (generated by roxygen2)
- `README.md` (even if authored via `README.Rmd`)

Common “don’t commit” items:

- user/session state (e.g. `.Rhistory`, `.Rproj.user/`)
- built artifacts (`*.tar.gz`, `*.Rcheck/`)
- local caches

If you publish a pkgdown site from the repo, decide explicitly whether the built site output
is committed (e.g., `docs/`) or deployed via CI.

## Commit discipline (small, reviewable steps)

What “good” looks like:

- A commit message explains _why_, not just _what_.
- Commits are small enough that a reviewer can understand them quickly.
- Generated files that are part of the package source are kept in sync.

Practical commit boundaries for R packages:

- **API change**: code + tests.
- **Docs change**: roxygen edits + regenerated `man/` and `NAMESPACE`.
- **Deps change**: `DESCRIPTION` + code updates to use `pkg::fun()`.

Avoid mixing unrelated changes (formatting, refactors, behavior changes) in the
same commit; it makes review and debugging slower.

## Keeping main green (local vs CI)

CI is not a different standard; it’s the same standard in a cleaner environment.

If CI frequently finds issues first, tighten the local loop:

- Run `devtools::document()` when you change roxygen, exports, or imports.
- Run `devtools::check()` before pushing.
- Keep dependency usage explicit (`pkg::fun()`), especially in examples/tests.

If you _must_ push to get a signal (e.g., OS-specific failures), treat that as
an exception and immediately reproduce locally where possible.

## Release and tagging basics

Even internal packages benefit from a lightweight release discipline:

- Keep `NEWS.md` meaningful (user-facing changes).
- Bump version intentionally.
- Tag releases so you can correlate behavior with versions.

Common r-lib tooling:

```r
usethis::use_version("patch")
```

Then:

- commit the version bump
- create a Git tag (e.g., `v1.2.3`)
- create a GitHub Release if that’s how your org communicates changes

For CRAN packages, release discipline is stricter; this page is about the
workflow mechanics.

## Recommended GitHub repo settings

These settings prevent common “works locally” and collaboration failures:

- Protect `main`.
- Require status checks (the `check-standard` workflow) before merging.
- Require PR review for non-trivial repos.
- Prefer squash merge if you want a linear history; prefer merge commits if you
  want to preserve commit structure.

The most important setting: don’t allow merges when checks are red.

## How This Connects to CI and pkgdown

GitHub is where you typically:

- Run `R CMD check` on every push/PR (via r-lib/actions `check-standard`).
- Build/deploy a pkgdown site.

Those fit naturally once the repo is on GitHub.

Once your repo is on GitHub, the highest leverage automation is usually:

- Run checks on every PR (`check-standard`).
- Build/deploy pkgdown on merges to `main`.

Related skills:

- `r-lib/r-cmd-check-ci` for check/CI triage and r-lib/actions guidance.
- `r-lib/documentation-roxygen2-pkgdown` for pkgdown site workflow.

## Common Pitfalls

- **Large commits / no commits for days:** makes review and debugging harder.
- **Treating CI as the first check run:** CI should confirm; local `check()`
  should discover.
- **Credentials surprises:** set up GitHub credentials intentionally.
- **Forgetting to commit `man/*.Rd` / `NAMESPACE`:** leads to “works locally” but fails on CI.
- **Letting generated output drift:** if you use `README.Rmd`, render it regularly.
- **Using `library()`/`require()` in package code:** this often “works locally” but
  fails in clean sessions and check.
- **Accidentally committing secrets:** never commit tokens/keys; use GitHub
  Secrets and env vars for CI.
- **Big binary files or data dumps:** prefer `inst/extdata` for small assets; for
  large artifacts, use releases or external storage.

## References

- R Packages (2e), “The whole game”: https://r-pkgs.org/whole-game.html
- usethis: `use_git()`: https://usethis.r-lib.org/reference/use_git.html
- usethis: `use_github()`: https://usethis.r-lib.org/reference/use_github.html
