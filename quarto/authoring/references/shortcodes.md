# Shortcodes

Shortcodes are special commands that expand into content at render time. Quarto provides several built-in shortcodes.

## Syntax

Shortcodes use double curly braces with angle brackets:

````markdown
{{< shortcode-name argument >}}
````

Or with named parameters:

````markdown
{{< shortcode-name param="value" >}}
````

## Video

Embed videos from various sources:

### YouTube

````markdown
{{< video https://www.youtube.com/embed/VIDEO_ID >}}
````

Or with just the ID:

````markdown
{{< video https://youtu.be/VIDEO_ID >}}
````

### Vimeo

````markdown
{{< video https://vimeo.com/VIDEO_ID >}}
````

### Local Video

````markdown
{{< video video.mp4 >}}
````

### Video Options

````markdown
{{< video https://youtu.be/VIDEO_ID
title="Video Title"
start="30"
aspect-ratio="16x9"
width="100%"

> }}
````

Options:

- `title` - Video title
- `start` - Start time in seconds
- `width` / `height` - Dimensions
- `aspect-ratio` - `16x9`, `4x3`, `1x1`, `21x9`

## Include

Include content from other files:

### Basic Include

````markdown
{{< include _content.qmd >}}
````

### Include Section

Include only part of a file:

````markdown
{{< include _content.qmd#section-id >}}
````

### Include with Path

````markdown
{{< include path/to/file.qmd >}}
````

### Usage Notes

- Included files are processed as Quarto markdown
- Use `_` prefix for files to exclude from rendering
- Paths are relative to the including document

## Embed

Embed output from Jupyter notebooks:

### Embed Cell Output

````markdown
{{< embed notebook.ipynb#cell-id >}}
````

### Embed with Options

````markdown
{{< embed notebook.ipynb#fig-plot echo=true >}}
````

Options:

- `echo` - Show source code (`true`/`false`)

### Finding Cell IDs

Cell IDs are set in notebook metadata or automatically generated.

## Meta

Access document metadata:

````markdown
The title is: {{< meta title >}}
Author: {{< meta author >}}
````

### Nested Metadata

````markdown
{{< meta format.html.theme >}}
````

### In Code Blocks

Works in code blocks too:

````markdown
```yaml
title: { { < meta title > } }
```
````

## Var

Access variables from `_variables.yml`:

### Define Variables

Create `_variables.yml`:

```yaml
version: 2.0.0
company: Acme Corp
```

### Use Variables

````markdown
Current version: {{< var version >}}
Published by {{< var company >}}.
````

### Nested Variables

```yaml
contact:
  email: info@example.com
  phone: 555-1234
```

````markdown
Email: {{< var contact.email >}}
````

## Env

Access environment variables:

````markdown
Home directory: {{< env HOME >}}
User: {{< env USER >}}
````

### Default Value

````markdown
{{< env MY_VAR default="not set" >}}
````

## Pagebreak

Insert a page break:

````markdown
Content before.

{{< pagebreak >}}

Content after (on new page in PDF).
````

Works across formats (PDF, Word, HTML print).

## Kbd

Describe keyboard shortcuts:

````markdown
Press {{< kbd Ctrl+C >}} to copy.
Save with {{< kbd Cmd+S >}} on Mac.
````

### Multiple Keys

````markdown
{{< kbd Ctrl+Shift+P >}}
{{< kbd Cmd-Option-Esc >}}
````

## Lipsum

Generate placeholder text:

````markdown
{{< lipsum 1 >}}
````

Generates one paragraph of Lorem Ipsum.

### Multiple Paragraphs

````markdown
{{< lipsum 3 >}}
````

## Placeholder

Generate placeholder images:

````markdown
{{< placeholder 400 300 >}}
````

Creates a 400x300 placeholder image.

### With Format

````markdown
{{< placeholder 400 300 format=svg >}}
````

## Version

Show Quarto version:

````markdown
Built with Quarto {{< version >}}.
````

## Contents

Rearrange document content:

````markdown
{{< contents heading >}}
````

Shows content under a specific heading. Useful for reorganizing included content.

## Conditional Shortcodes

Shortcodes can be format-specific:

````markdown
::: {.content-visible when-format="html"}
{{< video video.mp4 >}}
:::

::: {.content-visible when-format="pdf"}
See video at: https://example.com/video
:::
````

## Custom Shortcodes

Create custom shortcodes via extensions. Example extension structure:

```txt
_extensions/
└── my-shortcode/
    ├── _extension.yml
    └── my-shortcode.lua
```

## Shortcodes in Code

Shortcodes work in inline code and code blocks:

````markdown
`{{< meta title >}}`
````

```yaml
version: {{< var version >}}
```

## Escaping Shortcodes

To show shortcode syntax without executing:

````markdown
{{{< shortcode >}}}`
````

Or use raw block:

````markdown
```{.markdown shortcodes=false}
{{< shortcode >}}
```
````

## Examples

### Documentation Site

````markdown
# {{< meta title >}} v{{< var version >}}

{{< include _installation.qmd >}}

## Video Tutorial

{{< video https://youtu.be/TUTORIAL_ID >}}

## Keyboard Shortcuts

- Copy: {{< kbd Ctrl+C >}}
- Paste: {{< kbd Ctrl+V >}}

{{< pagebreak >}}

## Appendix

{{< include _appendix.qmd >}}
````

### Project Variables

`_variables.yml`:

```yaml
product:
  name: "MyApp"
  version: "2.1.0"
  year: 2024
```

Document:

````markdown
# {{< var product.name >}}

Version {{< var product.version >}} - Copyright {{< var product.year >}}
````

## Resources

- [Quarto Shortcodes](https://quarto.org/docs/extensions/shortcodes.html)
- [Video Embedding](https://quarto.org/docs/authoring/videos.html)
- [Includes](https://quarto.org/docs/authoring/includes.html)
