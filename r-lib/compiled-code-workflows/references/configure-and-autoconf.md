# `configure` and Autoconf (when to use it)

A `configure` script can probe the system before compilation (e.g., to find headers/libs or feature flags). It also raises the maintenance cost.

## Use `configure` only when you must

Good reasons:

- You need to detect a system library and compute correct flags.
- You need feature tests that cannot be expressed as simple Makevars settings.

Bad reasons:

- “It feels more professional.”
- You can hard-code paths.

## Keep it minimal

- Prefer a small `configure` that detects what you need and writes variables.
- Keep platform differences explicit (e.g., `configure.win` for Windows).

## CRAN implications

- Don’t download large or variable artifacts during install.
- Don’t generate opaque blobs without shipping sources when required.

## References

- CRAN policy (external libraries, downloads, sources): https://cran.r-project.org/web/packages/policies.html
