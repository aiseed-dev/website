#!/usr/bin/env python3
"""customers.csv を JSON / YAML に往復変換し、3 形式とも内容が同一で
あることを示す。それぞれの強みもサイズで比較する。
"""
from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import yaml

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def main():
    csv_path = DATA / "customers.csv"

    # CSV → list of dicts
    t0 = time.perf_counter()
    with csv_path.open() as f:
        rows = list(csv.DictReader(f))
        for r in rows:
            r["monthly_yen"] = int(r["monthly_yen"])
    csv_load = time.perf_counter() - t0

    # → JSON
    t0 = time.perf_counter()
    json_path = OUT / "customers.json"
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    json_write = time.perf_counter() - t0

    # → YAML
    t0 = time.perf_counter()
    yaml_path = OUT / "customers.yaml"
    yaml_path.write_text(yaml.safe_dump(rows, allow_unicode=True, sort_keys=False))
    yaml_write = time.perf_counter() - t0

    # 往復: JSON → CSV にもう一度落として元と一致するか
    t0 = time.perf_counter()
    rows_back = json.loads(json_path.read_text())
    rt_csv = OUT / "customers-roundtrip.csv"
    with rt_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows_back[0].keys())
        w.writeheader()
        for r in rows_back:
            w.writerow(r)
    rt = time.perf_counter() - t0

    print("=== 形式変換 ===")
    print(f"  CSV → list[dict] : {csv_load*1000:6.1f} ms")
    print(f"  → JSON           : {json_write*1000:6.1f} ms  ({json_path.stat().st_size:>5} B)")
    print(f"  → YAML           : {yaml_write*1000:6.1f} ms  ({yaml_path.stat().st_size:>5} B)")
    print(f"  JSON → CSV 往復   : {rt*1000:6.1f} ms")
    print()

    same = csv_path.read_text().strip().split("\n") == rt_csv.read_text().strip().split("\n")
    print(f"  CSV ⇄ JSON ⇄ CSV 完全往復: {'✓ 一致' if same else '✗ 不一致'}")
    print()

    # サンプル
    print("=== JSON 抜粋 ===")
    print(json_path.read_text()[:200] + " ...")
    print()
    print("=== YAML 抜粋 ===")
    print(yaml_path.read_text()[:200] + " ...")


if __name__ == "__main__":
    main()
