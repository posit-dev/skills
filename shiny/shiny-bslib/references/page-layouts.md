# Page Layouts in bslib

This reference covers the page-level layout functions in bslib that structure entire Shiny applications. These are the top-level containers that determine the overall architecture of your app.

## Table of Contents

- [Dashboard Layouts](#dashboard-layouts)
  - [page_sidebar()](#page_sidebar)
  - [page_navbar()](#page_navbar)
  - [page_fillable()](#page_fillable)
- [Basic Page Layouts](#basic-page-layouts)
- [Filling vs Scrolling Behavior](#filling-vs-scrolling-behavior)
- [Mobile Considerations](#mobile-considerations)
- [Production Best Practices](#production-best-practices)

## Dashboard Layouts

### page_sidebar()

The primary function for creating single-page dashboards with a sidebar and main content area.

**Basic structure:**
```r
ui <- page_sidebar(
  title = "My dashboard",
  sidebar = sidebar("Sidebar content"),
  "Main content area"
)
```

**Best practice:** Keep inputs in the `sidebar` and outputs in the main content area. Wrap outputs in `card()` and sidebar contents in `sidebar()` for titles and custom styling.

**Example with cards:**
```r
ui <- page_sidebar(
  title = "Penguins Dashboard",
  sidebar = sidebar(
    selectInput("species", "Species", choices = unique(penguins$species))
  ),
  card(
    full_screen = TRUE,
    card_header("Bill Length"),
    plotOutput("bill_length")
  ),
  card(
    card_header("Summary Statistics"),
    verbatimTextOutput("summary")
  )
)
```

**Key parameters:**
- `title`: App title displayed at the top
- `sidebar`: A `sidebar()` object with inputs/controls
- `theme`: Optional `bs_theme()` object for styling
- `fillable`: Whether the page should fill the viewport height (default TRUE)
- `fillable_mobile`: Whether fillable behavior applies on mobile (default FALSE)
- `class = "bslib-page-dashboard"`: Adds a light gray background behind the main area, which looks best when cards are used as the primary content containers

### page_navbar()

Use `page_navbar()` for multi-page dashboards with a top navigation bar. Each page is defined with `nav_panel()`.

**Basic structure:**
```r
ui <- page_navbar(
  title = "Multi-Page Dashboard",
  nav_panel("Page 1", "Content for page 1"),
  nav_panel("Page 2", "Content for page 2"),
  nav_panel("Page 3", "Content for page 3")
)
```

**With sidebar:**
```r
ui <- page_navbar(
  title = "Penguins Dashboard",
  sidebar = sidebar(
    selectInput("color_by", "Color by", choices = c("species", "island"))
  ),
  nav_spacer(),
  nav_panel("Bill Length", card(...)),
  nav_panel("Bill Depth", card(...)),
  nav_panel("Body Mass", card(...)),
  nav_item(tags$a("Documentation", href = "https://example.com"))
)
```

**Important caveat:** `page_navbar()`'s `sidebar` argument puts the same sidebar on every page. If you need different sidebars per page or conditional sidebar contents, see the [sidebars reference](sidebars.md) for strategies.

**Key parameters:**
- `title`: App title in the navbar
- `sidebar`: Optional `sidebar()` shown on all pages
- `id`: ID for tracking the active page (accessible as `input$<id>`)
- `fillable`: Can be TRUE (all pages), FALSE (no pages), or a vector of page names
- `theme`: Optional `bs_theme()` object

**Dashboard appearance:** Add `class = "bslib-page-dashboard"` to individual `nav_panel()` containers (not the `page_navbar()` itself) to get a light gray background on specific pages:

```r
page_navbar(
  title = "My App",
  nav_panel("Dashboard", class = "bslib-page-dashboard",
    card(...),
    card(...)
  ),
  nav_panel("About", "Plain white background here")
)
```

**Navigation helpers:**
- `nav_spacer()`: Adds spacing/pushes subsequent items right
- `nav_item()`: Adds arbitrary HTML (e.g., links) to navbar
- `nav_menu()`: Creates dropdown menus

### page_fillable()

A screen-filling page layout where content grows/shrinks to fit the browser window. This is the foundation for filling layouts in bslib.

**Key behavior:** Direct children of `page_fillable()` become fill items, meaning they'll resize to fill available space. This is ideal for dashboards where you want outputs to adapt to the viewport size. Typical usage wraps `layout_columns()` (or similar layout containers) and `card()` components as direct children.

**When to use:**
- Dashboards with plots/maps that should expand to fill the screen
- Single-page apps where all content should be visible without scrolling
- Apps with dynamic layouts that adapt to window size

Note: `page_sidebar()` and `page_navbar()` are built on top of `page_fillable()` and inherit its filling behavior by default.

## Basic Page Layouts

Beyond dashboard layouts, bslib provides traditional page functions:

- **`page_fluid()`**: Full-width page that resizes horizontally but scrolls vertically
- **`page_fixed()`**: Fixed-width page (940px default) that scrolls vertically
- **`page()`**: Most flexible option with manual control

These are useful when you don't want filling behavior and prefer traditional scrolling layouts.

## Filling vs Scrolling Behavior

### Filling Layouts (Default for Dashboard Pages)

Both `page_sidebar()` and `page_navbar()` default to `fillable = TRUE`, where outputs are encouraged to grow/shrink to fit the browser window.

**Benefits:**
- Content adapts to available screen space
- Professional dashboard appearance
- No scrolling needed when content fits

**Considerations:**
When content has large intrinsic minimum heights:
- Set `height` on cards that shouldn't resize
- Set `min_height` on cards that need a minimum size
- Set `max_height` on cards that shouldn't grow too large

**Example:**
```r
layout_columns(
  card(min_height = 200, max_height = 400, plotOutput("plot1")),
  card(height = 300, lorem::ipsum(10))
)
```

### Scrolling Layouts

For pages with many outputs or long content, set `fillable = FALSE` to disable filling behavior. This causes outputs to fall back to their default heights (~400px for plots) with page scrolling enabled. Pass `fillable = FALSE` directly to `page_sidebar()` or `page_navbar()`.

**For page_navbar(), use selective filling:**
```r
ui <- page_navbar(
  title = "Mixed Layout",
  fillable = c("Overview", "Analysis"),  # Only these pages fill
  nav_panel("Overview", ...),      # Fills viewport
  nav_panel("Analysis", ...),      # Fills viewport
  nav_panel("Details", ...)        # Scrolls normally
)
```

## Mobile Considerations

By default, filling layout is disabled on mobile devices to prevent awkward resizing on small screens. Set `fillable_mobile = TRUE` on `page_sidebar()` or `page_navbar()` to enable filling on mobile.

**Best practices for mobile:**
- Use `min_height` on cards to prevent excessive shrinking
- Sidebars collapse by default on mobile (configurable via `sidebar(open = ...)`)
- Test responsive breakpoints using browser dev tools
- Consider using `layout_column_wrap()` for responsive multi-column layouts

## Production Best Practices

### Pin Bootstrap Version

Before deploying to production, hard-code the Bootstrap version to prevent breakage on updates. Pass `theme = bs_theme(version = 5)` to any page function. This ensures your app uses Bootstrap 5 (recommended for modern features) and won't break if bslib's default version changes.

### Theming

Pass a `bs_theme()` object to the `theme` parameter of any page function to customize appearance. See [theming.md](theming.md) for comprehensive theming guidance.

### Plot Styling

Use the `thematic` package to ensure plots match your theme. Call `thematic::thematic_shiny()` in your server function or `app.R` to automatically style `plotOutput()` to match your CSS theme colors.

### Performance Tips

- For apps with many outputs, consider using `fillable = FALSE` and letting users scroll
- Use `card(full_screen = TRUE)` to allow expanding individual visualizations
- Consider using `navset_card_tab()` to organize related outputs within a single card
- Profile your app with `profvis` to identify rendering bottlenecks
