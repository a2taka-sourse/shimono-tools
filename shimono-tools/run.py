#!/usr/bin/env python3
"""
shimono-tools — SeesaaWiki → Miraheze移行トラッカー & 下腦世界史データ整備

コマンド:
  list        SeesaaWikiとMirahezeの記事一覧を取得
  compare     両Wikiを突き合わせて移行状況を生成
  preview     移行状況wikitextをローカルに出力（Botなしで確認可）
  publish     移行状況ページをMirahezeに反映（Bot設定が必要）
  corpus      SeesaaWiki全文取得（RAGコーパス用・時間がかかる）
  history     SeesaaWiki編集履歴取得（重要変更史用）
  world       動的全史CSVを構造化データに変換
  sitewide    Common.css/jsを生成→プレビュー or Mirahezeに反映
  all         list + compare + preview を一括実行

使い方:
  python run.py all
  python run.py list
  python run.py compare
  python run.py preview
  python run.py publish        # .envにBot認証情報が必要
  python run.py sitewide       # CSS/JSをdata/に生成（手動コピー用）
  python run.py sitewide push  # interface-admin付与後にBot経由でプッシュ
  python run.py world
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def cmd_list():
    from seesaa_scraper import scrape_list
    from miraheze_client import save_pages
    scrape_list()
    save_pages()


def cmd_compare():
    _require("data/seesaa_articles.json", "seesaa_articles.json")
    _require("data/miraheze_articles.json", "miraheze_articles.json")
    from compare import compare
    compare()


def cmd_preview():
    _require("data/migration_status.json", "migration_status.json")
    from miraheze_publisher import preview
    preview()


def cmd_publish():
    _require("data/migration_status.json", "migration_status.json")
    from miraheze_publisher import push
    push()


def cmd_corpus():
    from seesaa_scraper import scrape_full_corpus
    scrape_full_corpus()


def cmd_history():
    _require("data/seesaa_articles.json", "seesaa_articles.json")
    from seesaa_history import scrape_all_history
    scrape_all_history()


def cmd_world():
    from world_history import convert
    convert()


def cmd_review():
    from review_queue import review_loop
    reset = len(sys.argv) > 2 and sys.argv[2] == "--reset"
    review_loop(reset=reset)


def cmd_sitewide():
    from sitewide_generator import push_sitewide, preview_sitewide
    if len(sys.argv) > 2 and sys.argv[2] == "push":
        push_sitewide()
    else:
        preview_sitewide()


def cmd_all():
    cmd_list()
    cmd_compare()
    cmd_preview()


def _require(path: str, name: str):
    if not (Path(__file__).parent / path).exists():
        cmd = name.replace("seesaa_articles", "list").replace(
            "miraheze_articles", "list").replace("migration_status", "compare")
        print(f"ERROR: {path} が存在しません。先に `python run.py list` を実行してください。")
        sys.exit(1)


COMMANDS = {
    "list":     cmd_list,
    "compare":  cmd_compare,
    "preview":  cmd_preview,
    "publish":  cmd_publish,
    "corpus":   cmd_corpus,
    "history":  cmd_history,
    "world":    cmd_world,
    "sitewide": cmd_sitewide,
    "review":   cmd_review,
    "all":      cmd_all,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(0 if len(sys.argv) < 2 else 1)

    COMMANDS[sys.argv[1]]()
