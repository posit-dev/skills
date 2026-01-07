# Callouts

Callouts are specially formatted blocks for notes, warnings, tips, and other highlighted content.

## Callout Types

Quarto provides five built-in callout types:

### Note

````markdown
::: {.callout-note}
This is a note callout.
:::
````

### Warning

````markdown
::: {.callout-warning}
This is a warning callout.
:::
````

### Important

````markdown
::: {.callout-important}
This is an important callout.
:::
````

### Tip

````markdown
::: {.callout-tip}
This is a tip callout.
:::
````

### Caution

````markdown
::: {.callout-caution}
This is a caution callout.
:::
````

## Custom Titles

Use a heading for custom title:

````markdown
::: {.callout-note}

## Custom Title Here

Content of the callout.

:::
````

Or use `title` attribute:

````markdown
::: {.callout-note title="My Custom Title"}
Content of the callout.
:::
````

## Appearance Options

Three appearance styles:

### Default

Colored header with icon:

````markdown
::: {.callout-note}
Default appearance.
:::
````

### Simple

Lighter, no colored header:

````markdown
::: {.callout-note appearance="simple"}
Simple appearance.
:::
````

### Minimal

Borders only, no header background or icon:

````markdown
::: {.callout-note appearance="minimal"}
Minimal appearance.
:::
````

### Document Default

Set default appearance in YAML:

```yaml
callout-appearance: simple
```

## Collapsible Callouts

Make callouts expandable/collapsible:

### Collapsed by Default

````markdown
::: {.callout-tip collapse="true"}

## Expand for Details

Hidden content revealed on click.

:::
````

### Expanded by Default

````markdown
::: {.callout-tip collapse="false"}

## Click to Collapse

Content visible initially but can be collapsed.

:::
````

Note: `collapse="false"` makes it collapsible but expanded initially. Without `collapse`, the callout is not collapsible.

## Icons

### Disable Icon

````markdown
::: {.callout-note icon="false"}
No icon on this callout.
:::
````

### Document Default

```yaml
callout-icon: false
```

## Cross-Referenceable Callouts

Add an ID to reference callouts:

````markdown
::: {#nte-important .callout-note}

## Important Information

This callout can be referenced.

:::

See @nte-important for details.
````

### Callout Prefixes

| Type      | Prefix |
| --------- | ------ |
| Note      | `nte-` |
| Tip       | `tip-` |
| Warning   | `wrn-` |
| Important | `imp-` |
| Caution   | `cau-` |

### Example

````markdown
::: {#tip-shortcut .callout-tip}

## Keyboard Shortcut

Press Ctrl+S to save.
:::

::: {#wrn-data .callout-warning}

## Data Warning

Back up your data first.

:::

See @tip-shortcut for the shortcut and @wrn-data for the warning.
````

## Complex Content

Callouts can contain any content:

### Lists

````markdown
::: {.callout-note}

## Steps to Follow

1. First step
2. Second step
3. Third step

:::
````

### Code

````markdown
::: {.callout-tip}

## Code Example

```{r}
x <- 1 + 1
```

## Code Block Example

```r
x <- 1 + 1
```

Or

```{.r}
x <- 1 + 1
```

:::
````

### Multiple Paragraphs

````markdown
::: {.callout-important}
First paragraph.

Second paragraph with **bold** text.
:::
````

### Images

````markdown
::: {.callout-note}

## Visual Guide

![Diagram](diagram.png)

:::
````

## Nested Callouts

Callouts can be nested (use more colons for outer):

````markdown
::: {.callout-note}

## Outer Callout

::: {.callout-tip}
Nested callout.
:::

:::
````

## Format-Specific Options

### HTML Options

```yaml
format:
  html:
    callout-appearance: simple
    callout-icon: true
```

### PDF Options

```yaml
format:
  pdf:
    callout-appearance: default
```

### RevealJS

Callouts work in presentations but `collapse` is not available.

## Styling Callouts

### Custom CSS (HTML)

```css
.callout-note {
  border-left-color: #0066cc;
}

.callout-note .callout-title {
  background-color: #e6f0ff;
}
```

### SCSS Variables

```scss
$callout-color-note: #0066cc;
$callout-color-tip: #00cc66;
```

## Summary of Attributes

| Attribute         | Values                                           | Description      |
| ----------------- | ------------------------------------------------ | ---------------- |
| `.callout-{type}` | `note`, `warning`, `important`, `tip`, `caution` | Callout type     |
| `appearance`      | `default`, `simple`, `minimal`                   | Visual style     |
| `collapse`        | `true`, `false`                                  | Make collapsible |
| `icon`            | `true`, `false`                                  | Show/hide icon   |
| `title`           | String                                           | Custom title     |
| `#id`             | `nte-`, `tip-`, `wrn-`, `imp-`, `cau-` + name    | For cross-refs   |

## Examples

### Installation Guide

````markdown
::: {.callout-note}

## Prerequisites

Make sure you have R 4.0+ installed.

:::

::: {.callout-warning}

## Backup First

Back up your existing installation before proceeding.

:::

::: {.callout-tip collapse="true"}

## Troubleshooting

If you encounter errors, try clearing your cache.

:::
````

### Documentation

````markdown
::: {.callout-important}

## Breaking Change

This version changes the default behavior.
See migration guide below.

:::

::: {.callout-caution}

## Experimental Feature

This API may change in future versions.

:::
````

## Resources

- [Quarto Callouts](https://quarto.org/docs/authoring/callouts.html)
