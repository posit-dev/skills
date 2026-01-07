# Converting distill to Quarto

Guide for converting distill articles and blogs to Quarto format.

## Overview

Key differences:

1. Format: `distill_article` → `html`
2. Configuration: R YAML → Quarto YAML
3. Asides: `<aside>` → `::: {.column-margin}`
4. Appendices: Heading-based

## Quick Start

### 1. Rename File

```bash
mv article.Rmd article.qmd
```

### 2. Update YAML

#### distill

```yaml
title: "My Article"
author:
  - name: "Jane Doe"
    affiliation: University
output: distill::distill_article
```

#### Quarto

```yaml
title: "My Article"
author:
  - name: "Jane Doe"
    affiliations:
      - University
format: html
```

## YAML Conversion

### Basic Article

#### distill

```yaml
title: "Research Article"
description: "A brief description"
author:
  - name: "Jane Doe"
    url: https://example.com
    affiliation: University Name
    affiliation_url: https://university.edu
    orcid_id: 0000-0000-0000-0000
date: "2024-01-15"
output:
  distill::distill_article:
    toc: true
    toc_depth: 3
```

#### Quarto

```yaml
title: "Research Article"
description: "A brief description"
author:
  - name: "Jane Doe"
    url: https://example.com
    affiliations:
      - name: University Name
        url: https://university.edu
    orcid: 0000-0000-0000-0000
date: 2024-01-15
format:
  html:
    toc: true
    toc-depth: 3
```

### Author Metadata

#### distill

```yaml
author:
  - name: "First Author"
    affiliation: Institution A
    affiliation_url: https://a.edu
  - name: "Second Author"
    affiliation: Institution B
```

#### Quarto

```yaml
author:
  - name: "First Author"
    affiliations:
      - name: Institution A
        url: https://a.edu
  - name: "Second Author"
    affiliations:
      - Institution B
```

### Citation Metadata

#### distill

```yaml
citation_url: https://example.com/article
bibliography: references.bib
```

#### Quarto

```yaml
citation:
  url: https://example.com/article
bibliography: references.bib
```

## Aside Content

### distill

```html
<aside>This content appears in the margin.</aside>
```

Or with R Markdown:

````markdown
::: {.l-body-outset}
Wide content here.
:::
````

### Quarto

````markdown
::: {.column-margin}
This content appears in the margin.
:::
````

Or inline:

````markdown
Main text here.
[This appears in the margin.]{.aside}
````

## Layout Classes

### distill

````markdown
::: {.l-body}
Default body width.
:::

::: {.l-body-outset}
Slightly wider than body.
:::

::: {.l-page}
Page width.
:::

::: {.l-screen}
Full screen width.
:::

::: {.l-screen-inset}
Screen width with padding.
:::
````

### Quarto

````markdown
::: {.column-body}
Default body width.
:::

::: {.column-body-outset}
Slightly wider than body.
:::

::: {.column-page}
Page width.
:::

::: {.column-screen}
Full screen width.
:::

::: {.column-screen-inset}
Screen width with padding.
:::
````

### Layout Mapping

| distill           | Quarto                 |
| ----------------- | ---------------------- |
| `.l-body`         | `.column-body`         |
| `.l-body-outset`  | `.column-body-outset`  |
| `.l-page`         | `.column-page`         |
| `.l-page-outset`  | `.column-page-outset`  |
| `.l-screen`       | `.column-screen`       |
| `.l-screen-inset` | `.column-screen-inset` |
| `.l-gutter`       | `.column-margin`       |

## Figures

### distill

````markdown
```{r, layout="l-body-outset", fig.cap="Caption"}
plot(1:10)
```
````

### Quarto

````markdown
```{r}
#| column: body-outset
#| fig-cap: "Caption"

plot(1:10)
```
````

## Appendices

### distill

````markdown
## Appendix

### Acknowledgments

Thanks to...

### Author Contributions

Author A did...
````

### Quarto

````markdown
## Acknowledgments {.appendix}

Thanks to...

## Author Contributions {.appendix}

Author A did...
````

Or use an appendix section:

````markdown
::: {#appendix}

## Additional Details

More content here.
:::
````

## Code Display

### distill

```yaml
output:
  distill::distill_article:
    code_folding: true
```

### Quarto

```yaml
format:
  html:
    code-fold: true
    code-tools: true
```

## Blog Migration

### distill Blog Structure

```txt
_site.yml
_posts/
  2024-01-01-first-post/
    first-post.Rmd
  2024-01-15-second-post/
    second-post.Rmd
```

### Quarto Blog Structure

```txt
_quarto.yml
posts/
  first-post/
    index.qmd
  second-post/
    index.qmd
```

### Site Configuration

#### Distill (`_site.yml`)

```yaml
name: "My Blog"
title: "My Blog"
navbar:
  right:
    - text: "About"
      href: about.html
```

#### Quarto (`_quarto.yml`)

```yaml
project:
  type: website

website:
  title: "My Blog"
  navbar:
    right:
      - text: "About"
        href: about.qmd

format:
  html:
    theme: cosmo
```

### Blog Listing

- `_quarto.yml`

  ```yaml
  website:
    title: "My Blog"
  ```

- `index.qmd`

  ````markdown
  ---
  title: "My Blog"
  listing:
    contents: posts
    type: default
    sort: "date desc"
  ---
  ````

## Post Front Matter

### distill

```yaml
title: "Post Title"
description: "Brief description"
author:
  - name: "Author Name"
date: 2024-01-15
categories:
  - R
  - Data Science
preview: preview.png
output:
  distill::distill_article:
    self_contained: false
```

### Quarto

```yaml
title: "Post Title"
description: "Brief description"
author: "Author Name"
date: 2024-01-15
categories:
  - R
  - Data Science
image: preview.png
```

## Creative Commons

### distill

```yaml
creative_commons: CC BY
```

### Quarto

```yaml
license: "CC BY"
```

Or more detailed:

```yaml
license:
  type: CC BY
  url: https://creativecommons.org/licenses/by/4.0/
```

## Step-by-Step Conversion

### For Articles

1. Rename `.Rmd` to `.qmd`.
2. Update format from `distill::distill_article` to `html`.
3. Convert author metadata structure.
4. Replace `<aside>` with `::: {.column-margin}`.
5. Convert layout classes (`.l-*` to `.column-*`).
6. Update figure chunk options.
7. Add `.appendix` class to appendix sections.

### For Blogs

1. Create `_quarto.yml` from `_site.yml`.
2. Rename post directories (optional).
3. Rename `.Rmd` files to `.qmd` or `index.qmd`.
4. Update post front matter.
5. Create listing page for blog index.
6. Migrate about page.

### Test Render

```bash
quarto render article.qmd
```

For blogs:

```bash
quarto preview
```

## Common Features

### Table of Contents

```yaml
format:
  html:
    toc: true
    toc-depth: 3
    toc-location: left
```

### Citations

Same BibTeX workflow works:

```yaml
bibliography: references.bib
csl: style.csl
```

### Self-Contained Output

```yaml
format:
  html:
    embed-resources: true
```

## Resources

- [Quarto HTML Documents](https://quarto.org/docs/output-formats/html-basics.html)
- [Quarto Websites](https://quarto.org/docs/websites/)
- [Article Layout](https://quarto.org/docs/authoring/article-layout.html)
