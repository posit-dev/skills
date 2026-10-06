# Advanced Testing Topics

## Skipping Tests

Skip tests conditionally when requirements aren't met:

### Built-in Skip Functions

```r
test_that("API integration works", {
  skip_if_offline()
  skip_if_not_installed("httr2")
  skip_on_cran()
  skip_on_os("windows")

  result <- call_external_api()
  expect_true(result$success)
})
```

**Common skip functions:**
- `skip()` - Skip unconditionally with message
- `skip_if()` - Skip if condition is TRUE
- `skip_if_not()` - Skip if condition is FALSE
- `skip_if_offline()` - Skip if no internet
- `skip_if_not_installed(pkg)` - Skip if package unavailable
- `skip_on_cran()` - Skip on CRAN checks
- `skip_on_os(os)` - Skip on specific OS
- `skip_on_ci()` - Skip on continuous integration
- `skip_unless_r(version)` - Skip unless R version requirement met (testthat 3.3.0+)

### Custom Skip Conditions

```r
skip_if_no_api_key <- function() {
  if (Sys.getenv("API_KEY") == "") {
    skip("API_KEY not available")
  }
}

skip_if_slow <- function() {
  if (!identical(Sys.getenv("RUN_SLOW_TESTS"), "true")) {
    skip("Slow tests not enabled")
  }
}

test_that("authenticated endpoint works", {
  skip_if_no_api_key()

  result <- call_authenticated_endpoint()
  expect_equal(result$status, "success")
})
```

## Testing Flaky Code

### retry with `try_again()`

Test code that may fail occasionally (network calls, timing-dependent code):

```r
test_that("flaky network call succeeds eventually", {
  result <- try_again(
    times = 3,
    {
      response <- make_network_request()
      expect_equal(response$status, 200)
      response
    }
  )

  expect_type(result, "list")
})
```

### Mark Tests as Flaky

```r
test_that("timing-sensitive operation", {
  skip_on_cran()  # Too unreliable for CRAN

  start <- Sys.time()
  result <- async_operation()
  duration <- as.numeric(Sys.time() - start)

  expect_lt(duration, 2)  # Should complete in < 2 seconds
})
```

## Managing Secrets in Tests

### Environment Variables

```r
test_that("authenticated API works", {
  # Skip if credentials unavailable
  api_key <- Sys.getenv("MY_API_KEY")
  skip_if(api_key == "", "MY_API_KEY not set")

  result <- call_api(api_key)
  expect_true(result$authenticated)
})
```

### Local Configuration Files

```r
test_that("service integration works", {
  config_path <- test_path("fixtures", "test_config.yml")
  skip_if_not(file.exists(config_path), "Test config not found")

  config <- yaml::read_yaml(config_path)
  result <- connect_to_service(config)
  expect_true(result$connected)
})
```

**Never commit secrets:**
- Add config files with secrets to `.gitignore`
- Use environment variables in CI/CD
- Provide example config files: `test_config.yml.example`

### Testing Without Secrets

Design tests to degrade gracefully:

```r
test_that("API client works", {
  api_key <- Sys.getenv("API_KEY")

  if (api_key == "") {
    # Mock the API when credentials unavailable
    local_mocked_bindings(
      make_api_call = function(...) list(status = "success", data = "mocked")
    )
  }

  result <- my_api_wrapper()
  expect_equal(result$status, "success")
})
```

## Custom Expectations

Create domain-specific expectations for clearer tests:

### Simple Custom Expectations

```r
# In helper-expectations.R
expect_valid_email <- function(email) {
  expect_match(email, "^[^@]+@[^@]+\\.[^@]+$")
}

expect_positive <- function(x) {
  expect_true(all(x > 0), info = "All values should be positive")
}

expect_named_list <- function(object, names) {
  expect_type(object, "list")
  expect_named(object, names, ignore.order = TRUE)
}
```

Usage:

```r
test_that("user validation works", {
  user <- create_user("test@example.com")
  expect_valid_email(user$email)
})
```

### Complex Custom Expectations

```r
expect_valid_model <- function(model) {
  act <- quasi_label(rlang::enquo(model))

  expect(
    inherits(act$val, "lm") && !is.null(act$val$coefficients),
    sprintf("%s is not a valid linear model", act$lab)
  )

  invisible(act$val)
}
```

