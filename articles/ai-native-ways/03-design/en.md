---
slug: design
number: "03"
lang: en
title: "Designing — With Mermaid and Claude Design"
subtitle: "Structural diagrams, UI, slides, business materials — all from text"
description: Business design — architecture diagrams, UI mockups, slides, proposals — has moved away from specialized tools into the era of text-and-AI generation. Mermaid for structural diagrams, Claude Design for UI and screens, Marp for slides. No more Figma, no more PowerPoint, no more Adobe XD.
date: 2026.05.02
label: AI Native 03
title_html: <span class="accent">Design</span>, also in text.<br><span class="accent">Mermaid</span> and <span class="accent">Claude</span> generate it.
prev_slug: markdown
prev_title: "Writing Documents — Markdown as the Minimal Choice"
next_slug: data-formats
next_title: "Holding Data — Think in JSON, CSV, YAML"
---

# Designing — With Mermaid and Claude Design

Change the tools you build designs with.

Until now, business design required separate specialized tools by purpose: PowerPoint, Visio, Figma, Sketch, Adobe XD, Canva, Photoshop. Steep learning curves, proprietary file formats, ongoing subscription fees.

The era has changed.

**Design, too, is generated from text.** Structural diagrams in Mermaid. UI and screens in Claude Design. Slides in Markdown. Every output traces back to text or code. **Editable, version-controllable, AI runs alongside as a colleague.**

## Types of design and their tools

Organize the work that "design" covers in business.

| Kind | Tool |
|---|---|
| **Structural diagrams** (flow, ER, sequence, architecture) | Mermaid (generated from text) |
| **UI / screens** (web, app drafts) | Claude Design (HTML+CSS output) |
| **Slides** (presentations) | Markdown → Marp / reveal.js |
| **Inset diagrams / explainers** | Mermaid + Claude Design |
| **Posters, flyers, handouts** | Claude Design / SVG |
| **Logos / serious branding** | Specialist designer (Claude assists with drafts) |

What unites them: **save not the final PDF or PNG, but the text and code that produced it.**

## Structural diagrams in Mermaid

Business systems, organizations, data relationships — every diagram that conveys *structure* can be written in Mermaid.

```
graph TD
  A[User] --> B[Web Server]
  B --> C[(Database)]
  B --> D[Cache]
  C -.->|slow| B
```

Four nodes and the arrows between them, expressed in plain text.

A diagram drawn in PowerPoint becomes an image the moment it's pasted into Word; structure is lost. It cannot be moved. Diffs are invisible. **Mermaid is text.** Git diffs work. AI reads it. You can edit it. It is still readable in ten years.

What you can write:

- Flowcharts (process flow)
- Sequence diagrams (APIs, human interactions)
- ER diagrams (data relationships)
- Class diagrams (object relationships)
- Gantt charts (project planning)
- State diagrams (screen / data state changes)
- Mind maps
- Architecture diagrams (system layout)

GitHub, Notion, Zed — most places render Mermaid natively. There is no need to memorize the syntax. **Ask Claude "draw this structure in Mermaid," and it returns the code.** You only need to read it.

## UI and screens in Claude Design

"Screen drafts," "UI mockups" — these used to live in Figma or Sketch. Steep learning curves, mandatory subscriptions, sealed inside the designer's workspace.

**Claude Design** changed this.

Ask "make a login form" and HTML + CSS + (if needed) JavaScript come back. Open the result in a browser, and there is a working screen. "Make it more refined." "Use a blue palette." "Left-align it." Speak the instruction in words, and the code rewrites itself.

```
You:    Make an inventory management screen UI. Product list, search box, add button.
Claude: (HTML+CSS returns)
You:    More whitespace, three columns.
Claude: (revised version returns)
```

This is not a Figma replacement. **It is faster than Figma, and the output is code-native** — it can be handed straight to development. It maps cleanly onto the HTML+CSS+minimal-JS stack from Chapter 7.

In business, this enables:

- Show "here's the screen idea" instantly during a customer pitch
- Embed a working HTML mockup inside the spec (not just an image)
- Compare multiple design candidates side-by-side before development starts
- Use the finished mockup as the development starting point
- Adjust live during stakeholder discussions

If a specialist designer is involved, **make the draft in Claude Design and hand it to them**: "this direction, polished further." Designers spend their time on what truly requires their expertise — brand consistency, print accuracy, photo selection.

## Slides also in Markdown

Presentation decks, too, written in Markdown.

`Marp` and `reveal.js` convert Markdown into HTML slides. One slide = one `---`-separated section in Markdown.

```markdown
# AI-Native Ways of Working

Change your tools, and the way you think changes

---

## Why now

The era of tools changed with AI

---

## Conclusion

One person + AI can do the work
```

That alone produces three slides exportable to PDF, HTML, and PNG.

Compared to PowerPoint:

- **PowerPoint**: binary format, formatting and content intermixed, no Git diff, AI cannot read it cleanly
- **Markdown + Marp**: text, structure only, Git diffs work, AI reads and writes

For slides that need complex layout, have Claude Design produce the HTML for that slide alone. **Base in Markdown; decoration in Claude.**

The speed of business presentation creation jumps:

