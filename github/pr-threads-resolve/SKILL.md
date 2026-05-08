---
name: pr-threads-resolve
description: Bulk resolve unresolved PR review threads. Useful after manually addressing threads or after using /pr-threads-address.
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

## When to use

Use this command when you have already addressed PR review threads and want to bulk resolve them, or when you need to clean up threads that are no longer relevant.

## Example

```
/pr-threads-resolve
```

This will:

- List all unresolved threads on the PR for the current branch
- Show what each thread is about
- Ask which threads to resolve (all or specific ones)
- Resolve the selected threads
- Provide a summary of resolved items

## CLI Reference

### List Review Threads

Enumerate all review threads with filtering:

```bash
gh pr-review threads list --pr <number> --repo <owner/repo>
```

**Common filters:**

- `--unresolved` — Show only unresolved threads
- `--resolved` — Show only resolved threads

### View PR Reviews and Comments

Display reviews, inline comments, and replies with full context:

```bash
gh pr-review review view --pr <number> --repo <owner/repo>
```

**Common filters:**

- `--reviewer <login>` — Filter by specific reviewer
- `--states <list>` — Filter by review state (APPROVED, CHANGES_REQUESTED, COMMENTED, DISMISSED)
- `--unresolved` — Show only unresolved threads
- `--not_outdated` — Exclude outdated threads
- `--tail <n>` — Show only the last n replies per thread
- `--include-comment-node-id` — Include GraphQL node IDs for replies

### Resolve / Unresolve Threads

Toggle thread resolution status:

```bash
# Resolve a thread
gh pr-review threads resolve --thread-id <PRRT_...> --pr <number> --repo <owner/repo>

# Unresolve a thread
gh pr-review threads unresolve --thread-id <PRRT_...> --pr <number> --repo <owner/repo>
```

### Bulk Resolve Example

Substitute the actual PR number and repo slug resolved in "Resolve PR context first" — the `42` / `owner/repo` below are placeholders.

```bash
gh pr-review threads list --pr 42 --unresolved --repo owner/repo | \
  jq -r '.threads[].id' | \
  xargs -I {} gh pr-review threads resolve --thread-id {} --pr 42 --repo owner/repo
```

## Usage Notes

1. **Required flags**: Every `gh pr-review` subcommand (`threads list`, `threads resolve`, `threads unresolve`, `review view`, `comments reply`, etc.) requires both `--pr <number>` and `--repo <owner/repo>`. Resolve them once at the start of the workflow and reuse on every call — do not drop them in pipelines or `xargs` loops.

2. **Thread IDs**: Thread IDs (format `PRRT_...`) can be obtained from `review view --include-comment-node-id` or `threads list` commands.

3. **State Filters**: When using `--states`, provide a comma-separated list: `--states APPROVED,CHANGES_REQUESTED`

4. **Unresolved Focus**: Use `--unresolved --not_outdated` together to focus on actionable comments that need attention.
