# Versioning

This repo does not enforce one “true” versioning scheme, but you should be consistent.

## Practical guidance

- Use **patch** releases for bug fixes and internal improvements.
- Use **minor** releases for new features that preserve backward compatibility.
- Use **major** releases for breaking changes.

CRAN-specific constraints:

- every CRAN resubmission/update must have an increased version number
- even if you are fixing a submission rejection, increasing the version reduces confusion

## usethis helpers

```r
usethis::use_version("patch")
usethis::use_version("minor")
usethis::use_version("major")
usethis::use_version("dev")
usethis::use_dev_version()
```

Key behaviors (per usethis documentation):

- updates the `Version` field in `DESCRIPTION`
- adds a new heading to `NEWS.md` (if it exists)
- commits those changes if the project uses Git (and can optionally push)

## Dev versions

usethis uses a 4-component “dev” version convention:

`<major>.<minor>.<patch>.<dev>`

For example, after releasing `1.2.3`, a common convention is to bump to `1.2.3.9000`.

Whether you use dev versions is a project choice, but if you do, be consistent.

## References

- usethis: https://usethis.r-lib.org/reference/use_version.html
- R Packages (2e): version numbers: https://r-pkgs.org/lifecycle.html#sec-lifecycle-version-number
- CRAN policy (re-submission section): https://cran.r-project.org/web/packages/policies.html
