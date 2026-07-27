# AI時代の暮らし — aiseed.dev

自然農法・リジェネラティブ農業の実践と、構造分析・ブログを発信するウェブサイト。

## サイト構成

```
html/
├── index.html             # トップページ
├── about/                 # 私たちのアプローチ
├── natural-farming/       # 自然農法とは
├── light-farming/         # Light Farming（Christine Jones博士の土壌科学）
│   ├── full/              # 論文全訳（前半）
│   └── full-2/            # 論文全訳（後半）
├── gallery/               # 畑の記録（写真）
├── privacy/               # プライバシーポリシー
├── insights/              # Insights — 構造分析（地政学・食料安全保障・AI）
├── dashboard/             # 物理量ダッシュボード（素のHTML/CSS/JS・静的JSON）
├── blog/                  # Blog — 構造分析ノート（時事・速報的な分析）
├── claude-debian/         # Claudeと一緒に学ぶDebian（全24章）
├── ai-native-ways/        # AIネイティブな仕事の作法（独立タイポグラフィ）
├── en/                    # 英語版サブツリー（/en/insights, /en/blog, /en/claude-debian, /en/ai-native-ways など）
├── css/style.css          # メインスタイルシート
├── js/main.js             # JavaScript
└── images/                # 画像素材
```

記事ソース（ビルド入力）は **シリーズ = 1つの AsciiDoc ファイル**。
日英両方の本文とフロントマターを1ファイルに持ち、
[pyasciidoc](https://github.com/aiseed-dev/pyasciidoc) がレンダリングする:

```
articles/
├── insights.adoc                  # Insights 全28章
├── blog.adoc                      # Blog 全44記事
├── claude-debian.adoc             # Claudeと一緒に学ぶDebian 全24章
├── claude-debian-server.adoc      # └ サーバー編 全11章
├── ai-native-ways.adoc            # AIネイティブな仕事の作法 全12章
├── ai-native-ways-software.adoc   # └ ソフトウェア開発編 全23章
├── phosphorus-and-farming.adoc    # リンと農業 全10章
├── fable.adoc                     # Fable 5 が帰ってきた 全9章(日本語のみ)
├── assets/<シリーズ>/<記事ID>/     # 画像・PDF(en- プレフィックスは EN 専用)
│   └── _root/                     # シリーズ直下のビルド入力(template-example.html 等)
└── examples/ai-native-ways/       # example-N/ サンプルコード
```

シリーズファイルの中の1記事は次の形。記事の並び順がそのまま prev/next
連鎖になる（手書きの連鎖キーは不要。隣の章の実タイトルと違う表記に
したいときだけ `prev_title.ja:` 等を明示する）:

```asciidoc
// ===== article: 021-software-three-transitions =====
---
slug: software-three-transitions
date: 2026.05.22
title.ja: 日本語タイトル
title.en: English title
description.ja: …
description.en: …
hero_image: IMG_3481.jpg
---
ifdef::lang-ja[]
= 日本語タイトル

日本語本文(AsciiDoc)。
endif::[]
ifdef::lang-en[]
= English title

English body.
endif::[]
```

- フロントマター: 日英で同じ値のキーは裸(`date:`)、異なる値は
  `key.ja` / `key.en`。`lang` は書かない(ビルド時に合成)。
- 本文は AsciiDoc: 見出し `==`、リスト `*`/`.`（入れ子は `**`/`..`）、
  引用 `____`、表 `|===`、区切り線 `'''`、強調 `*太字*`/`_斜体_`、
  チェーン図 `[.chain-diagram]` + `--`〜`--`（行末 ` +` で改行保持）、
  ハイライト `[.highlight-box]` + `--`〜`--`、Mermaid は ```` ```mermaid ````
  フェンスのまま。
- ビルドは `.build/articles/`（gitignore 済み）に従来型ツリーを展開して
  から行う（`tools/build/series.py`）。書き損じ（ifdef の閉じ忘れ等）は
  行番号付きで即エラーになり、開発サーバーはブラウザに赤バナーで表示する。

旧レイアウト（1記事=1フォルダの ja.md/en.md）のアーカイブは
`/home/dev/dev/website` に残っている。**今後の執筆・デプロイはこの
リポジトリで行うこと**（旧リポジトリからデプロイしない）。
Markdown からの一括変換は `tools/convert_md_to_adoc.py`、新旧ビルドの
突き合わせ検証は `tools/verify_migration.py`（判定除外は
`verify-allowlist.txt`）。

ヘッダーメニューの「記事」ドロップダウン配下に「構造分析」「AIネイティブな
仕事の作法」「Claudeと一緒に学ぶDebian」がぶら下がる（デスクトップはホバー、
モバイルはアコーディオン）。

## テーマ

- **自然農法**: 福岡正信氏の四原則（不耕起・無肥料・無農薬・無除草）
- **リジェネラティブ農業**: 土壌炭素固定、菌根菌ネットワーク、生物多様性
- **Light Farming**: Christine Jones博士の光合成ベースの土壌再生理論
- **Insights**: 構造的思考による分析（肥料危機、地政学、AIの使い方）
- **Blog**: 時事的な構造分析ノート（イラン戦争・サプライチェーン断絶など）
- **Claudeと一緒に学ぶDebian**: Claudeを横に置いて読む新しい形の教科書（全24章）
- **AIネイティブな仕事の作法**: 副題「AI 時代の自由人のための道具たち」。
  Office・Java・C# から離れて Markdown・JSON・Python で AI を同僚として
  使う実用エッセイ（独立タイポグラフィ、親シリーズ全 14 章）。
  第 1 章「AI（ChatGPT・Claudeなど）活用マニュアル」が普通の人向けの
  入口で 6 つのコツを置き、第 2 章以降がそれを領域別の道具立てに
  落としていく。サブシリーズ「ソフトウェア開発編」（全 11 章）で
  **ソフトウェア工学からリベラルアーツへの基盤転換** を論証。底流の
  概念フレーム（15 概念）は `framing-second-renaissance` スキルに集約
  ── 合成的入口はブログ
  [`021-software-three-transitions`](articles/blog/021-software-three-transitions/)

## 物理量ダッシュボード

`/dashboard/` に、構造分析で追ってきた **物理量**（価格・流量・在庫・残高・
残り日数）を一覧表示するダッシュボードがある。物理量・単位・観測日・出所だけを
提示し、主張も予測も載せない（読者が物理的事実から判断する）。

- フロント: [`html/dashboard/`](html/dashboard/) — 素の HTML/CSS/JS・ビルド工程なし・
  静的 JSON を 1 回 fetch して描画。
- パイプライン: [`tools/dashboard/`](tools/dashboard/) — Python 標準ライブラリのみ。
  `python3 -m tools.dashboard.build` で 取得 → 計算 → `html/dashboard/data/dashboard.json` を出力。
  新指標 = カタログに 1 レコード追加。詳細は [tools/dashboard/README.md](tools/dashboard/README.md)。

## 関連アプリ

- **[Debian 移行ウィザード (`apps/debian-migrate/`)](apps/debian-migrate/)** ──
  Python + Flet で書いた Windows / macOS / Linux 対応のデスクトップ
  アプリ。連載「Claudeと一緒に学ぶDebian」(第 4・6・7 章) を GUI に
  落とし、初心者でも事前準備 (アプリ棚卸し → 代替提案 → ハードウェア
  チェック → USB 作成ガイド) を進められるようにしたもの。API キー
  不要、AI 連携は「Claude 用プロンプトをコピー」ボタンで claude.ai
  に貼る方式。

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

Markdown で書いた Insights / Blog / 書籍 / AIネイティブな仕事の作法を HTML に変換する:

```bash
python3 tools/build_article.py --all                                                  # 全シリーズビルド
python3 tools/build_article.py articles/insights/11-healthcare-fiscal/ja.md           # 単一 Insights 記事
python3 tools/build_article.py articles/blog/013-phosphate-crisis-2027/ja.md          # 単一 Blog 記事
python3 tools/build_article.py articles/claude-debian/00-prologue/en.md               # 単一章 (EN)
python3 tools/build_article.py articles/ai-native-ways/00-prologue/ja.md              # 単一エッセイ
```

出力は `html/insights/`, `html/blog/`, `html/claude-debian/`, `html/ai-native-ways/`
および それらの `html/en/...` 配下。`--all` の最後で `html/sitemap.xml` と
`html/robots.txt` も再生成され、静的トップページ 10 件（JA/EN × home・about・
natural-farming・light-farming・privacy）の `style.css` / `main.js` 参照には
コンテンツハッシュ由来のキャッシュバスター `?v=<hash>` が刻印される。

全シリーズの記事・章ページは共通のエッセイ型テンプレート
（`tools/templates/chapter.html` / `chapter.en.html`）で描画される。
ai-native-ways の詳細は [articles/ai-native-ways/README.md](articles/ai-native-ways/README.md) 参照。

記法・オプションの詳細は [docs/manuals/build_article.md](docs/manuals/build_article.md) 参照（ツール全体の一覧は [tools/README.md](tools/README.md)）。

### 開発サーバー（ビルド + 監視 + 配信 + ライブリロード）

```bash
python3 tools/serve.py                # http://localhost:8000
python3 tools/serve.py --port 8080
```

`articles/`, `tools/templates/`, `html/{css,js}` を監視する。
`articles/<シリーズ>.adoc` の保存は**そのシリーズだけの差分ビルド**
（数秒）、それ以外の変更はフルビルド。ビルドが終わると開いている
ブラウザは**自動でリロード**される（配信 HTML に SSE クライアントを
注入）。ビルド失敗（ifdef の閉じ忘れ等）は、ブラウザ画面上部に
行番号付きの赤バナーで表示され、修正して保存すれば自動で消える。

### aiseed-builder(WordPress風の管理画面・いちばん簡単)

エンジニア向けの Zed を使わなくても、専用アプリでサイトを運営できる:

```bash
../aiseed-builder/aiseed_builder/main.py .    # あるいは Zed のタスク 0
```

WordPress の管理画面と同じ感覚——左のシリーズ一覧 → 記事一覧 →
タイトルをクリック → 本文を編集 → 「更新」。保存すると数秒でビルドされ、
プレビューは自動でリロードされる。本文だけを差し替えるので構造を壊す
心配がない。フォーム受信箱・公開面の点検(DNS)もプラグインとして入る。
サイト側の設定は `site.json` の `builder` キー。
詳細は [~/dev/aiseed-builder](../aiseed-builder/README.md)。

(`apps/site-editor/` は aiseed-builder の前身。汎用化して独立したので、
今後の開発は aiseed-builder 側で行う)

### Zed で書く

このリポジトリを Zed で開くと AsciiDoc 拡張が自動インストールされる
（`.zed/settings.json`）。執筆の流れ:

- **`Ctrl+Alt+P`** — ライブプレビュー開始（保存するたびブラウザに反映）
- **`Ctrl+Alt+B`** — 開いているシリーズだけビルド / **`Ctrl+Alt+Shift+B`** — フルビルド
- **`Ctrl+Shift+O`**（アウトライン）— シリーズ内の記事タイトル一覧へジャンプ
- スニペット: `art`（新しい記事の骨組み）、`quote`、`quoteby`、`chain`、
  `box`、`table`、`mermaid`、`img`、`note`
- タスク一覧はコマンドパレット → `task: spawn`（`.zed/tasks.json`）

### 任意のディレクトリをターゲットにする

`tools/build_article.py` と `tools/serve.py` はどこから起動しても、`--site`
でサイトディレクトリを明示できる（省略時はスクリプトの親ディレクトリ、
または環境変数 `AISEED_SITE`）。

サイト側に必要なレイアウト:

```
<site>/
├── articles/
│   ├── insights/         # Insights 記事 (NN-slug/{ja,en}.md)
│   ├── claude-debian/    # 任意: 書籍章 (NN-slug/{ja,en}.md)
│   ├── ai-native-ways/   # 任意: エッセイ連載 (NN-slug/{ja,en}.md)
│   └── blog/             # Blog 記事 (NNN-slug/{ja,en}.md + アセット)
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
