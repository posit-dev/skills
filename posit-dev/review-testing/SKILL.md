---
name: review-testing
description: Review test code for quality, design, and completeness after implementing a feature or fixing a bug. Use when the user asks to "review my tests", "check my test quality", "are these tests good enough", "review testing", or after completing a feature implementation that includes tests. Also use when tests feel brittle, flaky, or superficial. Cross-references production code to find coverage gaps.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "0.1"
license: MIT
---

You are reviewing test code that was written alongside a feature implementation or bug fix. Your goal is to ensure the tests are well-designed, thorough, and maintainable — not just that they pass. Tests that merely mirror implementation details create a false sense of security and become a maintenance burden during refactoring.

## Review Scope

Identify what to review:

1. **Find changed test files** on the current branch (relative to the base branch).
2. **Find the production code** those tests cover — trace imports, function calls, and file naming conventions to map tests back to their targets.
3. **Find related existing tests** for the same modules or functions that weren't changed — these may need updates or reveal gaps.

Read test files first, before production code. If you can infer the feature's requirements and edge cases from the tests alone, that's a sign the tests are well-written. If you need to read the implementation to understand what the tests are doing, that's a finding worth reporting.

## What Makes a Test Valuable

Every test earns its place by delivering on four qualities. When reviewing, weigh each test against these:

**Regression protection** — Does this test actually catch bugs? A test that exercises trivial code or skips the complex branches protects against nothing. Check: does the test touch the business-critical logic, or does it only verify the happy path of a simple getter?

**Refactoring resilience** — Will this test break when someone restructures the code without changing its behavior? Tests coupled to internal method names, call sequences, or private state will punish every future cleanup with false failures. This erodes trust in the suite and creates "refactoring fear" where developers avoid improving code because they don't want to fix dozens of tests.

**Fast feedback** — Unit tests should run in milliseconds. If a test hits the filesystem, network, or database when it doesn't need to, that's a design issue. But don't confuse speed with value — an integration test that takes 200ms to verify a real database query is better than a fast unit test that mocks out the database and verifies nothing meaningful.

**Maintainability** — Can someone unfamiliar with this code read the test and understand both what it verifies and why? Tests with sprawling setup, cryptic variable names, or deeply nested mocking configurations fail this check.

These four qualities are in tension. A test that maximizes regression protection by hitting real databases sacrifices speed. A test that maximizes refactoring resilience by only testing public APIs might miss internal edge cases. The right balance depends on the type of test (unit vs. integration) and what it's protecting.

## Review Areas

### 1. Assertion Completeness

The most common weakness in generated tests: asserting only the most obvious output and missing the full "blast radius" of a state change.

When a test triggers an action, ask what *else* changed as a consequence. If a test adds an item to a cart, does it only check the item count? Or does it also verify the price calculation, the subtotal update, and that other cart items are unaffected?

**Flag when:**
- A test asserts a return value but ignores side effects
- A test checks that an operation succeeded but not that it produced the right result
- A test verifies the happy path but skips boundary conditions (empty inputs, nulls, maximum values, off-by-one)
- Error-path tests only check that an error was thrown, not that the error message, type, or cleanup behavior is correct

### 2. Test Structure

Each test should have exactly one Arrange-Act-Assert cycle. The arrange phase sets up preconditions, the act phase triggers the behavior, and the assert phase verifies the outcome. If you see a test that acts and asserts multiple times in sequence, it's testing multiple behaviors and should be split.

