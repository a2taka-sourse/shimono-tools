#!/usr/bin/env bash
# auto-commit.sh — runs PostToolUse on Write (async)
# Auto-commits new or modified notes to git

VAULT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MARKER="$VAULT_ROOT/.arscontexta"

[ -f "$MARKER" ] || exit 0
[ -f "$VAULT_ROOT/.git/HEAD" ] || exit 0

# Read config
GIT_ENABLED=$(python3 -c "
import re
try:
    with open('$MARKER') as f:
        for line in f:
            m = re.match(r'^git:\s*(true|false)', line.strip())
            if m: print(m.group(1)); break
    else:
        print('true')
except: print('true')
" 2>/dev/null)

[ "$GIT_ENABLED" = "false" ] && exit 0

cd "$VAULT_ROOT"

# Only commit if there are staged or unstaged changes
if git status --porcelain | grep -qE '^(M|A|\?\?)'; then
  git add -A 2>/dev/null
  git commit -m "vault update: $(date '+%Y-%m-%d %H:%M')" --no-verify 2>/dev/null || true
fi

exit 0
