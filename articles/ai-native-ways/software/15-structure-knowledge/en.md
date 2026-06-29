---
slug: structure-knowledge
number: "10"
part: "2"
lang: en
title: "Make Your Knowledge Legible — Preparation Is the Main Body, AI the Last Move"
subtitle: "OCR, classification, codifying tacit knowledge — move scattered, unwritten knowledge into a written, structured state. A no-regret investment you recover even without AI."
description: Before you put AI on top, build information worth putting it on. Scattered files, paper and scanned PDFs, tacit knowledge that lives only in someone's head — move them into a written, structured state with OCR, classification, and codification. Preparation is the main body; AI is the last move. What to keep and how to structure it is a judgment only people can make, and it pays off as the end of personnel lock-in even if you never put AI on it — a no-regret investment. Put the prepared information into 2-05's files and 2-02's pgvector, and the next chapter mounts RAG on it.
date: 2026.07.16
label: Independence 10
title_html: Preparation is the <span class="accent">main body</span>,<br>AI the <span class="accent">last move</span>.
prev_slug: fastapi
prev_title: "Build an API — Expose Core Logic with FastAPI"
next_slug: ai
next_title: "Set Up Your Own AI — LLM and RAG"
---

# Make Your Knowledge Legible — Preparation Is the Main Body, AI the Last Move

By here, the parts are in place. Foundation, gate, documents, code, mail,
meetings, web, API — the tools stand. But the **information itself** that
flows over them is still scattered. Files sunk to the bottom of a shared
folder, paper and scanned PDFs, and the heaviest of all — **tacit knowledge
that lives only in someone's head.**

Before you put AI on top, there is work to do: **build information worth
putting it on.**

## Preparation is the main body, AI the last move

Don't get the order wrong. RAG, and your own AI, **stand only on prepared
information.** Put the cleverest model you like on scattered, unwritten
information, and what comes out is garbage (garbage in, garbage out).

So this chapter comes before the AI. The work is three things — **read the
paper (OCR), align the scatter (classification and structuring), write out
what's in people's heads (codifying tacit knowledge).**

And this preparation has two properties.

- It is **judgment only people can make.** What to keep, what to discard, how
  to structure it — this is the judgment of people who know the work, and it
  can't be handed off wholesale to AI (3-03). AI helps with the draft, but
  people decide.
- It is a **no-regret investment.** Structure the information and you recover
  it **even if you put no AI on it at all.** Personnel lock-in dissolves,
  handover gets easier, the business gets healthier. AI is merely the last
  move laid on top.

> Prepared information beats a cleverer model.
> Preparation is the main body. AI is the last move.

## Read the paper — OCR

The first barrier is **information a machine can't read.** Paper, scans,
image PDFs, handwriting.

- For fixed-form, typeset text, **Tesseract** and other OSS OCR turn it into
  text.
- For complex forms and figure-laden layouts, have an **open-weight vision
  model** (the local AI you stand up in 2-11) read it and render it to
  Markdown.

```bash
# example: give a scanned PDF a text layer (OSS OCR)
ocrmypdf --language eng input.pdf output.pdf   # searchable PDF + text
```

Aim the output at **Markdown and plain text.** Don't lock it into a
proprietary format — so that later anyone, and any AI, can read it (the
standard-format principle of 2-04).

## Align the scatter — classification and structuring

Next, **align** the scattered files.

- **One place** — gather them into the file-shaped document store you took
  back in 2-05.
- **Add metadata** — type, department, date, version, held in the filename or
  xattr (2-05).
- **Structure in Markdown** — headings, bullets, tables, into a form both
  machine and human can read. Let AI draft, and people fix.

Here AI is a powerful assistant. "Classify these 200 files by type and add a
summary" — classification and summarization both run on the local model
(2-11). But **the axis of classification is decided by people.** What counts
as "the same type" for the business is something only those who know the
business can tell.

## Write out what's in people's heads — codifying tacit knowledge

The heaviest, and most valuable, is **unwritten knowledge.** The vague parts
of a spec, the exception handling, the reasons things are the way they are —
all in the head of a veteran in charge. When this disappears, the system
becomes "it runs, but no one understands it" (the human dependency of 3-04).

The method is the same one used for core logic in 2-09 — **interview the
people on the ground, have AI draft, and have the ground confirm.**

- Ask and record the person in charge → AI drafts the transcription and
  structuring
- The person reads the draft and fixes the errors (this is the verification —
  only people can do it)
- Put the finalized version, in Markdown, into the document store

The moment tacit knowledge is **written down**, it becomes a transferable
asset. Independent of whether you ever put AI on it, the company gets stronger
right here.

## And then, mount the AI

Only once the prepared information is in place comes the next chapter.
**Embed the written, structured documents into 2-02's pgvector and mount RAG
on them** (2-11).

Skip the preparation and build RAG, and the sources are vague and the answers
unreliable. With the preparation done, an **AI that answers from your own real
data, with citations,** stands up cleanly.

> RAG quality is decided not by the model's cleverness but by **how well the
> information you mounted is prepared.**

## Summary

Before the AI, prepare the information.

- **OCR** — paper and scans into Markdown, with Tesseract or a vision model
- **Classification and structuring** — one place, aligned with metadata and
  Markdown (the axis decided by people)
- **Codifying tacit knowledge** — interview → AI draft → the ground confirms
  (same as 2-09)
- **AI is the last move** — mount the prepared information on pgvector; RAG is
  the next chapter (2-11)

Preparation pays off even without AI on top — personnel lock-in dissolves,
handover gets easier. **Preparation is the main body. Prepared information
beats a cleverer model.**

In the next chapter, on top of this prepared information, we set up our own AI.

---

## Related articles

- [2-05: Take Documents Back — Embed OnlyOffice Docs in PocketBase](/en/ai-native-ways/software/documents/)
- [2-09: Build an API — Expose Core Logic with FastAPI](/en/ai-native-ways/software/fastapi/)
- [2-11: Set Up Your Own AI — LLM and RAG](/en/ai-native-ways/software/ai/)
- [3-03: The Structural Diseconomy of the SIer Outsourcing Model](/en/ai-native-ways/software/sier-uneconomic/)
