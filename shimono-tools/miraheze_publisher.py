"""
Miraheze publisher — generate and push migration status page.

Requires bot credentials in .env:
  MIRAHEZE_BOT_USER     e.g. YourUsername@MigrationBot
  MIRAHEZE_BOT_PASSWORD (from Special:BotPasswords)

Target page: [[下腦Wiki移行状況]]
"""
import json
import os
from datetime import datetime
from pathlib import Path

import requests

from config import MIRAHEZE_API, MIRAHEZE_WIKI, DATA_DIR, MIGRATION_PAGE_TITLE, MIGRATION_PAGE_CATEGORY


# ── Visual helpers ───────────────────────────────────────────────────────────

BAR_FILLED  = "█"
BAR_EMPTY   = "░"
BAR_WIDTH   = 40  # characters

# Colour palette (MediaWiki inline CSS)
COLOR = {
    "green":  "#4caf50",
    "red":    "#ef5350",
    "blue":   "#42a5f5",
    "orange": "#ff9800",
    "grey":   "#9e9e9e",
    "bg":     "#e8e8e8",
}


def _ascii_bar(pct: float, width: int = BAR_WIDTH) -> str:
    """Unicode block-character progress bar: [████░░░░░░] 41.4%"""
    filled = round(pct / 100 * width)
    empty  = width - filled
    return f"[{BAR_FILLED * filled}{BAR_EMPTY * empty}]"


def _html_bar(pct: float, color: str, height: str = "14px") -> str:
    """Inline-CSS coloured bar (works in standard MediaWiki HTML)."""
    pct = min(max(pct, 0), 100)
    return (
        f'<div style="background:{COLOR["bg"]};border-radius:3px;'
        f'overflow:hidden;width:100%;height:{height};">'
        f'<div style="background:{color};width:{pct:.1f}%;height:100%;"></div>'
        f'</div>'
    )


def _chart_row(label: str, count: int, total: int, color: str,
               note: str = "") -> str:
    """One row of the bar chart table."""
    pct = count / total * 100 if total else 0
    note_wt = f" <small>({note})</small>" if note else ""
    return (
        f"|-\n"
        f"| {label}{note_wt} || style='text-align:right' | '''{count}''' "
        f"|| {_html_bar(pct, color)} "
        f"|| style='text-align:right' | {pct:.1f}%"
    )


def _article_list_wikitext(articles: list[dict], key: str = "title",
                            link_type: str = "internal") -> str:
    lines = []
    for a in articles:
        title = a[key]
        if link_type == "internal":
            lines.append(f"# [[{title}]]")
        else:
            url = a.get("seesaa_url") or a.get("miraheze_url") or ""
            lines.append(f"# [{url} {title}]")
    return "\n".join(lines) if lines else "（なし）"


# ── Main wikitext generator ──────────────────────────────────────────────────

