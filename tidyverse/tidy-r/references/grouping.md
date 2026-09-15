# Modern Grouping and Column Operations (dplyr >=1.2.0)

## Per-operation grouping with .by

The `.by` argument is preferred for per-operation grouping. Use `group_by()` when grouping must persist across multiple operations. `.by` results are always ungrouped.

### Basic usage

```r
data |>
  summarise(
    mean_value = mean(value),
    .by = category
  )
```

### Multiple grouping variables

```r
data |>
  summarise(
    total = sum(revenue),
    .by = c(company, year)
  )
```

### .by with mutate (window functions)

```r
data |>
  mutate(
    pct_of_group = revenue / sum(revenue),
    rank = row_number(desc(revenue)),
    .by = region
  )
```

### .by with filter (group-level filtering)

```r
data |>
  filter(
    revenue == max(revenue),
    .by = region
  )
```

### Place .by on its own line

```r
# Good - readable
data |>
  summarise(
    mean_value = mean(value),
    .by = category
  )

# Avoid - crammed
data |>
  summarise(mean_value = mean(value), .by = category)
```

### Avoid for single operations - use .by instead

```r
# Avoid
data |>
  group_by(category) |>
  summarise(mean_value = mean(value)) |>
  ungroup()
```

### Avoid - redundant ungroup() around .by

`.by` always returns ungrouped data, so `ungroup()` before or after is a no-op. Remove it.

```r
# Avoid - ungroup() is redundant
data |>
  ungroup() |>
  mutate(
    centered = x - mean(x),
    .by = group
  )

# Good
data |>
  mutate(
    centered = x - mean(x),
    .by = group
  )
```

### Consolidating mutate() calls

When multiple columns share the same `.by`, combine them in a single `mutate()`.

```r
# Avoid - repeating .by = year across separate mutate() calls
data |>
  mutate(
    above_med_a = a > median(a),
    .by = year
  ) |>
  mutate(
    above_med_b = b > median(b),
    .by = year
  )

# Good - one mutate(), one .by
data |>
  mutate(
    above_med_a = a > median(a),
    above_med_b = b > median(b),
    .by = year
  )
```

**When to keep separate `mutate()` calls:**

- **Different `.by` variables** between the calls
- **Sequential dependency**: a later column uses a column created in an earlier `mutate()` within the same grouped context (the new column must exist before the group-level aggregate can reference it)

```r
# Separate calls needed: different .by variables
data |>
  mutate(
    x_lag = dplyr::lag(x),
    .by = id
  ) |>
  mutate(
    above_med = x_lag > median(x_lag),
    .by = year
  )

# Separate calls needed: b_rank depends on b_centered
data |>
  mutate(
    b_centered = b - mean(b),
    .by = group
  ) |>
  mutate(
    b_rank = row_number(desc(b_centered)),
    .by = group
  )
```

## .by with tidyr::fill()

tidyr supports `.by` in `fill()`, matching the dplyr pattern:

```r
# Good - per-operation grouping
data |>
  tidyr::fill(value, .by = group, .direction = "down")

# Avoid - group_by/ungroup wrapper
data |>
  group_by(group) |>
  tidyr::fill(value, .direction = "down") |>
  ungroup()
```

## pick() for column selection

Use `pick()` inside data-masking functions to select columns by name or tidyselect helpers:

```r
data |>
  summarise(
    n_x_cols = ncol(pick(starts_with("x"))),
    n_y_cols = ncol(pick(starts_with("y")))
  )
```

### pick() to pass selected columns to functions

```r
data |>
  mutate(
    row_mean = rowMeans(pick(where(is.numeric)))
  )
```

## across() for applying functions

Apply one or more functions to multiple columns:

### Single function

```r
data |>
  summarise(
    across(where(is.numeric), \(x) mean(x)),
    .by = group
  )
```

### Multiple functions with naming

```r
data |>
  summarise(
    across(
      c(revenue, cost),
      list(mean = \(x) mean(x), sd = \(x) sd(x)),
      .names = "{.fn}_{.col}"
    ),
    .by = region
  )
```

### Conditional transformation

```r
data |>
  mutate(
    across(where(is.character), str_to_lower)
  )
```

## reframe() for multi-row results

When a summary returns multiple rows per group, use `reframe()` instead of `summarise()`:

```r
data |>
  reframe(
    quantile = c(0.25, 0.50, 0.75),
    value = quantile(x, c(0.25, 0.50, 0.75)),
    .by = group
  )
```

## Data masking vs tidy selection

Understand the difference for writing functions:

- **Data masking** (`arrange`, `filter`, `mutate`, `summarise`): expressions evaluated in data context
- **Tidy selection** (`select`, `relocate`, `across`, `pick`): column selection helpers

### Embrace with {{ }} for function arguments

```r
my_summary <- function(data, summary_var) {
  data |>
    summarise(mean_val = mean({{ summary_var }}))
}
```

### Character vectors in data-masked contexts use .data[[]]

```r
for (var in names(mtcars)) {
  mtcars |> count(.data[[var]]) |> print()
}
```

### Character vectors in tidy-select contexts use all_of()/any_of()

The `across(all_of())` bridge is the canonical pattern for passing character vectors into tidy-select:

```r
vars <- c("mpg", "wt", "hp")

# Good - across(all_of()) for character vectors
mtcars |>
  summarise(across(all_of(vars), mean))

# Good - any_of() when some columns may not exist
mtcars |>
  select(any_of(vars))

# Avoid - .data[[]] inside tidy-select (deprecated)
mtcars |>
  select(.data[["mpg"]], .data[["wt"]])
```

### Access calling-environment variables with .env

Use `.env$var` to disambiguate when a local variable shares a name with a column:

```r
threshold <- 10
data |>
  filter(value > .env$threshold)
```

### Multiple columns use across()

```r
my_summary <- function(data, summary_vars) {
  data |>
    summarise(across({{ summary_vars }}, \(x) mean(x)))
}
```
