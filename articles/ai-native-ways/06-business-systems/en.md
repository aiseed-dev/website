---
slug: business-systems
number: "06"
lang: en
title: "Working with Business Systems — Augment Legacy Assets with AI"
subtitle: "Don't break Java and C#. Redraw the boundary"
description: You don't need to rewrite business systems in Python. Treat 100,000 lines of Java code as a data source. What AI should rewrite is not the substance but the boundary. Keep the legacy assets intact, and write new work in Python with AI.
date: 2026.05.02
label: AI Native 06
title_html: Don't <span class="accent">break</span> the legacy.<br><span class="accent">Augment</span> it with AI.
prev_slug: office-replacement
prev_title: "Changing Paperwork — A Realistic Path Away from Office"
next_slug: web
next_title: "Building for the Web — Back to HTML+CSS+JavaScript"
---

# Working with Business Systems — Augment Legacy Assets with AI

For those responsible for business systems.

When someone says "drop Java and C#, rewrite everything in Python," it doesn't sound realistic. Of course it doesn't. Core systems running for ten or twenty years carry a deep accumulation of business knowledge. They contain edge cases not in any document. The risk of rewriting is far greater than the risk of staying as you are.

You don't need to rewrite. **Just redraw the boundary.** Keep the substance in Java or C#; write new functionality in Python with AI. Connect them across the boundary with data (JSON / CSV).

## "Rewrite everything" is a trap

Most "rewrite the legacy in Python" projects fail.

The reason is simple. Old code carries business rules that are not in any document. "Billing closes on the 10th of July, but extended to the 5th of the following month to account for the Obon holidays" — no one remembers this rule. It exists only in the code.

Rewrite, and the rule is lost. You notice a few months later, when something is billed wrong.

**Code is acting as the spec.** Rewriting the code is rewriting the spec. That is harder than building a new system from scratch.

## Redraw the boundary

The new way of relating to legacy is to redraw the boundary.

Existing systems keep running in Java or C#. New functionality runs in Python and Claude, taking data (CSV or JSON) from the existing systems as input. The output of the new functionality goes back to the existing systems as CSV or JSON.

```
Legacy core system (Java/C#)
       │
       │  CSV / JSON export
       ↓
New processing layer (Python + Claude)
       │
       │  CSV / JSON import
       ↓
Legacy core system (Java/C#)
```

Don't touch the internals of the legacy. **Make only the boundary surface AI-native.**

This way you keep the business knowledge and gain a 10x speedup in new development. Small risk, large effect.

## Treat as a data source

Treat the legacy system as a data source.

Have the Java core system emit CSV or JSON every day. Read the database directly if appropriate. If there's an XML API, hit it from Python.

You are not "calling the legacy system directly." You are "running new processing on the data the legacy system emits." **The boundary is data, so AI can touch it.**

## Example: monthly anomaly detection

Suppose you want a "detect unusual movement" mechanism on monthly sales data.

Old method:
1. File a change request against the core system
2. Write a design document
3. Get reviews
4. Implement in Java
5. Test
6. Submit a production release request
7. It works months later

New method:
1. Have the core system export sales CSV daily (just one new job)
2. Run anomaly detection in a Python script (Claude writes it)
3. Output to CSV or a Slack notification
4. Working the next day

The core system is untouched. **You add only one new layer at the boundary.**

If you want better detection, you tune the Python script. If you want to stop, you stop the job. Impact on the core system is zero.

## Push business knowledge into Markdown

The legacy carries business knowledge. Push it out into Markdown a little at a time.

Java comments, SQL queries, operations runbooks, past incident reports — hand them to Claude and have them organized in Markdown. Make documents humans can read about "what this code does" and "what rules are embedded here."

It does not have to be perfect. **What matters is that business knowledge accumulates in a form AI can read.** Next time the same business is touched, Claude can refer to the past Markdown. It compounds.

This is also insurance for the day a system needs replacing. If a spec exists separately from the code, the risk of replacement falls.

## SQL is still strong

The center of business systems is the database. SQL is a 50-year-old language and will run for another 50 years.

Hit the existing database with SQL from Python. Ask Claude "write the SQL for this requirement," and complex queries return in seconds. **You barely need to learn SQL.** Reading is enough.

The same applies to old PL/SQL or T-SQL. Claude writes both.

## Escape vendor lock-in

Oracle, SAP, Salesforce, Microsoft business products — these are not selling "products." They are selling "the situation in which you have to keep using the product."

Two ways out.

**One: full replacement at once**

This nearly always fails (as above).

**Two: redraw the boundary and shift the center of gravity gradually**

New features are written outside. Have the product emit CSV / JSON. Eventually, what the product holds is "past data and past rules" only. New value is created outside.

After a few years, the product's importance has dropped. At contract renewal, you have the evidence to say "we may not need this anymore." **You take the initiative back from the vendor to your side.**

> Don't break the legacy. Redraw the boundary, and move with AI on the outside.

## In summary

Don't rewrite business systems. Keep them.

New work happens outside the boundary, in Python and Claude. Data flows across the boundary as CSV and JSON. Business knowledge is gradually pushed out as Markdown.

This way you keep the business knowledge of legacy assets and gain a 10x speedup. Small risk, large effect.

The next chapter moves to building for the web. "You don't need React. HTML, CSS, and JavaScript are enough." A return to the origin.

---

## Related

- [Chapter 05: Changing Paperwork — A Realistic Path Away from Office](/en/ai-native-ways/office-replacement/)
- [Chapter 04: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/)
- [Structural Analysis 11: Regulation Redesign](/en/insights/regulation-redesign/)
