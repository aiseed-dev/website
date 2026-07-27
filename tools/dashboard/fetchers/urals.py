"""ウラル価格 fetcher。

Brent と同じ env 駆動パターン（出所が確定したら埋めるだけ）:

    URALS_API_URL / URALS_API_KEY / URALS_JSON_PATH
"""

from __future__ import annotations

from .brent import BrentFetcher


class UralsFetcher(BrentFetcher):
    indicator_id = "urals"
    cadence = "daily"
    env_url = "URALS_API_URL"
    env_key = "URALS_API_KEY"
    env_path = "URALS_JSON_PATH"
    source = "CREA"
