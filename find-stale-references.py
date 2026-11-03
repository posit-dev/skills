#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///

"""Find stale references to renamed skills after a migration.

Usage:
    ./find-stale-references.py [paths...]
    uv run find-stale-references.py ~/my-project
    ./find-stale-references.py --rename old-name=new-name [paths...]
    ./find-stale-references.py --list-renames

By default, checks the r-lib `r-*` prefix renames (see the "Migration"
section of the renaming PR):

    cli                -> r-cli
    cran-extrachecks   -> r-cran-extrachecks
    lifecycle          -> r-lifecycle
    mirai              -> r-mirai
    testing-r-packages -> r-testthat

Provide your own mapping with --rename old=new (repeatable) to check a
different migration; supplying any --rename replaces the default set.

Two kinds of matches are reported:

  path    A path-like reference (e.g. "r-lib/cli/SKILL.md" or "./cli/").
          Almost certainly a stale skill reference.

  name    A bare name mention (e.g. "`testing-r-packages`"). Review these:
          the old name may also refer to an R package ("cli"), a website
          ("cli.r-lib.org"), or an ordinary word ("lifecycle").

Hidden directories are searched too (a stale reference in .claude/ or
.agents/ is still stale), but .git, node_modules, and similar are skipped.

Exits with status 1 if any matches are found, 0 otherwise, so the script
can be used as a CI check.
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_RENAMES = {
    "cli": "r-cli",
    "cran-extrachecks": "r-cran-extrachecks",
    "lifecycle": "r-lifecycle",
    "mirai": "r-mirai",
    "testing-r-packages": "r-testthat",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    "target",
}

TEXT_EXTENSIONS = {
    ".md",
    ".markdown",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".qmd",
    ".rmd",
    ".ipynb",
    ".py",
    ".r",
    ".rs",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".bash",
    ".zsh",
    ".html",
    ".css",
    ".xml",
    ".csv",
    ".ini",
    ".cfg",
}


def find_matches(text: str, old: str) -> list[tuple[str, int, int]]:
    """Return (kind, start, end) spans for references to `old` in `text`."""
    escaped = re.escape(old)
    patterns = [
        # Path-like reference: old/ but not inside a longer name (r-cli/).
        ("path", rf"(?<![\w-]){escaped}/"),
        # Bare name mention, excluding longer hyphenated names (r-cli-app)
        # and compound words.
        ("name", rf"(?<![\w-]){escaped}(?![\w-])"),
    ]
    matches = []
    for kind, pattern in patterns:
        for match in re.finditer(pattern, text):
            matches.append((kind, match.start(), match.end()))
    return matches


def iter_text_files(paths: list[Path]):
    """Yield text files under the given paths, skipping known binary dirs."""
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in TEXT_EXTENSIONS:
                yield path
            continue
        for item in sorted(path.rglob("*")):
            if not item.is_file():
                continue
            if any(part in SKIP_DIRS for part in item.parts):
                continue
            if item.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            yield item


def context_window(line: str, start: int, end: int, width: int = 100) -> str:
    """Return a trimmed snippet of `line` centered on the match span."""
    pad = max(0, (width - (end - start)) // 2)
    lo = max(0, start - pad)
    hi = min(len(line), end + pad)
    snippet = line[lo:hi].strip()
    prefix = "..." if lo > 0 else ""
    suffix = "..." if hi < len(line) else ""
    return prefix + snippet + suffix


def scan(paths: list[Path], renames: dict[str, str]) -> list[dict]:
    """Scan files and return a list of match records."""
    records = []
    for file_path in iter_text_files(paths):
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(lines, start=1):
            for old, new in renames.items():
                for kind, start, end in find_matches(line, old):
                    records.append(
                        {
                            "file": str(file_path),
                            "line": lineno,
                            "kind": kind,
                            "old": old,
                            "new": new,
                            "context": context_window(line, start, end),
                        }
                    )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find stale references to renamed skills.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to scan (default: current directory).",
    )
    parser.add_argument(
        "--rename",
        action="append",
        default=[],
        metavar="OLD=NEW",
        help="Add an old=new skill rename to check (repeatable). "
        "Supplying any --rename replaces the default rename set.",
    )
    parser.add_argument(
        "--list-renames",
        action="store_true",
        help="Print the rename mapping that would be checked and exit.",
    )
    parser.add_argument(
        "--kinds",
        default="path,name",
        help="Comma-separated match kinds to report: path, name "
        "(default: both).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output matches as JSON instead of text.",
    )
    args = parser.parse_args()

    kinds = {k.strip() for k in args.kinds.split(",") if k.strip()}
    unknown = kinds - {"path", "name"}
    if unknown:
        parser.error(
            f"unknown kind(s): {', '.join(sorted(unknown))}; "
            "expected path and/or name"
        )
    renames = dict(DEFAULT_RENAMES)
    if args.rename:
        renames = {}
        for pair in args.rename:
            if "=" not in pair:
                parser.error(f"--rename expects OLD=NEW, got: {pair}")
            old, new = pair.split("=", 1)
            renames[old] = new

    if args.list_renames:
        for old, new in renames.items():
            print(f"{old} -> {new}")
        return 0

    paths = [Path(p) for p in args.paths]
    missing = [p for p in paths if not p.exists()]
    if missing:
        for p in missing:
            print(f"error: path does not exist: {p}", file=sys.stderr)
        return 2

    records = [r for r in scan(paths, renames) if r["kind"] in kinds]

    if args.json:
        print(json.dumps(records, indent=2))
    else:
        by_file: dict[str, list[dict]] = {}
        for record in records:
            by_file.setdefault(record["file"], []).append(record)

        for file_path, file_records in sorted(by_file.items()):
            print(f"{file_path}")
            for record in file_records:
                print(
                    f"  {record['kind']:>4}  L{record['line']:<4} "
                    f"{record['old']} -> {record['new']}"
                )
                print(f"        {record['context']}")
        if records:
            path_count = sum(1 for r in records if r["kind"] == "path")
            name_count = sum(1 for r in records if r["kind"] == "name")
            print(
                f"\n{len(records)} match(es) in {len(by_file)} file(s) "
                f"({path_count} path, {name_count} name). "
                "Name mentions may be false positives: review each one."
            )
        else:
            print("No stale references found.")

    return 1 if records else 0


if __name__ == "__main__":
    sys.exit(main())
