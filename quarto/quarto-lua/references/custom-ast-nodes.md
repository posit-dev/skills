# Custom AST Nodes

Quarto extends Pandoc's AST with custom node types.
Filters match these by name in handler tables (e.g., `{ Callout = handle_callout }`).

## Available Node Types

**Block-level:** Callout, ConditionalBlock, Tabset, PanelLayout, FloatRefTarget, DecoratedCodeBlock, Theorem, Proof.

**Inline-level:** Shortcode.

**Other:** LatexEnvironment, LatexInlineCommand, HtmlTag.

Note: `_quarto.ast.add_handler()` is internal to Quarto.
Extension authors interact via standard filter handlers.

## Constructor Signatures

### `quarto.Callout(tbl)`

- `type`: `string` - callout type (note, caution, warning, tip, important).
- `title`: `pandoc.Inlines` or `string` (optional).
- `icon`: `boolean` or `string` (optional, defaults based on type).
- `appearance`: `string` - "minimal", "simple", or "default" (optional).
- `collapse`: collapse state (optional).
- `content`: `pandoc.Blocks` or list (optional, defaults to empty Blocks).
- `attr`: `pandoc.Attr` (optional, defaults to empty Attr).

### `quarto.ConditionalBlock(tbl)`

- `node`: `pandoc.Div` - the div holding the content.
- `behavior`: `string` - "content-visible" or "content-hidden".
- `condition`: list of 2-element lists (optional, defaults to `{}`).
  Each sublist: `{"when-format"|"unless-format"|"when-profile"|"unless-profile", value}`.

### `quarto.Tabset(tbl)`

- `tabs`: list of `quarto.Tab` objects (optional, defaults to empty list).
- `level`: `number` - heading level for tabs (optional, default `2`).
- `attr`: `pandoc.Attr` (optional, defaults to `pandoc.Attr("", {"panel-tabset"})`).

### `quarto.Tab(tbl)`

- `title`: `pandoc.Inlines` or `string` (required).
- `content`: `pandoc.Blocks` or `string` (optional, string parsed as markdown).
- `active`: `boolean` (optional, default `false`).

## Filter Timing

Eight phases available via the `at` property in `_extension.yml` or document YAML.
This list is the full `filter-entry-point` enum that Quarto validates against.
The Quarto AST documentation page describes only the first six, so prefer this list.

1. `pre-ast`
2. `post-ast`
3. `pre-quarto`
4. `post-quarto`
5. `pre-render`
6. `post-render`
7. `pre-finalize`
8. `post-finalize`

Syntax in `_extension.yml` or document YAML:

```yaml
filters:
  - path: my-filter.lua
    at: pre-quarto
```

Default (no `at`): filters listed before a "quarto" marker get `pre-quarto`, filters listed after get `post-render`.

## FloatRefTarget

Cross-referenceable elements (figures, tables, listings) are represented as `FloatRefTarget` custom AST nodes.
Filters operating on these should use the `FloatRefTarget` handler:

```lua
return {
  { FloatRefTarget = function(el)
      -- el.caption, el.content, el.identifier, etc.
      return el
    end
  }
}
```
