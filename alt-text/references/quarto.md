# Alt Text in Quarto Documents

This reference covers how to find figures and add alt text in `.qmd` files.

## Finding figures

```bash
# List all figure labels with file and line number
grep -n "#| label: fig-" *.qmd

# Find figures in a specific file
grep -n "#| label: fig-" my-document.qmd

# Find a specific figure
grep -rn "#| label: fig-splines-predictor-outcome" *.qmd
```

## For each figure

1. **Locate** — use grep to find file and line number
2. **Read context** — read ~50 lines around the chunk (prose before + code + prose after)
3. **Extract details** — note `fig-cap`, ggplot code, data generation, surrounding explanation
4. **Draft alt text** — apply the three-part structure from the main skill
5. **Verify** — check against the quality checklist

## Adding fig-alt

Use the hashpipe syntax inside the code chunk:

```r
#| label: fig-penguin-scatter
#| fig-cap: "Bill length vs. bill depth for 344 penguins."
#| fig-alt: >
#|   Scatter chart of bill length vs. bill depth for 344 penguins
#|   across three species. Gentoo penguins form a distinct cluster
#|   at higher bill depth. Adelie and Chinstrap overlap but separate
#|   along the bill length axis, with Chinstrap skewing higher.
plot_code_here()
```

Note: use `fig-alt` (hyphen) in `.qmd` files.

## Auditing existing alt text

When alt text already exists, leave it alone unless it fails one of these checks:

**Relative references** — alt text must be self-contained. Fix phrases like:
- "A plot identical to the one above…" → describe the plot fully
- "Much like the first one…" → stand-alone description

**Missing key information** — fix if alt text omits:
- Chart type as the first words
- Axis labels and what they represent
- The key pattern or takeaway

**Grammar and spelling errors** — alt text is read aloud by screen readers.
