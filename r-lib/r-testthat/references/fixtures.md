# Test Fixtures and Data Management

Test fixtures arrange the environment into a known state for testing. testthat provides several approaches for managing test data and state.

## Fixture Approaches

### Constructor Helper Functions

Create reusable test objects on-demand:

```r
# In tests/testthat/helper-fixtures.R or within test file
new_sample_data <- function(n = 10) {
  data.frame(
    id = seq_len(n),
    value = rnorm(n),
    category = sample(letters[1:3], n, replace = TRUE)
  )
}

test_that("function handles data correctly", {
  data <- new_sample_data(5)
  result <- process_data(data)
  expect_equal(nrow(result), 5)
})
```

**Advantages:**
- Fresh data for each test
- Parameterizable
- No file I/O

**Use when:**
- Data is cheap to create
- Multiple tests need similar but not identical data
- Data should vary between tests

### Local Functions with Cleanup

Handle side effects using `withr::defer()`:

```r
local_temp_csv <- function(data, pattern = "test", env = parent.frame()) {
  path <- withr::local_tempfile(pattern = pattern, fileext = ".csv", .local_envir = env)
  write.csv(data, path, row.names = FALSE)
  path
}

test_that("CSV reading works", {
  data <- data.frame(x = 1:3, y = letters[1:3])
  csv_path <- local_temp_csv(data)

  result <- read_my_csv(csv_path)
  expect_equal(result, data)
  # File automatically cleaned up after test
})
```

**Advantages:**
- Automatic cleanup
- Encapsulates setup and teardown
- Composable

**Use when:**
- Tests create side effects (files, connections)
- Setup requires multiple steps
- Cleanup logic is non-trivial

### Static Fixture Files

Store pre-created data files in `tests/testthat/fixtures/`:

```
tests/testthat/
├── fixtures/
│   ├── sample_data.rds
│   ├── config.json
│   └── reference_output.csv
└── test-processing.R
```

Access with `test_path()`:

```r
test_that("function processes real data", {
  data <- readRDS(test_path("fixtures", "sample_data.rds"))
  result <- process_data(data)

  expected <- readRDS(test_path("fixtures", "expected_output.rds"))
  expect_equal(result, expected)
})
```

**Advantages:**
- Tests against real data
- Expensive-to-create data computed once
- Human-readable (for JSON, CSV, etc.)

**Use when:**
- Data is expensive to create
- Data represents real-world cases
- Multiple tests use identical data
- Data is complex or represents edge cases

## Helper Files

Files in `tests/testthat/` starting with `helper-` are automatically sourced before tests run.

```r
# tests/testthat/helper-fixtures.R

# Custom expectations
expect_valid_user <- function(user) {
  expect_type(user, "list")
  expect_named(user, c("id", "name", "email"))
  expect_type(user$id, "integer")
}

# Test data constructors
new_user <- function(id = 1L, name = "Test User", email = "test@example.com") {
  list(id = id, name = name, email = email)
}

# Shared fixtures
standard_config <- function() {
  list(
    timeout = 30,
    retries = 3,
    verbose = FALSE
  )
}
```

Then use in tests:

```r
test_that("user validation works", {
  user <- new_user()
  expect_valid_user(user)
})
```

## Setup Files

Files starting with `setup-` run only during `R CMD check` and `devtools::test()`, not during `devtools::load_all()`.

```r
# tests/testthat/setup-options.R

# Set options for test suite
withr::local_options(
  list(
    reprex.clipboard = FALSE,
    reprex.html_preview = FALSE,
    usethis.quiet = TRUE
  ),
  .local_envir = teardown_env()
)
```

**Use setup files for:**
- Package-wide test options
- Environment variable configuration
- One-time expensive operations
- Test suite initialization

## Managing File System State

### Use temp directories exclusively

```r
test_that("file writing works", {
  # Good: write to temp directory
  path <- withr::local_tempfile(lines = c("line1", "line2"))

  # Bad: write to working directory
  # writeLines(c("line1", "line2"), "test_file.txt")

  result <- process_file(path)
  expect_equal(result, expected)
})
```

### Clean up automatically with withr

```r
test_that("directory operations work", {
  # Create temp dir that auto-cleans
  dir <- withr::local_tempdir()

  # Create files in it
  file.create(file.path(dir, "file1.txt"))
  file.create(file.path(dir, "file2.txt"))

  result <- process_directory(dir)
  expect_length(result, 2)
  # Directory automatically removed after test
})
```

### Test files stored in fixtures

```r
test_that("file parsing handles edge cases", {
  # Read from committed fixture
  malformed <- test_path("fixtures", "malformed.csv")

  expect_warning(
    result <- robust_read_csv(malformed),
    "Malformed"
  )
  expect_true(nrow(result) > 0)
})
```

## Database Fixtures

### In-memory SQLite

```r
test_that("database queries work", {
  con <- DBI::dbConnect(RSQLite::SQLite(), ":memory:")
  withr::defer(DBI::dbDisconnect(con))

  # Create schema
  DBI::dbExecute(con, "CREATE TABLE users (id INTEGER, name TEXT)")
  DBI::dbExecute(con, "INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')")

  result <- query_users(con)
  expect_equal(nrow(result), 2)
})
```

### Fixture SQL scripts

```r
test_that("complex queries work", {
  con <- DBI::dbConnect(RSQLite::SQLite(), ":memory:")
  withr::defer(DBI::dbDisconnect(con))

  # Load schema from fixture
  schema <- readLines(test_path("fixtures", "schema.sql"))
  DBI::dbExecute(con, paste(schema, collapse = "\n"))

  result <- complex_query(con)
  expect_s3_class(result, "data.frame")
})
```

## Complex Object Fixtures

### Save and load complex objects

Create fixtures interactively:

```r
# Run once to create fixture
complex_model <- expensive_training_function(data)
saveRDS(complex_model, "tests/testthat/fixtures/trained_model.rds")
```

Use in tests:

```r
test_that("predictions work", {
  model <- readRDS(test_path("fixtures", "trained_model.rds"))

  new_data <- data.frame(x = 1:5, y = 6:10)
  predictions <- predict(model, new_data)

  expect_length(predictions, 5)
  expect_type(predictions, "double")
})
```

## Fixture Organization

```
tests/testthat/
├── fixtures/
│   ├── data/              # Input data
│   │   ├── sample.csv
│   │   └── users.json
│   ├── expected/          # Expected outputs
│   │   ├── processed.rds
│   │   └── summary.txt
│   ├── models/            # Trained models
│   │   └── classifier.rds
│   └── sql/               # Database schemas
│       └── schema.sql
├── helper-constructors.R  # Data constructors
├── helper-expectations.R  # Custom expectations
├── setup-options.R        # Test suite config
└── test-*.R               # Test files
```

## Best Practices

**Keep fixtures small:**
- Store minimal data needed for tests
- Use constructors for variations
- Commit fixtures to version control

**Document fixture origins:**
```r
# tests/testthat/fixtures/README.md
# sample_data.rds
Created from production data on 2024-01-15
Contains 100 representative records with PII removed

# malformed.csv
Edge case discovered in issue #123
Contains intentional formatting errors
```

**Use consistent paths:**
```r
# Always use test_path() for portability
data <- readRDS(test_path("fixtures", "data.rds"))

# Never use relative paths
# data <- readRDS("fixtures/data.rds")  # Bad
```

**Prefer deterministic fixtures:**
```r
# Good: reproducible
set.seed(123)
data <- data.frame(x = rnorm(10))

# Better: no randomness
data <- data.frame(x = seq(-2, 2, length.out = 10))
```
