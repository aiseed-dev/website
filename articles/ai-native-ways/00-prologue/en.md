---
slug: prologue
number: "00"
lang: en
title: "Office for paperwork, Java/C# for business systems — but AI runs on Python and text"
subtitle: Information processing is becoming simple work that AI can do
description: OpenAI and Anthropic run on Python. Data is Markdown, JSON, YAML. Between AI-native tools and the standard tools of the enterprise, a decisive divide runs through. Office, Java, and C# — get rid of them.
date: 2026.05.01
label: AI Native 00
title_html: Paperwork is <span class="accent">Office</span>.<br>Business systems are <span class="accent">Java/C#</span>.<br>But AI is <span class="accent">Python and text</span>.
prev_slug:
prev_title:
next_slug: python
next_title: "Writing Logic — Have AI Write Python For You"
---

# Prologue — Office for paperwork, Java/C# for business systems, but AI runs on Python and text

Paperwork runs on Office. Business systems run on Java and C#. But AI runs on Python and text.

Here lies a decisive divide.

## Change your tools

OpenAI runs on Python. So does Anthropic. Their SDKs are Python-first. Data is Markdown, JSON, YAML. This is no accident — it comes from the very structure of AI itself.

Word files, Excel sheets, PDFs all need to be converted to text before AI can read them. Each conversion strips away formatting and structure. Legacy Java and C# code, when shown to AI, yields lower-quality advice than Python would.

> Between AI-native tools and the standard tools of the enterprise, a decisive divide runs through.

## Get rid of them

**Office, Java, and C# — get rid of them, fast.**

The work these tools were built for — formatting documents, building tables, creating screens, writing code — has become simple work that AI can do.

People are still carrying heavy tools to perform tasks that AI could handle. This is what is happening, right now, in most workplaces.

Change the tools, and your thinking changes. Change your thinking, and you start spending time on work only humans can do.

## This concerns everyone

This is not a story for engineers alone.

For office workers: switch from Word to Markdown, and from Excel to JSON / SQLite (drop CSV — it loses information; chapter 4). AI immediately becomes someone you can consult.

For sales: shift your reports from formatted documents to structured data. AI returns analysis and proposals.

For people on the shop floor: keep procedures in plain text. AI translates them, supports new-hire training.

For sole proprietors: keep invoices, contracts, and blog posts in Markdown. Claude becomes, effectively, your employee.

For developers: write new things in Python. For websites, use HTML and CSS and the bare minimum of JavaScript. You don't need React.

## Python is for everyone

Drop the prejudice that Python belongs to engineers.

Converting Excel files. Extracting data from emails. Organizing PDFs. Standardizing file formats. These are everyday tasks for office workers and sole proprietors.

In Python, they take a few lines. And you don't need to write the code yourself. **Ask Claude in your own language, and the code comes back.** Just run it.

The skill is not writing Python. The skill is using Python. This is the new literacy.

## The minimal stack

It does not change by occupation.

```
documents : Markdown
data      : JSON / YAML / SQLite / OnlyOffice / Parquet (drop CSV)
processing: Python
web       : HTML + CSS + JavaScript
diagrams  : Mermaid
```

All text. AI can read and write it directly. It will still be readable in ten years.

## One way of working, every domain — Linux + Python + AI

The toolkit looks like many pieces, but **the practice underneath
them is one**:

> **Linux + Python + AI as your assistant** — with this alone, you
> can handle **writing, software development, design, embedded —
> all in the same way**.

| Domain | The same practice |
| --- | --- |
| **Writing** | Markdown / AsciiDoc / MyST / LaTeX — written as text, versioned in Git, Claude proofreads and translates |
| **Software development** | Python / HTML+CSS+JS — written as text, versioned in Git, Claude writes the code |
| **Data work** | JSON / SQLite / Parquet — held as structure, analyzed in JupyterLab + Polars + Claude |
| **Design** | Mermaid / Claude Design / D3 / Blender / CAD — written as scripts, Claude writes the syntax |
| **Embedded** | Design and verify in Python, **Claude translates to C / C++** (Chapter 9) |

All the same motion: **hold things as text and code → record history
in Git → Claude writes, the human decides**. Once you've learned
this practice, **changing domain no longer means relearning
different tools, different cultures, different subscriptions**.

### The entry is a little hard, but only once

Honestly — **the entrance is a bit of work**:

- Get comfortable with Linux (terminal, file system, `ls` / `cd` /
  permissions)
- Learn how to *use* Python (`uv` install, libraries, JupyterLab)
- Three Git motions (`add` / `commit` / `push`)
- Pick one editor (Zed / VSCodium / Neovim)
- Stand up Forgejo on a miniPC of your own (Chapter 2)

Cross that threshold and **every domain feels the same**. Word
mechanics, Excel mechanics, Figma mechanics, PowerPoint mechanics,
each CAD package's mechanics, each 3D tool's mechanics — you don't
have to keep memorizing them **separately**.

> **Pay the "one-time small entry cost" and the return — "every
> domain, the same way" — lasts a lifetime.** The total cost of
> separately mastering Office, Figma, Photoshop, SolidWorks, and
> every other specialized tool is far higher than the cost of
> Linux + Python + AI.

