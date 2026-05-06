---
slug: claude-debian-16-python-flutter-other
lang: en
number: "16"
title: Chapter 16 — Python, Flutter, and Other Environments
subtitle: When you need a language, build it up with Claude
description: Python on `uv` as the main line, miniforge alongside for data science and ML. GUI via Flutter/Dart; Rust narrowed to speeding up Python hot spots (PyO3). Other choices (web, CLI) live as a map for when you need them. Working alongside Claude on Debian.
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

### This Book Picks `uv`

For Python package management we standardize on **`uv`** (Astral, written
in Rust). It's 10–100× faster than `pip` + `venv`, drops `requirements.txt`
in favor of `pyproject.toml` + `uv.lock` for **fully reproducible**
projects. It competes with `poetry`; we choose `uv` because it's
**faster and simpler**. Chapters 14 and 15 all assume `uv`.

```bash
# One-time
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### The Project Loop

```bash
# Create
uv init my-project && cd my-project

# Add dependencies (auto-updates pyproject.toml and uv.lock)
uv add requests pandas
uv add --dev pytest ruff

# Run
uv run python -m my_project
uv run pytest

# Move to another machine
git clone <repo> && cd <repo> && uv sync   # ← full reproduction
```

### CLI Tools: `uv tool install`

Python-written CLIs (`ruff`, `httpie`, `pre-commit`, `yt-dlp`, etc.) are
**not project dependencies and live in their own stream**. `uv tool` is the
upgraded successor to `pipx`.

```bash
uv tool install ruff
uv tool install httpie
uv tool install pre-commit

# List and upgrade
uv tool list
uv tool upgrade --all
```

`apt install pipx` works too, but **knowing one tool (uv) keeps the head
lighter**.

### Python Itself, Also Managed by `uv`

`pyenv` is no longer needed.

```bash
uv python install 3.12
uv python install 3.13
uv python list

# Pin Python 3.13 for this project
echo '3.13' > .python-version
uv sync   # installs it if missing
```

### Data Processing

Install pandas, polars, numpy via `uv add` rather than apt — you get the
latest.

- Large CSVs → **polars** (faster than pandas).
- Statistics → scipy, statsmodels.
- Visualization → matplotlib, plotly.

For **GPU deep learning, or scientific stacks involving GDAL / OpenCV /
R / Julia**, `uv` alone is not enough. See the next section,
**"Data Science / ML: Use miniforge."**

### Ask Claude ①: A Modern Python Project Skeleton

> I write Python for [data wrangling / web scraping / GUI / ML / scripting].
> Assuming `uv`, scaffold a project with:
> (1) `pyproject.toml` (dependencies, dev-deps, scripts entry point)
> (2) `.python-version` and `uv.lock`
> (3) configuration for `ruff` and `pytest`
> (4) a minimal `tests/` example
> (5) `README.md` showing `git clone && uv sync && uv run` flow

## Section 2 — Data Science / ML: Use miniforge

`uv` covers 90% of Python projects, but it falls short for **data science
and machine learning**:

- PyTorch + **CUDA / cuDNN**, TensorFlow + GPU
- **R / Julia** integration (rpy2 / PyJulia)
- Non-Python native deps like **GDAL / OpenCV / FFmpeg**
- Heavy scientific stacks: RAPIDS, scikit-image, GeoPandas, PyMC, ...
- Earliest Apple Silicon support

For these, PyPI wheels often aren't enough; the realistic path is to take
**pre-built binaries via conda-forge**. This book installs **miniforge**.

### Why miniforge, Not Anaconda

The Anaconda Distribution installer carries a **commercial-license
restriction** (since 2020, organizations of 200+ are paid; the default
`defaults` channel falls under the same terms). **miniforge avoids all
that**:

- Small installer (~150 MB).
- Default channel pinned to **conda-forge** (community-run, license-clean,
  largest package set).
- Free for both commercial and personal use.

### Installing

```bash
# Debian 13 / 12 (x86_64)
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
  -o ~/miniforge.sh
bash ~/miniforge.sh -b -p ~/miniforge3

