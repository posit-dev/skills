# Quarto Skills

Skills for Quarto document creation and publishing.

## Overview

This category contains skills that help with creating, styling, and publishing Quarto documents, presentations, websites, and PDFs. Skills support all major Quarto output formats.

## Available Skills

### `authoring`

Comprehensive guidance for Quarto document authoring. Write new Quarto documents with best practices and use Quarto-specific features like hashpipe syntax, cross-references, callouts, and extensions. See [detailed documentation below](#quarto-authoring-skill).

### `quarto-migration`

Guidance for migrating R Markdown ecosystem projects to Quarto. Convert R Markdown files, migrate bookdown/blogdown/xaringan/distill projects. See [detailed documentation below](#quarto-migration-skill).

### `brand-yml`

Create and use `_brand.yml` files for consistent branding across Quarto documents and Shiny applications. Use when working with brand styling, corporate identity, colors, fonts, or logos in Quarto projects.

**Organization**: Main skill file includes workflows and decision tree. Reference files provide framework-specific integration guides:
- `brand-yml-spec.md` - Complete brand.yml specification.
- `shiny-r.md` - Shiny for R integration with bslib.
- `shiny-python.md` - Shiny for Python integration with ui.Theme.
- `quarto.md` - Quarto integration for all formats (HTML, dashboards, RevealJS presentations, Typst PDFs, websites).

**Note**: This skill is also registered in the shiny category since brand.yml works across both Shiny and Quarto projects.

**Resources**:
- [brand.yml project](https://posit-dev.github.io/brand-yml/)
- [Quarto brand.yml docs](https://quarto.org/docs/authoring/brand.html)
- [Shiny for R brand.yml guide](https://rstudio.github.io/bslib/articles/brand-yml/)
- [Shiny for Python brand.yml docs](https://shiny.posit.co/py/api/core/ui.Theme.html#shiny.ui.Theme.from_brand)

## Potential Skills

This category could include skills for:

- Publishing workflows
- Extension development
- Template creation
- Multi-format output
- Parameterized reports
- Website and book publishing
- Presentation design

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new skills to this category. We encourage you to use [Anthropic's skill-creator](https://github.com/anthropics/skills) when building new skills.

## Resources

- [Quarto](https://quarto.org/)
- [Quarto brand.yml docs](https://quarto.org/docs/authoring/brand.html)
- [brand.yml project](https://posit-dev.github.io/brand-yml/)
- [Quarto extensions](https://quarto.org/docs/extensions/)

---

## Skills

### Quarto Authoring Skill

Comprehensive guidance for Quarto document authoring.

This skill provides best practices for writing Quarto documents (.qmd). It covers the full range of Quarto authoring features including code cells, cross-references, figures, tables, citations, callouts, diagrams, and more.

#### When to Use This Skill

- Writing new Quarto documents with best practices.
- Understanding Quarto's cell options syntax (comment symbol + `|`).
- Setting up cross-references for figures, tables, sections, and equations.
- Using Quarto-specific features like callouts, divs, and spans.
- Configuring YAML front matter for documents and projects.
- Finding and using Quarto extensions.

#### Maintenance

- Review skill content when new Quarto versions are released.
- Check the [Quarto changelog](https://github.com/quarto-dev/quarto-cli/blob/main/news/) for breaking changes and new features.
- Cross-check syntax examples against [Quarto Documentation](https://quarto.org/).
- Update examples to reflect current best practices.
- Remove deprecated syntax or features.

#### Skills Reference Documentation

##### Quarto Features

| Reference                                                             | Description                                      |
| --------------------------------------------------------------------- | ------------------------------------------------ |
| [code-cells.md](quarto-authoring/references/code-cells.md)                   | Hashpipe syntax, execution options, code display |
| [cross-references.md](quarto-authoring/references/cross-references.md)       | Labels, prefixes, all reference types            |
| [figures.md](quarto-authoring/references/figures.md)                         | Figures, subfigures, layouts, lightbox           |
| [tables.md](quarto-authoring/references/tables.md)                           | Pipe tables, grid tables, styling                |
| [citations.md](quarto-authoring/references/citations.md)                     | Bibliography, CSL, footnotes                     |
| [callouts.md](quarto-authoring/references/callouts.md)                       | Callout types, appearance, collapsible           |
| [diagrams.md](quarto-authoring/references/diagrams.md)                       | Mermaid, Graphviz/DOT diagrams                   |
| [layout.md](quarto-authoring/references/layout.md)                           | Column classes, margin content                   |
| [shortcodes.md](quarto-authoring/references/shortcodes.md)                   | Built-in shortcodes                              |
| [conditional-content.md](quarto-authoring/references/conditional-content.md) | Format-specific content                          |
| [divs-and-spans.md](quarto-authoring/references/divs-and-spans.md)           | Fenced divs, spans, raw blocks                   |
| [yaml-front-matter.md](quarto-authoring/references/yaml-front-matter.md)     | Document and project YAML                        |
| [extensions.md](quarto-authoring/references/extensions.md)                   | Using and finding extensions                     |

#### External Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Quarto CLI Code](https://github.com/quarto-dev/quarto-cli)
- [Community Extensions List](https://m.canouil.dev/quarto-extensions/)

#### Authors

- [Mickaël CANOUIL](https://github.com/mcanouil)

### Quarto Migration Skill

Guidance for migrating R Markdown ecosystem projects to Quarto.

This skill covers converting R Markdown (.Rmd) documents and migrating bookdown, blogdown, xaringan, and distill projects to Quarto. It includes common migration patterns such as option naming changes (dots to dashes), cross-reference prefix changes, and YAML structure updates.

#### When to Use This Skill

- Converting R Markdown (.Rmd) files to Quarto (.qmd).
- Migrating bookdown projects to Quarto book format.
- Migrating blogdown sites to Quarto websites.
- Converting xaringan slides to Quarto RevealJS.
- Migrating distill articles or blogs to Quarto.

#### Maintenance

- Review skill content when new Quarto versions are released.
- Check the [Quarto changelog](https://github.com/quarto-dev/quarto-cli/blob/main/news/) for breaking changes affecting migration paths.
- Cross-check migration steps against [Quarto Documentation](https://quarto.org/).
- Update examples to reflect current best practices.

#### Skills Reference Documentation

| Reference                                              | Description                |
| ------------------------------------------------------ | -------------------------- |
| [rmarkdown.md](quarto-migration/references/rmarkdown.md)     | R Markdown to Quarto       |
| [bookdown.md](quarto-migration/references/bookdown.md)       | bookdown to Quarto         |
| [xaringan.md](quarto-migration/references/xaringan.md)       | xaringan to RevealJS       |
| [distill.md](quarto-migration/references/distill.md)         | distill to Quarto          |
| [blogdown.md](quarto-migration/references/blogdown.md)       | blogdown to Quarto website |

#### External Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)

#### Authors

- [Mickaël CANOUIL](https://github.com/mcanouil)
