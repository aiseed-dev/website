#!/usr/bin/env python3
"""最小の業務 API ── FastAPI 1 ファイル、SQLite、約 70 行。

機能:
  GET  /              ── ヘルスチェック
  POST /orders        ── 受注を登録(JSON)
  GET  /orders        ── 受注一覧
  GET  /orders/{id}   ── 1 件取得
  GET  /stats         ── 集計(件数 + 売上合計)
  GET  /docs          ── Swagger UI(自動生成)

第 7 章「動的処理はサーバ側、最小限に」── 業務 Web に必要な動的部分は
これくらいで足りる。フロントは静的 HTML で読み書きする(Markdown ビルド)。
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).parent / "out" / "orders.db"
DB_PATH.parent.mkdir(exist_ok=True)


@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            item TEXT NOT NULL,
            qty INTEGER NOT NULL,
            unit_price INTEGER NOT NULL,
            total INTEGER GENERATED ALWAYS AS (qty * unit_price) VIRTUAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")


class OrderIn(BaseModel):
    customer: str = Field(..., min_length=1, max_length=100)
    item: str = Field(..., min_length=1, max_length=100)
    qty: int = Field(..., gt=0, le=10_000)
    unit_price: int = Field(..., gt=0, le=10_000_000)


class OrderOut(BaseModel):
    id: int
    customer: str
    item: str
    qty: int
    unit_price: int
    total: int
    created_at: str


app = FastAPI(title="aiseed orders", version="0.1.0")
init_db()


@app.get("/")
def health():
    return {"status": "ok", "service": "aiseed orders", "version": "0.1.0"}


@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order: OrderIn):
    with db() as c:
        cur = c.execute(
            "INSERT INTO orders (customer, item, qty, unit_price) VALUES (?, ?, ?, ?)",
            (order.customer, order.item, order.qty, order.unit_price),
        )
        row = c.execute("SELECT * FROM orders WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)


@app.get("/orders")
def list_orders(limit: int = 50):
    with db() as c:
        rows = c.execute("SELECT * FROM orders ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    with db() as c:
        row = c.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="not found")
        return dict(row)


@app.get("/stats")
def stats():
    with db() as c:
        row = c.execute(
            "SELECT COUNT(*) as count, COALESCE(SUM(total), 0) as revenue FROM orders"
        ).fetchone()
        by_item = c.execute(
            "SELECT item, COUNT(*) as count, SUM(total) as revenue "
            "FROM orders GROUP BY item ORDER BY revenue DESC"
        ).fetchall()
    return {
        "count": row["count"],
        "revenue": row["revenue"],
        "by_item": [dict(r) for r in by_item],
    }
