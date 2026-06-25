# build_creativeweb_archive.py

旧サイト **creativeweb.jp**（ASP.NET Core MVC + Razor）を、`aiseed.dev` 上の
静的アーカイブ `/creativeweb/` に書き出すツール。

旧サイトは動的フレームワーク上で動くが、コンテンツ自体は実質静的だった
（シェルは Razor にハードコード、本文は HTML フラグメント、メタ情報は JSON）。
このツールは **.NET を一切動かさず**、リポジトリ内のデータを直接読んで
静的 HTML を生成する。生成時に:

- **AdSense** と **旧 Google Analytics（UA-16580464-4）** を完全に除去
- **aiseed の Google Analytics（G-9FLQ963JXM）** を全ページに注入
- ルート絶対パス（`/css`, `/img`, `/umb`, `/archive` …）を `/creativeweb/` 配下へ書き換え
- 旧サイトの 301 リダイレクト（textpage.json の `RedirectUrl`）を meta-refresh stub で再現

## 入力（旧サイトのリポジトリ）

`--src` には CreativeWeb プロジェクトのルート（`.csproj` のある階層）を渡す。
読むのは以下だけ:

```
<src>/App_Data/config/textpage.json     # テキストページのメタ（14セクション）
<src>/App_Data/config/blogindex.json    # ブログ記事インデックス（249件）
<src>/App_Data/config/categorydata.json # ブログのカテゴリー
<src>/App_Data/config/manga.json        # マンガのシリーズ/各話
<src>/App_Data/html/**/*.html           # 本文フラグメント
<src>/wwwroot/{css,js,lib,fonts,images,img}  # 静的アセット
<src>/Views/About|PrivacyPolicy/Index.cshtml # この2ページだけ本文が cshtml 内
```

## 使い方

```bash
# 生成（出力先を空にしてから）
python3 tools/build_creativeweb_archive.py \
    --src /home/niji/dev/aiseed-dev/CreativeWeb/CreativeWeb \
    --out html/creativeweb --clean
```

| オプション | 既定 | 説明 |
|---|---|---|
| `--src DIR` | （必須） | CreativeWeb プロジェクトのルート |
| `--out DIR` | （必須） | 出力先。通常 `html/creativeweb` |
| `--clean` | off | 出力先を削除してから生成 |
| `--img-mode {referenced,all}` | `referenced` | `img/`（228MB）を参照画像のみ（既定）か全部コピーするか |
| `--no-assets` | off | アセットコピーをスキップ（HTML だけ素早く再生成） |

### img-mode について

`wwwroot/img` は 228MB / 3759 ファイルあるが、実際に本文から参照されるのは
約 1200 枚（~91MB）。既定の `referenced` は生成 HTML/CSS を走査して
参照された画像だけをコピーし、リポジトリの肥大を抑える。完全な原本コピーが
要るときだけ `--img-mode all`。

## 出力（約449ページ）

`html/creativeweb/` 配下に、旧サイトと同じパス構造で生成する:

| 種別 | 出力パス | 数 |
|---|---|---|
| テキストページ | `/{part}/{name}/index.html`（`home/index`→`/index.html`） | ~83 |
| 孤立フラグメント | textpage.json 未登録だが実在する本文も救済 | ~1 |
| リダイレクト stub | 旧→新の 301 を meta-refresh で再現 | ~23 |
| ブログ記事 | `/archive/{id}/index.html` | 249 |
| ブログ索引 | `/blog/index.html`、`/blog/page/{n}/index.html`（5件/頁） | ~50 |
| ブログカテゴリー | `/blog/categories/`、`/blog/categories/{cat}/` | ~11 |
| マンガ | `/manga/`、`/manga/{series}/`、`/manga/{series}/{page}/` | ~32 |

各ページ上部に「これは creativeweb.jp のアーカイブです」バーを表示する。

### 除外したもの（移行時のユーザー決定）

- **`/learning/`**（オンライン教室）— 別途扱うためアーカイブに含めない。ナビからも除外
- **ブログ検索 / お問い合わせフォーム / Disqus コメント** — 静的化で動かないため除去。
  お問い合わせは aiseed.dev への案内ページに差し替え

### 既知の壊れたリンク

生成物の内部リンク約 28,000 本のうち ~114 本が 404 になるが、これらは
**旧 WordPress 時代の permalink（`/wp/archives/...`）や、ライブ環境でも
既に欠落している画像** など、原本（creativeweb.jp 本体）でも 404 だったもの。
アーカイブは原本と同じ状態を保つ。

## デプロイ

生成物（~114MB）は **リポジトリにコミットしない**。コミットするのはこの
スクリプトだけで、デプロイ前に毎回再生成する:

```bash
cd /home/niji/dev/aiseed-dev/website
python3 tools/build_creativeweb_archive.py \
    --src /home/niji/dev/aiseed-dev/CreativeWeb/CreativeWeb \
    --out html/creativeweb --clean
python3 tools/deploy.py        # ./html を Cloudflare Pages (aiseed-dev) へ
```

→ `https://aiseed.dev/creativeweb/` で配信。

## 旧ドメイン creativeweb.jp の停止とリダイレクト

creativeweb.jp は さくら VPS で動いていたが廃止予定。**VPS を落としても
旧 URL が生き続ける**よう、Cloudflare 側でリダイレクトするのが推奨。
アーカイブは旧サイトと同じパス構造を `/creativeweb/` 配下に持つので、
「パス先頭に `/creativeweb` を足すだけ」で旧 URL が全部つながる:

```
creativeweb.jp/umb/install/  →  https://aiseed.dev/creativeweb/umb/install/
creativeweb.jp/archive/9     →  https://aiseed.dev/creativeweb/archive/9
```

### 推奨: Cloudflare（サーバー不要）

1. **creativeweb.jp を Cloudflare に追加** — Add a site → `creativeweb.jp`。
   表示された 2 つのネームサーバーを **.jp ドメインのレジストラ側で設定**
   （NS を Cloudflare へ向ける）。これで DNS 管理が VPS から切り離される。
2. **ダミー DNS レコード** — リダイレクトを発火させるために必要。
   - A レコード `creativeweb.jp` → `192.0.2.1`（ダミー）、**Proxied（オレンジ雲）**
   - CNAME `www` → `creativeweb.jp`、**Proxied**
   - エッジでリダイレクトされるので、この IP には実際にはアクセスされない。
3. **Redirect Rule**（Rules → Redirect Rules → Create）
   - When: `Hostname` `contains` `creativeweb.jp`
   - Then: Dynamic redirect / Status `301` / Preserve query string ON
   - Expression:
     ```
     concat("https://aiseed.dev/creativeweb", http.request.uri.path)
     ```

これで全パス＋クエリ付きで 301 転送、証明書も Cloudflare が自動発行。
**VPS は停止して良い。**

### 代替: 自前サーバー（nginx）

サーバーを 1 台維持する場合の vhost:

```nginx
server {
    server_name creativeweb.jp www.creativeweb.jp;
    return 301 https://aiseed.dev/creativeweb$request_uri;
    # 443 用に Let's Encrypt 証明書が必要
}
```

廃止前提ならサーバー維持コストがかかるため非推奨。

## 依存

標準ライブラリのみ（追加インストール不要）。
