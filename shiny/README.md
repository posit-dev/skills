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

### `shiny-r-optimize`

Diagnose and fix performance problems in existing Shiny for R apps — slow startup, sluggish interactions, blocking operations, and apps that need to support more users. Use when an app is slow, hangs, recomputes too much, or must scale beyond prototyping.

**Organization**: SKILL.md provides the diagnostic workflow (understand the complaint → read the app → measure → classify the bottleneck → fix cheapest-first → verify), a quick-wins triage scan, and a symptom-to-fix table. Reference files provide the depth:
- `diagnosis.md` - Profiling with profvis/debrief, reactive-graph inspection with reactlog, micro-benchmarks (bench), load testing (shinyloadtest/shinycannon), the multi-process model, and Connect/Posit Connect Cloud capacity knobs
- `reactive-graph.md` - Narrowing reactive dependencies: shared reactives, req(), isolate(), bindEvent(), freezeReactiveValue(), debounce()/throttle(), timers
- `caching.md` - bindCache() keys and scopes, caching data vs. plots, memoise(), cachem backends, deployment caveats
- `async-tasks.md` - The flush cycle, ExtendedTask, future_promise/mirai/crew, and the hard rules for worker code
- `data-loading.md` - Load-once patterns, fast file formats (fread/feather/parquet/DuckDB), pool + dbplyr, downloads and uploads
- `rendering-ui.md` - Output suspension via tabs, gating with req(), renderUI alternatives, plot/table rendering costs, perceived performance

**Resources** (sources used in developing this skill — useful starting points for optimization work):
- [Shiny performance articles](https://shiny.posit.co/r/articles/improve/)
- [Shiny: Non-blocking operations (async)](https://shiny.posit.co/r/articles/improve/nonblocking/)
- [Shiny: Caching with bindCache](https://shiny.posit.co/r/articles/improve/caching/)
- [Mastering Shiny: Performance](https://mastering-shiny.org/performance.html) and [Scaling](https://mastering-shiny.org/scaling-general.html)
- [promises documentation](https://rstudio.github.io/promises/)
- [profvis](https://rstudio.github.io/profvis/) and [debrief](https://r-lib.github.io/debrief/) for profiling
- [reactlog](https://rstudio.github.io/reactlog/) for reactive-graph inspection
- [shinyloadtest](https://rstudio.github.io/shinyloadtest/) and [shinycannon](https://github.com/rstudio/shinycannon) for load testing
- [mirai](https://mirai.r-lib.org/) and [crew](https://wlandau.github.io/crew/) for async worker backends
- [DuckDB R client](https://r.duckdb.org/) and [pool](https://rstudio.github.io/pool/) for data access
- [Posit Connect scheduler settings](https://docs.posit.co/connect/admin/appendix/off-host-scheduler/)
- [Managing long-running operations in Shiny (Joe Cheng, 2024)](https://opensource.posit.co/resources/videos/2024-05-15_joe-cheng-managing-long-running-operations-in-shiny-posit/)

## Potential Skills

This category could include skills for:

- Shiny app architecture and best practices
- Reactive programming patterns
- UI/UX design for Shiny apps
- ~~Performance optimization~~ (covered by `shiny-r-optimize`)
- Testing Shiny applications
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
