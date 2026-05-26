const WIKI = {
  name: "しかバトン Wiki",
  api: "https://shikabaton.miraheze.org/w/api.php",
  home: "https://shikabaton.miraheze.org/wiki/",
  articleBase: "https://shikabaton.miraheze.org/wiki/"
};

const HOME_FOLDERS = [
  { title: "Category:架空国家一覧", label: "国家", description: "国家と政体をめぐる" },
  { title: "Category:架空人物一覧", label: "人物", description: "人物の記録を読む" },
  { title: "Category:歴史", label: "歴史", description: "出来事と時代" },
  { title: "Category:地理", label: "地理", description: "大陸と地域" },
  { title: "Category:軍事", label: "軍事", description: "組織と装備" },
  { title: "Category:メディア", label: "メディア", description: "画像と映像資料" },
  { title: "Category:ニュース", label: "ニュース", description: "報道と更新" },
  { title: "Category:架空戦争・紛争・事件一覧", label: "事件", description: "戦争・紛争・事件" }
];

const windows = document.querySelector("#windows");
const tasks = document.querySelector("#task-buttons");
const template = document.querySelector("#window-template");
const startMenu = document.querySelector("#start-menu");
const startButton = document.querySelector("#start-button");
const connectionLight = document.querySelector("#connection-light");
let zIndex = 20;
let windowNumber = 0;

function api(params) {
  const query = new URLSearchParams({
    action: "query",
    format: "json",
    formatversion: "2",
    origin: "*",
    ...params
  });
  return fetch(`${WIKI.api}?${query}`).then(async response => {
    if (!response.ok) throw new Error(`APIから応答がありません (${response.status})`);
    const data = await response.json();
    if (data.error) throw new Error(data.error.info);
    return data;
  });
}

function pageUrl(title) {
  return `${WIKI.articleBase}${encodeURIComponent(title.replaceAll(" ", "_"))}`;
}

function absoluteMediaUrl(url) {
  if (!url) return "";
  if (url.startsWith("//")) return `https:${url}`;
  if (url.startsWith("/")) return new URL(url, WIKI.home).href;
  return url;
}

function setRoute(key, value) {
  const url = new URL(window.location.href);
  url.search = "";
  if (key && value) url.searchParams.set(key, value);
  history.replaceState(null, "", url);
}

function escapeHtml(value) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

function addShareButton(toolbar, key, value, status) {
  const share = document.createElement("button");
  share.textContent = "共有";
  share.onclick = async () => {
    const url = new URL(window.location.href);
    url.search = "";
    if (key && value) url.searchParams.set(key, value);
    try {
      await navigator.clipboard.writeText(url.href);
      status.textContent = "共有リンクをコピーしました";
    } catch {
      window.prompt("このリンクをコピーしてください", url.href);
    }
  };
  toolbar.append(share);
}

function activate(win) {
  document.querySelectorAll(".window").forEach(item => item.classList.remove("active"));
  document.querySelectorAll(".task-button").forEach(item => item.classList.remove("active"));
  win.classList.remove("minimized");
  win.hidden = false;
  win.style.zIndex = ++zIndex;
  win.classList.add("active");
  win.taskButton.classList.add("active");
}

function makeWindow(title, dimensions = {}) {
  windowNumber += 1;
  const win = template.content.firstElementChild.cloneNode(true);
  const body = win.querySelector(".window-body");
  const status = win.querySelector(".statusbar");
  win.querySelector("h2").textContent = title;
  win.style.width = `${dimensions.width || 640}px`;
  win.style.height = `${dimensions.height || 470}px`;
  win.style.left = `${dimensions.left ?? 120 + (windowNumber % 5) * 28}px`;
  win.style.top = `${dimensions.top ?? 38 + (windowNumber % 5) * 24}px`;

  const task = document.createElement("button");
  task.className = "task-button";
  task.textContent = title;
  task.onclick = () => activate(win);
  tasks.append(task);
  win.taskButton = task;

  win.querySelector(".close").onclick = () => {
    win.remove();
    task.remove();
  };
  win.querySelector(".minimize").onclick = () => {
    win.hidden = true;
    task.classList.remove("active");
  };
  win.onpointerdown = () => activate(win);
  enableDragging(win);
  windows.append(win);
  activate(win);
  return { win, body, status, toolbar: win.querySelector(".toolbar"), task };
}

