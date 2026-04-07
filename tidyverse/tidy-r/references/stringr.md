# String Manipulation with stringr

Use stringr over base R string functions. Benefits: consistent `str_` prefix, string-first argument order, pipe-friendly and vectorized.

## Core patterns

### Pipe-friendly chaining

```r
text |>
  str_to_lower() |>
  str_trim() |>
  str_replace_all("pattern", "replacement") |>
  str_extract("\\d+")
```

### Detection and extraction

```r
str_detect(text, "pattern")       # logical: does it match?
str_which(text, "pattern")        # integer: which elements match?
str_count(text, "pattern")        # integer: how many matches?
str_extract(text, "pattern")      # first match
str_extract_all(text, "pattern")  # all matches (returns list)
str_match(text, "(\\w+)@(\\w+)")  # capture groups as matrix
```

### Replacement

```r
str_replace(text, "old", "new")       # first occurrence
str_replace_all(text, "old", "new")   # all occurrences
str_remove(text, "pattern")           # remove first match
str_remove_all(text, "pattern")       # remove all matches
```

### Splitting and combining

```r
str_split(text, ",")                  # split into list
str_split_fixed(text, ",", n = 3)     # split into matrix (fixed columns)
str_split_i(text, ",", i = 2)         # extract ith piece directly
str_c("a", "b", "c", sep = "-")      # combine with separator
str_flatten(words, collapse = ", ")   # collapse vector to single string
```

### Substring operations

```r
str_sub(text, 1, 5)                   # extract positions 1-5
str_sub(text, -3)                     # last 3 characters
str_length(text)                      # character count
str_trunc(text, 20)                   # truncate with ellipsis
```

### Formatting

```r
str_to_lower(text)                    # lowercase
str_to_upper(text)                    # uppercase
str_to_title(text)                    # title case
str_to_sentence(text)                # sentence case
str_trim(text)                        # remove leading/trailing whitespace
str_squish(text)                      # trim + collapse internal whitespace
str_pad(text, 10, side = "left")      # pad to fixed width
str_wrap(text, width = 80)            # word wrap
```

### Interpolation

```r
str_glue("Hello {name}, you scored {score}!")
str_glue_data(df, "{name}: {value}")
```

## Pattern helpers

Use these for clarity about what kind of matching you intend:

```r
str_detect(text, fixed("$"))           # literal match (no regex)
str_detect(text, regex("\\d+"))        # explicit regex (default)
str_detect(text, regex("hello", ignore_case = TRUE))  # case-insensitive
str_detect(text, coll("e", locale = "fr"))  # locale-aware collation
str_detect(text, boundary("word"))     # word boundaries
```

## stringr vs base R

| stringr | base R | Notes |
|---------|--------|-------|
| `str_detect(text, "pat")` | `grepl("pat", text)` | Argument order differs |
| `str_extract(text, "pat")` | `regmatches(text, regexpr(...))` | Much simpler |
| `str_replace_all(text, "a", "b")` | `gsub("a", "b", text)` | Argument order differs |
| `str_split(text, ",")` | `strsplit(text, ",")` | |
| `str_length(text)` | `nchar(text)` | |
| `str_sub(text, 1, 5)` | `substr(text, 1, 5)` | |
| `str_to_lower(text)` | `tolower(text)` | |
| `str_to_upper(text)` | `toupper(text)` | |
| `str_to_title(text)` | `tools::toTitleCase(text)` | |
| `str_trim(text)` | `trimws(text)` | |
| `str_glue("Hello {x}")` | `sprintf("Hello %s", x)` | More readable |
