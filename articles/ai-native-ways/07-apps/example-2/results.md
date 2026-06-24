# 計測結果 — 第 08 章 example-2

実行環境: Linux 6.18 / Python 3.11 / click 8.x / SQLite 3.45

## 規模と性能

| 項目 | 数値 |
|------|------|
| `journal.py` 行数 | **約 100 行**(コメント込み) |
| 依存パッケージ | **click のみ**(SQLite は標準ライブラリ) |
| サブコマンド数 | **5 個** + `--help` |
| 1 サブコマンドの実行時間 | **数 ms**(Python 起動 + SQLite クエリ) |
| 起動オーバーヘッド | 約 50 ms(Python インタプリタ) |

## デモシナリオ(`make all` の出力)

### 1. メモを 8 件投入

```
$ journal add "山田農園と打ち合わせ。来月から週次納品" --tag meeting
  added #1: 山田農園と打ち合わせ。来月から週次納品
$ journal add "経費レポートを Claude に作らせた、20 分で完了" --tag review
  added #2: 経費レポートを Claude に作らせた、20 分で完了
...(計 8 件)
```

### 2. 一覧(最新 5 件)

```
$ journal list --limit 5
    8  2026-05-05 06:11  経理: 4 月分の領収書を Claude に分類させた、3 分
    7  2026-05-05 06:11  Mochi.ai の LP に「365 日返金保証」を追記
    6  2026-05-05 06:11  [todo] 山田農園に来週納品手配のメールを送る
    5  2026-05-05 06:11  今月の MRR が目標に到達
    4  2026-05-05 06:11  [ops] サーバ再起動 04:00 完了、ダウンタイム 12 秒
```

### 3. タグ絞り込み

```
$ journal list --tag meeting
    1  2026-05-05 06:11  [meeting] 山田農園と打ち合わせ。来月から週次納品
```

### 4. 全文検索

```
$ journal search 山田
  '山田' に一致: 2 件
      6  2026-05-05  山田農園に来週納品手配のメールを送る
      1  2026-05-05  山田農園と打ち合わせ。来月から週次納品
```

### 5. タグ別集計(JSON, `out/stats.json`)

```json
{
  "total": 8,
  "by_tag": [
    {"tag": "(no-tag)", "n": 3},
    {"tag": "todo",     "n": 1},
    {"tag": "review",   "n": 1},
    {"tag": "ops",      "n": 1},
    {"tag": "meeting",  "n": 1},
    {"tag": "lead",     "n": 1}
  ]
}
```

JSON で出すので、cron で集計 → Slack に投げる、なども容易。

### 6. Markdown エクスポート(`out/journal.md`)

```markdown
# 業務日報

件数: 8

## 2026-05-05

- 06:11  `meeting` 山田農園と打ち合わせ。来月から週次納品
- 06:11  `review` 経費レポートを Claude に作らせた、20 分で完了
- 06:11  `lead` 新規顧客 C016 が問い合わせ、料金で要確認
- 06:11  `ops` サーバ再起動 04:00 完了、ダウンタイム 12 秒
...
```

そのまま月次報告に貼り付けられる Markdown が出る。

### 7. 自動生成のヘルプ

```
$ journal --help
Usage: journal.py [OPTIONS] COMMAND [ARGS]...

  一行メモから月次報告まで、ひとつの CLI で。

Commands:
  add     メモを追加。
  export  Markdown 形式でエクスポート(月次報告用)。
  list    最新のメモを一覧。
  search  全文検索(LIKE)。
  stats   件数・タグ別集計を JSON で。
```

`@click.command()` のデコレータと docstring から **自動生成**。
`--help` を書く必要がない。

## CLI vs SaaS(章本文との対応)

| 項目 | Notion / Evernote | この CLI |
|------|------------------|---------|
| 月額 | $10〜 | **0 円** |
| データの所有権 | サービス側 | **自分** |
| 検索 | 数 ms(クラウド) | **数 ms(SQLite)** |
| エクスポート | 限定的 | **Markdown 完全** |
| AI 連携 | 限定的 | **journal.py を Claude に渡せる** |
| サービス終了で消える? | 消える | **消えない** |

## 来月の運用

cron に登録:

```cron
0 9 * * 1   journal export --since "$(date -d 'last week' +%Y-%m-%d)" --out /tmp/weekly.md
```

毎週月曜 9:00 に「先週の業務日報」が `/tmp/weekly.md` に出る。それを
Claude に「これを月次報告用に要約して」と渡せば、月次報告も自動。

## 再現手順

```bash
pip install click
make clean && make all
```

実行は数秒で完了。
