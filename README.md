# しかバトン Wiki Explorer

`https://explorer.samismith.com/` の「WikiをWindowsデスクトップとして歩く」発想をもとにした、しかバトン Wiki 用の Windows XP 風ビューアーです。

## できること

- カテゴリをフォルダー、記事をファイルとして探索
- Wiki の全文検索
- 最近の更新の表示
- 記事本文をビューアー内で閲覧
- 元の Wiki 記事へ移動

## 起動

静的ファイルのみで動きます。ローカル確認には、このフォルダーで簡易Webサーバーを開始して `http://localhost:8000/` を開きます。

```powershell
python -m http.server 8000
```

## 公開

`index.html`、`styles.css`、`app.js` を静的ホスティングへ置くだけで公開できます。GitHub Pages、Cloudflare Pages、Netlify などが使えます。

接続先は [app.js](./app.js) 冒頭の `WIKI` 設定です。

```js
const WIKI = {
  name: "しかバトン Wiki",
  api: "https://shikabaton.miraheze.org/w/api.php",
  home: "https://shikabaton.miraheze.org/wiki/",
  articleBase: "https://shikabaton.miraheze.org/wiki/"
};
```

## API と管理権限

現在のビューアーは閲覧専用で、MediaWiki の公開APIだけを呼びます。管理者用トークンやパスワードをブラウザー側コードに置く必要はありません。

将来、ビューアー内で編集や画像投稿を行う場合は、利用者本人がWikiへログインした状態でMediaWikiのCSRFトークンを取得する設計にし、管理者資格情報を公開サイトに埋め込まないでください。
