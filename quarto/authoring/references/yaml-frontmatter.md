# YAML Front Matter

YAML front matter configures document metadata, format options, and execution settings.
It's located at the top of a document and is enclosed by `---`.

## Basic Document YAML

```yaml
title: "Document Title"
author: "Author Name"
date: today
format: html
```

## Title Block

### Basic Metadata

```yaml
title: "My Document"
subtitle: "A Subtitle"
author: "Jane Doe"
date: 2024-01-15
```

### Date Options

```yaml
date: 2024-01-15           # Specific date
date: today                 # Current date
date: now                   # Current date and time
date: last-modified         # File modification date
```

### Date Formatting

```yaml
date: today
date-format: "MMMM D, YYYY"  # January 15, 2024
date-format: "D/M/YYYY"      # 15/1/2024
date-format: iso             # 2024-01-15
date-format: long            # January 15, 2024
date-format: short           # 1/15/24
```

## Author Metadata

### Single Author

```yaml
author: "Jane Doe"
```

### Detailed Author

```yaml
author:
  name: "Jane Doe"
  email: jane@example.com
  url: https://janedoe.com
  orcid: 0000-0000-0000-0000
```

### Multiple Authors

```yaml
author:
  - name: "Jane Doe"
    email: jane@example.com
    affiliations:
      - name: "University A"
        department: "Statistics"
  - name: "John Smith"
    affiliations:
      - name: "University B"
```

### Affiliations

```yaml
author:
  - name: "Jane Doe"
    affiliations:
      - id: univ-a
        name: "University A"
        city: "Boston"
        state: "MA"
        country: "USA"
```

## Abstract and Keywords

```yaml
title: "Research Paper"
abstract: |
  This is the abstract.
  It can span multiple lines.
keywords:
  - data science
  - statistics
  - machine learning
```

## Format Configuration

### Single Format

```yaml
format: html
```

### Format with Options

```yaml
format:
  html:
    toc: true
    code-fold: true
    theme: cosmo
```

### Multiple Formats

```yaml
format:
  html:
    toc: true
  pdf:
    documentclass: article
  docx: default
```

## HTML Format Options

```yaml
format:
  html:
    toc: true
    toc-depth: 3
    toc-location: left
    toc-title: "Contents"
    number-sections: true
    code-fold: true
    code-tools: true
    code-line-numbers: true
    theme: cosmo
    css: custom.css
    fontsize: 1.1em
    linestretch: 1.5
    mainfont: "Georgia"
```

### Themes

```yaml
format:
  html:
    theme: cosmo          # Bootstrap theme
    theme:                # Custom theme
      light: cosmo
      dark: darkly
    theme: custom.scss    # Custom SCSS
```

Built-in themes: `default`, `cerulean`, `cosmo`, `cyborg`, `darkly`, `flatly`, `journal`, `litera`, `lumen`, `lux`, `materia`, `minty`, `morph`, `pulse`, `quartz`, `sandstone`, `simplex`, `sketchy`, `slate`, `solar`, `spacelab`, `superhero`, `united`, `vapor`, `yeti`, `zephyr`.

## PDF Format Options

```yaml
format:
  pdf:
    documentclass: article
    papersize: a4
    fontsize: 11pt
    geometry:
      - margin=1in
    toc: true
    number-sections: true
    colorlinks: true
    mainfont: "Times New Roman"
    monofont: "Fira Code"
```

### LaTeX Options

```yaml
format:
  pdf:
    include-in-header:
      - text: |
          \usepackage{custom}
    include-before-body:
      - file: before.tex
    keep-tex: true
```

## Word (DOCX) Options

```yaml
format:
  docx:
    toc: true
    number-sections: true
    reference-doc: template.docx
    highlight-style: github
```

## RevealJS Options

```yaml
format:
  revealjs:
    theme: dark
    transition: slide
    slide-number: true
    chalkboard: true
    controls: true
    progress: true
```

## Execution Options

```yaml
execute:
  echo: true # Show code
  eval: true # Run code
  warning: false # Hide warnings
  message: false # Hide messages
  error: false # Stop on error
  cache: true # Cache results
  freeze: auto # Freeze outputs
```

### Per-Format Execution

```yaml
format:
  html:
    execute:
      echo: true
  pdf:
    execute:
      echo: false
```

## Bibliography

```yaml
bibliography: references.bib
csl: apa.csl
link-citations: true
citation-location: margin
```

## Cross-References

```yaml
crossref:
  fig-title: "Figure"
  tbl-title: "Table"
  eq-prefix: "Equation"
  chapters: true
```

## Language and Localization

```yaml
lang: en-US
```

```yaml
lang: de
crossref:
  fig-title: "Abbildung"
  tbl-title: "Tabelle"
```

## Table of Contents

```yaml
toc: true
toc-depth: 3
toc-title: "Table of Contents"
toc-location: left # HTML only
```

## Numbering

```yaml
number-sections: true
number-depth: 3
number-offset: [0, 0] # Start from specific number
```

## Code Highlighting

```yaml
highlight-style: github
highlight-style: monokai
highlight-style:
  light: github
  dark: monokai
```

## Project Configuration

In `_quarto.yml`:

```yaml
project:
  type: website
  output-dir: _site

website:
  title: "My Site"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: about.qmd
        text: About
  sidebar:
    style: floating
    contents: auto

format:
  html:
    theme: cosmo
    toc: true
```

### Project Types

```yaml
project:
  type: website    # Website
  type: book       # Book
  type: default    # Default (single files)
  type: manuscript # Academic manuscript
```

## Book Configuration

```yaml
project:
  type: book

book:
  title: "My Book"
  author: "Jane Doe"
  date: today
  chapters:
    - index.qmd
    - intro.qmd
    - part: "Part I"
      chapters:
        - chapter1.qmd
        - chapter2.qmd
    - summary.qmd
  appendices:
    - appendix.qmd
```

## Website Configuration

```yaml
website:
  title: "My Website"
  description: "Site description"
  site-url: https://example.com

  navbar:
    background: primary
    left:
      - text: "Home"
        href: index.qmd
      - text: "Blog"
        href: blog/index.qmd

  sidebar:
    contents:
      - section: "Getting Started"
        contents:
          - start.qmd
          - install.qmd

  page-footer:
    center: "Copyright 2024"
```

## Parameters

```yaml
params:
  data_file: "data.csv"
  threshold: 0.5
  show_advanced: true
```

Use in document:

````markdown
```{r}
#| label: read-data

data <- read.csv(params$data_file)
```
````

## Include Files

```yaml
include-in-header:
  - text: |
      <script src="custom.js"></script>
  - file: header.html

include-before-body:
  - file: before.html

include-after-body:
  - file: footer.html
```

## Metadata Files

```yaml
metadata-files:
  - _metadata.yml
```

Shared settings in `_metadata.yml`:

```yaml
author: "Jane Doe"
format:
  html:
    theme: cosmo
```

## Resources

- [Quarto Document Options](https://quarto.org/docs/reference/formats/html.html)
- [PDF Options](https://quarto.org/docs/reference/formats/pdf.html)
- [Project Configuration](https://quarto.org/docs/projects/quarto-projects.html)
