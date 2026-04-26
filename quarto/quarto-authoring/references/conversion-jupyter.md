# Jupyter Notebook (.ipynb) and Quarto (.qmd) Interoperability

Quarto can render `.ipynb` files directly and convert between `.ipynb` and `.qmd` in both directions.

## Direct Rendering (No Conversion Required)

Quarto renders `.ipynb` files as-is:

```bash
quarto render notebook.ipynb
quarto render notebook.ipynb --to pdf
```

Cell outputs stored in the notebook are used by default; set `execute: enabled: true` to force re-execution.

## Converting Between Formats

`quarto convert` works in both directions:

```bash
quarto convert notebook.ipynb   # → notebook.qmd
quarto convert notebook.qmd     # → notebook.ipynb
```

Converting `.ipynb` → `.qmd`: extracts cell source into code blocks, converts markdown cells to prose, and discards stored outputs (Quarto re-executes on next render).

Converting `.qmd` → `.ipynb`: produces a notebook with cells matching the `.qmd` structure, without executing them.

## Key Differences: .ipynb vs .qmd

| Feature         | .ipynb                 | .qmd                      |
| --------------- | ---------------------- | ------------------------- |
| Cell options    | Cell metadata JSON     | Hashpipe comments (`#\|`) |
| Version control | JSON (noisy diffs)     | Plain text (clean diffs)  |
| Edit experience | Jupyter UI             | Any text editor           |
| Inline outputs  | Stored in file         | Re-computed on render     |

## Cell Option Migration

Jupyter cell metadata becomes hashpipe options in `.qmd`.

**Before (.ipynb cell metadata):**

```json
{
  "tags": ["remove-input"]
}
```

**After (.qmd):**

```
#| echo: false
```

### Common Metadata Mappings

Quarto options use the `#|` prefix in code cells.

| Jupyter / nbconvert tag         | Quarto option      |
| ------------------------------- | ------------------ |
| `remove-input` / `hide-input`   | `echo: false`      |
| `remove-output` / `hide-output` | `output: false`    |
| `remove-cell`                   | `include: false`   |
| `raises-exception`              | `error: true`      |

## YAML Front Matter

`.qmd` files use YAML front matter; `.ipynb` files use notebook-level metadata JSON.
After converting `.ipynb` → `.qmd`, add YAML at the top:

```yaml
---
title: "My Analysis"
author: "Jane Doe"
date: today
format: html
execute:
  echo: true
  warning: false
jupyter: python3
---
```

For engine and kernel selection, see [engines.md](engines.md).

## Controlling Re-Execution

For `.ipynb` files, Quarto uses stored cell outputs by default.
For `.qmd` files, Quarto re-executes all cells on every render.

To use stored outputs when rendering a `.qmd` (e.g. after `quarto convert`):

```yaml
execute:
  enabled: false
```

To force re-execution of a `.ipynb`:

```yaml
execute:
  enabled: true
```

For project-level caching and freeze, see [engines.md](engines.md).

## When to Use Each Format

Prefer `.qmd` when:

- The document is under version control (clean diffs, no output blobs).
- You want hashpipe options instead of JSON cell metadata.
- You are working in any editor, not just Jupyter UI.

Prefer `.ipynb` when:

- The notebook is primarily interactive exploration.
- It is shared with users who do not use Quarto.
- It relies heavily on Jupyter widgets.

## Resources

- [Jupyter Kernel Execution](https://quarto.org/docs/advanced/jupyter/kernel-execution.html)
- [Quarto convert CLI](https://quarto.org/docs/cli/convert.html)
