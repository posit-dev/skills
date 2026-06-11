---
name: pr-threads-address
description: "Address PR review feedback by systematically working through every unresolved PR review thread on the current branch's PR - analyze each comment, make the requested code changes (with tests where useful), commit, and optionally reply and resolve."
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

### Resolve PR context

Every `gh pr-review` subcommand requires both `--pr <number>` and `--repo <owner/repo>` — do not omit either. Look the values up once at the start of the workflow and substitute the literal numbers and slugs into every later command.

Get the PR number for the current branch:

```bash
gh pr view --json number -q .number
```

Get the repository slug:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

Then pass the resulting values directly — e.g. `--pr 42 --repo posit-dev/skills` — on every subsequent `gh pr-review` call in this workflow (review view, comments reply, threads resolve, etc.).

## Workflow

1. Fetch and display all unresolved PR review threads
2. Analyze each thread to understand the requested changes
3. For each thread:
   1. Make the necessary code modifications
   2. (When possible) Add unit tests to verify the change
   3. Commit the changes with descriptive commit messages using conventional commit specification
4. Report back with a summary of addressed threads
5. Ask if the user wants to resolve the threads. If so, reply to each thread indicating what was done and then resolve the thread.

## CLI Reference

### View PR Reviews and Comments

Display all reviews, inline comments, and replies for a pull request:

```bash
gh pr-review review view --pr <number> --repo <owner/repo>
```

**Common filters:**

- `--reviewer <login>` — Filter by specific reviewer
- `--states <list>` — Comma-separated review states (APPROVED, CHANGES_REQUESTED, COMMENTED, DISMISSED)
- `--unresolved` — Show only unresolved threads
- `--tail <n>` — Show only the last n replies per thread
- `--include-comment-node-id` — Include GraphQL node IDs for replies

### Reply to Review Threads

```bash
gh pr-review comments reply --thread-id <PRRT_...> --body "<reply-text>" --repo <owner/repo> --pr <number>
```

For multi-line replies, pass `--body "$(cat <<'EOF' ... EOF\n)"` heredoc syntax.

### Resolve a Thread

```bash
gh pr-review threads resolve --thread-id <PRRT_...> --pr <number> --repo <owner/repo>
```

Thread IDs (format `PRRT_...`) come from `review view --include-comment-node-id`.
