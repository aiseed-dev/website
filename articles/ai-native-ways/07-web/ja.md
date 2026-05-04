---
slug: web
number: "07"
title: Webを作る ── HTML+CSS+JavaScriptという原点回帰
subtitle: 中身は Markdown と Mermaid。外枠だけ HTML+CSS
description: Web を二層に分ける。中身は Markdown と Mermaid、外枠は最小限の HTML+CSS+JavaScript、両者を Python が繋ぐ。中身を Markdown に保てば、同じデータが Web 以外の用途(PDF、印刷、AI 分析、電子書籍)にも流用できる。
date: 2026.05.02
label: AI Native 07
title_html: 中身は <span class="accent">Markdown+Mermaid</span>。<br>外枠だけ <span class="accent">HTML+CSS+JS</span>。
prev_slug: business-systems
prev_title: 業務システムと付き合う ── 並行稼働で書き換える
next_slug: apps
next_title: アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ
---

# Webを作る ── HTML+CSS+JavaScriptという原点回帰

Web を作る道具を、**二層に分ける**。

- **中身**(コンテンツ): Markdown と Mermaid で書く
- **外枠**(フレーム): HTML と CSS と最小限の JavaScript

両者を Python が繋ぐ。これだけで、ビルドが消え、依存が消え、デプロイが軽くなる。そして ── ここが大きい ── **中身が Web 以外の用途にも流用できる**。

## React の疲れ

過去 10 年、Web 開発は「フレームワークの軍拡」だった。

jQuery、Backbone、Angular、React、Vue、Svelte。ビルドツールは Grunt、Gulp、Webpack、Rollup、Vite、Turbopack。CSS は Sass、Less、PostCSS、Tailwind、CSS-in-JS。サーバーサイドレンダリングは Next.js、Nuxt、Remix、SvelteKit、Astro。

これらは何かの問題を解いてきた。しかし、解いた問題と新しく作った問題を比べると、**割に合わない**ことが増えてきた。

- ビルド設定の習得に数週間かかる
- 依存パッケージが 1000 個以上になる
- セキュリティアップデートが毎週来る
- 一年後にビルドが通らなくなる
- 簡単な Web サイトを作るのに 100 MB のフォルダが要る

これは技術ではなく、自家製の複雑さだ。

## WordPress の罠

「自分は React なんか使っていない、WordPress だ」── 多くの人が、現在こう思っているはずだ。

それは正しい。世界の Web サイトの **約 43%** が WordPress で動いている。日本でも企業の公式サイト、個人ブログ、ニュースメディア、自治体の Web ── あらゆる場所に WordPress がある。

しかし、WordPress には WordPress の罠がある。React の罠と質は違うが、**深刻さは同じか、それ以上**だ。

**問題 1: コンテンツが MySQL に閉じ込められる**

WordPress の記事は、テキストファイルではなく、MySQL の中の HTML 混じりのレコードとして保存される。同じ記事を PDF にしたい、別のサイトに移したい、AI に渡して分析したい ── 全部、エクスポート作業から始まる。

しかも、エクスポート形式は `.xml`(WordPress 独自の WXR)で、HTML タグや独自ショートコード(`[gallery]` など)が混ざっている。**コンテンツが、WordPress に閉じ込められる**。これは第2章で見た「Excel に閉じ込められたデータ」と同じ構造だ。

**問題 2: プラグインがセキュリティ地雷原**

WordPress の機能拡張は、世界中の有志が作ったプラグインに頼る。一つのサイトに 20〜30 のプラグインが入っているのは普通だ。それぞれが定期的に脆弱性を出す。**サイト全体が攻撃面の集合体**になる。

世界の Web の 43% が WordPress で動くということは、攻撃者にとって **43% の標的が同じ装置**だということだ。Mythos 級の AI が来る時代に、これは致命的な構造になる(構造分析シリーズ第5章「Mythos が来た」参照)。

**問題 3: アップデートが壊す**

WordPress 本体、テーマ、プラグイン ── これらが互いに依存している。一つを更新すると、別のものが動かなくなる。「アップデートを当てたらサイトが落ちた」は WordPress 運用の日常だ。