# Shell integration (rewrites .bashrc / .zshrc, one-time)
~/miniforge3/bin/conda init bash    # if you use bash
~/miniforge3/bin/conda init zsh     # if you use zsh
```

Open a new terminal.

**Important**: by default, the `base` environment is **auto-activated on
shell startup**. This collides with uv project `.venv`s. Turn it off
right away.

```bash
conda config --set auto_activate_base false
```

Now: "activate a conda env only when you mean to."

### The Loop

```bash
# Create an env (Python version + main libs)
conda create -n ds python=3.12 \
  numpy pandas polars scipy scikit-learn jupyterlab matplotlib seaborn

conda activate ds

# Add later
conda install -c conda-forge gdal opencv

# Export the env (share with the team)
conda env export --from-history > environment.yml

# Reproduce on another PC
conda env create -f environment.yml
```

`--from-history` records **only the packages you explicitly asked for**
(automatic dependencies are excluded). That's the readable form for
team distribution.

### GPU (CUDA)

```bash
conda create -n dl python=3.12 \
  pytorch torchvision pytorch-cuda=12.1 \
  -c pytorch -c nvidia

conda activate dl
python -c "import torch; print(torch.cuda.is_available())"   # expect True
```

The big win: the CUDA toolkit is **scoped inside the conda env**. No more
breaking the system by `apt install`-ing CUDA globally. Different
projects can use different CUDA versions side by side.

### Jupyter Lab

```bash
conda activate ds
jupyter lab --no-browser --port 8888
```

Open `http://localhost:8888/?token=…` in your browser. The conda-forge
build of Jupyter is the most reliable.

### When to Use Which

