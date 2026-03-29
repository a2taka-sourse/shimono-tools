"""
半自動記事移行レビューワークフロー。

未移行記事を1件ずつ表示し、Go/Skip/タイトル変更を選んで移行する。
キューの状態は data/review_queue.json に保存し、中断・再開が可能。

使い方:
  python run.py review          # レビュー開始 (前回の続きから)
  python run.py review --reset  # キューをリセットして最初から
"""
import io
import json
import os
import sys
import time
from pathlib import Path

import requests

from config import (
    DATA_DIR, MIRAHEZE_API, MIRAHEZE_WIKI,
    SEESAA_BASE, STATUS_JSON,
)
from seesaa_scraper import get_article_content
from seesaa_converter import html_to_wikitext

# Windows コンソールの文字化け対策
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

QUEUE_JSON = DATA_DIR / "review_queue.json"
REVIEW_LOG = DATA_DIR / "review_log.json"


# ── キュー管理 ────────────────────────────────────────────────────────────────

def build_queue() -> list[dict]:
    """migration_status.json の seesaa_only からキューを生成する。"""
    if not STATUS_JSON.exists():
        print("ERROR: migration_status.json がありません。先に run.py compare を実行してください。")
        sys.exit(1)

    status = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    items = []
    for a in status["seesaa_only"]:
        title = a.get("title") if isinstance(a, dict) else str(a)
        url   = a.get("seesaa_url", f"{SEESAA_BASE}/d/{title}") if isinstance(a, dict) else f"{SEESAA_BASE}/d/{title}"
        items.append({
            "title":          title,
            "seesaa_url":     url,
            "target_title":   title,   # 変更可能
            "status":         "pending",  # pending | done | skipped
            "pushed_at":      None,
        })
    return items


def load_queue() -> list[dict]:
    if QUEUE_JSON.exists():
        return json.loads(QUEUE_JSON.read_text(encoding="utf-8"))
    return build_queue()


