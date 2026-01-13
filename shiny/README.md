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

### `shiny-react`

Build Shiny applications with React frontends using the `@posit/shiny-react` library. Use when creating modern, component-based UIs with React while leveraging Shiny's reactive backend (R or Python).

**Organization**: Main skill file covers quick start and essential patterns. Reference files provide deep dives:
- `typescript-api.md` - Complete TypeScript API for hooks and components
- `r-backend.md` - R Shiny backend patterns with render_json and post_message
- `python-backend.md` - Python Shiny backend patterns
- `shadcn-setup.md` - shadcn/ui and Tailwind CSS integration guide
- `internals.md` - How shiny-react works under the hood (registries, bindings)

**Key Features**:
- `useShinyInput` / `useShinyOutput` hooks for bidirectional communication
- `useShinyMessageHandler` for server-to-client messages
- `ImageOutput` component for Shiny plots
- shadcn/ui integration with Tailwind CSS
- Support for both R and Python Shiny backends

**Resources**:
- [shiny-react GitHub](https://github.com/wch/shiny-react)
- [create-shiny-react-app](https://www.npmjs.com/package/create-shiny-react-app)
- [shadcn/ui](https://ui.shadcn.com/)

## Potential Skills

This category could include skills for:

- Shiny app architecture and best practices
- Reactive programming patterns
- UI/UX design for Shiny apps
- Performance optimization
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
