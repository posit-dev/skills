# Mocking in testthat

Mocking temporarily replaces function implementations during testing, enabling tests when dependencies are unavailable or impractical (databases, APIs, file systems, expensive computations).

## Core Mocking Functions

### `local_mocked_bindings()`

Replace function implementations within a test:

```r
test_that("function works with mocked dependency", {
  local_mocked_bindings(
    get_user_data = function(id) {
      list(id = id, name = "Test User", role = "admin")
    }
  )

  result <- process_user(123)
  expect_equal(result$name, "Test User")
})
```

### `with_mocked_bindings()`

Replace functions for a specific code block:

```r
test_that("handles API failures gracefully", {
  result <- with_mocked_bindings(
    api_call = function(...) stop("Network error"),
    {
      tryCatch(
        fetch_data(),
        error = function(e) "fallback"
      )
    }
  )

  expect_equal(result, "fallback")
})
```

## S3 Method Mocking

Use `local_mocked_s3_method()` to mock S3 methods:

```r
test_that("custom print method is used", {
  local_mocked_s3_method(
    print, "myclass",
    function(x, ...) cat("Mocked output\n")
  )

  obj <- structure(list(), class = "myclass")
  expect_output(print(obj), "Mocked output")
})
```

## S4 Method Mocking

Use `local_mocked_s4_method()` for S4 methods:

```r
test_that("S4 method override works", {
  local_mocked_s4_method(
    "show", "MyS4Class",
    function(object) cat("Mocked S4 output\n")
  )

  # Test code using the mocked method
})
```

## R6 Class Mocking

Use `local_mocked_r6_class()` to mock R6 classes:

```r
test_that("R6 mock works", {
  MockDatabase <- R6::R6Class("MockDatabase",
    public = list(
      query = function(sql) data.frame(result = "mocked")
    )
  )

  local_mocked_r6_class("Database", MockDatabase)

  db <- Database$new()
  expect_equal(db$query("SELECT *"), data.frame(result = "mocked"))
})
```

## Common Mocking Patterns

### Database Connections

```r
test_that("database queries work", {
  local_mocked_bindings(
    dbConnect = function(...) list(connected = TRUE),
    dbGetQuery = function(conn, sql) {
      data.frame(id = 1:3, value = c("a", "b", "c"))
    }
  )

  result <- fetch_from_db("SELECT * FROM table")
  expect_equal(nrow(result), 3)
})
```

### API Calls

```r
test_that("API integration works", {
  local_mocked_bindings(
    httr2::request = function(url) list(url = url),
    httr2::req_perform = function(req) {
      list(status_code = 200, content = '{"success": true}')
    }
  )

  result <- call_external_api()
  expect_true(result$success)
})
```

### File System Operations

```r
test_that("file processing works", {
  local_mocked_bindings(
    file.exists = function(path) TRUE,
    readLines = function(path) c("line1", "line2", "line3")
  )

  result <- process_file("dummy.txt")
  expect_length(result, 3)
})
```

### Random Number Generation

```r
test_that("randomized algorithm is deterministic", {
  local_mocked_bindings(
    runif = function(n, ...) rep(0.5, n),
    rnorm = function(n, ...) rep(0, n)
  )

  result <- randomized_function()
  expect_equal(result, expected_value)
})
```

## Advanced Mocking Packages

### webfakes

Create fake web servers for HTTP testing:

```r
test_that("API client handles responses", {
  app <- webfakes::new_app()
  app$get("/users/:id", function(req, res) {
    res$send_json(list(id = req$params$id, name = "Test"))
  })

  web <- webfakes::local_app_process(app)

  result <- get_user(web$url("/users/123"))
  expect_equal(result$name, "Test")
})
```

### httptest2

Record and replay HTTP interactions:

```r
test_that("API call returns expected data", {
  httptest2::with_mock_dir("fixtures/api", {
    result <- call_real_api()
    expect_equal(result$status, "success")
  })
})
```

First run records real responses; subsequent runs replay them.

## Mocking Best Practices

**Mock at the right level:**
- Mock external dependencies (APIs, databases)
- Don't mock internal package functions excessively
- Keep mocks simple and focused

**Verify mock behavior:**
```r
test_that("mock is called correctly", {
  calls <- list()
  local_mocked_bindings(
    external_func = function(...) {
      calls <<- append(calls, list(list(...)))
      "mocked"
    }
  )

  my_function()

  expect_length(calls, 1)
  expect_equal(calls[[1]]$arg, "expected")
})
```

**Prefer real fixtures when possible:**
- Use test data files instead of mocking file reads
- Use webfakes for full HTTP testing instead of mocking individual functions
- Mock only when fixtures are impractical

**Document what's being mocked:**
```r
test_that("handles unavailable service", {
  # Mock the external authentication service
  # which is unavailable in test environment
  local_mocked_bindings(
    auth_check = function(token) list(valid = TRUE)
  )

  # test code
})
```

## Migration from Deprecated Functions

**Old (deprecated):**
```r
with_mock(
  pkg::func = function(...) "mocked"
)
```

**New (recommended):**
```r
local_mocked_bindings(
  func = function(...) "mocked",
  .package = "pkg"
)
```

The new functions work with byte-compiled code and are more reliable across platforms.
