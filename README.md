# AI時代の暮らし — aiseed.dev

自然農法・リジェネラティブ農業の実践と、構造分析・ブログを発信するウェブサイト。

## サイト構成

```
html/
├── index.html          # トップページ
├── about/              # 自然農法とは
├── light-farming/      # Light Farming（Christine Jones博士の土壌科学）
│   ├── full/           # 論文全訳（前半）
│   └── full-2/         # 論文全訳（後半）
├── gallery/            # 畑の記録（写真）
├── insights/           # Insights — 構造分析（地政学・食料安全保障・AI）
├── blog/               # Blog — 構造分析ノート（時事・速報的な分析）
├── claude-debian/      # Claudeと一緒に学ぶDebian（全24章の書籍）
├── natural-farming/    # 自然農法（旧版）
├── contact/            # お問い合わせ
├── en/                 # 英語版サブツリー（/en/insights, /en/blog, /en/claude-debian など）
├── css/style.css       # メインスタイルシート
├── js/main.js          # JavaScript
└── images/             # 画像素材
```

Markdown ソース（ビルド入力）はリポジトリ直下:

```
articles/
├── insights/           # Insights 記事（NN-slug.md, en-NN-slug.md）
└── claude-debian/      # Claudeと一緒に学ぶDebian（NN-slug.md, en-NN-slug.md）
blog/                   # Blog 記事（NNN-slug.md, en-NNN-slug.md）
```

ヘッダーメニューでは「記事」親項目の下に「構造分析」と「Claudeと一緒に学ぶDebian」がぶら下がる（デスクトップはホバー、モバイルはアコーディオン）。

## テーマ

- **自然農法**: 福岡正信氏の四原則（不耕起・無肥料・無農薬・無除草）
- **リジェネラティブ農業**: 土壌炭素固定、菌根菌ネットワーク、生物多様性
- **Light Farming**: Christine Jones博士の光合成ベースの土壌再生理論
- **Insights**: 構造的思考による分析（肥料危機、地政学、AIの使い方）
- **Blog**: 時事的な構造分析ノート（イラン戦争・サプライチェーン断絶など）
- **Claudeと一緒に学ぶDebian**: Claudeを横に置いて読む新しい形の教科書（全24章）

## 技術構成

- 静的HTML/CSS/JS
- Google Fonts: Zen Old Mincho, Noto Sans JP
- Google Analytics: G-9FLQ963JXM
- ホスティング: aiseed.dev

## 開発

### セットアップ

```bash
pip install -r requirements.txt
```

### ビルド

Markdown で書いた Insights / Blog / 書籍記事を HTML に変換する:

```bash
python3 tools/build_article.py --all                                         # 全記事ビルド
python3 tools/build_article.py articles/insights/09-healthcare-fiscal.md     # 単一 Insights 記事
python3 tools/build_article.py blog/013-phosphate-crisis-2027.md             # 単一 Blog 記事
python3 tools/build_article.py articles/claude-debian/00-prologue.md         # 単一章
```

出力は `html/insights/`, `html/blog/`, `html/claude-debian/`, および
それらの `html/en/...` 配下。`--all` の最後で `html/sitemap.xml` と
`html/robots.txt` も再生成され、静的トップページ 8 件（JA/EN × home・about・
natural-farming・light-farming）の `style.css` / `main.js` 参照には
コンテンツハッシュ由来のキャッシュバスター `?v=<hash>` が刻印される。

記法・オプションの詳細は [tools/README.md](tools/README.md) 参照。

### 開発サーバー（ビルド + 監視 + 配信）

```bash
python3 tools/serve.py                # http://localhost:8000
python3 tools/serve.py --port 8080
```

`articles/`, `blog/`, `tools/templates/`, `html/{css,js}` を監視し、変更があれば
`build_article.py --all` を自動実行する。ブラウザのリロードは手動（CSS/JS は
`?v=<hash>` が変わるので強制リロード不要）。

### 任意のディレクトリをターゲットにする

`tools/build_article.py` と `tools/serve.py` はどこから起動しても、`--site`
でサイトディレクトリを明示できる（省略時はスクリプトの親ディレクトリ、
または環境変数 `AISEED_SITE`）。

サイト側に必要なレイアウト:

```
<site>/
├── articles/
│   ├── insights/         # Insights 記事 (NN-slug.md, en-NN-slug.md)
│   └── claude-debian/    # 任意: 書籍章 (NN-slug.md, en-NN-slug.md)
├── blog/                 # Blog 記事 (NNN-slug.md, en-NNN-slug.md)
├── html/                 # 出力先（index.html, css/, js/, images/ 等）
├── tools/templates/      # 任意: ここにテンプレートを置けばバンドルを上書き
└── site.json             # 任意: site_url, site_name, copyright_text 等の上書き
```

`site.json` の例:

```json
{
  "site_url": "https://example.com",
  "site_name": { "ja": "自分のサイト", "en": "My Site" },
  "copyright_text": { "ja": "自分のサイト", "en": "My Site" },
  "default_og_image": "/images/og-default.jpg"
}
```

```bash
# 別のサイトをビルド
python3 /path/to/website/tools/build_article.py --site /path/to/other-site --all

# 別サイトの開発サーバーを起動
python3 /path/to/website/tools/serve.py --site /path/to/other-site

# 環境変数で既定を与える
export AISEED_SITE=/path/to/other-site
python3 /path/to/website/tools/build_article.py --all
```

### 新しいサイトをゼロから始める

`tools/init_site.py` が最小のサンプルサイト（articles/insights / blog / html /
tools/templates / site.json / CLAUDE.md / README.md）を任意ディレクトリに
展開する:

```bash
python3 /path/to/website/tools/init_site.py /path/to/new-site
python3 /path/to/website/tools/build_article.py --site /path/to/new-site --all
python3 /path/to/website/tools/serve.py --site /path/to/new-site
```

- 既存ファイルは既定でスキップ。上書きしたい場合は `--force`
- 何が書かれるかだけ見たい場合は `--dry-run`
- 利用可能なスキャフォールド一覧は `--list`

スキャフォールドは `tools/scaffolds/default/` にあり、CSS・テンプレート・
`CLAUDE.md` は Claude Code で扱いやすい最小構成になっている。

### 静的配信のみ

既にビルド済みの HTML をそのまま確認する場合:

```bash
cd html && python3 -m http.server 8000
```