**Flag when:**
- A test has multiple act phases (testing a workflow, not a behavior)
- The arrange phase is so large that the actual behavior being tested is buried
- Assertions appear inside setup helpers or utility functions (this hides what's being verified and reduces helper reusability)
- Test logic contains conditionals or loops — tests should be straight-line code with a deterministic path

### 3. Fixture and State Management

How test data is created and managed determines whether the suite is maintainable at scale.

**Inline setup** (all data created directly in the test body) is fine for simple tests but becomes a liability when constructor signatures change — you'll update every test that instantiates that object.

**Implicit setup** (shared `beforeEach`/`setUp`/`setup()` blocks) eliminates duplication but forces every test to share the same fixtures, often creating "general fixtures" where each test uses only a fraction of the setup. This obscures what a test actually depends on.

**Delegated setup** (factory functions, builders, helpers called explicitly in each test) keeps each test readable while centralizing construction logic. Constructor changes only require updating the helper.

**Flag when:**
- A shared setup block creates objects that most tests don't use
- Tests depend on external files, database state, or global variables defined elsewhere (the "Mystery Guest" smell — everything a test needs should be visible in its body or one function call away)
- Tests assume resources exist without creating them (files, database records, environment variables)
- Tests mutate shared state without cleanup, causing order-dependent failures

### 4. Mocking Boundaries

Mocks are essential for isolating units of code, but overuse turns tests into mirrors of the implementation.

**The key principle:** mock at architectural boundaries, not at every function call. A test that mocks every collaborator to verify a specific call sequence will break the moment someone refactors the internals, even if the behavior is unchanged. Use stubs (which return canned data) for query-type dependencies and mocks (which verify interactions) only for side-effect-heavy commands like sending emails or writing to external systems.

Different teams have different mocking philosophies — some isolate every collaborator (London/mockist style), others let real objects collaborate freely and only mock at process boundaries (Detroit/classical style). Neither is wrong, but the codebase's existing convention should be respected. Flag inconsistency within a project, not deviation from a universal rule.

**Flag when:**
- A test mocks types it doesn't own (third-party libraries, framework internals). When that library updates, the mock still passes against outdated assumptions. Recommend: thin adapter wrappers, real implementations in integration tests, or official testing utilities provided by the framework (e.g., MemoryRouter, test databases, in-memory caches).
- Mock density is high — if a test requires 4+ mock configurations, the production code likely has too many responsibilities
- A test verifies call counts or argument sequences on internal methods. This couples the test to how the code works rather than what it does.
- Stubs are being verified (checking that a stub was called is testing the implementation, not the behavior)

### 5. Test Smells

Common patterns that signal deeper problems:

| Smell | What It Looks Like | Why It Matters |
|---|---|---|
| **Assertion Roulette** | Multiple assertions with no failure messages | When it fails, you can't tell which assertion broke without debugging |
| **Eager Test** | One test exercises several unrelated methods | Failures are ambiguous — which behavior actually broke? |
| **Lazy Test** | Multiple tests call the same method with identical inputs | Redundant tests add maintenance cost without improving coverage |
| **Sleepy Test** | Hard-coded `sleep()`/`Sys.sleep()`/`setTimeout()` delays | Flaky in CI, slow everywhere. Use polling or explicit waits. |
| **Rotten Green** | Assertions inside `try`/`tryCatch` blocks or conditional branches | The test always passes because the assertion is never reached |
| **Sensitive Equality** | Asserting against string representations (`toString()`, `print()` output) | Breaks on any formatting change; assert structural properties instead |
| **Print Statement** | `print()`/`console.log()` instead of assertions | Debugging leftovers that verify nothing programmatically |
| **Snapshot Abuse** | Snapshot tests used as a substitute for behavioral assertions | Snapshotting an entire component or output is easy to generate but verifies nothing intentionally — any change triggers a failure, and developers blindly update the snapshot. Reserve snapshots for outputs where the exact text/structure matters (error messages, CLI output, rendered documents). |
| **Implementation Mirror** | Test computes expected values using the same logic as production code | If the test reimplements the calculation it's supposed to verify, it will always agree with the production code — including when both are wrong. Expected values should be independently derived (hardcoded from a known-good source, manually calculated, or from a reference implementation). |

### 6. Naming and Readability

Test names should describe behavior, not implementation. A well-named test suite reads like a specification of the feature.

**Flag when:**
- Test names reference internal method names (e.g., `test_processData_returns_true`) — these break when methods are renamed
- Test names are generic (`test1`, `test_it_works`, `test_basic`)
- The test name doesn't tell you what scenario is being tested or what the expected outcome is

Prefer behavioral names: `test_expired_subscription_blocks_access`, `delivery_with_past_date_is_invalid`, `empty_cart_shows_zero_total`.

### 7. Coverage Gaps

Cross-reference the production code changes against the test suite:

- Are there branches or conditions in the production code that no test exercises?
- Are error paths tested? (Not just "does it throw" but "does it throw the right thing and clean up properly")
- Are edge cases covered? (Empty collections, null/NA/None/undefined inputs, boundary values, concurrent access if applicable)
- If the production code changed existing behavior, were existing tests updated to reflect the new behavior?

This is where reading the production code matters. Walk through the implementation and note every decision point — each `if`, `match`, `switch`, error handler, or early return. Then check whether the test suite exercises both sides of that decision.

When reviewing R tests using `testthat`, check if the `testing-r-packages` skill is available and invoke it for R-specific conventions and patterns.

## Response Format

```
## Summary
[Overall assessment: How well do these tests protect the codebase?
Note the ratio of meaningful tests to superficial ones.]

## Critical Issues (Blocking)
[Tests that provide false confidence or will cause real problems.
e.g., rotten green tests, mocked-out assertions, missing error-path coverage
for critical operations.]

## Required Changes
[Design problems that weaken the test suite.
e.g., implementation-coupled mocks, missing blast-radius assertions,
mystery guest dependencies, assertion roulette.]

## Strong Suggestions
[Improvements to test quality and maintainability.
e.g., better naming, fixture refactoring, additional edge cases.]

## Noted
[Minor style or convention issues. Mention once, then move on.]

## Verdict
Request Changes | Needs Discussion | Approve

## Next Steps
[Options for proceeding]
```

Use `file:line` references for every finding. Quote the specific test code that demonstrates the issue and show what better code looks like.

## Next Steps

At the end of the review, offer the user these options:

**Discuss and address findings:** Use the AskUserQuestion tool to systematically walk through the issues. Group by severity or topic, offer resolution options, and clearly mark the recommended choice.

**Fix the issues:** Offer to apply the fixes directly. Work through them in priority order — blocking issues first, then required changes, then suggestions. After each group, confirm before continuing.

**Add to a pull request:** When reviewing in the context of a PR, offer to post the review as a PR comment. Include attribution: "Review assisted by the [review-testing skill](https://github.com/posit-dev/skills/blob/main/posit-dev/review-testing/SKILL.md)."

If operating as a subagent, skip the next steps and output only the review findings.
