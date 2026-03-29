# しかバトンRAG 設計ナレッジ

v1.0 | 2026-03

---

## 0. このドキュメントについて

しかバトン（@tatari_tani）が創作する架空世界「下腦（げのう）」の設定を知識源とするRAGシステムの設計資料です。AITuberとしての接続・クラウドホスティング・設定の改訂管理を主要要件とします。

---

## 1. 目標・要件

| 項目 | 内容 |
|------|------|
| 知識源 | しかバトンの架空世界創作Wiki・X（@tatari_tani）発言 |
| アクセス制限 | 秘密URLトークン（URLを知っている人だけアクセス可） |
| ホスティング | クラウド・どの端末からでもブラウザでアクセス可 |
| AITuber接続 | WebSocketエンドポイントで接続 |
| データ更新 | 日次自動更新 + チャットからの随時追加 |

---

## 2. 技術スタック

```
フロントエンド:  Next.js (Vercel)          ← 無料枠
バックエンド:    FastAPI (Render)           ← 無料枠
Vector DB:       Supabase pgvector          ← 無料枠
LLM:             Gemini 2.0 Flash API       ← 無料枠
Embedding:       Gemini text-embedding-004  ← 無料枠
認証:            秘密URLトークン            ← 無料
AITuber接続:     WebSocket (/ws/chat)       ← 無料
```

**将来移行候補:** DGX Spark導入時にOllama（qwen2.5:72b）へ切り替え。LLMの向き先を1行変えるだけで移行できるよう設計する。

---

## 3. 知識源の分類

### RAGに入れるもの（正典）

| ソース | 種別 | 取り込み方法 |
|--------|------|-------------|
| 架空世界創作Wiki | 正典・架空世界の事実 | WikiページURLを貼ったら自動取得 |
| X発言 (@tatari_tani) | 作者の公式発言 | GUIで手動ペースト登録 |
| チャットメモ | 随時追加の設定 | 会話中「この設定を保存して」で追加 |
| mdファイル | まとめ設定 | ドロップで取り込み |

### RAGに入れないもの（別管理）

| ソース | 理由 | 用途 |
|--------|------|------|
| 骨粉史 | 制作秘話・架空世界の正典ではない。現実の出来事・日付・架空設定が混在する | 動画台本・「しかバトンが女性である100の証拠」の崩壊根拠ネタ帳として手元参照 |

---

## 4. データスキーマ

### 4-1. chunksテーブル（ベクトルDB）

```sql
CREATE TABLE chunks (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  text            TEXT NOT NULL,
  embedding       VECTOR(768),         -- Gemini text-embedding-004

  -- ソース管理
  source_type     TEXT NOT NULL,       -- 'wiki'|'x_post'|'md'|'chat_memo'
  source_url      TEXT,
  source_title    TEXT,

  -- 破棄設定管理
  status          TEXT DEFAULT 'active', -- 'active'|'deprecated'|'retconned'
  deprecated_reason TEXT,
  superseded_by   UUID REFERENCES chunks(id),

  -- 時系列管理
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now(),
  content_date    DATE
);

-- インデックス
CREATE INDEX ON chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON chunks (status);
CREATE INDEX ON chunks (source_type);

-- 全文検索
ALTER TABLE chunks ADD COLUMN fts TSVECTOR
  GENERATED ALWAYS AS (to_tsvector('japanese', text)) STORED;
CREATE INDEX ON chunks USING GIN(fts);
```

### 4-2. timeline_eventsテーブル（年表DB）

設定の前倒し改訂が繰り返される架空世界のために、イベントソーシング型で管理する。

