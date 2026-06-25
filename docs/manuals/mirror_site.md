# mirror_site.py

既存サイトを静的ファイル束にミラーするツール。SiteSucker の Python 版。

各ページを実ブラウザ（ヘッドレス Chromium）で開き、**HTML** と、そのページが
読み込む**すべてのファイル**（CSS・JS・画像・フォント…）を保存し、参照をローカル
相対パスに書き換える。出力フォルダをそのまま Cloudflare Pages 等に上げれば、
**元の動的サイト（WordPress 等）を停止できる**（攻撃対象面ごと畳める）。

> なぜ `requests` / `wget` ではなくブラウザか：ブラウザはページが実際に読み込む
> アセット（CSS 内から参照されるものを含む）を自分で発見して取得する。さらに `--js`
> を付ければ、本文を JavaScript で組み立てるページ（SPA）もレンダーして保存できる。

> **既定では JavaScript を実行しない。** 保存される HTML は**サーバーが返した生のまま**
> ＝小さく、クライアント側ウィジェット（広告 AdSense・アナリティクス）がレンダー時に
> 注入する巨大な iframe / DOM が入らない。本文を JS で描画するサイト（SPA 等）だけ
> `--js` を付ける（その分、ウィジェットで膨らんだ重い HTML になる）。ブラウザはどちらでも
> ページの読み込み・解析を行うので、リンクや静的参照の CSS・画像は常に保存される。

---

## セットアップ（初回のみ）

```bash
./.venv/bin/pip install playwright
./.venv/bin/playwright install chromium
```

> 既にマシンに Chromium があり、環境変数 `PLAYWRIGHT_BROWSERS_PATH`
> がそれを指している場合は、`playwright install` を省ける。

## 使い方

```bash
# 基本：https://example.com/ をクロールして ./mirror/ に保存
python3 tools/mirror_site.py https://example.com/ --out mirror

# ページ数の上限を上げる
python3 tools/mirror_site.py https://example.com/ --out mirror --max-pages 300

# 本文を JS で描画する SPA：JavaScript を実行してレンダー後の HTML を保存
python3 tools/mirror_site.py https://example.com/ --out mirror --js

# SPA など描画が遅いサイトで、読み込み後に追加待機（ミリ秒）。--js と併用
python3 tools/mirror_site.py https://example.com/ --out mirror --js --wait 1500

# 既存ファイルは再取得しない（中断からの再開・差分更新）
python3 tools/mirror_site.py https://example.com/ --out mirror --skip-existing
```

## オプション

| 引数 | 既定 | 説明 |
|---|---|---|
| `URL`（位置引数） | — | クロール開始 URL（例 `https://example.com/`）。**必須** |
| `--out DIR` | `mirror` | 出力ディレクトリ |
| `--max-pages N` | `200` | クロールする HTML ページ数の上限 |
| `--same-host-only` | **オン** | 開始ホストのリンクだけを辿る（既定で有効） |
| `--wait MS` | `0` | `networkidle` 到達後の追加待機（ミリ秒） |
| `--js` | オフ | JavaScript を実行し、レンダー後の HTML を保存。SPA など本文を JS で組み立てるサイト向け。**既定はオフ**（生 HTML を保存。広告・解析の注入 DOM が入らず軽量） |
| `--skip-existing` | オフ | 出力先に既にあるファイルは再取得しない。既存ページは取得をスキップ（リンクはディスク上の HTML から読み出してクロールは継続）、既存アセットは上書きしない。中断からの再開・差分更新に使う |

---

## 仕組み（処理の流れ）

1. **読み込み** — Playwright が各ページを開き、`networkidle`（通信が落ち着くまで、
   タイムアウト 45 秒）まで待つ。`--wait` 指定時はさらに待機。`page.content()` で
   HTML を取得。**既定**ではブラウザコンテキストを `java_script_enabled=False` で
   生成するため、ページのスクリプトは走らず、`page.content()` はサーバーが返した生
   HTML 相当（広告・解析の注入物なし）になる。`--js` 指定時のみ JS を実行し、レンダー
   後の HTML を保存する。リンク収集（後述）は Playwright の隔離実行環境で動くため、
   JS 無効でも機能する。
2. **リンク収集** — ページ内の `<a href>` を全部取り、絶対 URL 化＋フラグメント除去。
   `http(s)` のみ、`--same-host-only` なら開始ホストのみ、未訪問なら待ち行列へ
   （幅優先クロール）。`--skip-existing` で既存ページをスキップする場合は、ブラウザで
   開く代わりにディスク上の保存済み HTML から `<a href>` を正規表現で抜き出してリンク
   収集する（再取得せずクロールだけ継続できる）。
3. **アセット保存** — `response` イベントで、ページが読み込んだ **GET かつ 200 かつ
   非 HTML** のレスポンス本文（CSS・JS・画像・フォント等）をすべて保存。HTML は
   別途保存するのでここでは除外。`--skip-existing` 時は、出力先に既にあるファイルは
   上書きしない（ただし書き換えのためホスト名は記録する）。
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
| 保存 HTML が広告・解析コードで肥大化する | `--js` を付けて取得している。広告（AdSense）や解析がレンダー時に `<ins class="adsbygoogle">` や `<iframe>` を注入している。静的・サーバーレンダリングのサイトなら `--js` を外す（既定）と入らない |
| 本文が空・欠ける | そのページは本文を JS で描画している。`--js` を付けて取り直す（既定では JS を実行しないため、生 HTML に本文が無いと取れない） |
| `--skip-existing` で更新が反映されない | 出力先に既にあるページ／アセットは再取得されない。更新したいページは出力先の該当ファイルを削除してから実行する |
| 一部ページが取れない | `<a href>` で辿れないページ。開始 URL を変える、または手動で URL を追加クロール |
| 外部サイトまで保存される | 既定で `--same-host-only` は有効。ページ**リンク**は開始ホストのみ辿るが、ページが読み込む**アセット**はクロスオリジンでも `_ext/<host>/` に保存される（描画に必要なため） |
