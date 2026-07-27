SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

OUT := out

.PHONY: all simulate test compile-c clean

all: simulate test

simulate:
	@mkdir -p $(OUT)
	@python3 simulate.py

test:
	@echo
	@echo "=== ユニットテスト(ヒステリシス境界) ==="
	@python3 -c "from sensor_logic import HeaterController; \
c = HeaterController(); \
c.tick(0, 18.0); assert c.heater_on, 'should turn ON below target-hysteresis'; \
print('  ✓ 18℃ で ON'); \
c.tick(1, 23.6); assert not c.heater_on, 'should turn OFF above target+hysteresis'; \
print('  ✓ 23.6℃ で OFF'); \
c.tick(2, 22.0); assert not c.heater_on, 'should stay OFF in dead-band'; \
print('  ✓ 22℃ では状態維持'); \
c2 = HeaterController(); \
[c2.tick(i, None) for i in range(6)]; assert c2.alarm, 'sensor timeout should trigger alarm'; \
print('  ✓ センサ 5 分無応答でアラーム'); \
print('  4 件すべて pass')"

compile-c:
	@echo
	@echo "=== C コードのコンパイル(ロジック層のみ、HAL なしで構文チェック) ==="
	@echo "extern void set_heater(int on){} extern void trigger_alarm(const char*m){} extern void log_event(const char*m){} extern float read_temperature_sensor(void){return 0;} int main(){return 0;}" > $(OUT)/_stub.c
	@gcc -Wall -O2 -c sensor_logic.c -o $(OUT)/sensor_logic.o
	@gcc -Wall $(OUT)/sensor_logic.o $(OUT)/_stub.c -o $(OUT)/sensor_test 2>&1 | tail -3
	@printf "  ✓ コンパイル成功 (%s bytes)\n" "$$(stat -c%s $(OUT)/sensor_logic.o)"
	@rm -f $(OUT)/_stub.c

clean:
	rm -rf $(OUT)
