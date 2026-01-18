# Running checks “as CRAN”

CRAN explicitly asks maintainers to run `R CMD check --as-cran` on the source tarball that will be submitted.

This reference focuses on a practical workflow that gets you as close as possible to what CRAN will do, while keeping iteration time reasonable.

## Recommended workflow

### 1) Start from a clean state

- Work from a clean git checkout (or at least no uncommitted changes).
- Prefer a clean library (so you notice missing dependencies early).

### 2) Build a source tarball

From the package root:

```sh
R CMD build .
```

This produces a tarball like `pkg_1.2.3.tar.gz`.

### 3) Run `R CMD check --as-cran` on the tarball

```sh
R CMD check --as-cran pkg_1.2.3.tar.gz
```

Why check the tarball?

- it checks exactly what you will upload
- it avoids “works locally, fails from tarball” differences
- it mirrors CRAN’s expectation

### 4) Read the _first_ real problem

When checks fail, later messages are often cascading effects.

Practical approach:

- scan for the first “ERROR”
- then inspect the relevant log in the `pkg.Rcheck/` directory

Common log entry points:

- `pkg.Rcheck/00check.log`
- `pkg.Rcheck/00install.out`
- `pkg.Rcheck/tests/testthat.Rout*` (if tests fail)

### 5) Re-check after fixes

- Fix one issue at a time.
- Re-run the same tarball check loop.

For faster iterations, you can use `devtools::check(args = "--as-cran")`, but for submission confidence, do the tarball check at least once.

## Platform preflight

Even if your local tarball check is clean:

- run CI on Linux/macOS/Windows when feasible
- use hosted check services if you don’t have access to those machines

Common options:

- win-builder: https://win-builder.r-project.org/
- macbuilder: https://mac.r-project.org/macbuilder/submit.html

## References

- CRAN policy (Submission section): https://cran.r-project.org/web/packages/policies.html
- CRAN submission checklist: https://cran.r-project.org/web/packages/submission_checklist.html
