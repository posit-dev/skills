---
name: pr-threads-resolve
description: Bulk resolve unresolved PR review threads on the current branch’s PR — typically after threads have been addressed manually or via /pr-threads-address
compatibility: Designed for Claude Code; requires gh CLI and gh-pr-review extension
metadata:
  author: Barret Schloerke (@schloerke)
  version: "1.0"
license: MIT
---

## Prerequisites

### gh pr-review extension

Before using this command, check if the gh pr-review extension is installed:

```bash
gh extension list | grep -q pr-review || gh extension install agynio/gh-pr-review
```

### Resolve PR context first

Every `gh pr-review` subcommand requires both `--pr <number>` and `--repo <owner/repo>` — do not omit either. Look the values up once at the start of the workflow and substitute the literal numbers and slugs into every later command.

Get the PR number for the current branch:

```bash
gh pr view --json number -q .number
```

Get the repository slug:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

Then pass the resulting values directly — e.g. `--pr 42 --repo posit-dev/skills` — on every subsequent `gh pr-review` call in this workflow (list, resolve, view, reply).

## Workflow

1. Fetch and display all unresolved PR review threads
2. Show thread details (file, line, comment text)
3. Ask for confirmation or allow selective resolution
4. Resolve the confirmed threads
5. Report back with a summary of resolved threads

## CLI Reference

### List Review Threads

```bash
gh pr-review threads list --pr <number> --repo <owner/repo>
```

Filter with `--unresolved` or `--resolved`.

### Resolve / Unresolve Threads

```bash
gh pr-review threads resolve --thread-id <PRRT_...> --pr <number> --repo <owner/repo>
gh pr-review threads unresolve --thread-id <PRRT_...> --pr <number> --repo <owner/repo>
```

### Bulk Resolve Example

Substitute the actual PR number and repo slug resolved in "Resolve PR context first" — the `42` / `owner/repo` below are placeholders.

```bash
gh pr-review threads list --pr 42 --unresolved --repo owner/repo | \
  jq -r '.threads[].id' | \
  xargs -I {} gh pr-review threads resolve --thread-id {} --pr 42 --repo owner/repo
```
