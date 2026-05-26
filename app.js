const WIKI = {
  name: "しかバトン Wiki",
  api: "https://shikabaton.miraheze.org/w/api.php",
  home: "https://shikabaton.miraheze.org/wiki/",
  articleBase: "https://shikabaton.miraheze.org/wiki/"
};

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

function escapeHtml(value) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
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

async function loadCategory(view, categoryTitle, history) {
  view.body.innerHTML = '<div class="loading">フォルダーを読み込んでいます...</div>';
  const title = categoryTitle ? categoryTitle.replace(/^Category:/, "") : "カテゴリ";
  view.win.querySelector("h2").textContent = `${title} - ${WIKI.name}`;
  view.task.textContent = title;
  setToolbar(view.toolbar, [...history.map(item => item.label), title], history.length ? () => {
    const previous = history[history.length - 1];
    loadCategory(view, previous.title, history.slice(0, -1));
  } : null);
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
        button.innerHTML = `<span class="file-icon"></span><span>${escapeHtml(item.label)}</span>`;
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

async function openArticle(title) {
  const view = makeWindow(`${title} - 記事`, { width: 760, height: 565 });
  setToolbar(view.toolbar, ["記事", title], null);
  const external = document.createElement("button");
  external.textContent = "元の記事";
  external.onclick = () => window.open(pageUrl(title), "_blank", "noopener");
  view.toolbar.append(external);
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
  });
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
openReadme();
