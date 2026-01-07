# Converting xaringan to Quarto RevealJS

Guide for converting xaringan presentations to Quarto RevealJS format.

## Overview

Key differences:

1. Format: `moon_reader` → `revealjs`
2. Slide separators: `---` → headers
3. Incremental: `--` → `::: {.incremental}`
4. Speaker notes: `???` → `::: {.notes}`

## Quick Start

### 1. Rename File

```bash
mv slides.Rmd slides.qmd
```

### 2. Update YAML

#### Xaringan

```yaml
output:
  xaringan::moon_reader:
    lib_dir: libs
    nature:
      highlightStyle: github
```

#### Quarto

```yaml
format:
  revealjs:
    theme: default
    highlight-style: github
```

### 3. Convert Slides

Replace `---` with headers:

````markdown
# xaringan

---

# Slide Title

Content

---

# Next Slide

# Quarto

## Slide Title

Content

## Next Slide
````

## YAML Conversion

### Basic Presentation

#### Xaringan

```yaml
title: "My Presentation"
author: "Jane Doe"
date: "2024-01-15"
output:
  xaringan::moon_reader:
    css: ["default", "custom.css"]
    nature:
      ratio: "16:9"
      highlightStyle: github
      highlightLines: true
      countIncrementalSlides: false
```

#### Quarto

```yaml
title: "My Presentation"
author: "Jane Doe"
date: 2024-01-15
format:
  revealjs:
    theme: default
    css: custom.css
    slide-number: true
    highlight-style: github
    code-line-numbers: true
    width: 1600
    height: 900
```

### Common Options

| xaringan                 | Quarto RevealJS                       |
| ------------------------ | ------------------------------------- |
| `ratio: "16:9"`          | `width: 1600` / `height: 900`         |
| `highlightStyle: github` | `highlight-style: github`             |
| `highlightLines: true`   | `code-line-numbers: true`             |
| `countdown`              | `chalkboard: true` or timer extension |
| `autoplay: 30000`        | `auto-slide: 30000`                   |

## Slide Separators

### xaringan

Uses `---` to separate slides:

````markdown
# First Slide

Content

---

# Second Slide

More content

---

class: center, middle

# Centered Slide
````

### Quarto

Uses headers (level 1 or 2):

````markdown
# First Slide

Content

## Second Slide

More content

## Centered Slide {.center}
````

Or with explicit separators:

```yaml
format:
  revealjs:
    slide-level: 2
```

## Incremental Reveals

### xaringan

Uses `--` within a slide:

````markdown
# Incremental

- ## First point

- ## Second point

- Third point
````

### Quarto

Use incremental class:

````markdown
## Incremental

::: {.incremental}

- First point
- Second point
- Third point

:::
````

Or globally:

```yaml
format:
  revealjs:
    incremental: true
```

Per-slide opt-out:

````markdown
## Non-Incremental {.nonincremental}

- All at once
- All at once
````

## Speaker Notes

### xaringan

Uses `???`:

````markdown
# Slide Title

Content here.

???

Speaker notes go here.
They can span multiple lines.
````

### Quarto

Uses notes div:

````markdown
## Slide Title

Content here.

::: {.notes}
Speaker notes go here.
They can span multiple lines.
:::
````

## Two-Column Layouts

### xaringan

````markdown
.pull-left[
Left content
]

.pull-right[
Right content
]
````

### Quarto

````markdown
::: {.columns}

::: {.column width="50%"}
Left content
:::

::: {.column width="50%"}
Right content
:::

:::
````

## Slide Classes

### xaringan

````markdown
---

class: inverse, center, middle

# Dark Slide
````

### Quarto

````markdown
## Dark Slide {.inverse .center .middle}

Or use theme variants.
````

Background options:

````markdown
## Slide with Background {background-color="black"}
````

## Code Highlighting

### xaringan

````markdown
```{r, highlight.output=c(1,3)}
# Highlighted output
```
````

### Quarto

````markdown
```{r}
#| code-line-numbers: "1,3"

# Highlighted lines
```
````

Or in output:

````markdown
```{r}
#| output-line-numbers: "1,3"
```
````

## CSS Customization

### xaringan

```yaml
output:
  xaringan::moon_reader:
    css: ["default", "my-theme.css"]
```

### Quarto

```yaml
format:
  revealjs:
    theme: [default, custom.scss]
    css: styles.css
```

### Custom SCSS

```scss
// custom.scss
$body-bg: #f0f0f0;
$body-color: #333;
$link-color: #007bff;

.reveal h1 {
  color: navy;
}
```

## Fragments (Animations)

### xaringan

````markdown
.animated.fadeIn[
Content fades in
]
````

### Quarto

````markdown
::: {.fragment .fade-in}
Content fades in
:::
```

Fragment types:

- `.fade-in`
- `.fade-out`
- `.fade-up`
- `.highlight-red`
- `.strike`

## Images and Figures

### xaringan

````markdown
![](image.png)

.center[
![](centered.png)
]
````

### Quarto

````markdown
![](image.png)

![](centered.png){fig-align="center"}
````

### Full-Screen Background

````markdown
## {background-image="image.jpg" background-size="cover"}

Content overlaid on image.
````

## Special Slides

### Title Slide

Automatic in Quarto from YAML.

### Section Headers

````markdown
# Section Title {.section}
````

### Thank You Slide

````markdown
## Thank You! {.center .middle}

Questions?
````

## Common xaringan Features

### Countdown Timer

Install extension:

```bash
quarto add gadenbuie/countdown
```

### Chalkboard

```yaml
format:
  revealjs:
    chalkboard: true
```

### Self-Contained

```yaml
format:
  revealjs:
    embed-resources: true
```

## Step-by-Step Conversion

### 1. Rename and Update YAML

```bash
mv slides.Rmd slides.qmd
```

Update format to `revealjs`.

### 2. Convert Slide Separators

Replace `---` with `##` headers.

### 3. Convert Incremental

Replace `--` with `::: {.incremental}`.

### 4. Convert Notes

Replace `???` with `::: {.notes}`.

### 5. Convert Columns

Replace `.pull-left`/`.pull-right` with columns divs.

### 6. Update Classes

Replace `class:` with attributes on headers.

### 7. Test Render

```bash
quarto render slides.qmd
```

## Example Conversion

### xaringan

````markdown
---
title: "My Talk"
output: xaringan::moon_reader
---

# Introduction

Welcome!

---

# Points

- ## First

- Second

???
Remember to pause here.

---

class: inverse, center

# Thank You!
````

### Quarto

````markdown
---
title: "My Talk"
format: revealjs
---

## Introduction

Welcome!

## Points

::: {.incremental}

- First
- Second

:::

::: {.notes}
Remember to pause here.
:::

## Thank You! {.inverse .center}
````

## Resources

- [Quarto RevealJS](https://quarto.org/docs/presentations/revealjs/)
- [RevealJS Options](https://quarto.org/docs/reference/formats/presentations/revealjs.html)
- [Presentation Features](https://quarto.org/docs/presentations/)
