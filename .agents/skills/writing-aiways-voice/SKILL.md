---
name: writing-aiways-voice
description: Voice, tone, and prose conventions for the aiseed.dev essay series "AIネイティブな仕事の作法" (articles/ai-native-ways/). Use when drafting or editing chapter prose in either Japanese or English, to keep new chapters indistinguishable from existing chapters 00–12. Covers heading patterns, bold/italic/blockquote usage, Mermaid conventions, related-articles formatting, and the JA→EN adaptation rules. Pair with authoring-aiways-chapter (mechanical scaffold) and building-ai-native-software-series (sub-series driver).
---

# The voice of "AIネイティブな仕事の作法"

The series has a distinctive register: **structural, self-reliant, assertive — with evidence**. Each chapter argues that one layer of legacy tooling can be replaced by AI-native structure (Markdown, JSON, Python, SQLite, Parquet, plain text), and the prose enacts that thesis by being structurally tight rather than rhetorically warm.

These rules are extracted from chapters 00 through 12 of `articles/ai-native-ways/`. If a rule below contradicts an existing chapter, the existing chapter wins — update this skill.

Sub-series chapters (e.g. `software/`) share the same voice; only the chapter label, the index page they appear on, and the "次の章" / "前の章" chain change. Do not soften the register because the sub-series is more argumentative — keep the same declarative, evidence-led tone.

## Register

- **である調** in Japanese; declarative present in English. No ですます, no apologetic hedges ("might want to consider").
- Tone is **assertive** but **not affective**: state, don't exclaim. The persuasion comes from cumulative reasons, not adjectives.
- Address the reader as an adult who has used Excel and has heard of Markdown. Do not over-explain common tools.
- Brand-name verdicts are allowed when justified ("Microsoft 365 Copilotは最も危険") — but the next sentence must say *why*.

Three adjectives to keep in mind: **構造的 (structural) · 自立的 (autonomous) · 断定的 (declarative, evidence-backed)**.

## Opening a chapter

The first 3–5 lines after `# Title` must do all of:

1. Drop one **bold sentence** that compresses the chapter's claim.
2. Anchor to a prior chapter or the prologue so the reader knows where they are in the arc.
3. Move to the **concrete action** in the next paragraph — not background, not history.

Example (`01-python/ja.md`):

```markdown
**AI ネイティブな働き方への最初の一歩は、ここで決まる**。

序章で挙げた「最初にやること」── Excel(と Word)に埋め込まれた
マクロ・VBA・グラフ・ピボットを、Python に外部化する ── を、この
章で実際にやる。
```

Avoid: "本章では…について説明します" / "In this chapter we will discuss…".

## Headings

- `## h2` is the working unit. Most chapters are h1 → several h2 → optional h3. Deep nesting is rare.
- **h2 titles are declarative sentences**, not topic labels:
  - `Python は全員のものだ` (01)
  - `Word は書式の檻だ` (02)
  - `JSON は構造をそのまま持つ` (04)
  - `処理する人から判断する人へ` (05)
- Use ` ── ` (the em-dash compound) inside titles to attach a clarifier: `データを持つ ── JSONとYAMLで考える`.
- h3 appears only when an h2 splits into clearly named sub-procedures (e.g. `ONLYOFFICE をインストールする` under `最初にやること`).
- There is **no obligatory ending heading**. Some chapters use `## 結びに`, most just end with a forward-looking paragraph: `次の章では、…を見ていく。`

## Bold, italic, blockquote — they are typographic devices

The template renders these without the usual semantics:

| Markdown | Renders as | Use it for |
|---|---|---|
| `**bold**` | yellow highlight | **slogan compression** — a single sentence the reader should be able to lift out: `**処理する人から判断する人へ**`, `**CSV は捨てる**` |
| `*italic*` | accent-color text (no slant) | rare; reserve for a term being introduced |
| `> blockquote` | paper-deep callout | a 1–3 line compressed restatement of the section's thesis |
| `---` | `◆ ◆ ◆` decoration | section breaks, and **always once** before `## 関連記事` |

Rules of thumb (per audit of 00–12):

- Use `**bold**` 2–4 times per chapter, not more. Each occurrence should be quotable on its own line.
- Use `>` blockquote 1–4 times per chapter, on key turns. Often the blockquote contains an embedded `**bold**`.
- Avoid `*italic*` in Japanese prose — CJK italics look fragile and the accent color is better deployed via `<span class="accent">` in `title_html`.

Example of the blockquote/bold combination (`00-prologue/ja.md`):

```markdown
> 効率化ではない。**仕事の質と、個人の自立と、社会の多様性**の話だ。
```

## Lists

