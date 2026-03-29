"""
SeesaaWiki HTML → MediaWiki wikitext ベスト・エフォート変換。

変換できない要素は <!-- TODO: ... --> コメントで残す。
移行後にMiraheze上で手動整形することを前提にしている。
"""
import re
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

from config import SEESAA_WIKI, SEESAA_BASE


# ── ヘルパー ─────────────────────────────────────────────────────────────────

def _is_seesaa_internal(href: str) -> bool:
    return f"/{SEESAA_WIKI}/d/" in href


def _seesaa_href_to_title(href: str) -> str:
    """'/w/.../d/PAGE' → デコードされたページタイトル"""
    m = re.search(rf"/{re.escape(SEESAA_WIKI)}/d/([^/?#]+)", href)
    if not m:
        return ""
    try:
        return unquote(m.group(1), encoding="euc_jis_2004")
    except Exception:
        return unquote(m.group(1))


# ── 要素ごとの変換 ────────────────────────────────────────────────────────────

def _node(el, list_depth: int = 0) -> str:
    """再帰的にノードをwikitext文字列に変換する。"""
    if isinstance(el, NavigableString):
        return str(el)

    tag = el.name.lower() if el.name else ""

    # ── ブロック要素 ──────────────────────────────────────────────────────
    if tag in ("p", "div", "section", "article"):
        inner = _children(el, list_depth)
        inner = inner.strip()
        return f"\n{inner}\n" if inner else ""

    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(tag[1])
        marks = "=" * level
        text = el.get_text(strip=True)
        return f"\n{marks} {text} {marks}\n"

    if tag in ("ul", "ol"):
        items = []
        for li in el.find_all("li", recursive=False):
            bullet = "*" if tag == "ul" else "#"
            prefix = bullet * (list_depth + 1)
            items.append(prefix + " " + _children(li, list_depth + 1).strip())
        return "\n" + "\n".join(items) + "\n"

    if tag == "li":
        return _children(el, list_depth).strip()

    if tag == "br":
        return "\n"

    if tag == "hr":
        return "\n----\n"

    if tag in ("table",):
        return _table(el)

    if tag in ("blockquote",):
        inner = _children(el, list_depth).strip()
        lines = [f"  {l}" for l in inner.splitlines()]
        return "\n" + "\n".join(lines) + "\n"

    if tag == "pre":
        inner = el.get_text()
        return f"\n<pre>{inner}</pre>\n"

    # ── インライン要素 ────────────────────────────────────────────────────
    if tag in ("strong", "b"):
        return f"'''{_children(el, list_depth)}'''"

    if tag in ("em", "i"):
        return f"''{_children(el, list_depth)}''"

    if tag in ("s", "del", "strike"):
        return f"<s>{_children(el, list_depth)}</s>"

    if tag == "u":
        return f"<u>{_children(el, list_depth)}</u>"

    if tag in ("sup",):
        return f"<sup>{_children(el, list_depth)}</sup>"

    if tag in ("sub",):
        return f"<sub>{_children(el, list_depth)}</sub>"

    if tag == "a":
        href = el.get("href", "")
        text = el.get_text(strip=True)
        if not href:
            return text
        # SeesaaWiki「新規作成」リンク (e/add?pagename=...) → 存在しないページへの wiki リンク
        if "/e/add?" in href:
            m = re.search(r"pagename=([^&]+)", href)
            if m:
                try:
                    page = unquote(m.group(1), encoding="euc_jis_2004")
                except Exception:
                    page = unquote(m.group(1))
                return f"[[{page}]]"
            return text
        # SeesaaWiki カテゴリリンク (/c/数字/) → スキップ（後で Category タグに変換）
        if re.search(rf"/{re.escape(SEESAA_WIKI)}/c/\d+/", href):
            return ""
        # 内部ページリンク
        if _is_seesaa_internal(href):
            page = _seesaa_href_to_title(href)
            if not page:
                return text
            if page == text:
                return f"[[{page}]]"
            return f"[[{page}|{text}]]"
        # アンカーリンク（TOC用）→ テキストのみ返す（目次はどうせ除去）
        if href.startswith("#"):
            return text
        # 外部リンク
        return f"[{href} {text}]" if text else href

    if tag == "img":
        alt = el.get("alt", "")
        src = el.get("src", "")
        fname = src.split("/")[-1].split("?")[0]
        return f"<!-- TODO: [[File:{fname}|{alt}]] -->"

    if tag == "span":
        return _children(el, list_depth)

    if tag in ("head", "script", "style", "noscript"):
        return ""

    # その他：子要素を処理
    return _children(el, list_depth)


def _children(el: Tag, list_depth: int = 0) -> str:
    return "".join(_node(child, list_depth) for child in el.children)


def _table(el: Tag) -> str:
    """HTML table → MediaWiki table syntax。"""
    cls = el.get("class", [])
    cls_str = " ".join(cls) if cls else "wikitable"
    style = el.get("style", "")
    style_part = f' style="{style}"' if style else ""

    lines = [f'{{| class="{cls_str}"{style_part}']

    for row in el.find_all("tr"):
        lines.append("|-")
        cells = row.find_all(["th", "td"])
        for cell in cells:
            prefix = "!" if cell.name == "th" else "|"
            # セルの属性
            attrs = []
            if cell.get("colspan"):
                attrs.append(f'colspan="{cell["colspan"]}"')
            if cell.get("rowspan"):
                attrs.append(f'rowspan="{cell["rowspan"]}"')
            if cell.get("style"):
                attrs.append(f'style="{cell["style"]}"')
            attr_str = " ".join(attrs)

            inner = _children(cell).strip()
            # テーブル内テーブルは再帰変換済み
            if attr_str:
                lines.append(f"{prefix} {attr_str} | {inner}")
            else:
                lines.append(f"{prefix} {inner}")

    lines.append("|}")
    return "\n" + "\n".join(lines) + "\n"