### Windows / Mac give you the same practice too

We said "Linux," but **the practice itself is the same on Mac and
Windows**:

- **Mac** (macOS): Unix-based — terminal (zsh), Homebrew, Python.
  Feels nearly identical to Linux.
- **Linux**: Ubuntu / Debian / Fedora / Arch — any of them.
- **Windows**: WSL2 + Ubuntu gives you a Linux compatibility layer
  — Microsoft itself ships this.

So **you can start tomorrow on whatever machine you have today**.
Once you're comfortable, expand to a miniPC or a Linux box — that
ties into the self-hosting story in Chapter 2.

### AI carries the syntax — that's what makes "the same way" possible

Why does "every domain, the same way" work? Because **Claude writes
the syntax**:

- Markdown symbols, Python grammar, HTML/CSS selectors, Mermaid
  notation, Polars APIs, Altair declarations, D3 selections,
  Blender's `bpy`, Build123d's geometry, Forgejo's `systemd` unit,
  C pointers — **Claude writes all of it**.
- What humans learn: **what to make, what structure to hold it in,
  whether the result is right**.
- Once you have this practice, entering a new domain becomes:
  **"this is something to ask Claude for."**

The D3 / Blender / ComfyUI / CAD section of Chapter 3, the embedded
work of Chapter 9 — these are all the **same extension** of the same
practice. The era of "every specialist tool with its own
operations" is replaced by the era of **"extend one practice across
every domain."**

### In short — desk work, unified

Writing documents, building tables, drawing charts, composing
diagrams, writing code, building slides, building web pages,
building apps, designing parts in CAD, building 3D models, writing
hardware control, generating reports, replying to email, drafting
contracts — **all of these get handled the same way**.

The need to **separately master office software, design software,
development environments, CAD packages, and countless SaaS** is
gone. Desk work as a whole consolidates into **one practice**:
Linux + Python + AI.

> In short, **desk work becomes unified**.
> This is the destination this book's toolkit aims for.

## Hand the fine-grained work to AI — AI is genuinely capable of it

What makes "every domain, the same way" possible is simple. **The
fine-grained work can be handed off to AI in its entirety** — and
**AI has the capability to actually carry it through**.

Nearly all of what humans have spent time on as "fine-grained work"
can be handed to AI:

- **Remembering syntax** — Markdown symbols, Python grammar, CSS
  selectors, SQL, Mermaid notation, Polars APIs, Altair
  declarations, D3 selections, Blender's `bpy`, CAD script
  syntax, `systemd` units, C pointers
- **Drafting** — email, reports, contracts, proposals, blog posts,
  documentation, meeting notes, release notes
- **Formatting and conversion** — Word to Markdown, Excel to
  Parquet, English to Japanese, PDF to text, image to text, table
  to bullet list
- **Boilerplate** — web templates, configuration files, init code,
  test scaffolding, Dockerfiles, CI configs
- **Lookups** — how to use an API, which library to pick, what an
  error means, summaries of papers and precedents
- **Proofreading, polishing, translation, summarization**

These all go to Claude. And **Claude really does have the capacity
to carry them through**:

- Writes hundreds of programming languages and dozens of markup
  variants **in parallel**.
- Drafts business writing, technical writing, regulatory text,
  even academic text.
- Converts between formats **almost instantly**.
- Generates context-aware boilerplate **in bulk**.
- Answers lookups **faster than searching yourself**, and
  structured.

### Treat AI like a colleague or junior — trust the handoff, check the result

Two common mistakes here:

- **"Just to be safe, I'll do this fine-grained piece myself."**
- Or the opposite: **"AI said so" — accepted without checking.**

Both are old habits. The right approach is simple: **treat AI the
way you would treat a colleague or junior staff member.**

> **Trust enough to delegate, then check the result properly** —
> that is the heart of this book's practice with AI.

When you hand work to a capable colleague or junior, you do both
sides:

**The "trust enough to delegate" side:**

- **State clearly what you want done** (inputs, outputs, conditions,
  deadlines).
- Don't over-specify every step — once the scope is set, leave the
  middle to them.
- Don't take it back with "it's faster if I do it myself."

**The "check the result properly" side:**

