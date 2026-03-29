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
(function () {
    'use strict';

    /* ── メモ: 置換マップ (U+795E → U+FA19) ──────────────────── */
    var KAMI_MAP = {
        "神華": "\ufa19\u83ef",
        "神護": "\ufa19\u8b77",
        "神灣": "\ufa19\u7063",
        "神聖": "\ufa19\u8056"
    };
    /* ─────────────────────────────────────────────────────────── */

    /* 閲覧ページ以外では実行しない（エディターでwikitextが壊れるため） */
    if (mw.config.get('wgAction') !== 'view') return;

    var content = document.getElementById('mw-content-text');
    if (!content) return;

    var keys = [
    "神華",
    "神護",
    "神灣",
    "神聖"
];
    if (keys.length === 0) return;

    /* 全キーに対して1本の正規表現を構築 */
    var escaped = keys.map(function (w) {
        return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    });
    var pattern = new RegExp(escaped.join('|'), 'g');

    function processTextNode(node) {
        var text = node.nodeValue;
        pattern.lastIndex = 0;
        if (!pattern.test(text)) return;

        pattern.lastIndex = 0;
        var frag = document.createDocumentFragment();
        var lastIndex = 0;
        var match;

        while ((match = pattern.exec(text)) !== null) {
            /* マッチ前のテキスト */
            if (match.index > lastIndex) {
                frag.appendChild(
                    document.createTextNode(text.slice(lastIndex, match.index))
                );
            }
            /* 旧字体スパン — U+FA19 に文字置換してラップ */
            var span = document.createElement('span');
            span.className = 'shimono-kami';
            span.textContent = KAMI_MAP[match[0]];   /* 神 (U+795E) → U+FA19 に置換 */
            frag.appendChild(span);
            lastIndex = match.index + match[0].length;
        }

        /* マッチ後の残りテキスト */
        if (lastIndex < text.length) {
            frag.appendChild(document.createTextNode(text.slice(lastIndex)));
        }

        node.parentNode.replaceChild(frag, node);
    }

    /* テキストノードを収集（DOM変更前に全収集してから処理） */
    var iter = document.createNodeIterator(
        content,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    var textNodes = [];
    var node;
    while ((node = iter.nextNode())) {
        /* <h1> と .mw-headline は除外（ページタイトル・目次の整合性保持） */
        var el = node.parentElement;
        if (el && (el.closest('h1') || el.closest('.mw-headline'))) continue;
        textNodes.push(node);
    }

    textNodes.forEach(processTextNode);
}());
