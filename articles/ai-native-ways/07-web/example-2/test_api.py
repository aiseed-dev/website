#!/usr/bin/env python3
"""走らせて API を叩いて動作確認 + 結果を out/ に保存する。

外部の HTTP サーバを立てずに FastAPI の TestClient で完結させる
(httpx ベース、本物の HTTP サーバとほぼ同じ挙動)。
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from fastapi.testclient import TestClient

import app as app_module

# テスト用にデータベースをリセット
app_module.DB_PATH.unlink(missing_ok=True)
app_module.init_db()

client = TestClient(app_module.app)
OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)


def main():
    log = []

    def call(method: str, url: str, **kw):
        t0 = time.perf_counter()
        r = client.request(method, url, **kw)
        dt = (time.perf_counter() - t0) * 1000
        log.append(f"{method:5s} {url:24s} → {r.status_code}  ({dt:.1f} ms)")
        return r

    # ヘルスチェック
    r = call("GET", "/")
    assert r.status_code == 200

    # 受注を 5 件登録
    samples = [
        {"customer": "山田農園", "item": "キャベツ", "qty": 50, "unit_price": 180},
        {"customer": "鈴木商店", "item": "玉葱", "qty": 200, "unit_price": 95},
        {"customer": "高橋食品", "item": "キャベツ", "qty": 30, "unit_price": 180},
        {"customer": "佐藤畜産", "item": "トマト", "qty": 80, "unit_price": 250},
        {"customer": "田中株式会社", "item": "キャベツ", "qty": 100, "unit_price": 180},
    ]
    for s in samples:
        r = call("POST", "/orders", json=s)
        assert r.status_code == 201

    # 一覧
    r = call("GET", "/orders")
    orders = r.json()

    # 個別取得
    call("GET", f"/orders/{orders[0]['id']}")
    call("GET", "/orders/9999")  # 404

    # 統計
    r = call("GET", "/stats")
    s = r.json()

    # OpenAPI スキーマ
    r = call("GET", "/openapi.json")
    schema = r.json()

    # 出力保存
    (OUT / "orders.json").write_text(json.dumps(orders, ensure_ascii=False, indent=2))
    (OUT / "stats.json").write_text(json.dumps(s, ensure_ascii=False, indent=2))
    (OUT / "openapi.json").write_text(json.dumps(schema, ensure_ascii=False, indent=2))
    (OUT / "request-log.txt").write_text("\n".join(log) + "\n")

    print("\n=== 動作確認 ===")
    for line in log:
        print(f"  {line}")
    print()
    print("=== 集計結果 (GET /stats)===")
    print(f"  件数  : {s['count']} 件")
    print(f"  売上  : {s['revenue']:,} 円")
    print(f"  商品別:")
    for it in s["by_item"]:
        print(f"    {it['item']:6s} {it['count']} 件 / {it['revenue']:>8,} 円")
    print()
    print(f"  → out/orders.json     ({(OUT / 'orders.json').stat().st_size} B)")
    print(f"  → out/stats.json      ({(OUT / 'stats.json').stat().st_size} B)")
    print(f"  → out/openapi.json    ({(OUT / 'openapi.json').stat().st_size} B)")
    print(f"  → out/request-log.txt")


if __name__ == "__main__":
    main()
