# cf-publish (Flet)

A small, no-terminal desktop GUI for **designers** to publish a local folder to
[Cloudflare Pages](https://pages.cloudflare.com/). Pick a folder, name the
project, hit **Publish**. No `wrangler`, no `npm`, no command line.

This is the **Flet** entry in a 3-way trial (Rust CLI vs Flet GUI vs Flutter
GUI). The point of the Flet version is reusing the repo's existing Python deploy
logic (`httpx` + `blake3`) while getting a Flutter-quality UI.

## What it does

- Implements the same half-official **Direct Upload API** that `wrangler` uses
  under the hood — ported from `tools/cloudflare_pages_deploy.py` in this repo.
  (Logic is **copied** into `deploy_core.py`, not imported across the repo.)
- Walks the chosen folder (skipping dotfiles / dot-directories), hashes each
  file with `blake3(base64(bytes) + ext)[:32]`, uploads only the assets
  Cloudflare is missing, then creates a deployment and shows the resulting URL.

## Files

| File | Purpose |
|---|---|
| `main.py` | Flet UI (declarative `@ft.component` + hooks, 1.0 Beta / 0.85 line). |
| `deploy_core.py` | UI-agnostic deploy logic. Raises `DeployError` (never `sys.exit`); reports progress via an `on_progress(str)` callback. |
| `pyproject.toml` / `requirements.txt` | Pinned deps: `flet[all]>=0.80,<0.86`, `httpx`, `blake3`. |

## UI

- **Site / project name** — required text field.
- **Public folder** — `FilePicker` directory chooser; the chosen path is shown
  and remembered in `~/.config/cloudflare/cf-publish-flet.json`.
- **Branch** — dropdown, `main (production)` (default) or `preview`.
- **Publish** — disabled with a spinner while a deploy runs; long work runs off
  the UI thread via `page.run_thread`.
- **Log** — scrollable area that appends progress lines.
- **On success** — the deployment URL with **copy** and **open** buttons.
- **Settings (gear)** — dialog to enter `CLOUDFLARE_API_TOKEN` and
  `CLOUDFLARE_ACCOUNT_ID`, saved to `~/.config/cloudflare/pages.env`
  (`KEY=VALUE`, `chmod 600`). Opens automatically on first run if creds are
  missing.

Credentials load order: **environment variables first**, then
`~/.config/cloudflare/pages.env`.

## Requirements

- Python 3.11+
- A Cloudflare API token with **Cloudflare Pages: Edit** permission, and your
  account ID. (Enter them in the gear dialog, or export
  `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID`.)

## Install (uv — preferred)

```bash
cd apps/cf-publish/flet
uv venv
uv pip install -r requirements.txt   # or: uv pip install -e .
```

(With `pip`: `python3.11 -m venv .venv && ./.venv/bin/pip install -r requirements.txt`.)

## Run (dev)

```bash
uv run flet run        # opens the desktop window
# or:  ./.venv/bin/flet run
```

## Build (distribution)

```bash
flet build macos       # -> build/macos/ .app bundle
flet build linux       # -> build/linux/ bundle
```

> **Flutter SDK required.** `flet run` (desktop) and `flet build` need the
> Flutter SDK and a Flet desktop client. The container this app was scaffolded
> in did **not** have Flutter installed, so the GUI was **not** actually
> launched here — only `import` resolution and `py_compile` of both modules
> were verified (plus the pure-Python deploy logic was exercised offline). Run
> the dev/build commands above on a machine with Flutter to see the window.

## Notes / fallback

This relies on Cloudflare's Direct Upload API, which is semi-official. If
Cloudflare changes it and uploads start failing, fall back to `wrangler` or the
Pages Git integration.
