"""データモデル（核） — 全指標を単一の構造で表す。

仕様 §2 を Python に落としたもの。`Point` は (date, value, source) の観測 1 件。
`Indicator` はカタログの 1 レコード。新指標 = 1 レコード追加（コード変更不要）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# kind: 指標の種別（§2）
KINDS = {"price", "flow", "clock", "stock", "constant"}

# acquisition: 取得方法（§2）
ACQUISITIONS = {"auto", "derived", "manual"}

# cadence: 取得頻度（§4）
CADENCES = {"daily", "monthly", "quarterly", "event"}


@dataclass(frozen=True)
class Point:
    """series に追記される観測 1 件。value は数値または状態文字列。"""

    date: str  # ISO 8601 (YYYY-MM-DD)
    value: Any  # float | int | str（状態指標は文字列）
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {"date": self.date, "value": self.value, "source": self.source}


@dataclass
class Indicator:
    """カタログの 1 レコード。"""

    id: str
    name_ja: str
    name_en: str
    chokepoint: str
    kind: str
    acquisition: str
    cadence: str
    unit: str
    source: str
    note: str = ""
    threshold: dict[str, Any] | None = None
    derived: str | None = None  # DERIVED レジストリのキー
    target_date: str | None = None  # clock(derived) の期日
    series: list[Point] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Indicator":
        assert d["kind"] in KINDS, f"unknown kind: {d['kind']}"
        assert d["acquisition"] in ACQUISITIONS, f"unknown acquisition: {d['acquisition']}"
        assert d["cadence"] in CADENCES, f"unknown cadence: {d['cadence']}"
        series = [Point(**p) for p in d.get("series", [])]
        return cls(
            id=d["id"],
            name_ja=d["name_ja"],
            name_en=d["name_en"],
            chokepoint=d["chokepoint"],
            kind=d["kind"],
            acquisition=d["acquisition"],
            cadence=d["cadence"],
            unit=d["unit"],
            source=d.get("source", ""),
            note=d.get("note", ""),
            threshold=d.get("threshold"),
            derived=d.get("derived"),
            target_date=d.get("target_date"),
            series=series,
        )

    def latest(self) -> Point | None:
        return self.series[-1] if self.series else None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "id": self.id,
            "name_ja": self.name_ja,
            "name_en": self.name_en,
            "chokepoint": self.chokepoint,
            "kind": self.kind,
            "acquisition": self.acquisition,
            "cadence": self.cadence,
            "unit": self.unit,
            "source": self.source,
            "note": self.note,
            "threshold": self.threshold,
            "series": [p.to_dict() for p in self.series],
        }
        if self.target_date:
            out["target_date"] = self.target_date
        return out
