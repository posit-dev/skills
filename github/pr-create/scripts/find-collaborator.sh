#!/usr/bin/env bash
# Usage: find-collaborator.sh <owner/repo> <name>
# Lists collaborators with push access whose display name matches <name>.

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: find-collaborator.sh <owner/repo> <name>" >&2
  exit 1
fi

repo="$1"
name="$2"

gh api "repos/${repo}/collaborators" --paginate \
  --jq '.[] | select(.permissions.push) | .login' \
  | while read -r login; do
      display_name=$(gh api "users/$login" --jq '.name // ""' 2>/dev/null)
      echo "$login -> $display_name"
    done | grep -i "$name"
