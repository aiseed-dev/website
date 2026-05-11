---
slug: embedded
number: "09"
lang: en
title: "Building Embedded — Think in Python, Have Claude Translate"
subtitle: "Even with hardware, think in Python"
description: Microcontrollers and IoT devices have to be written in C or C++. But design and validation can happen in Python. Run it, verify it in Python, then have Claude translate to C. The hardest part of embedded — proving the logic is correct — gets dramatically easier.
date: 2026.05.02
label: AI Native 09
title_html: Think in <span class="accent">Python</span>.<br>Have <span class="accent">Claude</span> translate.
prev_slug: apps
prev_title: "Building Apps — CLI Tools, Flet Apps, Flutter Apps"
next_slug: ai-delegation
next_title: "Knowing What Work to Hand to AI"
---

# Building Embedded — Think in Python, Have Claude Translate

For those working with embedded systems and microcontrollers.

Hardware constraints mean the final code lives in C or C++, or at lightest in Rust or MicroPython. But **design and validation can happen in Python**. Do design and validation in Python, confirm it works, then translate to C. With this, the hardest part of embedded development — "proving the logic is correct" — becomes dramatically easier.

## What is hard about embedded

Anyone who has written embedded code knows.

- Behavior cannot be checked without flashing the device
- Hardware debugging takes 10x the time of PC debugging
- Even printing a single value requires UART setup
- Memory runs out, buffers overflow, timing slips
- A one-line fix means re-flashing firmware

Logic errors and hardware instability **mix together**. When something doesn't work, you can't tell whether it's the code, the wiring, or the power supply.

This is the single biggest reason embedded development has been slow.

## Think in Python

In a new embedded project, the first thing to write is Python.

Read sensor values, apply a filter, make a decision — instead of writing this on the device, write it first in Python. Prepare sample data as CSV, load it in Python, pass through the filter, output the decision.

```python
# Validate the logic with sample data
import csv

def detect_anomaly(values):
    avg = sum(values) / len(values)
    return any(abs(v - avg) > 3 for v in values[-10:])

with open("sensor_log.csv") as f:
    rows = [float(r["value"]) for r in csv.DictReader(f)]

print("anomaly:", detect_anomaly(rows))
```

This code runs on a PC. Executes in a second. You can plot a graph for visual confirmation. You can change test data and run it many times.

You can prove the logic is correct, separated from the hardware.

## Translation is Claude's job

Once the logic works in Python, translate it to C.

Ask Claude "translate this Python code to C++ that runs on Arduino, with fixed array sizes" and the translation comes back.

```cpp
// Translated C++ for Arduino
bool detectAnomaly(float values[], int size) {
    float sum = 0;
    for (int i = 0; i < size; i++) sum += values[i];
    float avg = sum / size;
    int start = size - 10;
    if (start < 0) start = 0;
    for (int i = start; i < size; i++) {
        if (fabs(values[i] - avg) > 3) return true;
    }
    return false;
}
```

Flash it to the device and run. **Logic is already verified in Python; if it doesn't work on hardware, the cause is on the hardware side.** Debugging gets a direction.

## Choosing the language

The embedded language is determined by hardware and use case.

| Hardware | Language | Use case |
|----------|----------|----------|
| Arduino, AVR | C, C++ | Learning, simple control |
| ESP32, RP2040 | C, C++, MicroPython | IoT, wireless |
| STM32, NXP | C, C++, Rust | Industrial, precise control |
| Raspberry Pi | Python, C++ | Edge AI, image processing |
| Microcontrollers (prototype) | MicroPython | Prototyping, education |

The first choice, when hardware allows, is **MicroPython or Python**. If performance or capacity rules out Python, move to C or Rust.

For a Raspberry Pi class device, the final form is often Python too. **If you can ship Python, no translation needed.**

## MicroPython as a choice

Small microcontrollers like ESP32 or RP2040 can run MicroPython, a subset of Python.

Python code written on a PC transfers almost unchanged to the device. The edit cycle is fast (no compile, transfer in seconds). Debugging feels like PC.

