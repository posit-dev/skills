---
name: cran-extrachecks
description: >
  Prepare R packages for CRAN submission by checking for common ad-hoc requirements not caught by devtools::check(). Use when: (1) Preparing a package for first CRAN release, (2) Preparing a package update for CRAN resubmission, (3) Reviewing a package to ensure CRAN compliance, (4) Responding to CRAN reviewer feedback. Covers documentation requirements, DESCRIPTION field standards, URL validation, examples, and administrative requirements.
---

# CRAN Extra Checks

Help R package developers prepare packages for CRAN submission by systematically checking for common ad-hoc requirements that CRAN reviewers enforce but `devtools::check()` doesn't catch.

## Workflow

1. **Initial Assessment**: Ask user if this is first submission or resubmission
2. **Run Standard Checklist**: Work through each item systematically (see below)
3. **Identify Issues**: As you review files, note specific problems
4. **Propose Fixes**: Suggest specific changes for each issue found
5. **Implement Changes**: Make edits only when user approves
6. **Verify**: Confirm all changes are complete

## Standard CRAN Preparation Checklist

Work through these items systematically:

1. **Create NEWS.md**: Run `usethis::use_news_md()` if not already present
2. **Create cran-comments.md**: Run `usethis::use_cran_comments()` if not already present
3. **Update install instructions**: Review README for aspirational install instructions (usually `install.packages("pkgname")`)
4. **Proofread DESCRIPTION**: Carefully review `Title:` and `Description:` fields (see detailed guidance below)
5. **Check function documentation**: Verify all exported functions have `@return` and `@examples` (see detailed guidance below)
6. **Verify copyright holder**: Check that `Authors@R:` includes a copyright holder with role `[cph]`
7. **Review bundled file licensing**: Check licensing of any included third-party files
8. **Run URL checks**: Use `urlchecker::url_check()` and fix any issues

## Detailed CRAN Checks

### Documentation Requirements

**Return Value Documentation (Strictly Enforced)**

CRAN now strictly requires `@return` documentation for all exported functions. Use the roxygen2 tag `@return` to document what the function returns.

- Required even for functions marked `@keywords internal`
- Required even if function returns nothing - document as `@return None` or similar
- Must be present for every exported function

Example:
```r
# Missing @return - WILL BE REJECTED
#' Calculate sum
#' @export
my_sum <- function(x, y) {
  x + y
}

# Correct - includes @return
#' Calculate sum
#' @param x First number
#' @param y Second number
#' @return A numeric value
#' @export
my_sum <- function(x, y) {
  x + y
}

# For functions with no return value
#' Print message
#' @param msg Message to print
#' @return None, called for side effects
#' @export
print_msg <- function(msg) {
  cat(msg, "\n")
}
```

**Examples for Exported Functions**

If your exported function has a meaningful return value, it will almost definitely require an `@examples` section. Use the roxygen2 tag `@examples`.

- Required even for functions marked `@keywords internal`
- Exceptions exist for functions used purely for side effects (e.g., creating directories)
- Examples must be executable

**Un-exported Functions with Examples**

If you write roxygen examples for un-exported functions, you must either:

1. Call them with `:::` notation: `pkg:::my_fun()`
2. Use `@noRd` tag to suppress `.Rd` file creation

**Using `\dontrun{}` Sparingly**

`\dontrun{}` should only be used if the example really cannot be executed (e.g., missing additional software, API keys, etc.).

- If showing an error, wrap the call in `try()` instead
- Consider custom predicates (e.g., `googlesheets4::sheets_has_token()`) with `if ()` blocks
- Sometimes `interactive()` can be used as the condition
- Lengthy examples (> 5 sec) can use `\donttest{}`

**Never Comment Out Code in Examples**

```r
# BAD - Will be rejected
#' @examples
#' # my_function(x)  # Don't do this!
```

CRAN's guidance: "Examples/code lines in examples should never be commented out. Ideally find toy examples that can be regularly executed and checked."

