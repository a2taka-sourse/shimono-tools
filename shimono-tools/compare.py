"""
Compare SeesaaWiki and Miraheze article lists.
Produces migration_status.json for the visualization page.

Article classifications:
  migrated           — exists on both wikis (title match)
  seesaa_only        — on SeesaaWiki, not yet on Miraheze
  miraheze_exclusive — on Miraheze only, clearly not migrated content
                       (Twitter archives, YouTube lists, etc.)
  miraheze_new       — on Miraheze only, new original content
"""
import json
import re
from pathlib import Path

from config import DATA_DIR, MIRAHEZE_EXCLUSIVE_PATTERNS


# SeesaaWiki uses JIS X 0213 characters that Miraheze normalizes to modern forms.
# Map old/variant forms → modern Unicode equivalents for title matching.
# These substitutions apply ONLY to comparison — display titles are unchanged.
CHAR_NORMALIZE: dict[str, str] = {
    "\u85ed": "神",   # 藭 (U+85ED, JIS X 0213 旧字体) → 神
    # Add more mappings here as new collisions are discovered
}


def _normalize(title: str) -> str:
    """
    Normalize title for fuzzy matching.
    Handles:
      - leading/trailing whitespace
      - underscore ↔ space
      - namespace prefix stripping
      - JIS X 0213 旧字体 → modern Unicode substitution (e.g. 藭→神)
    """
    title = title.strip().replace("_", " ")
    # Strip namespace prefixes
    for ns in ("Category:", "Template:", "Help:", "MediaWiki:", "File:"):
        if title.startswith(ns):
            return ""
    # Apply character normalization (旧字体 → 新字体)
    for old, new in CHAR_NORMALIZE.items():
        title = title.replace(old, new)
    return title.lower()


def _is_exclusive(title: str) -> bool:
    """True if the Miraheze page is clearly not a SeesaaWiki migration."""
    return any(re.search(pat, title) for pat in MIRAHEZE_EXCLUSIVE_PATTERNS)


def compare(
    seesaa_path: Path | None = None,
    miraheze_path: Path | None = None,
    output_path: Path | None = None,
) -> dict:
    seesaa_path  = seesaa_path  or DATA_DIR / "seesaa_articles.json"
    miraheze_path = miraheze_path or DATA_DIR / "miraheze_articles.json"
    output_path  = output_path  or DATA_DIR / "migration_status.json"

    seesaa   = json.loads(seesaa_path.read_text(encoding="utf-8"))
    miraheze = json.loads(miraheze_path.read_text(encoding="utf-8"))

    # Build normalized Miraheze lookup: norm_title → page_dict
    mira_lookup: dict[str, dict] = {}
    for p in miraheze:
        norm = _normalize(p["title"])
        if norm:
            mira_lookup[norm] = p

    # Classify SeesaaWiki articles
    migrated: list[dict] = []
    seesaa_only: list[dict] = []
    seesaa_norms: set[str] = set()

    for a in seesaa:
        norm = _normalize(a["title"])
        seesaa_norms.add(norm)

        if norm in mira_lookup:
            migrated.append({
                "title": a["title"],
                "seesaa_url": a["url"],
                "miraheze_url": mira_lookup[norm]["url"],
                "status": "migrated",
            })
        else:
            seesaa_only.append({
                "title": a["title"],
                "seesaa_url": a["url"],
                "status": "seesaa_only",
            })

    # Classify Miraheze-only articles
    miraheze_exclusive: list[dict] = []
    miraheze_new: list[dict] = []

    for p in miraheze:
        norm = _normalize(p["title"])
        if not norm or norm in seesaa_norms:
            continue
        entry = {"title": p["title"], "miraheze_url": p["url"],
                 "categories": p.get("categories", [])}
        if _is_exclusive(p["title"]):
            miraheze_exclusive.append(entry)
        else:
            miraheze_new.append(entry)

    total = len(seesaa)
    pct = round(len(migrated) / total * 100, 1) if total else 0.0

    result = {
        "stats": {
            "seesaa_total":        total,
            "migrated":            len(migrated),
            "migration_pct":       pct,
            "seesaa_only":         len(seesaa_only),
            "miraheze_exclusive":  len(miraheze_exclusive),
            "miraheze_new":        len(miraheze_new),
        },
        "migrated":           migrated,
        "seesaa_only":        seesaa_only,
        "miraheze_exclusive": miraheze_exclusive,
        "miraheze_new":       miraheze_new,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    s = result["stats"]
    print("\n=== 移行状況 ===")
    print(f"SeesaaWiki 総記事数 : {s['seesaa_total']}")
    print(f"移行済み            : {s['migrated']} ({s['migration_pct']}%)")
    print(f"未移行              : {s['seesaa_only']}")
    print(f"Miraheze独自(排他)  : {s['miraheze_exclusive']}  (Twitter/YouTube等)")
    print(f"Miraheze独自(新規)  : {s['miraheze_new']}")
    print(f"\n保存: {output_path}")
    return result


if __name__ == "__main__":
    compare()
