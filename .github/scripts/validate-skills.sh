#!/bin/bash
# Validates all skill directories changed in a pull request.
#
# Skills in this repo exist at varying depths:
#   <skill-name>/SKILL.md                    (top-level, e.g. brand-yml/)
#   <category>/<skill-name>/SKILL.md         (nested, e.g. github/pr-create/)
#
# Usage: validate-skills.sh <base-ref>
#   base-ref    The base branch name to diff against (e.g. "main").
#               When omitted or when the remote is unavailable, all skills are validated.
#
# Exit codes:
#   0  All validated skills passed.
#   1  One or more skills failed validation.

set -uo pipefail

BASE_REF="${1:-}"

# Find the nearest ancestor directory of a file that contains SKILL.md.
find_skill_root() {
  local dir
  dir=$(dirname "$1")
  while [ "$dir" != "." ]; do
    [ -f "$dir/SKILL.md" ] && echo "$dir" && return 0
    dir=$(dirname "$dir")
  done
  return 1
}

changed_skills=()
if [ -n "$BASE_REF" ]; then
  while IFS= read -r file; do
    root=$(find_skill_root "$file") && changed_skills+=("$root")
  done < <(git diff --name-only "origin/${BASE_REF}...HEAD" 2>/dev/null | grep -v '^$')
  mapfile -t changed_skills < <(printf '%s\n' "${changed_skills[@]:-}" | sort -u | grep -v '^$')
fi

if [ "${#changed_skills[@]}" -eq 0 ]; then
  echo "Could not determine changed skills from git diff; validating all skills."
  mapfile -t changed_skills < <(find . -name 'SKILL.md' -not -path './.git/*' \
    | sed 's|^\./||' \
    | sed 's|/SKILL\.md$||' \
    | sort -u)
fi

if [ "${#changed_skills[@]}" -eq 0 ]; then
  echo "No skill directories found, skipping validation."
  exit 0
fi

FAILED=0
for skill in "${changed_skills[@]}"; do
  if [ ! -d "$skill" ]; then
    echo "Skipping deleted skill: $skill"
    continue
  fi

  skill-validator check --emit-annotations -o markdown "$skill/" \
    | tee >(grep -v '^::' >> "${GITHUB_STEP_SUMMARY:-/dev/null}") || FAILED=1
done

if [ $FAILED -ne 0 ]; then
  echo ""
  echo "Skill validation failed!"
  echo ""
  echo "See the Job Summary for detailed validation results:"
  echo "  https://github.com/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
  echo ""
fi

exit $FAILED