| Use | Tool |
|------|------|
| Web apps, APIs, CLIs, business scripts | **uv** |
| Data analysis (pandas / polars, CPU-only) | **uv is enough** |
| Machine learning / deep learning (GPU) | **miniforge** |
| Scientific computing (GDAL / OpenCV / R / Julia) | **miniforge** |
| Jupyter-notebook-centric exploration | **miniforge** (conda-forge's jupyterlab + ipykernel are the most stable) |
| When wheels won't build on Apple Silicon | **miniforge** |

**Start projects with uv; bring in miniforge when the problem demands it**.
The two live in different directories (`~/miniforge3/envs/` and
`<project>/.venv/`) so they don't fight. As long as you've turned off
auto-activate, **you can step into either world by being explicit**.

### Ask Claude ②: Stand Up a DS / ML Environment

> My use case is [image classification / NLP / time series / statistical
> analysis], with [GPU / CPU only]. Scaffold an `environment.yml` for
> miniforge with the minimum packages. Show me how to start Jupyter Lab,
> how to combine Python with R if needed, and how to run this without
> conflicting with my existing uv project.

## Section 3 — Flutter / Dart

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

### Ask Claude ③: Flet or Flutter

> I want to build a GUI app for [purpose].
> Compare Flet (Python) and Flutter (Dart) along these axes:
> (1) Learning cost.
> (2) Need for mobile distribution (iOS / Android).
> (3) Performance.
> (4) Magnitude of the AI-completion benefit (Claude / Copilot).
> (5) Long-term maintainability.

## Section 4 — Rust (To Speed Up Python)

Rust is a wonderful language, but in this book we **don't use it
standalone**. Daily scripts, business logic, GUI, web — all of these go
faster, stay easier to maintain, and pair better with AI when written in
Python (with `uv`).

The place we reach for Rust is **"replace a Python hot spot with Rust."**

### You Already Benefit from Rust

Many of the main tools in this book are **written in Rust under the hood**:

| Tool | Implementation | Effect |
|---|---|---|
| **uv** | Rust | 10–100× faster than pip + venv |
| **ruff** | Rust | 10–100× faster than flake8 + black + isort |
| **polars** | Rust | several to ten times faster than pandas DataFrames |
| **pydantic v2** | Rust (core) | data validation an order of magnitude faster |
| **fnm** | Rust | Node.js version management |
| **Zed** | Rust | the editor we adopted in Chapter 13 |

You enjoy Rust without writing it. That is the 2026 reality of where
Rust lives — **Python broad on the surface, Rust fast at the bottom.**

### When You Do Reach for Rust

Profile your Python with `cProfile` or `py-spy`. **If a single function
takes more than half** the running time, that's your Rust candidate.

```bash
# Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

The cleanest way to call Rust from Python is **maturin + PyO3**:

```bash
uv tool install maturin
maturin new --bindings pyo3 my_fastlib
cd my_fastlib
maturin develop   # build and install into the same project's uv venv
```

Now `import my_fastlib` works on the Python side — Rust functions called
as Python functions.

### Use Rust, Don't Write It

- Pick existing Rust-built tools (uv / ruff / polars, etc.).
- Write Rust yourself **only for hot spots that profiling pointed to**.
- Pin behavior with Python tests first, then translate to Rust.
- **Ask Claude to "rewrite this Python function in Rust via maturin/PyO3"** — that prompt works fine.

Don't "learn Rust first, then build something." **Get stuck in Python
first, then drop to Rust** — that's the right order.

### Ask Claude ④: Move a Python Hot Spot to Rust

> I profiled my Python code [paste] with `cProfile`. Function [name]
> accounted for [percentage] of total runtime. Show me, with a minimal
> example, how to rewrite it in Rust via maturin + PyO3, keeping the
> Python-side interface unchanged.

## Section 5 — Databases

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

## Section 6 — The Habit of Switching Environments

### Isolate Per Project

- Python: `uv` (project-local `.venv/`).
- Node: `fnm`.
- Rust: `rustup` toolchains.
- Docker: per-container.

**Don't install directly into the system Python or system npm.** Each
project gets its own isolated environment, so when one breaks, the rest
don't go with it.

### Throw Away Environments You Don't Use

Periodically, prune projects and language environments you don't use.
This is the biggest cause of disk bloat.

```bash
# Wipe all node_modules in one shot
find ~/Projects -name node_modules -type d -exec rm -rf {} +

# uv cache hygiene (per-project .venv lives in the project itself)
uv cache prune
du -sh ~/.cache/uv ~/.local/share/uv

# Flatpak runtime cleanup
flatpak uninstall --unused -y
```

### Ask Claude ⑤: Environment Diet

> My home directory is consuming the following: [output of `du -sh`].
> Sort what's safe to delete, what must not be deleted, and the caches I should clean periodically.
> Also draft a shell script for periodic cleanup.

## Section 7 — How to Read the Map

The environments listed in this chapter can all be revisited when you need them. **It is enough if you remember the table of contents below.**

| Use | First choice | Second choice |
| --- | --- | --- |
| Python project management | **uv** | — |
| Data science / ML / GPU | **miniforge** | — |
| Notebook-centric exploration | **miniforge** | uv + jupyter also viable |
| Data wrangling, scripting | Python (uv) | — |
| GUI app | Flet / Flutter | — |
| Web frontend | TypeScript + Vite | — |
| Backend / API | Python (uv + FastAPI) / Node.js / Go | — |
| CLI tool | Rust / Go | Python |
| Systems-adjacent, performance | Rust | Go |
| Database | SQLite | PostgreSQL |
| Isolated environment | Docker | — |

The biggest goal of Chapter 16 is **to have this table in your head**. Mastery of any one technology can wait until you need it, then proceed with Claude.

## Summary

What you did in this chapter:

1. Standardized the Python stack on `uv` (project + tools + Python versions).
2. Brought in **miniforge** for data science and ML, with a clean coexistence story alongside uv.
3. Got the position of Flutter / Dart.
4. Decided that Rust isn't used standalone — only to **speed up Python hot spots** (maturin + PyO3).
5. How to choose between SQLite and PostgreSQL.
6. Built the habit of isolating and pruning environments.

This closes Part 4. **Your Debian is now a development foundation you can put your hands on at any time.** When something you want to build appears, you can have its language environment ready in 30 minutes.

In Part 5 (Chapters 17–20), we move into **operation and growth**. Updates, troubles, growing the environment, engaging with the community — the practice of running the daily life and keeping the environment alive over time.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
