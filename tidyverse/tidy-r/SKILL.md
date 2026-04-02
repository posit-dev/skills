---
name: tidy-r
description: |
  Modern tidyverse patterns, style guide, and migration guidance for R development. Use when writing, reviewing, or refactoring tidyverse code. Covers native pipe, join_by(), .by grouping, pick/across/reframe, filter_out/when_any/when_all, recode_values/replace_values/replace_when, tidy selection, stringr, naming conventions, and migration from base R or older tidyverse APIs.
metadata:
  r_version: "4.5+"
  tidyverse_version: "2.0+"
  dplyr_version: "1.2+"
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, mcp__r-btw__*
---

# Writing Modern Tidyverse R

This skill covers modern tidyverse patterns for R 4.5+ and tidyverse 2.0+, style guidelines, and migration from legacy patterns.

## Core philosophy

R's tidyverse evolves. Code from blog posts and StackOverflow often uses deprecated APIs, magrittr pipes, or base R patterns where a modern tidyverse function exists. This skill encodes the current recommended approach so the model writes code that experienced R developers would recognize as idiomatic.

## When to use this skill

- Writing new R code with dplyr, tidyr, stringr, purrr, or other tidyverse packages
- Reviewing or refactoring existing R code for modern patterns
- Migrating from base R, magrittr pipes, or older tidyverse APIs
- Applying tidyverse style conventions (naming, spacing, error handling)
- Choosing between similar functions (e.g., `case_when` vs `recode_values`)
- Working with joins, grouping, recoding, or string manipulation in R

## When NOT to use this skill

- Writing data.table code (different paradigm)
- Pure base R projects that intentionally avoid tidyverse
- Shiny UI/server logic (use a Shiny-specific skill)
- Package development internals (NAMESPACE, DESCRIPTION, roxygen)
- ggplot2 visualization (use the socviz skill)
- Statistical modeling or Bayesian analysis

## Instructions

When you receive a request, classify it and consult the appropriate reference:

### Step 1: Classify the request

| Category | Reference file | Trigger |
|----------|---------------|---------|
| **Joins** | [join-examples.md](references/join-examples.md) | Merging data, `*_join`, `join_by`, matching rows, lookup tables |
| **Grouping & columns** | [grouping-examples.md](references/grouping-examples.md) | `.by`, `group_by`, `across`, `pick`, `reframe`, column operations |
| **Recoding & replacing** | [recode-replace-examples.md](references/recode-replace-examples.md) | `case_when`, `recode_values`, `replace_values`, `replace_when`, `filter_out`, `when_any`, `when_all`, recoding, replacing, conditional updates |
| **Strings** | [stringr-examples.md](references/stringr-examples.md) | String manipulation, regex, `str_*` functions, text processing |
| **Style** | [tidyverse-style.md](references/tidyverse-style.md) | Naming, formatting, spacing, error messages, `cli::cli_abort` |
| **Migration** | [migration-examples.md](references/migration-examples.md) | Updating old code, base R conversion, deprecated functions |

### Step 2: Read the reference file(s)

Use the Read tool to load the relevant reference. For requests that span multiple categories (e.g., "rewrite this old code" touches migration + style), read multiple files.

### Step 3: Apply core principles

1. **Use modern tidyverse patterns** - Prioritize dplyr 1.2+ features, native pipe, and current APIs
2. **Write readable code first** - Optimize only when necessary
3. **Follow tidyverse style guide** - Consistent naming, spacing, and structure
4. **Use R MCP tools** - Automatically resolve function documentation and library references without being asked. If the `mcp__r-btw__*` tools are unavailable, fall back to running R help via Bash (see below)

### R documentation lookup fallback

When `mcp__r-btw__*` tools are available, use them to look up function signatures, help pages, and package docs. When they are not available (e.g., the r-btw MCP server is not configured), fall back to Bash:

```bash
# Help page for a function
Rscript --vanilla -e '?dplyr::recode_values' 2>/dev/null || Rscript --vanilla -e 'utils::help("recode_values", package = "dplyr")'

# Function signature / arguments
Rscript --vanilla -e 'args(dplyr::recode_values)'

# List exported functions in a package
Rscript --vanilla -e 'ls("package:dplyr")'

# Check if a package is installed
Rscript --vanilla -e 'requireNamespace("dplyr", quietly = TRUE)'
```

### Step 4: Write the code

Follow the quick reference and anti-patterns below. When in doubt, consult the reference files.

## Quick reference

### Pipe and lambda

- Always `|>`, never `%>%`
- Always `\(x)`, never `function(x)` or `~` in map/keep/etc.

