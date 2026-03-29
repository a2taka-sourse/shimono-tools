"""
U+FA19 (神の旧字体) 専用 WOFF2 サブセットを生成し、
Base64 で CSS に直接埋め込む。

ファイルアップロード不要。外部CDN不要。
data/font-face.css に @font-face ルールを出力し、
sitewide_generator.py がそれを Common.css に組み込む。

対応フォント (どれか1つをダウンロードして使う):
  ① Source Han Serif JP (源ノ明朝) — 推奨
       https://github.com/adobe-fonts/source-han-serif/releases/latest
       → SourceHanSerifJP-Regular.otf をダウンロード

  ② IPAmj明朝
       https://moji.or.jp/ipamjfont/
       → IPAmjMincho.ttf をダウンロード

インストール:
  pip install fonttools brotli

使い方:
  python make_font_subset.py SourceHanSerifJP-Regular.otf

出力:
  data/ipamj-fa19-subset.woff2   — WOFF2 バイナリ (確認用)
  data/font-face.css             — Base64 埋め込み済み @font-face ルール

次のステップ:
  python run.py sitewide
  → data/common.css に @font-face が自動で含まれる
  → MediaWiki:Common.css の内容を data/common.css に置き換えるだけでOK
"""
import base64
import sys
from pathlib import Path

from config import DATA_DIR


TARGET_CODEPOINT = 0xFA19   # 神の旧字体 (CJK Compatibility Ideograph)
OTF_OUT     = "shimono-kami-fa19.otf"   # Miraheze アップロード用 (MIME: application/vnd.ms-opentype)
WOFF2_OUT   = "ipamj-fa19-subset.woff2" # ローカルテスト用
FONTCSS_OUT = "font-face.css"


def _check_deps() -> None:
    missing = []
    try:
        import fontTools  # noqa: F401
    except ImportError:
        missing.append("fonttools")
    try:
        import brotli  # noqa: F401
    except ImportError:
        missing.append("brotli")
    if missing:
        print(f"ERROR: 必要なライブラリが不足しています: {', '.join(missing)}")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)


def _has_distinct_glyph(font) -> bool:
    """U+FA19 と U+795E が別グリフかどうか確認する。"""
    cmap = font.getBestCmap()
    if TARGET_CODEPOINT not in cmap or 0x795E not in cmap:
        return False
    return cmap[TARGET_CODEPOINT] != cmap[0x795E]


def make_subset(font_path: str) -> None:
    _check_deps()

    from fontTools.subset import Subsetter, Options
    from fontTools.ttLib import TTFont

    src = Path(font_path)
    if not src.exists():
        print(f"ERROR: フォントファイルが見つかりません: {src}")
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    otf_out     = DATA_DIR / OTF_OUT
    woff2_out   = DATA_DIR / WOFF2_OUT
    fontcss_out = DATA_DIR / FONTCSS_OUT

    print(f"読み込み中: {src.name}")
    font = TTFont(str(src))

    cmap = font.getBestCmap()
    if TARGET_CODEPOINT not in cmap:
        print(f"ERROR: このフォントに U+{TARGET_CODEPOINT:04X} が含まれていません。")
        print("  Source Han Serif JP か IPAmjMincho を使用してください。")
        sys.exit(1)

    if _has_distinct_glyph(font):
        print(f"OK U+{TARGET_CODEPOINT:04X} の旧字体グリフを確認 (U+795E と別グリフ)")
    else:
        print(f"NG U+{TARGET_CODEPOINT:04X} は U+795E と同じグリフです。")
        print("  このフォントでは旧字体の見た目にならない可能性があります。")

    # ── OTF サブセット (Miraheze アップロード用) ──────────────────────
    # flavor=None → 圧縮なし OTF。MIME: application/vnd.ms-opentype
    # Miraheze の MIME 検出と一致するためアップロードが通る。
    options_otf = Options()
    options_otf.flavor = None
    options_otf.desubroutinize = True
    options_otf.retain_gids = False
    options_otf.name_IDs = []
    options_otf.layout_features = []

    font_otf = TTFont(str(src))
    subsetter_otf = Subsetter(options=options_otf)
    subsetter_otf.populate(unicodes=[TARGET_CODEPOINT])
    subsetter_otf.subset(font_otf)
    font_otf.save(str(otf_out))
    print(f"OTF 生成:   {otf_out.name}  ({otf_out.stat().st_size / 1024:.1f} KB)  ← Miraheze にアップロード")

    # ── WOFF2 サブセット + Base64 (ローカルテスト用) ─────────────────
    font_w2 = TTFont(str(src))
    options_w2 = Options()
    options_w2.flavor = "woff2"
    options_w2.desubroutinize = True
    options_w2.retain_gids = False
    options_w2.name_IDs = []
    options_w2.layout_features = []

    subsetter_w2 = Subsetter(options=options_w2)
    subsetter_w2.populate(unicodes=[TARGET_CODEPOINT])
    subsetter_w2.subset(font_w2)
    font_w2.save(str(woff2_out))
    print(f"WOFF2 生成: {woff2_out.name}  ({woff2_out.stat().st_size / 1024:.1f} KB)  ← ローカルテスト用")

    # ── font-face.css (Miraheze の Special:Filepath URL を使用) ──────
    font_face_css = f"""\
/* ================================================================
 * 下腦Wiki — U+FA19 旧字体フォント
 *
 * Source: {src.name}
 * U+FA19 (神の旧字体) の1グリフのみを収録したサブセット。
 * unicode-range 指定により U+FA19 を含む要素にのみ適用される。
 *
 * アップロード: Special:Upload → {OTF_OUT}
 * ================================================================ */
@font-face {{
    font-family: 'ShimonoKami';
    src: url('/wiki/Special:Filepath/{OTF_OUT}') format('opentype');
    unicode-range: U+FA19;
}}
"""
    fontcss_out.write_text(font_face_css, encoding="utf-8")
    print(f"CSS 生成:   {fontcss_out.name}")
    print()
    print("次のステップ:")
    print(f"  1. Miraheze にアップロード:")
    print(f"     https://shikabaton.miraheze.org/wiki/Special:Upload")
    print(f"     ファイル: {otf_out}  (拡張子: .otf)")
    print()
    print("  2. CSS/JS 再生成:")
    print("     python run.py sitewide")
    print()
    print("  3. MediaWiki:Common.css を data/common.css の内容に置き換え")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    make_subset(sys.argv[1])
