"""CREA 月次データ fetcher（ロシア石油の流れ）。

CREA（Centre for Research on Energy and Clean Air）の月次トラッカーは現状
プログラム的な安定 API が無いため、ここは「出所が現れ次第埋める」枠として
置いている。CREA_CSV_URL を与えると、最小スキーマの CSV を読み込む:

    date,indicator_id,value,source

未設定なら空を返し、該当指標は manual 側（append.py）で補う。
"""

from __future__ import annotations

import csv
import io
import os

from ..models import Point
from .base import http_text

# この fetcher が面倒を見る指標群（cadence=monthly）
INDICATOR_IDS = [
    "russia_seaborne_crude_exports",
    "russia_shadow_fleet_share",
    "russia_false_flag_vessels",
    "russia_products_g7_dependence",
]


class CreaMonthlyFetcher:
    indicator_id = "russia_oil_flow"  # 複数指標をまとめて返すグループ fetcher
    cadence = "monthly"

    def fetch_grouped(self) -> dict[str, list[Point]]:
        url = os.environ.get("CREA_CSV_URL")
        out: dict[str, list[Point]] = {i: [] for i in INDICATOR_IDS}
        if not url:
            return out
        text = http_text(url)
        for row in csv.DictReader(io.StringIO(text)):
            ind = row["indicator_id"]
            if ind in out:
                out[ind].append(
                    Point(date=row["date"], value=float(row["value"]),
                          source=row.get("source", "CREA"))
                )
        return out

    def fetch(self) -> list[Point]:
        # 単一指標インターフェース互換（build はグループ対応を優先して使う）
        return []
