"""SQLite 単一ファイルの append-only series ストア（仕様 §4「保存」）。

series は追記のみ。同じ (indicator_id, date) の重複は無視する（冪等）。
重い DB は不要 — 標準ライブラリの sqlite3 だけ。
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .models import Point

DEFAULT_DB = Path(__file__).resolve().parent / "data" / "series.sqlite3"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS series (
    indicator_id TEXT NOT NULL,
    date         TEXT NOT NULL,
    value        TEXT NOT NULL,   -- JSON-encoded（数値 or 文字列）
    source       TEXT NOT NULL,
    PRIMARY KEY (indicator_id, date)
);
"""


class Store:
    """append-only な観測ストア。"""

    def __init__(self, path: Path | str = DEFAULT_DB) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(_SCHEMA)
        self.conn.commit()

    def append(self, indicator_id: str, point: Point) -> bool:
        """1 件追記。新規なら True、既存(同日)なら False。"""
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO series (indicator_id, date, value, source) "
            "VALUES (?, ?, ?, ?)",
            (indicator_id, point.date, json.dumps(point.value), point.source),
        )
        self.conn.commit()
        return cur.rowcount > 0

    def append_many(self, indicator_id: str, points: list[Point]) -> int:
        return sum(self.append(indicator_id, p) for p in points)

    def series(self, indicator_id: str) -> list[Point]:
        rows = self.conn.execute(
            "SELECT date, value, source FROM series WHERE indicator_id = ? "
            "ORDER BY date ASC",
            (indicator_id,),
        ).fetchall()
        return [Point(date=d, value=json.loads(v), source=s) for d, v, s in rows]

    def latest_values(self) -> dict[str, Any]:
        """各 indicator_id の最新値（derived 計算の入力に使う）。"""
        out: dict[str, Any] = {}
        rows = self.conn.execute(
            "SELECT indicator_id, value FROM series s WHERE date = "
            "(SELECT MAX(date) FROM series WHERE indicator_id = s.indicator_id)"
        ).fetchall()
        for ind_id, value in rows:
            out[ind_id] = json.loads(value)
        return out

    def close(self) -> None:
        self.conn.close()
