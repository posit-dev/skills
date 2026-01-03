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

### Sequence Diagrams

````markdown
```{mermaid}
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob
    B-->>A: Hi Alice
    A->>B: How are you?
    B-->>A: Great!
```
````

### Class Diagrams

````markdown
```{mermaid}
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Duck : +String beakColor
    Duck : +swim()
    Duck : +quack()
```
````

### State Diagrams

````markdown
```{mermaid}
stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```
````

### Entity Relationship

````markdown
```{mermaid}
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER {
        string name
        string email
    }
    ORDER {
        int orderNumber
        date created
    }
```
````

### Gantt Charts

````markdown
```{mermaid}
gantt
    title Project Schedule
    dateFormat  YYYY-MM-DD
    section Phase 1
    Task 1      :a1, 2024-01-01, 30d
    Task 2      :after a1, 20d
    section Phase 2
    Task 3      :2024-02-15, 25d
```
````

### Pie Charts

````markdown
```{mermaid}
pie title Distribution
    "Category A" : 40
    "Category B" : 30
    "Category C" : 30
```
````

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

### Directed Graph

````markdown
```{dot}
digraph {
  rankdir=LR;
  node [shape=box];

  Start -> Process1;
  Start -> Process2;
  Process1 -> End;
  Process2 -> End;
}
```
````

### Undirected Graph

````markdown
```{dot}
graph {
  A -- B -- C;
  B -- D;
}
```
````

### Styled Nodes

````markdown
```{dot}
digraph {
  node [shape=ellipse, style=filled, fillcolor=lightblue];

  A [label="Start", shape=circle, fillcolor=green];
  B [label="Process"];
  C [label="End", shape=doublecircle, fillcolor=red];

  A -> B -> C;
}
```
````

### Subgraphs

````markdown
```{dot}
digraph {
  subgraph cluster_0 {
    label = "Cluster 1";
    A -> B;
  }
  subgraph cluster_1 {
    label = "Cluster 2";
    C -> D;
  }
  B -> C;
}
```
````

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

### Fixed Size

````markdown
```{mermaid}
%%| fig-width: 8
%%| fig-height: 5

flowchart LR
  A --> B
```
````

### Responsive (HTML)

By default, diagrams are responsive in HTML. Disable with:

````markdown
```{mermaid}
%%| fig-responsive: false

flowchart LR
  A --> B
```
````

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

### With Title and Label

````markdown
```{mermaid}
%%| label: fig-themed
%%| fig-cap: "Themed diagram."

---
title: My Diagram
config:
  theme: neutral
---

flowchart TD
  A --> B --> C
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