function enableDragging(win) {
  const bar = win.querySelector(".titlebar");
  let drag = null;
  bar.addEventListener("pointerdown", event => {
    if (event.target.closest("button") || window.innerWidth < 681) return;
    drag = { x: event.clientX - win.offsetLeft, y: event.clientY - win.offsetTop };
    bar.setPointerCapture(event.pointerId);
  });
  bar.addEventListener("pointermove", event => {
    if (!drag) return;
    win.style.left = `${Math.max(0, event.clientX - drag.x)}px`;
    win.style.top = `${Math.max(0, event.clientY - drag.y)}px`;
  });
  bar.addEventListener("pointerup", () => {
    drag = null;
  });
}

function setToolbar(toolbar, crumbs, goBack) {
  toolbar.replaceChildren();
  if (goBack) {
    const back = document.createElement("button");
    back.textContent = "← 戻る";
    back.onclick = goBack;
    toolbar.append(back);
  }
  const address = document.createElement("div");
  address.className = "address";
  address.textContent = `📂 ${WIKI.name} / ${crumbs.join(" / ")}`;
  toolbar.append(address);
}

function errorBody(body, error) {
  body.innerHTML = `<div class="error">読み込みに失敗しました。<br>${escapeHtml(error.message)}</div>`;
}

function openCategories(categoryTitle) {
  const label = categoryTitle ? categoryTitle.replace(/^Category:/, "") : "カテゴリ";
  const view = makeWindow(`${label} - ${WIKI.name}`, { width: 670, height: 485 });
  loadCategory(view, categoryTitle, []);
}

function openHome() {
  const view = makeWindow(`${WIKI.name} - ホーム`, { width: 790, height: 560, left: 110, top: 44 });
  setRoute(null, null);
  setToolbar(view.toolbar, ["ホーム"], null);
  addShareButton(view.toolbar, null, null, view.status);
  view.body.innerHTML = `
    <section class="explorer-home">
      <header class="home-hero">
        <h3>しかバトン Wiki</h3>
        <p>世界の記録を選んでください</p>
      </header>
      <h4>主要フォルダー</h4>
      <div class="home-grid"></div>
      <div class="home-section-heading">
        <h4>写真のある資料</h4>
        <button class="xp-button all-folders" type="button">すべてのカテゴリ</button>
      </div>
      <div class="featured-grid"><div class="loading">資料を探しています...</div></div>
    </section>`;
  const homeGrid = view.body.querySelector(".home-grid");
  HOME_FOLDERS.forEach(folder => {
    const button = document.createElement("button");
    button.className = "home-folder";
    button.innerHTML = `<span class="home-folder-icon" aria-hidden="true"></span><strong>${escapeHtml(folder.label)}</strong><small>${escapeHtml(folder.description)}</small>`;
    button.onclick = () => openCategories(folder.title);
    homeGrid.append(button);
  });
  view.body.querySelector(".all-folders").onclick = () => openCategories(null);
  loadFeatured(view);
}

async function loadFeatured(view) {
  const featured = view.body.querySelector(".featured-grid");
  try {
    const changes = await api({
      list: "recentchanges",
      rcnamespace: "0",
      rclimit: "30",
      rcprop: "title",
      rcshow: "!bot"
    });
    const titles = [...new Set(changes.query.recentchanges.map(change => change.title))];
    const thumbnails = await loadThumbnails(titles, 220);
    const pages = titles.filter(title => thumbnails.has(title)).slice(0, 4);
    featured.replaceChildren();
    if (!pages.length) {
      featured.innerHTML = '<div class="empty">画像付き資料はまだ見つかりませんでした。</div>';
      return;
    }
    pages.forEach(title => {
      const button = document.createElement("button");
      button.className = "featured-item";
      button.innerHTML = `<img src="${escapeHtml(thumbnails.get(title))}" alt=""><span>${escapeHtml(title)}</span>`;
      button.onclick = () => openArticle(title);
      featured.append(button);
    });
  } catch (error) {
    featured.innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  }
}

