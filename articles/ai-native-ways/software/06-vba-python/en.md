---
slug: vba-python
number: "06"
part: "1"
lang: en
title: "Move VBA to Python — Rewrite Excel Macros with AI"
subtitle: "Move the business macros no one can fix anymore to Python, with the running version as your answer key"
description: Chapter 5's first worked example. The Excel VBA macros at the foot of nearly every company — black boxes whose author is gone and no one can fix — get moved to Python with AI. Use the running macro as the answer key and move them one at a time, comparing the same inputs and outputs. The spreadsheet (human I/O) stays in Excel; the processing (the machine) moves to Python — code that is readable, testable, and runs anywhere.
date: 2026.06.30
label: Introduction 6
title_html: Turn the VBA <span class="accent">black box</span><br>into readable Python.
prev_slug: customer-codev
prev_title: "Customers Co-Develop with AI"
next_slug: website
next_title: "Build a Website — In Dialogue with AI"
---

# Move VBA to Python — Rewrite Excel Macros with AI

As Chapter 5 showed, a customer can build with AI. The first worked example sits
at the foot of nearly every company — **Excel VBA macros.** Years of business
logic are written there; the author is gone, and no one can fix it. Move it to
**Python** with AI.

## Why move to Python

- **VBA is tied to Excel.** Once the author leaves, it tends to become a **black
  box** no one understands
- **Python is readable, testable, and runs anywhere** — one of the languages AI
  handles best
- **The spreadsheet (human I/O) stays in Excel; the processing (the machine)
  moves to Python** — split by role (covered in detail in the Independence
  part's data foundation)

## How — use the running version as the answer key

Not all at once. One macro at a time, with the **running version as the "answer
key."**

1. Hand the existing macro to AI and have it **explain what it does** (put the spec into words)
2. Have AI **write Python** with the same inputs and outputs
3. Run the old macro and the new Python against the same Excel, and **compare the results**
4. Fix until they match; once they match, switch over

```python
# e.g. a VBA aggregation macro, in Python (Polars)
import polars as pl
df = pl.read_excel("sales.xlsx")
df.group_by("dept").agg(pl.col("sales").sum()).write_excel("dept_summary.xlsx")
```

People enter and read in Excel; the machine crunches in Python. When the old and
new outputs match, remove the old macro — without stopping, one at a time.

## In dialogue, little by little

You don't have to spell out the spec up front. **Work with AI in dialogue,**
comparing against the running version and fixing as you go. Ask on the spot when
something is unclear. This is exactly the way of building from Chapter 5.

## Summary

- **Turn the VBA black box into readable Python**
- **Use the running version as the answer key** — compare I/O and move one at a time
- **The spreadsheet stays the human's tool; processing moves to the machine (Python)**

Next, another worked example — building a **website** with AI in dialogue.

---

## Related articles

- [Chapter 5: Customers Co-Develop with AI](/en/ai-native-ways/software/customer-codev/)
- [Parent series, Chapter 2: Writing Logic — Have AI Write It in Python](/en/ai-native-ways/python/)
- [Parent series, Chapter 7: Living with Business Systems — Rewrite by Running in Parallel](/en/ai-native-ways/business-systems/)
