# aiseed.dev 物理量ダッシュボード 仕様書 v0.1

## 0. 目的

構造分析で追ってきた「物理量」を一覧表示し、読者が政治的言説ではなく物理的事実から自分で判断できる場を作る。

**ダッシュボードは主張しない。** 物理量・単位・観測日・出所を提示するだけ。予測も結論も載せない（編集方針 §6）。

---

## 1. 設計原則

- **物理量主義** — 価格・流量・在庫・残高など、ゼロに向かう／積み上がる物理量のみを扱う。
- **流れ > 価格** — 各指標を「価格（世界需給が決める下流の読み取り値）」と「流れ（量・経路・割引。制御が実際に行使される層）」に分類し、視覚的に区別する。
- **小さく・自立し・育つ** — 重いフレームワーク・バンドラ・コンテナを使わない。指標はデータ追加だけで増える（コード変更不要）。
- **自動取得優先** — 自動で取得できるものは、できるだけ Python でコード化する。手入力は、プログラム的な出所が無い指標の残余に限り、出所が現れ次第 fetcher に昇格させる。

---

## 2. データモデル（核）

全指標を単一の構造で表す。これが「育つ」の根拠 — **新指標 = 1レコード追加**。

```json
{
  "id": "urals_brent_spread",
  "name_ja": "ウラル–ブレント割引",
  "name_en": "Urals-Brent discount",
  "chokepoint": "russia_oil_flow",
  "kind": "flow",
  "acquisition": "derived",
  "cadence": "daily",
  "unit": "USD/bbl",
  "series": [
    { "date": "2026-02-28", "value": 12.6, "source": "CREA" }
  ],
  "threshold": null,
  "note": "流れの実現率（1-割引）。価格上昇を相殺する側。"
}
```

`threshold` の例（ゼロ／期限に向かう指標）:

```json
"threshold": { "value": 0, "label": "NWF枯渇", "direction": "down" }
```

### kind（指標の種別）

| kind | 意味 | UI上の扱い |
|------|------|-----------|
| `price` | 価格。世界需給が決める。下流の読み取り値 | スコアボード色 |
| `flow` | 流れ。量・経路・割引。制御が行使される層 | 実体色（強調） |
| `clock` | 時計。ゼロや期限に向かうカウントダウン | ゲージ／残り日数 |
| `stock` | 在庫。在庫日数など | ゲージ |
| `constant` | 構造定数。依存率などほぼ動かない事実 | 固定表示 |

### acquisition（取得方法）

| acquisition | 意味 | 人手 |
|------|------|------|
| `auto` | Python fetcher が API/スクレイプで取得 | なし |
| `derived` | 他指標から計算（スプレッド・比率・残り日数） | なし |
| `manual` | プログラム的な出所が無く人手入力（Gemini検証） | あり |

**方針: 既定は `auto` か `derived`。`manual` は残余であり、出所が見つかり次第 `auto` に昇格させる。**

---

## 3. 指標カタログ（隘路ごと）

各指標: 名称 / kind / 取得 / 単位 / 主な出所。値は観測のたびに `series` へ追記。

### 3.1 ホルムズ / 原油 (`hormuz_crude`)

| 名称 | kind | 取得 | 単位 | 出所 |
|------|------|------|------|------|
| ブレント価格 | price | auto | USD/bbl | ICE / 商品価格API |
| ウラル価格 | price | auto | USD/bbl | oilpriceapi / CREA |
| ウラル–ブレント割引 | flow | derived | USD/bbl | （計算） |
| ホルムズ通航状況 | flow | manual | 状態(開/制限) | 海事筋 |
| ホルムズ通過比率（世界海上原油） | constant | manual(static) | % (~20–25) | 一般統計 |

### 3.2 ロシア石油の流れ (`russia_oil_flow`)

| 名称 | kind | 取得 | 単位 | 出所 |
|------|------|------|------|------|
| 海上原油輸出量 | flow | auto(月次) | 前月比% / mb/d | CREA |
| 制裁影の船団比率 | flow | auto(月次) | % | CREA |
| 偽旗船隻数 | flow | auto(月次) | 隻 | CREA |
| 製品のG7+依存率 | flow | auto(月次) | % | CREA |

### 3.3 ロシア財政（時計）(`russia_fiscal`)

| 名称 | kind | 取得 | 単位 | 出所 |
|------|------|------|------|------|
| NWF流動資産残高 | clock | auto(月次) | 兆ルーブル（→0） | 財務省 / Meduza |
| 財政赤字（累計） | clock | auto(月次) | 兆ルーブル | 財務省 / FT |
| 軍事支出 vs 石油ガス収入 | constant | derived | 比 | （計算） |
| 政策金利 | price | auto | % | CBR |

### 3.4 副産物 (`byproduct_trap`)

| 名称 | kind | 取得 | 単位 | 出所 |
|------|------|------|------|------|
| 硫黄スポット価格 | price | manual | 指数 / USD | SunSirs / World Bank |
| ナフサ在庫日数（日本） | stock | manual | 日 | 自前トラッキング |

### 3.5 リン酸肥料（春作の時計）(`phosphate`)

| 名称 | kind | 取得 | 単位 | 出所 |
|------|------|------|------|------|
| DAP価格（Gulf / インド入札） | price | auto | USD/t | AFBF / SunSirs |
| 中国リン酸輸出停止状況 | flow | manual | 状態 | NDRC |
| 日本リン安在庫日数 | stock | manual | 日 | 自前トラッキング |
| Mosaic稼働率 | flow | auto(四半期) | % | Mosaic IR |

