#!/usr/bin/env python3
"""100 個の Excel / CSV をまとめて集計する。

章本文: 「100 個の .xlsx から特定列を抽出する月次作業: Excel VBA で半日。
pandas で glob を使って一気に処理すれば 30 秒。」
これを実測する。
"""
from __future__ import annotations

import glob
import json
import sys
import time
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def aggregate(pattern: str, label: str) -> dict:
    files = sorted(glob.glob(pattern))
    t0 = time.perf_counter()
    if pattern.endswith(".xlsx"):
        df = pd.concat(pd.read_excel(f) for f in files)
    else:
        df = pd.concat(pd.read_csv(f) for f in files)
    by_item = df.groupby("商品").agg(
        件数=("売上", "count"),
        数量合計=("数量", "sum"),
        売上合計=("売上", "sum"),
        平均単価=("単価", "mean"),
    ).round(1).sort_values("売上合計", ascending=False)
    elapsed = time.perf_counter() - t0
    print(f"\n=== {label} ===")
    print(f"  読み込み: {len(files)} ファイル, {len(df):,} 行")
    print(f"  処理時間: {elapsed:.3f} 秒")
    print(by_item.to_string())
    return {
        "label": label,
        "files": len(files),
        "rows": len(df),
        "elapsed_seconds": round(elapsed, 3),
        "top_item": by_item.index[0],
        "top_revenue": int(by_item.iloc[0]["売上合計"]),
    }


def main():
    results = []
    if (HERE / "xlsx").exists():
        results.append(aggregate(str(HERE / "xlsx" / "*.xlsx"), "Excel (.xlsx) を pandas で集計"))
    if (HERE / "csv").exists():
        results.append(aggregate(str(HERE / "csv" / "*.csv"), "CSV を pandas で集計"))

    out = OUT / "summary.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n  → {out}")


if __name__ == "__main__":
    main()