```sql
CREATE TABLE timeline_events (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- 架空世界内の時間軸
  world_date    TEXT,        -- '神華暦元年'/'不明'など柔軟に
  world_era     TEXT,        -- '建国期'/'戦乱期'など時代区分

  -- 現実の更新時間軸
  created_at    TIMESTAMPTZ DEFAULT now(),
  revised_at    TIMESTAMPTZ,
  revision_note TEXT,        -- '前倒し改訂'/'設定追加'など

  -- イベント内容
  entity_name   TEXT,        -- エンティティ名
  event_type    TEXT,        -- '建国'/'戦争'/'滅亡'/'改名'など
  description   TEXT,

  -- 設定の状態
  canon_status  TEXT DEFAULT 'canon',
  -- 'canon'      現行正典
  -- 'retconned'  改訂済み（前倒しで上書きされた）
  -- 'legend'     劇中の伝説・不確かな情報
  -- 'deprecated' 完全廃止

  -- ベクトルDBとの紐付け
  chunk_ids     UUID[],

  -- 改訂履歴
  superseded_by UUID REFERENCES timeline_events(id)
);
```

---

## 5. 検索フロー（ハイブリッド）

ベクトル検索だけでは設定の前倒し改訂が混在して返ってくるため、年表DBとのハイブリッドで管理する。

```
クエリ受信
    ↓
時系列問い？（「いつ」「〜年」「建国」など）
    ├─ Yes → 年表DB優先検索（canon_statusでフィルタ）
    │         → 関連chunk_idsでベクトルDBから詳細取得
    └─ No  → ベクトル検索メイン
              → ヒットchunkに紐づく年表イベントも付加
    ↓
Context Builder（active/canon のみ返す・deprecated は明示）
    ↓
Gemini API
    ↓
Answer + Citations
```

---

## 6. 改訂管理の運用

設定が前倒し改訂されたとき：

1. 旧イベントの `canon_status` を `retconned` に変更
2. `revision_note` に改訂理由を記録
3. 新イベントを `canon` で作成
4. 旧イベントの `superseded_by` に新イベントIDを記録

プロンプトでの明示：

```
[現行設定] 〇〇は△△である（出典：Wiki 2024/3）
[廃止設定 ※参考のみ / 改訂理由：前倒し] かつて〇〇は□□であった
```

---

## 7. インジェスト4方式

| 方式 | トリガー | 処理 |
|------|----------|------|
| WikiページURL自動取得 | URLをチャットに貼る | HTTPスクレイピング → chunking → embedding → Supabase |
| mdファイルドロップ | ファイルをUIにドロップ | テキスト抽出 → chunking → embedding → Supabase |
| X発言手動ペースト | GUIにテキストをペースト | そのままchunking → embedding → Supabase |
| チャットメモ保存 | 「この設定を保存して」 | 直前の会話内容 → embedding → Supabase |

日次自動更新：Wikiをクロールして差分があれば旧チャンクをdeprecatedにして新チャンクを追加。

---

## 8. 秘密URL認証

```
# アクセス例
https://your-app.vercel.app/abc123secret

# AITuber接続例
wss://your-api.render.com/ws/chat?token=abc123secret
```

Next.js middlewareでトークンを検証。一致しない場合は403を返す。

---

## 9. 全体アーキテクチャ

```
[ブラウザ / AITuberソフト]
        ↓ HTTPS / WebSocket
[Next.js on Vercel]  ← 秘密URL認証
        ↓
[FastAPI on Render]
 ├─ POST /chat
 ├─ WS   /ws/chat        AITuber用
 ├─ POST /ingest/md
 ├─ POST /ingest/url
 ├─ POST /ingest/paste
 └─ POST /memo/save
        ↓
[Retriever]
 ├─ pgvector検索 (Supabase)
 ├─ 全文検索 (pg全文検索)
 └─ 年表DB検索 (timeline_events)
        ↓
[Context Builder]  active/canon のみ・deprecated は明示
        ↓
[Gemini API]
        ↓
Answer + Citations
```

---

## 10. 実装優先順位

1. Supabaseテーブル作成（chunks + timeline_events）
2. mdインポーター（ファイルドロップ取り込み）
3. 検索API + チャットUI（動作確認）
4. Wiki URLフェッチャー + 日次更新cron
5. WebSocketエンドポイント（AITuber接続）

---

## 改訂履歴

v1.0  2026-03  Claudeとの対話から初版を生成
