#!/usr/bin/env bash
# session-capture.sh — runs at Stop
# Archives session state and creates mining task

VAULT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MARKER="$VAULT_ROOT/.arscontexta"

[ -f "$MARKER" ] || exit 0

SESSION_FILE="$VAULT_ROOT/ops/sessions/current.json"
SESSIONS_DIR="$VAULT_ROOT/ops/sessions"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Archive current session
if [ -f "$SESSION_FILE" ]; then
  # Update last_activity
  SESSION_ID=$(python3 -c "import json; d=json.load(open('$SESSION_FILE')); print(d.get('session_id', '$TIMESTAMP'))" 2>/dev/null || echo "$TIMESTAMP")
  ARCHIVE_FILE="$SESSIONS_DIR/${TIMESTAMP}.json"
  cp "$SESSION_FILE" "$ARCHIVE_FILE"

  # Create mining task in queue
  if [ -f "$VAULT_ROOT/ops/queue/queue.json" ]; then
    python3 - <<PYEOF 2>/dev/null
import json
from datetime import datetime

queue_file = "$VAULT_ROOT/ops/queue/queue.json"
with open(queue_file) as f:
    data = json.load(f)

task = {
    "id": "session-mine-$TIMESTAMP",
    "type": "session-mining",
    "status": "pending",
    "target": "$ARCHIVE_FILE",
    "batch": "session-$TIMESTAMP",
    "created": datetime.utcnow().isoformat() + "Z",
    "current_phase": "extract",
    "completed_phases": []
}

data["tasks"].append(task)

with open(queue_file, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF
  fi
fi

echo "Session captured: $TIMESTAMP"