async function loadCategory(view, categoryTitle, history) {
  view.body.innerHTML = '<div class="loading">フォルダーを読み込んでいます...</div>';
  const title = categoryTitle ? categoryTitle.replace(/^Category:/, "") : "カテゴリ";
  setRoute("category", categoryTitle || "all");
  view.win.querySelector("h2").textContent = `${title} - ${WIKI.name}`;
  view.task.textContent = title;
  setToolbar(view.toolbar, [...history.map(item => item.label), title], history.length ? () => {
    const previous = history[history.length - 1];
    loadCategory(view, previous.title, history.slice(0, -1));
  } : null);
  addShareButton(view.toolbar, "category", categoryTitle || "all", view.status);
  try {
    let items;
    if (!categoryTitle) {
      const result = await api({ list: "allcategories", aclimit: "80" });
      items = result.query.allcategories.map(category => ({
        title: `Category:${category["*"] || category.category || category.name}`,
        label: category["*"] || category.category || category.name,
        type: "subcat"
      }));
    } else {
      const result = await api({
        list: "categorymembers",
        cmtitle: categoryTitle,
        cmtype: "subcat|page",
        cmlimit: "100"
      });
      items = result.query.categorymembers.map(item => ({
        title: item.title,
        label: item.title.replace(/^Category:/, ""),
        type: item.ns === 14 ? "subcat" : "page"
      }));
      const articleImages = await loadThumbnails(items.filter(item => item.type === "page").map(item => item.title), 110);
      items.forEach(item => {
        item.thumbnail = articleImages.get(item.title);
      });
    }

    if (!items.length) {
      view.body.innerHTML = '<div class="empty">このフォルダーは空です。</div>';
    } else {
      const grid = document.createElement("div");
      grid.className = "file-grid";
      items.forEach(item => {
        const button = document.createElement("button");
        const category = item.type === "subcat";
        button.className = `file-item ${category ? "category" : "article"}`;
        const visual = item.thumbnail
          ? `<img class="file-thumbnail" src="${escapeHtml(item.thumbnail)}" alt="">`
          : '<span class="file-icon"></span>';
        button.innerHTML = `${visual}<span>${escapeHtml(item.label)}</span>`;
        button.ondblclick = () => {
          if (category) {
            loadCategory(view, item.title, [...history, { title: categoryTitle, label: title }]);
          } else {
            openArticle(item.title);
          }
        };
        button.onclick = () => {
          view.status.textContent = category ? `${item.label} フォルダー - ダブルクリックで開く` : `${item.label} - ダブルクリックで読む`;
        };
        grid.append(button);
      });
      view.body.replaceChildren(grid);
    }
    view.status.textContent = `${items.length} 個の項目`;
  } catch (error) {
    errorBody(view.body, error);
    view.status.textContent = "接続エラー";
  }
}

async function loadThumbnails(titles, size) {
  if (!titles.length) return new Map();
  const result = await api({
    titles: titles.slice(0, 50).join("|"),
    prop: "images",
    imlimit: "1"
  });
  const imageByArticle = new Map((result.query.pages || [])
    .filter(page => page.images?.length)
    .map(page => [page.title, page.images[0].title]));
  const imageTitles = [...new Set(imageByArticle.values())];
  if (!imageTitles.length) return new Map();
  const images = await api({
    titles: imageTitles.join("|"),
    prop: "imageinfo",
    iiprop: "url",
    iiurlwidth: String(size)
  });
  const sourceByImage = new Map((images.query.pages || [])
    .filter(page => page.imageinfo?.[0]?.thumburl)
    .map(page => [page.title, absoluteMediaUrl(page.imageinfo[0].thumburl)]));
  return new Map([...imageByArticle]
    .filter(([, imageTitle]) => sourceByImage.has(imageTitle))
    .map(([articleTitle, imageTitle]) => [articleTitle, sourceByImage.get(imageTitle)]));
}

async function openArticle(title) {
  const view = makeWindow(`${title} - 記事`, { width: 760, height: 565 });
  setToolbar(view.toolbar, ["記事", title], null);
  setRoute("page", title);
  const external = document.createElement("button");
  external.textContent = "元の記事";
  external.onclick = () => window.open(pageUrl(title), "_blank", "noopener");
  view.toolbar.append(external);
  addShareButton(view.toolbar, "page", title, view.status);
  view.body.innerHTML = '<div class="loading">記事を開いています...</div>';
  try {
    const query = new URLSearchParams({
      action: "parse",
      page: title,
      prop: "text|displaytitle",
      format: "json",
      formatversion: "2",
      origin: "*"
    });
    const response = await fetch(`${WIKI.api}?${query}`);
    const data = await response.json();
    if (data.error) throw new Error(data.error.info);
    const content = document.createElement("div");
    content.className = "article-view";
    content.innerHTML = `<h1>${data.parse.displaytitle}</h1><section class="wiki-content">${data.parse.text}</section>`;
    sanitizeWikiContent(content);
    view.body.replaceChildren(content);
    view.status.textContent = `${WIKI.name} の記事`;
  } catch (error) {
    errorBody(view.body, error);
  }
}

