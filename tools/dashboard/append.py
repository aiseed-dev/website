#!/usr/bin/env python3
"""manual 指標の 1 件追記 CLI（仕様 §4 / §5）。

プログラム的な出所が無い指標の残余を人手で追記する。出所が見つかり次第、
fetcher 化して auto 側へ移す。value は数値でも状態文字列でも可。

    python3 tools/dashboard/append.py <indicator_id> <date> <value> <source>

例:
    python3 tools/dashboard/append.py hormuz_transit_status 2026-06-05 制限 "海事筋"
    python3 tools/dashboard/append.py naphtha_stock_days_jp 2026-06-05 18 "自前トラッキング"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import Point
from .storage import DEFAULT_DB, Store

HERE = Path(__file__).resolve().parent
INDICATORS = HERE / "catalog" / "indicators.json"


def known_ids() -> set[str]:
    raw = json.loads(INDICATORS.read_text("utf-8"))["indicators"]
    return {i["id"] for i in raw}


def coerce(value: str):
    """数値に見えるものは float に、それ以外は状態文字列のまま。"""
    try:
        return float(value)
    except ValueError:
        return value


def main() -> None:
    ap = argparse.ArgumentParser(description="manual 指標を 1 件追記")
    ap.add_argument("indicator_id")
    ap.add_argument("date", help="YYYY-MM-DD")
    ap.add_argument("value")
    ap.add_argument("source")
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()

    ids = known_ids()
    if args.indicator_id not in ids:
        ap.error(f"unknown indicator_id: {args.indicator_id}\n"
                 f"catalog に無い指標です。先に indicators.json へレコードを足してください。")

    store = Store(args.db)
    try:
        ok = store.append(
            args.indicator_id,
            Point(date=args.date, value=coerce(args.value), source=args.source),
        )
    finally:
        store.close()
    if ok:
        print(f"appended {args.indicator_id} {args.date} = {args.value} ({args.source})")
        print("→ 反映するには: python3 tools/dashboard/build.py --offline")
    else:
        print(f"既に {args.indicator_id} {args.date} は存在します（追記のみ・上書きしません）")


if __name__ == "__main__":
    main()
