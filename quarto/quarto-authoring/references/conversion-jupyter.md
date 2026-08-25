# Jupyter Notebook (.ipynb) and Quarto (.qmd) Interoperability

## Direct Rendering

Quarto renders `.ipynb` files without conversion:

```bash
quarto render notebook.ipynb
quarto render notebook.ipynb --to pdf
```

Cell outputs stored in the notebook are used by default.
Set `execute: enabled: true` in YAML front matter to force re-execution.

## Converting Between Formats

`quarto convert` works in both directions:

```bash
quarto convert notebook.ipynb   # → notebook.qmd
quarto convert notebook.qmd     # → notebook.ipynb
```

Converting `.ipynb` → `.qmd` extracts cell source into code blocks, converts markdown cells to prose, and discards stored outputs (Quarto re-executes on next render).

Converting `.qmd` → `.ipynb` produces a notebook matching the `.qmd` structure, without executing cells.

## When to Use Each Format

Prefer `.qmd` for version-controlled documents: plain text produces clean diffs, cell options use hashpipe syntax (`#|`) instead of JSON metadata, and any text editor can be used.

Prefer `.ipynb` for interactive exploration, sharing with users who do not use Quarto, or workflows that rely heavily on Jupyter widgets.

## Resources

- [Quarto convert CLI](https://quarto.org/docs/tools/jupyter-lab.html)
- [Jupyter Kernel Execution](https://quarto.org/docs/computations/jupyter.html)
