---
name: render-plan
description: Use when you have a finalized markdown plan or spec file and need to share it as a polished, Posit-themed HTML deliverable. Handles plans, specs, design docs, and similar prose-heavy markdown that needs to leave Claude looking like a finished document.
---

# render-plan

Render a markdown plan or spec to a self-contained, Posit-themed HTML document. Applies the Posit style guide to the source markdown first, then renders with Quarto using the canonical Posit `_brand.yml`.

## When to use this skill

- A plan, spec, design doc, or similar prose `.md` is finalized and needs to be shared as a polished document.
- The recipient should not need Quarto, a brand file, or any toolchain to read it — output is a single self-contained `.html`.
- The source markdown should also be cleaned up against the Posit style guide as part of the operation.

This skill is **not** for: authoring new content (write the `.md` first), generic markdown-to-HTML rendering (use Quarto directly), or producing PDF/DOCX (HTML only).

## Prerequisites

Quarto must be installed and on `PATH`. Verify with `quarto --version`. If missing:

- macOS: `brew install quarto`
- Linux: <https://quarto.org/docs/get-started/>
- Windows: <https://quarto.org/docs/get-started/>

If Quarto is missing, **stop the pipeline before invoking doc-reviewer** — otherwise the source file gets edited but no HTML is produced.

## Arguments

- `<path-to-plan.md>` — required. Path to the source markdown file.
- `--no-open` — optional. Do not auto-open the rendered HTML in a browser.

## Workflow

Execute these steps in order. Stop on the first failure.

1. **Validate input.** Confirm the path exists and ends in `.md`. If not, report the mismatch and stop. Source is not modified.

2. **Check Quarto.** Run `command -v quarto`. If it returns nothing, print the install instructions for the user's OS (see Prerequisites) and stop. Do this **before** step 3 so a missing install never leaves the source edited with no HTML to show for it.

3. **Apply the Posit style guide.** Invoke the `doc-reviewer` skill against the source file:

   ```
   Skill("doc-reviewer")
   ```

   doc-reviewer writes its edits to the source `.md` in place. The user ends up with a cleaned-up plan alongside the rendered HTML — this is intentional.

4. **Render.** Run the wrapper script with the (now edited) input file:

   ```bash
   bash "<skill-dir>/scripts/render.sh" "<path-to-plan.md>" [--no-open]
   ```

   The script stages a temp workspace with the input, the vendored `_brand.yml`, and a generated `_quarto.yml` (which enables `embed-resources: true`). It runs `quarto render`, moves the self-contained HTML next to the original `.md` (overwriting any existing file of the same name), and opens it in the browser unless `--no-open` was passed.

5. **Report.** Print the absolute output path returned by the script.

## Error handling

| Failure | Behavior |
|---------|----------|
| Input file missing or wrong extension | Stop with an error. Source is not modified. |
| Quarto missing | Print OS-specific install instructions and stop. Source is not modified. |
| `doc-reviewer` fails | Stop before render. Source file may be partially modified; report this. |
| `quarto render` fails | Stop and print Quarto's stderr. The source has already been edited by `doc-reviewer`; mention this so the user is not surprised by dirty git status. |
| Browser open fails | Warn but do not fail. Output path is already printed. |

## Skill-to-skill chain

Step 3 invokes the `doc-reviewer` skill via Claude's `Skill` tool. This is intentional and documented here so future maintainers understand the dependency: `render-plan` is a thin orchestration over the existing `doc-reviewer` skill and a Quarto render. If `doc-reviewer` changes its contract (e.g., starts requiring an explicit file path argument), update step 3.

## Keywords

render, plan, spec, html, Posit, theming, brand.yml, quarto, doc-reviewer, design doc, deliverable, embed-resources, self-contained, style guide
