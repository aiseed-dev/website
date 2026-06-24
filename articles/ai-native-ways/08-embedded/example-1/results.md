# 計測結果 — 第 09 章 example-1

実行環境: Linux 6.18 / Python 3.x / gcc 13

## シミュレーション(主目的)

```
=== シミュレーション結果 ===
  シミュレーション時間: 240 分(4 時間)
  実行時間: 0.3 ms
  ヒーター ON 分数: 94 / 240
  温度範囲: 18.0〜23.84℃ (平均 21.87℃)
  発生イベント: 20 件
```

| 比較 | サイクル時間 |
|------|-------------|
| 実機 (C + ESP32 書き込み) | 約 **2 分** |
| 実機 (MicroPython 転送) | 約 **5 秒** |
| シミュレーション (このスクリプト) | **0.3 ms** |
| 実機 / シミュレーション | **約 400,000 倍** |

## イベントログ(`out/summary.json` 抜粋)

```
t=   0 ON  (18.0℃ ≤ 20.5)
t=  16 OFF (23.6℃ ≥ 23.5)
t=  32 ON  (20.4℃ ≤ 20.5)
t=  42 OFF (23.7℃ ≥ 23.5)
t=  59 ON  (20.5℃ ≤ 20.5)
t=  64 ALARM ヒーター強制 OFF (センサ 5 分無応答)
t=  67 復旧 (センサ復活)
t=  74 ON  (20.4℃ ≤ 20.5)
...
```

仕様通りに動いている:

- **ヒステリシス**: 20.5℃で ON、23.5℃で OFF(目標 22 ±1.5)
- **フェイルセーフ**: センサ 5 分無応答で強制 OFF + ALARM
- **復旧**: センサが復活すると通常制御に戻る
- **過熱防止**: 連続 30 分稼働で強制 5 分休憩(本シミュではトリガしない範囲)

## ユニットテスト

```
=== ユニットテスト(ヒステリシス境界) ===
  ✓ 18℃ で ON
  ✓ 23.6℃ で OFF
  ✓ 22℃ では状態維持
  ✓ センサ 5 分無応答でアラーム
  4 件すべて pass
```

実機でテストすると、4 件のテストにそれぞれ 30 分(温度を変える時間)。
合計 **2 時間以上**。Python では **数 ms**。

## C への翻訳(`sensor_logic.c`)

```c
#define TARGET                  22.0f
#define HYSTERESIS               1.5f
#define MAX_ON_MINUTES          30

void controller_tick(uint32_t minute) {
    float temp = read_temperature_sensor();
    bool sensor_ok = !isinf(temp);

    if (!sensor_ok) {
        ctrl.silent_minutes++;
        if (ctrl.silent_minutes >= SENSOR_TIMEOUT_MINUTES) {
            ctrl.heater_on = false;
            set_heater(false);
            trigger_alarm("...");
        }
        return;
    }
    ...
}
```

**閾値定数も状態遷移も Python 版と完全一致**。
`make compile-c` で gcc でコンパイル通ることを確認:

```
=== C コードのコンパイル(ロジック層のみ、HAL なしで構文チェック) ===
  ✓ コンパイル成功 (3640 bytes)
```

実機 (ESP32) では `read_temperature_sensor()` `set_heater()` `trigger_alarm()`
の 3 関数を ESP-IDF で実装するだけ。**ロジック本体は触らない**。

## 実機への移行手順(参考)

1. Python でロジック完成 ✓
2. ユニットテスト 4 件 pass ✓
3. シミュレーションで 4 時間ぶんの動作確認 ✓
4. Claude に「ESP-IDF で動く C に翻訳して」 → `sensor_logic.c`
5. ハードウェア依存の HAL 関数 (3 個) を ESP-IDF で書く
6. `idf.py build flash` で ESP32 に焼く
7. 実機で 1 時間動作確認 → デプロイ

実機を触るのは **最後の 30 分だけ**。残りはすべて開発機の上で完結する。

## 再現手順

```bash
make clean && make all        # シミュレーション + テスト
make compile-c                # C コードがコンパイル通る確認
```
