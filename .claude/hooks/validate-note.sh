#!/usr/bin/env bash
# validate-note.sh — runs PostToolUse on Write
# Validates YAML frontmatter on new notes

VAULT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MARKER="$VAULT_ROOT/.arscontexta"

[ -f "$MARKER" ] || exit 0

# Get the file that was written (from env or stdin)
FILE="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"
[ -z "$FILE" ] && exit 0

# Only validate notes in project folders
case "$FILE" in
  *ctf/*.md|*shimono/*.md|*ai-lain/*.md) ;;
  *) exit 0 ;;
esac

# Skip index files
case "$FILE" in
  *index.md) exit 0 ;;
esac

ISSUES=""

# Check for YAML frontmatter
if ! head -1 "$FILE" | grep -q '^---'; then
  ISSUES="$ISSUES\n  MISSING: YAML frontmatter (file must start with ---)"
fi

# Check for description field
if ! grep -q '^description:' "$FILE"; then
  ISSUES="$ISSUES\n  MISSING: description field"
elif grep -q '^description: ""' "$FILE" || grep -q '^description:$' "$FILE"; then
  ISSUES="$ISSUES\n  EMPTY: description field (must add context beyond the title)"
fi

# Check for topics field
if ! grep -q '^topics:' "$FILE"; then
  ISSUES="$ISSUES\n  MISSING: topics field (must link to project hub)"
elif grep -q '^topics: \[\]' "$FILE"; then
  ISSUES="$ISSUES\n  EMPTY: topics field (must include [[ctf/index]], [[shimono/index]], or [[ai-lain/index]])"
fi

# Check for type field
if ! grep -q '^type:' "$FILE"; then
  ISSUES="$ISSUES\n  MISSING: type field"
fi

if [ -n "$ISSUES" ]; then
  echo "⚠ Schema validation for $(basename "$FILE"):"
  echo -e "$ISSUES"
  echo "  Fix these before the note is complete."
fi

exit 0
