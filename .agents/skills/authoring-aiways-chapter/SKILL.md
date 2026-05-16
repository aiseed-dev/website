---
name: authoring-aiways-chapter
description: Scaffolds a new chapter in the aiseed.dev essay series "AIネイティブな仕事の作法" (articles/ai-native-ways/). Use when adding, renumbering, or splitting a chapter — handles the bilingual ja.md/en.md frontmatter, the prev/next link chain, the example-N/ evidence folders, and the build command. Use together with writing-aiways-voice (style/tone) and building-ai-native-software-series (software-development sub-series driver).
---

# Authoring an "AIネイティブな仕事の作法" chapter

A chapter lives in `articles/ai-native-ways/NN-slug/` with paired `ja.md` and `en.md`. The build tool (`tools/build_article.py::build_aiways_chapter`) renders each into the series' independent typography template (`articles/ai-native-ways/template.html` / `template.en.html`). For voice and prose conventions, read `writing-aiways-voice` first; this skill covers the mechanical scaffold only.

## Directory layout

```
articles/ai-native-ways/
├── README.md                 # series-level spec (do not modify casually)
├── template.html             # JA Jinja2 template
├── template.en.html          # EN Jinja2 template
└── NN-slug/                  # one chapter = one folder
    ├── ja.md                 # required
    ├── en.md                 # required
    └── example-N/            # optional evidence folders, ignored by build
```

Rules enforced by `tools/build_article.py`:

- Folder name **must start with a digit** (`NN-slug`); folders whose name does not start with a digit (e.g. `example-1/`) are skipped.
- Sorting is **string-sort on folder name**, so use 2-digit zero-padded numbers (`00`, `01`, …, `23`).
- The chapter label is derived from `number`: `00` → 序章 / Prologue, otherwise 第N章 / Chapter N (`_aiways_chapter_label` in `tools/build_article.py:476`).

## Frontmatter (required)

Both `ja.md` and `en.md` start with YAML frontmatter using the schema shared across `articles/insights/`, `articles/blog/`, `articles/claude-debian/`. Series-specific labels (序章 / 第N章 / 年) are derived by the build side; do **not** put them in frontmatter.

```yaml
---
slug: coder-end                 # URL: /ai-native-ways/{slug}/
number: "13"                    # zero-padded string, must match folder prefix
lang: en                        # EN only; omit on ja.md
title: 章のタイトル(JA) / Chapter Title (EN)
subtitle: 副題 — hero-subtitle に表示
description: SEO/OG 用の短い説明(1〜2文)
date: 2026.06.01                # dot-separated, monotonically increasing across chapters
label: AI Native 13             # "AI Native NN" — NN matches `number`
title_html: ...<br>...          # optional: overrides hero-title with HTML fragment
prev_slug: one-plus-ai          # previous chapter's slug (omit on chapter 00)
prev_title: 1人+AIで作る — 新しい仕事の単位
next_slug: builder              # next chapter's slug (omit on final chapter)
next_title: ビルダーという役割
---
```

### Field-by-field conventions (from existing chapters 00–12)

| field | convention | example |
|---|---|---|
| `slug` | English kebab-case, ≤ 3 words, theme-noun | `python`, `office-replacement`, `one-plus-ai` |
| `number` | quoted string, zero-padded | `"00"`, `"12"` |
| `title` (JA) | 体言止め or 命令形 + `──` + 説明補足 | `処理を書く ── AIにPythonで書いてもらう` |
| `title` (EN) | imperative or noun phrase, em-dash for subtitle attachment | `Writing Logic — Have AI Write Python For You` |
| `subtitle` | 1 sentence, 30〜60 chars JA / 60〜100 chars EN | varies |
| `description` | 1〜2 sentences, ends with the chapter's payoff | varies |
| `date` | `YYYY.MM.DD` dot-separated; later chapters get later dates | `2026.05.01` for 00, increment per chapter |
| `label` | `AI Native NN` literal | `AI Native 00` |
| `title_html` | single-line HTML fragment with `<br>` and `<span class="accent">…</span>` | `事務処理は<span class="accent">Office</span>。<br>…` |
| `prev_*` / `next_*` | slug + title of adjacent chapter, empty/omitted at ends | — |

### `title_html` (optional but recommended)

Wraps the hero-title's key terms in the series' accent color (`#c8442a`). Apply to **tool names, structures, or actions** — not to feelings or modifiers. JA and EN positions can differ because of grammar; preserve which **concept** is accented rather than which word.

```yaml
# 00-prologue/ja.md
title_html: 事務処理は<span class="accent">Office</span>。<br>業務ソフトは<span class="accent">Java/C#</span>。<br>しかしAIは、<span class="accent">Pythonとテキスト</span>。

# 00-prologue/en.md
title_html: Paperwork is <span class="accent">Office</span>.<br>Business systems are <span class="accent">Java/C#</span>.<br>But AI is <span class="accent">Python and text</span>.
```

