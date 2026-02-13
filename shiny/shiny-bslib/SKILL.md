---
name: shiny-bslib
description: Build modern Shiny dashboards and applications using bslib (Bootstrap 5). Use this skill when creating or updating Shiny apps with modern layouts, themes, and components. Covers page layouts (page_sidebar, page_navbar, page_fillable), grid systems (layout_columns, layout_column_wrap), cards, value boxes, navigation (navset functions), sidebars, filling layouts, theming (bs_theme, Bootswatch themes), UI components (accordions, tooltips, popovers, toasts), and special inputs. This skill assumes familiarity with basic Shiny and focuses on modern bslib features for Bootstrap 5 dashboards.
---

# Modern Shiny Apps with bslib

Build professional, modern Shiny dashboards and applications using bslib's Bootstrap 5 components and layouts.

## Overview

bslib is a modern UI toolkit for Shiny that provides:
- **Dashboard layouts**: Page-level functions for organizing apps (`page_sidebar`, `page_navbar`, `page_fillable`)
- **Grid systems**: Flexible layouts for arranging content (`layout_columns`, `layout_column_wrap`)
- **Cards**: Primary containers for organizing outputs with full-screen support
- **Value boxes**: Specialized components for displaying KPIs and metrics
- **Navigation**: Multi-page and tabbed interfaces (`navset_*` functions)
- **Sidebars**: Flexible sidebar layouts at page and component levels
- **Filling layouts**: System for creating responsive, viewport-filling applications
- **Theming**: Powerful customization with Bootstrap 5 variables and Sass
- **UI components**: Accordions, tooltips, popovers, and toasts
- **Special inputs**: Modern input widgets (switches, dark mode, task buttons, code editor)

This skill focuses on modern features for Bootstrap 5 and assumes basic Shiny knowledge.

## When to Use This Skill

Use this skill when:
- Building new Shiny dashboards or applications
- Modernizing existing Shiny apps with bslib
- Creating responsive, professional-looking interfaces
- Implementing custom themes or dark mode
- Organizing complex multi-page applications
- Adding modern UI components to Shiny apps

## Quick Start Guide

### Basic Dashboard Structure

**Single-page dashboard:**
```r
library(shiny)
library(bslib)

ui <- page_sidebar(
  title = "My Dashboard",
  theme = bs_theme(version = 5, bootswatch = "flatly"),
  sidebar = sidebar(
    selectInput("variable", "Variable", choices = names(mtcars))
  ),
  card(
    full_screen = TRUE,
    card_header("Plot"),
    plotOutput("plot")
  )
)

server <- function(input, output) {
  output$plot <- renderPlot({
    hist(mtcars[[input$variable]], main = input$variable)
  })
}

shinyApp(ui, server)
```

**Multi-page dashboard:**
```r
ui <- page_navbar(
  title = "Analytics Platform",
  theme = bs_theme(version = 5),
  nav_panel("Overview", overview_ui),
  nav_panel("Analysis", analysis_ui),
  nav_panel("Reports", reports_ui)
)
```

### Essential Patterns

**Value boxes for KPIs:**
```r
layout_column_wrap(
  width = 1/4,
  fill = FALSE,
  value_box(title = "Users", value = "1,234", theme = "primary"),
  value_box(title = "Revenue", value = "$56K", theme = "success"),
  value_box(title = "Growth", value = "+18%", theme = "info")
)
```

**Cards with full-screen:**
```r
card(
  full_screen = TRUE,  # Always enable for visualizations
  card_header("Sales Trend"),
  plotOutput("sales_plot")
)
```

**Responsive grid layouts:**
```r
layout_column_wrap(
  width = "300px",  # Auto-adjusts columns based on screen size
  card(...),
  card(...),
  card(...)
)
```

## Core Concepts

### Page-Level Layouts

The foundation of your app structure. Choose based on your needs:

- **`page_sidebar()`** - Single-page dashboard with sidebar
- **`page_navbar()`** - Multi-page app with top navigation
- **`page_fillable()`** - Viewport-filling layout for custom arrangements
- **`page_fluid()`** - Scrolling layout (for long-form content)

**→ See [page-layouts.md](references/page-layouts.md) for detailed guidance**

### Grid Systems

Arrange cards, value boxes, and other UI elements in responsive grids:

- **`layout_column_wrap()`** - Uniform grid with auto-wrapping (recommended for most cases)
- **`layout_columns()`** - 12-column Bootstrap grid with precise control

**→ See [grid-layouts.md](references/grid-layouts.md) for detailed guidance**

### Cards

The primary container for organizing dashboard content:

- Visual grouping with borders and padding
- Full-screen expansion for visualizations
- Support for headers, footers, and multiple body sections
- Integration with filling layouts

**Key practice:** Always use `full_screen = TRUE` for cards containing plots, maps, or tables.

**→ See [cards.md](references/cards.md) for detailed guidance**

### Value Boxes

Specialized components for displaying key metrics and KPIs:

- Prominent value display
- Optional icons or sparklines
- Built-in theming
- Perfect for dashboard headers

**→ See [value-boxes.md](references/value-boxes.md) for detailed guidance**

### Navigation

Organize content into pages and tabs:

- **Page-level**: `page_navbar()` for multi-page apps
- **Component-level**: `navset_*()` functions for tabbed content
- **Styles**: underline, tab, pill, card variants

**→ See [navigation.md](references/navigation.md) for detailed guidance**

### Sidebars

Organize inputs and controls:

- **Page-level**: `page_sidebar()` or `page_navbar(sidebar = ...)`
- **Component-level**: `layout_sidebar()` within cards
- Conditional content and dynamic open/close
- Accordions for grouping inputs

**→ See [sidebars.md](references/sidebars.md) for detailed guidance**

### Filling Layouts

Understanding the fill system is crucial for modern bslib apps:

- **Fillable containers**: Can make children grow/shrink
- **Fill items**: Elements that resize to match container
- **Fill carriers**: Elements that are both fillable and fill items

**Key insight:** Fill activates when containers have defined heights. Used for viewport-filling dashboards.

**→ See [filling.md](references/filling.md) for detailed guidance**

### Theming

Customize appearance with Bootstrap 5 variables:

- **`bs_theme()`**: Core theming function
- **Bootswatch themes**: Pre-built professional themes
- **Custom colors and fonts**: Main colors (`bg`, `fg`, `primary`) and Google Fonts
- **Sass variables**: Fine-grained control over Bootstrap styling
- **Dynamic theming**: Runtime theme switching (dark mode)

**→ See [theming.md](references/theming.md) for detailed guidance**

### UI Components

Additional components for rich interfaces:

- **Accordions**: Collapsible sections for organizing content
- **Tooltips**: Hover-triggered contextual help
- **Popovers**: Click-triggered interactive containers
- **Toasts**: Temporary notification messages

**→ See [components.md](references/components.md) for detailed guidance**

### Special Inputs

Modern input widgets beyond standard Shiny inputs:

- **`input_switch()`**: Toggle switch (modern checkbox alternative)
- **`input_dark_mode()`**: Dark mode toggle with theme switching
- **`input_task_button()`**: Button for long-running operations
- **`input_code_editor()`**: Code editor with syntax highlighting
- **`input_submit_textarea()`**: Textarea with explicit submission

**→ See [inputs.md](references/inputs.md) for detailed guidance**

## Common Workflows

### Building a Dashboard from Scratch

1. **Choose page layout** based on structure needs (single-page vs multi-page)
2. **Add theme** with `bs_theme()` (consider Bootswatch for quick start)
3. **Create sidebar** with inputs for filtering/controls
4. **Add value boxes** at the top for key metrics (set `fill = FALSE` on container)
5. **Arrange cards** with `layout_column_wrap()` or `layout_columns()`
6. **Enable full-screen** on all visualization cards
7. **Test responsiveness** at multiple screen sizes
8. **Add theming for plots** with `thematic::thematic_shiny()`

### Modernizing an Existing App

1. **Replace page function**: Change `fluidPage()` to `page_sidebar()` or `page_navbar()`
2. **Wrap outputs in cards**: Add `card()` around outputs with `full_screen = TRUE`
3. **Update grid system**: Replace `fluidRow()`/`column()` with `layout_columns()`
4. **Add theme**: Include `theme = bs_theme(version = 5)`
5. **Group metrics**: Convert key metrics to `value_box()` components
6. **Organize inputs**: Use accordions in sidebars for cleaner organization
7. **Test filling behavior**: Ensure layouts work with new fill system

### Creating Custom Themes

1. **Start with Bootswatch**: Choose a theme close to desired look
2. **Customize main colors**: Adjust `bg`, `fg`, `primary` via `bs_theme_update()`
3. **Set fonts**: Use `font_google()` for typography
4. **Fine-tune variables**: Override specific Bootstrap Sass variables
5. **Add custom rules**: Use `bs_add_rules()` for additional styling
6. **Enable plots theming**: Call `thematic::thematic_shiny()`
7. **Test with `bs_themer()`**: Use interactive widget during development
8. **Extract to file**: Move theme configuration to separate `theme.R` file