- A 30-minute talk: written as 30 lines of Markdown
- Marp instantly produces PDF / HTML
- Edits are edits to Markdown
- Past slides become searchable (all text)
- The proposal document and the deck come from the same Markdown source

## Build business documents while keeping structure intact

Proposals, reports, specifications, internal documents, press releases — all are built with **Markdown as the body, Mermaid for diagrams, Claude Design for any decorative graphics**.

Concrete arrangement:

```
articles/proposal-2026/
  ├── ja.md              # Body (Markdown)
  ├── architecture.mmd   # Structural diagram (Mermaid)
  ├── ui-mockup.html     # Screen example (Claude Design output)
  └── cover.svg          # Cover page (SVG)
```

Python assembles these into a PDF (`pandoc`, `weasyprint` both work). Each component is independent and reusable elsewhere:

- The same Markdown can also generate an internal-wiki HTML version
- The same structural diagram can be pasted into another deck
- The UI mockup can go directly to the development side
- The same source materials produce PDF, HTML, print, and AI input — convert by purpose

"Design" and "content" are separated. **Editing does not become hell.** Fix one place; every output reflects it. This is exactly the principle from Chapter 7: "content in Markdown+Mermaid, frame only in HTML/CSS."

## The division of work with designers also changes

Claude Design cannot do everything. Serious branding, complex printed pieces, visual production involving photography — these remain the specialist designer's territory.

But **you can produce the draft yourself**, and that changes the division of work.

Before:

- Convey requirements verbally or in writing
- Designer interprets and produces a design
- The result differs from what was imagined
- Many round trips

After:

- You produce three screen drafts in Claude Design
- Hand to the designer
- "This direction, polished further"
- Intent transmitted in one round

**Designer expertise concentrates on what truly demands expertise.** Time stops being spent on the draft phase. This is the same shape as Chapter 6's "stop outsourcing business-system rewrites; the floor + Claude completes the loop." **The floor produces the draft; specialists focus on the finish.**

## You don't need to draw it yourself

Common to everything above: **humans don't really need to "draw."**

- No need to memorize Mermaid syntax. Ask Claude "draw this structure in Mermaid."
- No need to learn CSS. Ask Claude "make this kind of screen."
- No need to think about slide layout. Ask Claude "lay out this content as five Marp slides."

What humans do is **articulate intent in words, judge what comes back, instruct revisions**. That's it. The work of "drawing" passes to AI. The time spent thinking about *what to convey* increases.

> Don't memorize design symbols and rules. Acquire the ability to convey intent to Claude. That is the new literacy.

## Still readable in ten years

20-year-old PowerPoint files sometimes have substituted fonts, shifted shapes, or won't open at all. Old Adobe Illustrator `.ai` files may not open in newer versions. Figma designs disappear when the service ends.

Mermaid, Markdown, SVG, HTML+CSS — these are text. A file from 20 years ago renders fine today. 20 years from now will be the same. **AI reads them even more easily.**

> Hold design as structure too.

Formatting decorates display. Structure crosses time.

## In numbers

30-page slide deck in PowerPoint: prose and layout intermixed, **4 hours**. Same content in Marp: 30 lines of Markdown, 1-second build, edits are just Markdown changes — total **30 minutes**. **8x faster.**

UI mockup in Figma: $15/month subscription, 1 hour of shape manipulation, image-exported (not interactive) when handed to development. Claude Design "make a login form" returns HTML+CSS instantly, runs in the browser, ready for development. **Zero subscription.**

A one-line Mermaid diagram change in Git: 1 added, 1 removed, reviewed in 30 seconds. The same change in PowerPoint: file shows "binary changed," not reviewable.

A 20-year-old `.ppt` file: substituted fonts, shifted shapes, hard to reproduce. A Markdown / Mermaid file from the same era renders perfectly today.

## In summary

Move design tools to be text-centric.

- Structural diagrams: **Mermaid**
- UI and screens: **Claude Design** (HTML+CSS output)
- Slides: **Markdown + Marp / reveal.js**
- Inset diagrams and handouts: **Mermaid + Claude Design**
- Business documents: **Markdown as body, diagrams and screens as separate files**

Step away from specialized tools — Figma, Sketch, Adobe XD, PowerPoint, Visio. Hold designs as text and code that AI can write. Subscription fees disappear, learning curves shrink, editing stops being hell, and AI runs alongside as a colleague.

Specialist designers remain necessary. **But their time goes to specialist territory, not drafts** — you take the draft work over with Claude.

The next chapter moves to how you hold data — from Excel to JSON / CSV / YAML, with SQLite + Python for mutable data and Parquet + DuckDB for large-scale data.

---

## Related

- [Chapter 02: Writing Documents — Markdown as the Minimal Choice](/en/ai-native-ways/markdown/)
- [Chapter 04: Holding Data — Think in JSON, CSV, YAML](/en/ai-native-ways/data-formats/)
- [Chapter 07: Building for the Web — Back to HTML+CSS+JavaScript](/en/ai-native-ways/web/)
- [Prologue: Office for paperwork, Java/C# for business systems — but AI runs on Python and text](/en/ai-native-ways/prologue/)
