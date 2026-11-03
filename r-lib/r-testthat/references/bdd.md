# BDD-Style Testing with describe() and it()

Behavior-Driven Development (BDD) testing uses `describe()` and `it()` to create specification-style tests that read like natural language descriptions of behavior.

## When to Use BDD Syntax

**Use BDD (`describe`/`it`) when:**
- Documenting intended behavior of new features
- Testing complex components with multiple related facets
- Following test-first development workflows
- Tests serve as specification documentation
- You want hierarchical organization of related tests
- A group of tests (in `it()` statements) rely on a single fixture or local options/envvars (set up in `describe()`)

**Use standard syntax (`test_that`) when:**
- Writing straightforward unit tests
- Testing implementation details
- Converting existing test_that() tests (no need to change working code)

**Key insight from testthat:** "Use `describe()` to verify you implement the right things, use `test_that()` to ensure you do things right."

## Basic BDD Syntax

### Simple Specifications

```r
describe("matrix()", {
  it("can be multiplied by a scalar", {
    m1 <- matrix(1:4, 2, 2)
    m2 <- m1 * 2
    expect_equal(matrix(1:4 * 2, 2, 2), m2)
  })

  it("can be transposed", {
    m <- matrix(1:4, 2, 2)
    expect_equal(t(m), matrix(c(1, 3, 2, 4), 2, 2))
  })

  it("can compute determinant", {
    m <- matrix(c(1, 2, 3, 4), 2, 2)
    expect_equal(det(m), -2)
  })
})
```

Each `it()` block:
- Defines one specification (like `test_that()`)
- Runs in its own environment
- Has access to all expectations
- Can use withr and other testing tools

## Nested Specifications

Group related specifications hierarchically:

```r
describe("User authentication", {
  describe("login()", {
    it("accepts valid credentials", {
      result <- login("user@example.com", "password123")
      expect_true(result$authenticated)
      expect_type(result$token, "character")
    })

    it("rejects invalid email", {
      expect_error(
        login("invalid-email", "password"),
        class = "validation_error"
      )
    })

    it("rejects wrong password", {
      expect_error(
        login("user@example.com", "wrong"),
        class = "auth_error"
      )
    })
  })

  describe("logout()", {
    it("clears session token", {
      session <- create_session()
      logout(session)
      expect_null(session$token)
    })

    it("invalidates refresh token", {
      session <- create_session()
      logout(session)
      expect_error(refresh(session), "Invalid token")
    })
  })

  describe("password_reset()", {
    it("sends reset email", {
      local_mocked_bindings(send_email = function(...) TRUE)
      result <- password_reset("user@example.com")
      expect_true(result$email_sent)
    })

    it("generates secure token", {
      result <- password_reset("user@example.com")
      expect_gte(nchar(result$token), 32)
    })
  })
})
```

Nesting creates clear hierarchies:
- Top level: Component or module
- Second level: Functions or features
- Third level: Specific behaviors

## Pending Specifications

Mark unimplemented tests by omitting the code:

```r
describe("division()", {
  it("divides two numbers", {
    expect_equal(division(10, 2), 5)
  })

  it("returns Inf for division by zero")  # Pending

  it("handles complex numbers")  # Pending
})
```

Pending tests:
- Show up in test output as "SKIPPED"
- Document planned functionality
- Serve as TODO markers
- Don't cause test failures

## Complete Test File Example

```r
# tests/testthat/test-data-processor.R

describe("DataProcessor", {
  describe("initialization", {
    it("creates processor with default config", {
      proc <- DataProcessor$new()
      expect_r6_class(proc, "DataProcessor")
      expect_equal(proc$config$timeout, 30)
    })

    it("accepts custom configuration", {
      proc <- DataProcessor$new(config = list(timeout = 60))
      expect_equal(proc$config$timeout, 60)
    })

    it("validates configuration options", {
      expect_error(
        DataProcessor$new(config = list(timeout = -1)),
        "timeout must be positive"
      )
    })
  })

  describe("process()", {
    describe("with valid data", {
      it("processes numeric data", {
        proc <- DataProcessor$new()
        result <- proc$process(data.frame(x = 1:10))
        expect_s3_class(result, "data.frame")
        expect_equal(nrow(result), 10)
      })

      it("handles missing values", {
        proc <- DataProcessor$new()
        data <- data.frame(x = c(1, NA, 3))
        result <- proc$process(data)
        expect_false(anyNA(result$x))
      })

      it("preserves column names", {
        proc <- DataProcessor$new()
        data <- data.frame(foo = 1:3, bar = 4:6)
        result <- proc$process(data)
        expect_named(result, c("foo", "bar"))
      })
    })

    describe("with invalid data", {
      it("rejects NULL input", {
        proc <- DataProcessor$new()
        expect_error(proc$process(NULL), "data cannot be NULL")
      })

      it("rejects empty data frame", {
        proc <- DataProcessor$new()
        expect_error(proc$process(data.frame()), "data cannot be empty")
      })

      it("rejects non-data.frame input", {
        proc <- DataProcessor$new()
        expect_error(proc$process(list()), class = "type_error")
      })
    })
  })

  describe("summary()", {
    it("returns summary statistics", {
      proc <- DataProcessor$new()
      data <- data.frame(x = 1:10, y = 11:20)
      proc$process(data)

      summary <- proc$summary()
      expect_type(summary, "list")
      expect_named(summary, c("rows", "cols", "processed_at"))
    })

    it("throws error if no data processed", {
      proc <- DataProcessor$new()
      expect_error(proc$summary(), "No data has been processed")
    })
  })
})
```

