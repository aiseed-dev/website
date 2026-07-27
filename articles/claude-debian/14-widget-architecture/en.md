---
slug: claude-debian-14-widget-architecture
lang: en
number: "14"
title: Chapter 14 — Implementing the Widget Architecture
subtitle: Build your own app from small, reusable parts
description: Learn the Widget architecture — designing apps as a composition of small independent parts — together with Claude. Take a small clock app as the subject and implement Widget decomposition, state management, layout, and reuse.
date: 2026.04.23
label: Claude × Debian 14
prev_slug: claude-debian-13-dev-tools
prev_title: Chapter 13 — Building the Development Tools
next_slug: claude-debian-15-claude-development
next_title: Chapter 15 — Development with Claude in Practice
cta_label: Learn with Claude
cta_title: A big feature is the sum of small parts.
cta_text: Build a single Widget as an independent small unit. Combine them. Once this pattern is in your hands, every UI is within reach.
cta_btn1_text: Continue to Chapter 15
cta_btn1_link: /en/claude-debian/15-claude-development/
cta_btn2_text: Back to Chapter 13
cta_btn2_link: /en/claude-debian/13-dev-tools/
---

## What Is a Widget

A Widget is **a small UI part that runs independently**. A button, an input field, a list, a card, a clock, a graph — each one carries its own state and appearance, and works when separated from the rest.

A large app is built by composing Widgets. Stacked hierarchically, they form the whole. React's Component, Flutter's Widget, Vue's Component, Flet's Control — the names differ, but the way of thinking is the same.

In this chapter, we take a small clock app as the subject and internalize the Widget architecture. **Claude writes the code itself.** What you acquire is **the way of thinking about design** and **how to instruct Claude**.

## Section 1 — The Subject: a Simple Dashboard

We will build an app like this.

```
+-------------------------------+
|   Clock (13:42:30)            |
+-------------------------------+
|   Today's schedule (3 items)  |
|   - 10:00 Meeting             |
|   - 14:00 Submit document     |
|   - 18:00 Dinner              |
+-------------------------------+
|   Weather (Sunny, 18°C)       |
+-------------------------------+
```

A structure of three stacked Widgets. Each one runs independently and has its own data source.

### Language and Framework

This book recommends **Python + Flet** (Flutter-based, callable from Python).
No Dart / Flutter setup required, runs as fast as possible.

For Python package management we use **`uv`** (covered in Chapter 16).
It's 10–100× faster than `pip` + `venv`, and **projects are far more
reproducible**. Instead of `requirements.txt`, use `pyproject.toml` plus
`uv.lock`.

```bash
# Install uv (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create the project and add Flet
mkdir ~/Projects/my-dashboard && cd ~/Projects/my-dashboard
uv init
uv add flet
```

This produces `pyproject.toml`, `uv.lock`, and `.venv/` automatically.
Moving to another PC takes just `git clone && uv sync` — **two lines
for full reproduction**.

## Section 2 — Decompose into Widgets

### The First Step in Design

Before you start writing, **decide which Widgets to split into**.

- **ClockWidget.** Updates the current time every second.
- **ScheduleWidget.** Shows today's schedule.
- **WeatherWidget.** Shows current weather.
- **DashboardApp.** The parent that lays the three out.

