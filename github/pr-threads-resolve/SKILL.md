---
name: pr-threads-resolve
description: Bulk resolve unresolved PR review threads. Useful after manually addressing threads or after using /pr-threads-address.
compatibility: Designed for Claude Code; requires gh CLI and gh-pr-review extension
metadata:
  author: Barret Schloerke (@schloerke)
  version: "1.0"
license: MIT
---

# /pr-threads-resolve

**Usage:** `/pr-threads-resolve [PR_NUMBER]`

**Description:** Bulk resolve unresolved PR review threads. Useful after manually addressing threads or after using `/pr-threads-address`.

**Note:** If `PR_NUMBER` is omitted, the command will automatically detect and use the PR associated with the current branch.

## Resolve PR context first

Before running any `gh pr-review` subcommand, resolve the PR number and repo once and reuse them. Every `gh pr-review` subcommand requires both `--pr <number>` and `--repo <owner/repo>` — do not omit either.

```bash
PR_NUMBER="${1:-$(gh pr view --json number -q .number)}"
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
```

Pass `--pr "$PR_NUMBER" --repo "$REPO"` on every subsequent `gh pr-review` call in this workflow (list, resolve, view, reply).

## Workflow

1. Resolve `PR_NUMBER` and `REPO` as shown above
2. Fetch and display all unresolved PR review threads
3. Show thread details (file, line, comment text)
4. Ask for confirmation or allow selective resolution
5. Resolve the confirmed threads
6. Report back with a summary of resolved threads

## When to use

Use this command when you have already addressed PR review threads and want to bulk resolve them, or when you need to clean up threads that are no longer relevant.

## Example

```
/pr-threads-resolve 42
```

This will:
- List all unresolved threads on PR #42
- Show what each thread is about
- Ask which threads to resolve (all or specific ones)
- Resolve the selected threads
- Provide a summary of resolved items

## Prerequisites

Before using this command, check if the gh pr-review extension is installed:

```bash
gh extension list | grep -q pr-review || gh extension install agynio/gh-pr-review
```

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

```bash
# Assumes PR_NUMBER and REPO were resolved as shown in "Resolve PR context first".
gh pr-review threads list --pr "$PR_NUMBER" --unresolved --repo "$REPO" | \
  jq -r '.threads[].id' | \
  xargs -I {} gh pr-review threads resolve --thread-id {} --pr "$PR_NUMBER" --repo "$REPO"
```

## Usage Notes

1. **Required flags**: Every `gh pr-review` subcommand (`threads list`, `threads resolve`, `threads unresolve`, `review view`, `comments reply`, etc.) requires both `--pr <number>` and `--repo <owner/repo>`. Resolve them once at the start of the workflow and reuse on every call — do not drop them in pipelines or `xargs` loops.

2. **Thread IDs**: Thread IDs (format `PRRT_...`) can be obtained from `review view --include-comment-node-id` or `threads list` commands.

3. **State Filters**: When using `--states`, provide a comma-separated list: `--states APPROVED,CHANGES_REQUESTED`

4. **Unresolved Focus**: Use `--unresolved --not_outdated` together to focus on actionable comments that need attention.
