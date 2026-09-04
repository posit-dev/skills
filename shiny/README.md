# Shiny Skills

Skills for Shiny app development in both R and Python.

## Overview

This category contains skills that help with building, styling, and deploying Shiny applications. Skills support both Shiny for R (using bslib) and Shiny for Python frameworks.

## Available Skills

### `brand-yml`

Create and use `_brand.yml` files for consistent branding across Shiny applications (R and Python) and Quarto documents. Use when working with brand styling, corporate identity, colors, fonts, or logos.

**Organization**: Main skill file includes workflows and decision tree. Reference files provide framework-specific integration guides:
- `brand-yml-spec.md` - Complete brand.yml specification
- `shiny-r.md` - Shiny for R integration with bslib
- `shiny-python.md` - Shiny for Python integration with ui.Theme
- `quarto.md` - Quarto integration for all formats

**Note**: This skill is also registered in the quarto category since brand.yml works across both Shiny and Quarto projects.

**Resources**:
- [brand.yml project](https://posit-dev.github.io/brand-yml/)
- [Shiny for R brand.yml guide](https://rstudio.github.io/bslib/articles/brand-yml/)
- [Shiny for Python brand.yml docs](https://shiny.posit.co/py/api/core/ui.Theme.html#shiny.ui.Theme.from_brand)
- [Quarto brand.yml docs](https://quarto.org/docs/authoring/brand.html)

### `shiny-bslib`

Build modern Shiny dashboards and applications using bslib with Bootstrap 5. Use when creating or updating Shiny apps with modern layouts, themes, and components.

**Organization**: Comprehensive reference skill with main SKILL.md providing overview and workflows, plus 14 detailed reference files:
- `migration.md` - Legacy Shiny to modern bslib migration guide
- `page-layouts.md` - Page-level layout functions (page_sidebar, page_navbar, page_fillable)
- `grid-layouts.md` - Multi-column grid systems (layout_columns, layout_column_wrap)
- `cards.md` - Card components with full-screen support
- `value-boxes.md` - KPI and metrics display components
- `navigation.md` - Navigation containers and multi-page patterns
- `sidebars.md` - Sidebar layouts and organization
- `filling.md` - Fillable containers and fill items system
- `theming.md` - Basic theming (colors, fonts, Bootswatch). See shiny-bslib-theming for advanced theming
- `accordions.md` - Collapsible sections and sidebar organization
- `tooltips-popovers.md` - Hover tooltips and click-triggered popovers
- `toasts.md` - Temporary notification messages
- `inputs.md` - Special bslib input widgets (switches, dark mode, task buttons, code editor, submit textarea)
- `best-practices.md` - bslib-specific patterns and common gotchas

**Key features covered**:
- Dashboard layouts (single-page and multi-page)
- Responsive grid systems
- Card-based content organization
- Value boxes for KPIs
- Comprehensive theming system
- Filling vs scrolling layouts
- Modern UI components
- Mobile and responsive design

**Resources**:
- [bslib website](https://rstudio.github.io/bslib/)
- [bslib articles](https://rstudio.github.io/bslib/articles/)
- [Bootstrap 5 documentation](https://getbootstrap.com/docs/5.0/)
- [Bootswatch themes](https://bootswatch.com/)

### `shiny-bslib-theming`

Comprehensive theming for Shiny apps using bslib and Bootstrap 5. Use when customizing app appearance beyond basic Bootswatch themes — covers bs_theme(), custom colors, typography, Bootstrap Sass variables, custom Sass/CSS rules, dark mode, dynamic theming, and plot theming with the thematic package.

**Organization**: SKILL.md covers core theming workflow (bs_theme, Bootswatch, colors, fonts, Sass variables, low-level theming functions, interactive theming tools, plot theming), plus 2 reference files:
- `sass-and-css-variables.md` - Bootstrap's two-layer variable system, CSS custom properties, utility classes
- `dark-mode.md` - Color modes, dark mode (input_dark_mode, toggle_dark_mode), dynamic theming, component compatibility

**Resources**:
- [bslib theming articles](https://rstudio.github.io/bslib/articles/theming/)
- [Bootstrap 5 Sass variables](https://rstudio.github.io/bslib/articles/bs5-variables/)
- [Bootswatch themes](https://bootswatch.com/)
- [thematic package](https://rstudio.github.io/thematic/)

### `shiny-reactivity`

Design and debug Shiny's reactive graph in R. Use when choosing between `reactive()`, `observe()`, `observeEvent()`, and `eventReactive()`; managing state with `reactiveValues`; controlling when things run with `req()`, `bindEvent()`, `bindCache()`, or `debounce()`; or debugging reactivity with reactlog, tracebacks, and profvis.

**Organization**: Single self-contained SKILL.md covering reactive-graph design patterns, common anti-patterns (the observer-writes-reactiveValues trap), and a debugging workflow.

**Resources**:
- [Mastering Shiny: Reactivity](https://mastering-shiny.org/reactivity-intro.html)
- [reactlog package](https://rstudio.github.io/reactlog/)

### `shiny-testing`

Test Shiny apps in R across three layers — pure functions with testthat, reactive logic with `shiny::testServer()`, and end-to-end with shinytest2 (`AppDriver`, snapshots). Use when writing or fixing tests for a Shiny app or module, testing reactives without a browser, setting up shinytest2, or deciding what to test where.

**Organization**: Single self-contained SKILL.md organized by the three testing layers, cheapest first, with guidance on what to test where.

**Resources**:
- [shinytest2 package](https://rstudio.github.io/shinytest2/)
- [Mastering Shiny: Testing](https://mastering-shiny.org/scaling-testing.html)

### `shiny-for-agents`

Drive, inspect, and debug a running Shiny app (R and Python) with a browser tool (Playwright or agent-browser). Use when launching a Shiny app for inspection, driving its UI without flaky sleeps, reading server-side errors the browser can't see, or authoring an app to be legible to agents.

**Organization**: SKILL.md explains Shiny's split-runtime model and agent-driving workflow, plus helper scripts:
- `scripts/launch_app_dev.R` - Launch a Shiny app in a dev-friendly mode for inspection
- `scripts/wait_for_shiny_idle.js` - Wait on `shiny:busy`/`shiny:idle` events instead of fixed sleeps

**Resources**:
- [Shiny JavaScript events](https://shiny.posit.co/r/articles/build/js-events/)

## Potential Skills

This category could include skills for:

- Shiny app architecture and best practices
- UI/UX design for Shiny apps
- Performance optimization
- Deployment strategies
- Module development
- Extension creation

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new skills to this category. We encourage you to use [Anthropic's skill-creator](https://github.com/anthropics/skills) when building new skills.

## Resources

- [Shiny for R](https://shiny.posit.co/r/)
- [Shiny for Python](https://shiny.posit.co/py/)
- [bslib package](https://rstudio.github.io/bslib/)
- [brand.yml project](https://posit-dev.github.io/brand-yml/)
