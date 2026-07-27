---
slug: claude-debian-server-07-database
lang: en
number: "07"
title: Chapter 7 — The Database as a Foundation
subtitle: When to use SQLite and PostgreSQL, and installing PostgreSQL
description: The server itself can be rebuilt. The only thing that cannot be rebuilt is the data. So the place where your data lives is the foundation you should design first. Grasp the difference between a pile of files and a database, split the territory between SQLite and PostgreSQL, and put PostgreSQL 17 on your Debian 13 box so you own your own database — this chapter lays that foundation.
date: 2026.06.10
label: Claude × Debian Server 07
prev_slug: claude-debian-server-06-systemd-services
prev_title: Chapter 6 — The Service as a Unit
next_slug: claude-debian-server-08-fastapi
next_title: Chapter 8 — Running Your Own App
cta_label: Learn with Claude
cta_title: The data is the only thing you cannot rebuild.
cta_text: A server can be reinstalled as many times as you like. But your records, photos, and ledgers happen only once. Rather than scattering them across someone else's cloud, you gather them into your own database on your own machine. This is the chapter where you lay the foundation.
cta_btn1_text: Continue to Chapter 8
cta_btn1_link: /en/claude-debian/server/08-fastapi/
cta_btn2_text: Back to Chapter 6
cta_btn2_link: /en/claude-debian/server/06-systemd-services/
---

## Why a Chapter on Databases

One idea runs underneath this whole server sub-series. **The server itself can be rebuilt. The only thing that cannot be rebuilt is the data.** If the OS breaks, you reinstall it. If a config file is wrong, you rewrite it. An app can be reinstalled. But the household records you built up over three years, your family's photos, your work notes — once those are lost, they do not come back. This idea gets its full treatment in [Chapter 10](/en/claude-debian/server/10-backup/), but there is one thing that absolutely must come first: **designing where your data lives, as a foundation.**

And one more thing. Photos in that cloud, the budget in another app, notes in yet another service — before you know it, the data of your daily life is scattered across the servers of several different companies. **As long as your data stays scattered across other companies' cloud services, you never get the initiative back. You gather it into your own database, on your own machine.** This is the step that gives concrete form to the "data sovereignty" we confirmed in Chapter 1.

So what is the difference between a pile of files and a database? CSVs, spreadsheets, text files here and there — you can hold data in those too. But as the volume grows and you start touching it from several places, you hit walls. Can you produce "total food spending last month" in one shot (searching)? Have you registered the same item twice (consistency)? Will two apps writing at the same time corrupt it (concurrent access)? A database is a place for **"data that has structure,"** built from the ground up to handle exactly these things.

This foundation pays off from here on out. The app you build with FastAPI in Chapter 8, and the service you publish to the outside world in Chapter 9 — boiled down, both run on top of this database. So now, we lay the foundation.

## Section 1 — When to Use SQLite and PostgreSQL

When you hear "database," the first two names that come up are SQLite and PostgreSQL. But these two are not competitors. They are **tools with different territory.** Neither is superior; each is suited to different things.

**SQLite** turns an entire database into **a single file.** One file called `notes.db` is the whole database. No server process is needed. Zero configuration. `apt install sqlite3` and you are done. The basic way to use it is embedded inside an application, and it is ideal for a single writer, small scale, and personal apps. It looks humble, but it is in fact the most widely deployed database in the world — countless copies of SQLite run inside your phone and inside your browser.

**PostgreSQL** is a full-blown database that **runs resident as a service.** It is a resident of the `systemctl` world you learned in Chapter 6: it stays up and waits for connections. Multiple apps and multiple users can connect at the same time, there is permission management for who can do what, and you can connect over the network. Its transactions — the mechanism that bundles a set of operations into "do all of it or none of it" — are the real thing.

Which to choose? Here are the axes for the decision.

| Axis | Leans SQLite | Leans PostgreSQL |
|---|---|---|
| Who writes | A single app of yours | Multiple apps / people |
| Concurrent access | Mostly solo | Many at once |
| Data volume | Small to medium | Medium to large |
| Want separate permissions? | No | Yes, per user |
| Connecting over the network | Mostly no | Yes |
| Operational effort | Near zero | Managed as a service |