## State Inspection

Detect unintended global state changes:

```r
# In setup-state.R
set_state_inspector(function() {
  list(
    options = options(),
    env_vars = Sys.getenv(),
    search = search()
  )
})
```

testthat will warn if state changes between tests.

## CRAN-Specific Considerations

### Time Limits

Tests must complete in under 1 minute:

```r
test_that("slow operation completes", {
  skip_on_cran()  # Takes 2 minutes

  result <- expensive_computation()
  expect_equal(result$status, "complete")
})
```

### File System Discipline

Only write to temp directory:

```r
test_that("file output works", {
  # Good
  output <- withr::local_tempfile(fileext = ".csv")
  write.csv(data, output)

  # Bad - writes to package directory
  # write.csv(data, "output.csv")
})
```

### No External Dependencies

Avoid relying on:
- Network access
- External processes
- System commands
- Clipboard access

```r
test_that("external dependency", {
  skip_on_cran()

  # Code requiring network or system calls
})
```

### Platform Differences

Use `expect_equal()` for numeric comparisons (allows tolerance):

```r
test_that("calculation works", {
  result <- complex_calculation()

  # Good: tolerant to floating point differences
  expect_equal(result, 1.234567)

  # Bad: fails due to platform differences
  # expect_identical(result, 1.234567)
})
```

## Test Performance

### Identify Slow Tests

```r
devtools::test(reporter = "slow")
```

The `SlowReporter` highlights performance bottlenecks.

### Test Shuffling

Detect unintended test dependencies:

```r
# Randomly reorder tests
devtools::test(shuffle = TRUE)

# In test file
test_dir("tests/testthat", shuffle = TRUE)
```

If tests fail when shuffled, they have unintended dependencies on execution order.

## Parallel Testing

Enable parallel test execution in `DESCRIPTION`:

```
Config/testthat/parallel: true
```

**Requirements for parallel tests:**
- Tests must be independent
- No shared state between tests
- Use `local_*()` functions for all side effects
- Snapshot tests work correctly in parallel (testthat 3.2.0+)

## Testing Edge Cases

### Boundary Conditions

```r
test_that("handles boundary conditions", {
  expect_equal(my_func(0), expected_at_zero)
  expect_equal(my_func(-1), expected_negative)
  expect_equal(my_func(Inf), expected_infinite)
  expect_true(is.nan(my_func(NaN)))
})
```

### Empty Inputs

```r
test_that("handles empty inputs", {
  expect_equal(process(character()), character())
  expect_equal(process(NULL), NULL)
  expect_equal(process(data.frame()), data.frame())
})
```

### Type Validation

```r
test_that("validates input types", {
  expect_error(my_func("string"), class = "vctrs_error_cast")
  expect_error(my_func(list()), "must be atomic")
  expect_no_error(my_func(1:10))
})
```

## Debugging Failed Tests

### Interactive Debugging

```r
# Run test interactively
devtools::load_all()
test_that("problematic test", {
  # Add browser() to pause execution
  browser()

  result <- problematic_function()
  expect_equal(result, expected)
})
```

### Print Debugging in Tests

```r
test_that("debug output", {
  data <- prepare_data()
  print(str(data))  # Visible when test fails

  result <- process(data)
  print(result)

  expect_equal(result, expected)
})
```

### Capture Output for Inspection

```r
test_that("inspect messages", {
  messages <- capture_messages(
    result <- function_with_messages()
  )

  print(messages)  # See all messages when test fails
  expect_match(messages, "Processing complete")
})
```

## Testing R6 Classes

```r
test_that("R6 class works", {
  obj <- MyClass$new(value = 10)

  expect_r6_class(obj, "MyClass")  # testthat 3.3.0+
  expect_equal(obj$value, 10)

  obj$increment()
  expect_equal(obj$value, 11)
})
```

## Testing S4 Classes

```r
test_that("S4 validity works", {
  obj <- new("MyClass", slot1 = 10, slot2 = "test")

  expect_s4_class(obj, "MyClass")
  expect_equal(obj@slot1, 10)

  expect_error(
    new("MyClass", slot1 = -1),
    "slot1 must be positive"
  )
})
```
