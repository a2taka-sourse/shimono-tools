"""
SeesaaWiki scraper — article list and full content.

URL patterns (from shimono_knowledge_v1.md §7-2):
  Page list:  https://seesaawiki.jp/WIKI/l/
  Article:    https://seesaawiki.jp/WIKI/d/PAGE_NAME
  Encoding:   euc_jis_2004
"""
import json
import re
import time
from pathlib import Path
from urllib.parse import unquote, urljoin

import requests
from bs4 import BeautifulSoup

from config import (
    SEESAA_BASE, SEESAA_LIST, SEESAA_WIKI,
    SEESAA_ENCODING, REQUEST_DELAY, DATA_DIR,
)


def _get(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=30, headers={"User-Agent": "ShimonoBot/1.0"})
    resp.encoding = SEESAA_ENCODING
    resp.raise_for_status()
    time.sleep(REQUEST_DELAY)
    return BeautifulSoup(resp.text, "html.parser")


def get_article_list() -> list[dict]:
    """
    Scrape all article titles from the /l/ index pages.
    Handles pagination automatically.
    """
    articles = []
    seen_titles: set[str] = set()
    page = 1

    while True:
        url = SEESAA_LIST if page == 1 else f"{SEESAA_LIST}?page={page}"
        print(f"  記事一覧 page {page}: {url}")

        try:
            soup = _get(url)
        except requests.HTTPError as e:
            print(f"  HTTP {e.response.status_code} — ページ終端と判断")
            break

        # SeesaaWiki /l/ lists articles as links containing /d/
        raw_links = soup.select(f'a[href*="/{SEESAA_WIKI}/d/"]')

        # Filter out edit/history/etc. links — keep only article links
        new_found = 0
        for a in raw_links:
            href = a.get("href", "")
            # Must match exactly /WIKI/d/TITLE (no trailing path segments)
            m = re.match(rf".*/{re.escape(SEESAA_WIKI)}/d/([^/?#]+)$", href)
            if not m:
                continue

            encoded_name = m.group(1)
            # Decode EUC-JP URL encoding
            try:
                title = unquote(encoded_name, encoding=SEESAA_ENCODING)
            except Exception:
                title = unquote(encoded_name)

            # Skip MenuBar, FrontPage, and other system pages
            if title in seen_titles or title.startswith(("MenuBar", "SideBar")):
                continue

            seen_titles.add(title)
            articles.append({
                "title": title,
                "url": urljoin("https://seesaawiki.jp", href),
                "encoded_name": encoded_name,
            })
            new_found += 1

        print(f"  → {new_found}件追加 (累計 {len(articles)}件)")

        if new_found == 0:
            break

        # Check for next-page link
        next_link = soup.find("a", string=re.compile(r"次[のへ]?|Next|>>"))
        if not next_link:
            break
        page += 1

    return articles


def get_article_content(article: dict) -> dict:
    """Scrape full text content of a single article page."""
    soup = _get(article["url"])

    # SeesaaWiki content area — try common selectors in priority order
    content_div = (
        soup.find("div", id="content_block_0")
        or soup.find("div", class_="wiki-content")
        or soup.find("div", id="main")
        or soup.find("article")
    )

    content_text = content_div.get_text("\n", strip=True) if content_div else ""
    content_html = str(content_div) if content_div else ""

    # Last-modified date
    last_modified = ""
    for selector in [{"name": "time"}, {"class_": "update"}, {"class_": "lastmodified"}]:
        tag = soup.find(**selector)
        if tag:
            last_modified = tag.get_text(strip=True)
            break

    return {**article, "content_text": content_text, "content_html": content_html, "last_modified": last_modified}


def scrape_list(output_path: Path | None = None) -> list[dict]:
    """Fetch article list only (fast). Saves to data/seesaa_articles.json."""
    output_path = output_path or DATA_DIR / "seesaa_articles.json"
    print("=== SeesaaWiki 記事一覧取得 ===")
    articles = get_article_list()
    print(f"合計 {len(articles)} 件")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"保存: {output_path}")
    return articles


def scrape_full_corpus(output_path: Path | None = None) -> list[dict]:
    """
    Fetch full article content for RAG corpus (slow — ~214 requests).
    Saves to data/seesaa_full_corpus.json.
    """
    output_path = output_path or DATA_DIR / "seesaa_full_corpus.json"
    print("=== SeesaaWiki 全文取得 (RAGコーパス) ===")

    # Load existing list or re-scrape
    list_path = DATA_DIR / "seesaa_articles.json"
    if list_path.exists():
        articles = json.loads(list_path.read_text(encoding="utf-8"))
        print(f"既存リストから {len(articles)} 件読み込み")
    else:
        articles = get_article_list()

    results = []
    for i, article in enumerate(articles):
        print(f"  [{i+1}/{len(articles)}] {article['title']}")
        try:
            results.append(get_article_content(article))
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append({**article, "content_text": "", "content_html": "", "error": str(e)})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n全文コーパス保存: {output_path}")
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="全文も取得する（遅い）")
    args = parser.parse_args()

    if args.full:
        scrape_full_corpus()
    else:
        scrape_list()
