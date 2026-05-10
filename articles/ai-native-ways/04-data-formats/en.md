---
slug: data-formats
number: "04"
lang: en
title: "Holding Data — Think in JSON, CSV, YAML"
subtitle: "Excel is not a table — it is a collection of formatting"
description: An Excel sheet looks like a table, but it is really a bundle of formatting wrapped around data. The structure underneath is buried. JSON, CSV, and YAML hold the structure bare. That is what AI can read directly.
date: 2026.05.02
label: AI Native 04
title_html: Hold data as <span class="accent">structure</span>, not as tables.<br><span class="accent">JSON / CSV / YAML</span> make that possible.
prev_slug: design
prev_title: "Designing — With Mermaid and Claude Design"
next_slug: office-replacement
next_title: "Changing Paperwork — A Realistic Path Away from Office"
---

# Holding Data — Think in JSON, CSV, YAML

Switch the tools you hold data in to JSON, CSV, or YAML.

That single change turns data into "structure" that AI can read and write. Most data that has been carefully arranged inside Excel is locked in a cage of formatting. Bare it, and AI starts working as a colleague.

## Excel is not a table

Open an Excel file. Borders, merged cells, color-coding, bold, font sizes, comments, filters, pivot tables. All of these are saved together with the "data."

You set out to total "2025 sales," and before you know it you are tweaking cell colors. "Blue is confirmed, red is provisional, yellow needs review" — this rule is not in the filename, not in the comments, not in any other document. **It exists only in the head of the person who built the file.**

When that person leaves, the rule disappears. Excel expresses structure through formatting, and in doing so removes the structure itself from the file.

This is not a flaw in Excel. Excel is a tool for humans to lay out tables. Formatting comes to the front because that is what it is for.

But the essence of data is not formatting. The essence is structure. "This is a date. This is an amount. This is a customer ID." The definitions are what make data data. Formatting is just decoration for display.

## JSON holds structure as it is

JSON is text. It writes the shape of data as it is.

```json
{
  "customer": "Yamada Farm",
  "orders": [
    { "date": "2026-04-01", "item": "cabbage", "qty": 12, "price": 180 },
    { "date": "2026-04-08", "item": "onion",   "qty": 24, "price":  95 }
  ]
}
```

That alone expresses a customer with multiple orders, with hierarchy intact. The structure — "a customer has many orders" — is visible the moment you open the file. **There is no formatting metadata.** No colors, no borders, no fonts. They are not needed.

Formatting is needed at display time. It is not needed at storage time.

## CSV holds tables as they are

For pure tables — rows and columns only — CSV is the right shape.

```csv
date,item,qty,price
2026-04-01,cabbage,12,180
2026-04-08,onion,24,95
```

No borders, no color-coding, no filters. The first row is column names; everything after is values. That is all.

CSV is old. It has been around for more than thirty years. That is exactly why almost every piece of software can read it. AI reads it without trouble. Excel itself can open CSV (and conversely, exporting Excel to CSV strips formatting but preserves data).

> Data you want as a table belongs in CSV. If you want to view it in Excel, open it in Excel.

CSV inside, Excel only at the entry. With that, your data stays in a form AI can read.

## YAML holds settings as they are

For configuration — the parameters that drive a system — YAML is the right shape.

```yaml
site:
  name: aiseed.dev
  language: en
  features:
    - markdown
    - rss
    - sitemap

build:
  output: html/
  cache: true
  threads: 4
```

It is more readable to humans than JSON, and it allows comments. Lines starting with `#` are comments. You can leave a note inside the configuration about *why* a setting is what it is.

YAML is also what powers Markdown frontmatter (the section between `---` at the top of the file).

## What AI reads is structure

This is the decisive point.

When you hand Claude an Excel file, it first unzips the .xlsx, reads the XML, strips formatting metadata, and pulls out cell values. **What AI needs is bare structure from the start.**

Hand Claude JSON, CSV, or YAML, and there is no conversion. It reads them directly. It writes them directly.

> Hold data as structure, and AI becomes a colleague.

This is not a metaphor. It is a technical fact. As long as your interaction with AI is text-based, JSON, CSV, and YAML are the shared language for data.

## Which one to use

The choice is simple.

- **Tables (rows and columns)** → CSV
- **Hierarchy (nesting)** → JSON
- **Configuration (with comments)** → YAML

You can use all three in one project. Invoice data in JSON, product master in CSV, system configuration in YAML — pick what fits the shape.

If you are unsure, ask Claude "what shape should this data take?" and it will read the data and answer.

## When an Excel file lands in your inbox

As long as you work inside an organization, Excel files will keep arriving. What do you do with them?

It is easy. Hand them to Claude and say "make this CSV" or "make this JSON."

Read the CSV/JSON. Think. Transform it. If your response needs to be Excel, convert the CSV/JSON to Excel (Claude can do that as well).

**Keep your own working surface as structured data.** Absorb the formats your organization demands at the entry and exit only. The substance — the structure — stays intact.

## Readable in ten years

A 20-year-old Excel file (.xls format) sometimes opens with broken layout in today's Excel. Macros stop working. Fonts get substituted.

CSV is just a text file. In ten years, in twenty years, any text editor can read it. AI can read it even more easily. JSON and YAML are the same.

> Save the structure. Throw away the formatting.

Formatting decorates the present. Structure crosses time.

## In numbers

10,000 rows of sales data: 1.2 MB as `.xlsx`, 280 KB as CSV. **One-quarter.** Formatting metadata accounts for four times the actual data.

Aggregating monthly sales via Excel pivot table: 5 minutes of clicking, no reproducibility. The same aggregation in `pandas`: 3 lines of code, 0.1 seconds to run, the Python script reusable next month.

Monthly job extracting specific columns from 100 `.xlsx` files: half a day in VBA. With `pandas` and `glob`, processed in a single sweep, 30 seconds. **Ask Claude; the code arrives immediately.**

Claude's recognition rate when handed JSON / CSV: near 100% (structure is bare). When handed `.xlsx`: depending on format, 70–80% (merged cells and formatting degrade it). **The more you hold data as structure, the less AI gets it wrong.**

## In summary

Change your tools, and the way you handle data changes.

From Excel to JSON, CSV, YAML. A single step that shifts data from "appearance on screen" to "structure you can process." AI becomes a colleague. Still readable in ten years.

The four chapters so far have laid out the shared practices — Markdown, Mermaid, Python, and structured data formats (JSON / CSV / YAML, plus Parquet + DuckDB at scale). These are the minimal AI-native stack that does not depend on occupation.

From the next chapter, we move into work-type-specific practices. First, for office workers.

---

## Related

- [Chapter 01: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Chapter 02: Writing Documents — Markdown as the Minimal Choice](/en/ai-native-ways/markdown/)
- [Prologue: Office for paperwork, Java/C# for business systems — but AI runs on Python and text](/en/ai-native-ways/prologue/)
- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/)
