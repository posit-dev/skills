# Modern Join Syntax (dplyr 1.1+)

## Use join_by() instead of character vectors

### Equality joins

```r
transactions |>
  inner_join(companies, by = join_by(company == id))
```

### Same-name columns

```r
# When both tables share a column name, use a single name
orders |>
  left_join(customers, by = join_by(customer_id))
```

### Inequality joins

```r
transactions |>
  inner_join(companies, by = join_by(company == id, year >= since))
```

### Rolling joins (closest match)

```r
transactions |>
  inner_join(companies, by = join_by(company == id, closest(year >= since)))
```

### Overlap joins

```r
# Find events during each interval
intervals |>
  inner_join(events, by = join_by(start <= time, end >= time))
```

### Avoid - Old character vector syntax

```r
# Avoid
transactions |>
  inner_join(companies, by = c("company" = "id"))
```

## Relationship and match handling

### Enforce expected cardinality with relationship

```r
# 1:1 - each row matches at most one row in the other table
inner_join(x, y, by = join_by(id), relationship = "one-to-one")

# Many-to-one - many x rows can match one y row (lookup pattern)
left_join(x, y, by = join_by(id), relationship = "many-to-one")

# One-to-many
inner_join(x, y, by = join_by(id), relationship = "one-to-many")
```

### Ensure all rows match

```r
inner_join(x, y, by = join_by(id), unmatched = "error")
```

### Prevent NA matching (recommended)

```r
# By default, NA matches NA in joins -- usually not desired
left_join(x, y, by = join_by(id), na_matches = "never")
```

### Combining guards for production code

```r
sales |>
  left_join(
    products,
    by = join_by(product_id),
    relationship = "many-to-one",
    unmatched = "error",
    na_matches = "never"
  )
```

## Logging joins with tidylog

Use `tidylog::` prefix for joins to verify expected behavior. Call directly without loading the package.

```r
result <- transactions |>
  tidylog::left_join(companies, by = join_by(company == id))

# tidylog output:
# left_join: added 2 columns (name, region)
#            > rows only in x      12
#            > rows only in y     (3)
#            > matched rows       988
#            > rows total        1000
```

### Interpreting join output

| Output | Meaning |
|--------|---------|
| `rows only in x` | Rows in left table with no match (kept as NA in left joins) |
| `rows only in y` | Rows in right table with no match (in parentheses, dropped in left joins) |
| `matched rows` | Rows that matched between tables |
| `rows total` | Final row count after join |

### When to use tidylog

- **Always for joins** to see how many rows matched, duplicated, or were dropped
- **Critical filters** with `tidylog::filter()` to verify expected row counts
- **Critical mutates** with `tidylog::mutate()` to verify expected changes
- **Any operation where silent data loss is a risk**

Don't use tidylog in production code, inside functions, or loops where output would be too verbose. It's for interactive verification only.
