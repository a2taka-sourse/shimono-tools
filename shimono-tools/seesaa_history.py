"""
SeesaaWiki edit history scraper — 重要変更史 (major change history) data source.

URL patterns (from shimono_knowledge_v1.md §7-2):
  History:  https://seesaawiki.jp/WIKI/history/PAGE_NAME
  Diff:     https://seesaawiki.jp/WIKI/diff/PAGE_NAME/REVISION_ID

Output: data/seesaa_changelog.json
  Per-article list of revisions with is_major flag.
"""
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from config import (
    SEESAA_BASE, SEESAA_WIKI, SEESAA_ENCODING,
    REQUEST_DELAY, DATA_DIR,
    MAJOR_THRESHOLDS, MAJOR_KEYWORDS,
)


def _get(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=30, headers={"User-Agent": "ShimonoBot/1.0"})
    resp.encoding = SEESAA_ENCODING
    resp.raise_for_status()
    time.sleep(REQUEST_DELAY)
    return BeautifulSoup(resp.text, "html.parser")


def _encode_title(title: str) -> str:
    """URL-encode article title in EUC-JP for SeesaaWiki URLs."""
    return quote(title.encode(SEESAA_ENCODING))


def _is_major(add_lines: int, del_lines: int, comment: str) -> bool:
    if add_lines >= MAJOR_THRESHOLDS["add_lines"]:
        return True
    if del_lines >= MAJOR_THRESHOLDS["del_lines"]:
        return True
    if any(kw in comment for kw in MAJOR_KEYWORDS):
        return True
    return False


def get_history(title: str) -> list[dict]:
    """
    Fetch all revisions for a single article.
    Returns list of revision dicts.
    """
    encoded = _encode_title(title)
    url = f"{SEESAA_BASE}/history/{encoded}"

    try:
        soup = _get(url)
    except requests.HTTPError:
        return []

    revisions = []

    # SeesaaWiki history page: table rows with revision data
    # Row structure varies by wiki version; we try multiple patterns
    for row in soup.select("table tr, ul li"):
        text = row.get_text(" ", strip=True)

        # Skip header rows
        if re.search(r"日時|編集者|コメント", text) and not re.search(r"\d{4}", text):
            continue

        # Look for a diff link to confirm this is a revision row
        diff_link = row.find("a", href=re.compile(r"/diff/"))
        if not diff_link:
            continue

        href = diff_link.get("href", "")
        rev_match = re.search(r"/diff/[^/]+/(\d+)", href)
        rev_id = rev_match.group(1) if rev_match else ""

        # Extract date (YYYY-MM-DD or similar)
        date_match = re.search(r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}", text)
        date = date_match.group(0) if date_match else ""

        # Extract +N/-N diff stats
        add_match = re.search(r"\+(\d+)", text)
        del_match = re.search(r"-(\d+)", text)
        add_lines = int(add_match.group(1)) if add_match else 0
        del_lines = int(del_match.group(1)) if del_match else 0

        # Comment — text after diff stats, rough heuristic
        comment_match = re.search(r"[+\-]\d+\s+(.+)$", text)
        comment = comment_match.group(1).strip() if comment_match else ""

        revisions.append({
            "revision_id": rev_id,
            "date": date,
            "comment": comment,
            "add_lines": add_lines,
            "del_lines": del_lines,
            "is_major": _is_major(add_lines, del_lines, comment),
            "diff_url": f"{SEESAA_BASE}/diff/{encoded}/{rev_id}",
        })

    return revisions


def scrape_all_history(output_path: Path | None = None) -> list[dict]:
    """
    Fetch edit history for all articles in seesaa_articles.json.
    Requires seesaa_articles.json to exist — run `python run.py list` first.
    """
    output_path = output_path or DATA_DIR / "seesaa_changelog.json"
    list_path = DATA_DIR / "seesaa_articles.json"

    if not list_path.exists():
        print("ERROR: data/seesaa_articles.json not found. Run `python run.py list` first.")
        return []

    articles = json.loads(list_path.read_text(encoding="utf-8"))
    print(f"=== 編集履歴取得 ({len(articles)}記事) ===")

    changelog = []
    for i, article in enumerate(articles):
        title = article["title"]
        print(f"  [{i+1}/{len(articles)}] {title}")
        try:
            revisions = get_history(title)
            major = [r for r in revisions if r["is_major"]]
            changelog.append({
                "article_title": title,
                "article_url": article["url"],
                "total_revisions": len(revisions),
                "major_revisions": major,
                "all_revisions": revisions,
            })
        except Exception as e:
            print(f"    ERROR: {e}")
            changelog.append({
                "article_title": title,
                "article_url": article["url"],
                "total_revisions": 0,
                "major_revisions": [],
                "all_revisions": [],
                "error": str(e),
            })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(changelog, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total_rev = sum(a["total_revisions"] for a in changelog)
    total_major = sum(len(a["major_revisions"]) for a in changelog)
    print(f"\n編集履歴合計: {total_rev}件 (重大変更: {total_major}件)")
    print(f"保存: {output_path}")
    return changelog


if __name__ == "__main__":
    scrape_all_history()
