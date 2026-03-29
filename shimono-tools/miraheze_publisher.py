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

from config import MIRAHEZE_API, MIRAHEZE_WIKI, DATA_DIR, MIGRATION_PAGE_TITLE


# ── Wikitext generation ──────────────────────────────────────────────────────

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


def generate_wikitext(status: dict) -> str:
    s = status["stats"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    remaining_pct = round(100 - s["migration_pct"], 1)

    migrated_wt   = _article_list_wikitext(status["migrated"])
    seesaa_wt     = _article_list_wikitext(status["seesaa_only"], link_type="external")
    exclusive_wt  = _article_list_wikitext(status["miraheze_exclusive"])
    new_wt        = _article_list_wikitext(status["miraheze_new"])

    return f"""\
<!-- この記事は自動生成されます。編集しても次回更新時に上書きされます。 -->
== 下腦Wiki 移行状況ダッシュボード ==
''自動生成 — 最終更新: {now}''

=== 概要 ===
旧Wikiからの記事移行の進捗状況です。

{{| class="wikitable" style="text-align:center; width:60%"
! 種別 !! 件数 !! 割合
|-
| style="text-align:left" | '''✓ 移行済み''' || '''{ s['migrated'] }''' || '''{s['migration_pct']}%'''
|-
| style="text-align:left" | ⏳ 未移行（SeesaaWikiのみ） || {s['seesaa_only']} || {remaining_pct}%
|-
| style="text-align:left" | 🐦 Miraheze独自（Twitter/YouTube等） || {s['miraheze_exclusive']} || —
|-
| style="text-align:left" | ✨ Miraheze新規記事 || {s['miraheze_new']} || —
|-
! 合計 (SeesaaWiki基準) !! {s['seesaa_total']} !! 100%
|}}

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

[[Category:管理]]
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
