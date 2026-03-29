"""
Miraheze MediaWiki API client — article list retrieval.

Endpoints used:
  action=query&list=allpages   → full article list with pagination
  action=query&prop=categories → category membership per article
"""
import json
from pathlib import Path

import requests

from config import MIRAHEZE_API, MIRAHEZE_BASE, DATA_DIR


def get_all_pages(namespace: int = 0) -> list[dict]:
    """
    Fetch all pages from Miraheze via MediaWiki allpages API.
    Handles continuation automatically.
    """
    pages = []
    params: dict = {
        "action": "query",
        "list": "allpages",
        "aplimit": 500,
        "apnamespace": namespace,
        "format": "json",
    }

    while True:
        resp = requests.get(MIRAHEZE_API, params=params, timeout=30,
                            headers={"User-Agent": "ShimonoBot/1.0"})
        resp.raise_for_status()
        data = resp.json()

        batch = data["query"]["allpages"]
        pages.extend(batch)
        print(f"  取得中: {len(pages)}件...")

        if "continue" not in data:
            break
        params["apcontinue"] = data["continue"]["apcontinue"]

    return pages


def get_categories_for(titles: list[str]) -> dict[str, list[str]]:
    """
    Fetch category membership for a list of page titles.
    Returns {title: [category_name, ...]} mapping.
    """
    cat_map: dict[str, list[str]] = {}

    for i in range(0, len(titles), 50):
        batch = titles[i : i + 50]
        params = {
            "action": "query",
            "prop": "categories",
            "titles": "|".join(batch),
            "cllimit": 100,
            "format": "json",
        }
        resp = requests.get(MIRAHEZE_API, params=params, timeout=30,
                            headers={"User-Agent": "ShimonoBot/1.0"})
        resp.raise_for_status()
        data = resp.json()

        for page_data in data["query"]["pages"].values():
            title = page_data["title"]
            cats = [
                c["title"].removeprefix("Category:")
                for c in page_data.get("categories", [])
            ]
            cat_map[title] = cats

    return cat_map


def save_pages(output_path: Path | None = None) -> list[dict]:
    """Fetch all Miraheze pages and save to JSON."""
    output_path = output_path or DATA_DIR / "miraheze_articles.json"
    print("=== Miraheze 記事一覧取得 ===")

    pages = get_all_pages()
    print(f"合計 {len(pages)} 件")

    # Add full URLs
    for p in pages:
        p["url"] = f"{MIRAHEZE_BASE}/{p['title'].replace(' ', '_')}"

    # Fetch categories for all pages
    print("カテゴリ情報取得中...")
    titles = [p["title"] for p in pages]
    cat_map = get_categories_for(titles)
    for p in pages:
        p["categories"] = cat_map.get(p["title"], [])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"保存: {output_path}")
    return pages


if __name__ == "__main__":
    save_pages()
