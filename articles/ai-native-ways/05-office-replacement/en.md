---
slug: office-replacement
number: "05"
lang: en
title: "Changing Paperwork — A Realistic Path Away from Office"
subtitle: "Don't try to swap everything at once. Change what's inside"
description: Telling people "drop Office now" doesn't move organizations. There is no need to drop it. Make the substance Markdown and CSV; use Office as the converter at the entrance and exit. That alone slashes office work time and brings AI in as a colleague.
date: 2026.05.02
label: AI Native 05
title_html: Finish your paperwork<br><span class="accent">outside Office</span>.
prev_slug: python
prev_title: "Writing Logic — Have AI Write Python For You"
next_slug: business-systems
next_title: "Working with Business Systems — Rewrite via Parallel Operation"
---

# Changing Paperwork — A Realistic Path Away from Office

For office workers.

Telling you "drop Office" does not move the organization. Word files arrive. You are asked to report in Excel. You are told to present in PowerPoint. That is reality.

But **your own working surface can be separated from Office**. Hold the substance in Markdown and CSV; use Office as a converter at the entrance and exit. With this single step, AI becomes a colleague.

## Separate entrance, substance, and exit

Divide paperwork into three parts.

- **Entrance**: files arriving from others (Word, Excel, PDF, email)
- **Substance**: where you think, work, and store
- **Exit**: files going out to others (Word, Excel, PDF, email)

For most people, all three have lived in Office. A Word file arrives, you open it in Word, edit it in Word, send it back as Word. An Excel file arrives, you open it in Excel, process it in Excel.

As long as the substance is in Office, AI cannot be a colleague. Data trapped in formatting is hard for Claude to handle.

## Replace in stages

You don't have to change everything at once. Move in four stages.

**Stage one: write notes in Markdown**

Meeting notes, personal research, task lists — documents you use alone. Start writing them in Markdown. Make `.md` files in a text editor (VS Code, even Notepad).

That alone lets you ask AI "summarize this note," "lay out the points." The startup time of opening Word also disappears.

**Stage two: keep tables in CSV**

Product lists, customer lists, ledgers — simple tables belong in CSV. Column names in the first row, data below. When you want to view in Excel, open in Excel (CSV opens in Excel directly).

In CSV, you can ask Claude "aggregate this by month," "find the outliers."

**Stage three: turn repetitive work into Python**

"Every month, take the Excel from A, total it up, normalize the format, and send to the boss" — this becomes Python. As Chapter 4 showed, Claude writes it. You run it.

Once written, it works next month and the month after. Thirty minutes of work becomes thirty seconds.

**Stage four: leave Office at the entrance and exit**

The organization runs on Word and Excel. When a Word file arrives, convert it to Markdown (ask Claude). When sending back requires Word, convert Markdown to Word.

Don't change the organization's rules. **Change only your own substance.** Without anyone noticing, your working time drops dramatically.

## A concrete example: the monthly report

Take "the monthly sales report."

Old flow:
1. Open the sales data in Excel
2. Build a pivot table
3. Make a chart
4. Paste into Word
5. Write the prose
6. Convert to PDF
7. Email the boss

New flow:
1. Open the sales data as CSV
2. Aggregate with Python (Claude wrote it), output as a Markdown table
3. Draw the chart in Mermaid
4. Paste into a Markdown file
5. Write the prose in Markdown (Claude drafts it)
6. Convert Markdown to PDF (`pandoc` or Claude both work)
7. Email the boss

The time drops by more than half. **And you'll do the same task next month** — the Python script and Markdown template remain.

## Consideration for boss and colleagues

You may worry: "won't I look strange producing different documents?"

You won't. Convert to Word at the exit, and what reaches your boss is the same as before. **No one notices the process changed.**

What does change visibly is the quality and speed of the output. "The layout is more consistent," "the numbers line up," "fewer typos" — these emerge automatically from the Markdown + Python + Claude combination.

Eventually, a boss or colleague will ask "how are you doing this?" Then you can teach them.

## Handling email

Email is a large part of paperwork.

Hand a long email to Claude and ask "give me the points as bullets" — a summary comes back. Ask for a draft reply: "polite," "blunt," "short," "long." **You read, judge, and send.**

You can extract "last month's customer complaint count" from a mailing-list archive (export to text, hand to Claude).

Email is not structured data, but as long as it is text, Claude can process it.

## What happens

If you walk through these four stages, what happens?

- The same work takes less than half the time
- Overtime disappears
- The freed time goes to new kinds of work
- "Thinking work" and "processing work" become clearly separated
- "Processing work" is delegated to AI
- "Thinking work" becomes your real job

> Hand the work AI can do to AI, and you spend your time on the work only humans can do.

This is not a threat. It is **liberation**.

## In summary

You don't need to drop Office. Use Office as the converter at the entrance and exit.

Hold the substance in Markdown and CSV. Automate repetitive work with Python. Claude works as a colleague. The organization's rules stay the same.

Office work is the easiest occupation to transition to AI-native. You don't need to be technical. **If you can read Markdown, understand CSV, and ask Claude — that is enough.**

The next chapter moves to working with business systems. For technical roles.

---

## Related

- [Chapter 04: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Chapter 01: Writing Documents — Markdown as the Minimal Choice](/en/ai-native-ways/markdown/)
- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/)
- [Are You Still Using Windows and Office?](/en/blog/windows-office-facts/)
