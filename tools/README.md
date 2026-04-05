# build_article.py

Markdown ファイルから HTML を生成するビルドツール。

## 使い方

```bash
# 単一記事をビルド
python3 tools/build_article.py articles/13-cases.md

# 全記事＋インデックスページをビルド
python3 tools/build_article.py --all

# 記事一覧を表示
python3 tools/build_article.py --list
```

## 依存ライブラリ

```bash
pip install -r requirements.txt
```

- [Jinja2](https://jinja.palletsprojects.com/) — テンプレートエンジン（`{{ variable }}` 構文）
- [markdown-it-py](https://markdown-it-py.readthedocs.io/) — CommonMark 準拠の Markdown パーサー

markdown-it-py は `table` 拡張を有効化済み。

## ファイル構成

```
articles/
  01-climate-mistake.md      # 日本語記事
  en-01-climate-mistake.md   # 英語記事（en- プレフィックス）
  ...
tools/
  build_article.py           # ビルドロジック
  templates/
    article.html             # 記事ページテンプレート（Jinja2）
    index.html               # インデックスページテンプレート（Jinja2）
html/
  insights/                  # 日本語 HTML 出力先
  en/insights/               # 英語 HTML 出力先
```

## 出力先

| 記事 | 出力先 |
|------|--------|
| `articles/09-healthcare-fiscal.md` | `html/insights/healthcare-fiscal/index.html` |
| `articles/en-09-healthcare-fiscal.md` | `html/en/insights/healthcare-fiscal/index.html` |

slug がディレクトリ名になる。

---

# Markdown 記法マニュアル

## フロントマター

ファイル先頭に `---` で囲んで記述する。**全てのフィールドは1行で書く**（YAML のネスト・配列は非対応）。

```yaml
---
slug: healthcare-fiscal
number: "09"
title: 社会の設計ミス
subtitle: 軍需産業、IT企業、デスクワーカー、医療、年金
description: 透析医療の化石資源依存、社会保険料30%超...
date: 2025.04.04
label: Structural Analysis 09
prev_slug: enterprise-tax
prev_title: 企業ITの税を引く
next_slug: subtraction-design
next_title: 引き算の設計
---
```

### 英語記事の追加フィールド

```yaml
lang: en
```

これがあると `/en/insights/` 以下に出力される。

### CTA カスタマイズ（省略可）

省略すると日英それぞれのデフォルト値が使われる。

```yaml
cta_label: Back to Soil
cta_title: 自然とともにあれば、生きられる
cta_text: 全ての構造分析は、一つの結論に向かう。
cta_btn1_text: 自然農法とは
cta_btn1_link: /about/
cta_btn2_text: Light Farming
cta_btn2_link: /light-farming/
```

## 標準 Markdown

Python-Markdown の仕様に従う。GitHub Flavored Markdown (GFM) とは一部異なる。

### 見出し

```markdown
## 大見出し
### 中見出し
```

### 太字・強調

```markdown
**太字** → <strong>太字</strong>
*斜体* → <em>斜体</em>
```

### リンク

```markdown
[テキスト](https://example.com)
```

### リスト

```markdown
- 項目1
- 項目2
- 項目3
```

番号付き:

```markdown
1. 最初
2. 次
3. 最後
```

### 段落

空行で段落を分ける。空行がないと同じ段落になる。

```markdown
最初の段落。

次の段落。
```

### テーブル（tables 拡張）

カスタムブロック外でもテーブルが使える。

```markdown
| 見出し1 | 見出し2 |
| ------- | ------- |
| セル1   | セル2   |
```

### 属性リスト（attr_list 拡張）

要素にクラスやIDを追加できる。

```markdown
段落テキスト
{: .my-class #my-id }
```

## 注意: Python-Markdown と GFM の違い

| 記法 | GFM | Python-Markdown |
|------|-----|-----------------|
| `~~取り消し線~~` | 対応 | **非対応** |
| 自動リンク `https://...` | 対応 | **非対応**（`[text](url)` で書く） |
| タスクリスト `- [ ]` | 対応 | **非対応** |
| コードブロック ` ``` ` | 対応 | 対応（ただしシンタックスハイライトなし） |

## カスタムブロック（独自拡張）

`:::type` で開始し `:::` で終了する。**Python-Markdown の機能ではなく、build_article.py 独自の前処理**。

### :::chain — 構造チェーン

因果関係や構造的な連鎖を表示する。`→` が矢印アイコンに変換される。

```markdown
:::chain
**タイトル：**
原因 → 結果1
→ 結果2
→ **最終結論**
:::
```

出力: 左ボーダー付きボックス。`→` は緑色の矢印になる。
内部では `**太字**` と改行のみ対応。標準 Markdown は処理されない。

### :::highlight — ハイライトボックス

重要な数字や事実を強調する。内部は標準 Markdown として処理される。

```markdown
:::highlight
**タイトル：**
項目1：数値
項目2：数値
**結論文**
:::
```

出力: 薄緑の背景ボックス。内部は `markdown.markdown()` で処理されるので、太字・リスト・リンク等が使える。

### :::quote — 引用ブロック

印象的な一文やまとめに使う。

```markdown
:::quote
自然は、壊されても回復する力を持っている。
人間も同じだ。
:::
```

出力: 左ボーダー付き、明朝体で表示。改行は `<br>` に変換される。
**太字等の Markdown は処理されない**（プレーンテキストのみ）。

### :::compare — 比較テーブル

パイプ記法のテーブルを比較用スタイルで表示する。

```markdown
:::compare
| 項目 | 従来 | 転換後 |
| --- | --- | --- |
| 土壌 | 化学肥料 | 微生物 |
| 水 | 地下水採掘 | 雨水循環 |
:::
```

出力: スタイル付きテーブル。1行目がヘッダー、`---` 行はスキップされる。

## カスタムブロック内の記法まとめ

| ブロック | `**太字**` | `→` 矢印 | Markdown 処理 | 改行 |
|----------|-----------|----------|--------------|------|
| :::chain | 対応 | 対応（緑矢印） | なし | `<br>` |
| :::highlight | 対応 | なし | **あり**（完全） | Markdown 準拠 |
| :::quote | なし | なし | なし | `<br>` |
| :::compare | なし | なし | なし | テーブル行 |

## 新しい記事を追加する手順

1. `articles/` に Markdown ファイルを作成

```bash
# 日本語
articles/14-new-topic.md

# 英語
articles/en-14-new-topic.md
```

2. フロントマターを書く（slug, number, title, subtitle, description, date, label, prev_slug, prev_title, next_slug, next_title）

3. 前の章の `next_slug` / `next_title` を更新する

4. `tools/html_to_md.py` の `ARTICLE_ORDER` にエントリを追加する

5. ビルド

```bash
python3 tools/build_article.py --all
```
