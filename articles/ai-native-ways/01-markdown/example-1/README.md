# 実例 1 — 12 ヶ月分の Word 議事録を Markdown に変える

第 01 章「文書を書く ── Markdownという最小の選択」の主張を裏付ける。

## 章のどの主張に対応するか

> Word の議事録 50 ファイル(計 5 MB)を Markdown にすると、合計 250 KB。**20 分の 1**。
> Git で履歴管理、`grep` で検索、Claude に渡すコストも比例して下がる。

(章本文「実例: 数字で見る」より)

実際にやってみると **18.7 倍**(50 ファイルの代わりに 12 ファイルで実演)。
詳細は [`results.md`](./results.md)。

## やること

1. **入力を作る**: Python の `python-docx` で 12 ヶ月分の議事録 `.docx` を生成
   (出席者・議題・決定事項・宿題を含む、それなりに本格的な構造)
2. **変換する**: `pandoc` で 12 ファイル全部を `.md` に変換
3. **計測する**: 元 docx 合計サイズ vs Markdown 合計サイズ
4. **検索する**: `grep` で「決定事項」「議題」「特定キーワード」を瞬時に抽出

全部 `make all` で動く。

## 構成

```
example-1/
├── README.md             ── このファイル
├── generate_minutes.py   ── サンプル .docx を生成する Python
├── Makefile              ── 入力生成 → 変換 → 計測 → 検索
├── results.md            ── 実測値
├── docx/                 ── 入力 (12 ファイル, 約 440 KB)
│   └── 2026-MM-minutes.docx
├── md/                   ── 変換結果 (12 ファイル, 約 23 KB)
│   └── 2026-MM-minutes.md
└── out/                  ── 検索結果のスナップショット
    ├── decisions.txt     ── 1 年分の決定事項を一意化したリスト
    ├── ai-policy-months.txt
    ├── hiring-months.txt
    └── all-topics.txt    ── 各月の議題タイトル一覧
```

## 実行

```bash
# 必要なツール
sudo apt install pandoc
pip install python-docx

# 入力生成 → 変換 → 計測 → 検索
make clean && make all
```

## なぜこれが「実例」になるのか

Word ファイルは「**書式**を持つ重い箱」だ。同じ内容をテキストにすると 18 倍小さくなる。
そして、テキストになれば:

- `grep` で全ファイルを 0.004 秒で検索できる(`grep デモ 1`)
- 1 年分の決定事項を sort/uniq で重複排除した一覧が秒で出る
- Git で diff、blame、履歴管理ができる
- Claude にまとめて渡しても、Word の半分以下のトークンで済む

Word のままでは、**1 年分の議事録から決定事項を抜き出す**には 12 ファイルを
1 つずつ開いて目で追わないといけない。Markdown にすれば、それは
1 行のシェルコマンドになる:

```bash
grep -h "^\*\*決定:\*\*" md/*.md | sort -u
```

これが、章で言う「**Word から Markdown へ。たった一歩で、書く対象が見栄えから中身に移る**」の具体形。
