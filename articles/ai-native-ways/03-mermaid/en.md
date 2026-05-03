---
slug: mermaid
number: "03"
lang: en
title: "Drawing Diagrams — Save the Structure with Mermaid"
subtitle: "A PowerPoint diagram dies the moment you copy it"
description: A diagram drawn in PowerPoint becomes an image the moment it is pasted, and loses its structure. Mermaid writes diagrams as text. Version-controllable. AI-readable. Editable. Diagrams, too, should be held as structure.
date: 2026.05.02
label: AI Native 03
title_html: Don't draw diagrams just to throw them away.<br>Save them as text with <span class="accent">Mermaid</span>.
prev_slug: data-formats
prev_title: "Holding Data — Think in JSON, CSV, YAML"
next_slug: python
next_title: "Writing Logic — Have AI Write Python For You"
---

# Drawing Diagrams — Save the Structure with Mermaid

Switch the tool you draw diagrams in to Mermaid.

That single change turns diagrams into "structure" that AI can read and write. Most diagrams drawn in PowerPoint or draw.io are locked in a graveyard called "image." Rewrite them as text, and diagrams too become colleagues.

## A PowerPoint diagram dies the moment you copy it

Someone draws a beautiful organizational chart in PowerPoint. They paste it into a Word report. The Word file gets passed to someone else. That person thinks "I want to move this box a little."

Then what happens? **The box won't move.** The moment it was pasted into Word, the diagram became an image. Where the original PowerPoint file lives, no one knows. The person who wants to change it has no choice but to redraw the entire diagram on top of the image.

This is not a flaw in PowerPoint. PowerPoint is a tool for humans to build slides. It assumes a diagram lives within a single slide. Reuse is a secondary concern.

But the essence of a working diagram is not the slide. The essence is structure. "A depends on B," "the process flows X → Y → Z" — the relationships are what make diagrams diagrams. Appearance is just decoration for display.

## Mermaid writes diagrams as text

Mermaid is text. Symbols express the diagram.

```
graph TD
  A[User] --> B[Web Server]
  B --> C[(Database)]
  B --> D[Cache]
  C -.->|slow| B
```

That alone expresses four nodes and the arrows between them. "User hits the web server, server accesses database and cache" — visible the moment you open the file.

Mermaid handles flowcharts, sequence diagrams, class diagrams, ER diagrams, Gantt charts, state diagrams — almost every kind of diagram you need at work. GitHub, Notion, VS Code, and most Markdown previewers render Mermaid natively.

## Version controllable

Put a PowerPoint file in Git, and you cannot see the diff. "What changed between the December slide and the January slide?" — you cannot tell. Because it is binary, Git can only see "everything changed."

Mermaid is text. Git diffs work normally. "An arrow was added here." "A node was renamed." All visible. Reviewable. Approvable. Reversible.

> Writing diagrams as text puts diagrams under the same quality control as code.

This matters. The familiar problems of organizational documentation — "we have diagrams but cannot tell if they are accurate" or "no one knows who last updated this and when" — disappear.

## AI can read it

Mermaid source is something Claude reads directly.

"Add a new node to this diagram." "Reverse the arrow direction." "Convert this to a sequence diagram." All can be asked of Claude. Paste back the Mermaid it returns, and the diagram is updated.

PowerPoint diagrams cannot do this. Hand a diagram as an image, and Claude sees a "picture," but the structure is only inferred. With Mermaid, there is no inference.

## What to write in Mermaid

Most diagrams you encounter at work.

- System architecture diagrams
- Process flowcharts
- Organization charts
- Customer–order ER diagrams
- Project Gantt charts
- State transitions (account created → awaiting verification → active, etc.)
- API sequence diagrams

Diagrams you would otherwise "draw in PowerPoint, export as image, paste into a report" are nearly all replaceable with Mermaid.

Complex pictures — photos, hand-drawn sketches, artistic diagrams — belong to other tools. But diagrams whose purpose is "to convey structure" are Mermaid territory.

## You don't need to draw it yourself

Take this one step further.

You don't need to memorize Mermaid syntax. Tell Claude "draw this system in Mermaid" and it will. Paste the result, see the rendered diagram, and instruct what to fix: "make this arrow thicker," "put the cache above the database." Claude will rewrite the Mermaid.

In other words, **you don't even need to memorize the symbols**. If the structure is clear in your head, Claude will apply the symbols.

What you need is to be able to **read** Mermaid. Once you can, you can correct what Claude produced. That, too, takes only a few hours.

## Readable in ten years

Open a 20-year-old PowerPoint file in today's PowerPoint, and fonts get substituted, shapes shift in position. The .ppt format is on its way out.

Mermaid is just a text file. Even if the Mermaid renderer evolves, the syntax barely changes. In ten years, in twenty years, any text editor can read the diagram source.

> Hold diagrams as structure too.

PowerPoint diagrams decorate the moment of display. Mermaid diagrams cross time.

## In summary

Change your tools, and the way you handle diagrams changes.

From PowerPoint to Mermaid. A single step that moves diagrams from "the graveyard of images" to "structure you can process." AI becomes a colleague. Version control works. Still readable in ten years.

The next chapter moves on to writing logic. "The skill is not writing code; the skill is using code" — about Python and Claude.

---

## Related

- [Chapter 02: Holding Data — Think in JSON, CSV, YAML](/en/ai-native-ways/data-formats/)
- [Chapter 01: Writing Documents — Markdown as the Minimal Choice](/en/ai-native-ways/markdown/)
- [Prologue: Office for paperwork, Java/C# for business systems — but AI runs on Python and text](/en/ai-native-ways/prologue/)
