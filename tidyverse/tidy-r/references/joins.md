# Modern Join Syntax (dplyr >=1.2.0)

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

