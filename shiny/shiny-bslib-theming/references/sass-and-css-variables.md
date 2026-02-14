# Bootstrap Sass and CSS Variables

Bootstrap 5 uses a two-layer variable system: Sass variables (compile-time) and CSS custom properties (runtime). Understanding both layers is key to effective theming with bslib.

## Table of Contents

- [Two-Layer Variable System](#two-layer-variable-system)
- [Sass Variables (Compile-Time)](#sass-variables-compile-time)
- [CSS Custom Properties (Runtime)](#css-custom-properties-runtime)
- [How bslib Connects the Layers](#how-bslib-connects-the-layers)
- [CSS Utility Classes](#css-utility-classes)

## Two-Layer Variable System

```
Sass Variables ($primary, $body-bg, ...)
  ↓  compiled by sass package
CSS Custom Properties (--bs-primary, --bs-body-bg, ...)
  ↓  applied at runtime
Rendered Styles
```

**Sass variables** control compile-time defaults. When you set `bs_theme(primary = "red")`, bslib places `$primary: red !default` before Bootstrap's own Sass, causing all downstream variables that reference `$primary` to update.

**CSS custom properties** (`--bs-*` prefixed) are emitted from the compiled Sass onto `:root`. They enable runtime overrides — including Bootstrap 5.3's color modes — without recompilation.

## Sass Variables (Compile-Time)

### How bs_theme() Uses Sass Variables

`bs_theme()` places variable defaults **before** Bootstrap's own defaults in the Sass compilation. Due to Sass's `!default` flag semantics, your values take precedence:

```r
# Sets $primary: red !default before Bootstrap processes its files.
# All variables referencing $primary (buttons, links, focus, etc.) update.
bs_theme(primary = "red")
```

### Variable Placement with .where

The `.where` parameter in `bs_add_variables()` controls where definitions are placed:

```
┌─────────────────────────────────────────┐
│ "defaults"     ← Your !default vars    │ ← bs_theme(...) and bs_add_variables()
│ Bootstrap's own !default vars           │
│ "declarations" ← Your declarations     │ ← Can reference $primary, $secondary, etc.
│ "rules"        ← Your rules            │ ← After all variable processing
└─────────────────────────────────────────┘
```

This is why referencing `$secondary` in `bs_theme()` fails (it's not yet defined), but works with `bs_add_variables(.where = "declarations")`.

### Finding Sass Variable Names

**Searchable reference:** https://rstudio.github.io/bslib/articles/bs5-variables/

**Categories of commonly used variables:**

| Category | Example Variables |
|---|---|
| **Colors** | `body-bg`, `body-color`, `primary`, `secondary`, `link-color` |
| **Typography** | `font-family-base`, `font-size-base`, `line-height-base`, `headings-font-weight` |
| **Spacing** | `spacer`, `spacers` (map) |
| **Borders** | `border-width`, `border-color`, `border-radius` |
| **Cards** | `card-bg`, `card-border-color`, `card-border-radius`, `card-cap-bg` |
| **Buttons** | `btn-padding-y`, `btn-padding-x`, `btn-border-radius`, `btn-font-size` |
| **Navbar** | `navbar-bg`, `navbar-padding-y`, `navbar-brand-font-size` |
| **Inputs** | `input-bg`, `input-border-color`, `input-border-radius`, `input-focus-border-color` |
| **Grid** | `grid-gutter-width`, `container-max-widths` (map) |

## CSS Custom Properties (Runtime)

### Root-Level Properties

Bootstrap compiles Sass variables into `--bs-*` CSS custom properties on `:root`:

```css
:root {
  --bs-primary: #0d6efd;
  --bs-primary-rgb: 13, 110, 253;    /* RGB triplet for rgba() usage */
  --bs-body-color: #212529;
  --bs-body-bg: #fff;
  --bs-body-font-family: system-ui, -apple-system, ...;
  --bs-body-font-size: 1rem;
  --bs-border-radius: 0.375rem;
  --bs-emphasis-color: #000;
  --bs-secondary-color: rgba(33, 37, 41, 0.75);
  --bs-link-color: #0d6efd;
  /* ... hundreds more */
}
```

### Semantic Color Variants

Each theme color gets three semantic variants for subtle UI contexts:

```css
:root {
  --bs-primary-text-emphasis: ...;    /* Text on subtle backgrounds */
  --bs-primary-bg-subtle: ...;        /* Subtle backgrounds */
  --bs-primary-border-subtle: ...;    /* Subtle borders */
}
```

These are heavily used by Bootstrap's alert, badge, and list-group components.

### Component-Level Properties

Many Bootstrap components define local CSS variables instead of relying on root variables:

```css
.navbar {
  --bs-navbar-padding-y: 0.5rem;
  --bs-navbar-color: rgba(var(--bs-emphasis-color-rgb), 0.65);
  /* ... */
}
```

This prevents style inheritance issues in nested contexts (e.g., nested tables).

### Color Modes and CSS Variable Overrides

Bootstrap 5.3 uses `[data-bs-theme="dark"]` to swap CSS custom properties without recompilation:

```css
/* Light mode (default) */
:root {
  --bs-body-color: #212529;
  --bs-body-bg: #fff;
  --bs-emphasis-color: #000;
}

/* Dark mode — same properties, different values */
[data-bs-theme="dark"] {
  --bs-body-color: #dee2e6;
  --bs-body-bg: #212529;
  --bs-emphasis-color: #fff;
  --bs-link-color: #6ea8fe;
  --bs-border-color: #495057;
}
```

No class changes needed on components — switching the `data-bs-theme` attribute on an ancestor cascades new values to all descendants automatically.

### Per-Element Theming

Apply `data-bs-theme` to any element for scoped theming:

```r
# This card renders in dark mode regardless of the page's global mode
tags$div(
  `data-bs-theme` = "dark",
  card(card_header("Dark Card"), "Always dark")
)
```

### Prefix

All CSS custom properties use `--bs-` prefix (configurable via the `$prefix` Sass variable).

### Limitations

Grid breakpoint CSS variables exist but **cannot** be used in media queries (CSS spec constraint). They can be used in other CSS contexts and via JavaScript.

## How bslib Connects the Layers

When you call `bs_theme(primary = "red")`:

1. bslib sets `$primary: red !default` in the Sass defaults layer
2. The sass package compiles all Bootstrap Sass (with your overrides)
3. Bootstrap's `_root.scss` emits `--bs-primary: red` (and all derived properties)
4. The compiled CSS is served to the browser

When `input_dark_mode()` toggles dark mode:
- It sets `data-bs-theme="dark"` on the `<html>` element (client-side)
- Bootstrap's pre-compiled dark mode CSS variables take effect
- No Sass recompilation happens

When `session$setCurrentTheme()` switches themes:
- A completely new Sass compilation produces new CSS
- The new CSS replaces the old one via Shiny's connection
- This is heavier than client-side color mode toggling

## CSS Utility Classes

Bootstrap provides utility classes for one-off styling without custom CSS. These use CSS custom properties internally and respond to color mode changes.

**Colors:**
```r
card_header(class = "bg-primary text-white", "Blue Header")
tags$p(class = "text-muted", "Secondary text")
tags$span(class = "text-danger fw-bold", "Error!")
```

**Common utilities:**

| Category | Examples |
|---|---|
| **Background** | `bg-primary`, `bg-secondary`, `bg-success`, `bg-danger`, `bg-light`, `bg-dark` |
| **Text color** | `text-primary`, `text-secondary`, `text-muted`, `text-white` |
| **Spacing** | `p-3` (padding), `m-4` (margin), `px-2`, `mt-3`, `gap-2` |
| **Display** | `d-flex`, `d-none`, `d-md-block`, `d-grid` |
| **Text** | `text-center`, `text-end`, `fw-bold`, `fs-5`, `text-truncate` |
| **Borders** | `border`, `border-primary`, `rounded`, `rounded-3` |
| **Flex** | `justify-content-between`, `align-items-center`, `flex-wrap` |

**Reference:** https://rstudio.github.io/bslib/articles/utility-classes/
