---
slug: in-house-business-systems
title: "With Fable's Release, Building Business Systems In-House Gains the Edge"
subtitle: "Use the running system as your answer key, and rebuild it one piece at a time without stopping it — from vendor outsourcing to in-house development"
date: 2026.06.13
description: With the release of Claude Fable 5, Stripe migrated 50 million lines of Ruby in a single day. Just as Nadella says, a business application is essentially a CRUD database with business logic. And Fable can rebuild it — one process at a time — using the running system as the answer key and comparing outputs on the same inputs. Start with read-only reports and queries; with Ruby + Sinatra + raw SQL, drop the middle translation (ORMs and shared classes); and replace the old system without ever stopping it. The advantage in maintaining business systems shifts from vendor outsourcing to in-house development.
lang: en
label: Blog
category: Structural Analysis Notes
---

# With Fable's Release, Building Business Systems In-House Gains the Edge

Alongside the release of Claude Fable 5 (June 9, 2026), Anthropic announced a case study. The payments company Stripe ran the migration of a 50-million-line Ruby codebase with Fable, finishing in a single day work that would have taken the whole team more than two months. It rewrote running code in place — without stopping it, while it was still alive.

Microsoft's CEO Satya Nadella said on a December 2024 podcast: "A business application is, in essence, nothing more than a CRUD database (create, read, update, delete) with business logic on top." Quite right. And Fable can now write that business-logic-on-CRUD database, instantly and perfectly.

Why can we say "perfectly"? Because Fable does not stop at writing. It runs the code itself, checks it, fixes it where it is off, and checks again — repeating this at machine speed, tens of thousands of times. All it needs is something to check against. And a business system always has something to check against: **the running, current system.** Feed the newly written process the same input, and compare it with the current system's result. The correct answer is running right next to you, every day.

Stripe's code was well-maintained and easy for AI to handle, so it had Fable rewrite it in place. The old core systems we are dealing with here are not like that, so you leave them running, build the new side separately, compare the results on the same inputs, and swap in one piece at a time. The basis is the same — because Fable can repeat "write, check, fix" at machine speed.

## Four things to hand Fable

So, to build the new side, what do you hand Fable? Four things are enough.

**Table definitions. Inputs. Outputs. The manual.**

The shape of the database. The data that came in. The reports and screens that went out. The document that states the business rules. — Every company already has these. The manual states the rules in plain language. For rules that are missing, just tell Fable, "Ask me what needs to be decided," and it will draw them out. The one who answers is the person on the floor who knows the work.

You do not need to read the current code. **Leave the code where it is.**

## Start with the easy part

The contents of a business system divide, by difficulty, into three.

The easiest is **read-only processing**. Batches that produce reports. List and search screens. Because they do not change the database, nothing breaks even if you fail. Connect read-only, and you can start today. A report that would take weeks and tens of thousands of dollars if you asked a vendor can be done the same day with Fable.

Next is **processing that writes to a single table**. Work like registering a customer master record. Copy the production database and build on top of the copy. Since you are only using your own company's data yourself, you need no one's permission.

The hard part is only **processing that spans multiple tables**. Write an order, draw down inventory, post the receivable — implementation gets hard here. But in terms of the number of screens, this is only a part of the system. If you head here after getting used to the tools in the easy layers, the height is not beyond one person.

A large core system is the same. Peel it off in order, and there is no problem. Even if it looks large, what it does inside — take input on a screen, read and write to the database, aggregate, produce reports — is not that complicated. As Nadella says: a CRUD database with business logic. What was complicated was not the work, but the way it was built. Peel it one piece at a time, and each piece is a simple job.

Note that processing that **sends something outward** — email, payments, integration with external systems — **can come last.** For the time being, leave it running as it is on the current system. The new side records its results, and the current system reads them and sends them out as before — since what they share is the database, old and new coexist naturally. There is no need to rush, anywhere.

## Checking is just comparing

The way to verify is simple too. **Feed the newly written process the same input, and compare it with the current system's result.** This is not about running the whole system twice. For each piece you want to verify, run it at hand and compare — that is all. You do nothing to the current side. Use each day's input as it is, and every day becomes a full-scale test. There is no need to make test data.

There is no need to wait, either. A business system stores years of past inputs and databases. Replay last year's worth, and month-ends, closings, and special-case customers can all be verified overnight.

Only where a difference appears does the person on the floor look. A mistake on the new side, a rule you were never told, an old bug from long ago — any of them is a gain. Only someone who knows the work can judge whether it is correct. The Japanese workplace has always been good at cross-checking and confirmation.

