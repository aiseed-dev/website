"""CBR 政策金利（key rate）fetcher。

ロシア中央銀行のキーレート XML（公開・キー不要）から最新値を取得する。
ネットワークやエンドポイントが使えない場合は base.safe_fetch が空を返す。
"""

from __future__ import annotations

import re

from ..models import Point
from .base import http_text

# CBR キーレートの動的 XML（日付範囲指定）。公開エンドポイント。
URL = "https://www.cbr.ru/hd_base/KeyRate/Dynamics/"


class CbrRateFetcher:
    indicator_id = "cbr_policy_rate"
    cadence = "daily"

    def fetch(self) -> list[Point]:
        html = http_text(URL)
        # 行: <td>DD.MM.YYYY</td><td>NN,NN</td> を素朴に拾う
        rows = re.findall(
            r"<td[^>]*>(\d{2}\.\d{2}\.\d{4})</td>\s*<td[^>]*>([\d,]+)</td>", html
        )
        if not rows:
            return []
        d, v = rows[0]  # 最新行
        dd, mm, yyyy = d.split(".")
        value = float(v.replace(",", "."))
        return [Point(date=f"{yyyy}-{mm}-{dd}", value=value, source="CBR")]
