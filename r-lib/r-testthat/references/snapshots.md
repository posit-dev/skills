# Snapshot Testing

Snapshot tests record expected output in human-readable files rather than inline code. They are ideal for:

- Complex output that's difficult to verify programmatically
- User-facing messages, warnings, and errors
- Mixed output types (printed text + messages + warnings)
- Binary formats like plots
- Text with complex formatting

## Basic Usage

```r
test_that("error messages are helpful", {
  expect_snapshot(
    my_function(bad_input)
  )
})
```

The first run creates `tests/testthat/_snaps/{test-file}/{test-name}.md` containing the captured output.

## Snapshot Workflow

**Initial creation:**
```r
devtools::test()  # Creates new snapshots
```

**Review changes:**
```r
testthat::snapshot_review('test-name')
```

**Accept changes:**
```r
testthat::snapshot_accept('test-name')
```

**Reject changes:**
```r
testthat::snapshot_reject('test-name')
```

**Download snapshots from GitHub CI:**
```r
testthat::snapshot_download_gh()
```

## Snapshot Types

### Output Snapshots

Capture printed output, messages, warnings, and errors:

```r
test_that("function produces expected output", {
  expect_snapshot({
    print(my_data)
    message("Processing complete")
    warning("Non-critical issue")
  })
})
```

### Value Snapshots

Capture the structure of R objects:

```r
test_that("data structure is correct", {
  expect_snapshot(str(complex_object))
})
```

### Error Snapshots

Capture error messages with call information:

```r
test_that("errors are informative", {
  expect_snapshot(
    error = TRUE,
    my_function(invalid_input)
  )
})
```

## Transform Function

Use `transform` to remove variable elements before comparison:

```r
test_that("output is stable", {
  expect_snapshot(
    my_api_call(),
    transform = function(lines) {
      # Remove timestamps
      gsub("\\d{4}-\\d{2}-\\d{2}", "[DATE]", lines)
    }
  )
})
```

Common uses:
- Remove timestamps or session IDs
- Normalize file paths
- Strip API keys or tokens
- Remove stochastic elements

## Variants

Use `variant` for platform-specific or R-version-specific snapshots:

```r
test_that("platform-specific behavior", {
  expect_snapshot(
    system_specific_function(),
    variant = tolower(Sys.info()[["sysname"]])
  )
})
```

Variants save to `_snaps/{variant}/{test}.md` instead of `_snaps/{test}.md`.

## Best Practices

- **Commit snapshots to git** - They are part of your test suite
- **Review snapshot diffs carefully** - Ensure changes are intentional
- **Keep snapshots focused** - One concept per snapshot
- **Use transform for stability** - Remove variable elements
- **Update snapshots explicitly** - Never auto-accept in CI
- **Fail on new snapshots in CI** - testthat 3.3.0+ does this automatically

## Snapshot Files

Snapshots are stored as markdown files in `tests/testthat/_snaps/`:

```
tests/testthat/
├── test-utils.R
└── _snaps/
    ├── test-utils.md
    └── windows/           # variant snapshots
        └── test-utils.md
```

Each snapshot includes:
- Test name as heading
- Code that generated the output
- Captured output

## Common Patterns

**Testing error messages:**
```r
test_that("validation errors are clear", {
  expect_snapshot(error = TRUE, {
    validate_input(NULL)
    validate_input("wrong type")
    validate_input(numeric())
  })
})
```

**Testing side-by-side comparisons:**
```r
test_that("diff output is readable", {
  withr::local_options(width = 80)
  expect_snapshot(
    waldo::compare(expected, actual)
  )
})
```

**Testing printed output with messages:**
```r
test_that("function provides feedback", {
  expect_snapshot({
    result <- process_data(sample_data)
    print(result)
  })
})
```
