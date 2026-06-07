"""Mosaic 稼働率 fetcher（四半期）。

Mosaic の IR 開示は四半期ごと。安定した数値 API が無いため、
MOSAIC_JSON_URL（{date,value} を返す）を与えれば auto 化される枠。
未設定なら空を返す。
"""

from __future__ import annotations

import os

from ..models import Point
from .base import http_json


class MosaicFetcher:
    indicator_id = "mosaic_utilization"
    cadence = "quarterly"

    def fetch(self) -> list[Point]:
        url = os.environ.get("MOSAIC_JSON_URL")
        if not url:
            return []
        data = http_json(url)
        return [Point(date=data["date"], value=float(data["value"]),
                      source="Mosaic IR")]
