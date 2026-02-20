# Callouts

Callouts are specially formatted blocks for notes, warnings, tips, and other highlighted content.

## Callout Types

Five built-in types: `note`, `warning`, `important`, `tip`, `caution`.

````markdown
::: {.callout-note}
This is a note callout.
:::
````

Replace `note` with any other type (`warning`, `important`, `tip`, `caution`) for the corresponding style.

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

Three styles: `default` (colored header with icon), `simple` (lighter, no colored header), `minimal` (borders only).

````markdown
::: {.callout-note appearance="simple"}
Simple appearance.
:::
````

Set document default in YAML:

```yaml
callout-appearance: simple
```

## Collapsible Callouts

````markdown
::: {.callout-tip collapse="true"}

## Expand for Details

Hidden content revealed on click.

:::
````

`collapse="true"` starts collapsed. `collapse="false"` starts expanded but is collapsible. Without `collapse`, the callout is not collapsible.

## Icons

Disable per-callout or document-wide:

````markdown
::: {.callout-note icon="false"}
No icon on this callout.
:::
````

```yaml
callout-icon: false
```

## Cross-Referenceable Callouts

Add an ID with the appropriate prefix to reference callouts:

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

## Nested Callouts

Use more colons for outer divs when nesting:

````markdown
:::: {.callout-note}

## Outer Callout

::: {.callout-tip}
Nested callout.
:::

::::
````

## Format-Specific Options

```yaml
# HTML
format:
  html:
    callout-appearance: simple
    callout-icon: true

# PDF
format:
  pdf:
    callout-appearance: default
```

RevealJS supports callouts but `collapse` is not available.

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

Callouts support any markdown content including lists, code blocks, images, and multiple paragraphs.

## Resources

- [Quarto Callouts](https://quarto.org/docs/authoring/callouts.html)
