---
slug: web
number: "07"
title: Webを作る ── HTML+CSS+JavaScriptという原点回帰
subtitle: React は要らない。フレームワークの罠から抜ける
description: Web サイトの 9 割は、HTML と CSS と最小限の JavaScript で十分だ。React も Next.js も Vite も要らない。AI が書けるのは生の HTML/CSS/JS。フレームワークを捨てれば、ビルドが消える、依存が消える、10年後も動く。
date: 2026.05.02
label: AI Native 07
title_html: Web は <span class="accent">HTML+CSS+JavaScript</span> で十分だ。<br>原点に戻る。
prev_slug: business-systems
prev_title: 業務システムと付き合う ── 並行稼働で書き換える
next_slug: apps
next_title: アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ
---

# Webを作る ── HTML+CSS+JavaScriptという原点回帰

Web を作る道具を、HTML と CSS と最小限の JavaScript に戻す。

それだけで、ビルドが消える、依存が消える、デプロイが軽くなる。AI が書きやすい言語で、AI が書きやすい量だけ書く。**Web サイトの 9 割は、これで十分だ**。

## React の疲れ

過去 10 年、Web 開発は「フレームワークの軍拡」だった。

jQuery、Backbone、Angular、React、Vue、Svelte。ビルドツールは Grunt、Gulp、Webpack、Rollup、Vite、Turbopack。CSS は Sass、Less、PostCSS、Tailwind、CSS-in-JS。サーバーサイドレンダリングは Next.js、Nuxt、Remix、SvelteKit、Astro。

これらは何かの問題を解いてきた。しかし、解いた問題と、新しく作った問題を比べると、**割に合わない**ことが増えてきた。

- ビルド設定の習得に数週間かかる
- 依存パッケージが 1000 個以上になる
- セキュリティアップデートが毎週来る
- 一年後にビルドが通らなくなる
- 簡単な Web サイトを作るのに 100MB のフォルダが要る

これは技術ではなく、自家製の複雑さだ。

## 静的 HTML で 9 割は足りる

Web サイトの 9 割は、本当のところ、ただの文書配信だ。

会社案内、製品紹介、ブログ、技術文書、ポートフォリオ、メニュー表、料金表、お問い合わせ ── これらに React は要らない。HTML と CSS で十分だ。動的要素が要るなら、最小限の JavaScript を直接書けばいい。

このサイト ── aiseed.dev ── も、静的 HTML / CSS / JavaScript で動いている。Markdown を Python で HTML に変換して、Cloudflare で配信する。React も Next.js も使っていない。**それで何の問題もない**。

> Web サイトの 9 割は文書配信だ。文書配信に React は要らない。

## AI が書きやすい言語

HTML、CSS、JavaScript。この三つは、AI が最も書きやすい言語だ。

理由は、コードの量が少なく、変換層がないからだ。React のコンポーネントを書くには JSX、状態管理、フック、TypeScript の型 ── 全部理解した上で書く必要がある。AI が書いても、その AI 出力をビルドする環境が要る。

生の HTML なら、Claude が出した HTML をそのままブラウザに渡せば動く。確認の往復が早い。**AI と人間のあいだに余計な層がない**。

## 何を捨てるか

新しく Web サイトを作るなら、以下を捨てる。

- **JavaScript フレームワーク**(React、Vue、Angular、Svelte)
- **ビルドツール**(Webpack、Vite、Turbopack、Parcel)
- **TypeScript**(JS で十分)
- **CSS フレームワーク**(Tailwind、Bootstrap)
- **パッケージマネージャ**(npm、yarn、pnpm)
- **node_modules**(`rm -rf node_modules` で消える)

そして残すのは:

- **HTML**(構造)
- **CSS**(見た目)
- **JavaScript**(動的要素のみ、必要最低限)
- **Markdown**(コンテンツソース)
- **Python**(ビルドスクリプト、必要なら)

これで、ビルドが消える。`python build.py` を実行すれば HTML が出てくる、それだけ。Web サーバーに HTML を置けば、サイトが動く。

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

## ビルドは Python スクリプト

このサイトのビルドは、Python スクリプト 1 ファイルで動く(`tools/build_article.py`)。Markdown を読んで、HTML テンプレートに流し込んで、出力する。それだけ。

依存は `Jinja2`、`markdown-it-py`、`Pillow` の 3 つだけ。`pip install -r requirements.txt` でインストール完了。`node_modules` は無い。

このスクリプト自体も、ほとんど Claude が書いた。書く必要はない、書かせればいい。**ビルドツールは自分で持つ**ことができる時代だ。

## デプロイも軽い

静的 HTML のデプロイは、ファイルをコピーするだけだ。

- Cloudflare Pages、GitHub Pages、Netlify、Vercel ── 全部無料か低価格
- 自分のサーバーに置きたければ、`scp` で送るだけ
- CDN に乗せれば、世界中で高速

CI/CD パイプラインも単純になる。「Markdown が変わったら Python ビルドして、HTML を CDN にアップロードする」── 数行のスクリプトで終わる。

## 10年後も動く

React のバージョン v15 で書いたコンポーネントは、v18 ではビルドできないことがある。Webpack の設定は 1 年ごとに書き直しを迫られる。

HTML、CSS、JavaScript の基本仕様は、25 年以上後方互換が保たれている。1999 年の HTML ファイルは、今のブラウザでも問題なく動く。**生の Web 標準は時間に強い**。

> フレームワークは時代に依存する。Web 標準は時代を超える。

## まとめ

Web を作る道具を、原点に戻す。

HTML と CSS と最小限の JavaScript。AI が書きやすい言語で、AI が書きやすい量だけ書く。フレームワークを捨てて、ビルドを消し、依存を消す。

このサイトがその実証だ。30,000 行のコード、42 ページ、24 時間で組み上げた。React は使っていない。それで何の問題もない。

次の章では、アプリを作る話に進む。CLI ツール、Flet アプリ、Flutter アプリ ── 段階的にスケールアップ。

---

## 関連記事

- [第6章: 業務システムと付き合う ── 既存資産を活かしつつAIで補う](/ai-native-ways/business-systems/)
- [第4章: 処理を書く ── AIにPythonで書いてもらう](/ai-native-ways/python/)
- [構造分析15: Mythos時代のセキュリティ設計](/insights/security-design/)
- [構造分析08: 企業ITの税を引く](/insights/enterprise-tax/)
