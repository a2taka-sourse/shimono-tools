#!/usr/bin/env bash
# session-orient.sh — runs at SessionStart
# Injects vault orientation into the session

VAULT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MARKER="$VAULT_ROOT/.arscontexta"

# Only run in this vault
[ -f "$MARKER" ] || exit 0

echo "=== Vault Orientation ==="
echo ""

# Show current date
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

# Inject folder tree (3 levels)
echo "=== Vault Structure ==="
if command -v tree &>/dev/null; then
  tree "$VAULT_ROOT" -L 3 --dirsfirst -I ".git|.claude|archive|*.json" 2>/dev/null
else
  find "$VAULT_ROOT" -maxdepth 3 -not -path "*/.git/*" -not -path "*/.claude/*" | head -50
fi
echo ""

# Show inbox pressure
INBOX_COUNT=$(find "$VAULT_ROOT/inbox" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "=== Inbox: $INBOX_COUNT items ==="
if [ "$INBOX_COUNT" -gt 0 ]; then
  find "$VAULT_ROOT/inbox" -name "*.md" 2>/dev/null | head -5
fi
echo ""

# Show goals summary
if [ -f "$VAULT_ROOT/self/goals.md" ]; then
  echo "=== Current Goals ==="
  head -30 "$VAULT_ROOT/self/goals.md"
  echo ""
fi

# Check maintenance conditions
OBS_COUNT=$(find "$VAULT_ROOT/ops/observations" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
TEN_COUNT=$(find "$VAULT_ROOT/ops/tensions" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

if [ "$OBS_COUNT" -ge 10 ] || [ "$TEN_COUNT" -ge 5 ]; then
  echo "=== Maintenance Alert ==="
  [ "$OBS_COUNT" -ge 10 ] && echo "  Observations: $OBS_COUNT pending (threshold: 10) → run /review"
  [ "$TEN_COUNT" -ge 5 ] && echo "  Tensions: $TEN_COUNT pending (threshold: 5) → run /review"
  echo ""
fi

# Check reminders
if [ -f "$VAULT_ROOT/ops/reminders.md" ]; then
  DUE=$(grep -E '^\- \[ \]' "$VAULT_ROOT/ops/reminders.md" 2>/dev/null | grep -v "^$" | head -3)
  if [ -n "$DUE" ]; then
    echo "=== Reminders ==="
    echo "$DUE"
    echo ""
  fi
fi

# Session state
SESSION_FILE="$VAULT_ROOT/ops/sessions/current.json"
if [ -f "$SESSION_FILE" ]; then
  echo "=== Previous Session State ==="
  cat "$SESSION_FILE"
  echo ""
fi

# Initialize new session
SESSION_ID="${CLAUDE_CONVERSATION_ID:-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$VAULT_ROOT/ops/sessions"
cat > "$SESSION_FILE" <<EOF
{
  "session_id": "$SESSION_ID",
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "notes_created": [],
  "notes_modified": [],
  "last_activity": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "=== Session started: $SESSION_ID ==="
