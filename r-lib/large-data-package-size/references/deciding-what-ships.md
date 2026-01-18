# Deciding what ships in the package

A package is not a general-purpose file distribution mechanism.

Use this decision tree:

## Ship it inside the package when

- it is required for core functionality
- it is small enough to keep the package lean
- it does not change frequently

## Prefer an external strategy when

- the data is large (dominates tarball size)
- it updates frequently
- it is user-specific or cache-like
- it is generated from upstream sources

External strategy options:

- separate data-only package (updates rarely)
- optional download in an explicit user action (not at install time)
- user-managed caching in an appropriate user directory

CRAN policy explicitly encourages keeping packages of the minimum necessary size and suggests separate data-only packages when large data is required.

## References

- CRAN policy (package size guidance): https://cran.r-project.org/web/packages/policies.html
