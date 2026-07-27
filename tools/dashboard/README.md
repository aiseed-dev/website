# 物理量ダッシュボード — バックエンド・パイプライン

構造分析で追ってきた **物理量** を一覧表示するダッシュボードの取得・計算・
出力パイプライン。仕様は [`docs/physical-dashboard-spec.md`](../../docs/physical-dashboard-spec.md)（v0.1）。

> **ダッシュボードは主張しない。** 物理量・単位・観測日・出所を提示するだけ。
> 予測も結論も載せない。読者が物理的事実から自分で判断する。

- フロントエンド（静的・ビルド工程なし）: [`html/dashboard/`](../../html/dashboard/)
- 出力 JSON（フロントが 1 回 fetch）: `html/dashboard/data/dashboard.json`

設計原則: **物理量主義 / 流れ > 価格 / 小さく・自立し・育つ / 自動取得優先**。
重いフレームワーク・バンドラ・コンテナ・常駐プロセスを使わない。
バックエンドは Python 標準ライブラリのみ（外部依存なし）。

---

## 構成

```
tools/dashboard/
├── models.py            # データモデル（核）— Indicator / Point。新指標 = 1 レコード
├── storage.py           # SQLite 単一ファイルの append-only series ストア
├── derived.py           # derived 計算（スプレッド・比率・残り日数）
├── build.py             # 単一エントリポイント: 取得 → 計算 → 静的 JSON 出力
├── append.py            # manual 指標の 1 件追記 CLI
├── catalog/
│   ├── chokepoints.json # 隘路（chokepoint）のメタデータ
│   └── indicators.json  # 指標カタログ（§3 全指標）。1 指標 1 レコード
└── fetchers/            # 1 指標 1 モジュール。レジストリに足すだけで増える
    ├── __init__.py      #   FETCHERS / GROUP_FETCHERS レジストリ
    ├── base.py          #   Fetcher Protocol・HTTP ヘルパ・safe_fetch
    ├── brent.py         #   ブレント価格（env 駆動）
    ├── urals.py         #   ウラル価格（env 駆動）
    ├── cbr_rate.py      #   ロシア政策金利（CBR 公開 XML）
    ├── bls_cpi.py       #   米国 食料品 CPI（BLS 公開 API）
    ├── crea_monthly.py  #   ロシア石油の流れ（CREA、グループ fetcher）
    └── mosaic.py        #   Mosaic 稼働率（四半期）
```

---

## 実行

```bash
# 全 cadence の fetcher を実行 → 計算 → JSON 出力（cron が叩く想定）
python3 -m tools.dashboard.build

# 日次のみ / 月次のみ
python3 -m tools.dashboard.build --cadence daily
python3 -m tools.dashboard.build --cadence monthly

# fetcher を一切叩かず、カタログ＋計算（カウントダウン等）だけで再生成
python3 -m tools.dashboard.build --offline
```

ネットワークや API キーが無くても落ちない（fetcher 障害は空ポイント扱い）。
その場合でも、カタログ同梱の点・静的定数・カウントダウンから JSON は生成される。

### 更新フロー（仕様 §5）

```
[自動]  cron → 期限の fetcher 実行 → SQLite 追記 → derived 計算 → 静的 JSON 出力
[手動]  観測 → append.py で 1 件追記 → 次回 build で JSON へ反映
```

cron 例（host の crontab 1 行）:

```cron
17 6 * * *  cd /path/to/website && python3 -m tools.dashboard.build >> /var/log/aiseed-dash.log 2>&1
```

### 手入力（manual の残余）

```bash
python3 -m tools.dashboard.append hormuz_transit_status 2026-06-05 制限 "海事筋"
python3 -m tools.dashboard.append naphtha_stock_days_jp 2026-06-05 18 "自前トラッキング"
python3 -m tools.dashboard.build --offline   # 反映
```

値は数値でも状態文字列（開/制限 など）でも可。`series` は追記のみ（同日重複は無視）。

---

## 育てかた

データモデルとフロントは触らず、**データとレジストリだけ**で成長する。

1. **新指標を足す** — `catalog/indicators.json` にレコードを 1 つ追加するだけ
   （`id` / `kind` / `acquisition` / `unit` / `chokepoint` / `source`、必要なら
   `threshold`・`note`・`series`）。フロントは自動でカードを増やす。
2. **manual → auto へ昇格** — 出所が見つかったら `fetchers/` に 1 モジュール書き、
   `fetchers/__init__.py` の `FETCHERS` に 1 行足し、カタログの `acquisition` を
   `manual` から `auto` に変える。
3. **derived を足す** — `derived.py` の `DERIVED` に `id -> 計算関数` を 1 行。
   計算できるものは決して手で入れない。

`brent` / `urals` / `mosaic` のような env 駆動 fetcher は、出所 URL を環境変数で
与えるだけで有効化される（`BRENT_API_URL` 等。詳細は各モジュールの docstring）。

---

## 保存

- SQLite 単一ファイル `tools/dashboard/data/series.sqlite3`（append-only、`.gitignore` 済み）。
- 観測の正本はこの SQLite。`dashboard.json` はそこから毎回再生成される派生物。
- カタログ同梱の `series`（documented/static 点）は毎ビルドで冪等に再追記される。
