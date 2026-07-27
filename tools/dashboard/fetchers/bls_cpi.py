"""米国 食料品 CPI fetcher（BLS 公開 API v2）。

series CUUR0000SAF11（Food, all urban consumers, NSA）の前年同月比を計算する。
BLS_API_KEY 環境変数があれば付与（無くても登録不要の上限内で叩ける）。
"""

from __future__ import annotations

import json
import os

from ..models import Point
from .base import http_json

SERIES_ID = "CUUR0000SAF11"  # Food
URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


class BlsCpiFetcher:
    indicator_id = "food_cpi"
    cadence = "monthly"

    def fetch(self) -> list[Point]:
        payload: dict = {"seriesid": [SERIES_ID], "latest": True}
        key = os.environ.get("BLS_API_KEY")
        if key:
            payload["registrationkey"] = key
        data = http_json(
            URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        rows = data["Results"]["series"][0]["data"]
        if len(rows) < 13:
            return []
        latest = rows[0]
        year_ago = rows[12]
        yoy = (float(latest["value"]) / float(year_ago["value"]) - 1) * 100
        month = latest["period"].lstrip("M").zfill(2)
        date = f"{latest['year']}-{month}-01"
        return [Point(date=date, value=round(yoy, 1), source="BLS")]
