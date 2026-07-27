# 計測結果 — 第 09 章 example-2

実行環境: Linux 6.18 / Python 3.11 / matplotlib 3.x / SQLite 3.45 / Noto Sans CJK JP

## データ投入

```
=== センサーデータ投入 ===
  期間          : 2026-04-25 〜 2026-05-01 (7 日)
  サンプリング  : 5 分間隔 × 3 センサ
  投入件数      : 6,048 件 (DB: 220 KB)
  投入時間      : 約 30 ms
```

| センサ | 件数 |
|--------|------|
| temperature | 2,016 |
| humidity | 2,016 |
| soil_moisture | 2,016 |

## 集計結果(`out/report.md` より)

| センサ | 最小 | 平均 | 最大 |
|--------|------|------|------|
| temperature (°C) | 10.9 | 20.0 | 29.3 |
| humidity (%)     | 38.4 | 69.9 | 100.0 |
| soil_moisture (%) | 21.3 | 30.0 | 39.6 |

## グラフ(`out/sensor.png`)

3 段表示で温度・湿度・土壌水分の 1 週間ぶん:

- **薄い線**: 5 分間隔の生データ(2,016 点)
- **濃い線**: 1 時間平均(SQL の `GROUP BY strftime`)

日内サイクル(温度: 朝低い → 昼高い)が見える。土壌水分はじわっと
低下していて、最終日に灌水が必要。

## SQL クエリの例

```sql
-- 1 時間ごとの温度平均
SELECT strftime('%Y-%m-%d %H:00', ts) AS hour, AVG(value)
FROM measurements
WHERE sensor = 'temperature'
GROUP BY hour
ORDER BY hour;
```

これだけで 2,016 点 → 168 点 に集約。グラフの「重なって読めない」を
解消する。

## 自動観察コメント(`out/report.md` の末尾)

```markdown
## 観察(自動)

- 温度の日内変動が **18.4℃** ── 大きい。換気またはシェード検討。
- 土壌水分が **39.6% → 21.3%** に低下 ── 灌水が必要。
```

これは **エージェントを呼ばずに** 判断ができる典型例。閾値で気づきを
出す。閾値はコードに 3 行。

エージェントに「このデータをどう思う?」と毎回聞くと、

- 1 回約 $0.05(コンテキスト 6,000 行を渡す)
- 365 日で $18

このスクリプトは:

- 1 回 $0(LLM を呼ばない)
- 365 日で $0

**コードに凍結できるものはエージェントに任せない**(章 10 と一致)。

## 来月の運用

cron に登録:

```cron
*/5  * * * *   curl http://esp32.local/sensor | python3 ingest.py  # 実機収集(別途)
0    7 * * 1   cd /home/me/greenhouse && make analyze              # 毎週月曜 7:00 に集計
```

毎週月曜の朝、`out/report.md` と `out/sensor.png` が更新される。それを
LINE に投げれば「気づき通知」も自動。

## 章本文との対応

> 1 週間 → 30 分 (matplotlib + Claude)

このフォルダは:

- データ収集パイプライン: 30 行
- グラフ作成: 50 行
- Markdown レポート: 30 行
- 合計: 約 110 行

実プロジェクトでも、**ここから 50 行追加すれば** Slack 通知 / メール送信 /
HTML ダッシュボードに発展できる。

## 再現手順

```bash
pip install matplotlib
sudo apt install fonts-noto-cjk
make clean && make all
```
