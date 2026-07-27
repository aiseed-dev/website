#!/usr/bin/env python3
"""SQLite のセンサーデータを集計してグラフ + Markdown レポートを出す。"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# 日本語フォントを優先(Noto Sans CJK JP, IPAexGothic)
matplotlib.rcParams["font.family"] = [
    "Noto Sans CJK JP", "IPAexGothic", "Noto Sans JP",
    "Hiragino Sans", "Yu Gothic", "DejaVu Sans",
]
matplotlib.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).parent
DB = HERE / "out" / "sensor.db"
OUT = HERE / "out"


def fetch(sensor: str):
    c = sqlite3.connect(DB)
    rows = c.execute(
        "SELECT ts, value FROM measurements WHERE sensor = ? ORDER BY ts", (sensor,)
    ).fetchall()
    return [r[0] for r in rows], [r[1] for r in rows]


def sensor_stats(sensor: str):
    c = sqlite3.connect(DB)
    r = c.execute(
        "SELECT MIN(value), MAX(value), AVG(value), COUNT(*) FROM measurements WHERE sensor = ?",
        (sensor,),
    ).fetchone()
    return {"min": r[0], "max": r[1], "avg": r[2], "n": r[3]}


def hourly_avg(sensor: str):
    c = sqlite3.connect(DB)
    rows = c.execute("""
        SELECT strftime('%Y-%m-%d %H:00', ts) AS hour, AVG(value)
        FROM measurements WHERE sensor = ? GROUP BY hour ORDER BY hour
    """, (sensor,)).fetchall()
    return [r[0] for r in rows], [r[1] for r in rows]


def main():
    from datetime import datetime
    sensors = [("temperature", "°C", "tab:red"),
               ("humidity",    "%",   "tab:blue"),
               ("soil_moisture","%",  "tab:green")]

    fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
    summary = {}
    for ax, (s, unit, color) in zip(axes, sensors):
        ts, vals = fetch(s)
        x = [datetime.fromisoformat(t) for t in ts]
        ax.plot(x, vals, color=color, linewidth=0.7, alpha=0.4)
        # 1 時間ごとの平均線も重ねる
        hts, hvals = hourly_avg(s)
        hx = [datetime.fromisoformat(h.replace(" ", "T")) for h in hts]
        ax.plot(hx, hvals, color=color, linewidth=2, alpha=0.9, label="hourly avg")
        ax.set_ylabel(f"{s} ({unit})")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
        ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))
        summary[s] = sensor_stats(s)

    plt.suptitle("温室センサー 1 週間ログ (2026-04-25 〜 05-01)")
    plt.tight_layout()
    plt.savefig(OUT / "sensor.png", dpi=120, bbox_inches="tight")

    # Markdown レポート
    md = ["# 温室センサー週次レポート\n",
          "期間: 2026-04-25 〜 2026-05-01(5 分間隔、3 センサ)\n",
          "## 統計\n",
          "| センサ | 最小 | 平均 | 最大 | 件数 |",
          "|--------|------|------|------|------|"]
    for s, unit, _ in sensors:
        st = summary[s]
        md.append(f"| {s} ({unit}) | {st['min']:.1f} | {st['avg']:.1f} | {st['max']:.1f} | {st['n']:,} |")
    md.append("\n## グラフ\n")
    md.append("![sensor](sensor.png)\n")
    md.append("\n## 観察(自動)\n")
    t = summary["temperature"]
    h = summary["humidity"]
    sm = summary["soil_moisture"]
    if t["max"] - t["min"] > 8:
        md.append(f"- 温度の日内変動が **{t['max']-t['min']:.1f}℃** ── 大きい。換気またはシェード検討。")
    if sm["max"] - sm["min"] > 5:
        md.append(f"- 土壌水分が **{sm['max']:.1f}% → {sm['min']:.1f}%** に低下 ── 灌水が必要。")
    if h["avg"] > 70:
        md.append(f"- 湿度平均 **{h['avg']:.1f}%** ── 高湿、病害リスク注意。")

    (OUT / "report.md").write_text("\n".join(md) + "\n")
    print("\n=== レポート生成 ===")
    print(f"  → {OUT / 'sensor.png'}  ({(OUT / 'sensor.png').stat().st_size/1024:.1f} KB)")
    print(f"  → {OUT / 'report.md'}   ({(OUT / 'report.md').stat().st_size} B)")
    print()
    for s, unit, _ in sensors:
        st = summary[s]
        print(f"  {s:18s} min {st['min']:5.1f} {unit:2s}  avg {st['avg']:5.1f}  max {st['max']:5.1f}  n={st['n']}")


if __name__ == "__main__":
    main()
