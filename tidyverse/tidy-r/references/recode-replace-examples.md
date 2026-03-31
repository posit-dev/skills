# Recoding, Replacing, and Filtering (dplyr 1.2+)

dplyr 1.2 introduced a family of functions for recoding and replacing values, and for NA-safe filtering. These replace older patterns (`case_match`, `recode`, `coalesce`, `na_if`, negated filters).

## The recode/replace family

|                           | **Recoding** (new column) | **Replacing** (update in place) |
|---------------------------|---------------------------|---------------------------------|
| **Match with conditions** | `case_when()`             | `replace_when()`                |
| **Match with values**     | `recode_values()`         | `replace_values()`              |

## recode_values()

Use instead of `case_match()` or repetitive `case_when()` with `==`.

### Formula interface

```r
score |>
  recode_values(
    1 ~ "Strongly disagree",
    2 ~ "Disagree",
    3 ~ "Neutral",
    4 ~ "Agree",
    5 ~ "Strongly agree"
  )
```

### Lookup table interface

```r
likert |>
  mutate(score = recode_values(score, from = lookup$from, to = lookup$to))
```

### With .unmatched = "error" for safety

```r
# Errors if any value has no match
score |>
  recode_values(
    1 ~ "Low",
    2 ~ "Medium",
    3 ~ "High",
    .unmatched = "error"
  )
```

### Avoid

```r
# Avoid - repetitive case_when with ==
case_when(score == 1 ~ "Strongly disagree", score == 2 ~ "Disagree", ...)

# Avoid - case_match() is soft-deprecated in dplyr 1.2
case_match(score, 1 ~ "Strongly disagree", 2 ~ "Disagree", ...)

# Avoid - recode() is soft-deprecated
recode(score, `1` = "Strongly disagree", `2` = "Disagree", ...)
```

## replace_values()

Use for partial updates by value. Unmatched values pass through unchanged.

### Replace specific values

```r
name |>
  replace_values(
    c("UNC", "Chapel Hill") ~ "UNC Chapel Hill",
    c("Duke", "Duke University") ~ "Duke"
  )
```

### Replace NA (replaces coalesce/tidyr::replace_na)

```r
x |> replace_values(NA ~ 0)
```

### Convert sentinel values to NA (replaces na_if)

```r
x |> replace_values(from = c(0, -99), to = NA)
```

## replace_when()

Use for conditional updates. Type-stable on the input; unmatched values pass through unchanged.

### Conditional updates

```r
racers |>
  mutate(
    time = time |>
      replace_when(
        id %in% id_banned ~ NA,
        id %in% id_penalty ~ time + 1/3
      )
  )
```

### Avoid - case_when with .default

```r
# Avoid - buries the primary input, loses type info
mutate(time = case_when(
  id %in% id_banned ~ NA,
  id %in% id_penalty ~ time + 1/3,
  .default = time
))
```

## case_when() with .unmatched = "error"

Still the right choice for complex conditional recoding into a new column. Use `.unmatched = "error"` for safety:

```r
tier <- case_when(
  time < 23 ~ "A",
  time < 27 ~ "B",
  time < 30 ~ "C",
  .unmatched = "error"
)
```

## filter_out()

NA-safe row removal. Treats `NA` as `FALSE`, so you don't accidentally drop NA rows:

```r
# Good - clear intent, NA-safe
data |> filter_out(deceased, date < 2012)

# Avoid - easy to get wrong with NA
data |> filter(!(deceased & date < 2012) | is.na(deceased) | is.na(date))
```

## when_any() and when_all()

Combine conditions with comma-separated syntax instead of `|` and `&`:

### OR conditions

```r
data |>
  filter(when_any(
    name %in% c("US", "CA") & between(score, 200, 300),
    name %in% c("PR", "RU") & between(score, 100, 200)
  ))
```

### Drop rows matching any condition

```r
data |>
  filter_out(when_any(
    is.na(value),
    status == "invalid"
  ))
```

### AND conditions

```r
data |>
  filter(when_all(
    score > 50,
    !is.na(region),
    status == "active"
  ))
```

## Migration quick reference

| Old pattern | New pattern |
|-------------|-------------|
| `case_match(x, val ~ result)` | `recode_values(x, val ~ result)` |
| `recode(x, old = "new")` | `recode_values(x, "old" ~ "new")` |
| `case_when(..., .default = x)` | `x \|> replace_when(...)` |
| `coalesce(x, default)` | `replace_values(x, NA ~ default)` |
| `na_if(x, val)` | `replace_values(x, val ~ NA)` |
| `tidyr::replace_na(x, default)` | `replace_values(x, NA ~ default)` |
| `filter(x != val \| is.na(x))` | `filter_out(x == val)` |
| `filter(c1 \| c2 \| c3)` | `filter(when_any(c1, c2, c3))` |
| `filter(c1 & c2 & c3)` | `filter(when_all(c1, c2, c3))` |
