---
name: writing-series-voice
description: Voice, tone, and prose rules for aiseed.dev's series "AI ネイティブなソフトウェア開発" (articles/ai-native-software.adoc) — structural, assertive, evidence-led, in Japanese である調 and declarative English. Use when drafting or editing chapter prose in either language. Covers the opening, declarative h2 headings, highlight/accent/callout usage in AsciiDoc, Mermaid conventions, the closing and 関連記事, JA→EN adaptation, and the review rules settled in the 2026-09/10 review pass — numbers need a source or get dropped, no model names in the body, chapters read as the first spec handed to an AI so code samples stay minimal, negative wording kept low. Pair with authoring-series-chapter (mechanics) and building-ai-native-software-series (what each chapter must contain).
---

# The voice of "AI ネイティブなソフトウェア開発"

The register is **structural, self-reliant, assertive — and backed by evidence**. Each chapter argues that one layer of legacy structure can be replaced, and the prose enacts that by being tight rather than warm.

If a rule here contradicts a chapter that has already been reviewed (see `docs/plan/rensai-minaoshi-hikitsugi.md` for which ones), the reviewed chapter wins — update this skill.

## Rules settled in the review pass (apply to every chapter)

These came out of the chapter-by-chapter review with the site owner. They override older habits.

1. **Every number has a source, or it goes.** A figure in the body either carries its source and date inline — `(Glass, IEEE Software, 2001)`, `(2026 年 9 月時点)` — or it is removed and the sentence is made structural. Do not "estimate" a number to keep a sentence vivid. If a search turns up evidence that *contradicts* the claim, change the claim, not the evidence. Prices are the owner's to judge: state list prices with date and conditions (税抜・年払い etc.), never invent a vendor's value proposition.
2. **The customer's numbers are the customer's.** Do not attribute measurements to "the author" or "発注者". If a figure can be calculated from public data, calculate it in the text with the inputs visible.
3. **No model names in the body** to sort capabilities into tiers (no "Opus は X、Fable/Mythos は Y"). Describe capabilities. A named product is fine as a *fact* with a source (e.g. what Anthropic has published about Claude-written code).
4. **This is an independent series.** Never "サブシリーズ", "ソフトウェア開発編", "親シリーズ", "sub-series", "parent series", "本書". Say 「この連載」 / "this series".
5. **Chapters are read as the first spec handed to an AI.** A reader passes a chapter to an AI and starts building. So: put the *decisions* first (what to use and not use, where it lives, how much you hold yourself, where borrowing begins), and keep code samples minimal — a few lines that show shape, not a working example. The AI already knows how to write the code; what it does not know is what this company chose.
6. **Keep negative wording low.** State what to do and where things go rather than what is bad. 「移る」「変わる」 over 「消える」 when the destination can be named. Words like 罠・攻撃・危険 are fine where the substance needs them (supply-chain attacks, safety of delegation), not as colour.
7. **Avoid hard chapter counts** (「全 14 章」「十一番目」). They go stale on every insertion. Say 「先頭から順に」, list the chapters, or link the index.
8. **Borrowed is borrowed.** When a list is headed "OSS" or "自分の側", do not put a hosted service in it. Cloudflare Pages is a borrowed window; say so, and say what the self-held alternative is.

## Register

- Japanese: **である調**. English: declarative present. No ですます, no "you might want to consider".
- Assertive, not affective: state, don't exclaim. Persuasion comes from stacked reasons, not adjectives.
- The reader has used Excel and heard of Markdown. Do not over-explain common tools.
- A verdict on a named vendor is allowed when the next sentence says *why*.

## Opening a chapter

The first lines after `= Title` do three things:

1. One *highlighted* sentence (`*…*`) that compresses the chapter's claim — or the claim stated plainly as the first sentence.
2. An anchor to an earlier chapter, by `{part}-{number}` and with a `link:`.
3. A move to the concrete subject in the next paragraph.

Avoid 「本章では…について説明します」 / "In this chapter we will discuss…".

## Headings

- `==` is the working unit. `===` only when an `==` splits into named sub-parts.
- **`==` titles are declarative sentences**, not topic labels: 「保守の単位は、コードから文脈へ移る」, not 「保守について」.
- ` ── ` attaches a clarifier: 「Web を公開する ── 自分の一台か、Cloudflare Pages か」.
- If one `==` carries two separate arguments, split it (2-01's 「ベンダーは自分からは開かない」 became three sections for this reason).

## Highlight, accent, callout

The template restyles these; treat them as typographic devices.

| AsciiDoc | Renders as | Use |
|---|---|---|
| `*text*` | bold on a yellow highlight | a sentence the reader could lift out on its own; 2–5 per chapter |
| `_text_` | accent colour, upright | rare — a term being introduced |
| `____` block | callout | a 1–3 line restatement at a key turn; 1–3 per chapter |
| `'''` | `◆ ◆ ◆` | exactly once, before `== 関連記事` |

## Lists and tables

- `*` bullets for parallel items, one grammatical mood per list. More than ~8 items → a table.
- `.` numbered lists for ordered procedures.
- Tables (`|===`) when items share columns. A three-column table is fine when it separates two senses of a word (see 1-04's 自由七科 / 近代のリベラルアーツ).

## Mermaid

- 1–2 per chapter. `flowchart TB` by default; `LR` only for a real left-to-right pipeline.
- Exactly two semantic colours:

  ```
  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  classDef bad  fill:#fef3e7,stroke:#c89559,color:#5a3f1a
  ```

- Label edges with the *reason*: `==>|設計とコードの価格が立たず分業が解ける|`, not `==>|変換|`.
- No model names in node labels; describe the capability (`コードを書く力`).

## Code

- Backtick fences with a language tag.
- A few lines that show the *shape* of a decision (a Caddyfile, three build commands). No full working programs — see rule 5.
- Comments reinforce the point, not the syntax.

## The three-section block (自立編 only)

Every 自立編 chapter ends, just before `== まとめ`, with:

- `== 確かめ方` / `== How to check you are done` — numbered, checkable by hand.
- `== 人が持つ物` / `== What the human holds` — *人が渡す値* and *AI が「やる前に言う」操作*.
- `== 確かめた版と日付` / `== Versions checked, and when` — tools, versions, the date written, and "if a version has moved, have the AI confirm the official procedure first".

## Closing

- `== まとめ` with a short bulleted compression, then one paragraph that hands off: 「次章では…」. The last chapter of a part hands off to the next part's first chapter by name and link (1-05 → 2-01).
- `'''`, then `== 関連記事` / `== Related articles`, 3–6 internal links, written `link:/ai-native-software/{slug}/[{part}-{number}: title]`. No duplicates, no links to the retired `/ai-native-ways/`.

## JA ↔ EN

- Same number and order of `==` sections, `____` callouts, and `|===` tables (the parity check in authoring-series-chapter enforces it).
- Translate concepts, not surface forms. Keep metaphors; swap nouns if needed.
- Accent and highlight mark the same *concept* in both, even if the words differ.
- English links use `/en/ai-native-software/…`.

## Anti-patterns

- Noun-only headings.
- Hedging adverbs (おそらく、やや、probably).
- A number with no source.
- A model name used as a capability tier.
- "サブシリーズ" / "parent series" / "本書".
- A long working code sample where a decision list would do.
- 「次章では」 that disagrees with the actual next chapter.
