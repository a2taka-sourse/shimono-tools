"""
Miraheze サイト全体設定の生成・プッシュ。

対象ページ:
  MediaWiki:Common.css  — 旧字体フォント設定
  MediaWiki:Common.js   — 地名検知→旧字体スパン置換スクリプト

Bot権限要件:
  interface-admin グループが必要。
  Special:UserRights でボットアカウント (Shikabaton@MigrationBot) に付与すること。

ローカル生成のみ (push なし) は:
  python sitewide_generator.py preview
"""
import os
import json
from pathlib import Path

import requests

from config import MIRAHEZE_API, MIRAHEZE_WIKI, DATA_DIR


# ── 旧字体マッピング ──────────────────────────────────────────────────────────
# JS が 神 (U+795E) を U+FA19 (CJK Compatibility Ideograph) に置換して表示する。
#
# なぜ U+FA19 が使えるか:
#   NFC 正規化で U+FA19→U+795E になるのは MediaWiki への保存時のみ。
#   JS は DOM を操作するだけで MediaWiki に保存しない。
#   ブラウザは DOM の文字コードをそのままフォントに渡すので NFC は発生しない。
#   → span.textContent = "\uFA19..." とすれば U+FA19 がレンダリングされる。
#
# フォント要件:
#   U+FA19 の旧字体グリフ（示 radical 形）を持つフォントが必要。
#   IPAmjMincho は U+FA19 の別グリフを明示的にサポートしている。
#
# ここに1行追加するだけで対象語を増やせる（メモレベルの実装）。
KAMI_MAP: dict[str, str] = {
    "神華": "\uFA19華",   # 大神華連邦・神華語 etc.
    "神護": "\uFA19護",   # 神護国 etc.
    "神灣": "\uFA19灣",   # 神灣国民政府 etc.
    "神聖": "\uFA19聖",   # 神聖大藭華帝国 etc.
}


# ── CSS ─────────────────────────────────────────────────────────────────────

def generate_css() -> str:
    """
    MediaWiki:Common.css への追記分。

    data/font-face.css が存在する場合 (make_font_subset.py 実行済み) は
    Base64 埋め込みの @font-face を先頭に挿入し、
    どの環境でも U+FA19 の旧字体グリフが表示されるようにする。

    font-face.css がない場合はシステムフォントのみで動作する
    (IPAmjMincho がインストールされている環境のみ旧字体表示)。

    注意: 以前に追加した「全体明朝体 font-family ルール」がある場合は
      MediaWiki:Common.css から手動で削除してください。
    """
    font_face_path = DATA_DIR / "font-face.css"
    font_face_block = ""
    if font_face_path.exists():
        font_face_block = font_face_path.read_text(encoding="utf-8") + "\n"
    else:
        font_face_block = (
            "/* @font-face 未生成。make_font_subset.py を実行すると"
            " U+FA19 の旧字体グリフが全環境で確実に表示されます。 */\n\n"
        )

    return font_face_block + """\
/* ================================================================
 * 下腦Wiki — 旧字体表示用フォント設定
 *
 * JS が 神 (U+795E) を U+FA19 (CJK Compatibility Ideograph) に置換。
 * ShimonoKami フォント (@font-face) が U+FA19 にのみ適用され、
 * 旧字体グリフ (示 radical 形) を確実に表示する。
 *
 * ⚠ 以前に追加した全体明朝体ルールがあれば削除してください。
 * ================================================================ */
.shimono-kami {
    font-family:
        'ShimonoKami',
        "IPAmjMincho",
        "Yu Mincho", "YuMincho", "游明朝",
        "Hiragino Mincho ProN", "HiraMinProN-W3",
        serif !important;
}
"""


# ── JavaScript ───────────────────────────────────────────────────────────────

