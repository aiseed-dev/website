"""Fetcher レジストリ（仕様 §4）。

レジストリに 1 行足すだけで指標が増える。グループ fetcher（複数指標を
まとめて返すもの）は GROUP_FETCHERS に置く。
"""

from .base import Fetcher, safe_fetch
from .bls_cpi import BlsCpiFetcher
from .brent import BrentFetcher
from .cbr_rate import CbrRateFetcher
from .crea_monthly import CreaMonthlyFetcher
from .mosaic import MosaicFetcher
from .urals import UralsFetcher

# 1 指標 1 ポイント列を返す fetcher
FETCHERS: list[Fetcher] = [
    BrentFetcher(),
    UralsFetcher(),
    CbrRateFetcher(),
    BlsCpiFetcher(),
    MosaicFetcher(),
]

# 複数指標をまとめて返す fetcher（fetch_grouped() を持つ）
GROUP_FETCHERS = [
    CreaMonthlyFetcher(),
]

__all__ = [
    "Fetcher",
    "safe_fetch",
    "FETCHERS",
    "GROUP_FETCHERS",
]