## Body (after the closing `---`)

- Start with `# 章タイトル` / `# Chapter Title`. The build strips this `<h1>` (it would duplicate the hero-title) — but write it anyway so the source Markdown reads cleanly.
- End with a `---` rule followed by `## 関連記事` / `## Related articles` and a bullet list of `- [title](url)` links to other chapters, `/insights/…`, `/blog/…`, `/claude-debian/`, etc.
- For prose, structure, accent usage, and Mermaid conventions, see the `writing-aiways-voice` skill.

## Adding a chapter — step-by-step

1. Choose `NN` and `slug`. Verify `NN` does not collide with existing folders.
2. Create the folder and the two source files:

   ```bash
   mkdir articles/ai-native-ways/NN-slug
   touch articles/ai-native-ways/NN-slug/ja.md
   touch articles/ai-native-ways/NN-slug/en.md
   ```

3. Write the JA frontmatter using the table above, then the body.
4. Write the EN frontmatter (must include `lang: en`); translate / adapt the body. Keep `title_html` accent **concepts** aligned across languages, not literal word positions.
5. Update the **previous chapter's** `next_slug` / `next_title` (both `ja.md` and `en.md`). If inserting between chapters, update both neighbors on both sides.
6. Build and preview:

   ```bash
   python3 tools/build_article.py articles/ai-native-ways/NN-slug/ja.md
   python3 tools/build_article.py articles/ai-native-ways/NN-slug/en.md
   ```

   The site index, sitemap, and series TOC update when running the full build:

   ```bash
   python3 tools/build_article.py --all
   ```

7. Confirm outputs:

   | source | output | URL |
   |---|---|---|
   | `NN-slug/ja.md` | `html/ai-native-ways/{slug}/index.html` | `/ai-native-ways/{slug}/` |
   | `NN-slug/en.md` | `html/en/ai-native-ways/{slug}/index.html` | `/en/ai-native-ways/{slug}/` |

## Renumbering / inserting

Renumbering a chapter touches three things:

1. The folder name (`NN-slug` → `NN'-slug`).
2. `number` and `label` inside both `ja.md` and `en.md`.
3. The `prev_*` / `next_*` chain on **all** adjacent chapters.

Run `python3 tools/build_article.py --all` once afterward to refresh the series TOC and the latest-articles tile on the site index.

## Evidence folders (`example-N/`)

Each chapter's claims are backed by **runnable evidence** in sibling folders. The build pipeline ignores any subfolder whose name does not start with a digit, so `example-1/`, `example-2/`, … are repo-only artifacts.

Place these 5 items in each `example-N/`:

1. `README.md` — what is being demonstrated, which claim in the chapter it supports
2. inputs — `source.md`, sample `*.docx`, CSV, code, etc.
3. `Makefile` (or `run.sh`) — one-shot reproduction command
4. `results.md` — measured numbers (build time, output size, page count, token ratio)
5. `out/` — generated artifacts, **committed** so readers can inspect via the git web UI

Use absolute numbers ("11.7秒", "9 KB"), not "fast" or "small". Pin dependency versions (`pandoc 3.1.x`, `pip install <pkg>==<ver>`).

A template `example-N/` lives in `00-prologue/example-1/`.

## Markdown → HTML conversion (CommonMark + tables)

The build uses `tools/build/markdown.py`. Be aware of these series-specific renderings:

| Markdown | HTML | Visual |
|---|---|---|
| `# Heading 1` | (stripped) | duplicates hero-title; do not rely on it |
| `## Heading 2` | `<h2>` | section heading |
| `### Heading 3` | `<h3>` | sub-section |
| `> quote` | `<blockquote><p>` | paper-deep background block |
| `**bold**` | `<strong>` | marker-highlight color, not weight |
| `*italic*` | `<em>` | accent color (`#c8442a`), not italic slant |
| `[t](u)` | `<a>` | accent-colored link |
| ` ```code``` ` | `<pre><code>` | JetBrains Mono |
| `---` | `<hr>` | rendered as `◆ ◆ ◆` decoration |

Because `**` renders as a yellow highlight and `*` renders as accent color, treat them as **typographic devices**, not weight/slant emphasis. See `writing-aiways-voice` for usage rules.

## Where to look in the codebase

- `articles/ai-native-ways/README.md` — full series spec (read this first if unsure)
- `tools/build_article.py:462` — `build_aiways_chapter()` entry point
- `tools/build_article.py:476` — `_aiways_chapter_label()` derives 序章 / 第N章
- `tools/build/template_vars.py` — `aiways_index_vars()` for series-index strings
- `articles/ai-native-ways/template.html` / `template.en.html` — page templates and `:root` CSS variables
