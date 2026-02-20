# Conditional Content

Quarto allows content to be shown or hidden based on output format, metadata, or profiles.

## Format-Based Conditions

### Content Visible

Show content only for specific formats:

````markdown
::: {.content-visible when-format="html"}
This only appears in HTML output.
:::
````

### Content Hidden

Hide content for specific formats:

````markdown
::: {.content-hidden when-format="pdf"}
This appears everywhere except PDF.
:::
````

### Unless Format

Show unless a specific format:

````markdown
::: {.content-visible unless-format="html"}
This appears in PDF, DOCX, etc., but not HTML.
:::
````

## Format Values

### Single Formats

| Format          | Value      |
| --------------- | ---------- |
| HTML            | `html`     |
| PDF             | `pdf`      |
| Word            | `docx`     |
| LaTeX           | `latex`    |
| RevealJS        | `revealjs` |
| Beamer          | `beamer`   |
| EPUB            | `epub`     |
| GitHub Markdown | `gfm`      |

### Format Aliases

Quarto groups related formats:

| Alias     | Includes                             |
| --------- | ------------------------------------ |
| `html`    | HTML, EPUB, RevealJS, Dashboard      |
| `pdf`     | PDF, LaTeX, Beamer                   |
| `html:js` | HTML formats with JavaScript support |

### Example with Aliases

````markdown
::: {.content-visible when-format="pdf"}
This appears in PDF, LaTeX, and Beamer.
:::
````

## Multiple Formats

### Either Format

````markdown
::: {.content-visible when-format="html"}
::: {.content-visible when-format="revealjs"}
This appears in HTML or RevealJS.
:::
:::
````

Or use aliases:

````markdown
::: {.content-visible when-format="html"}
Appears in all HTML-based formats.
:::
````

## Inline Conditions

For inline content, use spans:

````markdown
View the [interactive version]{.content-visible when-format="html"}
[figure]{.content-visible when-format="pdf"}.
````

## Metadata-Based Conditions

### When Meta

Show based on metadata values:

````markdown
::: {.content-visible when-meta="draft"}
DRAFT - Not for distribution.
:::
````

With YAML:

```yaml
draft: true
```

### Unless Meta

````markdown
::: {.content-visible unless-meta="draft"}
Final version content.
:::
````

### Nested Metadata

````markdown
::: {.content-visible when-meta="params.show-advanced"}
Advanced content here.
:::
````

YAML:

```yaml
params:
  show-advanced: true
```

## Profile-Based Conditions

### Define Profiles

In `_quarto.yml`:

```yaml
profile:
  default: production

  group:
    - [development, production]
```

### Profile-Specific Content

````markdown
::: {.content-visible when-profile="development"}
Debug information here.
:::

::: {.content-visible when-profile="production"}
Production content only.
:::
````

### Using Profiles

```bash
quarto render --profile development
```

## Conditional Code Blocks

### Format-Specific Code

````markdown
::: {.content-visible when-format="html"}

```{r}
# Interactive plot for HTML
plotly::plot_ly(data)
```

:::

::: {.content-visible when-format="pdf"}

```{r}
# Static plot for PDF
plot(data)
```

:::
````

### With QUARTO_EXECUTE_INFO

Quarto creates a JSON file with execution context information. Read it to conditionally execute code in any language.

#### R

````markdown
```{r}
quarto_info <- jsonlite::read_json(
  Sys.getenv("QUARTO_EXECUTE_INFO")
)
if (quarto_info$output$format == "html") {
  interactive_plot()
}
```
````

#### Python

````markdown
```{python}
import os
import json

with open(os.environ["QUARTO_EXECUTE_INFO"]) as f:
    quarto_info = json.load(f)

if quarto_info["output"]["format"] == "html":
    interactive_plot()
```
````

See [QUARTO_EXECUTE_INFO](https://quarto.org/docs/advanced/quarto-execute-info.html) for available fields.

## Conditional Includes

Include different files based on format:

````markdown
::: {.content-visible when-format="html"}

{{< include _interactive-content.qmd >}}

:::

::: {.content-visible when-format="pdf"}

{{< include _static-content.qmd >}}

:::
````

## Conditional YAML

Use conditional logic in YAML:

```yaml
format:
  html:
    include-in-header:
      - text: |
          <script src="interactive.js"></script>
  pdf:
    include-in-header:
      - text: |
          \usepackage{custom}
```

## Complex Conditions

### Combining Conditions

````markdown
::: {.content-visible when-format="html" when-meta="interactive"}
Interactive HTML content.
:::
````

Both conditions must be true.

### Nested Conditions

````markdown
::: {.content-visible when-format="html"}

::: {.content-visible when-meta="advanced"}
Advanced HTML content.
:::

Basic HTML content.

:::
````

## Resources

- [Quarto Conditional Content](https://quarto.org/docs/authoring/conditional.html)
- [Project Profiles](https://quarto.org/docs/projects/profiles.html)