- **Read what comes back, and verify it** (don't accept mechanically).
- For the parts that aren't quite right, **say what to change, in
  words**.
- If several rounds still don't land, **rethink the way you're
  asking**.
- **Make the important decisions yourself.**

The same applies to Claude:

- Output doesn't match expectations → ask for revisions in words.
- An error appears → paste the error, ask for cause and fix.
- Several rounds still don't resolve it → rethink the prompt, or
  rethink the design (Chapter 1's "Don't fear 'it didn't run'").
- Numbers, proper nouns, citations, whether code actually runs —
  **verify with your own eyes.**

**This isn't a special concession for AI.** Code you wrote yourself,
a report a colleague hands you — **you run the same checks, the same
tests, the same number-matching**. "I wrote it myself" doesn't make
it correct (typos, mistaken assumptions, arithmetic slips,
edge-case misses — everyone produces these). **What changes is only
that the writing now goes through AI. The verification practice
doesn't change.**

**Not "constantly second-guess," and not "swallow whole."**
**Trust the handoff, check the result properly** — exactly the
practice you'd use with a colleague.

> Verification and testing are **independent of who wrote the code
> or the document**. Yourself, a colleague, AI — the work is the
> same.

Getting used to this is the foundation of the book's practice. As
Chapter 5 will show, the moment you step outside Office, AI shifts
from "tool" to "colleague" — and **preparing to treat it as one
starts here.**

### What remains for humans is judgment

After the fine-grained work goes to AI, what stays with humans:

- **Deciding what to make**
- **Choosing what structure to hold it in** (Chapter 4)
- **Judging whether the output is correct**
- **Deciding who to deliver it to and how**
- **Taking responsibility**

These are the territory AI cannot take ("The limits of efficiency"
section, above).

> **Fine-grained work to AI. Judgment to humans.**
> Drawing this line changes the way of working itself.

## Tools shape thought

Write in Word, and you focus on formatting. Write in Markdown, and structure comes first.

Think in Excel, and your ideas become whatever fits in a table. Hold data in JSON, and the relationships are made plain.

Design in Java, and you start with class hierarchies. Write in Python, and you state what you want, directly.

Build with React, and you wrestle with build configs and bundle sizes. Write in HTML, and you focus on the content itself.

> Changing your tools is changing your thinking.

## In numbers

A Word file (50 KB, 5,000 characters) handed to Claude consumes about 8,000 tokens. The same content as Markdown takes 4,000 tokens. **Roughly half.** AI usage costs drop proportionally.

Extracting paragraphs containing "fertilizer" from 100 Word files: 30 minutes to write VBA. As Markdown, `grep -A 3 fertilizer *.md` does it in 0.1 seconds.

A 1.2 MB Excel `.xlsx` (10,000 rows of sales data) becomes **60 KB as Parquet**. **1/20.** Types preserved, faster to transfer to Claude, faster to parse.

Continuing to use Office, Java, and C# means paying more than double the AI costs every day.

## What becomes possible

From a single Markdown file, simultaneously generate **a print-quality PDF, a beautiful web page, presentation slides, an EPUB e-book, and AI-ready input.** The same source spreads across every medium.

`pandoc + xelatex` produces **book-publication-quality PDFs** from Markdown. Cover, table of contents, headers, page numbers, references, figure numbers — academic and commercial publishing standards generated by one command.

Markdown-ify a decade of internal documents, and Claude can analyze the organization's **decision patterns**. "How many times in the past five years was the same debate repeated," "which policies stuck and which faded" — all quantifiable. **The organization's collective knowledge becomes a searchable asset.**

Python and text are not just about saving money. They are the toolkit that lets **individuals and small teams produce work that previously required large corporations or expert teams.**

## Another purpose — autonomy, decentralization, diversity

There is a second purpose to these practices, beyond efficiency.

"Everyone using the same AI is more efficient" — society today reads
AI primarily as a **centralization-and-efficiency tool**. Microsoft 365
Copilot, ChatGPT Enterprise, Google Workspace AI — that's the direction
the industry pushes. If a whole organization rides on the same vendor's
AI, you do get a unified front. Support costs drop.

But when that AI is wrong, **the whole organization is wrong in the same
direction**. When the data policy changes, everyone's data flows in the
same direction. When the price goes up, everyone pays the same increase.
When the standard of judgment is uniformized, **diversity disappears
from the organization**. The Mythos-era single point of failure has
everyone riding it at once.

This book's practices go the other way. **Each person holds their own
tools, their own data, their own judgment.** AI is used, but as **an
extension of yourself** — not as an extension of a vendor. Markdown is
yours, JSON / YAML / SQLite is yours, Python scripts are yours, decisions are yours.

This is not a story about efficiency. It is a story about **individual
autonomy, organizational diversity, and societal resilience**. With
distribution, when one falls others keep moving. Each person grows their
own judgment in their own context. **Diversity itself is strength.**

> AI-native tools are not only tools for efficiency. They are tools for
> **individual autonomy and societal diversity** as well.

## Closing

Paperwork runs on Office, business systems on Java and C#, but AI runs on Python and text.

What changes in the AI era? **Information processing becomes simple work that AI can do.**

Formatting documents, building tables, writing emails, writing code, summarizing reports — these have become work to hand off to AI. Humans no longer need to do them.

Office, Java, and C# are tools from an era when humans handled information processing. Carrying these heavy tools to do work that AI could do — this is what is happening in most workplaces today.

What remains for humans is deciding **what to do, why to do it, and how to judge the results**. To focus there, hand the processing to AI. The tools for that are Python and text.

**Get rid of the old ones, fast.** Then AI becomes a colleague.

The chapters that follow walk through specific practices, area by area.

---

## Related

- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/)
- [Structural Analysis 12: AI and the Individual Business](/en/insights/ai-and-individual/)
- [Are You Still Using Windows and Office?](/en/blog/windows-office-facts/)
- [Learning Debian with Claude](/en/claude-debian/)
