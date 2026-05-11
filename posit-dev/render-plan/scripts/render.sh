#!/bin/bash
# render.sh — Render a markdown plan to Posit-themed HTML using Quarto.
#
# Usage:
#   render.sh <path-to-plan.md> [--no-open]
#
# Arguments:
#   <path-to-plan.md>  Required. Path to the source markdown file.
#   --no-open          Optional. Do not auto-open the rendered HTML in a browser.
#
# Behavior:
#   1. Validates that the input file exists and has a .md extension.
#   2. Stages a temp workspace with the input, the vendored _brand.yml, and
#      a generated _quarto.yml that enables brand theming and embed-resources.
#   3. Runs `quarto render` to produce a self-contained HTML file.
#   4. Moves the HTML next to the original input (overwriting any existing file).
#   5. Opens the HTML in the default browser unless --no-open was passed.
#   6. Prints the absolute output path on stdout.
#
# Notes:
#   This script does NOT check for Quarto or invoke doc-reviewer.
#   Both responsibilities sit upstream in SKILL.md, which Claude executes
#   before calling this script.

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: render.sh <path-to-plan.md> [--no-open]

Render a markdown plan to Posit-themed HTML using Quarto.

Arguments:
  <path-to-plan.md>  Required. Path to the source markdown file.
  --no-open          Optional. Do not auto-open the rendered HTML in a browser.
USAGE
}

INPUT=""
OPEN=1
for arg in "$@"; do
  case "$arg" in
    --no-open) OPEN=0 ;;
    --help|-h) usage; exit 0 ;;
    -*) echo "Unknown flag: $arg" >&2; usage >&2; exit 2 ;;
    *)
      if [ -z "$INPUT" ]; then
        INPUT="$arg"
      else
        echo "Unexpected extra argument: $arg" >&2
        usage >&2
        exit 2
      fi
      ;;
  esac
done

if [ -z "$INPUT" ]; then
  echo "Error: missing required <path-to-plan.md> argument." >&2
  usage >&2
  exit 2
fi

if [ ! -f "$INPUT" ]; then
  echo "Error: input file not found: $INPUT" >&2
  exit 1
fi

case "$INPUT" in
  *.md) ;;
  *)
    echo "Error: input must have .md extension: $INPUT" >&2
    exit 1
    ;;
esac

INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
INPUT_DIR="$(dirname "$INPUT_ABS")"
INPUT_BASE="$(basename "$INPUT_ABS" .md)"
OUTPUT_ABS="$INPUT_DIR/$INPUT_BASE.html"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAND_SRC="$SCRIPT_DIR/../templates/_brand.yml"

if [ ! -f "$BRAND_SRC" ]; then
  echo "Error: vendored _brand.yml not found at $BRAND_SRC" >&2
  exit 1
fi

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

cp "$INPUT_ABS" "$STAGE/$INPUT_BASE.md"
cp "$BRAND_SRC" "$STAGE/_brand.yml"

cat > "$STAGE/_quarto.yml" <<'QUARTO_YML'
project:
  type: default
format:
  html:
    embed-resources: true
QUARTO_YML

if ! quarto render "$STAGE/$INPUT_BASE.md" --to html >/tmp/render-plan-quarto.log 2>&1; then
  echo "Error: quarto render failed. See /tmp/render-plan-quarto.log for details." >&2
  echo "Note: the source markdown may already have been edited by doc-reviewer." >&2
  exit 1
fi

mv -f "$STAGE/$INPUT_BASE.html" "$OUTPUT_ABS"

if [ "$OPEN" -eq 1 ]; then
  case "$(uname -s)" in
    Darwin) open "$OUTPUT_ABS" >/dev/null 2>&1 || echo "Warning: failed to open browser." >&2 ;;
    Linux)  xdg-open "$OUTPUT_ABS" >/dev/null 2>&1 || echo "Warning: failed to open browser." >&2 ;;
    MINGW*|MSYS*|CYGWIN*) start "$OUTPUT_ABS" >/dev/null 2>&1 || echo "Warning: failed to open browser." >&2 ;;
    *) echo "Warning: unknown OS, skipping browser open." >&2 ;;
  esac
fi

echo "$OUTPUT_ABS"
