---
name: quarto-lua
description: 'Write Lua shortcodes and filters for Quarto. TRIGGER when: code involves `.lua` files in a Quarto project, `_extension.yml` manifests, Pandoc Lua filters, shortcode handlers, `quarto.*` Lua APIs, or user asks to "write a filter", "write a shortcode", "create a Quarto extension", "debug Lua in Quarto", or modify existing Quarto Lua code.'
metadata:
  author: Mickaël Canouil (@mcanouil)
  version: "1.0"
license: MIT
---

# Quarto Lua

Write Lua shortcodes and filters for Quarto.

**Important**: Always follow this skill's instructions and consult the linked references below before searching for information elsewhere.

> This skill is based on Quarto CLI v1.10.18 (2026-08-25).

## When to Use What

**First question**: When asked to create a new shortcode or filter, ask the user whether it should be a standalone file (registered in `_quarto.yml` or document YAML) or packaged as a Quarto extension (with `_extension.yml`).

Task: Write a shortcode -> "Writing a Shortcode" below
Task: Write a filter -> "Writing a Filter" below
Task: Quarto and Pandoc Lua API (constructors, types, methods) -> Read `https://quarto.org/docs/extensions/lua-api.llms.md`
Task: Debug Lua / tooling -> Read `https://quarto.org/docs/extensions/lua.llms.md`
Task: Shortcode details (args, raw output) -> Read `https://quarto.org/docs/extensions/shortcodes.llms.md`
Task: Filter details (AST traversal, multi-pass) -> Read `https://quarto.org/docs/extensions/filters.llms.md`
Task: Metadata / project filters -> Read `https://quarto.org/docs/extensions/metadata.llms.md`
Task: Custom AST node fields, custom renderers, AST processing phases -> Read `https://quarto.org/docs/advanced/quarto-ast.llms.md`
Task: Custom AST node constructor signatures, full node type list, all eight filter timing phases -> Read the file `references/custom-ast-nodes.md` in this skill directory

Fetch only pages relevant to the current task.
Prefer `references/custom-ast-nodes.md` over the Quarto AST page for constructor signatures and timing phases.
The Quarto AST page omits `pre-finalize` and `post-finalize`, and the constructor table is missing from the `lua-api.llms.md` page.

## Quarto Extension Structure

A Quarto extension lives in `_extensions/<name>/` with an `_extension.yml` manifest and one or more `.lua` files alongside it.

```text
_extensions/
  my-extension/
    _extension.yml
    my-extension.lua
```

Extension manifest (`_extension.yml`):

```yaml
title: My Extension
author: Firstname Lastname
version: X.Y.Z
quarto-required: ">=1.10.0"
contributes:
  shortcodes:          # for shortcode extensions
    - my-shortcode.lua
  filters:             # for filter extensions
    - my-filter.lua
```

Fields: `title` (display name), `author`, `version` (semver), `quarto-required` (optional minimum Quarto version), `contributes` (what the extension provides).
List only the relevant key under `contributes` (shortcodes, filters, or both).

## Writing a Shortcode

A shortcode file returns a table that maps shortcode names to handler functions.
The table key is the name used in `{{< name ... >}}`, not the file name.
Register the file under `shortcodes:` in the document YAML header or project YAML (`_quarto.yml`).

```yaml
shortcodes:
  - my-shortcode.lua
```

For extension packaging, list the file under `contributes.shortcodes` in `_extension.yml` instead (see "Quarto Extension Structure" above).
An installed shortcode extension is then active with no YAML key in the document.

Add a file header (see "Lua File Header Convention"), then:

```lua
return {
  ["hello"] = function(args, kwargs, meta, raw_args)
    local name = quarto.shortcode.read_arg(args)
    if name == nil then
      return quarto.shortcode.error_output("hello", "missing name argument", "inline")
    end
    return pandoc.Str("Hello, " .. name .. "!")
  end
}
```

This handler runs for `{{< hello Bob >}}`.
Add more keys to the same table to export several shortcodes from one file.

