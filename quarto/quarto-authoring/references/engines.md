# Compute Engines

Quarto separates the authoring layer (YAML front matter, hashpipe options, cross-references, layouts) from the compute engine that executes code cells.
All cell options, figure/table options, and cross-reference syntax are identical across engines.

## Engine Overview

| Engine    | Activated by                          | Primary language(s) | Notes                                               |
| --------- | ------------------------------------- | ------------------- | --------------------------------------------------- |
| `knitr`   | `{r}` cells                           | R                   | Default when R cells are present                    |
| `julia`   | `{julia}` cells                       | Julia               | Default when Julia cells are present (Quarto 1.9+)  |
| `jupyter` | `{python}` or any Jupyter kernel cell | Python, others      | Default for Python and other non-R, non-Julia cells |

Since Quarto 1.9, engine extensions allow third-party engines to register additional language identifiers.
The `{LANGUAGE}` cell surface and all hashpipe options remain the same regardless of the engine.

## Auto-Detection

Quarto picks the engine automatically from the first executable cell in the document:

- First `{r}` cell → knitr engine.
- First `{julia}` cell → julia engine (Quarto 1.9+).
- First `{python}` or other non-R, non-Julia cell → jupyter engine.

## Selecting an Engine Explicitly

Override auto-detection in YAML front matter:

```yaml
engine: knitr
```

```yaml
engine: jupyter
jupyter: python3 # kernel name (default: python3)
```

```yaml
engine: julia
```

The `jupyter` key accepts any installed kernel name:

```yaml
engine: jupyter
jupyter: ir        # R via IRkernel
jupyter: myenv     # named conda/venv kernel
jupyter: julia-1.10
```

List available kernels with:

```bash
jupyter kernelspec list
```

## Hashpipe Comment Prefix

The hashpipe comment prefix depends on the cell type:

- R, Python, Julia: `#|`
- Mermaid: `%%|`
- Graphviz/DOT: `//|`

## Engine-Specific Behaviour

### Table Output

**knitr engine**: Values returned from a cell that are recognised as table objects (e.g. data frames, matrices) are automatically rendered as markdown tables.

**jupyter engine**: Cells returning a display-protocol object auto-display as HTML in HTML output only.
For portable output across all formats, print a markdown string and use `output: asis`:

````markdown
```{language}
#| tbl-cap: "Summary statistics."
#| output: asis

# print markdown table string to stdout
```
````

### Inline Code

Inline code syntax differs by engine:

| Engine  | Inline syntax                                             |
| ------- | --------------------------------------------------------- |
| knitr   | `` `r expr` ``                                            |
| jupyter | Not supported natively in `.qmd`; use cell output instead |
| julia   | Not supported natively in `.qmd`; use cell output instead |

### Caching

Both knitr and jupyter engines support cell-level caching with `cache: true`.
For project-level freeze (skip re-execution when source is unchanged):

```yaml
execute:
  freeze: auto
```

## Engine Extensions (Quarto 1.9+)

Third-party extensions can register custom engines via the Quarto extension system.
Custom engines use the same `{LANGUAGE}` cell syntax and the same `#|` hashpipe options as built-in engines.
Install engine extensions with:

```bash
quarto add <extension>
```

Then activate in YAML:

```yaml
engine: <extension-engine-name>
```

## Resources

- [Using R](https://quarto.org/docs/computations/r.html)
- [Using Python](https://quarto.org/docs/computations/python.html)
- [Using Julia](https://quarto.org/docs/computations/julia.html)
- [Execution Options](https://quarto.org/docs/computations/execution-options.html)
- [Engine Extensions](https://quarto.org/docs/extensions/engine.html)