The policy is this. **SQLite first, PostgreSQL once it grows up — that is the natural path.** Start small, and move when it outgrows the file. But in this server sub-series there is a separate consideration. **Put PostgreSQL on the server from the start and get used to it.** Far better to get your hands dirty while it is still an experiment box than to scramble to learn it once production needs it. We do that in the back half of this chapter.

First, let's touch SQLite with a minimal example, to feel the foundation in your hands.

```bash
# Install SQLite (the command-line tool)
sudo apt install sqlite3

# Open a database (= a single file) at ~/data/notes.db
mkdir -p ~/data
sqlite3 ~/data/notes.db
```

Once you are at the `sqlite3` prompt, type just a few lines.

```sql
-- Create a table to hold notes
CREATE TABLE notes (id INTEGER PRIMARY KEY, body TEXT, created TEXT);

-- Insert a row
INSERT INTO notes (body, created) VALUES ('first note', '2026-06-10');

-- Pull it back out
SELECT * FROM notes;

-- List tables, then leave
.tables
.quit
```

The ones starting with a dot, like `.tables` and `.quit`, are SQLite's own commands; everything else is SQL, the common language. That little is all it takes — `~/data/notes.db` is now a perfectly real database in a single file. Backing it up or copying it means dealing with this one file — that is the lightness of SQLite.

### Ask Claude ①: Have It Judge Which One Suits

