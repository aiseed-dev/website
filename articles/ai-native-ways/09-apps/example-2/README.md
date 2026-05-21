# 実例 2 — `click` で業務メモ CLI(add/list/search/stats/export)

第 08 章「アプリを作る ── CLI ツール、Flet、Flutter」の **2 番目の角度**:
**サブコマンド構造を持った業務 CLI**。

## 章のどの主張に対応するか

> CLI ツールの作成と配布: 1 時間で書いて、`pip install` で世界中の Python
> ユーザーに即配布。

> CLI で動く処理を Flet で GUI 化する追加コスト: Flet ライブラリのインストール
> と数十行の追加コード、**1 時間**。Flutter で書き直すなら 1 ヶ月。

(章本文「実例: 数字で見る」より)

example-1 が「写真整理 CLI」(単一コマンド)、これは **5 つのサブコマンド**
を持つ業務 CLI を click で書く。CLI を「アプリ」として育てる入口。

## やること

`journal.py` 1 ファイル / 約 100 行で:

```bash
journal add     "テキスト" --tag meeting     # メモ追加
journal list    [--limit N] [--tag タグ]     # 一覧
journal search  "キーワード"                  # 全文検索(LIKE)
journal stats                                 # タグ別集計(JSON)
journal export  --out out/journal.md          # Markdown エクスポート
journal --help                                # 自動生成のヘルプ
```

ストレージは **SQLite 1 ファイル**(`out/journal.db`)。
`make all` でデモ実行(8 件投入 → 一覧・検索・集計・エクスポート)。

## 構成

```
example-2/
├── README.md
├── journal.py    ── click ベースの CLI(約 100 行)
├── Makefile      ── デモシナリオ
├── results.md
└── out/
    ├── journal.db   ── SQLite データ
    ├── stats.json   ── stats サブコマンドの出力
    └── journal.md   ── export サブコマンドの出力
```

## 実行

```bash
pip install click
make clean && make all
```

各サブコマンドのヘルプは `make help`。

## なぜこれが「実例」になるのか

業務メモ・日報の世界には 3 つの選択肢がある:

| 選択肢 | コスト | 自由度 |
|--------|-------|-------|
| Notion / Evernote | 月 $10〜 | サービス依存・退会で消える |
| Word + フォルダ | フォントずれ・検索しづらい | × |
| **CLI + Markdown** | **0 円** | **○ 全部自分のもの** |

このフォルダの CLI なら:

- メモは **SQLite**(1 ファイル、Git で履歴管理可)
- エクスポートは **Markdown**(章 01 の世界に直結)
- 全文検索は **SQL の LIKE**(数 ms)
- ヘルプは **自動生成**(click)
- スクリプトに組み込める(`for line in $(...); do journal add "$line"; done`)

そしてこのまま:

- **cron で毎時 stats を JSON 出力**(自動レポート)
- **メールから add に流す**(IMAP で受信 → CLI 呼び出し)
- **Flet で GUI 化**(章本文の言う「1 時間で GUI」、CLI ロジックを再利用)
- **PyPI で配布**(`pip install <your-journal>`)

これが章で言う「**まず CLI、必要なら GUI に上げる**」の具体形。

## 「Flet にする」の意味

このフォルダは Flet を使っていないが、Flet にする手順は:

```python
import flet as ft
from journal import conn  # 既存ロジックを再利用

def main(page: ft.Page):
    text = ft.TextField(label="メモ")
    def add_cb(e):
        with conn() as c:
            c.execute("INSERT INTO notes (text) VALUES (?)", (text.value,))
        text.value = ""
        page.update()
    page.add(text, ft.ElevatedButton("追加", on_click=add_cb))

ft.app(target=main)
```

**追加 30 行で GUI 完成**。CLI のロジック(SQLite アクセス・スキーマ)は
完全に再利用される。**書き直しは発生しない**。

これが章の「**CLI を一段ずつ昇格させる**」の意味。

## 配布

```bash
# 1. PyPI に上げる(pyproject.toml を 1 つ書くだけ)
pip install build twine
python3 -m build
twine upload dist/*

# 2. ユーザは
pip install your-journal
journal add "first note"
```

App Store の審査も Apple Developer Program も要らない。**世界中の Python
ユーザーに即配布**。
