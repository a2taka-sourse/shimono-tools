from pathlib import Path

SEESAA_WIKI = "shikabatonnokakusekai"
SEESAA_BASE = f"https://seesaawiki.jp/{SEESAA_WIKI}"
SEESAA_LIST = f"{SEESAA_BASE}/l/"
SEESAA_ENCODING = "euc_jis_2004"

MIRAHEZE_WIKI = "shikabaton"
MIRAHEZE_API = f"https://{MIRAHEZE_WIKI}.miraheze.org/w/api.php"
MIRAHEZE_BASE = f"https://{MIRAHEZE_WIKI}.miraheze.org/wiki"

REQUEST_DELAY = 1.2  # seconds between requests

VAULT_ROOT = Path(__file__).parent.parent
DATA_DIR = Path(__file__).parent / "data"
INBOX_DIR = VAULT_ROOT / "inbox"

# Paths
SEESAA_JSON     = DATA_DIR / "seesaa_articles.json"
MIRAHEZE_JSON   = DATA_DIR / "miraheze_articles.json"
STATUS_JSON     = DATA_DIR / "migration_status.json"
CORPUS_JSON     = DATA_DIR / "seesaa_full_corpus.json"
CHANGELOG_JSON  = DATA_DIR / "seesaa_changelog.json"
WORLD_JSON      = DATA_DIR / "world_history.json"
WORLD_CSV_OUT   = DATA_DIR / "world_history_structured.csv"
WORLD_CSV_IN    = INBOX_DIR / "架空世界動的全史 - シート1.csv"

# Miraheze visualization page title
MIGRATION_PAGE_TITLE = "下腦Wiki移行状況"

# Articles on Miraheze that are NOT migrated from SeesaaWiki
# (Twitter archives, YouTube lists, etc.)
MIRAHEZE_EXCLUSIVE_PATTERNS = [
    "Twitter", "YouTube", "動画一覧", "ツイート", "移行状況",
]

# Major edit detection thresholds (from shimono_knowledge_v1.md §7-5)
MAJOR_THRESHOLDS = {"add_lines": 5, "del_lines": 3}
MAJOR_KEYWORDS = [
    "新設", "作成", "追加", "改定", "建国", "戦争", "条約",
    "滅亡", "独立", "創設", "廃止", "改名",
]
