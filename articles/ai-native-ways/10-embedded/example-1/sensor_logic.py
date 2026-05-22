#!/usr/bin/env python3
"""温室の温度制御ロジック ── まず Python で書いて、シミュレーションで詰める。

仕様:
- 温度センサが 1 分ごとに値を返す(℃, 浮動小数点)
- 設定: 目標温度 22℃、ヒステリシス ±1.5℃
- ヒーターを ON/OFF する
- 連続稼働時間が 30 分を超えたら必ず 5 分休む(過熱防止)
- 5 分間センサ無応答ならフェイルセーフでヒーター OFF + 警報

これを実機(ESP32 + MicroPython)に移植する前に、ここで完全に検証する。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HeaterController:
    target: float = 22.0
    hysteresis: float = 1.5
    max_on_minutes: int = 30
    forced_rest_minutes: int = 5
    sensor_timeout_minutes: int = 5

    # state
    heater_on: bool = False
    on_run_minutes: int = 0
    forced_rest_remaining: int = 0
    silent_minutes: int = 0
    alarm: bool = False

    # log
    events: list[str] = field(default_factory=list)

    def tick(self, t_minute: int, sensor_temp: Optional[float]) -> None:
        # フェイルセーフ: センサ無応答
        if sensor_temp is None:
            self.silent_minutes += 1
            if self.silent_minutes >= self.sensor_timeout_minutes:
                if self.heater_on or not self.alarm:
                    self.events.append(f"t={t_minute:>4} ALARM ヒーター強制 OFF (センサ {self.silent_minutes} 分無応答)")
                self.heater_on = False
                self.alarm = True
            return
        else:
            if self.silent_minutes >= self.sensor_timeout_minutes:
                self.events.append(f"t={t_minute:>4} 復旧 (センサ復活)")
            self.silent_minutes = 0
            self.alarm = False

        # 強制休止中
        if self.forced_rest_remaining > 0:
            self.forced_rest_remaining -= 1
            if self.heater_on:
                self.heater_on = False
                self.events.append(f"t={t_minute:>4} 強制 OFF (連続 {self.max_on_minutes} 分到達)")
            return

        # 通常制御
        if self.heater_on:
            self.on_run_minutes += 1
            if self.on_run_minutes >= self.max_on_minutes:
                self.heater_on = False
                self.forced_rest_remaining = self.forced_rest_minutes
                self.on_run_minutes = 0
                self.events.append(f"t={t_minute:>4} 強制 OFF + {self.forced_rest_minutes} 分休止開始")
                return
            if sensor_temp >= self.target + self.hysteresis:
                self.heater_on = False
                self.on_run_minutes = 0
                self.events.append(f"t={t_minute:>4} OFF ({sensor_temp:.1f}℃ ≥ {self.target + self.hysteresis})")
        else:
            if sensor_temp <= self.target - self.hysteresis:
                self.heater_on = True
                self.on_run_minutes = 0
                self.events.append(f"t={t_minute:>4} ON  ({sensor_temp:.1f}℃ ≤ {self.target - self.hysteresis})")