**Guarding Examples with Suggested Packages**

Use `@examplesIf` for entire example sections requiring suggested packages:

```r
#' @examplesIf rlang::is_installed("dplyr")
#' library(dplyr)
#' my_data %>% my_function()
```

For individual code blocks within examples:
```r
#' @examples
#' if (rlang::is_installed("dplyr")) {
#'   library(dplyr)
#'   my_data %>% my_function()
#' }
```

### DESCRIPTION Title Field

CRAN enforces strict Title requirements:

**Use Title Case**

Capitalize all words except articles like 'a', 'the'. Use `tools::toTitleCase()` to help format.

**Avoid Redundancy**

Common phrases that get flagged:
- "A Toolkit for" → Remove
- "Tools for" → Remove
- "for R" → Remove

Examples:
```r
# BAD
Title: A Toolkit for the Construction of Modeling Packages for R

# GOOD
Title: Construct Modeling Packages

# BAD
Title: Command Argument Parsing for R

# GOOD
Title: Command Argument Parsing
```

**Quote Software/Package Names**

Put all software and R package names in single quotes:

```r
# GOOD
Title: Interface to 'Tiingo' Stock Price API
```

**Length Limit**

Keep titles under 65 characters.

### DESCRIPTION Description Field

**Never Start With Forbidden Phrases**

CRAN will reject descriptions starting with:
- "This package"
- Package name
- "Functions for"

```r
# BAD
Description: This package provides functions for rendering slides.
Description: Functions for rendering slides to different formats.

# GOOD
Description: Render slides to different formats including HTML and PDF.
```

**Expand to 3-4 Sentences**

Single-sentence descriptions are insufficient. Provide a broader description of:
- What the package does
- Why it may be useful
- Types of problems it helps solve

```r
# BAD (too short)
Description: Render slides to different formats.

# GOOD
Description: Render slides to different formats including HTML and PDF.
    Supports custom themes and progressive disclosure patterns. Integrates
    with 'reveal.js' for interactive presentations. Designed for technical
    presentations and teaching materials.
```

**Quote Software Names, Not Functions**

```r
# BAD
Description: Uses 'case_when()' to process data.

# GOOD
Description: Uses case_when() to process data with 'dplyr'.
```

Software, package, and API names get single quotes (including 'R'). Function names do not.

**Expand All Acronyms**

All acronyms must be fully expanded on first mention:

```r
# BAD
Description: Implements X-SAMPA processing.

# GOOD
Description: Implements Extended Speech Assessment Methods Phonetic
    Alphabet (X-SAMPA) processing.
```

**Publication Titles Only in Double Quotes**

Only use double quotes for publication titles, not for phrases or emphasis:

```r
# BAD
Description: Handles dates like "the first Monday of December".

# GOOD
Description: Handles dates like the first Monday of December.
```

### URL and Link Validation

**All URLs Must Use HTTPS**

CRAN requires `https://` protocol for all URLs. HTTP links will be rejected.

```r
# BAD
URL: http://paleobiodb.org/

# GOOD
URL: https://paleobiodb.org/
```

**No Redirecting URLs**

CRAN rejects URLs that redirect to other locations. Example rejection:

```
Found the following (possibly) invalid URLs:
URL: https://h3geo.org/docs/core-library/coordsystems#faceijk-coordinates
     (moved to https://h3geo.org/docs/core-library/coordsystems/)
```

**Use urlchecker Package**

```r
# Find redirecting URLs
urlchecker::url_check()

# Automatically update to final destinations
urlchecker::url_update()
```

**Check for Invalid File URIs**

Relative links in README must exist after package build. Common issue:

```
Found the following (possibly) invalid file URI:
     URI: CODE_OF_CONDUCT.md
       From: README.md
```

This occurs when files are in `.Rbuildignore`. Solutions:
1. Remove file from `.Rbuildignore`
2. Use `usethis::use_code_of_conduct()` which generates sections without relative links