- `-` bullets for **parallel items** (tools, structures, choices). Keep them at one or two levels max.
- `1.` numbered lists for **ordered procedures or ranked priorities** ("最初にやること三つ").
- Each bullet starts with a noun or verb in the **same grammatical mood** as its siblings. Mixing imperatives with noun phrases inside one list breaks the rhythm.

## Mermaid diagrams

- **1–2 diagrams per chapter** is the norm; 3 is a maximum.
- Use `flowchart TB` (top-bottom) by default; `flowchart LR` only when the relationship is genuinely a left-to-right pipeline.
- No sequence/ER/class diagrams — this series shows **structural flow and dispatch**, not protocol timing or schema.
- Use exactly two semantic colors, every chapter:

  ```mermaid
  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34   /* AI-native / recommended */
  classDef bad  fill:#fef3e7,stroke:#c89559,color:#5a3f1a   /* legacy / dependent / risky */
  ```

  Green = AI-native, autonomous, recommended. Orange/tan = legacy, dependent, vendor-locked. Do not introduce a third semantic color casually.

- Label edges with the *reason* for the relationship, not just the verb: `==>|テキスト変換 = 書式が崩れ、構造が消える|` rather than `==>|変換|`.

## Code blocks

- Fenced with the language tag (` ```python `, ` ```bash `, ` ```yaml `, ` ```mermaid `).
- Keep snippets under ~15 lines. Real evidence belongs in `example-N/`, not in the chapter body.
- Comments inside code should reinforce the chapter's point ("# 100万行でも秒で集計"), not narrate syntax.

## Closing a chapter and "関連記事"

- Final paragraph forecasts the next chapter: `次の章では、領域ごとに具体的な作法を見ていく。`
- Then one `---` rule.
- Then `## 関連記事` (JA) / `## Related articles` (EN) with a bullet list:

  ```markdown
  ## 関連記事

  - [構造分析08: 企業ITの税を引く](/insights/enterprise-tax/)
  - [構造分析12: AIと個人事業](/insights/ai-and-individual/)
  - [Claudeと一緒に学ぶDebian](/claude-debian/)
  ```

- Targets are usually internal: other chapters in the series, `/insights/…`, `/blog/…`, `/claude-debian/`. External links are rare.

## JA ↔ EN adaptation

Translate **concepts**, not surface forms.

- **Tone parity**: both versions are declarative. EN uses imperative or present indicative, never "you might want to".
- **Accent parity**: the *concept* highlighted by `<span class="accent">` should match across languages, even when the words differ. JA `<span class="accent">使う能力</span>` ↔ EN `<span class="accent">using</span>` is acceptable because both highlight the act, not the affix.
- **Idiom relocation**: Japanese metaphors like 「Office の檻」 become "cage of formatting" in English — keep the metaphor, swap the noun if needed.
- **Loanword handling**: technical loanwords stay (`API`, `Markdown`, `Pydantic`). Localized loans (`ロックイン` ↔ `lock-in`) stay parallel.
- **Section count and order** stay the same. Heading wording can adapt, but do not reorder, merge, or split sections between languages.

## Common claims this series will make

Recurring moves to use deliberately (not as filler):

- **The two-language framing** — "Office vs Python", "Java/C# vs Python", "vendor AI vs your own stack". Each chapter picks one such axis and shows how the AI-native side dissolves the legacy one.
- **The "下層に任せる" argument** — type safety belongs in the package layer (Polars/Rust, SQLite/C, Pydantic/Rust), not in human code. Python is the connector, not the workhorse.
- **The autonomy frame** — "集中化された 1 つより、自立した N が強い". Centralization is presented as a single point of failure, not as efficiency.
- **Evidence reflex** — when a claim is testable, link to an `example-N/` folder with numbers ("11.7秒で完走", "9KB").

## Anti-patterns

- Headings that are nouns alone (`Python について`) — make them declarative.
- Bullet lists longer than ~8 items — split into a table or subsections.
- Hedging adverbs ("おそらく", "やや", "probably") — strike them.
- Mermaid diagrams without color, without edge labels, or with more than three semantic colors.
- "関連記事" that points to the same article twice, or only to external sites.
- "次の章" pointers that disagree with `next_slug` in the frontmatter.

## Quick checklist for a finished chapter

- [ ] First 3–5 lines: bold claim, prior-chapter anchor, concrete move.
- [ ] All h2 are declarative sentences; h3 used only for named sub-procedures.
- [ ] 2–4 `**bold**` lines, each independently quotable.
- [ ] 1–4 `>` blockquotes on key turns.
- [ ] 1–2 Mermaid `flowchart` diagrams with green/orange classDef.
- [ ] No `*italic*` in Japanese unless introducing a term.
- [ ] Closes with a `次の章` paragraph, then `---`, then `## 関連記事`.
- [ ] EN version mirrors section order and accent **concepts**.
- [ ] Any testable claim either cites numbers inline or links to an `example-N/` folder.
