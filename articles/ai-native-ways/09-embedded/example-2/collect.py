#!/usr/bin/env python3
"""1 週間ぶんの「センサーデータ」を生成して SQLite に投入する。

実機(ESP32 + DHT22 + 土壌湿度センサ)のデータを模した、温室の
1 週間ぶんの計測ログ ── 5 分間隔、3 種類のセンサー ──
合計 (7 days × 24 hours × 12 / hour) × 3 sensors = 6,048 件。

実機がまだ無くても、ここで処理パイプラインを完成させてから
ハードを準備すればいい(章 09 の主張)。
"""
from __future__ import annotations

import math
import random
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

DB = Path(__file__).parent / "out" / "sensor.db"
DB.parent.mkdir(exist_ok=True)


def init_db():
    DB.unlink(missing_ok=True)
    c = sqlite3.connect(DB)
    c.execute("""
    CREATE TABLE measurements (
        id INTEGER PRIMARY KEY,
        sensor TEXT NOT NULL,
        value REAL NOT NULL,
        unit TEXT NOT NULL,
        ts TIMESTAMP NOT NULL
    )""")
    c.execute("CREATE INDEX idx_sensor_ts ON measurements (sensor, ts)")
    c.commit()
    return c


def main():
    c = init_db()
    start = datetime(2026, 4, 25, 0, 0, 0)
    rows = []
    for minute in range(0, 7 * 24 * 60, 5):  # 5 分間隔、1 週間
        t = start + timedelta(minutes=minute)
        # 日内サイクル: 6:00 で最低、14:00 で最高
        h = t.hour + t.minute / 60
        diurnal_temp = 20 + 8 * math.sin((h - 8) * math.pi / 12)
        diurnal_humid = 70 - 25 * math.sin((h - 8) * math.pi / 12)
        # ランダムノイズ
        temp = round(diurnal_temp + random.gauss(0, 0.4), 2)
        humid = round(max(0, min(100, diurnal_humid + random.gauss(0, 2.5))), 2)
        soil = round(35 + random.gauss(0, 1.5) - minute * 0.001, 2)  # じわっと乾燥
        ts = t.isoformat(timespec="seconds")
        rows.extend([
            ("temperature", temp, "°C", ts),
            ("humidity", humid, "%", ts),
            ("soil_moisture", soil, "%", ts),
        ])

    t0 = time.perf_counter()
    c.executemany(
        "INSERT INTO measurements (sensor, value, unit, ts) VALUES (?, ?, ?, ?)", rows
    )
    c.commit()
    elapsed = time.perf_counter() - t0

    n = c.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]
    by_s = c.execute("SELECT sensor, COUNT(*) FROM measurements GROUP BY sensor").fetchall()
    print(f"=== センサーデータ投入 ===")
    print(f"  期間          : 2026-04-25 〜 2026-05-01 (7 日)")
    print(f"  サンプリング  : 5 分間隔 × 3 センサ")
    print(f"  投入件数      : {n:,} 件 (DB: {DB.stat().st_size/1024:.1f} KB)")
    print(f"  投入時間      : {elapsed*1000:.0f} ms")
    for s, count in by_s:
        print(f"    {s:18s} {count} 件")


if __name__ == "__main__":
    main()
