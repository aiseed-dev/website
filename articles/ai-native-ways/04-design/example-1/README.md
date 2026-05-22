# 実例 1 — Mermaid 5 種類を SVG / PNG に焼く

第 03 章「デザインをする ── Mermaid と Claude デザインで作る」の主張を裏付ける。

## 章のどの主張に対応するか

> Mermaid 図 1 枚の Git 差分: 1 行追加・1 行削除、レビュー 30 秒で済む。
> 同じ変更を PowerPoint でやると、ファイル全体が "binary changed" としか見えない。

> 20 年前の `.ppt` ファイル: フォント置換で図形がずれ、再現困難。
> 同じ時代の Markdown / Mermaid ファイルは、今のレンダラで完全再現。

(章本文「実例: 数字で見る」より)

## やること

業務で書く 5 種類の図を、**全部 Mermaid テキストで定義し、コマンドで SVG/PNG に焼く**。

| ファイル | 種類 | 内容 |
|---------|------|------|
| `system-architecture.mmd` | フローチャート | Web + API + DB + Claude のシステム構成 |
| `sequence-order.mmd` | シーケンス図 | 注文受付の API 呼び出しフロー |
| `er-customer.mmd` | ER 図 | 顧客 / 注文 / 商品 のスキーマ |
| `gantt-launch.mmd` | ガントチャート | 1 人 + AI で SaaS をローンチする 4 ヶ月計画 |
| `state-order.mmd` | 状態遷移図 | 注文状態のライフサイクル |

合計 5 ファイル、ソース合計 **2,488 byte**(2.4 KB)。これを Markdown 記事に
そのまま埋め込めば、GitHub も Notion もネイティブで描画する。コマンドでも
SVG / PNG に変換できる。

## 構成

```
example-1/
├── README.md
├── Makefile
├── puppeteer-config.json   ── headless chromium を root で動かす設定
├── results.md
├── src/                    ── ソース (5 つの .mmd, 計 2.4 KB)
│   ├── system-architecture.mmd
│   ├── sequence-order.mmd
│   ├── er-customer.mmd
│   ├── gantt-launch.mmd
│   └── state-order.mmd
└── out/                    ── 生成物 (SVG ×5, PNG ×5)
```

## 実行

```bash
# 必要なツール
sudo apt install fonts-noto-cjk
npm install -g @mermaid-js/mermaid-cli

make clean && make all
```

## なぜこれが「実例」になるのか

5 種類の業務図(構成、API シーケンス、スキーマ、計画、状態遷移)を、
**合計 2.4 KB のテキスト 5 ファイルで定義**できる。

PowerPoint なら、それぞれ別ファイル、計 数 MB、編集すると差分が見えない、
バージョン管理に乗らない、AI に渡しても XML を解凍することから始まる。

Mermaid なら:

- ソースは Git の通常の diff で見える(1 行追加が 1 行追加に見える)
- Markdown に直接埋められる(GitHub・Notion・VS Code がレンダリング)
- Claude が読める・書ける(`graph TD` の文法で出してくれる)
- コマンドで SVG / PNG / PDF に焼ける(`mmdc -i x.mmd -o x.svg`)
- 10 年後も同じ文法で動く(Mermaid は OSS、Mermaid.js が読める限り)

これが章で言う「**Mermaid はテキストだ。Git の差分が出る、AI が読める、
書き換えられる、10 年後も読める**」の具体形。