Principles for splitting:
1. **One Widget has one concern** (clock is clock, weather is weather).
2. **Don't pass data directly between Widgets** (only through the parent).
3. **Keep the API a Widget exposes minimal** (initialize and update, that's it).

### Ask Claude ①: Discuss the Decomposition

> I'm building a dashboard app in Flet that lays out a clock, a schedule, and weather.
> I'm thinking of splitting it into three Widgets:
> - ClockWidget: updates the time every second.
> - ScheduleWidget: today's schedule list.
> - WeatherWidget: current weather.
>
> Tell me whether this split is reasonable, and whether you can suggest improvements.
> Make a table for each Widget covering its responsibility (what it knows, what it shows, how it talks to the outside).

Through dialogue with Claude, pin down the design. **Don't write code at this stage.** Spending 30 minutes to an hour on design alone is worth it.

## Section 3 — The First Widget: the Clock

### How to Instruct Claude to Write It

Have Claude write the first Widget.

> Please write a ClockWidget in Flet.
>
> Requirements:
> - Display the current time in `HH:MM:SS` format.
> - Update every second.
> - Large, centered text.
> - Implemented as an independent class (separated from the main function).
>
> Provide the full code in a single file, plus a small sample showing ClockWidget running standalone.
> Assume Python 3.11 or later, latest Flet.

Read the code Claude returns. **You don't have to understand all of it.** Just verify three things.

1. The class is named `ClockWidget`.
2. The time-update logic lives inside the class.
3. The main function uses that class in what looks like a runnable sample.

### Run It

```bash
cd ~/Projects/my-dashboard
# save Claude's code as clock_widget.py
python3 clock_widget.py
```

If a window opens and the clock ticks, you've succeeded. If not, paste the error to Claude as-is.

### Ask Claude ②: Handling the Error

> When I ran the following code, I got an error:
> ```
> [code]
> ```
> ```
> [the full error message]
> ```
>
> Tell me the cause and how to fix it. Show the full corrected code.

## Section 4 — Composing Widgets

### Build the Parent Widget

Build the parent that lays out the three Widgets.

> Please write a DashboardApp that displays ClockWidget, ScheduleWidget, and WeatherWidget stacked vertically.
> Assume each Widget already exists in its own file (clock_widget.py, schedule_widget.py, weather_widget.py).
>
> Requirements:
> - Each Widget is an independent class.
> - DashboardApp only imports them and lays them out.
> - The screen size adapts to the window width.
> - Vertical scrolling is enabled.

This is the heart of the Widget architecture: **the parent only places children**. It doesn't reach into the contents of the children.

### ScheduleWidget and WeatherWidget

In the same flow, have Claude write the remaining two. Schedule starts with hard-coded entries; Weather starts with dummy data.

**The point: build the smallest version that runs first, then connect to real data.** Connecting straight to an external API makes debugging painful.

## Section 5 — Entry to State Management

### State Inside a Widget

ClockWidget holds the state "current time." In Flet you handle it like this.

```python
# Conceptual example written by Claude
class ClockWidget(ft.UserControl):
    def build(self):
        self.time_text = ft.Text(size=48)
        return self.time_text

    def did_mount(self):
        # start a timer that updates every second
        ...
```

### Passing Data from Parent to Child

When you want to pass a "city name" from the parent to WeatherWidget.

```python
class WeatherWidget(ft.UserControl):
    def __init__(self, city: str):
        super().__init__()
        self.city = city
```

The parent initializes it as `WeatherWidget(city="Tokyo")`.

### Ask Claude ③: A State-Management Question

> Tell me about state management in Flet:
> (1) State a Widget should hold internally (the clock's current time, the latest weather data).
> (2) Things the parent should pass to the child (display city, theme color).
> (3) Handling state across parent and child (settings several Widgets share).
>
> Show beginner-friendly, simple guidance, with the dashboard app as the example.
> Avoid overly complex state-management libraries.

## Section 6 — Polish the Look

### Colors, Fonts, Spacing

Once it works, polish the look. Instruct Claude.

> Polish the look of the current DashboardApp under the following principles:
> - Dark theme (background #1a1a1a, foreground #e0e0e0).
> - 16 px gap between Widgets.
> - Rounded card style (border_radius=12).
> - The clock is large (72 pt), the rest medium.
> - A Japanese-aware font (Noto Sans JP).
>
> Don't rewrite the whole code; add a constants section that gathers the styles.

**Polishing the look raises the readability of the code at the same time.** Gathering colors and sizes into constants makes future changes easier.

## Section 7 — Reusing a Widget

### An Application: a TimerWidget

You have a ClockWidget; you can build a "countdown timer" with the same structure.

> Please build a TimerWidget that counts down from a specified number of minutes, with the same structure as ClockWidget.
> Where the structures share something, create a base class BaseTimeWidget and derive both from it.

This is where **code consolidation** happens. When several Widgets share the same structure, gather the shared parts — that's how software grows.

### An Important "Don't"

**Don't over-consolidate.** Abstracting too early makes future change harder.

- The same code shows up twice: still copy-paste.
- A third occurrence: consider consolidating.
- A fourth, with hints of more: consolidate.

You build this sense in dialogue with Claude.

### Ask Claude ④: Avoiding Over-Design

> I am building Widgets. Right now ClockWidget and TimerWidget have similar code.
> Which is appropriate at this stage:
> (1) Leave them as two independent Widgets.
> (2) Extract the shared part into a function.
> (3) Build a base class BaseTimeWidget and derive from it.
> (4) Rebuild around an event-driven architecture.
>
> Decide based on the current code [paste] and the outlook ahead [I might also build a Claude dialogue UI].

## Section 8 — The "Way of Thinking" Earned in This Chapter

If, beyond the code, the following stays with you, the chapter has succeeded.

1. **Decide the split before you start writing.** The boundaries between Widgets are themselves the quality of the design.
2. **First, build the smallest thing that runs.** Adding features comes later. Empty cards are fine to start.
3. **The parent only places children.** Don't reach into the children.
4. **Keep state inside the Widget that holds it.** Don't drag state across parent and child.
5. **Consolidate from the third occurrence on.** Premature abstraction is the breeding ground of bugs.

This applies on the Web, on mobile, and in GUI — all of them. We came in through Python/Flet, but the way of thinking transfers directly to React and Flutter.

## Summary

What you did in this chapter:

1. Picked a small dashboard app as the subject.
2. Discussed Widget decomposition with Claude.
3. Had Claude write each Widget, one at a time, and made it run.
4. Composed the parent to form the whole.
5. Acquired the minimum of state management.
6. Polished the look and got a sense for reuse (consolidation).

What you hold now:
- A working dashboard app (Python / Flet).
- Design notes for Widget decomposition.
- The way of thinking: "build small and compose."

In Chapter 15, we move into the practice of using Claude Code to **grow this app into something more practical**. Connecting to real data, error handling, tests, build and distribution — you experience the first lap of full-fledged app development.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
