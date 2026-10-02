---
name: authoring-series-chapter
description: Mechanics for adding, moving, renumbering, or splitting a chapter in an aiseed.dev series that is managed as one AsciiDoc file — chiefly "AI ネイティブなソフトウェア開発" (articles/ai-native-software.adoc), and the same format used by insights, blog, claude-debian, phosphorus-and-farming, and fable. Covers the `// ===== article:` separator, the bare-key / key.ja / key.en frontmatter, the ifdef::lang-ja[] / ifdef::lang-en[] bodies, part/number numbering, site.json series registration, the build and link checks, and the JA/EN parity checks. Use with writing-series-voice (prose) and building-ai-native-software-series (what each chapter of that series must contain).
---

# Authoring a chapter in a one-file series

Every series on aiseed.dev is **one `.adoc` file** under `articles/`. A chapter is a block inside that file. There are no per-chapter folders, no `ja.md` / `en.md` pairs, and no hand-written prev/next chain. The old `articles/ai-native-ways/` layout (and its two series) was retired on 2026-09-21; ignore anything that still describes it.

## The file

```
// ai-native-software — シリーズ全記事(このファイル1つで管理)
// 記事の区切り: // ===== article: <記事ID> =====
// フロントマター: 日英共通は裸キー、異なる値は key.ja / key.en
// 本文: ifdef::lang-ja[] / ifdef::lang-en[] で言語別
// prev/next 連鎖は書かない(記事の並び順から自動導出)

// ===== article: 01-coder-top =====
---
slug: coder-top
number: 01
part: 1
title.ja: …
title.en: …
subtitle.ja: …
subtitle.en: …
description.ja: …
description.en: …
date: 2026.06.01
label: Introduction 1
title_html.ja: …<br><span class="accent">…</span>
title_html.en: …
---
ifdef::lang-ja[]
= 章のタイトル

本文…

== 関連記事

* link:/ai-native-software/coder-end/[1-03: …]
endif::[]
ifdef::lang-en[]
= Chapter Title

Body…

== Related articles

* link:/en/ai-native-software/coder-end/[1-03: …]
endif::[]
```

Rules the build relies on:

- **The article ID** (`01-coder-top`) is internal. Its numeric prefix is only for humans scanning the file; it does **not** set order or URL. The ID may lag the displayed number after a renumber — that is fine.
- **Order = position in the file.** prev/next links and the index order are derived from where the block sits. To move a chapter, move the whole block.
- **URL = `slug`.** `/ai-native-software/{slug}/` and `/en/ai-native-software/{slug}/`. Treat slugs as permanent; renaming one breaks inbound links (add a line to `html/_redirects` if you must).
- **Frontmatter**: a bare key applies to both languages; `key.ja` / `key.en` split it. Do not write prev/next keys.
- **Bodies**: each language sits between `ifdef::lang-ja[]` (or `lang-en`) and `endif::[]`. The `= Title` line is stripped by the template (the hero already shows it) but write it anyway.

## Numbering (ai-native-software)

- `part`: `1` 導入編 / `2` 自立編 / `3` 転換編.
- `number`: restarts at `01` in each part. The displayed badge is `{part}-{number}` (e.g. `2-11`).
- `label`: `Introduction N` / `Independence N` / `Shift N`.
- In prose, refer to chapters by `{part}-{number}` (`2-07`), never by the article ID.
- `site.json` → `builder.series[]` declares the series: `file`, `label`, `label_en`, `url_base`, `subtitle(_en)`, `description(_en)`, and `parts[{key,name_ja,name_en}]`. A new series is not built until it is listed there.

## Adding or moving a chapter

1. Write the block (frontmatter + JA body + EN body) and place it at the right position in the file.
2. Set `part` / `number` / `label`. If you inserted into the middle of a part, renumber every later chapter in that part (`number` and `label`).
3. Fix every prose reference that named a shifted number. Grep for the old `{part}-{number}` strings across the series file **and** `articles/blog.adoc`, `insights.adoc`, `claude-debian.adoc`, `fable.adoc`, `phosphorus-and-farming.adoc`.
4. Update the previous chapter's closing paragraph (`次章では…`) and the new chapter's own.
5. Run the checks below, then build.

## Checks to run every time

**JA/EN parity.** The two languages must have the same number of `==` sections, `____` quote blocks, and `|===` tables, in the same order:

```bash
python3 - <<'PY'
import re
from pathlib import Path
t = Path("articles/ai-native-software.adoc").read_text(encoding="utf-8")
p = re.split(r"^// ===== article: (.+?) =====$", t, flags=re.M)
it = iter(p[1:]); bad = 0
for aid, body in zip(it, it):
    ja = body.split("ifdef::lang-ja[]")[1].split("endif::[]")[0]
    en = body.split("ifdef::lang-en[]")[1].split("endif::[]")[0]
    for name, f in (("節", lambda s: len(re.findall(r"^== ", s, flags=re.M))),
                    ("引用", lambda s: s.count("\n____\n")),
                    ("表", lambda s: s.count("\n|===\n"))):
        if f(ja) != f(en):
            print("MISMATCH", aid, name, f(ja), f(en)); bad += 1
print("bad", bad)
PY
```

**Build.**

```bash
python3 tools/build_article.py --all
```

Do not run this while `tools/serve.py` (the auto-rebuilding preview) is running — both delete `.build/` and one of them will crash with `FileNotFoundError`.

**Internal links.** After the build, every `href="/…"` in `html/` must resolve:

```bash
python3 - <<'PY'
import re
from pathlib import Path
root = Path("html"); bad = 0
for f in root.rglob("*.html"):
    for u in set(re.findall(r'href="(/[^"#?]*)"', f.read_text(encoding="utf-8"))):
        q = root / u.lstrip("/")
        if u.endswith("/"): q = q / "index.html"
        if not q.exists(): print("BROKEN", u, f); bad += 1
print("broken", bad)
PY
```

**Generated files.** `html/sitemap.xml` is regenerated by every build; leave it out of commits (`git checkout -- html/sitemap.xml`) — the site owner rebuilds it. `html/ai-native-software/` and `html/en/ai-native-software/` are git-ignored.

## AsciiDoc that this site renders

| Source | Renders as | Use |
|---|---|---|
| `== Heading` | `<h2>` | the working unit of a chapter |
| `=== Heading` | `<h3>` | only when an h2 splits into named sub-parts |
| `*text*` | bold with a yellow highlight underlay | one quotable sentence |
| `_text_` | accent colour, upright (no slant) | rare; a term being introduced |
| `____` … `____` | callout block | 1–3 line restatement of a turn |
| `'''` | `◆ ◆ ◆` | once, before `== 関連記事` |
| `link:/path/[text]` | link | internal links; always `/ai-native-software/…` or `/en/ai-native-software/…` |
| ```` ```python ```` … ```` ``` ```` fences | code | the series uses backtick fences, not `----`; keep short (see writing-series-voice) |
| `\|===` table | table | the first row is the header |

## Where to look in the code

- `tools/build/series.py` — `expand_all()` splits each series file into `.build/articles/`.
- `tools/build_article.py` — `build_custom_series()`, `build_custom_index()`, `build_custom_chapter()`, `_custom_chapter_badge()` (the `{part}-{number}` badge), part-grouped index.
- `tools/build/template_vars.py` — `custom_index_vars`, nav/footer labels.
- `tools/templates/chapter.html` / `chapter.en.html` / `index.html` — page templates.
- `html/_redirects` — 301s for retired URLs (the old `/ai-native-ways/…` paths point here).
