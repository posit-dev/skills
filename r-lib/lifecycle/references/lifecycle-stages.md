# Lifecycle Stages Reference

## Table of Contents

- [Stage Diagram](#stage-diagram)
- [Stable](#stable)
- [Experimental](#experimental)
- [Deprecated](#deprecated)
- [Superseded](#superseded)
- [Retired Stages](#retired-stages)

## Stage Diagram

```
experimental --> stable --> deprecated
                   |
                   +--> superseded
```

Lifecycle stages apply to packages, functions, arguments, or specific argument values.

## Stable

The default stage. Functions are stable when the author is satisfied with the interface.

**Promises:**
- Breaking changes avoided where possible
- Breaking changes happen gradually through deprecation

**Breaking changes** reduce working code: removing functions/arguments, narrowing valid inputs, or changing output types.

**Not breaking changes:** Bug fixes that happen to break code relying on buggy behavior.

## Experimental

For functions released without long-term stability promises. Author reserves the right to make breaking changes without deprecation cycle.

**Guidelines:**
- Packages with version < 1.0.0 are at least somewhat experimental
- Non-CRAN packages require active relationship with maintainers

## Deprecated

Function has a better alternative and is scheduled for removal.

**Deprecation stages (in order):**

1. **Soft deprecated** (`deprecate_soft()`) - Warns only:
   - Users calling from global environment
   - Developers running tests
   - Does NOT warn when called indirectly by another package

2. **Deprecated** (`deprecate_warn()`) - Warns all users once per 8 hours

3. **Defunct** (`deprecate_stop()`) - Errors with helpful message about replacement

## Superseded

Function has a known better alternative but won't be removed. Receives only critical bug fixes.

**Key difference from deprecated:**
- No warning emitted
- Documentation explains recommended alternative
- Function preserved indefinitely (safer than stable in some ways)

**Examples:** `tidyr::gather()` and `tidyr::spread()` superseded by `pivot_longer()` and `pivot_wider()`.

## Retired Stages

No longer recommended:

- **Questioning** - Author uncertain about function; not actionable for users
- **Maturing** - Between experimental and stable; unclear actionable information
