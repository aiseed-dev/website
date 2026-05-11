---
slug: python
number: "01"
lang: en
title: "Writing Logic — Have AI Write Python For You"
subtitle: "Externalize macros, charts, and pivots into Python — the first thing to do"
description: Externalize the macros/VBA, charts, and pivots embedded in Excel (and Word) into Python. This is the first thing to do. With AI helping, nothing is hard anymore. You don't have to write it — ask Claude in your own language and the code comes back. Hit Shift+Enter in a JupyterLab cell and the result appears immediately.
date: 2026.05.02
label: AI Native 01
title_html: For code, the skill is not <span class="accent">writing</span>.<br>The skill is <span class="accent">using</span>.
prev_slug: prologue
prev_title: "Office for paperwork, Java/C# for business systems — but AI runs on Python and text"
next_slug: markdown
next_title: "Writing Documents — Markdown as the Minimal Choice"
---

# Writing Logic — Have AI Write Python For You

Switch the tool you write logic in to Python.

That single change turns repetitive work into one-time work. Reformatting Excel, totaling emails, extracting from PDFs, batch-renaming files. Most "30 minutes of manual office work" finishes in 10 lines of Python. **Claude writes it.** A human runs it.

## Python is for everyone

Drop the prejudice that Python belongs to engineers.

Python is the most readable language AI can write in. Unlike Java or C#, no long class definitions or type annotations are needed. The processing you want to express stands as it is.

```python
import csv

with open("orders.csv") as f:
    rows = list(csv.DictReader(f))

total = sum(int(r["qty"]) * int(r["price"]) for r in rows)
print(f"Total: {total}")
```

That is all it takes to read a CSV and compute a total. No prior knowledge required. "Open the CSV, multiply qty by price, sum it up" — that is what it says.

The skill of writing this code is not required. The skill of **reading** it is enough. If you can read it, you can judge whether the code Claude returned looks right.

## Not "writing" — "using"

Here is the new literacy.

Old common sense: learning programming = memorizing language syntax, designing algorithms, writing code.

New common sense: using programming = articulating what you want to process, having Claude write code, running it, checking results.

Compare the time it takes to memorize Excel functions with the time it takes to start having Claude write Python for you. The latter is dramatically shorter. Excel functions only work inside Excel; Python works on any data.

> The skill is not writing. The skill is using. This is the new literacy.

You don't need to learn "how to write code." You need to learn "how to put what you want to process into words." That is not technical skill — it is mental clarity.

## How to ask Claude

There are only three tricks to having Claude write Python for you.

**One: state the input and the output**

"Read the Excel file `orders.xlsx`, total sales per product, and write to CSV `summary.csv`." Input file and output file, both with their formats clear, and Claude does not get lost.

**Two: ask one thing at a time**

Not "do everything," but "first, write the code to load the data; next, the code to aggregate; last, the code to write CSV." Step by step. You can verify behavior partway. When something is wrong, it is easy to back up.

**Three: look at the result and correct**

The first version is rarely perfect. Run it, look at the output, send back "this is wrong" or "change this." **The conversation converges on the right answer.** This is what "using" code instead of "writing" it looks like.

## What kinds of work become Python

Most everyday tasks for office workers and sole proprietors.

- Gather a specific sheet from 100 Excel files and merge them
- Extract amounts from email bodies into a CSV
- Convert PDFs into searchable text
- Resize and rename images in bulk
- Scrape product information from a website
- Sort invoice PDFs into folders by month
- Walk through Markdown files and build a table of contents

Work that "a human keeps doing manually" becomes Python. Once written, it works next month and the month after.

## Have a runtime

To use Python, you need a runtime.

Three options.

**One: install Python on your own machine**

Run with the `python` command. Files on your machine just work. The first step has a small hurdle, but once installed, it works forever. Mac and Linux often have Python preinstalled. On Windows, install from the Microsoft Store.

**Two: use Claude's code execution**

Paste code into Claude and ask "run this." For light processing, you don't need to set up an environment locally.

**Three: use Google Colab**

Google's browser-based Python service. Free. Suited to heavier data processing.

If unsure, just start. Ask Claude "I want to set up a Python environment. Ask me what suits me, and tell me." It will guide you based on your situation.

## Don't fear "it didn't run"

In the early days, you'll often see errors when running Python.

That is normal. Copy the error text into Claude and say "I got this." Claude will identify the cause and return corrected code. **An error is not the end; it is input for the next instruction.**

> Paste the error text into Claude. Claude fixes it. You move on.

You don't need to feel "programming isn't for me." If you can paste an error message, that is enough.

## Readable in ten years

Python has been around for over thirty years. Some code broke in the migration from Python 2 to 3, but Python 3 code will keep running for another 10 or 20 years.

Excel VBA macros may stop working with each new Office version. Python code is text, dependencies are explicit, and AI can re-read it.

> Hold logic, too, as structure.

VBA runs today's Excel. Python keeps running across time.

## In numbers

Monthly job extracting amounts from 100 invoice PDFs: by hand, **4 hours**. With Python written by Claude, **3 seconds**. Next month, the same script in 3 seconds. **A 4,800x gap on the first run; infinite afterward.**

Office work aggregating 50 Excel files monthly: 5 minutes per file × 50 = **4 hours**. Write the `pandas` Python script once, and `python aggregate.py` runs in **10 seconds** thereafter.

Python learning curve: for the "ability to use," practicing reading Claude-written code for one week is enough to start using at work. The traditional self-study path to "ability to write" takes 6 months. **A 24x gap.**

Reaction to errors: searching and trial-and-error solo takes 30 minutes to 2 hours. Pasting the error text into Claude returns the cause and corrected code in 30 seconds. **60x faster or more.**

## In summary

Change your tools, and the way you process work changes.

From Excel manual labor to Python plus Claude. A single step turning repetitive work into one-time work. The skill of writing is not required. The **skill of using** is enough.

The next chapter moves on to writing documents — from Word to Markdown. With Python tooling now in place, the substance of documents can also move from formatting to structure.

---

## Related

- [Chapter 02: Writing Documents — Markdown as the Minimal Choice](/en/ai-native-ways/markdown/)
- [Chapter 03: Designing — With Mermaid and Claude Design](/en/ai-native-ways/design/)
- [Chapter 04: Holding Data — Think in JSON, CSV, YAML](/en/ai-native-ways/data-formats/)
- [Structural Analysis 12: AI and the Individual Business](/en/insights/ai-and-individual/)
