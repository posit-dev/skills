---
name: llms-info-from-quartodoc
description: >
  Use when adding llms-full.txt to a Python package documentation site built
  with Quarto and quartodoc. Triggers when the user wants to make their package
  docs fully consumable by LLMs, mentions the llmstxt.org spec, or asks about
  generating rich LLM context files for quartodoc sites.
metadata:
  author: Elizabeth Nelson (@enelson)
  version: "1.0"
license: MIT
---

# LLM-Friendly Docs from quartodoc

Generate `llms-full.txt` for Python package documentation sites built with Quarto and quartodoc, following the [llmstxt.org](https://llmstxt.org/) spec.

Quarto 1.9 generates `llms.txt` (a concise link index) natively — you don't need to write that. This skill covers `llms-full.txt` only: the same structure as `llms.txt`, but with cleaned page content under each entry, giving LLMs and coding assistants the full documentation context.

## The llms-full.txt Format

Per the llmstxt.org spec:

- **H1 heading**: Project name
- **Blockquote**: Short project summary (from `website.description` or package metadata)
- **H2 sections**: Content grouped by topic, matching the sidebar structure
- **Per entry**: markdown link followed by cleaned page content

---

## Workflow

### Step 1: Understand the site structure

Read `_quarto.yml` to understand:
- Sidebar structure (IDs, contents, sections) — this determines section grouping
- quartodoc configuration (package name, API sections) — determines API reference pages
- Base URL (`website.site-url`) — needed for absolute URLs in the output
- Site description (`website.description`) — used in the blockquote

### Step 2: Write `scripts/generate_llms_full_txt.py`

Model the script after `references/generate-llms-full-txt-example.py` and adapt it to the project's sidebar layout, quartodoc sections, and content structure.

**Script responsibilities:**

1. Parse `_quarto.yml` sidebars to discover pages in sidebar order
2. Read quartodoc-generated `_sidebar.yml` files for API reference pages
3. For each page:
   - Extract title from YAML frontmatter (`pagetitle` > `title` > filename)
   - Build the page URL (`.qmd` → `.html`, `index.qmd` → trailing slash)
   - Clean the QMD content (see below)
4. Write `llms-full.txt` with section H2 headers, markdown links, and cleaned content

**QMD content cleaning pipeline** (apply in order):
1. Strip YAML frontmatter (`---` blocks at top)
2. Remove Quarto div fences (`:::`, `::::`, etc.)
3. Remove raw HTML blocks (` ```{=html} ... ``` `)
4. Remove shinylive/quartodoc metadata comments (`#| key: value`)
5. Convert Quarto code fences (`{python}`, `{shinylive-python}`, etc.) to plain ` ```python `
6. Strip inline HTML tags (`<...>`)
7. Collapse 3+ consecutive blank lines to 2

**Use `@dataclass` for site structure types:**
```python
@dataclass
class Page:
    title: str
    url: str
    source: Path

@dataclass
class Section:
    title: str
    pages: list[Page]
```

**Edge cases to handle:**
- Fragment-only hrefs (e.g. `#section`) — resolve to parent page, deduplicate
- Missing `.qmd` files — skip with a warning
- Duplicate entries across sections — deduplicate by URL

### Step 3: Write tests

Unit tests covering:
- QMD content cleaning (each cleaning step independently)
- Sidebar walking (all 4 entry formats: string, section dict, href dict, file dict)
- URL generation (`index.qmd` → trailing slash, `.qmd` → `.html`, nested paths)
- Title extraction (`pagetitle` precedence, missing frontmatter)
- Integration test: build site structure from a minimal `_quarto.yml` fixture

### Step 4: Integrate into build

Add a Makefile target. `llms-full.txt` is committed to the repo — not a build-only artifact — so changes are reviewable in PRs.

```makefile
llms-full-txt: $(PYBIN) quartodoc
	$(PYBIN) scripts/generate_llms_full_txt.py

all: quartodoc llms-full-txt site
```

Add `llms-full.txt` to `_quarto.yml` project resources so Quarto copies it to the output:
```yaml
project:
  resources:
    - llms-full.txt
```

### Step 5: Add CI freshness check

After the site build step, add:
```yaml
- name: Check llms-full.txt is up to date
  run: |
    make llms-full-txt
    git diff --exit-code llms-full.txt || \
      (echo "Run 'make llms-full-txt' locally and commit the result." && exit 1)
```

**After all steps:** run `make llms-full-txt` and commit `llms-full.txt`.

---

## Additional Reference

See `references/generate-llms-full-txt-example.py` for a complete working implementation to study and adapt.