When MicroPython hits its limits — memory, speed, available libraries — translate just that part to C. **You don't have to translate everything.** Keep what can stay in Python.

## Hardware is something Claude can also handle

Schematics, wiring, datasheets — Claude can help interpret these too.

"I want to connect this OLED display module to an ESP32. Tell me the wiring and the code." Pin assignments, library, init code, display code all come back.

If the datasheet is a PDF, extract the text and hand to Claude — "what does register 0x21 of this sensor do?" — and it answers.

**Hardware knowledge is also held by AI.** The era of fighting hardware alone is over.

## Sensor data analysis is also Python

When you can extract data from the embedded device, analysis happens in Python too.

Have it emit CSV or JSON, bring it to a PC, analyze in Python. `pandas` for aggregation, `matplotlib` for graphs, `numpy` for numerics. Claude writes all of it.

"The sensor logs temperature every minute. From this CSV, find the time of day when temperature spiked, and graph it." Code comes back.

**The embedded body runs in C, but everything around it — verification, analysis, visualization — runs in Python and AI.** That is the new shape of embedded development.

## Example: a room temperature monitor

A concrete example.

**Goal**: an ESP32 that measures room temperature and notifies when it exceeds 30 °C.

**Stage 1 (Python on PC)**:

Write the logic in Python. Prepare sample temperature data (CSV) and write the decision logic. Tune thresholds, denoise, set notification conditions — all experimented on a PC.

```python
def should_alert(temps):
    # Alert if the average of the last 5 minutes exceeds 30
    recent = temps[-5:]
    return sum(recent) / len(recent) > 30
```

**Stage 2 (MicroPython on the device)**:

Transfer the Python logic to MicroPython. Since MicroPython is a subset of Python, it runs almost as is. Wire up a real temperature sensor (DHT22, etc.) and run with real data.

**Stage 3 (translate to C if needed)**:

Battery-powered for long durations, tight memory — then translate to C. Ask Claude, the translation comes out.

In many cases, Stage 2 is the end. MicroPython is sufficient.

## Readable in ten years

C has been around for 50 years. It will run for another 50. Python has been around for 30 and will run for another 30.

Embedded knowledge that has been locked into industry-specific languages (old PLC ladder logic, automotive special standards) gets pushed out into Python and C and Markdown. **Move from vendor-specific formats to formats that cross time.**

This is a long game. But you can advance a little every day.

## In numbers

ESP32 temperature-sensor logic development:

- Old way, starting in C++: **2 weeks** (compile + flash + debug)
- New way, validate in Python first, then transfer to MicroPython: **2 days**
- **7x faster**

Re-flash cycle:

- C++ + flash: **~2 minutes**
- MicroPython transfer: **~5 seconds**
- Python simulation: **~0.1 seconds**
- C vs Python: a **1,200x gap**

20-year-old industrial PLC ladder logic, untouchable since the original engineer retired: Claude reads the ladder, translates to Python, documents in Markdown — **1 week**. By hand, half a year or more, with no guarantee even with a veteran engineer.

Sensor data visualization: building a custom web dashboard takes 1 week. With Python's `matplotlib` plus a `plot()` line, then "make this an HTML report" to Claude — practical-quality result in **30 minutes**.

## In summary

Even in embedded, think in Python.

Design and verify in Python, then translate to C if needed. Claude handles the translation. **Time spent fighting hardware decreases, and you focus on the real problem — sensors, logic, operations.**

The nine chapters so far have laid out the AI-native toolset. Python, Markdown, Mermaid, JSON/CSV/YAML, leaving Office, business systems, web, apps, embedded.

The next chapter moves to common practice in advanced form. "Knowing what work to hand to AI" — the judgment of what to delegate and what to keep.

---

## Related

- [Chapter 08: Building Apps — CLI Tools, Flet Apps, Flutter Apps](/en/ai-native-ways/apps/)
- [Chapter 01: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Structural Analysis 15: Security Design for the Mythos Era](/en/insights/security-design/)
