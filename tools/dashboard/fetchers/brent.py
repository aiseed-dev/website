"""ブレント価格 fetcher。

商品価格 API はキー必須のものが多いため、エンドポイントとキーを環境変数で
与える方式にしている（出所が確定したらここを埋めるだけで auto 化が完了する）:

    BRENT_API_URL  … {value} を返す JSON の URL（任意。未設定なら空を返す）
    BRENT_API_KEY  … Authorization: Bearer に載せる（任意）
    BRENT_JSON_PATH… ドット区切りで値の位置（例 "data.price"。既定 "price"）
"""

from __future__ import annotations

import os
from datetime import date
from typing import Any

from ..models import Point
from .base import http_json


def dig(obj: Any, path: str) -> Any:
    for key in path.split("."):
        obj = obj[key]
    return obj


class BrentFetcher:
    indicator_id = "brent"
    cadence = "daily"
    env_url = "BRENT_API_URL"
    env_key = "BRENT_API_KEY"
    env_path = "BRENT_JSON_PATH"
    source = "ICE"

    def fetch(self) -> list[Point]:
        url = os.environ.get(self.env_url)
        if not url:
            return []  # 出所未設定 — manual 側で補える
        headers = {}
        key = os.environ.get(self.env_key)
        if key:
            headers["Authorization"] = f"Bearer {key}"
        data = http_json(url, headers=headers)
        value = float(dig(data, os.environ.get(self.env_path, "price")))
        return [Point(date=date.today().isoformat(), value=round(value, 2),
                      source=self.source)]
