# Markdown Linting

Quarto documents should follow standard [markdownlint](https://github.com/markdownlint/markdownlint) rules. This file covers only Quarto-specific allowances and configuration — refer to the markdownlint docs for general rules.

## Quarto-Specific Allowances

### Line Length (MD013)

Typically disabled for Quarto — prose paragraphs may be long and YAML/code lines can exceed limits.

### Duplicate Headings (MD024)

Repeated headers are common in structured Quarto documents (e.g., repeated "Example" sections).

### Multiple H1 (MD025)

Quarto documents may have multiple H1 headers, especially in books and multi-part documents.

### Inline HTML (MD033)

Quarto uses HTML in specific contexts:

- Shortcodes: `{{< shortcode >}}`
- Raw HTML blocks: `` ```{=html} ``
- Elements like `<div>`, `<span>`, `<iframe>` for advanced layouts

### First Line H1 (MD041)

Quarto uses YAML front matter before the first heading, so MD041 should be disabled.

## Configuration

### Example `.markdownlint.yaml`

```yaml
default: true

MD013: false
MD024: false
MD025: false
MD033:
  allowed_elements:
    - div
    - span
    - iframe
MD041: false
```

### Example `.markdownlint-cli2.yaml`

```yaml
config:
  default: true
  MD013: false
  MD024: false
  MD025: false
  MD041: false

globs:
  - "**/*.md"
  - "**/*.qmd"
```

## Quarto Div Formatting

When using fenced divs, ensure proper blank-line spacing:

````markdown
Some text.

::: {.callout-note}
Note content here.
:::

More text.
````

Key points:

- Blank line before opening `:::`.
- Blank line after closing `:::`.
- Use `::::` (four+ colons) for nesting outer divs.

## Resources

- [markdownlint Rules](https://github.com/markdownlint/markdownlint/blob/main/docs/RULES.md)
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
- [Quarto Markdown Basics](https://quarto.org/docs/authoring/markdown-basics.html)
