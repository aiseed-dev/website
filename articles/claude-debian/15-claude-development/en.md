---
slug: claude-debian-15-claude-development
lang: en
number: "15"
title: Chapter 15 — Development with Claude in Practice
subtitle: Grow a small app into something connected to real data and worth using every day
description: Connect the Chapter 14 dashboard to real data, write tests, handle errors, and make it distributable. Use Claude Code to walk the lap from "it just runs" to "an app you can use."
date: 2026.04.23
label: Claude × Debian 15
prev_slug: claude-debian-14-widget-architecture
prev_title: Chapter 14 — Implementing the Widget Architecture
next_slug: claude-debian-16-python-flutter-other
next_title: Chapter 16 — Python, Flutter, and Other Environments
cta_label: Learn with Claude
cta_title: Just running isn't usable.
cta_text: Connect to real data, handle failures, add tests, make it distributable. That is the distance between "runs" and "usable." Walk it together with Claude.
cta_btn1_text: Continue to Chapter 16
cta_btn1_link: /en/claude-debian/16-python-flutter-other/
cta_btn2_text: Back to Chapter 14
cta_btn2_link: /en/claude-debian/14-widget-architecture/
---

## A Lap of a Real App

The dashboard you built in Chapter 14 runs, but it is still a "toy." It isn't connected to real data; it crashes if an error happens; it has no tests; you can't distribute it.

In Chapter 15, we grow that toy into **an app you can use every day**. Walk the basic development cycle once around, with Claude Code.

## Section 1 — Real-World Use of Claude Code

### Enter the Project and Launch

```bash
cd ~/Projects/my-dashboard
claude
```

Once it's up, tell Claude Code the state of the project.

> This directory holds the Flet-based dashboard app I built in Chapter 14.
> Today I want to do the following:
> (1) Connect WeatherWidget to real data (Open-Meteo API).
> (2) Show errors in the UI on failure.
> (3) Add tests.
> (4) README and a launcher script.
>
> Read the current file layout and propose where to start.

Claude Code reads the files, gets a sense of the current state, and returns a plan.

### Review Each Change as It Comes

Claude Code can rewrite many files in a sweep. But **don't auto-approve**.

- Confirm each file change one by one.
- If the intent isn't clear, ask back.
- Always confirm "the reasoning for why."

This is the same posture as the answer to the Copilot problem ([Chapter 12, "The Copilot Problem"](/en/blog/copilot-correct-looking-but-wrong/)). The final responsibility for code an AI wrote is borne by the human.

## Section 2 — Connecting to Real Data

### Picking a Weather API

There are several free weather APIs to choose from.

- **Open-Meteo.** No registration; commercial use OK; latitude / longitude based.
- **OpenWeatherMap.** Registration required; free tier available.
- **JMA (Japan Meteorological Agency) JSON.** Official data; Japan only.

This book recommends **Open-Meteo**. No registration; you can try it immediately.

### Have Claude Implement It

> Connect WeatherWidget to the Open-Meteo API.
>
> Requirements:
> - Latitude / longitude (default: Tokyo 35.6762, 139.6503) can be passed in from the parent.
> - Refresh every 30 minutes.
> - On fetch failure, show the error in the UI (do not crash).
> - Use the standard library (urllib) or httpx instead of requests.
>
> Don't break the existing class structure.

Review what comes back. In particular, look closely at **error handling**. Network failure, API outage, JSON parsing failure — all three will happen.

## Section 3 — Working with Errors

### Three Layers

Errors are handled at three layers.

**Layer 1: defensive programming.**
Catch expected errors (network failure, API format change) with `try / except`.

**Layer 2: what you show the user.**
Show "fetch failed" in the UI and offer a retry button. Don't crash.

**Layer 3: write to the log.**
For the developer (you) to be able to follow the cause, write to a file.

```python
# Standard Python logging
import logging
from pathlib import Path

log_dir = Path.home() / ".local" / "share" / "my-dashboard"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_dir / "app.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

Common pitfall: passing a literal `'~/...'` to `logging.basicConfig`
**won't expand the tilde** — it creates a directory literally named `~`.
Use `Path.home()` to resolve it first.

### Ask Claude ①: Reviewing Error Handling

> In my WeatherWidget [paste code], please verify that the following error cases are covered:
> (1) Network disconnection.
> (2) A 500 error from the API.
> (3) A change in the JSON format of the API response.
> (4) Timeout (no response within 10 seconds).
> (5) The response is fine, but the forecast data is empty.
>
> For cases that aren't covered, show the smallest code change to handle them.

## Section 4 — Writing Tests

### The Smallest Unit of a Test

Use `pytest`. This book installs it via **`uv add --dev pytest`** so it
gets recorded as a per-project dev dependency in `pyproject.toml`.
`apt install python3-pytest` is for the system Python and isn't used in
real projects.

```python
# tests/test_clock_widget.py
def test_format_time():
    from my_dashboard.clock_widget import format_time
    assert format_time(13, 42, 30) == "13:42:30"
    assert format_time(0, 0, 0) == "00:00:00"
```

### Have Claude Write Them

> Please write pytest unit tests for ClockWidget's time-format function `format_time` and WeatherWidget's JSON-parse function `parse_weather`.
>
> - Happy path: 3 cases each.
> - Sad path: invalid input, empty, extreme values — 3 cases each.
> - Tests are independent (no dependencies on each other).
> - Mocked (no network access).
>
> Match the existing code's structure; get the import paths right.

### Run the Tests

```bash
uv run pytest tests/
```

Prefixing with `uv run` uses the pytest in your project's `.venv/`.

Confirm they all pass. If something is red, judge whether the code is wrong or the test is wrong.

### Tests Are Living Things

Tests aren't a "write once, done." Add tests every time you add a feature. This habit is what gives you confidence in your code over time.

## Section 5 — Move Configuration Outside

### From Hard-Coded to a Config File

Take the constants written into the app (latitude / longitude, refresh interval, API endpoint) and move them out into an external config file.

```toml
# config.toml
[weather]
latitude = 35.6762
longitude = 139.6503
refresh_interval_minutes = 30

