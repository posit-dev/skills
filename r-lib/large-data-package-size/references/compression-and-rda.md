# Compression and `.rda` discipline

Internal datasets (`data/*.rda`) are convenient, but you still need to keep them lean.

## Practical rules

- Don’t ship raw data dumps.
- Reduce to the smallest representation that supports your examples and use cases.
- Prefer stable column types and avoid duplication.

## Diagnostics

- Compare object sizes (`lobstr::obj_size()` or `utils::object.size()`).
- Re-check after changes; data can balloon silently.

## When `.rda` is the wrong choice

- The dataset is huge.
- The dataset changes frequently.
- The dataset is better treated as an external resource.

Then prefer an external strategy.

## Related

- [external-data-strategies.md](external-data-strategies.md)
