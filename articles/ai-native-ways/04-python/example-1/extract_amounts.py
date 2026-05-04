#!/usr/bin/env python3
"""100 個の請求書 PDF から、合計金額と請求先を抽出する。

章本文の主張: 「100 個の請求書 PDF から金額を抽出する月次作業:
手作業で 4 時間。Claude が書いた Python で 3 秒。」── を実測する。
"""
from __future__ import annotations

import csv
import glob
import json
import re
import time
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).parent
PDF_DIR = HERE / "pdf"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

INVOICE_NO_RE = re.compile(r"INV-2026-(\d{4})")
CUSTOMER_RE = re.compile(r"請求先[:：]\s*(.+?)\s*御中")
TOTAL_RE = re.compile(r"合計金額[:：]?\s*([\d,]+)\s*円")


def parse_pdf(path: Path) -> dict:
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    inv = INVOICE_NO_RE.search(text)
    cust = CUSTOMER_RE.search(text)
    tot = TOTAL_RE.search(text)
    return {
        "file": path.name,
        "invoice_no": inv.group(0) if inv else "",
        "customer": cust.group(1) if cust else "",
        "total": int(tot.group(1).replace(",", "")) if tot else 0,
    }


def main():
    files = sorted(glob.glob(str(PDF_DIR / "*.pdf")))
    t0 = time.perf_counter()
    rows = [parse_pdf(Path(f)) for f in files]
    elapsed = time.perf_counter() - t0

    by_customer = {}
    grand = 0
    parsed_ok = 0
    for r in rows:
        if r["total"]:
            parsed_ok += 1
            grand += r["total"]
            by_customer[r["customer"]] = by_customer.get(r["customer"], 0) + r["total"]

    csv_path = OUT / "extracted.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "invoice_no", "customer", "total"])
        w.writeheader()
        w.writerows(rows)

    json_path = OUT / "summary.json"
    summary = {
        "files": len(files),
        "parsed_ok": parsed_ok,
        "elapsed_seconds": round(elapsed, 3),
        "grand_total_yen": grand,
        "top_customers": sorted(
            ({"customer": k, "total": v} for k, v in by_customer.items()),
            key=lambda r: r["total"],
            reverse=True,
        )[:10],
    }
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print(f"\n=== 100 個の請求書 PDF から金額抽出 ===")
    print(f"  処理時間: {elapsed:.3f} 秒  ({len(files)} ファイル)")
    print(f"  抽出成功: {parsed_ok} / {len(files)} 件")
    print(f"  合計金額: {grand:,} 円")
    print()
    print("=== 顧客別ランキング(上位 10 社) ===")
    for r in summary["top_customers"]:
        print(f"  {r['customer']:<14}  {r['total']:>12,} 円")
    print(f"\n  → {csv_path}")
    print(f"  → {json_path}")


if __name__ == "__main__":
    main()
