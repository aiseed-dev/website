# 計測結果 — 第 07 章 example-2

実行環境: Linux 6.18 / FastAPI 0.136 / Pydantic 2.13 / SQLite 3.45 / Python 3.11

## API レイテンシ(11 リクエスト)

```
GET   /                        → 200  (10.3 ms)
POST  /orders                  → 201  ( 5.3 ms)
POST  /orders                  → 201  ( 4.3 ms)
POST  /orders                  → 201  ( 4.3 ms)
POST  /orders                  → 201  ( 4.2 ms)
POST  /orders                  → 201  ( 4.0 ms)
GET   /orders                  → 200  ( 3.2 ms)
GET   /orders/5                → 200  ( 3.2 ms)
GET   /orders/9999             → 404  ( 3.0 ms)
GET   /stats                   → 200  ( 4.4 ms)
GET   /openapi.json            → 200  (26.2 ms)
```

| 操作 | 平均レイテンシ |
|------|--------------|
| 単純 GET | 約 3〜4 ms |
| POST(SQLite 書き込み + バリデーション) | 約 4〜5 ms |
| 集計クエリ(GROUP BY) | 約 4 ms |
| Swagger スキーマ生成 | 約 26 ms(初回のみ) |

10 ms 未満で応答。**SQLite は単一マシンの業務 API には十分** 速い。

## 規模

| 項目 | 数値 |
|------|------|
| `app.py` 行数 | **約 70 行**(コメント込み) |
| 依存パッケージ | fastapi, uvicorn, pydantic(計 3 個) |
| `node_modules` | **0 KB** |
| データベースサーバ | **不要**(SQLite はファイル) |
| 起動時間 | < 1 秒 |
| メモリ | 約 50 MB |

## 集計結果(`GET /stats`)

5 件の受注を投入したあと:

```json
{
  "count": 5,
  "revenue": 71400,
  "by_item": [
    {"item": "キャベツ", "count": 3, "revenue": 32400},
    {"item": "トマト",   "count": 1, "revenue": 20000},
    {"item": "玉葱",     "count": 1, "revenue": 19000}
  ]
}
```

集計は SQL の `GROUP BY` 1 行:

```sql
SELECT item, COUNT(*), SUM(total) FROM orders GROUP BY item ORDER BY SUM(total) DESC
```

ORM もデコレータも要らない。

## バリデーション(自動)

```python
class OrderIn(BaseModel):
    customer: str = Field(..., min_length=1, max_length=100)
    qty: int = Field(..., gt=0, le=10_000)
    unit_price: int = Field(..., gt=0, le=10_000_000)
```

これだけで、不正リクエストは **422** で弾かれる。手書きの if 文ゼロ。

## OpenAPI スキーマ(`out/openapi.json`、6.7 KB)

`/docs` で **Swagger UI**、`/redoc` で **ReDoc** ── 両方とも自動生成。
チームへの API 仕様共有が「URL を渡す」で終わる。

## デプロイ(参考)

```bash
# 開発
uvicorn app:app --reload

# 本番(systemd)
ExecStart=/usr/bin/uvicorn app:app --host 0.0.0.0 --port 8000

# fly.io
fly launch --image python:3.11
fly deploy
```

**月 0〜数百円**で本番運用できる。Postgres も Redis も要らない規模なら
SQLite + Cloudflare Tunnel で月 0 円も可能。

## 章本文との対応

> 動的処理はサーバ側で書く。Python(FastAPI)だけでいいのでは。
> それも、最小限にする。

このフォルダは:

- **70 行の単一ファイル**(`app.py`)
- **3 つの依存パッケージ**(fastapi, uvicorn, pydantic)
- **DB サーバなし**(SQLite)
- **Swagger 自動**

「最小限」がどこまで小さくできるかの実演。

## 再現手順

```bash
pip install fastapi uvicorn httpx
make clean && make all       # TestClient で動作確認
# または
make serve                   # http://localhost:8000/docs
```
