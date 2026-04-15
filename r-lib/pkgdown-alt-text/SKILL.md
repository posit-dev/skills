---
name: pkgdown-alt-text
description: >
  Add accessible alt text to all images and plots in a pkgdown site. Use when
  the user wants to add, improve, or audit alt text for figures in vignettes,
  articles, or README files in an R package with a pkgdown site. Triggers for
  requests about accessibility, fig.alt, figure descriptions, screen reader
  support, or making a pkgdown site more accessible.
metadata:
  author: Emil Hvitfeldt (@emilhvitfeldt)
  version: "1.0"
license: MIT
---

# Add Alt Text to a pkgdown Site

Generate accessible alt text for all images and plots across the pkgdown site.

ARGUMENTS
- label: (optional) specific chunk label or image to target
- file: (optional) specific vignette or README file to process

## Where images appear in a pkgdown site

| Location | Image type | Can have alt text? |
|----------|------------|-------------------|
| `vignettes/*.Rmd` or `vignettes/*.qmd` | code-generated plots | Yes — `fig.alt` chunk option |
| `vignettes/*.Rmd` | static images via `knitr::include_graphics()` | Yes — `fig.alt` chunk option |
| `README.Rmd` / `README.md` | code-generated plots | Yes — `fig.alt` chunk option |
| `README.Rmd` / `README.md` | markdown images `![](path)` | Yes — fill in the bracket |
| `README.Rmd` / `README.md` | HTML `<img src=...>` tags | Yes — add `alt="..."` attribute |
| `R/*.R` `@examples` | code-generated plots | **No — pkgdown limitation** |

There is currently no way to add alt text to plots generated in `@examples`
blocks. Focus effort on vignettes and README.

## Step 1 — Find missing alt text

### Build the site and read warnings

The most reliable way: let pkgdown identify all missing alt text automatically.

```r
# Build only articles (faster than full site)
Rscript -e "pkgdown::build_articles()"

# Or build the full site
Rscript -e "pkgdown::build_site()"
```

pkgdown prints a warning for every code chunk that produces a plot but has no
`fig.alt`. Note down every file and chunk mentioned.

### Find chunks missing fig.alt in vignettes

```bash
# Find chunks that already have fig.alt (to see what's covered)
grep -rn "fig.alt\|fig-alt" vignettes/ README.Rmd

# Find all knitr::include_graphics() calls (static images in chunks)
grep -rn "include_graphics" vignettes/ README.Rmd
```

### Find static images missing alt text

```bash
# Markdown images with empty alt: ![](path)
grep -rn "!\[\](" vignettes/ README.md README.Rmd

# All markdown images — review each for descriptive alt text
grep -rn "!\[" vignettes/ README.md README.Rmd

# HTML <img> tags — check each for a non-empty alt attribute
grep -rn "<img" vignettes/ README.md README.Rmd
```

Package logos are commonly written as HTML `<img>` tags at the top of
`README.Rmd`. Check that the `alt` attribute is present and descriptive:

```html
<!-- Missing alt -->
<img src='man/figures/logo.png' align="right" height="139" />

<!-- Fixed -->
<img src='man/figures/logo.png' align="right" height="139"
  alt="Package hex logo: a blue hexagon with the package name." />
```

## Step 2 — Audit quality of existing alt text

When alt text already exists, leave it alone unless it has a concrete problem.
Only rewrite alt text that fails one of these checks:

**Relative references** — alt text must be self-contained. Screen readers
don't know what "above" refers to. Fix phrases like:
- "A plot identical to the one above..." → describe the plot fully
- "Much like the first one..." → stand-alone description
- "The same data as shown above..." → name the data explicitly

**Missing key information** — fix if the alt text omits:
- Chart type as the first words
- Axis labels and what they represent
- The key pattern or takeaway

**Grammar and spelling errors** — alt text is read aloud by screen readers.
Fix typos and grammatically broken sentences.

If existing alt text is accurate, complete, and self-contained, do not change
it even if you would have phrased it differently.

## Step 3 — Generate alt text for each figure

For each missing or weak figure, read ~50 lines of context around the chunk:
- The plotting code (what type of chart, axes, variables)
- Any data generation or transformation above the chunk
- The surrounding prose (explains the purpose and key insight)
- The `fig.cap` if present (alt text should complement, not duplicate it)

Apply **Amy Cesal's formula** for data visualization alt text:
1. **Chart type** — first words identify the format
2. **Data description** — axes, variables, what is shown
3. **Key insight** — the pattern or takeaway (usually in surrounding prose)

Use the source code to extract precise details: variable names, axis labels,
facet structure, color encodings, specific value ranges. This is the key
advantage over typical alt text scenarios.

See the `quarto-alt-text` skill for detailed writing guidelines, chart-type
templates, length guidelines, and a quality checklist — the same principles
apply here.

## Step 4 — Add fig.alt to Rmd chunks

The `fig.alt` chunk option works for both code-generated plots and static
images loaded with `knitr::include_graphics()`.

### Hashpipe syntax (preferred)

```r
#| fig.alt: >
#|   Scatter chart of bill length vs. bill depth for 344 penguins
#|   across three species. Gentoo penguins form a distinct cluster
#|   at higher bill depth. Adelie and Chinstrap overlap but separate
#|   along the bill length axis, with Chinstrap skewing higher.
plot_code_here()
```

### Knitr chunk option syntax

````markdown
```{r penguin-scatter, fig.alt="Scatter chart of bill length vs. bill depth..."}
plot_code_here()
```
````

### Multiple plots in one chunk

When a chunk produces multiple plots, `fig.alt` accepts a vector — one string
per plot, in order:

```r
#| fig.alt:
#|   - "Histogram of bill length. Right-skewed distribution with a peak at 45-50mm."
#|   - "Histogram of bill depth. Bimodal distribution with peaks at 15mm and 18mm."
```

## Step 5 — Add alt text to static markdown images

For `![](path)` images, fill in the bracket:

```markdown
<!-- Before -->
![](man/figures/logo.png)

<!-- After -->
![A hexagonal logo with a blue background and white text reading 'pkgdown'.](man/figures/logo.png)
```

For purely decorative images (no informational content), an empty alt
explicitly signals to screen readers to skip the image — leave the bracket
empty intentionally and add a comment to make this clear:

```markdown
<!-- Decorative banner, intentionally no alt text -->
![](man/figures/decorative-banner.png)
```

## Step 6 — Verify

```r
# Rebuild articles and confirm no more fig.alt warnings
Rscript -e "pkgdown::build_articles()"
```

No warnings about missing alt text means all vignette plots are covered.

## Quarto vignettes (`.qmd`)

For vignettes using Quarto format, use the Quarto-style `fig-alt` option:

```r
#| fig-alt: >
#|   Scatter chart of bill length vs. bill depth for 344 penguins
#|   across three species.
```

Note the hyphen (`fig-alt`) vs the dot (`fig.alt`) used in `.Rmd` files.
