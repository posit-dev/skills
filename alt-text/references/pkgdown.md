# Alt Text in pkgdown Sites

This reference covers how to find images and add alt text across a pkgdown site.

## Where images appear

| Location | Image type | Can have alt text? |
|----------|------------|-------------------|
| `vignettes/*.Rmd` or `vignettes/*.qmd` | code-generated plots | Yes — `fig.alt` chunk option |
| `vignettes/*.Rmd` | static images via `knitr::include_graphics()` | Yes — `fig.alt` chunk option |
| `README.Rmd` / `README.md` | code-generated plots | Yes — `fig.alt` chunk option |
| `README.Rmd` / `README.md` | markdown images `![](path)` | Yes — fill in the bracket |
| `README.Rmd` / `README.md` | HTML `<img src=...>` tags | Yes — add `alt="..."` attribute |
| `R/*.R` `@examples` | code-generated plots | **No — pkgdown limitation** |

There is currently no way to add alt text to plots generated in `@examples` blocks.
Focus effort on vignettes and README.

## Step 1 — Find missing alt text

### Find chunks missing fig.alt in vignettes

```bash
# Find chunks that already have fig.alt (to see what's covered)
grep -rn "fig\.alt\|fig-alt" vignettes/

# Find all plot-producing chunks — each one needs a fig.alt
grep -rn "ggplot\|geom_\|autoplot\|include_graphics" vignettes/
```

Compare the two lists to identify chunks with plots but no `fig.alt`.

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

**Relative references** — alt text must be self-contained. Fix phrases like:
- "A plot identical to the one above…" → describe the plot fully
- "The same data as shown above…" → name the data explicitly

**Missing key information** — fix if alt text omits chart type, axis labels, or
the key pattern.

**Grammar and spelling errors** — alt text is read aloud by screen readers.

## Step 3 — Add fig.alt to Rmd chunks

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
#|   - "Histogram of bill length. Right-skewed distribution with a peak at 45–50mm."
#|   - "Histogram of bill depth. Bimodal distribution with peaks at 15mm and 18mm."
```

## Step 4 — Add alt text to static markdown images

For `![](path)` images, fill in the bracket:

```markdown
<!-- Before -->
![](man/figures/logo.png)

<!-- After -->
![A hexagonal logo with a blue background and white text reading 'pkgdown'.](man/figures/logo.png)
```

For purely decorative images, leave the bracket empty intentionally and add a
comment:

```markdown
<!-- Decorative banner, intentionally no alt text -->
![](man/figures/decorative-banner.png)
```

## Step 5 — Verify

Because pkgdown does not warn about missing alt text in vignettes, verify by
re-running the same grep from Step 1 and confirming every plot-producing chunk
now has a `fig.alt`:

```bash
# Should list every chunk with a plot
grep -rn "ggplot\|geom_\|autoplot\|include_graphics" vignettes/

# Should now match the same chunks
grep -rn "fig\.alt\|fig-alt" vignettes/
```

For the home page, `build_site()` will warn if any README images are still
missing alt text.

## Quarto vignettes (`.qmd`)

For vignettes using Quarto format, use `fig-alt` (hyphen) instead of `fig.alt` (dot):

```r
#| fig-alt: >
#|   Scatter chart of bill length vs. bill depth for 344 penguins
#|   across three species.
```