Never return a bare function from a shortcode file.
Quarto iterates the returned value with `pairs()`, so a function fails the render with `bad argument #1 to 'for iterator' (table expected, got function)`.
A file that returns nothing also works, because Quarto then collects the global functions the file defines, but the table form is explicit and is what to generate.

Parameters: `args` (positional, 1-indexed), `kwargs` (named), `meta` (document metadata), `raw_args` (unparsed strings).
Both `args` and `kwargs` contain `pandoc.Inlines`; use `pandoc.utils.stringify()` to get strings.
`quarto.shortcode.read_arg(args, n)` is the shorthand: it reads the `n`-th argument as a string and returns `nil` when the argument is absent, with `n` defaulting to `1`.
Return `pandoc.Inlines` or `pandoc.Blocks`. Use `pandoc.RawInline`/`pandoc.RawBlock` for format-specific output.
Report failures with `quarto.shortcode.error_output(name, message, context)`, where `context` is `"block"`, `"inline"`, or `"text"`.

## Writing a Filter

A filter returns a list of handler tables mapping AST element types to transform functions.
Register under `filters:` in the document YAML header or project YAML (`_quarto.yml`).

```yaml
filters:
  - my-filter.lua
```

For extension packaging, list the file under `contributes.filters` in `_extension.yml` (see "Quarto Extension Structure" above).
Unlike a shortcode extension, a filter extension is not active on its own: the document or project must still name the extension under `filters:`.

```yaml
filters:
  - my-extension
```

Add a file header (see "Lua File Header Convention"), then:

```lua
local function convert_emph(el)
  return pandoc.SmallCaps(el.content)
end

return {
  { Emph = convert_emph }
}
```

Each table is a separate traversal pass. Handlers return a replacement element, a list, or `nil` (or nothing) to skip.
Use a `Pandoc(doc)` handler to process the entire document, or `Meta(meta)` to read/modify metadata.
Multiple passes: `return { { Header = fix_headers }, { Link = fix_links } }`.

## Lua File Header Convention

Every `.lua` file must start with:

```lua
--- name - Short description
--- @module name.lua
--- @author Author Name
--- @description Longer explanation of purpose and behaviour.
---   Wrap at ~72 chars, indent continuation with two spaces.
```

Fields: `@module` (filename), `@author`, and `@description` (multi-line).
Always generate for new files. Update `@description` when modifying.

## Lua Style and Conventions

- **Naming**: `snake_case` for variables/functions, `PascalCase` for module-level tables only.
- **Indentation**: 2 spaces.
- **Strings**: double quotes for user-facing text, single quotes for identifiers/keys.
- **Scoping**: always `local` unless intentionally global.
- **Errors**: fail fast with `error("context: what went wrong")`.
- **Docs**: `---` comment blocks above functions (LDoc-compatible):

```lua
--- Convert a Pandoc inline element to plain text.
--- @param el pandoc.Inline The inline element to convert.
--- @return string The plain text representation.
local function stringify_inline(el)
  return pandoc.utils.stringify(el)
end
```

## Common Patterns

### `pandoc.utils.stringify()`

Converts any AST element to plain text. Use for shortcode arguments and metadata fields.

### Format Detection

Check the output format before emitting format-specific content:

```lua
if quarto.doc.is_format("html") then
  -- HTML-only logic
end
```

### Quarto Document APIs

```lua
-- HTML only; no-op for PDF/Typst
quarto.doc.add_html_dependency({
  name = "my-dep", version = "0.1.0",
  stylesheets = { "style.css" }, scripts = { "script.js" }
})

-- Works for all formats (HTML, LaTeX/PDF, Typst)
quarto.doc.include_text("in-header", "...")
-- Positions: "in-header", "before-body", "after-body"
```

### Debugging

```lua
quarto.log.output("my-var:", my_var)
```

### Multi-file Modules

```lua
local utils = require("./utils")
local parsing = require("./sub/parsing")
```

Quarto replaces the standard Lua `require()` so that a path that starts with `./` or `../` resolves relative to the calling script.
Always use the relative form.
It resolves against the file that calls it, so it also works inside a module that another module requires.