## Stay on Java or C#, and Fable's power does not come out

You might think, "Why not just use Fable while staying on our current Java or C#?" That way Fable's power does not come out. Because shared classes and the giant components of the JRE / .NET tie everything together. Fable's strength is the loop: write, check, fix, check again. In a tied-together environment, every redo means re-reading the whole thing, and every fix ripples across the whole. And the time spent looking up the correct usage of a giant component is, by now, longer than the time spent writing.

At the center of the tying-together is the tool that hides SQL. It has names: Java's Hibernate, .NET's Entity Framework Core. The sales pitch was commonality — "the same code runs on any database." The reality is the opposite. Only the favored combination (Oracle Database for Hibernate, SQL Server for EF Core) runs comfortably; choose another database and you are plagued by small bugs and inefficiencies. It works, but it is hard to use. And the difficulty gets blamed on the database you chose. **Selling commonality while in reality excluding other databases** — it was a tool of monopoly more cunning than an outright ban.

The answer is simple. Take back the common tongue that was hidden. **Make each process independent, and write it in raw SQL.** A monthly aggregation is SQL plus a few dozen lines — complete in a single file. Share no code, no components. Share only the database. Fable is extremely good at SQL; ask in plain language and it writes even complex aggregations correctly, and fixes its own mistakes by running them itself. The human just compares the numbers that come out against the existing report, once.

Do this, and one business process becomes one file. What you hand Fable is just the table definitions and that one file. The impact of a fix, too, stays within that one file. Look at the one file and you understand the whole of that process — you do not need to go read the giant external components. Shared classes, the ORM, the giant components — they were a middle translation wedged between SQL and you. Drop the middle translation. In the AI era, this matters most.

## Keep the tools small

For the language, I recommend Ruby.

Not Python? you might ask. Python is a good language, but for business systems it has too many tools. The work of a business system — take input on a screen, read and write to the database — Ruby can handle all of it. And Ruby is simple. There is basically one way to write things, so Fable does not get lost. Speed is no worry either — the heavy computation is done by the database's SQL.

From Java or C# to Ruby — I imagine that sounds worrying. The track record answers it. **Stripe has run the world's payments on Ruby for 15 years.** 50 million lines — a scale no smaller than Japan's large core systems. It has kept running at that scale, and now it has even been proven that Fable can migrate it in a day. You are not switching to a small language. You are switching to a language with one of the largest track records in the world.

The framework is Sinatra. A small tool that just has you write routes and processing, barely changed since 2007. Because there is only one way to write, Fable's output stays stable.

**Ruby + Sinatra + raw SQL.** Write one process, in one file, in SQL. Do not tie processes together with shared classes. If they are not tied together, you can build one at a time, verify one at a time, and swap one at a time. Conversely, a system tied together with shared classes cannot have just one piece replaced. You can only switch everything at once — the dread of "switchover day" was created by the shared classes.

## Conclusion

Start with fixes to reports and inquiry screens. Order it from a vendor and it is weeks and tens of thousands of dollars in estimates and approvals. With Fable, it is the same day. Read-only processing breaks nothing even if you fail. The next fix — do not order it; have Fable do it. Right now. Ordering it from a vendor is, by now, a waste of money.

To say what to do in one line: **update the system without stopping it.** Have Fable write the code, compare it with the current system, and replace what matches. The current system keeps running to the end, so there is no dread of "switchover day." Swapping servers one at a time without stopping the processing — that is the ordinary procedure everyone in infrastructure has always followed. You just do the same thing, one process at a time. Even if a mistake turns up after a swap, no worry. Tell Fable, and the fix is quick. Because each process is independent, the impact is closed within that one piece.

The materials are all there. The method is just to compare. The tools are small. What remains is only to begin.

Let me also write down the price of not beginning. Look at the amount you pay every year in maintenance and operations outsourcing. Millions a year — for a large company, hundreds of millions. The same work can now be done in-house, the same day. If you keep paying the same amount next year and the year after, that is entirely wasted. And leaving it unaddressed becomes an expense you cannot account for. For a company, it can become grounds for a shareholder derivative suit; for a local government, for a resident audit request.

With Ruby + Sinatra, you can do it.

One more thing: the language is not the place to be dogmatic. If you are good at Python, developing with Python + FastAPI is fine too. Building the system in Ruby and using Python only when you need data analysis is also fine. What matters is not the language but the way of building — make processes independent, write SQL raw, and update without stopping.
