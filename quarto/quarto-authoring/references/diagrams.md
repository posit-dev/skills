# Diagrams

Quarto natively supports Mermaid and Graphviz diagrams, rendering them automatically across output formats.

## Mermaid Diagrams

Mermaid is a JavaScript-based diagramming tool using text definitions.

### Basic Syntax

````markdown
```{mermaid}
flowchart LR
  A[Start] --> B[Process]
  B --> C[End]
```
````

### Flowcharts

````markdown
```{mermaid}
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```
````

Direction options: `TB` (top-bottom), `TD` (top-down), `BT`, `RL`, `LR`.

All standard Mermaid diagram types are supported: `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, `gantt`, `pie`, etc. Use standard Mermaid syntax inside `{mermaid}` code cells.

## Mermaid Cell Options

Use `%%|` for options:

````markdown
```{mermaid}
%%| label: fig-flowchart
%%| fig-cap: "Process flowchart."

flowchart LR
  A --> B --> C
```
````

### Common Options

| Option           | Description        | Example         |
| ---------------- | ------------------ | --------------- |
| `label`          | Cross-reference ID | `fig-diagram`   |
| `fig-cap`        | Caption            | `"My diagram."` |
| `fig-width`      | Width              | `6` (inches)    |
| `fig-height`     | Height             | `4` (inches)    |
| `fig-responsive` | Responsive sizing  | `true`, `false` |

### External File

````markdown
```{mermaid}
%%| file: diagram.mmd
```
````

## Graphviz/DOT Diagrams

Graphviz uses DOT language for graph descriptions.

### Basic Syntax

````markdown
```{dot}
digraph G {
  A -> B -> C;
  B -> D;
}
```
````

Use `digraph` for directed graphs, `graph` for undirected. Standard DOT features (subgraphs, node styling, rank direction) all work.

## Graphviz Cell Options

Use `//|` for options:

````markdown
```{dot}
//| label: fig-graph
//| fig-cap: "Network diagram."

digraph {
  A -> B -> C;
}
```
````

### External File

````markdown
```{dot}
//| file: network.dot
```
````

## Cross-Referencing Diagrams

Both Mermaid and Graphviz diagrams can be cross-referenced:

````markdown
```{mermaid}
%%| label: fig-process
%%| fig-cap: "The data processing workflow."

flowchart LR
  Input --> Process --> Output
```

See @fig-process for the workflow.
````

## Sizing

Use `%%| fig-width` and `%%| fig-height` cell options. Diagrams are responsive by default in HTML; disable with `%%| fig-responsive: false`.

## Theming

### Mermaid Themes

Configure Mermaid theming using a YAML block inside the code cell:

````markdown
```{mermaid}
---
config:
  theme: forest
---

flowchart LR
  A --> B
```
````

Available themes: `default`, `forest`, `dark`, `neutral`, `base`.

### Custom Theme Variables

````markdown
```{mermaid}
---
config:
  theme: base
  themeVariables:
    primaryColor: "#f0f0f0"
    primaryBorderColor: "#333"
    fontFamily: "Fira Code, monospace"
---

flowchart LR
  A --> B
```
````

### Theming and Render Format

When using `mermaid-format: js` (the default for HTML), Quarto controls theming and may override custom theme configurations.
The YAML config block inside the Mermaid cell might appear to have no effect.

To ensure custom theming works:

1. Use native Quarto theming options in document YAML.
2. Change to `mermaid-format: svg` or `mermaid-format: png`.

```yaml
format:
  html:
    mermaid:
      theme: forest
```

Or use a different render format:

```yaml
format:
  html:
    mermaid-format: svg
```

With `svg` or `png` format, the YAML config block inside Mermaid cells will be respected.

### CSS Customization

For additional styling in HTML:

```css
:root {
  --mermaid-font-family: "Fira Code", monospace;
}
```

### Graphviz Styling

Use DOT attributes:

````markdown
```{dot}
digraph {
  bgcolor="transparent";
  node [fontname="Helvetica", fontsize=12];
  edge [color=gray];

  A -> B;
}
```
````

## Rendering

### HTML Output

Diagrams rendered with JavaScript (Mermaid) or as SVG (Graphviz).

### PDF/DOCX Output

Rendered as images using Chrome/Chromium.

Requires Chrome or Edge installed, or set:

```yaml
mermaid:
  puppeteer:
    executablePath: /path/to/chrome
```

## Diagram in Figures

Combine with figure elements:

````markdown
::: {#fig-workflow}

```{mermaid}
flowchart TD
  A --> B --> C
```

Complete workflow diagram.
:::

````

## Tips

### Complex Diagrams

For complex diagrams, use external files:

````markdown
```{mermaid}
%%| file: complex-diagram.mmd
%%| fig-cap: "Complex system architecture."
```

````

### Accessibility

Add alt text:

````markdown
```{mermaid}
%%| fig-alt: "Flowchart showing three sequential steps."

flowchart LR
  A --> B --> C
```
````

## Resources

- [Quarto Diagrams](https://quarto.org/docs/authoring/diagrams.html)
- [Mermaid Documentation](https://mermaid.js.org/)
- [Graphviz Documentation](https://graphviz.org/documentation/)
- [DOT Language](https://graphviz.org/doc/info/lang.html)

