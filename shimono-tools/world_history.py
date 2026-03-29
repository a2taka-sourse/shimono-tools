"""
Convert 架空世界動的全史 CSV to structured timeline_events format.

Input CSV:  国,年,出来事   (from inbox/架空世界動的全史 - シート1.csv)
Output:     data/world_history.json         — structured for timeline_events DB
            data/world_history_structured.csv — spreadsheet-friendly

Column mapping to RAG schema (shikabaton_rag_design.md §4-2):
  国       → entity_name
  年       → world_date  (raw) + world_era (inferred)
  出来事   → description + event_type (inferred)
"""
import csv
import json
import re
from pathlib import Path

from config import DATA_DIR, WORLD_CSV_IN


# ── Era classification ──────────────────────────────────────────────────────

ERA_RANGES = [
    (0,    999,  "古代"),
    (1000, 1399, "中世"),
    (1400, 1799, "近世"),
    (1800, 1899, "近代初期"),
    (1900, 1930, "大戦前"),
    (1931, 1945, "世界大戦期"),
    (1946, 1979, "戦後"),
    (1980, 2099, "現代"),
]

EVENT_KEYWORDS: dict[str, list[str]] = {
    "建国": ["建国", "樹立", "成立", "設立", "創設", "建設"],
    "滅亡": ["滅亡", "滅ぼ", "廃止", "崩壊", "消滅", "廃国"],
    "戦争": ["戦争", "戦い", "侵攻", "攻撃", "軍事", "クーデター",
             "革命", "蜂起", "動乱", "内乱", "反乱", "開戦"],
    "条約": ["条約", "合意", "協定", "締結", "講和"],
    "改名": ["改称", "改名", "改組"],
    "降伏": ["降伏", "無条件降伏"],
    "独立": ["独立", "自治"],
    "割譲": ["割譲", "占領", "併合"],
    "即位": ["即位", "就任", "大統領", "首相", "皇帝", "将軍"],
}


def _parse_year(raw: str) -> tuple[int | None, str]:
    """Return (numeric_year_or_None, normalized_world_date_string)."""
    raw = raw.strip()

    # "18世紀" / "7世紀"
    m = re.match(r"(\d+)世紀", raw)
    if m:
        return (int(m.group(1)) - 1) * 100 + 50, raw

    # "1765-1769年"
    m = re.match(r"(\d+)-\d+年", raw)
    if m:
        return int(m.group(1)), raw

    # "1931年2月20日" / "1931年"
    m = re.match(r"(\d+)年", raw)
    if m:
        return int(m.group(1)), raw

    # Fallback: find any 4-digit year
    m = re.search(r"(\d{4})", raw)
    if m:
        return int(m.group(1)), raw

    return None, raw


def _get_era(year: int | None) -> str:
    if year is None:
        return "不明"
    for lo, hi, era in ERA_RANGES:
        if lo <= year <= hi:
            return era
    return "不明"


def _infer_event_type(description: str) -> str:
    for event_type, keywords in EVENT_KEYWORDS.items():
        if any(kw in description for kw in keywords):
            return event_type
    return "その他"


def convert(
    input_path: Path | None = None,
    output_json: Path | None = None,
    output_csv: Path | None = None,
) -> list[dict]:
    input_path  = input_path  or WORLD_CSV_IN
    output_json = output_json or DATA_DIR / "world_history.json"
    output_csv  = output_csv  or DATA_DIR / "world_history_structured.csv"

    if not input_path.exists():
        print(f"ERROR: CSVが見つかりません: {input_path}")
        return []

    print(f"=== 動的全史 変換 ===")
    print(f"入力: {input_path}")

    events: list[dict] = []

    with input_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nation      = (row.get("国") or "").strip()
            year_raw    = (row.get("年") or "").strip()
            description = (row.get("出来事") or "").strip()

            if not description:
                continue

            year_int, world_date = _parse_year(year_raw)
            events.append({
                "world_date":    world_date,
                "world_era":     _get_era(year_int),
                "entity_name":   nation,
                "event_type":    _infer_event_type(description),
                "description":   description,
                "canon_status":  "canon",
                "source_type":   "csv_import",
                "source_url":    "",
                "revision_note": "",
                "_sort_year":    year_int or 0,   # internal only
            })

    # Sort chronologically within each nation
    events.sort(key=lambda e: (e["_sort_year"], e["entity_name"]))
    for e in events:
        del e["_sort_year"]

    # ── Save JSON ────────────────────────────────────────────────────────────
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ── Save structured CSV ──────────────────────────────────────────────────
    fieldnames = [
        "world_date", "world_era", "entity_name", "event_type",
        "description", "canon_status", "source_type", "source_url", "revision_note",
    ]
    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)

    # ── Summary ──────────────────────────────────────────────────────────────
    from collections import Counter
    era_dist   = Counter(e["world_era"] for e in events)
    type_dist  = Counter(e["event_type"] for e in events)
    nation_cnt = len({e["entity_name"] for e in events})

    print(f"\n変換結果: {len(events)}件 / {nation_cnt}国")
    print("\n時代別:")
    for era, cnt in sorted(era_dist.items()):
        print(f"  {era}: {cnt}件")
    print("\nイベント種別 (上位):")
    for etype, cnt in type_dist.most_common(8):
        print(f"  {etype}: {cnt}件")
    print(f"\n保存:")
    print(f"  JSON: {output_json}")
    print(f"  CSV:  {output_csv}")

    return events


if __name__ == "__main__":
    convert()
