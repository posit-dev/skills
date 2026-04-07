---
name: tidy-r
description: >
  Modern tidyverse patterns, style guide, and migration guidance for R development. Use this skill when writing R code, reviewing tidyverse code, updating legacy R code to modern patterns, or enforcing consistent style. Covers native pipe usage, join_by() syntax, .by grouping, pick/across/reframe, filter_out/when_any/when_all, recode_values/replace_values/replace_when, tidy selection, stringr, naming conventions, and migration from base R or older tidyverse APIs.
metadata:
  r_version: ">=4.5.0"
  tidyverse_version: ">=2.0.0"
  dplyr_version: ">=1.2.0"
---

# Modern Tidyverse R Reference

Code from blog posts and StackOverflow often uses deprecated APIs, magrittr pipes, or base R patterns where a modern tidyverse function exists. This guide encodes the current recommended approach.

## Reference files

Consult the appropriate reference file for detailed patterns and examples:

| Topic | Reference file | When to consult |
|-------|---------------|-----------------|
| **Joins** | [joins.md](references/joins.md) | Merging data, `*_join`, `join_by`, matching rows, lookup tables |
| **Grouping & columns** | [grouping.md](references/grouping.md) | `.by`, `group_by`, `across`, `pick`, `reframe`, column operations |
| **Recoding & replacing** | [recode-replace.md](references/recode-replace.md) | `recode_values`, `replace_values`, `replace_when`, `filter_out`, `when_any`, `when_all` |
| **Strings** | [stringr.md](references/stringr.md) | String manipulation, regex, `str_*` functions, text processing |
| **Style** | [tidyverse-style.md](references/tidyverse-style.md) | Naming, formatting, spacing, error messages, `cli::cli_abort` |
| **Migration** | [migration.md](references/migration.md) | Updating old code, base R conversion, deprecated functions |

For requests that span multiple topics (e.g., "rewrite this old code" touches migration + style), read multiple files.

## Core principles

1. **Use modern tidyverse patterns** -- Prioritize dplyr 1.2+ features, native pipe, and current APIs
2. **Write readable code first** -- Optimize only when necessary
3. **Follow tidyverse style guide** -- Consistent naming, spacing, and structure

## Quick reference

### Pipe and lambda

- Always `|>`, never `%>%`
- Always `\(x)`, never `function(x)` or `~` in map/keep/etc.

### Code organization

Use newspaper style: high-level logic first, helpers below. Don't define functions inside other functions unless they are very brief.

### Grouping

- Use `.by` for per-operation grouping, never `group_by() |> ... |> ungroup()`
- Never add `ungroup()` before or after `.by` -- it always returns ungrouped data
- Consolidate multiple `mutate(.by = x)` calls into one when they share the same `.by`; keep separate only when `.by` differs or a later column depends on an earlier one
- Place `.by` on its own line for readability

### Joins

- Use `join_by()`, never `c("a" = "b")`
- Use `relationship`, `unmatched`, `na_matches` for quality control

### Recoding and replacing (dplyr >=1.2.0)

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

## Example

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
2. **Place `.by` on its own line** for readability
3. **Prefer `filter_out()` over negated `filter()`** for NA-safe row removal
4. **Use `recode_values()` over `case_match()`** (dplyr >=1.2.0 preferred API)
5. **Use `replace_when()` over `case_when()` with `.default`** when updating a column in place
6. **Name variables as nouns, functions as verbs** in snake_case
7. **Explain "why" in comments**, not "what"
