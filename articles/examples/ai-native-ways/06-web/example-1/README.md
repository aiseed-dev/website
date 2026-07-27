# 実例 1 — Markdown 3 枚 + Python 100 行で 3 ページの Web サイト

第 07 章「Webを作る ── HTML+CSS+JavaScriptという原点回帰」の主張を裏付ける。

## 章のどの主張に対応するか

> React + Next.js + TypeScript + Tailwind で業務 Web 構築:
> 開発 **3 ヶ月**、依存 **約 1,200 個**、`node_modules` **500 MB**。
> 同じ機能を HTML+CSS+FastAPI+Markdown で構築:
> 開発 **2 週間**、依存 **4 個**、合計 **10 MB**。

(章本文「実例: 数字で見る」より)

## やること

ある農園が「自分の Web サイトが欲しい」── これを最小スタックで作る。

1. **入力**: `src/index.md` `src/news.md` `src/shipping.md`(計 3 枚)
2. **ビルド**: `python3 build.py` ── 100 行の Python
3. **出力**: `out/*.html`(3 ページ)+ Mermaid 図 2 つを CDN で描画
4. **デプロイ**: `out/` を Cloudflare Pages や GitHub Pages に置くだけ

ビルド時間 **約 3 ms**、HTML 合計 **約 7 KB**、依存パッケージ **1 個**。

## 構成

```
example-1/
├── README.md
├── build.py            ── Markdown → HTML(100 行、依存は markdown-it-py のみ)
├── Makefile
├── results.md
├── src/                ── ソース(全部 Markdown)
│   ├── index.md        ── トップページ + Mermaid 配送フロー
│   ├── news.md         ── お知らせ
│   └── shipping.md     ── 配送解説 + Mermaid 図
└── out/                ── ビルド結果(これが Web サイト)
    ├── index.html
    ├── news.html
    └── shipping.html
```

## 実行

```bash
pip install markdown-it-py
make clean && make all

# ローカルで確認
make serve   # → http://localhost:8765
```

## なぜこれが「実例」になるのか

業務用の小さな Web サイトを作るのに **React も Next.js も Tailwind も
node_modules も要らない**。

- Markdown で書く(章 01 と同じ)
- Mermaid で図を入れる(章 03 と同じ)
- Python が HTML に焼く(章 04 と同じ)
- HTML/CSS/CDN で表示する(古典的な Web)

これだけで、

- ページの追加 = `src/foo.md` を 1 枚足して `make`
- 内容の変更 = Markdown を直して `make`
- デザイン変更 = `build.py` の CSS を直して `make`
- バージョン管理 = Git で diff が出る
- AI が編集に並走できる(全部テキストだから)
- 10 年後も読める(HTML は 30 年動いている)

業務系の Web に必要なものは、ほとんどここにある。フォーム送信や認証が
必要なら、第 7 章で言う「FastAPI を最小限」で足す。

このサイト(aiseed.dev)も同じ考え方で、150 ページ以上を Markdown +
Python ビルドで作っている。**React・Next.js・TypeScript はゼロ**。