**問題 4: PHP は AI の得意分野ではない**

WordPress のテーマやプラグインは PHP で書かれている。Claude は PHP も書けるが、Python よりは出力品質が安定しない。**AI ネイティブな仕事の道具立てとして、PHP は最適ではない**。

## WordPress から抜ける

WordPress を使っているなら、抜け道は明確だ。第6章で見た **並行稼働** と同じパターンで抜ける。

1. 既存の WordPress を残したまま、コンテンツを **Markdown にエクスポート** する(プラグインや CLI ツールで自動化、Claude が変換コードを書ける)
2. 新サイトを Markdown + 最小 HTML/CSS + Python で構築する
3. 同じ URL 構造を保つ(SEO 評価を維持)
4. ステージング環境で動作を確認、検索エンジンへのインデックス申請を準備
5. DNS を切り替える日を決める
6. 切り替え後、WordPress を読み取り専用にして 1 ヶ月運用
7. 問題なければ WordPress を停止、ホスティング契約を解除

費用面の効果も大きい。WordPress のマネージドホスティング(WP Engine、Kinsta など)は月額数千〜数万円。静的 HTML を Cloudflare Pages や GitHub Pages に置けば、**月額ゼロ円**になる。年間数万〜数十万円が消える。

> WordPress も並行稼働で抜ける。Markdown へエクスポートし、外枠だけ HTML/CSS で書き、Python で生成、静的配信する。これで WordPress を殺せる。

## 中身は Markdown + Mermaid。外枠は HTML+CSS+JS

Web サイトの本質は「中身」と「外枠」に分けられる。

| 種類 | 何を書くか | 道具 |
|---|---|---|
| **中身** | 文章、表、引用、コード、図 | **Markdown** + **Mermaid** |
| **外枠** | ヘッダー、ナビ、フッター、レイアウト、配色 | **HTML** + **CSS** + 最小限の JavaScript |
| **接続** | 中身を外枠に流し込んで HTML を生成 | **Python** |

これを混ぜて書くのが、これまでの Web 制作の罠だ。React のコンポーネントには、文章と書式とロジックが全部混ざっている。WordPress の記事には、HTML タグと文章が混ざっている。書き換えが地獄になる。

AI ネイティブな分け方は、**中身と外枠を完全に分離する**。中身は Markdown と Mermaid だけ。HTML タグは一切書かない。外枠は HTML と CSS で書くが、各記事の中身には触らない。Python が機械的に繋ぐ。

## なぜ中身を Markdown + Mermaid で持つか

中身を Markdown と Mermaid で書く最大の理由は、**データが Web 以外の用途でも使えるから**だ。

同じ Markdown ファイルから、

- Web ページが作れる(Python が HTML 化)
- PDF が作れる(`pandoc` でも Claude でも変換可能)
- 印刷用原稿に変換できる
- 電子書籍(EPUB)が作れる
- AI に渡して要約・翻訳・質問できる
- 別の媒体への貼り付けに流用できる
- Git で差分レビュー・履歴管理ができる
- 他の人と共同編集できる

**コンテンツが Web に閉じ込められない**。WordPress や Wix で書いたコンテンツは、サービスが終われば消える。Notion で書いたコンテンツは、Notion の形式に閉じ込められる。Markdown は、どこにも閉じ込められない。

これは、第1章「文書を書く」で見た「中身を Markdown に保つ」原則の Web 版だ。**入口・中身・出口を分ける**:

- **入口**: 各種フォーマット(画像、PDF、音声、Word)から Claude が Markdown 化
- **中身**: Markdown と Mermaid で持つ(Git でバージョン管理)
- **出口**: Web、PDF、印刷、AI 分析、電子書籍 ── 用途に応じて Python が変換

> 中身は Markdown に保つ。出口に応じて変換する。これが、データを 10 年後も使える形で残す方法だ。

## 外枠は最小限で書く

外枠 ── ヘッダー、ナビ、フッター、レイアウト、配色 ── は、HTML と CSS で **直接** 書く。**最小限**で。

