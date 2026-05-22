/*
 * 同じロジックの C 実装(ESP32 等の実機への移植イメージ)
 *
 * Python の sensor_logic.py を直接翻訳したもの。Claude に
 *   「これを ESP-IDF で動く C に翻訳して」と頼むだけで出てくる。
 * Python 側で完全に検証してからこちらに移すので、ロジックの
 * バグは混入しない。あとはハードウェア依存のピン制御だけ。
 */

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>

// ハードウェア層 (実機では GPIO・I2C・タイマ駆動)
extern float read_temperature_sensor(void);   // -INFINITY なら無応答
extern void  set_heater(bool on);
extern void  trigger_alarm(const char *msg);
extern void  log_event(const char *msg);

#define TARGET                  22.0f
#define HYSTERESIS               1.5f
#define MAX_ON_MINUTES          30
#define FORCED_REST_MINUTES      5
#define SENSOR_TIMEOUT_MINUTES   5

typedef struct {
    bool     heater_on;
    uint8_t  on_run_minutes;
    uint8_t  forced_rest_remaining;
    uint8_t  silent_minutes;
    bool     alarm;
} controller_t;

static controller_t ctrl;

void controller_tick(uint32_t minute) {
    float temp = read_temperature_sensor();
    bool  sensor_ok = !isinf(temp);

    if (!sensor_ok) {
        ctrl.silent_minutes++;
        if (ctrl.silent_minutes >= SENSOR_TIMEOUT_MINUTES) {
            if (ctrl.heater_on || !ctrl.alarm) {
                char buf[80];
                snprintf(buf, sizeof buf,
                         "t=%4u ALARM ヒーター強制 OFF (センサ %u 分無応答)",
                         minute, ctrl.silent_minutes);
                log_event(buf);
                trigger_alarm(buf);
            }
            ctrl.heater_on = false;
            set_heater(false);
            ctrl.alarm = true;
        }
        return;
    }

    if (ctrl.silent_minutes >= SENSOR_TIMEOUT_MINUTES) {
        char buf[80];
        snprintf(buf, sizeof buf, "t=%4u 復旧 (センサ復活)", minute);
        log_event(buf);
    }
    ctrl.silent_minutes = 0;
    ctrl.alarm = false;

    if (ctrl.forced_rest_remaining > 0) {
        ctrl.forced_rest_remaining--;
        if (ctrl.heater_on) {
            ctrl.heater_on = false;
            set_heater(false);
        }
        return;
    }

    if (ctrl.heater_on) {
        ctrl.on_run_minutes++;
        if (ctrl.on_run_minutes >= MAX_ON_MINUTES) {
            ctrl.heater_on = false;
            set_heater(false);
            ctrl.forced_rest_remaining = FORCED_REST_MINUTES;
            ctrl.on_run_minutes = 0;
            return;
        }
        if (temp >= TARGET + HYSTERESIS) {
            ctrl.heater_on = false;
            set_heater(false);
            ctrl.on_run_minutes = 0;
        }
    } else {
        if (temp <= TARGET - HYSTERESIS) {
            ctrl.heater_on = true;
            set_heater(true);
            ctrl.on_run_minutes = 0;
        }
    }
}
