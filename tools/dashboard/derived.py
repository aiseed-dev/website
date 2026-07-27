"""derived 指標の計算（仕様 §4「derived」）。

計算できるものは決して手で入れない。各 derived は最新値の dict を受け取り、
1 つの数値（または None）を返す。countdown は今日基準の残り日数。
"""

from __future__ import annotations

from datetime import date
from typing import Any, Callable


def days_until(target: str, today: date | None = None) -> int:
    """target(YYYY-MM-DD) までの残り日数。過ぎていれば負。"""
    today = today or date.today()
    y, m, d = (int(x) for x in target.split("-"))
    return (date(y, m, d) - today).days


def _ratio(num: Any, den: Any) -> float | None:
    try:
        num = float(num)
        den = float(den)
    except (TypeError, ValueError):
        return None
    if den == 0:
        return None
    return round(num / den, 3)


def _spread(a: Any, b: Any) -> float | None:
    try:
        return round(float(a) - float(b), 2)
    except (TypeError, ValueError):
        return None


# DERIVED: derived id -> (最新値 dict) -> 値 or None
DERIVED: dict[str, Callable[[dict[str, Any]], Any]] = {
    "urals_brent_spread": lambda d: _spread(d.get("brent"), d.get("urals")),
    "dap_corn_ratio": lambda d: _ratio(d.get("dap_price"), d.get("corn")),
    "military_vs_oilgas": lambda d: _ratio(
        d.get("military_spend"), d.get("oilgas_revenue")
    ),
    "china_ban_countdown": lambda _d: days_until("2026-08-31"),
    "us_midterm_countdown": lambda _d: days_until("2026-11-03"),
}