## Organizing Files with BDD

### Single Component per File

```r
# tests/testthat/test-user-model.R
describe("User model", {
  describe("validation", { ... })
  describe("persistence", { ... })
  describe("relationships", { ... })
})
```

### Multiple Related Components

```r
# tests/testthat/test-math-operations.R
describe("arithmetic operations", {
  describe("addition()", { ... })
  describe("subtraction()", { ... })
  describe("multiplication()", { ... })
  describe("division()", { ... })
})
```

### Hierarchical Domain Organization

```r
# tests/testthat/test-api-endpoints.R
describe("API endpoints", {
  describe("/users", {
    describe("GET /users", { ... })
    describe("POST /users", { ... })
    describe("GET /users/:id", { ... })
  })

  describe("/posts", {
    describe("GET /posts", { ... })
    describe("POST /posts", { ... })
  })
})
```

## Mixing BDD and Standard Syntax

You can use both styles in the same test file:

```r
# tests/testthat/test-calculator.R

# BDD style for user-facing functionality
describe("Calculator user interface", {
  describe("button clicks", {
    it("registers numeric input", { ... })
    it("handles operator keys", { ... })
  })
})

# Standard style for internal helpers
test_that("parse_expression() tokenizes correctly", {
  tokens <- parse_expression("2 + 3")
  expect_equal(tokens, c("2", "+", "3"))
})

test_that("evaluate_tokens() handles operator precedence", {
  result <- evaluate_tokens(c("2", "+", "3", "*", "4"))
  expect_equal(result, 14)
})
```

**Mixing guidelines:**
- Use BDD for behavioral specifications
- Use `test_that()` for implementation details
- Keep related tests in the same style within a section
- Don't nest `test_that()` inside `describe()` or vice versa

## BDD with Test Fixtures

Use the same fixture patterns as standard tests:

```r
describe("File processor", {
  # Helper function for tests
  new_test_file <- function(content) {
    path <- withr::local_tempfile(lines = content)
    path
  }

  describe("read_file()", {
    it("reads text files", {
      file <- new_test_file(c("line1", "line2"))
      result <- read_file(file)
      expect_length(result, 2)
    })

    it("handles empty files", {
      file <- new_test_file(character())
      result <- read_file(file)
      expect_equal(result, character())
    })
  })
})
```

## BDD with Snapshot Tests

Snapshots work naturally with BDD:

```r
describe("error messages", {
  it("provides helpful validation errors", {
    expect_snapshot(error = TRUE, {
      validate_user(NULL)
      validate_user(list())
      validate_user(list(email = "invalid"))
    })
  })

  it("shows clear permission errors", {
    expect_snapshot(error = TRUE, {
      check_permission("guest", "admin")
    })
  })
})
```

## BDD with Mocking

```r
describe("API client", {
  describe("fetch_user()", {
    it("handles successful response", {
      local_mocked_bindings(
        http_get = function(url) {
          list(status = 200, body = '{"id": 1, "name": "Test"}')
        }
      )

      user <- fetch_user(1)
      expect_equal(user$name, "Test")
    })

    it("handles 404 errors", {
      local_mocked_bindings(
        http_get = function(url) list(status = 404)
      )

      expect_error(fetch_user(999), class = "not_found_error")
    })
  })
})
```

## Test-First Workflow with BDD

1. **Write specifications first:**

```r
describe("order_total()", {
  it("sums item prices")
  it("applies tax")
  it("applies discount codes")
  it("handles free shipping threshold")
})
```

2. **Implement one specification at a time:**

```r
describe("order_total()", {
  it("sums item prices", {
    order <- list(items = list(
      list(price = 10),
      list(price = 20)
    ))
    expect_equal(order_total(order), 30)
  })

  it("applies tax")
  it("applies discount codes")
  it("handles free shipping threshold")
})
```

3. **Continue until all specs have implementations**

This workflow ensures you:
- Think about requirements before implementation
- Have clear success criteria
- Build incrementally
- Maintain focus on behavior

## Comparison: describe/it vs test_that

**describe/it:**
```r
describe("str_length()", {
  it("counts characters in string", {
    expect_equal(str_length("abc"), 3)
  })

  it("handles empty strings", {
    expect_equal(str_length(""), 0)
  })
})
```

**test_that:**
```r
test_that("str_length() counts characters", {
  expect_equal(str_length("abc"), 3)
})

test_that("str_length() handles empty strings", {
  expect_equal(str_length(""), 0)
})
```

Key differences:
- BDD groups related specs under `describe()`
- BDD uses "it" instead of "test_that"
- BDD enables nesting for hierarchy
- BDD supports pending specs without code
- Both produce identical test results

Choose based on your preferences and project style.
