# Curating the reference index

The reference index is where pkgdown sites usually win or lose usability.

## Strategy

- Group topics the way users search (not the way files are organized).
- Put the “front door” functions first.
- Avoid dumping 100 exports into one undifferentiated list.

Practical workflow:

1. Decide your “front door” functions (what most users should start with).
2. Group the rest by job-to-be-done.
3. Hide or de-emphasize low-level helpers unless they are user-facing.

## `_pkgdown.yml` patterns

Use the `reference:` section to define groups and ordering.

Practical advice:

- Keep group titles short and user-facing.
- Explicitly list key functions in the order you want.
- Add a final “Internal helpers” group only if needed.

### Example

```yaml
reference:
	- title: "Getting started"
		contents:
			- foo
			- bar
	- title: "Main workflows"
		contents:
			- starts_with("build_")
			- starts_with("render_")
	- title: "Helpers"
		contents:
			- matches("_impl$")
```

Notes:

- `contents:` supports helpers like `starts_with()` and `matches()`.
- Prefer explicit ordering for the top-level functions so the reference page reads well.
