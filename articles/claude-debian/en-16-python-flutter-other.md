---
slug: claude-debian-16-python-flutter-other
lang: en
number: "16"
title: Chapter 16 — Python, Flutter, and Other Environments
subtitle: When you need a language, build it up with Claude
description: How to install environments beyond Python / Flet — Flutter / Dart, Node.js, Rust, Go, Docker — and the knack of putting them together with Claude. Not for memorizing — as a map you can come back to when you need it.
date: 2026.04.23
label: Claude × Debian 16
prev_slug: claude-debian-15-claude-development
prev_title: Chapter 15 — Development with Claude in Practice
next_slug: claude-debian-17-updates-maintenance
next_title: Chapter 17 — Updates and Maintenance
cta_label: Learn with Claude
cta_title: Keep it as a map.
cta_text: You don't need to memorize all of this right now. Keep this chapter as a map you can come back to when you need it. With Claude, you can travel anywhere on the map.
cta_btn1_text: Continue to Part 5 / Chapter 17
cta_btn1_link: /en/claude-debian/17-updates-maintenance/
cta_btn2_text: Back to Chapter 15
cta_btn2_link: /en/claude-debian/15-claude-development/
---

## How to Read This Chapter

Chapter 16 functions as **a map**. Don't put your hands on every one of these right now. Just sort out where each language and environment sits, how to install it on Debian, and the knack of putting it together with Claude.

When you need it, come back, read the relevant section, and open Claude Code. **Don't make "memorizing" the goal.**

## Section 1 — Python (Going Deeper)

### Managing Multiple Virtual Environments

If you'll run multiple Python projects on one PC, the modern combination is `uv` or `pipx` rather than `venv` alone.

```bash
# uv (a fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Per project
cd ~/Projects/some-project
uv venv
uv pip install requests
```

### pipx: CLI Tools in Isolated Environments

For Python-written CLI tools (`pre-commit`, `httpie`, `ansible`), install with `pipx`. It doesn't pollute the system Python.

```bash
sudo apt install pipx
pipx install httpie
pipx install pre-commit
```

### Data Processing in Japanese

Install pandas, polars, numpy via pip rather than apt — you'll get the latest.

- Large CSVs → polars (faster than pandas).
- Statistics → scipy, statsmodels.
- Visualization → matplotlib, plotly.

### Ask Claude ①: A Modern Python Stack

> I write Python for [data wrangling / web scraping / GUI / ML / scripting].
> Tell me the recommended toolchain as of 2026 (package manager, editor extensions, type checker, formatter, test framework).
> Include the reasoning for which of pip, poetry, uv, and rye to pick.

## Section 2 — Flutter / Dart

### From Flet to Flutter

We used Flet in Chapters 14 and 15, but Flet runs Flutter inside. **If you want to build a serious cross-platform app, Flutter directly** is also an option.

### Installing Flutter

On Debian, follow the official steps.

```bash
# Required dependencies
sudo apt install git curl unzip xz-utils clang cmake ninja-build pkg-config libgtk-3-dev

# Get the Flutter SDK
git clone https://github.com/flutter/flutter.git -b stable ~/flutter
export PATH="$PATH:$HOME/flutter/bin"

# Verify
flutter doctor
```

### What Flutter Offers

- One codebase outputs to all of Linux, Windows, macOS, iOS, Android, and Web.
- Rendering uses Skia / Impeller; it doesn't depend on OS-native UI.
- Dart language (notation similar to TypeScript).
- **Best fit for people who want to build mobile apps.**

### Ask Claude ②: Flet or Flutter

> I want to build a GUI app for [purpose].
> Compare Flet (Python) and Flutter (Dart) along these axes:
> (1) Learning cost.
> (2) Need for mobile distribution (iOS / Android).
> (3) Performance.
> (4) Magnitude of the AI-completion benefit (Claude / Copilot).
> (5) Long-term maintainability.

## Section 3 — Node.js / TypeScript

### Version Management with `nvm` or `fnm`

```bash
# fnm (Rust-based, fast)
curl -fsSL https://fnm.vercel.app/install | bash

# Install LTS
fnm install --lts
fnm use lts-latest
```

### TypeScript Setup

```bash
npm init -y
npm install -D typescript @types/node
npx tsc --init
```

### Major Tools by Use

- Web frontend → React / Vue / Svelte.
- Backend → Express / Hono / NestJS.
- Scripts → tsx (run TypeScript instantly).
- Build → Vite, esbuild.

### Ask Claude ③: JS / TS in 2026

> I want to write [a browser SPA / a Node.js backend / scripts / Electron].
> As of 2026, which framework / tools should I pick?
> Include the reasons, and the older choices to avoid.

## Section 4 — Rust

### Install

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

`rustup`, `cargo`, and `rustc` are placed under your home directory.

