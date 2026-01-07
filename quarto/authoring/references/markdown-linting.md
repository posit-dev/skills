# Markdown Linting

Quarto documents should follow standard markdown linting rules for consistency and readability.
These guidelines are based on [markdownlint](https://github.com/markdownlint/markdownlint).

## Headers

### MD001: Header Levels Increment

Header levels should only increment by one level at a time.

````markdown
# Header 1

## Header 2

### Header 3
````

Not:

````markdown
# Header 1

### Header 3
````

### MD003: Header Style

Use ATX-style headers (`#`) consistently.

````markdown
# ATX Header

## Another Header
````

Not setext style:

````markdown
Setext Header
=============
````

### MD018: Space After Hash

Use exactly one space after the hash in headers.

````markdown
# Header
````

Not:

````markdown
#Header
#  Header
````

### MD022: Blank Lines Around Headers

Headers should be surrounded by blank lines.

````markdown
Some text.

## Header

More text.
````

### MD023: Headers at Line Start

Headers must start at the beginning of the line.

````markdown
## Header
````

Not:

````markdown
  ## Indented Header
````

### MD026: No Trailing Punctuation

Headers should not end with punctuation (except `?`).

````markdown
## What is Quarto?
````

Not:

````markdown
## Introduction.
## Summary:
````

## Lists

### MD004: Consistent List Markers

Use consistent unordered list markers throughout the document.

````markdown
- Item 1
- Item 2
- Item 3
````

Not:

````markdown
- Item 1
* Item 2
+ Item 3
````

### MD005: Consistent List Indentation

List items at the same level should have consistent indentation.

### MD006: Lists at Line Start

Top-level list items should start at the beginning of the line.

### MD007: List Indentation

Nested list items should use consistent indentation (2 spaces recommended for Quarto).

````markdown
- Parent item
  - Child item
    - Grandchild item
````

### MD030: Space After List Marker

Use exactly one space after list markers.

````markdown
- Item
1. Numbered item
````

### MD032: Blank Lines Around Lists

Lists should be surrounded by blank lines.

````markdown
Some text.

- Item 1
- Item 2

More text.
````

## Code Blocks

### MD031: Blank Lines Around Code Blocks

Fenced code blocks should be surrounded by blank lines.

````markdown
Some text.

```python
code_here()
```

More text.
````

### MD040: Code Block Language

Fenced code blocks should specify a language.

````markdown
```python
print("Hello")
```
````

Not:

````markdown
```
print("Hello")
```
````

For Quarto executable code blocks, use `{language}` syntax:

````markdown
```{python}
print("Hello")
```
````

### MD046: Code Block Style

Use fenced code blocks consistently, not indented code blocks.

## Whitespace

### MD009: Trailing Spaces

Lines should not have trailing spaces (except for intentional line breaks).

### MD010: No Hard Tabs

Use spaces instead of hard tabs for indentation.

### MD012: No Multiple Blank Lines

Do not use multiple consecutive blank lines.

````markdown
Some text.

More text.
````

Not:

````markdown
Some text.



More text.
````

### MD047: Single Newline at End

Files should end with a single newline character.

## Links and Images

### MD011: Correct Link Syntax

Use correct link syntax (not reversed).

````markdown
[text](url)
````

Not:

````markdown
(url)[text]
````

### MD034: No Bare URLs

Use proper link syntax instead of bare URLs in text.

````markdown
Visit [Quarto](https://quarto.org) for more information.
````

Not:

````markdown
Visit https://quarto.org for more information.
````

### MD039: No Spaces in Link Text

Do not use spaces inside link text brackets.

````markdown
[link text](url)
````

Not:

````markdown
[ link text ](url)
````

### MD042: No Empty Links

Links should have a valid destination.

### MD045: Image Alt Text

Images should have alternate text for accessibility.

````markdown
![Description of image](image.png)
````

Not:

````markdown
![](image.png)
````

## Emphasis and Formatting

### MD037: No Spaces in Emphasis

Do not use spaces inside emphasis markers.

````markdown
**bold text**
*italic text*
````

Not:

````markdown
** bold text **
* italic text *
````

### MD038: No Spaces in Code Spans

Do not use spaces inside inline code spans.

````markdown
Use `code` here.
````

Not:

````markdown
Use ` code ` here.
````

### MD049: Consistent Emphasis Style

Use consistent emphasis style (asterisks or underscores).

````markdown
*italic* and **bold**
````

## Quarto-Specific Allowances

Some rules have Quarto-specific considerations:

### Inline HTML (MD033)

Quarto allows certain HTML for:

- Shortcodes: `{{< shortcode >}}`
- Raw HTML blocks: `{=html}`
- Special formatting not available in markdown

### Line Length (MD013)

Line length limits are typically not enforced in Quarto documents, as prose paragraphs may be long.

### Ignored Rules

The following rules are typically disabled for Quarto:

| Rule  | Reason                                          |
| ----- | ----------------------------------------------- |
| MD024 | Repeated headers are common in structured docs. |
| MD025 | Quarto docs may have multiple H1 headers.       |
| MD041 | Quarto uses YAML front matter, not H1 first.     |

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

## Quarto Div Syntax

When using Quarto fenced divs, ensure proper formatting:

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
- Opening div uses `:::` (three colons) when nesting.
- Closing div uses `:::` (three colons).

## Resources

- [markdownlint Rules](https://github.com/markdownlint/markdownlint/blob/main/docs/RULES.md)
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
- [Quarto Markdown Basics](https://quarto.org/docs/authoring/markdown-basics.html)
