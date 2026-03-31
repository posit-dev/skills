# Modern Grouping and Column Operations (dplyr 1.1+)

## Per-operation grouping with .by

The `.by` argument replaces the old `group_by() |> ... |> ungroup()` pattern. Results are always ungrouped.

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

### Avoid - old persistent grouping pattern

```r
# Avoid
data |>
  group_by(category) |>
  summarise(mean_value = mean(value)) |>
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

### Character vectors use .data[[]]

```r
for (var in names(mtcars)) {
  mtcars |> count(.data[[var]]) |> print()
}
```

### Multiple columns use across()

```r
my_summary <- function(data, summary_vars) {
  data |>
    summarise(across({{ summary_vars }}, \(x) mean(x)))
}
```
