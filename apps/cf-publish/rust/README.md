# cf-publish (Rust)

A small single-binary CLI that deploys a local folder to **Cloudflare Pages**
using the same half-public *Direct Upload* API that `wrangler` drives — with
**no npm and no wrangler** dependency.

This is the Rust entry in a 3-way trial (Rust CLI vs Flet GUI vs Flutter GUI).
The selling point versus the Python reference
(`tools/cloudflare_pages_deploy.py`) is the output: one self-contained binary
you can copy to a mac/linux box and run, no interpreter or virtualenv required.

## Build

```sh
cargo build --release
```

The binary lands at `target/release/cf-publish`. The release profile strips
symbols and uses LTO, and `reqwest` is configured with `rustls-tls` (no OpenSSL
system dependency), so the result is a single, essentially static-ish binary.

## Usage

```sh
export CLOUDFLARE_API_TOKEN=...    # token with "Cloudflare Pages: Edit"
export CLOUDFLARE_ACCOUNT_ID=...   # account id from the dashboard

cf-publish ./public --project my-site
# first deploy creates the project automatically; pass --no-create to opt out
cf-publish ./public --project my-site --branch preview   # preview deploy
```

Credentials are read from the environment first, then from a `KEY=VALUE` file
at `~/.config/cloudflare/pages.env` (environment wins on conflict).

On success the deployment URL is printed to **stdout** (progress goes to
stderr), so it is easy to capture in scripts:

```sh
url=$(cf-publish ./public --project my-site)
```

### Options

| Argument        | Meaning                                              |
| --------------- | ---------------------------------------------------- |
| `directory`     | Public directory whose contents become the site.     |
| `--project`     | Pages project name (required).                        |
| `--branch`      | Branch; `main` = production, else a preview URL.      |
| `--no-create`   | Error instead of creating a missing project.         |

## Behavior

Mirrors the canonical Python tool:

1. Collect files under `directory`, skipping dotfiles and dot-directories;
   error if any file exceeds 25 MiB.
2. Per-file hash = `blake3(base64(bytes) ++ ext)` truncated to 32 hex chars
   (the wrangler scheme).
3. Resolve / create the project, fetch an upload JWT.
4. `check-missing` → upload only missing assets (batched ~500 files / ~30 MB)
   → `upsert-hashes`.
5. Create the deployment with the manifest as multipart form data; print the
   resulting URL.

## Reuse

Deploy logic lives in `src/pages.rs` as a library-style function
`deploy(dir, project, branch, create) -> anyhow::Result<String>` that returns
the URL and never calls `process::exit`, so a future GUI (Tauri/egui) can call
it directly.

## Status

Compiled and `--help`-verified, but **not** tested against the live Cloudflare
API — there are no Cloudflare credentials in CI. The HTTP request shapes are
modelled directly on the working Python reference.
