# mirror_site.py

既存の動的サイト（WordPress 等）を、**JavaScript 実行後の状態ごと**静的ファイル束に
ミラーするツール。SiteSucker の Python 版。

各ページを実ブラウザ（ヘッドレス Chromium）で開いて JS を走らせ、**レンダー後の
HTML** と、そのページが読み込む**すべてのファイル**（CSS・JS・画像・フォント…）を
保存し、参照をローカル相対パスに書き換える。出力フォルダをそのまま
Cloudflare Pages 等に上げれば、**元の動的サイトを停止できる**（攻撃対象面ごと畳める）。

> なぜ `requests` / `wget` ではなくブラウザか：それらは JavaScript を実行しないため、
> 最近のサイトでは本文が生 HTML に入っていない。Playwright で先にレンダーする。

> **JS が HTML を肥大化させる場合は `--no-js`。** クライアント側ウィジェット、とくに
> 広告（AdSense）やアナリティクスは、レンダー時に巨大な iframe / DOM を注入し、それが
> 保存ページに焼き込まれる。静的・サーバーレンダリングのサイトには不要なので、`--no-js`
> で JavaScript を無効化する。ブラウザはページの読み込み・解析は行う（リンクや静的参照の
> CSS・画像は保存される）が、スクリプトは走らないため、HTML は**サーバーが返した生のまま**
> ＝小さく、広告・解析の注入物がない状態で保存される。

---

## セットアップ（初回のみ）

```bash
./.venv/bin/pip install playwright
./.venv/bin/playwright install chromium
```

> この環境では Chromium がプリインストール済み（`PLAYWRIGHT_BROWSERS_PATH`）。
> その場合 `playwright install` は不要。

## 使い方

```bash
# 基本：https://example.com/ をクロールして ./mirror/ に保存
python3 tools/mirror_site.py https://example.com/ --out mirror

# ページ数の上限を上げる
python3 tools/mirror_site.py https://example.com/ --out mirror --max-pages 300

# SPA など描画が遅いサイトで、読み込み後に追加待機（ミリ秒）
python3 tools/mirror_site.py https://example.com/ --out mirror --wait 1500

# JS を実行せず、サーバーが返す生 HTML を保存（広告・解析の注入物が入らない）
python3 tools/mirror_site.py https://example.com/ --out mirror --no-js
```

## オプション

| 引数 | 既定 | 説明 |
|---|---|---|
| `URL`（位置引数） | — | クロール開始 URL（例 `https://example.com/`）。**必須** |
| `--out DIR` | `mirror` | 出力ディレクトリ |
| `--max-pages N` | `200` | クロールする HTML ページ数の上限 |
| `--same-host-only` | **オン** | 開始ホストのリンクだけを辿る（既定で有効） |
| `--wait MS` | `0` | `networkidle` 到達後の追加待機（ミリ秒） |
| `--no-js` | オフ | JavaScript を無効化し、サーバーの生 HTML を保存。広告・解析が注入する DOM が入らず軽量。静的・サーバーレンダリングのサイト向け |

---

## 仕組み（処理の流れ）

1. **レンダー** — Playwright が各ページを開き、`networkidle`（通信が落ち着くまで、
   タイムアウト 45 秒）まで待つ。`--wait` 指定時はさらに待機。`page.content()` で
   レンダー後の HTML を取得。`--no-js` 指定時はブラウザコンテキストを
   `java_script_enabled=False` で生成するため、ページのスクリプトは走らず、
   `page.content()` はサーバーが返した生 HTML 相当（広告・解析の注入物なし）になる。
   リンク収集（後述）は Playwright の隔離実行環境で動くため、JS 無効でも機能する。
2. **リンク収集** — ページ内の `<a href>` を全部取り、絶対 URL 化＋フラグメント除去。
   `http(s)` のみ、`--same-host-only` なら開始ホストのみ、未訪問なら待ち行列へ
   （幅優先クロール）。
3. **アセット保存** — `response` イベントで、ページが読み込んだ **GET かつ 200 かつ
   非 HTML** のレスポンス本文（CSS・JS・画像・フォント等）をすべて保存。HTML は
   別途レンダー版を保存するのでここでは除外。
4. **書き換え** — クロール後、保存し終えた全ホストを把握したうえで、**ページ HTML と
   `.css` ファイル**の中の絶対参照をローカルパスへ置換（下記）。
