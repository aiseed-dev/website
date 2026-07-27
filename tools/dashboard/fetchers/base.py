"""Fetcher の共通インターフェース（仕様 §4）。

1 指標 1 モジュール。`FETCHERS` レジストリに足すだけで増える。
fetcher は外部 API/スクレイプに依存するため、失敗してもパイプライン全体を
止めない（`safe_fetch` が例外を握りつぶし空リストを返す）。
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any, Protocol, runtime_checkable

from ..models import Point

USER_AGENT = "aiseed-dashboard/0.1 (+https://aiseed.dev)"
TIMEOUT = 20


@runtime_checkable
class Fetcher(Protocol):
    indicator_id: str
    cadence: str  # daily | monthly | quarterly | event

    def fetch(self) -> list[Point]:
        """[(date, value, source)] を返す。"""
        ...


def http_json(url: str, *, data: bytes | None = None,
              headers: dict[str, str] | None = None) -> Any:
    """JSON を 1 回取得する小さなヘルパ（stdlib のみ）。"""
    req = urllib.request.Request(url, data=data)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_text(url: str) -> str:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8")


def safe_fetch(fetcher: Fetcher) -> list[Point]:
    """fetch を例外安全に実行。失敗は空リスト（手入力側で補える）。"""
    try:
        return list(fetcher.fetch())
    except Exception as exc:  # noqa: BLE001 — fetcher 障害は全体を止めない
        print(f"  [warn] {fetcher.indicator_id}: fetch failed: {exc}")
        return []