> On my Debian 13 server, I want to run / build the following:
> [e.g., a personal budget app, a book list shared with family, a web app I'm building to learn, inventory tracking… list whatever comes to mind]
>
> For each, judge whether SQLite or PostgreSQL is the better place for the data, with reasons. Make explicit the axes you used (number of writers, concurrent access, whether separate permissions are needed, etc.). For any where "SQLite first, PostgreSQL once it grows up" is reasonable, add a rough sign for when to migrate.

Putting "which one for my use case" into words up front makes the rest of the design easier. Have Claude judge it, and the things you were unsure about get a reasoned line drawn through them.

## Section 2 — Installing PostgreSQL

As planned, we put PostgreSQL on the experiment box. On Debian 13 (trixie), what you get is **PostgreSQL 17.**

```bash
sudo apt install postgresql
```

This is where Chapter 6 pays off. **PostgreSQL starts running as a service the moment you install it.** So you check it with exactly the craft from Chapter 6.

```bash
systemctl status postgresql
```

If it shows `Active: active`, it is already running. On Debian, PostgreSQL is managed in units called "clusters" (just grasp this as the mechanism that lets you keep multiple versions side by side). The config files live under `/etc/postgresql/17/main/`.

```bash
# Peek at where the config files are
ls /etc/postgresql/17/main/
```

### The First Gate: "Peer Authentication"

Right after installing, typing `psql` straight away gets rejected. The first gate is **peer authentication.** In Debian's default setup, you can reach PostgreSQL's admin user `postgres` **only while you are the OS user `postgres`.** The mechanism authenticates by matching the OS-side user name against the DB-side user name — that is peer authentication. So the first entrance looks like this.

```bash
# Launch psql as the OS user postgres
sudo -u postgres psql
```

This drops you at a `postgres=#` prompt. `\q` leaves it.

### Create Your Own Role and Database

Doing everything as the `postgres` user is poor manners. In the spirit of Chapter 5's "least necessary privilege," create a role (user) for your app and a dedicated database.

```bash
# Create a role called myapp (set its password interactively)
sudo -u postgres createuser --pwprompt myapp

# Create a database myappdb owned by myapp
sudo -u postgres createdb -O myapp myappdb
```

Then try connecting as `myapp`.

```bash
psql -h localhost -U myapp -d myappdb
```

Adding `-h localhost` switches you from peer authentication to password authentication, so it asks for the password you just set. Now you have your own role and DB, with their own entrance.

### A Defensive Check — Where Is It Listening?

In Chapter 5 we practiced the craft of "confirming the attack surface (the entrances you've exposed) with your own eyes." We do that for the database too. See for yourself **where PostgreSQL is waiting for connections.**

```bash
ss -tlnp | grep 5432
```

PostgreSQL's port is 5432. If the address column of the output shows **`127.0.0.1:5432`**, that means "reachable only from within the same machine." It is not listening to the outside world.

```
LISTEN 0  244  127.0.0.1:5432  0.0.0.0:*  ...
```

This is the default state of PostgreSQL on Debian, and **external exposure is closed by default.** That is a safe default. If you ever want to connect from another machine, you would edit `listen_addresses` in `/etc/postgresql/17/main/postgresql.conf` and `pg_hba.conf` — but **before you open it, talk through the threat model with Claude first.** As Chapter 5 drilled in, exposing a database to the outside is a heavy decision. As long as it stays closed to `127.0.0.1`, the attack surface stays near zero.

### Ask Claude ②: Have It Explain Your PostgreSQL's Current State

> I have just installed PostgreSQL 17 on my Debian 13 server. When I checked its state, I got this output:
> ```
> [paste the output of systemctl status postgresql]
> ```
> ```
> [paste the output of ss -tlnp | grep 5432]
> ```
> Explain, one piece at a time, what state my PostgreSQL is in. In particular, tell me where it is waiting for connections (open to the outside, or closed), and which part of the output I can read that from. How would you assess this state from a security standpoint?

The trick is to paste **both** the `status` and `ss` output. "Is it running (status)" and "where is it open (ss)" are separate questions, and Claude reads the two against each other to assess your current defensive posture.

## Section 3 — Your First Table, and the Entrance to SQL

The database foundation is in place. Make one small example inside it, and peek at the entrance to SQL. Let's make the subject a household budget.

```bash
psql -h localhost -U myapp -d myappdb
```

Once you are at the `myappdb=>` prompt, create one table.

```sql
-- Budget table: date, item, amount
CREATE TABLE kakeibo (
    id     SERIAL PRIMARY KEY,
    hizuke DATE       NOT NULL,
    item   TEXT       NOT NULL,
    amount INTEGER    NOT NULL
);

-- Insert a few rows
INSERT INTO kakeibo (hizuke, item, amount) VALUES
    ('2026-06-01', 'rice', 2800),
    ('2026-06-02', 'vegetables', 650),
    ('2026-06-03', 'book', 1980);

-- Pull it back out
SELECT * FROM kakeibo;
```

Learn PostgreSQL's own handy commands too.

```sql
\d kakeibo   -- see this table's structure (schema)
\dt          -- list tables
\q           -- leave
```

`SERIAL` is a type that "auto-assigns a running number," `DATE` is a date, and `INTEGER` is an integer. `NOT NULL` is a constraint meaning "no empties allowed," and thanks to it, a "record with no amount" cannot slip in — that is one example of consistency.

### SQL Is Not a Thing to Memorize Anymore — It's a Thing to Have Claude Write and You Read

Here is the crucial point. **SQL is no longer something to memorize; it is something to have Claude write and you read.** Queries like "monthly totals" or "a breakdown by item" can be written without reciting SQL grammar from memory. The way to do it is simply to show Claude the table structure and tell it what you want in plain language.

```sql
-- First, grab this output to show the structure
\d kakeibo
```

Paste that `\d kakeibo` output and ask, "Write the SQL to produce monthly totals, and explain what each clause means." Don't swallow the returned SQL whole — read through what each clause means at least once. It is the same "have it write, you review" style as the unit files in Chapter 6. When an error comes up, paste the error message as-is. The "hand over the log as-is" craft you picked up in the main series' [Chapter 8 troubleshooting](/en/claude-debian/08-first-troubleshooting/) works here too.

### Ask Claude ③: Have It Design a Table for Your Own Data

> On PostgreSQL 17 on my Debian 13 server, I want to manage the following data:
> [e.g., reading log (book title, author, finish date, rating), inventory (item name, quantity, purchase date), customer notes… whatever data you want to accumulate]
>
> Design a table to hold this data. Write the `CREATE TABLE` statement, and for each column explain why you chose that type (TEXT / INTEGER / DATE / SERIAL, etc.), one by one. For any columns that should not allow empties (NOT NULL), add the reason too.

Table design is the first — and most consequential — judgment you make with a database. By having Claude explain the choice of types, you become able to read "why this shape" yourself. Do it once, and you can take a fair guess at the next table on your own.

## Section 4 — The Entrance to Protecting Your Data

Let me plant one piece of foreshadowing for Chapter 10 here. Having gone to the trouble of gathering data into a database, if you protect it the wrong way, the worst can happen: when the moment comes, all you have on hand is a **corrupt backup.**

What you must not do is **directly copy the files of a running database.** If you duplicate a file that PostgreSQL or SQLite is in the middle of writing, with `cp`, you freeze a half-written, incomplete state — and when you try to restore, it's broken. A dangerous method. The correct entrance is to have the database itself emit a "backup-shaped" output.

```bash
# PostgreSQL: dump myappdb as text (a collection of SQL statements)
pg_dump -h localhost -U myapp myappdb > ~/data/myappdb-backup.sql

# SQLite: copy safely with the dedicated command, even while running
sqlite3 ~/data/notes.db ".backup ~/data/notes-backup.db"
```

What `pg_dump` emits is **text.** Inside, it is a sequence of `CREATE TABLE` and `INSERT` statements — humans can read it, git can diff it, and you can even paste it to Claude to check the contents. That is a strength a binary copy does not have. SQLite's `.backup` is a dedicated command that, instead of copying the file directly, takes a copy in a state that is safe even mid-write.

Here we only go as far as getting our hands on "the correct entrance." **Automation (taking it at a fixed time every night, reliably) and — most important of all — the "restore drill" come in earnest in Chapter 10.** A backup is only half done if you merely take it; it is complete only when you can put it back — and that story is two chapters out.

### Ask Claude ④: Have It Write the Backup Steps for Your DB Setup

> My Debian 13 server has the following databases:
> [e.g., PostgreSQL 17's myappdb, SQLite's ~/data/notes.db]
>
> For each, write the minimal steps to take a correct, uncorrupted backup. Add a one-liner, understandable to a beginner, on why you must not directly copy the files of a running database. Also suggest where to put the backup files and how to name them (e.g., include the date).

This ④ is optional. But handing your setup to Claude once gives you a foundation for moving on to automation in Chapter 10.

## Summary

What you did in this chapter:

1. From the idea that "the only thing you cannot rebuild is the data," confirmed what it means to design where your data lives as a foundation.
2. Sorted out the difference between a pile of files and a database (searching, consistency, concurrent access, data that has structure).
3. Split the territory of SQLite and PostgreSQL in a table, and set the policy of "SQLite first, PostgreSQL once it grows up."
4. Touched SQLite as a single file, and installed PostgreSQL 17 on Debian 13.
5. Got past peer authentication, created your own role and DB, and confirmed with `ss`, with your own eyes, that it is only open on 127.0.0.1.
6. Peeked at the entrance to SQL with a budget table, and picked up the "have Claude write, you read" pattern.
7. Confirmed, hands-on, the correct entrance to uncorrupted backups (`pg_dump` / `.backup`).

What you hold now:
- A SQLite database that is a single file (`~/data/notes.db`).
- PostgreSQL 17 running as a service, with your own role and database (`myapp` / `myappdb`).
- Your first table holding "data that has structure" (`kakeibo`).
- The dialogue pattern of handing over `\d` output and having SQL written for you.
- How to take an uncorrupted backup (the entrance to Chapter 10).

The data foundation is in place. The OS and the apps can be rebuilt, but the data you have just started loading onto this foundation cannot — carrying that weight, we move on. In [Chapter 8, "Running Your Own App,"](/en/claude-debian/server/08-fastapi/) we build **your own app** on top of this foundation with Python and FastAPI — settling the directory layout and running it as a systemd service, together with Claude.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