# ── パブリック API ────────────────────────────────────────────────────────────

_STRIP_IDS = {
    "page-header", "page-header-inner",
    "page-social-link-top", "page-social-link-bottom",
    "page-toplink", "page-footer", "pageroot-form-box",
    "information-box",
}
_STRIP_CLASSES = {
    "page-social-link-top", "page-social-link-bottom",
    "adsense-box", "edit-link", "category-tag", "page-navi",
}
_STRIP_TAGS = {"script", "style", "noscript", "iframe"}

# 「このページを編集する」等のフッターリンクテキスト
_FOOTER_LINK_RE = re.compile(r"このページを編集|ページの編集|最終更新|履歴を見る")


def _clean(body: Tag) -> None:
    """SeesaaWikiのナビゲーション・メタ・広告要素を除去する。"""
    for tag in _STRIP_TAGS:
        for el in body.find_all(tag):
            el.decompose()

    for el_id in _STRIP_IDS:
        el = body.find(id=el_id)
        if el:
            el.decompose()

    for cls in _STRIP_CLASSES:
        for el in body.find_all(class_=cls):
            el.decompose()

    # 自動生成TOCブロック
    for el in body.find_all(id=re.compile(r"content_toc|^toc")):
        el.decompose()

    # ソーシャルシェアリンク
    for el in body.find_all("a", href=re.compile(r"twitter\.com/share|facebook\.com/sharer")):
        p = el.parent
        if p:
            p.decompose()

    # フッターリンク（「このページを編集する」等）
    for el in body.find_all("a", string=_FOOTER_LINK_RE):
        p = el.parent
        if p:
            p.decompose()

    # コメントリンク (/comment/)
    for el in body.find_all("a", href=re.compile(r"/comment/")):
        p = el.parent
        if p:
            p.decompose()

    # カテゴリセクション（#page-category）
    for el in body.find_all(id="page-category"):
        el.decompose()


def html_to_wikitext(html: str) -> str:
    """
    SeesaaWikiのレンダリング済みHTMLをMediaWiki wikitextに変換する。

    引数:
      html: get_article_content() が返す content_html

    戻り値:
      MediaWiki wikitext (ベスト・エフォート)
    """
    soup = BeautifulSoup(html, "html.parser")

    # コンテンツ本体を特定してからクリーニング
    body = (
        soup.find("div", id="page-body")
        or soup.find("div", id="content_block_0")
        or soup.find("div", id="main")
        or soup
    )
    _clean(body)

    wikitext = _children(body)

    # 連続する空行を2行に圧縮
    wikitext = re.sub(r"\n{3,}", "\n\n", wikitext)

    # SeesaaWikiの内部マーカー・フッターゴミを除去
    wikitext = _postprocess(wikitext)

    return wikitext.strip()


_JUNK_LINE_RE = re.compile(
    r"^\s*("
    r"google_ad_section\S*|"        # google_ad_section_end(name=s1) 等
    r"entry_bottom|pc_footer\S*|"   # SeesaaWiki テンプレートマーカー
    r'id="[^"]*"|'                   # id="pageroot-form-box" 等
    r"[/#\.][a-zA-Z#\-_\.0-9]+|"    # /class-name や #id-name 形式
    r")\s*$",
    re.MULTILINE,
)
_TOC_LINE_RE  = re.compile(r"^\*\s*\[#content_\d+[^\]]*\]\s*$", re.MULTILINE)
_TOC_HEADER_RE = re.compile(r"^'''目次'''\s*$", re.MULTILINE)
_EMPTY_LIST_RE = re.compile(r"^\*\s*$", re.MULTILINE)


def _dedup_wikilinks(text: str) -> str:
    """
    SeesaaWiki の「新規作成リンク」重複を除去する。
    「PAGE_TITLE[[PAGE_TITLE]]」→「[[PAGE_TITLE]]」
    """
    result: list[str] = []
    i = 0
    while i < len(text):
        start = text.find("[[", i)
        if start == -1:
            result.append(text[i:])
            break
        end = text.find("]]", start)
        if end == -1:
            result.append(text[i:])
            break
        link_content = text[start + 2 : end]
        page = link_content.split("|")[0]
        if start >= len(page) and text[start - len(page) : start] == page:
            # 直前のテキストにページ名が重複 → 重複分を除いて出力
            result.append(text[i : start - len(page)])
        else:
            result.append(text[i:start])
        result.append(text[start : end + 2])
        i = end + 2
    return "".join(result)


def _postprocess(wikitext: str) -> str:
    wikitext = _JUNK_LINE_RE.sub("", wikitext)
    wikitext = _TOC_LINE_RE.sub("", wikitext)
    wikitext = _TOC_HEADER_RE.sub("", wikitext)
    wikitext = _EMPTY_LIST_RE.sub("", wikitext)
    wikitext = _dedup_wikilinks(wikitext)
    wikitext = re.sub(r"\n{3,}", "\n\n", wikitext)
    return wikitext
