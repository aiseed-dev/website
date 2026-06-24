---
slug: embedded
number: "08"
part: "1"
lang: en
title: "Build Embedded — Think in Python, Have Claude Translate"
subtitle: "Software that drives devices can be built with AI too — logic in Python, production in C if needed"
description: Chapter 5's third worked example. Beyond web and office, software that drives devices (embedded) can be built with AI too. Read a sensor, turn a motor, show a display — think the logic in Python, verify it on your desk and on the real device, and have Claude translate it to C if speed or resources demand. Since much only shows up on the real hardware, run build-run-fix fast. This closes the Introduction part; on to Independence.
date: 2026.07.01
label: Introduction 8
title_html: Device software, too,<br>can be <span class="accent">built with AI</span>.
prev_slug: website
prev_title: "Build a Website — In Dialogue with AI"
next_slug: independence
next_title: "Becoming Independent from Microsoft and Google — The Whole Map"
---

# Build Embedded — Think in Python, Have Claude Translate

Chapter 5's third worked example. Beyond web and office, software that drives
**devices (embedded)** can be built with AI too. Read a sensor, turn a motor,
show a display — write the microcontroller software by **thinking in Python and,
if needed, having Claude translate it to C.**

## Think in Python; ship in C if needed

- The production language for embedded is often C / C++. But **thinking the logic
  in Python** is faster and easier to verify
- Run it on your desk (PC) in Python first, then load it onto the real device
  (Raspberry Pi Pico, ESP32, etc.) with **MicroPython**
- If speed or resources are tight, have **Claude translate** the settled logic
  to C (parent series, Chapter 8)

## How

1. Write what you want (threshold check on a sensor value → output) in Python, verify on the PC
2. Load it onto the device with MicroPython and run it
3. Translate to C and flash it if needed
4. Fix while watching it on the real device — this, too, is dialogue

```python
# e.g. spin a fan when temperature crosses a threshold (MicroPython)
from machine import Pin, ADC
temp = ADC(Pin(26)); fan = Pin(15, Pin.OUT)
while True:
    fan.on() if temp.read_u16() > THRESHOLD else fan.off()
```

## Verify on the real device

With embedded, **much only shows up on the real hardware.** So run build-run-fix
fast. Because AI writes quickly, you can repeat that trial any number of times.

## Summary

- Embedded, too, a customer can build with AI
- **Think the logic in Python**, and have Claude translate to C if needed
- **Run it on the real device and fix** — in dialogue

That closes the Introduction part — we saw a customer "build it themselves" with
AI across office, web, and embedded. Next, the **Independence part** replaces
Microsoft 365, Copilot, WordPress, core systems, and GitHub with OSS on your own
side, and breaks free of the vendors.

---

## Related articles

- [Chapter 5: Customers Co-Develop with AI](/en/ai-native-ways/software/customer-codev/)
- [Parent series, Chapter 8: Building Embedded — Think in Python, Have Claude Translate](/en/ai-native-ways/embedded/)
- [Independence, Chapter 2: Lay the Foundation — SQLite and more](/en/ai-native-ways/software/foundation/)