def generate_wikitext(status: dict) -> str:
    s   = status["stats"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")

    pct_migrated = s["migration_pct"]
    pct_remaining = round(100 - pct_migrated, 1)
    total = s["seesaa_total"]

    # ── ASCII art header bar ─────────────────────────────────────────────────
    ascii_bar = _ascii_bar(pct_migrated)

    # ── HTML progress bar (full-width, two-tone) ─────────────────────────────
    html_progress = (
        f'<div style="background:{COLOR["bg"]};border-radius:4px;'
        f'overflow:hidden;width:100%;height:20px;font-size:0;">'
        f'<div style="background:{COLOR["green"]};width:{pct_migrated:.1f}%;'
        f'height:100%;display:inline-block;"></div>'
        f'<div style="background:{COLOR["red"]};width:{pct_remaining:.1f}%;'
        f'height:100%;display:inline-block;"></div>'
        f'</div>'
    )

    # ── Bar chart table (2 separate charts with correct reference bases) ───────
    # Chart 1: SeesaaWiki migration (reference = seesaa_total)
    seesaa_chart_rows = "\n".join([
        _chart_row("✓ 移行済み", s["migrated"],    total, COLOR["green"]),
        _chart_row("⏳ 未移行",  s["seesaa_only"], total, COLOR["red"]),
    ])

    # Chart 2: Miraheze-side content (reference = miraheze total)
    miraheze_total = s["miraheze_exclusive"] + s["miraheze_new"]
    miraheze_chart_rows = "\n".join([
        _chart_row("🔵 Miraheze独自（排他）", s["miraheze_exclusive"], miraheze_total,
                   COLOR["blue"],   "Twitter/YouTube等"),
        _chart_row("✨ Miraheze新規",          s["miraheze_new"],       miraheze_total,
                   COLOR["orange"], "旧Wiki非対象"),
    ])
    miraheze_chart_total_label = miraheze_total or 1  # avoid div-by-zero display

    # ── Compact summary box ───────────────────────────────────────────────────
    summary_box = (
        f'<div style="border:2px solid {COLOR["green"]};border-radius:6px;'
        f'padding:1em;background:#f9fff9;font-family:monospace;">\n'
        f"'''移行進捗 — {s['migrated']} / {total} 記事'''\n\n"
        f"{ascii_bar} {pct_migrated}%\n\n"
        f"旧SeesaaWiki基準。未移行: {s['seesaa_only']}件\n"
        f'</div>'
    )

    # ── Article lists ─────────────────────────────────────────────────────────
    migrated_wt  = _article_list_wikitext(status["migrated"])
    seesaa_wt    = _article_list_wikitext(status["seesaa_only"], link_type="external")
    exclusive_wt = _article_list_wikitext(status["miraheze_exclusive"])
    new_wt       = _article_list_wikitext(status["miraheze_new"])

    return f"""\
<!-- この記事は自動生成されます。編集しても次回更新時に上書きされます。 -->
== 下腦Wiki 移行状況ダッシュボード ==
''自動生成 — 最終更新: {now}''

----

{summary_box}

{html_progress}

----

=== SeesaaWiki → Miraheze 移行チャート ===
''基準: 旧SeesaaWiki {total}記事''

{{| class="wikitable" style="width:100%"
! 種別 !! 件数 !! グラフ ({total}件 = 100%) !! ％
{seesaa_chart_rows}
|}}

=== Mirahezeコンテンツ内訳チャート ===
''基準: Miraheze独自ページ {miraheze_total}記事''

{{| class="wikitable" style="width:100%"
! 種別 !! 件数 !! グラフ ({miraheze_total}件 = 100%) !! ％
{miraheze_chart_rows}
|}}

=== 全体サマリー ===
{{| class="wikitable" style="text-align:center; width:50%"
! 種別 !! 件数
|-
| style="text-align:left;background:#e8f5e9" | ✓ 移行済み || '''{s['migrated']}'''
|-
| style="text-align:left;background:#ffebee" | ⏳ 未移行 || {s['seesaa_only']}
|-
| style="text-align:left;background:#e3f2fd" | 🔵 Miraheze独自（排他） || {s['miraheze_exclusive']}
|-
| style="text-align:left;background:#fff3e0" | ✨ Miraheze新規 || {s['miraheze_new']}
|-
! SeesaaWiki総数 !! {total}
|}}

----

=== 移行済み記事 ({s['migrated']}件) ===
{migrated_wt}

=== 未移行記事 ({s['seesaa_only']}件) ===
以下の記事はまだ新訳Wikiに存在しません。

{seesaa_wt}

=== Miraheze独自コンテンツ ===
==== Twitter/YouTube等 ({s['miraheze_exclusive']}件) ====
{exclusive_wt}

==== 新規記事 ({s['miraheze_new']}件) ====
{new_wt}

[[Category:{MIGRATION_PAGE_CATEGORY}]]
"""


# ── MediaWiki API ────────────────────────────────────────────────────────────

def _get_csrf_token(session: requests.Session, username: str, password: str) -> str:
    """Login with bot credentials and return a CSRF token."""
    # Step 1: get login token
    r = session.get(MIRAHEZE_API, params={
        "action": "query", "meta": "tokens", "type": "login", "format": "json"
    })
    r.raise_for_status()
    login_token = r.json()["query"]["tokens"]["logintoken"]

    # Step 2: login
    r = session.post(MIRAHEZE_API, data={
        "action": "login",
        "lgname": username,
        "lgpassword": password,
        "lgtoken": login_token,
        "format": "json",
    })
    r.raise_for_status()
    result = r.json()["login"]["result"]
    if result != "Success":
        raise ValueError(f"ログイン失敗: {result}")

    # Step 3: get edit token
    r = session.get(MIRAHEZE_API, params={
        "action": "query", "meta": "tokens", "format": "json"
    })
    r.raise_for_status()
    return r.json()["query"]["tokens"]["csrftoken"]


def push(status_path: Path | None = None) -> None:
    """Push migration status wikitext to Miraheze."""
    status_path = status_path or DATA_DIR / "migration_status.json"

    if not status_path.exists():
        print(f"ERROR: {status_path} が存在しません。先に `python run.py compare` を実行してください。")
        return

    username = os.getenv("MIRAHEZE_BOT_USER")
    password = os.getenv("MIRAHEZE_BOT_PASSWORD")
    if not username or not password:
        print("ERROR: .env に MIRAHEZE_BOT_USER / MIRAHEZE_BOT_PASSWORD を設定してください。")
        print("       Botアカウント作成: https://shikabaton.miraheze.org/wiki/Special:BotPasswords")
        return

    status = json.loads(status_path.read_text(encoding="utf-8"))
    wikitext = generate_wikitext(status)

    session = requests.Session()
    session.headers["User-Agent"] = "ShimonoMigrationBot/1.0"

    print("Mirahezeにログイン中...")
    csrf_token = _get_csrf_token(session, username, password)

    print(f"ページ更新: [[{MIGRATION_PAGE_TITLE}]]")
    r = session.post(MIRAHEZE_API, data={
        "action": "edit",
        "title": MIGRATION_PAGE_TITLE,
        "text": wikitext,
        "summary": f"移行状況自動更新 ({status['stats']['migration_pct']}%)",
        "token": csrf_token,
        "format": "json",
    })
    r.raise_for_status()
    edit_result = r.json()

    if edit_result.get("edit", {}).get("result") == "Success":
        url = f"https://{MIRAHEZE_WIKI}.miraheze.org/wiki/{MIGRATION_PAGE_TITLE.replace(' ', '_')}"
        print(f"✓ 更新完了: {url}")
    else:
        print(f"✗ エラー: {edit_result}")


def preview(output_path: Path | None = None) -> None:
    """Generate wikitext locally without pushing (for review)."""
    status_path = DATA_DIR / "migration_status.json"
    output_path = output_path or DATA_DIR / "migration_page.wiki"

    if not status_path.exists():
        print("ERROR: migration_status.json が存在しません。")
        return

    status = json.loads(status_path.read_text(encoding="utf-8"))
    wikitext = generate_wikitext(status)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(wikitext, encoding="utf-8")
    print(f"プレビュー生成: {output_path}")


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    load_dotenv()

    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        preview()
    else:
        push()