### Handling Suggested Package Dependencies

If CRAN runs `noSuggests` check, your package must work without Suggested packages installed.

**In Examples**

Entire example sections:
```r
#' @examplesIf rlang::is_installed("dplyr")
#' library(dplyr)
#' my_data %>% my_function()
```

Individual blocks:
```r
#' @examples
#' if (rlang::is_installed("dplyr")) {
#'   library(dplyr)
#'   my_data %>% my_function()
#' }
```

**In Tests**

```r
testthat::skip_if_not_installed("dplyr")
```

**Recursive Dependencies**

Watch for recursive dependencies. If using `sf::read_sf()`, the tibble package is required but sf only `Suggests` it. Guard appropriately.

**GitHub Action for Testing**

Use [this GitHub Action](https://github.com/r-lib/actions/blob/v2-branch/examples/check-no-suggests.yaml) to test your package without suggested packages.

### Administrative Requirements

**Copyright Holder Role**

Always add `[cph]` role to Authors field, even if you're the only author:

```r
# Required
Authors@R: person("John", "Doe", role = c("aut", "cre", "cph"))
```

**Posit-Supported Packages**

For packages in Posit-related GitHub organizations (posit-dev, rstudio, r-lib, tidyverse, tidymodels) or maintained by someone with a @posit.co email address, include Posit Software, PBC as copyright holder and funder:

```r
Authors@R: c(
  person("Jane", "Doe", role = c("aut", "cre"),
         email = "jane.doe@posit.co"),
  person("Posit Software, PBC", role = c("cph", "fnd"),
         comment = c(ROR = "03wc8by49"))
)
```

**LICENSE Year**

Update LICENSE year to current submission year:

```r
# If working on package in 2023, submitting in 2024
# Update: 2023 → 2024
```

**Method References**

CRAN may ask:

> If there are references describing the methods in your package, please add these in the description field...

If there are no references, reply to the email explaining this. Consider adding a preemptive note in `cran-comments.md`:

```markdown
## Method References

There are no published references describing the methods in this package.
The package implements original functionality for [brief description].
```

## Key Files to Review

Work through these files systematically:

- **DESCRIPTION**: Title, Description, Authors@R, URLs, License year
- **R/*.R**: Function documentation (`@return`, `@examples`, `@examplesIf`, `@noRd`)
- **README.md**: Install instructions, relative links, URLs
- **cran-comments.md**: Preemptive notes for reviewers
- **NEWS.md**: Version notes for this release
- **.Rbuildignore**: Files referenced in README

## Common Fix Patterns

**DESCRIPTION Title:**
```r
# Before
Title: A Toolkit for the Construction of Modeling Packages for R

# After
Title: Construct Modeling Packages
```

**DESCRIPTION Description:**
```r
# Before
Description: This package provides functions for rendering slides.

# After
Description: Render slides to different formats including HTML and PDF.
    Supports custom themes and progressive disclosure. Integrates with
    'reveal.js' for interactive presentations.
```

**Function Documentation:**
```r
# Before - Missing @return
#' Calculate total
#' @param x Values
#' @export
calc_total <- function(x) sum(x)

# After - Complete documentation
#' Calculate total
#' @param x Numeric values to sum
#' @return A numeric value representing the sum
#' @examples
#' calc_total(1:10)
#' @export
calc_total <- function(x) sum(x)
```

## Useful Tools

- `tools::toTitleCase()` - Format titles with proper capitalization
- `urlchecker::url_check()` - Find problematic URLs
- `urlchecker::url_update()` - Fix redirecting URLs
- `usethis::use_news_md()` - Create NEWS.md
- `usethis::use_cran_comments()` - Create cran-comments.md
- `usethis::use_code_of_conduct()` - Add CoC without relative links
- `usethis::use_build_ignore()` - Ignore files in R package build
- `usethis::use_package()` - Add a package dependency to DESCRIPTION
- `usethis::use_tidy_description()` - Tidy up DESCRIPTION formatting
