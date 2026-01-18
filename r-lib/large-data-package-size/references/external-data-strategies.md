# External data strategies

When data is too large to ship, choose an explicit strategy rather than ad-hoc downloads.

## Option 1: Separate data-only package

Best when:

- data is static or updates rarely
- data is broadly useful

This aligns with CRAN policy guidance for large data.

## Option 2: Optional downloads triggered by the user

Best when:

- data is large and not every user needs it

Rules of thumb:

- don’t download at install time
- use secure URLs (`https`)
- fail gracefully when offline
- document what is downloaded and where it is stored

## Option 3: Use system data

Sometimes the correct solution is to depend on a system library or dataset rather than bundling.

If you do, document requirements clearly.

## References

- CRAN policy (size, downloads, external resources): https://cran.r-project.org/web/packages/policies.html
