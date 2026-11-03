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
- `async-tasks.md` - The flush cycle, ExtendedTask, mirai/future_promise/crew, and the hard rules for worker code
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

### `shiny-py-optimize`

Diagnose and fix performance problems in existing Shiny for Python (py-shiny) apps — slow startup, sluggish interactions, blocking operations, and apps that need to support more users. Mirrors `shiny-r-optimize`'s workflow (understand the complaint → read the app → measure → classify the bottleneck → fix cheapest-first → verify) with Python-specific mechanics: the single asyncio event loop, `@reactive.extended_task`, module-level caching (no `bindCache` equivalent), and polars/DuckDB lazy data loading.

**Organization**: SKILL.md provides the diagnostic workflow, a quick-wins triage scan, and a symptom-to-fix table. Reference files provide the depth:
- `diagnosis.md` - OpenTelemetry tracing (built into Shiny ≥ 1.6), py-spy profiling, timing checks, load testing with shinyloadtest, the single-process asyncio model, sticky sessions, and Connect/Posit Connect Cloud capacity knobs
- `reactive-graph.md` - Narrowing reactive dependencies: shared `@reactive.calc`, `req()`, `reactive.isolate()`, `@reactive.event()`, update loops and `reactive.value.freeze()`, a tested debounce helper (not built into py-shiny), timers and polling
- `caching.md` - What `@reactive.calc` does and doesn't cache; module-level `functools.lru_cache`/`cachetools`/`diskcache` patterns and their hard rules (key completeness, read-only results, per-process caches)
- `async-tasks.md` - Why blocking hurts every session, the `@reactive.extended_task` pattern and its hard rules, `asyncio.to_thread` for sync I/O, process pools for CPU-bound work
- `data-loading.md` - Process-scope loading (Core module scope; imported modules in Express, whose top level runs per session), polars/parquet/DuckDB lazy loading, databases, downloads and uploads
- `rendering-ui.md` - Output suspension via tabs, `@render.ui` alternatives, plot/table rendering costs (`@render.data_frame` over `@render.table`), perceived performance

**Resources** (sources used in developing this skill — useful starting points for optimization work):
- [Shiny for Python: Non-blocking operations](https://shiny.posit.co/py/docs/nonblocking.html) — the concurrency model, `ExtendedTask`, executor patterns
- [Shiny for Python: Reading data](https://shiny.posit.co/py/docs/reading-data.html) — eager vs lazy loading, polars/DuckDB/ibis guidance
- [Shiny for Python: Reactive patterns](https://shiny.posit.co/py/docs/reactive-patterns.html) — `req`/`isolate`/`event`/timers/polling
- [Shiny for Python: OpenTelemetry](https://shiny.posit.co/py/docs/opentelemetry.html) — built-in tracing of reactive execution
- [Shiny for Python: Self-hosted deployments](https://shiny.posit.co/py/get-started/deploy-on-prem.html) — sticky sessions, why not multi-worker Gunicorn/uvicorn
- [py-shiny issue #335](https://github.com/posit-dev/py-shiny/issues/335) — `uvicorn --workers > 1` breaks Shiny (Joe Cheng)
- [py-shiny issue #564](https://github.com/posit-dev/py-shiny/issues/564) — debounce/throttle feature request; [Joe Cheng's `ratelimit.py` gist](https://gist.github.com/jcheng5/427de09573816c4ce3a8c6ec1839e7c0) is the reference debounce implementation
- [shinyloadtest (TypeScript rewrite)](https://github.com/posit-dev/shinyloadtest) — record/replay load testing for any Shiny app, including Python
- [Managing long-running operations in Shiny (Joe Cheng, 2024)](https://opensource.posit.co/resources/videos/2024-05-15_joe-cheng-managing-long-running-operations-in-shiny-posit/)
- [Building production-ready dashboards in Shiny for Python (Daniel Chen, SciPy 2025)](https://opensource.posit.co/resources/videos/2025-08-04_daniel-chen-shiny-for-python-building-production-ready-dashboards-in-python-scipy-2025/)
- [Shiny Express in depth](https://shiny.posit.co/py/docs/express-in-depth.html) — shared objects, startup cost, per-session top-level execution

## Potential Skills

This category could include skills for:

- Shiny app architecture and best practices
- Reactive programming patterns
- UI/UX design for Shiny apps
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