A bare name does not work inside a module.
Quarto puts only the directory of the top-level filter or shortcode file on `package.path`, so a module cannot load a file beside it by bare name.
The render stops with `module 'b' not found`.

```lua
-- _modules/a.lua
local b = require("b")    -- fails
local b = require("./b")  -- correct
```

A bare name called from the top-level file does load, but the module name is then global to the render.
If two filters each ship a `utils.lua`, the second filter silently receives the module of the first one.
This happens across separate installed extensions as well.
There is no error, only a wrong result.

Inside an extension, keep every module path within the extension directory.
`quarto add` copies only `_extensions/<name>/`, so a `require("../shared")` that works in the source project stops the render after installation with `cannot open .../_extensions/shared.lua`.
Put shared code in a subdirectory of the extension instead.

### Testing

```bash
quarto render example.qmd
```

## Quarto Lua API Surface

The entries below are names only.
Read `https://quarto.org/docs/extensions/lua-api.llms.md` for signatures and fields before you use one that this skill does not show in full.

- Version: `quarto.version`.
- Logging: `quarto.log.output`, `quarto.log.warning`, `quarto.log.debug`.
- Utilities: `quarto.utils.resolve_path`, `quarto.utils.string_to_inlines`, `quarto.utils.string_to_blocks`.
- Current render: `quarto.doc.input_file`, `quarto.doc.output_file`.
- Project: `quarto.project.directory`, `quarto.project.output_directory`, `quarto.project.offset`, `quarto.project.profile`.
- Format detection: `quarto.doc.is_format`, `quarto.doc.has_bootstrap`, `quarto.doc.cite_method`, `quarto.doc.pdf_engine`.
- Includes: `quarto.doc.include_text`, `quarto.doc.include_file`.
- Dependencies: `quarto.doc.add_html_dependency`, `quarto.doc.attach_to_dependency`, `quarto.doc.use_latex_package`, `quarto.doc.add_format_resource`, `quarto.doc.add_resource`, `quarto.doc.add_supporting`.
- Encoding: `quarto.json.encode`, `quarto.json.decode`, `quarto.base64.encode`, `quarto.base64.decode`.
- Tool paths: `quarto.paths.rscript`, `quarto.paths.tinytex_bin_dir`, `quarto.paths.typst`.
- Shortcode helpers: `quarto.shortcode.read_arg`, `quarto.shortcode.error_output`.
- Metadata and variables: `quarto.metadata.get`, `quarto.variables.get`.
- Custom node constructors: `quarto.Callout`, `quarto.ConditionalBlock`, `quarto.Tabset`, `quarto.Tab`.

Names that start with `_quarto` are internal to Quarto.
The one documented exception is `quarto._quarto.ast.add_renderer`, which adds a custom renderer for a custom node type.

## Custom AST Nodes

Quarto extends Pandoc's AST with custom node types that filters match by name, the same way as a Pandoc element.

Node types: Callout, ConditionalBlock, Tabset, PanelLayout, FloatRefTarget, DecoratedCodeBlock, Theorem, Proof, Shortcode, LatexEnvironment, LatexInlineCommand, HtmlTag.

Constructors: `quarto.Callout(tbl)`, `quarto.ConditionalBlock(tbl)`, `quarto.Tabset(tbl)`, `quarto.Tab(tbl)`.

Cross-referenceable figures, tables, and listings are all `FloatRefTarget` nodes.

Filter timing supports eight phases, `pre-ast` through `post-finalize`, set with the `at` property in `_extension.yml` or document YAML.

For the full node type list, constructor signatures, and timing phases, read `references/custom-ast-nodes.md`.

## Resources

- [Quarto Lua API](https://quarto.org/docs/extensions/lua-api.llms.md)
- [Pandoc Lua Filters reference](https://pandoc.org/lua-filters.html)
- [Pandoc community Lua filters](https://github.com/pandoc/lua-filters)
- [LuaRocks style guide](https://github.com/luarocks/lua-style-guide)
