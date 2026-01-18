# Compiled code quality gates

Compiled code raises the cost of portability mistakes. Treat these as non-negotiable quality gates.

## Gate 1: `R CMD check` stays boring

- Run `devtools::check()` early and often.
- Keep warnings and NOTEs from accumulating.
- Remember that your local machine is not the target environment.

## Gate 2: No “terminate the R process” behaviors

Compiled code must not terminate the running R process.

Avoid (or compile out) anything that can hard-stop the process:

- C/C++: `assert`, `abort`, `exit`, `std::terminate`
- Fortran: `STOP`

Instead:

- return an error to R (`Rf_error()` / `Rcpp::stop()`), or
- propagate an error code and handle it in R

CRAN policy explicitly calls this out as unacceptable behavior.

## Gate 3: Portability by default

- Never assume a particular compiler (GCC vs clang vs MSVC) feature set.
- Avoid undefined behavior.
- Avoid non-standard extensions unless guarded and justified.

## Gate 4: Deterministic results

- If randomness is involved, make seeding explicit.
- Avoid depending on system locale for parsing/formatting.

## Gate 5: Dependency discipline

- Header-only libraries: prefer vendoring as an R package dependency and using `LinkingTo`.
- System libraries: document and detect, but avoid fragile downloads at install time.

## References

- CRAN policy (compiled code behavior, package size, external libraries): https://cran.r-project.org/web/packages/policies.html