### What Rust Suits

- **Systems-adjacent.** Filesystems, network tools, CLIs.
- **Performance-critical.** Image processing, data pipelines.
- **Concurrency.** Servers and backends.
- **Safety-critical.** Strong memory safety and type safety.

### What Rust Doesn't Suit

- **Small scripts.** Python is enough.
- **Quick prototypes.** Rust compile times are long.
- **Exploratory work where requirements churn.** A type-strict language gives up flexibility.

### Ask Claude ④: Should I Pick Up Rust

> What I want to build is [purpose]. Should I learn Rust to build it, or build it in another language? Make the call.
> Be concrete about the learning cost (hours per week, for how many weeks) and the trade-off of what you get.

## Section 5 — Go

### Install

```bash
sudo apt install golang-go
# Or get the latest from the official site
```

### What Go Suits

- **CLI tools.** Easy to ship as a single file.
- **Servers.** Simple and fast.
- **Cloud-native (Kubernetes-style)** systems.

Faster to learn than Rust, sturdier than Python. The midpoint of "good-enough performance and good-enough safety."

## Section 6 — Docker

### Install

```bash
# From Docker's official repository
sudo apt install docker.io docker-compose

# Add yourself to the docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### When Docker Is Useful

- **Try a tool with complex dependencies.** PostgreSQL, Redis, MinIO.
- **Experiment without breaking your environment.** Drop the image and you're back where you started.
- **Run something close to production.** Reduce the gap between dev and prod.

### Ask Claude ⑤: First Steps with Docker

> I want to run [what you want to try] with Docker. Show a minimal docker-compose.yml example and the steps from launch → verify → stop.
> Cover the points beginners get stuck on (ports, volumes, networks), with workarounds.

## Section 7 — Databases

### SQLite

Comes with Debian. A single-file DB; enough for most personal use.

```bash
# Get going
sqlite3 ~/data/my.db
```

From Python, the standard library's `sqlite3`.

### PostgreSQL

If you want to go full-scale, PostgreSQL.

```bash
sudo apt install postgresql
sudo -u postgres createuser $USER
sudo -u postgres createdb $USER
psql
```

### Which to Choose

- Single user, want it all in one file → **SQLite**.
- Multi-user, multi-app, production → **PostgreSQL**.

As discussed in [Chapter 15, "Security Design in the Mythos Era"](/en/insights/security-design/), the strongest design is **not putting a DB into production**. For personal projects, SQLite often suffices.

## Section 8 — The Habit of Switching Environments

### Isolate Per Project

- Python: `uv venv` or `venv`.
- Node: `fnm`.
- Rust: `rustup` toolchains.
- Docker: per-container.

**Don't install directly into the system Python or system npm.** Each project gets its own isolated environment, so when one breaks, the rest don't go with it.

### Throw Away Environments You Don't Use

Periodically, prune projects and language environments you don't use. This is the biggest cause of disk bloat.

```bash
# Wipe all node_modules in one shot
find ~/Projects -name node_modules -type d -exec rm -rf {} +

# Inventory Python virtualenvs
du -sh ~/envs/*
```

### Ask Claude ⑥: Environment Diet

> My home directory is consuming the following: [output of `du -sh`].
> Sort what's safe to delete, what must not be deleted, and the caches I should clean periodically.
> Also draft a shell script for periodic cleanup.

## Section 9 — How to Read the Map

The environments listed in this chapter can all be revisited when you need them. **It is enough if you remember the table of contents below.**

| Use | First choice | Second choice |
| --- | --- | --- |
| Data wrangling, scripting | Python | — |
| GUI app | Flet / Flutter | — |
| Web frontend | TypeScript + Vite | — |
| Backend / API | Python / Node.js / Go | — |
| CLI tool | Rust / Go | Python |
| Systems-adjacent, performance | Rust | Go |
| Database | SQLite | PostgreSQL |
| Isolated environment | Docker | — |

The biggest goal of Chapter 16 is **to have this table in your head**. Mastery of any one technology can wait until you need it, then proceed with Claude.

## Summary

What you did in this chapter:

1. Sorted out the modern Python stack (uv, pipx).
2. Got the position of Flutter / Dart.
3. Updated the 2026 view of Node.js / TypeScript.
4. Confirmed where Rust and Go each shine.
5. Sorted out where Docker fits.
6. How to choose between SQLite and PostgreSQL.
7. Built the habit of isolating and pruning environments.

This closes Part 4. **Your Debian is now a development foundation you can put your hands on at any time.** When something you want to build appears, you can have its language environment ready in 30 minutes.

In Part 5 (Chapters 17–20), we move into **operation and growth**. Updates, troubles, growing the environment, engaging with the community — the practice of running the daily life and keeping the environment alive over time.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
