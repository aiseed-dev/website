#!/usr/bin/env python3
"""新エンジン: PL/SQL の請求計算ロジックを Python に翻訳したもの。

並行稼働の要点:
  - 既存システム (legacy.sql) と同じ入力に対して、同じ出力を返す
  - 違いが出たら、それは「文書化されていなかった業務ルール」
  - 違いが出なくなった時点で、新しいシステムに切り替える

このファイルが「業務知識を Markdown に出す」入口にもなる。
ロジックの各ブロックにコメントを書けば、それが仕様書になる。
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent

# --- 業務ルール(現場担当の頭の中にあったもの)----------------------------
REMOTE_REGIONS = {"北海道", "沖縄"}
SHIPPING_REMOTE = 1500
SHIPPING_NORMAL = 800
SHIPPING_FREE_THRESHOLD = 10000  # 小計 10,000 円以上で送料無料
MEMBER_DISCOUNT_RATE = 0.05      # 会員: 小計の 5% 引き
BULK_DISCOUNT_THRESHOLD = 30000  # 会員割引後の小計が 30,000 円以上で
BULK_DISCOUNT_RATE = 0.03        #   さらに 3% 引き
TAX_RATE = 0.10                  # 消費税 10%
# ---------------------------------------------------------------------


@dataclass
class Invoice:
    id: int
    customer: str
    subtotal: int
    shipping: int
    member_discount: int
    bulk_discount: int
    tax: int
    final_total: int


def calculate_invoice(order: dict) -> Invoice:
    """注文 1 件 → 請求書 1 件。SQL の VIEW と同じ出力にする。"""
    qty = int(order["qty"])
    unit_price = int(order["unit_price"])
    is_member = int(order["is_member"]) == 1
    region = order["region"]

    subtotal = qty * unit_price

    # 送料
    if subtotal >= SHIPPING_FREE_THRESHOLD:
        shipping = 0
    elif region in REMOTE_REGIONS:
        shipping = SHIPPING_REMOTE
    else:
        shipping = SHIPPING_NORMAL

    # 会員割引(切り捨て)
    member_discount = int(subtotal * MEMBER_DISCOUNT_RATE) if is_member else 0

    # 大口割引: 会員割引適用後の小計に対して 3%(切り捨て)
    after_member = subtotal - member_discount
    bulk_discount = (
        int(after_member * BULK_DISCOUNT_RATE)
        if after_member >= BULK_DISCOUNT_THRESHOLD
        else 0
    )

    pretax = subtotal - member_discount - bulk_discount + shipping
    tax = int(pretax * TAX_RATE)
    final_total = pretax + tax

    return Invoice(
        id=int(order["id"]),
        customer=order["customer"],
        subtotal=subtotal,
        shipping=shipping,
        member_discount=member_discount,
        bulk_discount=bulk_discount,
        tax=tax,
        final_total=final_total,
    )


def main():
    # 入力データ(legacy.sql と同じ INSERT 行に対応)
    rows = [
        {"id": 1, "customer": "山田農園", "region": "東京", "qty": 5, "unit_price": 2400, "is_member": 1},
        {"id": 2, "customer": "鈴木商店", "region": "北海道", "qty": 12, "unit_price": 1800, "is_member": 0},
        {"id": 3, "customer": "高橋食品", "region": "沖縄", "qty": 3, "unit_price": 3600, "is_member": 0},
        {"id": 4, "customer": "佐藤畜産", "region": "大阪", "qty": 8, "unit_price": 1500, "is_member": 1},
        {"id": 5, "customer": "田中株式会社", "region": "東京", "qty": 1, "unit_price": 12000, "is_member": 0},
        {"id": 6, "customer": "渡辺青果", "region": "北海道", "qty": 25, "unit_price": 800, "is_member": 1},
        {"id": 7, "customer": "中村製作所", "region": "東京", "qty": 4, "unit_price": 4500, "is_member": 0},
        {"id": 8, "customer": "小林技研", "region": "九州", "qty": 6, "unit_price": 2200, "is_member": 1},
        {"id": 9, "customer": "斎藤運輸", "region": "東京", "qty": 18, "unit_price": 950, "is_member": 1},
        {"id": 10, "customer": "加藤建設", "region": "沖縄", "qty": 2, "unit_price": 7800, "is_member": 0},
    ]

    invoices = [calculate_invoice(r) for r in rows]

    # SQLite の `.mode csv` はテキストカラムだけダブルクオートする。
    # 並行稼働の出力差分を「業務ロジックの差分」だけに絞るため、CSV の
    # 表現も SQLite に合わせる。
    # SQLite の `.mode csv` は: テキストカラムだけダブルクオート + 改行は CRLF
    out = HERE / "out" / "new_output.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("wb") as f:
        f.write(b"id,customer,subtotal,shipping,member_discount,bulk_discount,tax,final_total\r\n")
        for inv in invoices:
            line = (
                f'{inv.id},"{inv.customer}",{inv.subtotal},{inv.shipping},'
                f'{inv.member_discount},{inv.bulk_discount},{inv.tax},{inv.final_total}\r\n'
            )
            f.write(line.encode())
    print(f"  → {out}  ({len(invoices)} 件)")


if __name__ == "__main__":
    main()
