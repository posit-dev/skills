---
name: r-tidyverse-style
description: >
  Use when the user asks to review or clean up R code for tidyverse style,
  standardize formatting or names, remove redundant comments or wrappers, or
  make a behavior-preserving style pass. Also use when writing substantial new
  R package code if the user requests tidyverse style or the package already
  follows it. Not for routine small edits or general correctness, security,
  or test-quality reviews.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# Tidyverse style for R package code

Prefer the package's established conventions over the tidyverse guide unless the user requests a migration. Style is not proof of correctness; keep public behavior unchanged during cleanup.

## Work through the task

1. **Set scope and mode.** For a review, inspect the requested files or diff without editing. For cleanup, change only the agreed scope. When writing new code, inspect neighboring `R/` files, tests, and style configuration before choosing conventions. Check `DESCRIPTION` for supported R versions and dependencies when relevant.
2. **Protect interfaces.** Before renaming or reorganizing code, check exports, roxygen/NAMESPACE, S3/S4 methods, callers, tests, and user-visible conditions. Don't treat a public rename, changed default, error, return value, dependency, or supported R version as cosmetic.
3. **Triage observations.** Distinguish style, maintainability, and possible bugs. For generated-looking code, investigate comments that restate code, duplicate checks or helpers, pointless wrappers, speculative `tryCatch()` fallbacks, and docs or tests that contradict behavior. Confirm against callers and tests before removing anything; code provenance alone proves nothing. These are review heuristics, not tidyverse rules.
4. **Change in risk order.** Format scoped files first. Then simplify only verified redundancy, retaining comments about intent or constraints. Propose behavior-sensitive changes (pipe conversions, evaluation order, control flow, public names, error text) separately; make them only if the user has authorized that scope, with focused tests. Don't turn a style pass into an unrequested refactor.
5. **Verify and report.** Inspect the diff; run relevant focused tests and broader package checks when warranted. For review-only work, give prioritized findings with file/line references and suggested edits, without modifying files. For edits, state what changed, what was deferred, and which checks actually ran. Don't claim a style pass is a correctness or security review.

## Style rules

