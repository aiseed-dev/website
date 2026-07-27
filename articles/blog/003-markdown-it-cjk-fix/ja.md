---
slug: markdown-it-cjk-fix
title: markdown-itの太字が**のまま残るバグをClaudeが修正してPull Requestまでした
subtitle: SIerに委託に出す必要は全くなくなりました
description: markdown-it-pyで日本語混在テキストの太字が壊れるバグを発見。Claude Codeが原因を特定し、6行の修正を書き、フォークを作り、PRを提出するまでを1セッションで完了した。
date: 2026.04.08
label: Blog
category: AI開発ノート
---

## 何が起きたか

ブログ記事を書いていて、おかしな表示に気づいた。

```
ホルムズ海峡は世界の海上石油輸送の**20〜25%**が通過する。
```

これが太字にならず、`**` がそのまま表示される。

```
ホルムズ海峡は世界の海上石油輸送の**20〜25%**が通過する。
```

スペースを入れれば動く。しかし日本語の文中にスペースを入れるのは不自然だ。

```
ホルムズ海峡は世界の海上石油輸送の **20〜25%** が通過する。
```

これはバグだ。

## 原因

[markdown-it-py](https://github.com/executablebooks/markdown-it-py) の `scanDelims` 関数が原因だった。

CommonMarkの仕様では、`**` が太字の閉じとして機能するには **right-flanking delimiter** である必要がある。判定ロジンクはこうだ：

`right_flanking = not (isLastPunctChar and not (isNextWhiteSpace or isNextPunctChar))`

`**46%**を` の閉じ `**` で：
- `lastChar='%'` → 句読点 → `isLastPunctChar=True`
- `nextChar='を'` → CJK文字 → スペースでも句読点でもない

結果：`right_flanking = False`。閉じデリミタとして認識されない。

**つまり、CJK文字がASCII句読点の後に来ると、太字が壊れる。** これは日本語・中国語・韓国語すべてに影響する。

## 修正

`state_inline.py` の `scanDelims` に6行を追加した。CJK文字（U+2E80以上）を句読点として扱うことで、ワード境界として正しく認識させる。

```python
# Treat CJK ideographs as punctuation for flanking delimiter checks
if not isNextPunctChar and ord(nextChar) > 0x2E7F:
    isNextPunctChar = True
if not isLastPunctChar and ord(lastChar) > 0x2E7F:
    isLastPunctChar = True
```

テスト結果：

| 入力 | 修正前 | 修正後 |
|------|--------|--------|
| `湾岸の**46%**を供給` | **のまま残る | **46%** が太字 |
| `の**20〜25%**が通過する` | **のまま残る | **20〜25%** が太字 |
| `日本語の**太字**テスト` | 正常 | 正常 |
| `English **bold** test` | 正常 | 正常 |

英語のみのテキストへの影響はない。

## Claude Codeがやったこと

バグの発見から修正、PRの提出まで、私の方でコードを見ることも読むこともなかった。

1. **バグの発見** — ブログ記事のビルド結果をみて、Claudeに指示
2. **原因の特定** — `markdown-it-py` のソースを読み、`scanDelims` の flanking delimiter 判定ロジックを分析
3. **修正の実装の指示** — Claideは、バッチを作成するといったが、パッケージの修正を指示。Claideが、CJK文字を句読点として扱う6行の修正を作成
4. **テスト** — 日本語・英語の両方で8パターンのテストを実施
5. **フォークの作成** — `aiseed-dev/markdown-it-py` にフォークし、`fix/cjk-emphasis` ブランチにコミット
6. **PRの提出** — [executablebooks/markdown-it-py#387](https://github.com/executablebooks/markdown-it-py/pull/387) にPull Requestを作成
7. **自プロジェクトの更新** — `requirements.txt` をフォーク版に切り替え、全ページをリビルド

## SIerに委託する必要はない

従来なら、この種の作業は：
- バグの報告と調査の委託
- 外部ライブラリの調査と修正方針の検討
- フォークの管理とPRの作成
- テストの作成と実行

これらを外部に委託すれば、数日から数週間、それにコストがかかる。

ブログ記事を書いている最中にバグを見つけて、Claude Codeに指示をしたら、SIerに委託するのと同じことをしてくれました。

:::highlight
**SIerに委託に出す必要は、全くなくなりました。**

必要なのは、問題を正確に伝える力と、結果を判断する力だけだ。コードを読み書きする能力は、もう人間側に必要ない。
:::

## Links

- [Pull Request: Fix CJK emphasis delimiter detection](https://github.com/executablebooks/markdown-it-py/pull/387)
- [aiseed-dev/markdown-it-py (fork)](https://github.com/aiseed-dev/markdown-it-py/tree/fix/cjk-emphasis)