- HTML テンプレートは 1〜数ファイル
- CSS は 1 ファイル(数百〜数千行)
- JavaScript は本当に必要な要素(モバイルメニューの開閉など)だけ、数十行

これらは年に数回しか触らない。**外枠を凝りすぎない**。骨格は骨格として置く。時間は中身に使う。

**捨てるもの**:

- JavaScript フレームワーク(React、Vue、Angular、Svelte)
- ビルドツール(Webpack、Vite、Turbopack、Parcel)
- TypeScript(JS で十分)
- CSS フレームワーク(Tailwind、Bootstrap)
- パッケージマネージャ(npm、yarn、pnpm)
- `node_modules`(`rm -rf node_modules` で消える)

**残すもの**:

- HTML(構造)── テンプレート 1 ファイル
- CSS(見た目)── 1 ファイル
- JavaScript(動的要素のみ、必要最低限)── 数十行
- Markdown + Mermaid(中身)── 記事ごとに 1 ファイル

生の Web 標準と Markdown だけだ。**AI が最も書きやすい組み合わせ**。HTML / CSS / JS は変換層がなく、Markdown は AI のネイティブ表記。両方とも Claude が出した出力をそのまま使える。

## Python が両者を繋ぐ

Markdown を HTML に、Mermaid 図を SVG または画像に、外枠テンプレートに流し込む ── これは Python スクリプトの仕事だ。

```
articles/foo/ja.md  ──→  Python  ──→  html/foo/index.html
                              ↑
                      tools/templates/article.html (外枠)
```

このスクリプトを書く必要は無い。**Claude に頼んで書いてもらう**。`markdown-it-py` で Markdown を HTML 化、`Jinja2` でテンプレートに流し込む。両方合わせて 100〜200 行で書ける。

依存は 3〜4 つだけ:

- `markdown-it-py` ── CommonMark パーサ
- `Jinja2` ── HTML テンプレートエンジン
- `Pillow` ── 画像処理(OG 画像生成など、必要なら)
- (Mermaid 図はブラウザ側でレンダリングするか、`mermaid-cli` で SVG 化)

`pip install -r requirements.txt` で完結。`node_modules` は無い。

このサイト ── aiseed.dev ── のビルドスクリプト(`tools/build_article.py`)も、ほとんど Claude が書いた。**ビルドツールは自分の手元に持つ**ことができる時代だ。フレームワークの規約に従うのではなく、自分の規約で書く。

## 動的処理は FastAPI 一択

「動的なサイトは作れないのでは?」と思うかもしれない。違う。

動的処理はサーバー側で書く。**Python の FastAPI、これ一つでいい**。

Flask、Django、Go、Rust、Ruby ── 選択肢は山ほどある。しかし、選択肢を増やせば、組織は分裂する。「FastAPI で書こう」と決めれば、それ以上の議論は終わる。**選んだら、選んだことを忘れる**。これが AI ネイティブな道具立ての考え方だ。

なぜ FastAPI か:

- **Python だから**、このシリーズ全体のスタックと一致する
- 型ヒントと Pydantic が自然に使える
- async が標準
- OpenAPI ドキュメントが自動生成される
- **Claude が一番書きやすい**(オープンソースで学習データが豊富)
- ボイラープレートが少ない

## それも、最小限にする

最小限とは、具体的にこういうことだ。

- **ORM を使わない**。SQLAlchemy は要らない。PostgreSQL ドライバ(asyncpg または psycopg)で SQL を直接叩く
- **層を増やさない**。Repository 層、Service 層、Domain 層 ── 要らない。リクエストを受け、SQL を実行し、HTML を返す。それだけ
- **依存を増やさない**。FastAPI、PostgreSQL ドライバ、Jinja2(必要なら)── 三つで十分
- **設定ファイルを増やさない**。環境変数だけで動く
- **マイクロサービスにしない**。一つのプロセスで動かす

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncpg

app = FastAPI()

@app.get("/items", response_class=HTMLResponse)
async def items():
    conn = await asyncpg.connect(...)
    rows = await conn.fetch("SELECT name, price FROM items")
    html = "".join(f"<li>{r['name']}: {r['price']}</li>" for r in rows)
    return f"<ul>{html}</ul>"
