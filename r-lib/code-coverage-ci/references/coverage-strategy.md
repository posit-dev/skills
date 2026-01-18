# Coverage strategy (useful, not gamed)

## What coverage is good for

- finding untested branches
- validating error handling paths are exercised
- checking that refactors didn’t orphan key behavior

## What coverage is not

- a substitute for good assertions
- a goal to maximize at all costs

## Practical guidance

- Prefer adding tests for important behavior over chasing lines.
- Focus on:
  - error classes and messages
  - boundary conditions
  - optional dependencies and their guards
- Use coverage deltas in PRs to notice untested additions.
