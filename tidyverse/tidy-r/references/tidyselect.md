# Tidy Selection

Tidy selection is the column selection language used by `select()`, `relocate()`, `rename()`, `across()`, `pick()`, `pivot_longer()`, `pivot_wider()`, and other tidyverse functions that accept column specifications.

## Selection helpers

```r
starts_with("x")          # columns starting with "x"
ends_with("_id")           # columns ending with "_id"
contains("score")          # columns containing "score"
matches("^x\\d+$")        # columns matching a regex
num_range("x", 1:5)       # x1, x2, x3, x4, x5
last_col()                 # rightmost column
everything()               # all columns
where(is.numeric)          # columns satisfying a predicate
```

## Selecting by name

```r
data |> select(name, age)                      # by name
data |> select(name:age)                       # range
data |> select(!age)                           # exclude
data |> select(where(is.numeric) & !id)        # boolean combination
```

## Boolean algebra on selections

Selections support `!` (complement), `&` (intersection), and `|` (union):

```r
data |> select(where(is.numeric) & !c(id, year))
data |> select(starts_with("x") | ends_with("_total"))
data |> select(!where(is.character))
```

## Character vectors: all_of() and any_of()

Use `all_of()` for strict matching (errors if a name is missing) and `any_of()` for permissive matching (silently ignores missing names):

```r
vars <- c("mpg", "wt", "hp")

data |> select(all_of(vars))       # errors if any name absent
data |> select(any_of(vars))       # ignores missing names
```

### The across(all_of()) bridge pattern

This is the canonical way to pass character vectors into data-masked contexts that use tidy selection:

```r
vars <- c("revenue", "cost")

data |>
  summarise(across(all_of(vars), mean))

data |>
  mutate(across(all_of(vars), \(x) x / 1000))
```

## .data and .env pronouns

### .data in data-masked contexts

Use `.data[[var]]` when the column name is a string variable inside data-masked functions (`filter`, `mutate`, `summarise`):

```r
var <- "mpg"
mtcars |> filter(.data[[var]] > 20)
```

### .data is deprecated in tidy-select contexts

Do NOT use `.data$col` or `.data[[var]]` inside tidy-select functions (`select`, `across`, `pick`). Use string names or `all_of()`/`any_of()` instead:

```r
var <- "mpg"

# Good
data |> select(all_of(var))
data |> select(any_of(var))

# Avoid (deprecated)
data |> select(.data[[var]])
```

### .env for environment variables

Use `.env$var` to access variables from the calling environment when they might collide with column names:

```r
threshold <- 10

# Good - unambiguous
data |> filter(value > .env$threshold)

# Risky - if data has a "threshold" column, it shadows the local variable
data |> filter(value > threshold)
```

`.env` is most useful inside functions where you cannot control what columns the data has:

```r
filter_above <- function(data, col, cutoff) {
  data |> filter({{ col }} > .env$cutoff)
}
```

## Tidy selection vs data masking

| Context | Used by | Column selection | Character vector bridge |
|---------|---------|-----------------|----------------------|
| **Tidy selection** | `select`, `across`, `pick`, `relocate`, `pivot_*` | helpers like `where()`, `starts_with()` | `all_of(vars)` |
| **Data masking** | `filter`, `mutate`, `summarise`, `arrange` | `.data[[var]]` | `across(all_of(vars))` |

The two contexts have different rules. Tidy selection uses helper functions; data masking evaluates R expressions in the data frame environment. `{{ }}` (embrace) works in both contexts for forwarding a single function argument.