```

これだけで、「データベースから商品を取って HTML で返す」サーバーが動く。**これ以上の何が要るのか**を問い続ける。

Spring Boot の長大なクラス階層、Django の app/middleware/views/serializers、Express + Prisma + GraphQL のスタック ── これらは過去の複雑さの遺産だ。**Claude が直接 SQL を書ける時代に、ORM の抽象化は要らない**。

クライアント側の JavaScript も最小限。リンク遷移は `<a>` でいい。フォーム送信は `<form>` でいい。動的更新が要るなら HTMX(数 KB のライブラリ、フレームワークではない)。WebSocket は本当に必要なときに追加する。**最初から SPA を作らない**。

## これで 9 割は足りる

例えば、社内の在庫管理 Web アプリ:

```
ブラウザ ─→ FastAPI (Python, 1 ファイル, 200 行) ─→ PostgreSQL
```

これで動く。フロントエンド、バックエンド、データベース、すべて 1 人で作れる。Claude がコードを書く。**ユーザー数百人、レコード数百万件まで普通に動く**。

性能のために最初からマイクロサービスを設計する必要はない。実際に詰まったら、その時にスケールアウトを設計する。**9 割の業務 Web アプリは、そこまで来ない**。

選択肢を絞ることは、自由を捨てることではない。**思考を捨てる対象を絞ること**だ。技術選択の議論に時間を使わない。FastAPI と SQL と Jinja2 で書く。AI と一緒に。

> 動的層は、FastAPI 一択、最小限。

## デプロイも軽い

静的 HTML のデプロイは、ファイルをコピーするだけだ。

- Cloudflare Pages、GitHub Pages、Netlify、Vercel ── 全部無料か低価格
- 自分のサーバーに置きたければ、`scp` で送るだけ
- CDN に乗せれば、世界中で高速

CI/CD パイプラインも単純になる。「Markdown が変わったら Python ビルドして、HTML を CDN にアップロードする」── 数行のスクリプトで終わる。

## 10年後も動く

React のバージョン v15 で書いたコンポーネントは、v18 ではビルドできないことがある。Webpack の設定は 1 年ごとに書き直しを迫られる。

HTML、CSS、JavaScript の基本仕様は、25 年以上後方互換が保たれている。1999 年の HTML ファイルは、今のブラウザでも問題なく動く。**生の Web 標準は時間に強い**。

Markdown も、20 年前の規格(2004 年初版)からほとんど変わっていない。20 年後も同じファイルが読める。**外枠も中身も、時間を超える形式で持つ**。

> フレームワークは時代に依存する。Web 標準と Markdown は時代を超える。

## 実例: 数字で見る

React + Next.js + TypeScript + Tailwind で業務 Web 構築: 開発 **3 ヶ月**、依存パッケージ **約 1,200 個**、ビルド時間 **3 分**、`node_modules` **500 MB**。同じ機能を HTML+CSS+FastAPI+Markdown で構築: 開発 **2 週間**、依存 **4 個**、ビルド **5 秒**、合計 **10 MB**。

WordPress マネージドホスティング(WP Engine、Kinsta 等): 月額 **5,000〜30,000 円**。静的 HTML を Cloudflare Pages: 月額 **ゼロ円**。年間 **6 万〜36 万円の節約**。

ページ表示速度: Next.js + Vercel の動的レンダリング **約 800 ms**。静的 HTML + CDN **約 50 ms**。**16 倍速い**。

このサイト(aiseed.dev)の規模: **150 ページ以上、合計 30,000 行のコード、24 時間で組み上げた**。React・Next.js・TypeScript はゼロ。Markdown と Mermaid と最小 HTML/CSS だけ。

## 実例: 個人ブログを 30 分で世界配信する

Markdown と最小 HTML/CSS で、Cloudflare Pages にデプロイ。CDN 経由で世界配信、月額ゼロ円。

**手順 1: 最小プロジェクト構造**

```bash
mkdir myblog && cd myblog
mkdir -p src/posts templates html
```

```
myblog/
├── src/
│   ├── posts/        # Markdown 記事
│   └── style.css     # CSS
├── templates/
│   └── post.html     # 記事テンプレート
├── build.py          # ビルドスクリプト
└── html/             # 出力先
```

**手順 2: Claude にビルドスクリプトを書かせる**

```
あなた: src/posts/*.md を読んで、templates/post.html に流し込み、
        html/posts/{slug}/index.html に書き出す Python を書いて。
        markdown-it-py と Jinja2 を使う。
```

返ってくる `build.py`(80 行):

```python
from pathlib import Path
import markdown_it, jinja2, frontmatter

md = markdown_it.MarkdownIt()
env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

for src in Path("src/posts").glob("*.md"):
    post = frontmatter.load(src)
    html = md.render(post.content)
    out = Path(f"html/posts/{post['slug']}/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(env.get_template("post.html").render(
        title=post["title"], date=post["date"], body=html
    ))

# トップページとサイトマップ生成も同じ要領で...
```

**手順 3: 記事を書く**

```bash
cat > src/posts/2026-05-01.md <<EOF
---
slug: ai-native-ways
title: AIネイティブな仕事の作法
date: 2026.05.01
---

道具を変えれば、思考が変わる...
EOF
```

**手順 4: ビルド**

```bash
pip install markdown-it-py Jinja2 python-frontmatter
python3 build.py
```

`html/` 配下に静的サイトが完成。

**手順 5: Cloudflare Pages にデプロイ**

```bash
git init && git add -A && git commit -m "init" && git push
```

Cloudflare Pages のダッシュボードで GitHub リポジトリを連携、ビルドコマンド `python3 build.py`、出力ディレクトリ `html/` を指定。**5 分で世界配信開始**。

**手順 6: 表示速度を測る**

```bash
curl -w "%{time_total}\n" -o /dev/null -s https://myblog.pages.dev/posts/ai-native-ways/
```

返ってくる時間: `0.048` 秒。**世界どこからアクセスしても 50ms 以下**。WordPress マネージドホスティングでは到達できない速度。

**手順 7: 装飾を追加 ── Claude デザインで**

```
あなた: 個人ブログのトップページの HTML+CSS を、Linear のような
        落ち着いた配色で。Markdown 記事を綺麗に並べる
```

返ってくる HTML/CSS をテンプレートに組み込めば、**Silicon Valley のスタートアップ並みの見栄え**で記事が並ぶ。

**月額コスト**: Cloudflare Pages 無料プラン = **0 円**。同等品質を WordPress + WP Engine で実現すると月 5,000〜30,000 円。**年間で数十万円の差**、しかも速度は静的のほうが速い。

aiseed.dev 自体がこの構成。**150 ページ以上、React 無し、ビルド 5 秒、依存パッケージ 4 つ**。

## まとめ

Web を作る道具を、二層に分ける。

中身は **Markdown と Mermaid**。外枠は **HTML と CSS と最小限の JavaScript**。両者を **Python が繋ぐ**。

これでビルドが消え、依存が消え、デプロイが軽くなる。**そして、中身が Web 以外の用途にも流用できる**。同じ Markdown が、PDF にも、印刷にも、AI への入力にも、電子書籍にもなる。

このサイトがその実証だ。30,000 行のコード、150 ページ以上、24 時間で組み上げた。React は使っていない。Markdown と Mermaid と最小 HTML/CSS。それで何の問題もない。

次の章では、アプリを作る話に進む。CLI ツール、Flet アプリ、Flutter アプリ ── 段階的にスケールアップ。

---

## 関連記事

- [第1章: 文書を書く ── Markdownという最小の選択](/ai-native-ways/markdown/)
- [第3章: デザインをする ── Mermaid と Claude デザインで作る](/ai-native-ways/design/)
- [第6章: 業務システムと付き合う ── 並行稼働で書き換える](/ai-native-ways/business-systems/)
- [第4章: 処理を書く ── AIにPythonで書いてもらう](/ai-native-ways/python/)
- [構造分析15: Mythos時代のセキュリティ設計](/insights/security-design/)
