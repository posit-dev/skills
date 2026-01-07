# Divs and Spans

Divs and spans are Pandoc's fenced syntax for applying classes, IDs, and attributes to blocks and inline content.

## Fenced Divs

### Basic Syntax

````markdown
::: {.class-name}
Content inside the div.
:::
````

Three colons open, three colons close.

### Multiple Classes

````markdown
::: {.class1 .class2}
Content with multiple classes.
:::
````

### With ID

````markdown
::: {#my-id .my-class}
Content with ID and class.
:::
````

### With Attributes

````markdown
::: {.my-class key="value" data-info="something"}
Content with attributes.
:::
````

## Nested Divs

Use more colons for outer div:

````markdown
::: {.outer}
Outer content.

::: {.inner}
Inner content.
:::

More outer content.
:::
````

Or use different numbers:

````markdown
::: {.level1}
::: {.level2}
::: {.level3}
Deeply nested.
:::
:::
:::
````

## Spans

### Basic Syntax

````markdown
This is [styled text]{.highlight}.
````

### Multiple Classes

````markdown
[Important]{.bold .red}
````

### With ID

````markdown
[Target text]{#target-id}
````

### With Attributes

````markdown
[Text]{.class key="value"}
````

## Common Div Uses

### Custom Styling

````markdown
::: {.callout-box}
Important information here.
:::
````

With CSS:

```css
.callout-box {
  background: #f0f0f0;
  padding: 1em;
  border-left: 4px solid #007bff;
}
```

### Columns

````markdown
::: {.columns}

::: {.column width="50%"}
Left column.
:::

::: {.column width="50%"}
Right column.
:::

:::
````

### Centering

````markdown
::: {.center}
Centered content.
:::
````

### Hiding Content

````markdown
::: {.hidden}
This won't appear.
:::
````

## Raw Content Blocks

Insert format-specific content:

### HTML

````markdown
```{=html}
<div class="custom-html">
  <p>Raw HTML content.</p>
</div>
```
````

### LaTeX

````markdown
```{=latex}
\begin{center}
Raw LaTeX content.
\end{center}
```
````

### Typst

````markdown
```{=typst}
#align(center)[
  Raw Typst content.
]
```
````

### Inline Raw Content

`arkdown
Text with `<br>`{=html} line break.
````

## Layout Divs

### Tabsets

````markdown
::: {.panel-tabset}

## Tab 1

Tab 1 content.

## Tab 2

Tab 2 content.

:::
````

### Columns with Layout

````markdown
::: {layout-ncol=2}
![](image1.png)

![](image2.png)
:::
````

### Complex Layout

````markdown
::: {layout="[[1,1], [1]]"}
First cell.

Second cell.

Full-width cell.
:::
````

## Conditional Divs

### Format-Specific

````markdown
::: {.content-visible when-format="html"}
HTML-only content.
:::
````

### Hidden for Format

````markdown
::: {.content-hidden when-format="pdf"}
Hidden in PDF.
:::
````

## Special Divs

### Callouts

````markdown
::: {.callout-note}
Note content.
:::
````

### Cross-Referenceable

````markdown
::: {#fig-diagram}
![](diagram.png)

Figure caption.
:::
````

### Theorems

````markdown
::: {#thm-main}
Theorem statement.
:::
````

### Proof

````markdown
::: {.proof}
Proof content.
:::
````

## Span Uses

### Inline Styling

````markdown
This is [red text]{style="color: red;"}.
````

### Class Application

````markdown
The [key term]{.term} is defined as...
````

### Small Caps

````markdown
[Small Caps Text]{.smallcaps}
````

### Underline

````markdown
[Underlined text]{.underline}
````

### Keyboard Input

````markdown
Press [Ctrl]{.kbd}+[C]{.kbd} to copy.
````

## Custom CSS Classes

Define in CSS/SCSS:

```css
.important {
  color: red;
  font-weight: bold;
}

.code-highlight {
  background: #ffffcc;
  padding: 0.2em;
}

.margin-note {
  font-size: 0.9em;
  color: #666;
}
```

Use in document:

````markdown
This is [very important]{.important}.

The `function` takes [two arguments]{.code-highlight}.

[Additional context]{.margin-note}
````

## Attributes Reference

### Common Attributes

| Attribute | Description | Example             |
| --------- | ----------- | ------------------- |
| `.class`  | CSS class   | `.highlight`        |
| `#id`     | Element ID  | `#section-1`        |
| `style`   | Inline CSS  | `style="color:red"` |
| `width`   | Width       | `width="50%"`       |
| `height`  | Height      | `height="200px"`    |

### Data Attributes

````markdown
::: {data-value="42" data-type="number"}
Content with data attributes.
:::
````

Access in JavaScript:

```javascript
element.dataset.value; // "42"
element.dataset.type; // "number"
```

## Format-Specific Considerations

### HTML

Full CSS styling support. All classes and attributes render directly.

### PDF (LaTeX)

Limited styling. Some classes map to LaTeX commands:

- `.unnumbered` - Removes section numbering
- `.unlisted` - Excludes from TOC

### Word (DOCX)

Classes can map to Word styles via reference doc.

### RevealJS

Special classes:

- `.fragment` - Incremental reveal
- `.notes` - Speaker notes
- `.r-fit-text` - Auto-fit text

## Examples

### Styled Aside

````markdown
::: {.aside .note}
This is a side note with additional context.
:::
````

### Code with Caption

````markdown
::: {#lst-example}

```python
def hello():
    print("Hello")
```

Example Python function.
:::

````

### Multi-Column Layout

````markdown
::: {.columns}

::: {.column width="33%"}
### Column 1
First column content.
:::

::: {.column width="33%"}
### Column 2
Second column content.
:::

::: {.column width="33%"}
### Column 3
Third column content.
:::

:::
````

## Resources

- [Pandoc Divs and Spans](https://pandoc.org/MANUAL.html#divs-and-spans)
- [Quarto Markdown Basics](https://quarto.org/docs/authoring/markdown-basics.html)
