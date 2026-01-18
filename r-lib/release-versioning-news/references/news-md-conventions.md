# NEWS.md conventions

Good NEWS is for users.

## A good NEWS entry

- states the user-visible behavior change
- mentions the affected function(s) if relevant
- avoids internal implementation detail

Examples:

- “`foo()` now accepts character input and returns a tibble.”
- “Fixed a crash in `bar()` when `x` contains missing values.”
- “Breaking change: `baz()` no longer recycles inputs; it errors with a clear message.”

## Structure

Common patterns:

- Group by version (top-down, newest first).
- Within a release, consider headings like “Breaking changes”, “New features”, “Bug fixes”.

If your package has multiple audiences (users vs developers), bias toward user-facing summaries.

## Avoid

- listing PR numbers without context
- rewriting commit messages
- deeply technical notes that don’t help users upgrade

Also avoid:

- long “wall of text” release notes with no headings
- hiding breaking changes in the middle of a list

## Suggested section skeleton

```markdown
# pkgname 1.2.3

## Breaking changes

- ...

## New features

- ...

## Bug fixes

- ...
```
