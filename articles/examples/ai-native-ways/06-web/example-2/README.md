# 実例 2 — FastAPI 1 ファイルで業務 API + 自動 Swagger UI

第 07 章「Webを作る ── HTML+CSS+JavaScriptという原点回帰」の **2 番目の角度**:
**動的処理は FastAPI で最小限**(章本文の主張そのもの)。

## 章のどの主張に対応するか

> 動的処理はサーバー側で書く。Python(FastAPI)だけでいいのでは。
> それも、最小限にする。

(章本文より)

example-1 は静的サイト(Markdown → HTML)、これは **書き込み・集計が
必要な業務側** を最小サイズで実演する。

## やること

1. **`app.py`(70 行)** で受注 API を実装:
   - `GET /` — ヘルスチェック
   - `POST /orders` — 受注登録(JSON)
   - `GET /orders` — 一覧
   - `GET /orders/{id}` — 1 件取得(404 つき)
   - `GET /stats` — 集計(件数 / 売上 / 商品別)
   - `GET /docs` — **Swagger UI 自動生成**(無料)
2. **`test_api.py`** で 11 リクエストを叩いて結果を JSON に保存
3. ストレージは **SQLite 1 ファイル**(別 DB サーバ不要)
4. Pydantic で **自動バリデーション**(qty > 0、unit_price ≤ 10M、など)

## 構成

```
example-2/
├── README.md
├── app.py             ── FastAPI アプリ本体(約 70 行)
├── test_api.py        ── TestClient で 11 リクエスト走らせる
├── Makefile
├── results.md
└── out/
    ├── orders.db      ── SQLite データ(.gitignore してもよい)
    ├── orders.json    ── 一覧の応答
    ├── stats.json     ── 集計の応答
    ├── openapi.json   ── Swagger スキーマ(API ドキュメント)
    └── request-log.txt── 11 件のレイテンシ
```

## 実行

```bash
pip install fastapi uvicorn httpx
make all                # テスト走らせて結果を out/ に保存
make serve              # http://localhost:8000 で立てる(Swagger は /docs)
```

## なぜこれが「実例」になるのか

業務 Web に必要なのは:

1. **画面**(章 07 example-1 の Markdown → HTML)
2. **書き込み・集計**(このフォルダ:FastAPI + SQLite)
3. **認証**(必要なら、別途 30 行追加)

これだけ。**React も Next.js も Postgres も Redis も要らない**。

| 項目 | 大きいスタック | このスタック |
|------|--------------|------------|
| バックエンド | Express + TypeScript | **FastAPI 1 ファイル 70 行** |
| DB | Postgres + Redis + ORM | **SQLite 1 ファイル** |
| API ドキュメント | Swagger UI を別途設定 | **/docs で自動生成** |
| バリデーション | zod / class-validator | **Pydantic 自動** |
| 開発サーバ | nodemon + tsx + ts-node | **`uvicorn --reload`** |
| デプロイ | Docker + k8s + ロードバランサ | **`uvicorn app:app`** または fly.io |

これが章で言う「**Python(FastAPI)だけ、それも最小限**」の具体形。

## 自動生成された API ドキュメント

`make serve` してブラウザで `http://localhost:8000/docs` を開くと:

- 全エンドポイントの一覧
- リクエスト例 + 「Try it out」ボタン
- レスポンススキーマ
- バリデーションルール

これを **コードを書いた瞬間に自動で得られる**。Express で同じものを
作ろうとすると、`swagger-jsdoc` を入れて、デコレータを書いて、設定して...
**最低 半日**。FastAPI なら **0 秒**(自動)。

## バリデーション例

```python
class OrderIn(BaseModel):
    customer: str = Field(..., min_length=1, max_length=100)
    item: str = Field(..., min_length=1, max_length=100)
    qty: int = Field(..., gt=0, le=10_000)
    unit_price: int = Field(..., gt=0, le=10_000_000)
```

不正なリクエストには **422 + エラー詳細** が返る:

```json
POST /orders {"customer":"","item":"x","qty":-1,"unit_price":0}

→ 422 Unprocessable Entity
{
  "detail": [
    {"loc":["body","customer"],"msg":"String should have at least 1 character"},
    {"loc":["body","qty"],"msg":"Input should be greater than 0"},
    {"loc":["body","unit_price"],"msg":"Input should be greater than 0"}
  ]
}
```

これも **自動**。手書きのバリデーション関数は 1 行も書いていない。