def generate_js() -> str:
    """
    MediaWiki:Common.js への追記分。

    KAMI_MAP のキー（神華等）をテキストノードから検出し、
    値（U+FA19華等）に文字置換した上で <span class="shimono-kami"> でラップ。

    なぜ DOM 操作なら U+FA19 が使えるか:
      NFC 正規化 (U+FA19→U+795E) は MediaWiki への保存時にのみ発生する。
      JS は DOM を操作するだけで保存しないため、
      span.textContent = "\\uFA19..." と書けば U+FA19 がそのまま描画される。
      IPAmjMincho を持つ環境では旧字体グリフ（示 radical 形）が表示される。
    """
    # KAMI_MAP を JS オブジェクトリテラルに変換。
    # キー (神華等 = U+795E) は可読性のため非エスケープ。
    # 値 (U+FA19を含む) は ensure_ascii=True で \uFA19 形式にエスケープする。
    # → MediaWiki の NFC 正規化はリテラル文字にのみ適用され、
    #   \uXXXX エスケープシーケンス (ASCII) は正規化されない。
    entries = ",\n        ".join(
        f'{json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=True)}'
        for k, v in KAMI_MAP.items()
    )
    keys_json = json.dumps(list(KAMI_MAP.keys()), ensure_ascii=False, indent=4)

    return f"""\
/* ================================================================
 * 下腦Wiki — 旧字体表示スクリプト
 *
 * 地名（神華→U+FA19華 等）を文字レベルで置換し、
 * <span class="shimono-kami"> でラップして旧字体グリフを表示。
 *
 * NFC 正規化 (U+FA19→U+795E) は MediaWiki 保存時のみ発生する。
 * JS は DOM 操作のみで保存しないため U+FA19 をそのまま使える。
 *
 * 新しい語の追加: KAMI_MAP に1エントリ追加するだけ。
 * ================================================================ */
(function () {{
    'use strict';

    /* ── メモ: 置換マップ (U+795E → U+FA19) ──────────────────── */
    var KAMI_MAP = {{
        {entries}
    }};
    /* ─────────────────────────────────────────────────────────── */

    /* 閲覧ページ以外では実行しない（エディターでwikitextが壊れるため） */
    /* URL の ?action= と wgAction の両方を確認（VisualEditor 等のカバーのため） */
    var _action = mw.config.get('wgAction');
    var _search = window.location.search;
    if (_action !== 'view') return;
    if (_search.indexOf('action=edit') !== -1) return;
    if (_search.indexOf('action=submit') !== -1) return;
    if (document.querySelector('.ve-active, .ve-ui-surface')) return;

    var content = document.getElementById('mw-content-text');
    if (!content) return;

    var keys = {keys_json};
    if (keys.length === 0) return;

    /* 全キーに対して1本の正規表現を構築 */
    var escaped = keys.map(function (w) {{
        return w.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
    }});
    var pattern = new RegExp(escaped.join('|'), 'g');

    function processTextNode(node) {{
        var text = node.nodeValue;
        pattern.lastIndex = 0;
        if (!pattern.test(text)) return;

        pattern.lastIndex = 0;
        var frag = document.createDocumentFragment();
        var lastIndex = 0;
        var match;

        while ((match = pattern.exec(text)) !== null) {{
            /* マッチ前のテキスト */
            if (match.index > lastIndex) {{
                frag.appendChild(
                    document.createTextNode(text.slice(lastIndex, match.index))
                );
            }}
            /* 旧字体スパン — U+FA19 に文字置換してラップ */
            var span = document.createElement('span');
            span.className = 'shimono-kami';
            span.textContent = KAMI_MAP[match[0]];   /* 神 (U+795E) → U+FA19 に置換 */
            frag.appendChild(span);
            lastIndex = match.index + match[0].length;
        }}

        /* マッチ後の残りテキスト */
        if (lastIndex < text.length) {{
            frag.appendChild(document.createTextNode(text.slice(lastIndex)));
        }}

        node.parentNode.replaceChild(frag, node);
    }}

    /* テキストノードを収集（DOM変更前に全収集してから処理） */
    var iter = document.createNodeIterator(
        content,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    var textNodes = [];
    var node;
    while ((node = iter.nextNode())) {{
        /* <h1> と .mw-headline は除外（ページタイトル・目次の整合性保持） */
        var el = node.parentElement;
        if (el && (el.closest('h1') || el.closest('.mw-headline'))) continue;
        textNodes.push(node);
    }}

    textNodes.forEach(processTextNode);
}}());
"""


# ── MediaWiki API push ────────────────────────────────────────────────────────

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


def _edit_page(session: requests.Session, title: str,
               content: str, summary: str, token: str) -> None:
    r = session.post(MIRAHEZE_API, data={
        "action": "edit", "title": title, "appendtext": "\n" + content,
        "summary": summary, "token": token, "format": "json",
    })
    result = r.json()
    if result.get("edit", {}).get("result") == "Success":
        url = f"https://{MIRAHEZE_WIKI}.miraheze.org/wiki/{title.replace(' ', '_')}"
        print(f"✓ {title}: {url}")
    else:
        print(f"✗ {title}: {result}")
        if "error" in result and result["error"].get("code") == "protectedpage":
            print("  → interface-admin 権限が必要です。")
            print("  → Special:UserRights でボットアカウントに interface-admin を付与してください。")


def push_sitewide() -> None:
    """CSS と JS を MediaWiki: 名前空間に追記 (appendtext)。"""
    username = os.getenv("MIRAHEZE_BOT_USER")
    password = os.getenv("MIRAHEZE_BOT_PASSWORD")
    if not username or not password:
        print("ERROR: .env に MIRAHEZE_BOT_USER / MIRAHEZE_BOT_PASSWORD を設定してください。")
        return

    css = generate_css()
    js  = generate_js()

    session = requests.Session()
    session.headers["User-Agent"] = "ShimonoMigrationBot/1.0"

    print("Mirahezeにログイン中...")
    token = _get_csrf_token(session, username, password)

    _edit_page(session, "MediaWiki:Common.css", css,
               "下腦 旧字体フォント設定を追加", token)
    _edit_page(session, "MediaWiki:Common.js",  js,
               "下腦 旧字体置換スクリプトを追加", token)


def preview_sitewide() -> None:
    """CSS と JS をローカルファイルに出力（push なし）。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    css_path = DATA_DIR / "common.css"
    js_path  = DATA_DIR / "common.js"

    css_path.write_text(generate_css(), encoding="utf-8")
    js_path.write_text(generate_js(),  encoding="utf-8")

    print(f"CSS プレビュー: {css_path}")
    print(f"JS  プレビュー: {js_path}")
    print()
    print("適用手順 (interface-admin なし / 手動):")
    print(f"  1. https://{MIRAHEZE_WIKI}.miraheze.org/wiki/MediaWiki:Common.css を編集")
    print(f"     → {css_path} の内容を末尾に追記")
    print(f"  2. https://{MIRAHEZE_WIKI}.miraheze.org/wiki/MediaWiki:Common.js を編集")
    print(f"     → {js_path} の内容を末尾に追記")
    print()
    print("Bot で自動適用する場合 (interface-admin 必要):")
    print("  Special:UserRights で Shikabaton@MigrationBot に interface-admin を付与")
    print("  → python run.py sitewide")


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    load_dotenv()

    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        preview_sitewide()
    else:
        push_sitewide()