### 3.6 米国食料（批判の時計）(`us_food`)

| 名称 | kind | 取得 | 単位 | 出所 |
|------|------|------|------|------|
| DAP対トウモロコシ価格比 | constant | derived | 比 | （計算） |
| 食料品CPI | price | auto | % | BLS API |
| メキシコ野菜輸入比率 | constant | manual(static) | % (~77) | USDA ERS |

### 3.7 キューバ (`cuba`)

| 名称 | kind | 取得 | 単位 | 出所 |
|------|------|------|------|------|
| 燃料タンカー到着 | flow | manual | 隻 / バレル | AP / Reuters |
| 送電網状況 | price | manual | 状態 | キューバ当局 / 報道 |
| 燃料自給率 | constant | manual(static) | % (~40) | 報道 |

### 3.8 政治の時計 (`political_clock`)

| 名称 | kind | 取得 | 単位 | 期日 |
|------|------|------|------|------|
| 中国リン酸輸出停止 期限 | clock | derived | 残り日数 | 2026-08 |
| 米中間選挙 | clock | derived | 残り日数 | 2026-11-03 |

---

## 4. アーキテクチャ

### バックエンド (Python) — 自動取得優先

cron が起動する単一エントリポイントが、取得→計算→出力を一巡する。常駐プロセスなし。

```
1. 期限の来た fetcher を cadence 別に実行 → 生ポイントを SQLite に追記
2. derived 指標を計算（スプレッド・比率・残り日数）→ 追記
3. 静的 JSON を出力 → /var/www/aiseed/data/*.json
```

fetcher は 1指標1モジュール、共通インターフェース。レジストリに足すだけで増える:

```python
class Fetcher(Protocol):
    indicator_id: str
    cadence: str                 # daily | monthly | quarterly | event
    def fetch(self) -> list[Point]: ...   # [(date, value, source)]

FETCHERS = [BrentFetcher(), UralsFetcher(), CbrRateFetcher(),
            BlsCpiFetcher(), CreaMonthlyFetcher(), MosaicFetcher()]
```

derived は fetch 後に一括計算（手入力ゼロ — 計算できるものは決して手で入れない）:

```python
DERIVED = {
    "urals_brent_spread": lambda d: d["brent"] - d["urals"],
    "dap_corn_ratio":     lambda d: d["dap"] / d["corn"],
    "midterm_countdown":  lambda _: days_until("2026-11-03"),
    "china_ban_countdown":lambda _: days_until("2026-08-31"),
}
```

manual は残余のみ。小さな append CLI、または Gemini検証テキストを置く監視ファイル(inbox)から取り込む:

```
python append.py <indicator_id> <date> <value> <source>
```

- **保存**: SQLite 単一ファイル。`series` は追記のみ。重いDB不要。
- **スケジューラ**: host の crontab 1行のみ（Airflow 等は不要）。
- **コード**: 人間は Python のみ。性能や配布が要れば該当部のみ Cython / Rust を生成。この規模は Python で足りる。

### フロントエンド (素の HTML / CSS / JavaScript) — ビルド工程なし

- 単一 `index.html`。読み込み時に静的JSONを1回 fetch → 描画。フレームワーク・バンドラ・状態管理なし。
- ネイティブ ES Modules で部品を分割（ビルド不要、`<script type="module">`）。各部品は入力データだけで完結:

```javascript
renderIndicatorCard(indicator)  // → 要素: 値・単位・観測日・出所・kindバッジ
renderSparkline(series)         // → インラインSVG文字列（チャートライブラリなし）
renderChokepointSection(title, indicators)
renderClockGauge(indicator)     // threshold付きの残り日数/ゲージ
kindBadge(kind)                 // 価格/流れ/時計の色分け
```

- スパークラインは手書きインラインSVG。テキストは実DOM（検索に拾われ・選択でき・記事からリンクできる）。
- CSS は手書きの小さな1枚。kind 別に色分け。

### デプロイ

- nginx direct。静的 HTML/CSS/JS/JSON を直接配信。Docker / Kubernetes / microservices / バンドラ なし。

---

## 5. 更新フロー

```
[自動]  cron → 期限の fetcher 実行 → SQLite追記 → derived計算 → 静的JSON出力 → nginx配信
[手動]  観測 → Gemini検証(貼付) → append.py で1件追記 → 次回JSON出力に反映
```

記事の参照値とダッシュボードの指標を `id` で対応づける（記事 ↔ 指標の相互リンク）。手動指標は、出所が見つかり次第 fetcher 化して自動側へ移す。

---

## 6. 表示原則（編集方針）

- 表示するのは **物理量 ＋ 単位 ＋ 観測日 ＋ 出所** のみ。主張・予測を載せない。
- `threshold` は物理的に示す（NWF→0、中国停止 2026-08、中間選挙 2026-11）が、**結論は書かない**。読者が導く。
- `price` と `flow` を色で分け、「価格は数字、流れは実体」を一目で区別できるようにする。

---

## 7. MVP（足りる）と成長

- **Phase 1**: 静的JSON + 素のHTML/CSS/JS。`auto`/`derived` で取れる指標から離陸（ブレント・ウラル・政策金利・食料品CPI・各カウントダウン・スプレッド）。`manual` は最小限。
- **成長**: fetcher を1指標ずつ追加し、`manual` を `auto` へ昇格させる。隘路カテゴリも1つずつ追加。**データモデルとフロントは触らない。**

---

*この仕様自体が「小さく・自立し・育つ」を満たす: 単一データモデル、ライブラリ非依存の自己完結コンポーネント、自動取得優先のパイプライン、データで成長する構造。*