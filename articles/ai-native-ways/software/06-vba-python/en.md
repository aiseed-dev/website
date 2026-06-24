---
slug: vba-python
number: "06"
part: "1"
lang: en
title: "Move VBA to Python — Rewrite Excel Macros with AI"
subtitle: "Move security-fragile business macros to Python, with the running version as your answer key — Excel stays, rewritten in the language AI handles best"
description: Chapter 5's first worked example. The Excel VBA macros at the foot of nearly every company — security-fragile, their author gone, no one able to fix them — get moved to Python with AI. Python is the language AI itself is written in, so AI handles it best. Polars and openpyxl read, write, and edit Excel (.xlsx) directly, and they are easy for humans too (so OnlyOffice, which keeps OOXML, fits better than LibreOffice's ODF). Use the running macro as the answer key and move them one at a time.
date: 2026.06.30
label: Introduction 6
title_html: Fragile VBA into the<br>language AI loves — <span class="accent">Python</span>.
prev_slug: customer-codev
prev_title: "Customers Co-Develop with AI"
next_slug: website
next_title: "Build a Website — In Dialogue with AI"
---

# Move VBA to Python — Rewrite Excel Macros with AI

As Chapter 5 showed, an individual can build their own tool with OSS and AI. The
first worked example sits at the foot of nearly every company — **Excel VBA
macros.** Years of business logic are written there; the author is gone, and no
one can fix it. Move it to **Python** with AI.

## Why move to Python — and urgently

- **VBA is security-fragile.** Macros have long been a primary malware vector;
  Excel macros in email attachments were a staple of attacks. Carrying business
  VBA around is itself a risk — **it should be moved urgently**.
- **Once the author leaves, it becomes a black box.** VBA is tied to Excel and
  keeps running with no one able to read or fix it.
- **Python is what AI handles best.** AI itself is written in Python, and by now
  **AI writes AI in Python**. So have it write Python, and the accuracy is
  highest. It is also readable, testable, and runs anywhere.

## You don't have to give up Excel — Polars and openpyxl

"Move to Python" makes people brace to abandon Excel. Not so. Python has
**Polars** and **openpyxl**, which **read, write, and edit Excel files (.xlsx)
directly.** People keep entering and reading in Excel; only the processing (the
machine's work) moves from VBA to Python.

```python
# e.g. a VBA aggregation macro, in Python (Polars)
import polars as pl
df = pl.read_excel("sales.xlsx")
df.group_by("dept").agg(pl.col("sales").sum()).write_excel("dept_summary.xlsx")
```

Polars and openpyxl are **easy for humans, too**. The APIs are
straightforward and the code is readable — unlike the VBA black box, a person
can read it later and fix it.

One principle here: **never dump Excel to CSV.** CSV throws away all formatting,
formulas, and cell layout. **Keep it as .xlsx and handle it directly with Polars
and openpyxl** — Polars for aggregating and transforming values, openpyxl for
editing in place with formatting preserved; neither goes through CSV.

One more caveat. **LibreOffice and OpenOffice save in ODF (.ods)**, which Polars and
openpyxl handle **poorly**. So if you replace the spreadsheet application itself,
choose **OnlyOffice**, which keeps the same **OOXML (.xlsx)** as Microsoft — it
meshes directly with the Python tools (covered in Independence Chapter 4's
document foundation).

## How — use the running version as the answer key

Not all at once. One macro at a time, with the **running version as the "answer
key."**

1. Hand the existing macro to AI and have it **explain what it does** (put the spec into words)
2. Have AI **write Python** with the same inputs and outputs
3. Run the old macro and the new Python against the same Excel, and **compare the results**
4. Fix until they match; once they match, switch over

When the old and new outputs match, remove the old macro — without stopping, one
at a time. Ask AI on the spot when something is unclear. This is exactly the way
of building from Chapter 5.

You can also **build it from scratch without decoding the old macro**. What the
macro does, the person running the business should already know — so just tell AI
what you want and rebuild it in dialogue. **Using the running version as the
answer key, or building fresh in dialogue — either way works.**

## Summary

- **Fragile VBA → Python, urgently** — on security grounds alone, it cannot wait
- **Excel stays (.xlsx)** — don't dump to CSV (it loses formatting); handle
  .xlsx directly with Polars and openpyxl. If you replace it, use OnlyOffice
  (keeps OOXML), not ODF
- **Use the running version as the answer key** — compare I/O and move one at a time
- **Python is what AI handles best** — AI itself is written in Python

Next, another worked example — building a **website** with AI in dialogue.

---

## Related articles

- [Chapter 5: Customers Co-Develop with AI](/en/ai-native-ways/software/customer-codev/)
- [Independence Chapter 4: Take Documents Back — OnlyOffice Docs](/en/ai-native-ways/software/documents/)
- [Parent series, Chapter 2: Writing Logic — Have AI Write It in Python](/en/ai-native-ways/python/)
- [Parent series, Chapter 7: Living with Business Systems — Rewrite by Running in Parallel](/en/ai-native-ways/business-systems/)