The rules below selectively paraphrase the [tidyverse style guide](https://style.tidyverse.org/) ([source](https://github.com/tidyverse/style), consulted at commit `2aed77e`); this is not an official tidyverse skill. The links are citations, **not required reading**. Open a relevant chapter only when a rule needs clarification or the user requests verification, never all chapters by default.

### Syntax and names

Source: [Syntax](https://style.tidyverse.org/syntax.html).

- Prefer descriptive `snake_case` names: nouns for values, verbs for functions. Dots can obscure S3 method names. Check compatibility before renaming names used outside a file or package.
- Use two-space indentation, no tabs. Put spaces after commas, around ordinary infix operators, and around `=` in named arguments; not just inside parentheses or around `$`, `::`, `:`, `^`, or unary `-`. Tidy-evaluation operators have exceptions. Prefer syntax-aware formatting to regex edits.
- Use `<-` for assignment and `=` for named arguments; avoid semicolons and multiple statements on a line.
- Put opening braces at line ends, closing braces at line starts, and `else` beside the preceding `}`. Use braces for multiline branches and loops. Don't replace `if` with vectorized `ifelse()` or change `&`/`|` to `&&`/`||` without checking semantics.
- Put arguments of a long call on separate, consistently indented lines. Aim for readable line lengths (80 characters is a target, not a hard limit).
- Group related statements into visual paragraphs; use a single empty line to separate distinct thoughts, functions, or pipelines, not every statement. Avoid empty lines at the start or end of functions. A blank line before a comment block can tie its explanation to the code below.
- Prefer double quotes unless single quotes reduce escaping; spell logical constants `TRUE` and `FALSE`. Prefix comments with `# `. Keep comments explaining decisions or constraints; remove narration only after checking its purpose.
- Name arguments that control computation or override defaults, but don't require names for every conventional first data argument. Avoid partial matching.

### Functions and pipes

Sources: [Functions](https://style.tidyverse.org/functions.html), [Pipes](https://style.tidyverse.org/pipes.html).

- Use `function(...) { ... }` for named functions. Short single-expression anonymous functions can use `\(x) ...`; use `function()` for longer ones. Don't introduce formula lambdas or wrappers merely for style.
- Put long function definitions on multiple lines with consistent indentation. Use `return()` chiefly for early exits, on its own line; otherwise rely on the last expression. Side-effect functions may invisibly return their input, but changing an existing return value isn't cosmetic.
- Use pipes for transformations of one primary object; name intermediates when several objects participate or an intermediate has meaning. In multiline pipes, put the pipe at line end and indent steps by two spaces. Short pipes and several assignment layouts are acceptable.
- The guide favors `|>`, but don't mass-convert `%>%`: check the minimum R version, placeholders, pronouns, magrittr operators, and evaluation behavior. Treat migration as separate, tested work.

### Package files

Sources: [Files](https://style.tidyverse.org/files.html), [Package files](https://style.tidyverse.org/package-files.html), [Tests](https://style.tidyverse.org/tests.html).

- Use descriptive lowercase `.R` filenames with consistent `-` or `_` separators. Name a single-function file after its function; give a file of related functions a concise, evocative name. The guide uses `deprec-` for deprecated-function files.
- Put documented public functions before private helpers. If functions share a roxygen documentation block, place them immediately after it. Use section comments when helpful. Check collate order, registration, generated files, and load-time effects before moving code.
- Match `tests/testthat/test-<name>.R` to `R/<name>.R` when organizing tests. The book specifies test-file organization, **not** test design or coverage goals.
- In scripts, group `library()` calls near the top. Don't add `library()` calls inside package code or infer package dependency policy from this script guidance.

### Documentation and diagnostics

Sources: [Documentation](https://style.tidyverse.org/documentation.html), [Error messages](https://style.tidyverse.org/errors.html).

- Put roxygen comments next to code. Use concise sentence-case titles without final periods; explicit `@description` for longer descriptions. Prefix lines with `#' `, indent wrapped tags consistently, write complete parameter/return sentences, and use `@inheritParams` for shared text.
- Use backticks for R code, argument names, and values, not package names merely because they're packages. Add `@seealso`, `@family`, and links where useful. Use `@noRd` for internal functions documented with roxygen; don't add roxygen to every helper.
- Lead errors with a clear problem and useful location/details. Use “must” for a clear requirement and “Can't” when the failed operation is more natural. Use bullets or hints only when warranted; don't invent a diagnosis. The guide illustrates `cli` conventions, but adding a dependency is a separate decision.
- Check docs against actual signatures, defaults, return values, and examples. Error wording may be user-visible or snapshotted; changing validation rules, condition classes, or error timing isn't style cleanup.

### ggplot2 (when relevant)

Source: [ggplot2](https://style.tidyverse.org/ggplot2.html). Put `+` at line ends, indent subsequent layers, and prefer transforming data before calling `ggplot()` rather than inside its data argument. Verify any plot restructuring against existing behavior.

## Optional tools

Use `air format R/file.R` for scoped formatting (or `air format --check R/file.R` to check without writing). If installed, `jarl check .` provides lint findings and `ry check` flags possible type errors. Honor project configuration; investigate diagnostics rather than automatically applying fixes. None of these tools is required or proves behavior unchanged. Report unavailable tools or failing pre-existing tests.

## Examples

- Reviewing `R/import.R`: flag a comment that merely narrates the next line as style noise. Treat `tryCatch(..., error = function(e) NULL)` as a *possible bug* to investigate, not something to delete during a review.
- Cleaning a package that supports R 4.0: format the requested file, but leave `%>%` and exported names alone. Propose any base-pipe migration or public rename separately, with compatibility analysis and tests.

Use `r-testthat` for test design and `r-package-development` for package infrastructure rather than expanding this style pass into either task.
