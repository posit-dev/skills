# CRAN policy gotchas (common patterns)

This file captures recurring sources of CRAN feedback, with an emphasis on common failure modes and the fastest path to a CRAN-friendly fix.

## 1) Examples and vignettes

Avoid code in examples/tests/vignettes that is:

- network-dependent
- flaky / non-deterministic (unseeded randomness, time/date assumptions)
- long-running
- interactive (menus, prompts)
- writing outside temporary directories

Prefer:

- small deterministic examples
- `set.seed()` where randomness is used
- guarding optional features behind suggested packages:

  ```r
  if (requireNamespace("pkg", quietly = TRUE)) {
  	# example that uses pkg
  }
  ```

Notes:

- Use `\dontrun{}` sparingly; prefer examples that are safe to run.
- If something is only “sometimes safe” (e.g., network), consider `\donttest{}` and/or robust fallbacks.

## 2) Files, paths, and side effects

- Don’t write to the working directory.
- Prefer `tempdir()` / `withr::local_tempdir()`.
- Don’t write to the user’s home directory.
- Clean up any temporary files you create.

## 3) Dependency declarations and conditional usage

- If your package code uses a package at runtime, it generally belongs in `Imports`.
- `Suggests` is appropriate for optional features, optional examples/vignettes, and testing.

CRAN policy strongly prefers that packages listed in `Suggests` are used conditionally (so checks don’t fail when they’re not installed).

## 4) Package size and long runtimes

Common triggers:

- large embedded data
- large PDFs or other documentation artifacts
- long-running examples or vignettes

Practical mitigations:

- compress data and keep package size to the minimum necessary
- keep examples short (they’re examples, not tutorials)
- make expensive computations optional (but keep enough tests to validate correctness)

## 5) External software and downloads

- Source packages may not contain binary executables.
- Downloading content at install time is discouraged; if you must download, use secure mechanisms (https) and fixed versions.

If your package needs external libraries, ensure installation checks for existing system installs and provide clear build instructions.

## 6) Portability and platform differences

Common cross-platform gotchas:

- Windows paths and encoding issues
- case-insensitive file systems
- locale differences
- missing system libraries (CI passes on one OS, fails on another)

If something fails only on one platform, treat it as a portability bug.

## 7) “Policy-shaped” NOTEs

Some NOTE types usually deserve immediate attention:

- “uses the internet” checks
- writing outside tempdirs
- timeouts / long runtimes
- missing or inconsistent DESCRIPTION metadata

See also:

- CRAN policy: https://cran.r-project.org/web/packages/policies.html