function sanitizeWikiContent(container) {
  container.querySelectorAll("script, style, iframe, object, form, input, button").forEach(node => node.remove());
  container.querySelectorAll("*").forEach(node => {
    [...node.attributes].forEach(attribute => {
      if (attribute.name.startsWith("on")) node.removeAttribute(attribute.name);
    });
  });
  container.querySelectorAll("a").forEach(link => {
    const href = link.getAttribute("href") || "";
    const wikiPath = href.match(/^\/wiki\/(.+)/);
    if (wikiPath && !href.includes(":")) {
      const title = decodeURIComponent(wikiPath[1]).replaceAll("_", " ");
      link.href = "#";
      link.onclick = event => {
        event.preventDefault();
        openArticle(title);
      };
    } else if (href.startsWith("/")) {
      link.href = new URL(href, WIKI.home).href;
      link.target = "_blank";
      link.rel = "noopener";
    } else if (href.startsWith("//")) {
      link.href = `https:${href}`;
      link.target = "_blank";
      link.rel = "noopener";
    } else if (!/^(https?:|#|mailto:)/i.test(href)) {
      link.removeAttribute("href");
    } else if (/^https?:/i.test(href)) {
      link.target = "_blank";
      link.rel = "noopener";
    }
  });
  container.querySelectorAll("img").forEach(image => {
    const src = image.getAttribute("src");
    if (src?.startsWith("//")) image.src = `https:${src}`;
    else if (src?.startsWith("/")) image.src = new URL(src, WIKI.home).href;
    else if (src && !/^https?:/i.test(src)) image.removeAttribute("src");
    if (image.src) {
      image.classList.add("viewable-image");
      image.title = "クリックして画像ビューアーで開く";
      image.tabIndex = 0;
      image.onclick = event => {
        event.preventDefault();
        event.stopPropagation();
        openImageViewer(largestImageSource(image), image.alt || "画像");
      };
      image.onkeydown = event => {
        if (event.key === "Enter") openImageViewer(largestImageSource(image), image.alt || "画像");
      };
    }
  });
}

function largestImageSource(image) {
  const srcset = image.getAttribute("srcset");
  if (!srcset) return image.src;
  const candidates = srcset.split(",").map(item => item.trim().split(/\s+/)[0]);
  return absoluteMediaUrl(candidates[candidates.length - 1] || image.src);
}

function openImageViewer(source, title) {
  const view = makeWindow(`${title || "画像"} - 画像ビューアー`, { width: 760, height: 570 });
  view.toolbar.innerHTML = '<span class="viewer-label">Windows 画像と FAX ビューア</span>';
  const original = document.createElement("button");
  original.textContent = "原寸を開く";
  original.onclick = () => window.open(source, "_blank", "noopener");
  view.toolbar.append(original);
  view.body.className = "window-body image-viewer";
  const image = document.createElement("img");
  image.src = source;
  image.alt = title || "Wiki画像";
  view.body.replaceChildren(image);
  view.status.textContent = "画像を表示しています";
}

function openSearch() {
  const view = makeWindow(`検索 - ${WIKI.name}`, { width: 630, height: 460 });
  setToolbar(view.toolbar, ["検索"], null);
  view.body.innerHTML = `
    <form class="search-form">
      <input name="keyword" type="search" placeholder="記事名や言葉を入力" aria-label="検索語" autofocus>
      <button class="xp-button" type="submit">検索</button>
    </form>
    <ol class="results"><li class="empty">検索語を入力してください。</li></ol>`;
  const form = view.body.querySelector("form");
  const results = view.body.querySelector(".results");
  form.onsubmit = async event => {
    event.preventDefault();
    const keyword = new FormData(form).get("keyword").trim();
    if (!keyword) return;
    results.innerHTML = '<li class="loading">検索しています...</li>';
    try {
      const data = await api({ list: "search", srsearch: keyword, srlimit: "20" });
      results.replaceChildren();
      data.query.search.forEach(result => {
        const item = document.createElement("li");
        item.innerHTML = `<button>${escapeHtml(result.title)}</button><p class="snippet">${result.snippet}</p>`;
        sanitizeWikiContent(item.querySelector(".snippet"));
        item.querySelector("button").onclick = () => openArticle(result.title);
        results.append(item);
      });
      if (!data.query.search.length) results.innerHTML = '<li class="empty">見つかりませんでした。</li>';
      view.status.textContent = `${data.query.searchinfo.totalhits || data.query.search.length} 件の候補`;
    } catch (error) {
      results.innerHTML = `<li class="error">${escapeHtml(error.message)}</li>`;
    }
  };
}

async function openChanges() {
  const view = makeWindow(`最近の更新 - ${WIKI.name}`, { width: 600, height: 450 });
  setToolbar(view.toolbar, ["最近の更新"], null);
  view.body.innerHTML = '<div class="loading">更新履歴を読み込んでいます...</div>';
  try {
    const data = await api({
      list: "recentchanges",
      rcprop: "title|timestamp|user",
      rclimit: "40"
    });
    const list = document.createElement("ul");
    list.className = "changes-list";
    data.query.recentchanges.forEach(change => {
      const date = new Date(change.timestamp).toLocaleString("ja-JP");
      const item = document.createElement("li");
      item.innerHTML = `<button>${escapeHtml(change.title)}</button><div>${escapeHtml(date)} / ${escapeHtml(change.user || "不明")}</div>`;
      item.querySelector("button").onclick = () => openArticle(change.title);
      list.append(item);
    });
    view.body.replaceChildren(list);
    view.status.textContent = `${data.query.recentchanges.length} 件の更新`;
  } catch (error) {
    errorBody(view.body, error);
  }
}

function openReadme() {
  const view = makeWindow("Readme.txt - メモ帳", { width: 520, height: 390 });
  view.toolbar.remove();
  view.body.innerHTML = `<pre class="readme">========================================
 しかバトン Wiki Explorer
========================================

Windows XP のデスクトップから、しかバトン Wiki を
フォルダーのように探索するビューアーです。

使いかた
--------
・しかバトン Wiki: カテゴリをフォルダー表示
・記事を検索: Wiki全文検索
・最近の更新: 新しく変わった記事を確認
・フォルダーや記事はダブルクリックで開きます

このビューアーが使用するのは公開閲覧APIです。
編集、投稿、管理操作は元のWikiで行ってください。</pre>`;
  view.status.textContent = "Ln 1, Col 1";
}

const launchers = {
  home: openHome,
  categories: () => openCategories(null),
  search: openSearch,
  changes: openChanges,
  readme: openReadme
};

document.querySelectorAll("[data-launch]").forEach(button => {
  button.ondblclick = () => launchers[button.dataset.launch]();
  button.onclick = event => {
    if (button.closest(".start-menu")) {
      launchers[button.dataset.launch]();
      startMenu.hidden = true;
      startButton.setAttribute("aria-expanded", "false");
    } else if (event.detail === 1) {
      button.focus();
    }
  };
});

startButton.onclick = () => {
  startMenu.hidden = !startMenu.hidden;
  startButton.setAttribute("aria-expanded", String(!startMenu.hidden));
};

document.addEventListener("pointerdown", event => {
  if (!event.target.closest("#start-menu, #start-button")) {
    startMenu.hidden = true;
    startButton.setAttribute("aria-expanded", "false");
  }
});

function setClock() {
  document.querySelector("#clock").textContent = new Date().toLocaleTimeString("ja-JP", {
    hour: "2-digit",
    minute: "2-digit"
  });
}

setClock();
setInterval(setClock, 30000);
api({ meta: "siteinfo", siprop: "general" }).then(() => {
  connectionLight.className = "connection-light ok";
  connectionLight.title = "Wiki API に接続済み";
}).catch(() => {
  connectionLight.className = "connection-light failed";
  connectionLight.title = "Wiki API に接続できません";
});

const route = new URLSearchParams(window.location.search);
if (route.has("page")) openArticle(route.get("page"));
else if (route.has("category")) openCategories(route.get("category") === "all" ? null : route.get("category"));
else openHome();