### Implementing Dark Mode

1. **Define both themes**: Create light and dark `bs_theme()` objects
2. **Add toggle**: Include `input_dark_mode()` in sidebar or navbar
3. **Switch themes**: Use `session$setCurrentTheme()` reactively
4. **Enable plot theming**: Use `thematic::thematic_shiny(font = "auto")`
5. **Test custom styles**: Ensure custom CSS uses Sass variables for adaptability
6. **Consider persistence**: Save user preference with cookies/browser storage

### Organizing Multi-Page Apps

1. **Use `page_navbar()`**: Create top-level navigation structure
2. **Decide on sidebar approach**: Global sidebar or page-specific sidebars
3. **Create nav panels**: One `nav_panel()` per page
4. **Use nav menus**: Group related pages in dropdowns with `nav_menu()`
5. **Add nav items**: Include links, buttons with `nav_item()`
6. **Set fillable pages**: Use `fillable` parameter to control which pages fill viewport
7. **Add page IDs**: Enable tracking active page with `id` parameter
8. **Implement conditional logic**: Show/hide content based on active page

## Key Principles

### Always Enable Full-Screen for Visualizations

Users greatly value the ability to expand plots, maps, and tables:

```r
card(
  full_screen = TRUE,  # Always include
  card_header("Plot"),
  plotOutput("plot")
)
```

### Use Modern Layout Functions

Prefer `layout_column_wrap()` and `layout_columns()` over legacy `fluidRow()`/`column()`:

**Modern approach:**
```r
layout_column_wrap(
  width = 1/2,
  card(...),
  card(...)
)
```

### Wrap Everything in Cards

Cards provide structure, full-screen capability, and visual organization:

```r
# Good
card(full_screen = TRUE, card_header("Title"), plotOutput("plot"))

# Avoid
plotOutput("plot")
```

### Set fill = FALSE for Value Boxes

Prevent value boxes from expanding excessively:

```r
layout_column_wrap(
  width = 1/3,
  fill = FALSE,  # Important!
  value_box(...),
  value_box(...),
  value_box(...)
)
```

### Use Responsive Column Widths

Let layouts adapt to screen size:

```r
layout_column_wrap(
  width = "250px",  # Auto-adjusts columns
  ...
)
```

### Group Related Inputs with Accordions

Organize sidebar inputs for clarity:

```r
sidebar(
  accordion(
    accordion_panel("Essential Filters", ...),
    accordion_panel("Advanced Options", ...)
  )
)
```

### Pin Bootstrap Version for Production

Prevent breakage from version updates:

```r
page_navbar(
  theme = bs_theme(version = 5),
  ...
)
```

### Use Reactive Expressions for Shared Data

Avoid redundant computations:

```r
filtered_data <- reactive({
  data |> filter(category == input$category)
})

# Multiple outputs use filtered_data()
```

## Reference Files

For detailed information on specific topics:

- **[page-layouts.md](references/page-layouts.md)** - Page-level layout functions and patterns
- **[grid-layouts.md](references/grid-layouts.md)** - Multi-column grid systems
- **[cards.md](references/cards.md)** - Card components and features
- **[value-boxes.md](references/value-boxes.md)** - Value boxes for metrics and KPIs
- **[navigation.md](references/navigation.md)** - Navigation containers and patterns
- **[sidebars.md](references/sidebars.md)** - Sidebar layouts and organization
- **[filling.md](references/filling.md)** - Understanding fillable containers and fill items
- **[theming.md](references/theming.md)** - Complete theming guide
- **[components.md](references/components.md)** - Accordions, tooltips, popovers, toasts
- **[inputs.md](references/inputs.md)** - Special bslib input widgets
- **[best-practices.md](references/best-practices.md)** - Patterns, tips, and common gotchas

## Additional Resources

- **bslib website**: https://rstudio.github.io/bslib/llms.txt
- **Bootswatch themes**: https://bootswatch.com/
- **Bootstrap 5 documentation**: https://getbootstrap.com/docs/5.0/
- **Google Fonts**: https://fonts.google.com/
- **Font pairings**: https://fontpair.co/
- **thematic package**: For theming R plots to match CSS

## Getting Help

When working with bslib:

1. **Check reference files** in this skill for detailed guidance
2. **Use R help**: `?bslib::page_sidebar`, `?bslib::card`, etc.
3. **Browse examples**: `bslib::` package includes many examples
4. **Interactive exploration**: Use `bs_theme_preview()` and `bs_themer()`
5. **Read articles**: https://rstudio.github.io/bslib/articles/
6. **Community support**: Posit Community forum with `bslib` tag
