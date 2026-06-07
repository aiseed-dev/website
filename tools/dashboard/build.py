#!/usr/bin/env python3
"""ダッシュボードのビルド・エントリポイント（仕様 §4 / §5）。

cron が起動する単一エントリポイント。取得 → 計算 → 出力を一巡する。常駐なし。

    1. カタログ読み込み（chokepoints.json / indicators.json）
    2. カタログ同梱の series（documented/static 点）を SQLite に追記（冪等）
    3. 期限の来た fetcher を実行 → 生ポイントを SQLite に追記
    4. derived 指標を計算（スプレッド・比率・残り日数）
    5. 静的 JSON を出力 → html/dashboard/data/dashboard.json

ネットワークやキーが無くても落ちない（fetcher 障害は空ポイント扱い）。
その場合でもカタログ＋静的点＋カウントダウンで JSON は生成される。

使い方:
    python3 tools/dashboard/build.py                 # 全 cadence
    python3 tools/dashboard/build.py --cadence daily # 日次のみ
    python3 tools/dashboard/build.py --offline       # fetcher を一切叩かない
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path

from .derived import DERIVED, days_until
from .fetchers import FETCHERS, GROUP_FETCHERS, safe_fetch
from .models import Indicator, Point
from .storage import DEFAULT_DB, Store

HERE = Path(__file__).resolve().parent
CATALOG = HERE / "catalog"
# 出力先: 静的フロントエンドが 1 回 fetch する JSON。nginx/Cloudflare が直接配信。
DEFAULT_OUT = HERE.parents[1] / "html" / "dashboard" / "data" / "dashboard.json"


def load_catalog() -> tuple[list[dict], list[Indicator]]:
    chokepoints = json.loads((CATALOG / "chokepoints.json").read_text("utf-8"))["chokepoints"]
    raw = json.loads((CATALOG / "indicators.json").read_text("utf-8"))["indicators"]
    indicators = [Indicator.from_dict(d) for d in raw]
    return chokepoints, indicators


def seed_store(store: Store, indicators: list[Indicator]) -> None:
    """カタログ同梱の点（documented/static）を冪等に追記する。"""
    for ind in indicators:
        if ind.series:
            store.append_many(ind.id, ind.series)


def run_fetchers(store: Store, cadence: str | None) -> int:
    added = 0
    for f in FETCHERS:
        if cadence and f.cadence != cadence:
            continue
        pts = safe_fetch(f)
        n = store.append_many(f.indicator_id, pts)
        if n:
            print(f"  + {f.indicator_id}: {n} point(s)")
        added += n
    for gf in GROUP_FETCHERS:
        if cadence and gf.cadence != cadence:
            continue
        try:
            grouped = gf.fetch_grouped()
        except Exception as exc:  # noqa: BLE001
            print(f"  [warn] {gf.indicator_id}: {exc}")
            continue
        for ind_id, pts in grouped.items():
            n = store.append_many(ind_id, pts)
            if n:
                print(f"  + {ind_id}: {n} point(s)")
            added += n
    return added


def compute_derived(store: Store, indicators: list[Indicator]) -> None:
    """derived 指標を計算して series を埋める（手入力ゼロ）。"""
    latest = store.latest_values()
    today = date.today().isoformat()
    for ind in indicators:
        if ind.acquisition != "derived" or not ind.derived:
            continue
        fn = DERIVED.get(ind.derived)
        if fn is None:
            continue
        if ind.target_date:  # カウントダウン: 今日基準で毎回再計算（保存しない）
            value = days_until(ind.target_date)
            ind.series = [Point(date=today, value=value, source="（計算）")]
            continue
        value = fn(latest)
        if value is None:
            continue
        # 入力の最新日を継承（無ければ今日）
        d = max((latest.get(k, "") for k in ("brent", "urals", "dap_price")
                 if k in latest), default=today) or today
        ind.series = store.series(ind.id) + [
            Point(date=today, value=value, source="（計算）")
        ]


def assemble(chokepoints: list[dict], indicators: list[Indicator],
             store: Store) -> dict:
    by_cp: dict[str, list[dict]] = {cp["id"]: [] for cp in chokepoints}
    for ind in indicators:
        # derived は compute_derived が series を確定済み。それ以外は store から復元。
        if ind.acquisition != "derived":
            stored = store.series(ind.id)
            if stored:
                ind.series = stored
        if ind.chokepoint in by_cp:
            by_cp[ind.chokepoint].append(ind.to_dict())
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "spec": "docs/physical-dashboard-spec.md v0.1",
        "chokepoints": [
            {
                "id": cp["id"],
                "name_ja": cp["name_ja"],
                "name_en": cp["name_en"],
                "indicators": by_cp[cp["id"]],
            }
            for cp in sorted(chokepoints, key=lambda c: c.get("order", 99))
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="aiseed.dev 物理量ダッシュボード build")
    ap.add_argument("--cadence", choices=["daily", "monthly", "quarterly", "event"],
                    help="この cadence の fetcher のみ実行")
    ap.add_argument("--offline", action="store_true", help="fetcher を一切叩かない")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="SQLite ファイル")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="出力 JSON")
    args = ap.parse_args()

    chokepoints, indicators = load_catalog()
    store = Store(args.db)
    try:
        seed_store(store, indicators)
        if not args.offline:
            print("fetch:")
            run_fetchers(store, args.cadence)
        compute_derived(store, indicators)
        out = assemble(chokepoints, indicators, store)
    finally:
        store.close()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", "utf-8")
    n_ind = sum(len(cp["indicators"]) for cp in out["chokepoints"])
    print(f"wrote {out_path} — {len(out['chokepoints'])} chokepoints, {n_ind} indicators")


if __name__ == "__main__":
    main()
