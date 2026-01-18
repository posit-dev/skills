# Caching and user directories

Sometimes you can’t ship large data, but you still want a good user experience.

## CRAN-friendly principle

Packages should not write to the user’s home directory by default.

For R >= 4.0, CRAN policy allows packages to store user-specific data/config/cache files in user directories obtained from `tools::R_user_dir()`, provided that:

- sizes are kept as small as possible by default
- contents are actively managed (including removing outdated material)

## Design checklist

- Make caching opt-in or clearly user-triggered.
- Provide a way to:
  - list cache size
  - clear cache
  - set cache location (advanced)

## References

- CRAN policy (writing to user directories, `tools::R_user_dir()`): https://cran.r-project.org/web/packages/policies.html
