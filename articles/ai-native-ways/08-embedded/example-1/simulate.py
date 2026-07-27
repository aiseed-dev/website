#!/usr/bin/env python3
"""温度コントローラを実機抜きでシミュレーション + プロット。

実機に焼いて 1 サイクル試すには 2 分。Python シミュレーションは
0.1 秒。1,000 倍以上の差。
"""
from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path

from sensor_logic import HeaterController

random.seed(42)
HERE = Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def simulate_temperature(minutes: int, heater_states: list[bool]) -> list[float]:
    """簡単な熱モデル: ヒーター ON で +0.4℃/分、OFF で -0.15℃/分、外気は変動。"""
    temps = []
    t = 18.0  # 開始温度
    for m in range(minutes):
        # 外気の影響(夜間にかけて少し下がる)
        outside_pull = -0.05 if 0 <= m % 240 < 180 else -0.10
        warming = 0.4 if m < len(heater_states) and heater_states[m] else 0.0
        cooling = -0.15 if not (m < len(heater_states) and heater_states[m]) else 0.0
        t += warming + cooling + outside_pull + random.gauss(0, 0.05)
        temps.append(round(t, 2))
    return temps


def main():
    minutes = 240  # 4 時間ぶんを 0.X 秒で回す

    ctrl = HeaterController()
    heater_log = []
    temp_log = [18.0]
    sensor_dropouts = set(range(60, 67))  # 60〜66 分目だけセンサ無応答

    t0 = time.perf_counter()
    for m in range(minutes):
        # 直前の温度を入力。最初は 18℃。
        prev = temp_log[-1]
        sensor = None if m in sensor_dropouts else prev
        ctrl.tick(m, sensor)
        heater_log.append(ctrl.heater_on)
        # 次の分の温度を熱モデルで進める
        warming = 0.4 if ctrl.heater_on else 0.0
        cooling = -0.15 if not ctrl.heater_on else 0.0
        outside = -0.05
        next_t = prev + warming + cooling + outside + random.gauss(0, 0.05)
        temp_log.append(round(next_t, 2))
    elapsed = time.perf_counter() - t0

    # 結果書き出し
    summary = {
        "minutes_simulated": minutes,
        "elapsed_seconds": round(elapsed, 4),
        "heater_on_count": sum(heater_log),
        "alarm_triggered": ctrl.alarm,
        "events": ctrl.events,
        "temp_min": min(temp_log),
        "temp_max": max(temp_log),
        "temp_avg": round(sum(temp_log) / len(temp_log), 2),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    # CSV ログ
    with (OUT / "trace.csv").open("w") as f:
        f.write("minute,temp,heater\n")
        for i, (t, h) in enumerate(zip(temp_log[1:], heater_log)):
            f.write(f"{i},{t},{int(h)}\n")

    # ASCII プロット(温度推移)
    chart_lines = ["温度推移 (240 分, 縦軸 16〜26℃):"]
    LO, HI, ROWS = 16, 26, 12
    for r in range(ROWS, 0, -1):
        thresh = LO + (HI - LO) * r / ROWS
        line = f"  {thresh:5.1f}℃ │ "
        for t, h in zip(temp_log[1:], heater_log):
            if t >= thresh:
                line += "█" if h else "▓"
            else:
                line += " "
        chart_lines.append(line)
    chart_lines.append("        └" + "─" * minutes)
    chart_lines.append("        0" + " " * 58 + "60" + " " * 58 + "120"
                       + " " * 57 + "180" + " " * 57 + "240 (分)")
    chart = "\n".join(chart_lines)
    (OUT / "ascii-chart.txt").write_text(chart)

    print(f"\n=== シミュレーション結果 ===")
    print(f"  シミュレーション時間: 240 分(4 時間)")
    print(f"  実行時間: {elapsed*1000:.1f} ms")
    print(f"  ヒーター ON 分数: {summary['heater_on_count']} / {minutes}")
    print(f"  温度範囲: {summary['temp_min']}〜{summary['temp_max']}℃ (平均 {summary['temp_avg']}℃)")
    print(f"  発生イベント: {len(ctrl.events)} 件")
    print()
    for e in ctrl.events[:8]:
        print(f"    {e}")
    if len(ctrl.events) > 8:
        print(f"    ... ({len(ctrl.events) - 8} 件)")
    print()
    print(f"  → {OUT / 'summary.json'}")
    print(f"  → {OUT / 'trace.csv'}")
    print(f"  → {OUT / 'ascii-chart.txt'}")


if __name__ == "__main__":
    main()
