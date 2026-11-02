#!/usr/bin/env python3
"""
Generate llms-full.txt for a quartodoc-based Python package documentation site.

Note: llms.txt (link index) is generated natively by Quarto 1.9.
This script generates llms-full.txt, which adds cleaned page content
under each entry so LLMs get the full documentation context.

Usage:
    python scripts/generate_llms_full_txt.py
    python scripts/generate_llms_full_txt.py --site-dir .
    python scripts/generate_llms_full_txt.py --output llms-full.txt

Requires: pyyaml (pip install pyyaml)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Page:
    title: str
    url: str
    source: Path


@dataclass
class Section:
    title: str
    pages: list[Page] = field(default_factory=list)


@dataclass
class Site:
    name: str
    description: str
    base_url: str
    sections: list[Section] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Sidebar / _quarto.yml parsing
# ---------------------------------------------------------------------------


def load_quarto_config(site_dir: Path) -> dict:
    quarto_yml = site_dir / "_quarto.yml"
    if not quarto_yml.exists():
        raise FileNotFoundError(f"_quarto.yml not found in {site_dir}")
    with open(quarto_yml) as f:
        return yaml.safe_load(f)


def qmd_path_to_url(base_url: str, qmd_path: str) -> str:
    """Convert a .qmd path relative to site root to an absolute URL."""
    base_url = base_url.rstrip("/")
    path = qmd_path.strip("/")

    # index.qmd files map to the directory URL (trailing slash)
    if path.endswith("/index.qmd") or path == "index.qmd":
        url_path = path[: -len("index.qmd")].rstrip("/")
        return f"{base_url}/{url_path}/" if url_path else f"{base_url}/"

    # Regular .qmd files map to .html
    if path.endswith(".qmd"):
        path = path[: -len(".qmd")] + ".html"

    return f"{base_url}/{path}"


def extract_title(qmd_path: Path) -> str:
    """Extract title from QMD YAML frontmatter. Prefers pagetitle > title > filename."""
    if not qmd_path.exists():
        return qmd_path.stem

    content = qmd_path.read_text(encoding="utf-8")
    frontmatter = _extract_frontmatter(content)
    if frontmatter:
        parsed = yaml.safe_load(frontmatter)
        if isinstance(parsed, dict):
            return parsed.get("pagetitle") or parsed.get("title") or qmd_path.stem

    return qmd_path.stem


def _extract_frontmatter(content: str) -> str | None:
    """Return the raw YAML between opening --- and closing ---."""
    if not content.startswith("---"):
        return None
    end = content.find("\n---", 3)
    if end == -1:
        return None
    return content[3:end].strip()


def walk_sidebar_contents(
    contents: list,
    site_dir: Path,
    base_url: str,
    seen_urls: set[str],
) -> list[Page]:
    """
    Recursively walk a sidebar contents list and return Page objects.

    Handles all four quartodoc/Quarto entry formats:
    - "path/to/file.qmd"            (string)
    - {section: "Title", contents:} (section dict — flattened)
    - {href: "path.qmd", text: ...} (href dict)
    - {file: "path.qmd"}            (file dict)
    """
    pages: list[Page] = []

    for entry in contents:
        if isinstance(entry, str):
            # Plain string path
            _add_page(entry, site_dir, base_url, seen_urls, pages)

        elif isinstance(entry, dict):
            if "section" in entry:
                # Nested section — flatten into the current page list
                sub_contents = entry.get("contents", [])
                pages.extend(
                    walk_sidebar_contents(sub_contents, site_dir, base_url, seen_urls)
                )
            elif "href" in entry:
                href = entry["href"]
                # Skip fragment-only hrefs
                if href.startswith("#"):
                    continue
                # Strip fragment from href if present
                href = href.split("#")[0]
                _add_page(href, site_dir, base_url, seen_urls, pages)
            elif "file" in entry:
                _add_page(entry["file"], site_dir, base_url, seen_urls, pages)
            elif "contents" in entry:
                # Bare contents dict without section title
                pages.extend(
                    walk_sidebar_contents(
                        entry["contents"], site_dir, base_url, seen_urls
                    )
                )

    return pages


def _add_page(
    rel_path: str,
    site_dir: Path,
    base_url: str,
    seen_urls: set[str],
    pages: list[Page],
) -> None:
    url = qmd_path_to_url(base_url, rel_path)
    if url in seen_urls:
        return
    seen_urls.add(url)

    qmd_path = site_dir / rel_path
    if not qmd_path.exists():
        print(f"  Warning: {qmd_path} not found, skipping", file=sys.stderr)
        return

    pages.append(Page(title=extract_title(qmd_path), url=url, source=qmd_path))


def read_quartodoc_sidebar(sidebar_yml: Path, site_dir: Path, base_url: str, seen_urls: set[str]) -> list[Page]:
    """
    Read a quartodoc-generated _sidebar.yml file (lives next to the API reference index).
    Returns pages in sidebar order.
    """
    if not sidebar_yml.exists():
        return []

    with open(sidebar_yml) as f:
        data = yaml.safe_load(f)

    contents = data.get("contents", []) if isinstance(data, dict) else []
    return walk_sidebar_contents(contents, site_dir, base_url, seen_urls)


def build_site(config: dict, site_dir: Path) -> Site:
    """Build a Site from a parsed _quarto.yml config."""
    website = config.get("website", {})
    base_url = website.get("site-url", "").rstrip("/")
    name = website.get("title", "Package")
    description = website.get("description", "")

    site = Site(name=name, description=description, base_url=base_url)
    seen_urls: set[str] = set()

    # Walk each top-level sidebar
    sidebars = website.get("sidebar", [])
    if isinstance(sidebars, dict):
        sidebars = [sidebars]

    for sidebar in sidebars:
        sidebar_id = sidebar.get("id", "")
        contents = sidebar.get("contents", [])

        for entry in contents:
            if isinstance(entry, str):
                # A bare file entry at the top level — add as a one-page section
                pages = walk_sidebar_contents([entry], site_dir, base_url, seen_urls)
                if pages:
                    title = pages[0].title
                    site.sections.append(Section(title=title, pages=pages))

            elif isinstance(entry, dict) and "section" in entry:
                section_title = entry["section"]
                sub_contents = entry.get("contents", [])

                # Check if this section points to a quartodoc-generated _sidebar.yml
                quartodoc_cfg = config.get("quartodoc", {})
                api_sections = quartodoc_cfg.get("sections", [])
                api_dir = quartodoc_cfg.get("dir", "reference")

                sidebar_yml = site_dir / api_dir / "_sidebar.yml"
                is_api_section = any(
                    s.get("title") == section_title for s in api_sections
                ) or section_title.lower() in ("reference", "api reference", "api")

                if is_api_section and sidebar_yml.exists():
                    pages = read_quartodoc_sidebar(sidebar_yml, site_dir, base_url, seen_urls)
                else:
                    pages = walk_sidebar_contents(sub_contents, site_dir, base_url, seen_urls)

                if pages:
                    site.sections.append(Section(title=section_title, pages=pages))

    return site


# ---------------------------------------------------------------------------
# QMD content cleaning
# ---------------------------------------------------------------------------


def clean_qmd_content(content: str) -> str:
    """
    Clean QMD source for inclusion in llms-full.txt.
    Removes Quarto-specific markup, leaving clean markdown.
    """
    # 1. Strip YAML frontmatter
    content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

    # 2. Remove raw HTML blocks
    content = re.sub(r"```\{=html\}.*?```", "", content, flags=re.DOTALL)

    # 3. Remove shinylive/quartodoc cell metadata comments (#| key: value)
    content = re.sub(r"^#\|.*$", "", content, flags=re.MULTILINE)

    # 4. Convert Quarto code fences to plain markdown
    #    ```{python} -> ```python, ```{shinylive-python} -> ```python, etc.
    content = re.sub(
        r"```\{(shinylive-python|shinylive-r|python|r|bash|shell)\}",
        lambda m: "```python"
        if "python" in m.group(1)
        else "```r"
        if m.group(1) == "r"
        else "```bash",
        content,
    )
    # Remove any remaining ```{...} fences (e.g. ```{.python})
    content = re.sub(r"```\{[^}]*\}", "```", content)

    # 5. Remove Quarto div fences (lines that are only colons)
    content = re.sub(r"^:{3,}\s*(\{[^}]*\})?\s*$", "", content, flags=re.MULTILINE)

    # 6. Strip inline HTML tags
    content = re.sub(r"<[^>]+>", "", content)

    # 7. Collapse 3+ consecutive blank lines to 2
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip()


def load_page_content(page: Page) -> str:
    """Load and clean a page's QMD source."""
    if not page.source.exists():
        return ""
    raw = page.source.read_text(encoding="utf-8")
    return clean_qmd_content(raw)


