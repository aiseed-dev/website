# 計測結果 — 第 03 章 example-1

実行環境: Linux 6.18 / @mermaid-js/mermaid-cli 11.14 / Node 22

## ソース vs 出力サイズ

| 図 | `.mmd` ソース | `.svg` | `.png` (1600px) |
|---|--------------|-------|----------------|
| `system-architecture` | 543 B | 22,158 B | 36,112 B |
| `sequence-order` | 467 B | 29,404 B | 47,617 B |
| `er-customer` | 509 B | 70,730 B | 39,516 B |
| `gantt-launch` | 603 B | 13,061 B | 28,985 B |
| `state-order` | 366 B | 37,448 B | 31,983 B |
| **合計** | **2,488 B (2.4 KB)** | 172,801 B (169 KB) | 184,213 B (180 KB) |

ソースは 1 ファイルあたり 366〜603 byte の極小テキスト。

## Git diff の比較(章本文の主張の検証)

例えば `sequence-order.mmd` に「キャッシュチェック」のステップを 1 行入れる
と、`git diff` はこう見える:

```diff
   API->>DB: INSERT orders
+  API->>Cache: 重複チェック
   API->>Claude: 「住所を整形して」
```

**1 行追加が 1 行追加に見える**。レビュアーは「キャッシュチェックを
DB の後に入れたんだな」と 5 秒で理解できる。

同じ修正を PowerPoint でやれば、`git diff` は:

```
Binary files a/sequence.pptx and b/sequence.pptx differ
```

何が変わったかわからない。レビューが成り立たない。

## Claude に書いてもらう例

```
あなた: 注文確定 API のシーケンス図を書いて。
        顧客 → Web → FastAPI → DB → Claude(住所正規化)
Claude: (sequence-order.mmd 相当のテキストが返る)

あなた: そこに、決済 API への呼び出しを追加して
Claude: (1 行差分)
```

**人間は「描いて」いない**。意図を伝えただけ。Claude が文法を当てて、
mmdc が画像に焼く。

## 描画コマンド

```bash
mmdc -i src/sequence-order.mmd -o out/sequence-order.svg \
     -b transparent -t neutral
```

各図 1 〜 2 秒で SVG / PNG 完成。CI で自動レンダリングして PR コメントに
付けることも容易。

## 10 年後の互換性

Mermaid 11.x の文法は、`graph TD` `sequenceDiagram` `erDiagram`
`gantt` `stateDiagram-v2` ── どれもプレーンテキストの DSL。

Mermaid.js が GitHub に存在し続けるかぎり、これらは同じレンダリング結果を
返す。仮に Mermaid 自体が消えても、ソースを Claude に渡して別の DSL に
変換してもらえる。**ソースが構造として残っている**から。

PowerPoint の `.ppt` 形式は仕様変更のたびに過去ファイルが壊れる。Mermaid
のソースは壊れない(壊れるとしたらレンダラだけで、書き直せる)。

## 再現手順

```bash
sudo apt install fonts-noto-cjk
npm install -g @mermaid-js/mermaid-cli
make clean && make all
```
