---
slug: embedded
number: "08"
part: "1"
title: 組み込みを作る ── Python で考え、Claude に翻訳させる
subtitle: 機器を動かすソフトも AI と作れる ── ロジックは Python、本番は必要なら C へ
description: 1-05の三つ目の実例。Web やオフィスだけでなく、機器を動かすソフト(組み込み)も AI と作れる。センサーを読み、モーターを回し、表示する ── ロジックは Python で考えて手元と実機で確かめ、速度や資源が厳しければ Claude に C へ翻訳させる。実機でしか分からないことが多いから、作って・動かして・直すを速く回す。これで導入編を終え、自立編へ。
date: 2026.07.01
label: Introduction 8
title_html: 機器を動かすソフトも、<br><span class="accent">AI と作れる</span>。
prev_slug: website
prev_title: "Webサイトを作る ── AI と対話して"
next_slug: independence
next_title: "Microsoft と Google から自立する ── 全体像と対応表"
---

# 組み込みを作る ── Python で考え、Claude に翻訳させる

1-05の三つ目の実例。Web やオフィスだけでなく、**機器を動かすソフト(組み
込み)** も、AI と作れる。センサーを読み、モーターを回し、表示する ── マイコン
のソフトを、**Python で考えて、必要なら Claude に C へ翻訳させる**。

## 考えるのは Python、本番は必要なら C

- 組み込みの本番言語は C / C++ が多い。だが、**ロジックは Python で考える**
  ほうが速く、確かめやすい
- まず手元(PC)で Python で動かし、次に実機(Raspberry Pi Pico・ESP32 など)に
  **MicroPython** で載せる
- 速度や資源が厳しければ、確定したロジックを **Claude に C へ翻訳させる**
  (親シリーズ第8章)

## 進め方

1. やりたいこと(センサー値でしきい値判定 → 出力)を Python で書き、PC で確かめる
2. 実機に MicroPython で載せて動かす
3. 必要なら C へ翻訳して焼く
4. 実機で挙動を見ながら直す ── ここも対話

```python
# 例: 温度がしきい値を超えたらファンを回す(MicroPython)
from machine import Pin, ADC
temp = ADC(Pin(26)); fan = Pin(15, Pin.OUT)
while True:
    fan.on() if temp.read_u16() > THRESHOLD else fan.off()
```

## 実機で確かめる

組み込みは、**実機でしか分からないこと**が多い。だから、作って・動かして・
直すを速く回す。AI が速く書くから、この試行を何度でも繰り返せる。

## まとめ

- 組み込みも、顧客が AI と作れる
- **ロジックは Python で考え**、必要なら Claude が C へ翻訳
- **実機で動かして直す** ── 対話で

導入編はここまで ── 顧客が AI と組んで「自分で作れる」ことを、オフィス・Web・
組み込みで見た。次の **自立編**では、Microsoft 365・Copilot・WordPress・基幹
システム・GitHub を OSS で自分の側に置き換え、ベンダーから自立する。

---

## 関連記事

- [1-05: 顧客がAIと協働して開発する時代](/ai-native-ways/software/customer-codev/)
- [親シリーズ第8章: 組み込みを作る ── Pythonで考え、Claudeに翻訳させる](/ai-native-ways/embedded/)
- [2-02: 土台を据える ── PostgreSQL ほか](/ai-native-ways/software/foundation/)