# ---------------------------------------------------------------------------
# Output generation
# ---------------------------------------------------------------------------


def render_llms_full_txt(site: Site) -> str:
    lines: list[str] = []

    lines.append(f"# {site.name}")
    lines.append("")

    if site.description:
        lines.append(f"> {site.description}")
        lines.append("")

    for section in site.sections:
        lines.append(f"## {section.title}")
        lines.append("")

        for page in section.pages:
            lines.append(f"- [{page.title}]({page.url})")
            lines.append("")
            content = load_page_content(page)
            if content:
                lines.append(content)
                lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--site-dir", type=Path, default=Path("."), help="Root directory containing _quarto.yml (default: .)")
    parser.add_argument("--output", type=Path, default=Path("llms-full.txt"), help="Output file path (default: llms-full.txt)")
    args = parser.parse_args()

    site_dir = args.site_dir.resolve()
    print(f"Reading site config from {site_dir}/_quarto.yml", file=sys.stderr)

    config = load_quarto_config(site_dir)
    site = build_site(config, site_dir)

    content = render_llms_full_txt(site)
    args.output.write_text(content, encoding="utf-8")

    page_count = sum(len(s.pages) for s in site.sections)
    print(f"Wrote {args.output} ({len(site.sections)} sections, {page_count} pages)", file=sys.stderr)


if __name__ == "__main__":
    main()