### Code organization

Use newspaper style: high-level logic first, helpers below. Don't define functions inside other functions unless they are very brief.

### Grouping

- Use `.by` for per-operation grouping, never `group_by() |> ... |> ungroup()`
- Never add `ungroup()` before or after `.by` — it always returns ungrouped data
- Consolidate multiple `mutate(.by = x)` calls into one when they share the same `.by`; keep separate only when `.by` differs or a later column depends on an earlier one
- Place `.by` on its own line for readability

### Joins

- Use `join_by()`, never `c("a" = "b")`
- Use `relationship`, `unmatched`, `na_matches` for quality control

### Recoding and replacing (dplyr 1.2+)

| Task | Function |
|------|----------|
| Recode values (new column) | `recode_values()` |
| Replace values in place | `replace_values()` |
| Conditional update in place | `replace_when()` |
| Complex conditional (new column) | `case_when()` |
| Drop rows (NA-safe) | `filter_out()` |
| OR conditions | `when_any()` |
| AND conditions | `when_all()` |

### Error handling

Use `cli::cli_abort()` with problem statement + bullets, never `stop()`.

### R idioms

- `TRUE`/`FALSE`, never `T`/`F`
- `message()` for info, never `cat()`
- `map_*()` over `sapply()` for type stability
- `set.seed()` with date-time, never 42
- `qs2::qs_save()`/`qs2::qs_read()`, never `qs`

## Anti-patterns

| Avoid | Use instead |
|-------|-------------|
| `%>%` | `|>` |
| `function(x)` or `~` | `\(x)` |
| `by = c("a" = "b")` | `by = join_by(a == b)` |
| `multiple = "error"` in joins | `relationship = "many-to-one"` (or `"one-to-one"`) |
| `sapply()` | `map_*()` (type-stable) |
| `group_by() \|> ... \|> ungroup()` | `.by` argument |
| `ungroup() \|> mutate(..., .by = x)` | `mutate(..., .by = x)` (`.by` ignores existing groups) |
| Repeated `mutate(.by = x)` with same `.by` | Single `mutate()` with all columns and one `.by` |
| `cat()` for messages | `message()` or `cli::cli_inform()` |
| `stop()` for errors | `cli::cli_abort()` |
| `distinct(id)` | `distinct(id, .keep_all = TRUE)` |
| `mean(x, na.rm = TRUE)` | `mean(x)` with tidyna loaded |
| `case_match(x, ...)` | `recode_values(x, ...)` |
| `recode(x, ...)` | `recode_values(x, ...)` or `replace_values(x, ...)` |
| `filter(x != val \| is.na(x))` | `filter_out(x == val)` |
| `coalesce(x, default)` | `replace_values(x, NA ~ default)` |
| `na_if(x, val)` | `replace_values(x, val ~ NA)` |
| `qs::qsave()` / `qs::qread()` | `qs2::qs_save()` / `qs2::qs_read()` |

## Complete workflow example

```r
library(tidyverse)

# Read and clean data
sales <- read_csv("data/sales.csv") |>
  rename(
    region = Region,
    product = Product,
    revenue = Revenue,
    date = Date
  ) |>
  mutate(
    quarter = quarter(date),
    product = product |>
      replace_values(
        c("Widget A", "WidgetA") ~ "Widget A",
        c("Widget B", "WidgetB") ~ "Widget B"
      )
  ) |>
  filter_out(is.na(revenue))

# Enrich with lookup table
sales_enriched <- sales |>
  left_join(
    regions,
    by = join_by(region == region_code),
    unmatched = "error"
  )

# Summarise by group
quarterly <- sales_enriched |>
  summarise(
    total_revenue = sum(revenue),
    avg_revenue = mean(revenue),
    n_transactions = n(),
    .by = c(region_name, quarter)
  ) |>
  mutate(
    performance = revenue |>
      replace_when(
        total_revenue > 100000 ~ "high",
        total_revenue > 50000 ~ "medium"
      )
  ) |>
  arrange(region_name, quarter)
```

## Best practices

1. **Use `.unmatched = "error"`** in `case_when()` and `recode_values()` for defensive programming
4. **Place `.by` on its own line** for readability
5. **Prefer `filter_out()` over negated `filter()`** for NA-safe row removal
6. **Use `recode_values()` over `case_match()`** (dplyr 1.2+ preferred API)
7. **Use `replace_when()` over `case_when()` with `.default`** when updating a column in place
8. **Name variables as nouns, functions as verbs** in snake_case
9. **Explain "why" in comments**, not "what"
10. **Use `qs2` for serialization** with `.qs2` extension
