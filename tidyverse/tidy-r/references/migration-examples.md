# Migration: Base R and Old Tidyverse to Modern Patterns

## Base R to Modern Tidyverse

### Data manipulation

```r
subset(data, condition)          # -> filter(data, condition)
data[order(data$x), ]            # -> arrange(data, x)
aggregate(x ~ y, data, mean)     # -> summarise(data, mean(x), .by = y)
merge(x, y, by = "id")           # -> left_join(x, y, by = join_by(id))
```

### Functional programming

```r
sapply(x, f)                     # -> map(x, f)  # type-stable
lapply(x, f)                     # -> map(x, f)
vapply(x, f, numeric(1))         # -> map_dbl(x, f)
```

### String manipulation

```r
grepl("pattern", text)           # -> str_detect(text, "pattern")
gsub("old", "new", text)         # -> str_replace_all(text, "old", "new")
substr(text, 1, 5)               # -> str_sub(text, 1, 5)
nchar(text)                      # -> str_length(text)
strsplit(text, ",")              # -> str_split(text, ",")
tolower(text)                    # -> str_to_lower(text)
sprintf("Hello %s", name)       # -> str_glue("Hello {name}")
```

## Old to New Tidyverse Patterns

### Pipes

```r
data %>% function()              # -> data |> function()
```

### Anonymous functions

```r
map(x, function(x) x + 1)       # -> map(x, \(x) x + 1)
map(x, ~ .x + 1)                # -> map(x, \(x) x + 1)
```

### Grouping (dplyr 1.1+)

```r
group_by(data, x) |>
  summarise(mean(y)) |>
  ungroup()                      # -> summarise(data, mean(y), .by = x)
```

### Joins

```r
by = c("a" = "b")                # -> by = join_by(a == b)
```

### Column selection

```r
across(starts_with("x"))         # -> pick(starts_with("x"))  # for selection only
```

### Multi-row summaries

```r
summarise(data, x, .groups = "drop") # -> reframe(data, x)
```

### Data reshaping

```r
gather()/spread()                # -> pivot_longer()/pivot_wider()
```

### String separation (tidyr 1.3+)

```r
separate(col, into = c("a", "b"))
# -> separate_wider_delim(col, delim = "_", names = c("a", "b"))

extract(col, into = "x", regex)
# -> separate_wider_regex(col, patterns = c(x = regex))
```

### Superseded purrr functions (purrr 1.0+)

```r
map_dfr(x, f)                    # -> map(x, f) |> list_rbind()
map_dfc(x, f)                    # -> map(x, f) |> list_cbind()
map2_dfr(x, y, f)                # -> map2(x, y, f) |> list_rbind()
pmap_dfr(list, f)                # -> pmap(list, f) |> list_rbind()
imap_dfr(x, f)                   # -> imap(x, f) |> list_rbind()
```

### Recoding and replacing (dplyr 1.2+)

```r
case_match(x, val ~ result)      # -> recode_values(x, val ~ result)
recode(x, old = "new")           # -> recode_values(x, "old" ~ "new")
                                 #    or replace_values(x, "old" ~ "new")

# Conditional replacement: case_when with .default = x -> replace_when
case_when(
  cond1 ~ val1,
  cond2 ~ val2,
  .default = x
)                                # -> x |> replace_when(cond1 ~ val1, cond2 ~ val2)

# NA handling
coalesce(x, default)             # -> replace_values(x, NA ~ default)
na_if(x, val)                    # -> replace_values(x, val ~ NA)
tidyr::replace_na(x, default)    # -> replace_values(x, NA ~ default)
```

### Filter family (dplyr 1.2+)

```r
# Dropping rows with NA-safe negation
filter(x != val | is.na(x))      # -> filter_out(x == val)

# Combining conditions with OR
filter(cond1 | cond2 | cond3)    # -> filter(when_any(cond1, cond2, cond3))

# Combining conditions with AND (explicit)
filter(cond1 & cond2 & cond3)    # -> filter(when_all(cond1, cond2, cond3))
```

### Serialization

```r
qs::qsave(x, "file.qs")         # -> qs2::qs_save(x, "file.qs2")
qs::qread("file.qs")            # -> qs2::qs_read("file.qs2")
```

### Defunct in dplyr 1.2 (now errors)

```r
# Underscored SE verbs (defunct since 1.2, deprecated since 0.7)
mutate_()                        # -> mutate() with modern programming
filter_()                        # -> filter()
summarise_()                     # -> summarise()
# ... all *_() variants

# _each variants (defunct since 1.2, deprecated since 0.7)
mutate_each()                    # -> mutate(across(...))
summarise_each()                 # -> summarise(across(...))

# Multi-row summarise (defunct since 1.2, deprecated since 1.1)
summarise(data, x)               # -> reframe(data, x) for multi-row results
```

### For side effects

```r
for (x in xs) write_file(x)     # -> walk(xs, write_file)
for (i in seq_along(data)) {
  write_csv(data[[i]], paths[[i]])
}                                # -> walk2(data, paths, write_csv)
```