5. **出力** — `--out` 配下に静的ファイル束として書き出す。

### パスの対応規則

`local_rel()` がページ／アセットの URL をローカル相対パスへ写像する。

- **開始ホスト** → ルート相対（例 `/blog/foo/` → `blog/foo/index.html`）
- **別ホスト（クロスオリジン）のアセット** → `_ext/<host>/...` 配下
- **ページのルーティング** — どのページも「ディレクトリ＋ `index.html`」として扱う:
  - 末尾 `/` → `index.html` を付与
  - 末尾セグメントに `.` が無い → `/index.html` を付与
  - ファイル名で終わるページ URL → 既に `.html` でなければ `/index.html` を付与

### URL 書き換え規則

`rewrite_text()` が、保存した各ホストについて（長いホスト名から順に）
`https://host` / `http://host` / `//host` を次へ置換する:

- **開始ホスト** → 空文字（＝ルート相対パスになる）
- **別ホスト** → `/_ext/<host>`

この書き換えは **ページ HTML と `.css` のみ**に適用される。

---

## 出力ディレクトリの構造

```
mirror/
  index.html              # 開始ページ
  blog/foo/index.html     # 各ページ（path → path/index.html）
  wp-content/.../style.css # アセットは元のパスのまま
  wp-content/.../app.js
  images/hero.jpg
  _ext/fonts.gstatic.com/...   # クロスオリジンのアセット
```

## 確認とデプロイ

```bash
# ローカルで確認
./.venv/bin/python -m http.server --directory mirror 8000
# → http://localhost:8000/

# Cloudflare Pages へデプロイ（このリポジトリの補助ツール）
python3 tools/cloudflare_pages_deploy.py   # 使い方は同スクリプト参照
```

静的化して配信に切り替えたら、**元の動的オリジン（WordPress 等）を停止**できる。

---

## 制限・既知のエッジケース

このスクリプトは**出発点**で、以下は未対応（必要なら手で直すか、AI と一緒に拡張する）。

- **`srcset`（レスポンシブ画像）** — 書き換え対象外。複数 URL を持つ `srcset` の
  参照は手当てが要る。
- **JS が実行時に組み立てる URL** — 文字列連結等で動的生成される参照は捕捉・
  書き換えできない。
- **クエリ文字列付きアセット**（`style.css?v=123` 等） — 保存はパス部分のみ
  （`urlparse().path`）で行うため、HTML 側にクエリが残ると参照がずれて 404 に
  なりうる。
- **`.js` ファイル内の絶対 URL** — 書き換えは HTML と `.css` のみ。JS 内に残る
  開始ホストへの絶対 URL は、停止後のオリジンを指したままになる。
- **`<a href>` 以外の遷移** — JS ナビゲーション・フォーム・サイトマップのみで
  到達するページは辿られない（リンクとして `<a>` に出ていないため）。
- **保存対象** — `GET` かつ `200` かつ非 HTML のみ。POST・リダイレクト・エラー
  応答で得られる資産は保存されない。
- **`networkidle` 45 秒**で固定。落ち着かないページはスキップされる（標準エラーに
  `skip <url>: ...` を出力）。`--wait` は idle 後の追加待機であって、この
  タイムアウト自体は延ばさない。

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| `playwright is not installed` | 上記セットアップを実行 |
| ページが `skip ...` でスキップされる | `networkidle` に達していない。`--wait` を足すか、対象ページを個別に確認 |
| スタイル・画像が崩れる | `srcset` / JS 生成 URL / クエリ文字列付きアセットの可能性（上記制限） |
| 保存 HTML が広告・解析コードで肥大化する | `<ins class="adsbygoogle">` や `<iframe>` がレンダー時に展開・注入されている。静的・サーバーレンダリングのサイトなら `--no-js` で取り直す |
| `--no-js` で本文が空・欠ける | そのページは本文を JS で描画している。`--no-js` を外す（このオプションは生 HTML に本文が入っているサイト専用） |
| 一部ページが取れない | `<a href>` で辿れないページ。開始 URL を変える、または手動で URL を追加クロール |
| 外部サイトまで保存される | 既定で `--same-host-only` は有効。ページ**リンク**は開始ホストのみ辿るが、ページが読み込む**アセット**はクロスオリジンでも `_ext/<host>/` に保存される（描画に必要なため） |