[schedule]
source = "~/Documents/schedule.ics"

[theme]
dark = true
accent_color = "#4a7c59"
```

It can be read with Python's standard `tomllib` (3.11+).

### Ask Claude ②: Designing the Config

> List the items in my dashboard app's code that could be moved to external configuration.
> Give me an example of `config.toml` and the smallest code to load it.
> Assume that when the user edits `config.toml`, restarting the app picks up the change.

## Section 6 — Make It Distributable

### Dependencies Are Already in `pyproject.toml`

Anything added with `uv add` is recorded in `pyproject.toml`, and `uv.lock`
**fully pins versions**. No `requirements.txt` is needed.

```toml
# pyproject.toml (auto-updated by uv add)
[project]
name = "my-dashboard"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "flet>=0.20",
    "httpx>=0.27",
]

[dependency-groups]
dev = ["pytest>=8.0"]
```

Moving to another machine takes just two commands: `git clone && uv sync`.

### Launching

You usually don't need a shell wrapper; `uv run` runs it directly.

```bash
# In the project root
uv run python -m my_dashboard
```

If you want a single command name, install your project as a tool:

```bash
# Install your own project as an editable tool
uv tool install --editable .
# Then from anywhere
my-dashboard
```

Define an entry point in `pyproject.toml` and `uv tool install` puts the
command in `~/.local/bin/`.

```toml
[project.scripts]
my-dashboard = "my_dashboard.__main__:main"
```

### Desktop Entry

So you can launch it from the application menu.

```ini
# ~/.local/share/applications/my-dashboard.desktop
[Desktop Entry]
Type=Application
Name=My Dashboard
Exec=my-dashboard
Icon=/home/you/Projects/my-dashboard/assets/icon.png
Categories=Utility;
```

### Ask Claude ③: Finishing for Distribution

> I want to make my dashboard usable in three tiers:
> (1) For my own daily launch (desktop entry, one click from the menu).
> (2) Portable to another PC (git clone + 1 command and it runs).
> (3) Distributable to a friend (with documented steps).
>
> Create the files needed at each tier (README, requirements, desktop entry, install.sh, etc.).

## Section 7 — Grow It with Git

### Granularity of a Commit

One commit per feature add or fix. The message is "what" and "why" in one line.

```
feat(weather): add Open-Meteo API connection
fix(clock): fix display bug at midnight
test: add edge-case tests for format_time
refactor(config): move constants to config.toml
docs: add launch instructions to README
```

### How to Use Branches

For a small personal project, starting on `main` only is fine. Cut a branch only when you're trying a large change.

```bash
git checkout -b experiment/dark-theme
# try things
# if it works, merge to main; if not, throw it away
```

## Section 8 — Look Back at the Distance from "Runs" to "Usable"

From the "toy" of Chapter 14 to the "real app" of Chapter 15, here is what changed.

| Aspect | Toy (Ch 14) | Real app (Ch 15) |
| --- | --- | --- |
| Data | hard-coded | real API |
| Errors | crash | UI message + log |
| Tests | none | unit tests |
| Settings | inside the code | external file |
| Launch | python file.py | desktop entry |
| Distribution | impossible | works after git clone |

Put as numbers, the line count from "just runs" to "usable" more than doubles. **Walking that distance honestly is what engineering is.** AI helps at every step.

## Section 9 — What to Watch for in Development with Claude

### Slice It Small

Asking "do all of it at once" makes Claude return a wall of code. You can't read it through, and approval mistakes happen.

**Slice the instructions small.** One purpose (connect to weather API, add error handling, write tests) per dialogue.

### Don't Go Beyond What You Understand

If a function in Claude's reply is one you can't understand at all, that is a signal that you've stepped beyond **the range you can judge**.

In that case, ask Claude: "Explain each line of this code. What it does, and why it's done that way — for a beginner." You can't put code you don't understand into production.

### Ask Claude ④: Self-Evaluation

> I have walked the lap from Chapter 14 to Chapter 15 in this chapter.
> Looking at the current code [paste the final version], please evaluate:
> (1) Maintainability (will the future me, six months from now, read it and understand?).
> (2) Extensibility (is it easy to add a new Widget?).
> (3) Robustness (does it stay up under unexpected errors?).
> (4) Test coverage (are the important behaviors covered?).
> (5) Distribution quality (will it run on another PC?).
>
> Give a score out of 10 for each, and list the top three improvements in priority order.

## Summary

What you did in this chapter:

1. Launched Claude Code in the project and established review-as-you-go.
2. Connected to real data (Open-Meteo API).
3. Wired up errors at three layers (defensive, UI, log).
4. Wrote unit tests with pytest.
5. Externalized configuration into `config.toml`.
6. Made it launchable via a desktop entry.
7. Set the rhythm of growing it with Git.

What you hold now:
- A self-built dashboard you can use every day.
- A sound pattern of collaboration with Claude Code.
- A lap's worth of experience of engineering, from "runs" to "usable."

In Chapter 16, we widen the view beyond Python and Flet — to Flutter / Dart, Node.js, Rust, Docker. Get to a state where, when you need them, you can put them together with Claude.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
