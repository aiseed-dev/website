# Server Edition — Learning Debian with Claude

**Subtitle: Own your infrastructure with Claude, in a world without a GUI**

A sub-series of the parent series "Learning Debian with Claude" (`../`). The
parent series is primarily about the desktop (taking back your own desk); this
sub-series is about servers (owning your own infrastructure). The premise:
**a home server, with your data managed by you** — the body (apps and data)
lives on your machine at home, in your own databases (SQLite / PostgreSQL),
not in someone else's cloud; VPSes and clouds serve only as practice rigs
and as the "publishing entrance." Eleven chapters walk from driving a
screenless Debian over SSH, through hardening, running databases and your
own apps, publishing them, to protecting your data. No containers — apps
run as "directory + venv + systemd," isolated by dedicated users,
permission design, and systemd sandboxing.

Server administration is all text — logs, configs, errors — which makes it the
domain where the "learning with Claude" method works best. As in the parent
series, each chapter ends with "Ask Claude" boxes the reader fills in with
their own situation. The JA README is [`README.md`](README.md).

## Status

**All 11 chapters published** (JA + EN, 22 files).

## Layout

```
articles/claude-debian/server/
├── README.md           ── JA version
├── README.en.md        ── this file
└── NN-slug/            ── renumbered from 01 within the sub-series
    ├── ja.md
    └── en.md
```

Built by the same book pipeline as the parent series (the `BOOK_SUBSERIES`
registry in `tools/build_article.py`). Templates and frontmatter schema are
shared with the parent series; EN files set `lang: en` explicitly. Slugs take
the form `claude-debian-server-NN-…`; the URL stem strips that prefix.

## URLs

| Source | Output | URL |
|---|---|---|
| `01-what-is-a-server/ja.md` | `html/claude-debian/server/01-what-is-a-server/index.html` | `/claude-debian/server/01-what-is-a-server/` |
| `01-what-is-a-server/en.md` | `html/en/claude-debian/server/01-what-is-a-server/index.html` | `/en/claude-debian/server/01-what-is-a-server/` |
| (sub-series TOC, generated) | `html/claude-debian/server/index.html` | `/claude-debian/server/` |
| (sub-series TOC, generated) | `html/en/claude-debian/server/index.html` | `/en/claude-debian/server/` |

## Chapter labels

The frontmatter `label` field uses:

- JA: `Claude × Debian サーバー編 NN`
- EN: `Claude × Debian Server NN`

Breadcrumbs and the sidebar TOC display the combined series title
`Claudeと一緒に学ぶDebian — サーバー編` / `Learning Debian with Claude — Server Edition`.

## prev / next chain

Closed **within** the sub-series. Chapter 01 leaves `prev_slug:` empty; the
final chapter (11) leaves `next_slug:` empty. No bridging into the parent
series (pointing the final chapter's CTA buttons at the parent series is fine).

## Relationship to the parent index

- The parent index (`/claude-debian/`) announces this sub-series with a hero
  card at the top (generated).
- The parent chapter list does **not** include the sub-series chapters.
- The sub-series index (`/claude-debian/server/`) opens with a back-link to
  the parent index (generated).

## Chapters

| # | slug (stem) | Title |
|---|---|---|
| 01 | `01-what-is-a-server` | Chapter 1 — What Is a Server |
| 02 | `02-where-to-run` | Chapter 2 — Where to Put Your Server |
| 03 | `03-minimal-install` | Chapter 3 — The Minimal Install |
| 04 | `04-ssh` | Chapter 4 — SSH, the Front Door |
| 05 | `05-security-basics` | Chapter 5 — The Basics of Defense |
| 06 | `06-systemd-services` | Chapter 6 — The Service as a Unit |
| 07 | `07-database` | Chapter 7 — The Database as a Foundation |
| 08 | `08-fastapi` | Chapter 8 — Running Your Own App |
| 09 | `09-publishing` | Chapter 9 — Opening Up to the Outside World |
| 10 | `10-backup` | Chapter 10 — Protecting Your Data |
| 11 | `11-operations` | Chapter 11 — Growing Your Server |

Slugs are final; do not change them, for URL stability.

## Build

```bash
python3 tools/build_article.py --all                                        # everything
python3 tools/build_article.py articles/claude-debian/server/01-what-is-a-server/ja.md  # one chapter
```
