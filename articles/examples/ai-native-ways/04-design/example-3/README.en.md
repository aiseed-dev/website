# Example 3 — A business card, two ways

The Chapter 4 claim — **with text, AI, and a tiny script, you can produce
work that competes with specialized design tools** — demonstrated on
the smallest print item there is: a **business card**.

## Which chapter claim this maps to

> You don't need to open Word, Illustrator, or a dedicated design app to
> produce print-ready output from a text source. With AI in the loop,
> even layout tweaks become natural-language conversations.

Business cards are the most dimensionally demanding print item
(91 × 55mm at 9pt body text). If it works here, larger items (flyers,
postcards, envelope-printing) work in the same framework.

## What this does

A single `card-data.json` produces the same PDF via two paths:

```
       card-data.json (name, title, contact)
              │
       ┌──────┴──────┐
       ▼             ▼
  business_card.py   business-card{.html,.css}
  (ReportLab)         (HTML + Print CSS)
       │                   │
       ▼                   ▼
  91×55mm 1-up PDF    Open in browser → Ctrl+P → Save as PDF
  A4 10-up tile PDF   (or WeasyPrint for automation)
```

| Path | Output |
|---|---|
| **A. Python (ReportLab)** | `out/business-card-python.pdf` (1 card) + `out/business-card-sheet-python.pdf` (A4, 10-up) |
| **B. HTML + CSS** | `out/business-card-html.pdf` (1 card) + `out/business-card-sheet-html.pdf` (A4, 10-up) |

`make all` produces all four.

## Why two paths

- **A (Python)**: scale use cases — generate 100 cards for a team in one
  go, pull data from a database, fully automate. Code is around 100 lines.
- **B (HTML)**: visible immediately in a browser, easy CSS tweaking,
  accessible to designers who don't program. In production the browser's
  "Save as PDF" closes the loop (WeasyPrint just automates that step).

**Both paths produce identical PDFs at identical dimensions** — that is
the methodology's core (Chapter 4, "Building business material that
keeps its structure").

## Layout

```
example-3/
├── README.md  / README.en.md       Documentation
├── card-data.json                  Shared data (name, title, contact)
├── business_card.py                Path A: ReportLab → PDF
├── business-card.html              Path B: 1 card, HTML
├── business-card.css                       same, Print CSS
├── business-card-sheet.html                A4 10-up, HTML
├── business-card-sheet.css                 same, Print CSS
├── Makefile                        make all → run both paths
├── results.md                      Measurements
└── out/                            Generated PDFs (committed)
    ├── business-card-python.pdf
    ├── business-card-sheet-python.pdf
    ├── business-card-html.pdf
    └── business-card-sheet-html.pdf
```

## Setup

```bash
pip install reportlab weasyprint
# Optional, for Linux Japanese font fallback
sudo apt install fonts-noto-cjk
```

ReportLab uses its bundled CID fonts (HeiseiKakuGo-W5 / HeiseiMin-W3)
so no external font file is needed for Japanese. The HTML + CSS side
falls back to system "Mincho" / "Sans" (Mac: Hiragino, Windows: Yu,
Linux: Noto CJK).

## Usage

```bash
make all          # all four PDFs + size measurements
make python       # path A only
make html         # path B only
make clean        # wipe out/
```

## Design

- **Name (Japanese, Mincho 14pt)** — the dominant element
- **Name (English, Sans 9pt, gray)** — romanized
- **Title (JA · EN, Sans 9pt, accent `#c8442a`)** — aiseed.dev's accent color
- **Thin accent rule** — separates upper/lower
- **email / URL (Sans 9pt)** — contact

Tagline / job-role wording in the title slot matches aiseed.dev's
"free person of the AI era / builder" terminology. To change the
design, edit color constants in `business_card.py` or the relevant
CSS variables in `business-card.css`.

## Extensions

- **100 cards at once**: switch `card-data.json` to `card-data.csv` and
  loop in Python — one PDF, many cards (Chapter 4, "structure-preserving
  document assembly").
- **Two-sided card**: extend `make_single()` to emit two pages; put a
  QR code on the back via `pip install qrcode`.
- **Press-ready**: add 3mm bleed to make it 97 × 61mm and draw crop
  marks. Same Python file, more constants.
- **Multiple locales**: keep `card-data-ja.json` / `card-data-en.json`
  and pass the file as an argument.

All of these stay in the **same framework**. No commercial business-card
service, no Illustrator session, no Word merge field.
