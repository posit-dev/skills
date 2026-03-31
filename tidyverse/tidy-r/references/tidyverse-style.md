# Tidyverse Style Guide Summary

Based on https://style.tidyverse.org/

## Object Names

- Use **snake_case**: lowercase letters, numbers, underscores only
- Variables = **nouns**, functions = **verbs**
- Avoid reusing common function/variable names
- Prefix non-standard function arguments with `.` (e.g., `.data`, `.by`)
- Avoid dots in names except for S3 methods

```r
# Good
day_one
calculate_mean
user_data

# Bad
DayOne
calculateMean
day.one
```

## Spacing

**Commas**: space after, never before

```r
# Good
x[, 1]
mean(x, na.rm = TRUE)

# Bad
x[,1]
mean(x ,na.rm = TRUE)
```

**Infix operators**: surround with spaces (`==`, `+`, `-`, `<-`, etc.)

```r
# Good
x == y
z <- 2 + 2

# Bad
x==y
z<-2+2
```

**No spaces** for high-precedence operators: `::`, `$`, `@`, `[`, `[[`, `^`, `:`

```r
# Good
sqrt(x^2 + y^2)
x <- 1:10
pkg::fun()
```

## Assignment

Use `<-`, not `=`

```r
# Good
x <- 5

# Bad
x = 5
```

## Quotes

Use double quotes `"`; single `'` only when text contains double quotes

```r
# Good
"Text here"
'They said "hello"'
```

## Line Length

Limit to **80 characters**. For long function calls, put each argument on its own line:

```r
# Good
do_something(
  arg1 = "value",
  arg2 = "value",
  arg3 = "value"
)
```

## Braces

- `{` ends a line
- Contents indented by **2 spaces**
- `}` starts a line
- `else` on same line as `}`

```r
if (condition) {
  do_this()
} else {
  do_that()
}
```

## Functions

**Anonymous functions**: use `\(x)` for short lambdas

```r
# Good
map(x, \(x) x + 1)

# Bad
map(x, function(x) x + 1)
```

**Return**: use `return()` only for early returns; rely on implicit return otherwise

```r
# Good
add_one <- function(x) {
  x + 1
}

# Early return
check_input <- function(x) {
  if (is.null(x)) {
    return(NULL)
  }
  process(x)
}
```

**Multi-line definitions**: single-indent style preferred

```r
long_function_name <- function(
    a = "argument",
    b = "argument"
) {
  # body
}
```

## Pipes

- Use `|>` (not `%>%`)
- Space before pipe, newline after
- Indent continuation by 2 spaces

```r
# Good
data |>
  filter(x > 0) |>
  mutate(y = x * 2) |>
  summarise(mean(y))

# Bad
data |> filter(x > 0) |> mutate(y = x * 2)
```

**Avoid pipes when**:
- Manipulating multiple objects
- Meaningful intermediate objects deserve names

## Comments

- Start with `# ` (hash + space)
- Explain **why**, not what
- Use sentence case

```r
# Skip NA values because downstream analysis requires complete cases
data <- data |> filter(!is.na(value))
```

## Control Flow

- Use `&&` and `||` in conditions (not `&` and `|`)
- Use `TRUE`/`FALSE` (not `T`/`F`)
- Never use semicolons

## Error Messages

Use `cli::cli_abort()` for errors. See https://style.tidyverse.org/errors.html

**Problem statement**:
- Start with concise problem in sentence case, ending with `.`
- Use **"must"** when cause is clear: `` `n` must be a numeric vector, not a character vector.``
- Use **"can't"** when you cannot state what was expected: ``Can't find column `b` in `.data`.``

**Bullets**:
- `x` (cross) for problems
- `i` (info) for context
- `!` (warning) for warnings

**Formatting**:
- Surround argument names in backticks: `` `x` ``
- Use "column" to disambiguate (avoid "variable")
- Keep under 80 characters; let cli wrap
- List up to 5 issues, truncate with `...`

**Hints**: place last with `i` bullet, end with `?`

```r
cli::cli_abort(c(
  "{.arg x} must be a numeric vector, not {.obj_type_friendly {x}}.",
  "i" = "Did you mean to use {.fn as.numeric}?"
))
```