def save_queue(queue: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_JSON.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")


def _log(entry: dict) -> None:
    log = []
    if REVIEW_LOG.exists():
        log = json.loads(REVIEW_LOG.read_text(encoding="utf-8"))
    log.append(entry)
    REVIEW_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Miraheze API ──────────────────────────────────────────────────────────────

def _get_csrf_token(session: requests.Session, username: str, password: str) -> str:
    r = session.get(MIRAHEZE_API, params={
        "action": "query", "meta": "tokens", "type": "login", "format": "json"
    })
    login_token = r.json()["query"]["tokens"]["logintoken"]

    r = session.post(MIRAHEZE_API, data={
        "action": "login", "lgname": username,
        "lgpassword": password, "lgtoken": login_token, "format": "json",
    })
    if r.json()["login"]["result"] != "Success":
        raise ValueError(f"ログイン失敗: {r.json()['login']['result']}")

    r = session.get(MIRAHEZE_API, params={
        "action": "query", "meta": "tokens", "format": "json"
    })
    return r.json()["query"]["tokens"]["csrftoken"]


def _push_article(session: requests.Session, title: str,
                  wikitext: str, summary: str, token: str) -> bool:
    r = session.post(MIRAHEZE_API, data={
        "action":   "edit",
        "title":    title,
        "text":     wikitext,
        "summary":  summary,
        "token":    token,
        "format":   "json",
        "createonly": "1",   # 既存ページを上書きしない
    })
    result = r.json()
    if result.get("edit", {}).get("result") == "Success":
        return True
    err = result.get("error", {})
    if err.get("code") == "articleexists":
        print(f"  ! {title}: すでに存在します。Skipします。")
    else:
        print(f"  ! エラー: {result}")
    return False


# ── レビューループ ────────────────────────────────────────────────────────────

def _print_divider(label: str = "") -> None:
    width = 60
    print("\n" + "━" * width)
    if label:
        print(label)


def _show_preview(item: dict, index: int, total: int) -> None:
    _print_divider(f"[{index}/{total}] {item['title']}")
    if item["title"] != item["target_title"]:
        print(f"  → 移行先タイトル: {item['target_title']}")
    print(f"  SeesaaWiki: {item['seesaa_url']}")
    print(f"  Miraheze:   https://{MIRAHEZE_WIKI}.miraheze.org/wiki/{item['target_title'].replace(' ', '_')}")
    print()


def _fetch_preview(item: dict) -> str:
    """記事の冒頭テキスト200字を取得（失敗時は空文字）。"""
    try:
        art = get_article_content({"title": item["title"], "url": item["seesaa_url"]})
        text = art.get("content_text", "").strip()
        return text[:200] + ("…" if len(text) > 200 else "")
    except Exception as e:
        return f"（取得失敗: {e}）"


def _fetch_and_convert(item: dict) -> str:
    """SeesaaWiki本文を取得してwikitextに変換する。"""
    art = get_article_content({"title": item["title"], "url": item["seesaa_url"]})
    return html_to_wikitext(art.get("content_html", ""))


def review_loop(reset: bool = False) -> None:
    username = os.getenv("MIRAHEZE_BOT_USER")
    password = os.getenv("MIRAHEZE_BOT_PASSWORD")
    if not username or not password:
        print("ERROR: .env に MIRAHEZE_BOT_USER / MIRAHEZE_BOT_PASSWORD を設定してください。")
        sys.exit(1)

    if reset or not QUEUE_JSON.exists():
        queue = build_queue()
        save_queue(queue)
        print(f"キューを生成しました: {len(queue)}件")

    queue = load_queue()
    pending = [i for i, q in enumerate(queue) if q["status"] == "pending"]
    total   = len(queue)
    done    = sum(1 for q in queue if q["status"] == "done")
    skipped = sum(1 for q in queue if q["status"] == "skipped")

    print(f"\n=== 移行レビュー ===")
    print(f"合計: {total}件  完了: {done}  Skip: {skipped}  残り: {len(pending)}")
    if not pending:
        print("残りの記事はありません。")
        return

    # Mirahezeにログイン
    print("Mirahezeにログイン中...")
    session = requests.Session()
    session.headers["User-Agent"] = "ShimonoMigrationBot/1.0"
    try:
        token = _get_csrf_token(session, username, password)
        print("ログイン成功\n")
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    for idx_in_pending, qi in enumerate(pending):
        item = queue[qi]
        pos  = done + idx_in_pending + 1

        _show_preview(item, pos, total)

        # 冒頭プレビューを取得
        print("  内容を取得中...")
        preview = _fetch_preview(item)
        print(f"\n{preview}\n")

        while True:
            print("  [g] Go  [s] Skip  [t] タイトル変更してGo  [p] wikitext全文表示  [q] 終了")
            choice = input("  > ").strip().lower()

            if choice == "q":
                save_queue(queue)
                print(f"\n中断しました。({done + idx_in_pending}件完了)")
                return

            elif choice == "s":
                queue[qi]["status"] = "skipped"
                save_queue(queue)
                print("  → Skip")
                break

            elif choice == "t":
                new_title = input("  移行先タイトルを入力: ").strip()
                if new_title:
                    queue[qi]["target_title"] = new_title
                    item = queue[qi]
                    print(f"  → タイトルを「{new_title}」に変更しました。")

            elif choice == "p":
                print("\n取得・変換中...")
                wikitext = _fetch_and_convert(item)
                print("\n" + "─" * 60)
                print(wikitext[:2000])
                if len(wikitext) > 2000:
                    print(f"... (以下 {len(wikitext)-2000}文字省略)")
                print("─" * 60 + "\n")

            elif choice == "g":
                print("  変換・プッシュ中...")
                try:
                    wikitext = _fetch_and_convert(item)
                    target   = item["target_title"]
                    summary  = f"SeesaaWikiより移行: [[{item['title']}]]"
                    ok = _push_article(session, target, wikitext, summary, token)
                    if ok:
                        queue[qi]["status"]    = "done"
                        queue[qi]["pushed_at"] = time.strftime("%Y-%m-%d %H:%M")
                        save_queue(queue)
                        url = f"https://{MIRAHEZE_WIKI}.miraheze.org/wiki/{target.replace(' ', '_')}"
                        print(f"  ✓ 完了: {url}")
                        _log({"title": item["title"], "target": target,
                              "url": url, "at": queue[qi]["pushed_at"]})
                    else:
                        queue[qi]["status"] = "skipped"
                        save_queue(queue)
                except Exception as e:
                    print(f"  ! 失敗: {e}")
                break

    save_queue(queue)
    done_now = sum(1 for q in queue if q["status"] == "done")
    print(f"\n=== セッション終了 ===  完了: {done_now}/{total}件")
