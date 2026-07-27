# 計測結果 — 第 07 章 example-1

実行環境: Linux 6.18 / markdown-it-py / Python 3.x

## ビルド規模

| 項目 | 数値 |
|------|------|
| Markdown ソース | **71 行 / 約 1.8 KB**(3 ファイル) |
| `build.py`(ビルドスクリプト全部) | **109 行 / 約 4 KB** |
| pip 依存パッケージ | **1 個**(`markdown-it-py`) |
| `node_modules/` | **0 KB**(無し) |
| ビルド時間 | **2.6 ms** |
| 出力 HTML 合計 | **7,103 B (6.9 KB)** ── 3 ページ |
| ランタイム JS | **CDN の Mermaid 1 個だけ** |

## 比較(章本文の数字)

| 項目 | React + Next.js | このスタック |
|------|----------------|-------------|
| 開発期間 | 3 ヶ月 | この規模なら **数時間** |
| 依存パッケージ | 約 1,200 | **1** |
| `node_modules` | 約 500 MB | **0 MB** |
| ビルド時間 | 約 3 分 | **2.6 ms**(70,000 倍速い) |
| 配信ファイル合計 | 数 MB | **6.9 KB** |
| ホスティング月額 | Vercel Pro $20+ | Cloudflare Pages **$0** |

## 出力(`out/index.html` 抜粋)

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>山田農園 — 山田農園</title>
<style>:root { --ink: #1a1a1a; --paper: #f4f1ea; ... }</style>
</head>
<body>
<h1>山田農園</h1>
<p>徳島市で 3 代続く小さな農園です。...</p>
<table>...商品テーブル...</table>
<div class="mermaid">flowchart LR ...</div>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/...";
  mermaid.initialize({ startOnLoad: true });
</script>
</body>
</html>
```

完全に静的。CDN の Mermaid を 1 行 import するだけで図がレンダリングされる。
**JavaScript フレームワークは無い。バンドラも無い**。

## デプロイ(参考)

```bash
# Cloudflare Pages
wrangler pages deploy out/

# GitHub Pages
cp -r out/* ~/your-repo/docs/ && git push

# 自前サーバ
rsync -av out/ user@host:/var/www/
```

CDN の月額: Cloudflare Pages **無料枠で十分**(月 100,000 リクエストまで)。
WordPress マネージドホスティング(月 5,000〜30,000 円)と比較して
**年 6〜36 万円の節約**。

## ページの追加

```bash
$EDITOR src/contact.md   # 新しいページを書く
make                     # 2.6 ms で再ビルド
```

WordPress なら管理画面に入って投稿フォームに貼り付け、メディアをアップロード、
プラグイン設定を確認 ── そして 6 ヶ月後にプラグインを更新しないと
脆弱性で侵入される。**保守ゼロ**との差はそこ。

## 再現手順

```bash
pip install markdown-it-py
make clean && make all
```
