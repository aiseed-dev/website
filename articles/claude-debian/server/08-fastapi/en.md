---
slug: claude-debian-server-08-fastapi
lang: en
number: "08"
title: Chapter 8 — Running Your Own App
subtitle: Directory layout, Python, and FastAPI
description: This book never uses containers — apps run as a plain directory plus a venv plus a systemd service. That is exactly why the convention for where things go, instead of a container, is what creates order. Decide a directory layout, build a minimal API with Python and FastAPI, turn it into a systemd service, and run it on top of Chapter 7's database — Claude writes the code; you decide the structure, run it, and protect it.
date: 2026.06.10
label: Claude × Debian Server 08
prev_slug: claude-debian-server-07-database
prev_title: Chapter 7 — The Database as a Foundation
next_slug: claude-debian-server-09-publishing
next_title: Chapter 9 — Opening Up to the Outside World
cta_label: Learn with Claude
cta_title: An app runs in a plain directory.
cta_text: You can run your own app without a container. A plain directory, a venv, and a systemd service — those three are enough to stand up your own app on your own server. Claude writes the code. You decide the structure, run it, and protect it.
cta_btn1_text: Continue to Chapter 9
cta_btn1_link: /en/claude-debian/server/09-publishing/
cta_btn2_text: Back to Chapter 7
cta_btn2_link: /en/claude-debian/server/07-database/
---

## Why a Chapter on Running Your Own App

Chapter 6 handed you "the service as a unit," and Chapter 7 set down "the database as a foundation." A pattern for running things, and data to put on it. With both in hand, you can finally stand up your own app.

This book never uses containers. There is no Docker, no Kubernetes. **Apps run as a plain directory plus a venv plus a systemd service** — that is this book's consistent stance. Why? Containers are convenient, but they hide what is happening underneath. What this book aims for is to lift the lid and widen the range you can fix with your own hands. So your app, too: put code in a directory, create a Python virtual environment, run it with the systemd from Chapter 6 — and that alone makes it work.

But not using containers means you take on the "tidying" a container would otherwise have done for you. Where the code goes, where the secrets go, what is tracked in git, what gets backed up. **What creates order in place of a container is the convention for your directory layout.** This chapter starts by deciding that convention.

And one more thing. **In 2026, the app's code is written by Claude.** You do not type it out line by line. The development craft you picked up in the main series, [Chapter 15 "Developing with Claude"](/en/claude-debian/15-claude-development/) — put the spec into words, have it written, review it, run it and fix it — you now practice on a server. Writing the code is Claude's job; **deciding the structure, running it, and protecting it is yours.**

## Section 1 — Deciding the Directory Layout

Without a container, the convention for where things go is the whole foundation. Here I present this book's convention as one example, not as an absolute — once you understand the meaning, change it to your own taste.

Put the app's home at `/srv/myapp/`. `/srv` is the place Debian has long provided for "data served by this machine." Split the contents like this.

```
/srv/myapp/
├── app/        the code itself (tracked in git)
├── .venv/      the Python virtual environment (disposable, not in git)
├── .env        secrets such as connection info (chmod 600, not in git)
└── data/       files the app writes, if any (optional)
```

Keep four roles cleanly separate. **`app/` is the code**, tracked in git. **`.venv/` is the virtual environment**, created in the next section — because it is "disposable, recreatable at any time," it does not go in git. **`.env` is secrets** — it holds things like the database password, so `chmod 600` makes it readable only by its owner, and it absolutely never goes in git. **`data/` is where files the app writes live**, but only if you need it.

The data itself goes into the PostgreSQL (or SQLite) you set up in Chapter 7. You create `data/` only when you need to store "files as such," like uploaded images; structured data is left to the database.

Don't roll your own logs either. **Leave logging to journald.** You learned `journalctl -u myapp` in Chapter 6: as long as you run as a systemd service, lines the app prints to standard output are gathered into the journal automatically. Better to leave it to systemd than to create your own log file and worry about it bloating.

And run the app as a **dedicated system user**. This is the practice of "least privilege" drilled in Chapter 5. Even if the app is taken over, the attacker can only do what that user can.

```bash
# Create a dedicated user named myapp (no login, home at /srv/myapp)
sudo adduser --system --group --home /srv/myapp myapp
```

`--system` makes a non-login system user, `--group` creates a group of the same name, and `--home` sets the home directory. Matching the database role name `myapp` from Chapter 7 with the OS user name `myapp` here keeps your head from getting tangled later.

Once it exists, hand over ownership of the whole house and keep strangers out.

```bash
# Make everything under /srv/myapp belong to myapp
sudo chown -R myapp:myapp /srv/myapp

# Only the owner and its group may enter
sudo chmod 750 /srv/myapp
```

In the container way of working, "who may touch what" was carried by the container's walls. In this book, which uses no containers, **Linux ownership and permissions become those walls.** The app holds only the `myapp` user's privileges and cannot write outside `/srv/myapp`. The material of the wall differs; the isolation is the same. In Section 3 we make this wall one layer thicker with systemd's sandboxing.

Now make the single most useful table in this chapter. What, where, tracked in git, and is it a backup target.

| What | Where | In git | How to recover |
|---|---|---|---|
| Code | `/srv/myapp/app/` | yes | restore from git |
| Virtual environment | `/srv/myapp/.venv/` | no | recreate (next section's steps) |
| Secrets (connection info) | `/srv/myapp/.env` | no | **back up (Chapter 10)** |
| Files the app writes | `/srv/myapp/data/` | no | back up (Chapter 10) |
| The data itself | PostgreSQL `myappdb` | no | DB dump (Chapter 7 `pg_dump`) |

Stare at this table and you see Chapter 10's backup philosophy appearing directly in the directory layout. **Code can be restored from git. The venv can be recreated. The only things you cannot recreate are `.env` and the data.** So what backups truly need to protect narrows down to those two. Lay out the structure this way and "what do I need to protect?" reads straight off the layout itself. Conversely, jumble everything into a single directory and that distinction vanishes.

### Ask Claude ①: Design Your App's Layout and Tables

> I want to build my own app on a Debian 13 server:
> [e.g. a personal household-budget API, a memo share for the family, a small inventory tracker — describe concretely what you want to make]
>
> Without using a container, propose a layout that follows the convention "under `/srv/appname/`, split app/ (code), .venv/, .env, and data/." Along with that, design the PostgreSQL 17 tables to hold this app's data, in Chapter 7's style (with `CREATE TABLE` statements and the reason for each column's type). Include a mapping table of "tracked in git / recreatable / should be backed up."

Put what you want to make into words first, and design the layout and tables in one pass. With the map of the structure in hand, every section ahead turns into "filling in that map."

## Section 2 — Python and FastAPI

The structure is decided. Now build the contents. There are many web frameworks, but here we use **FastAPI**. Three reasons. It **becomes a web API with little code**. Its **documentation (`/docs`) grows automatically**. And it is **one of the frameworks Claude is most fluent in**. This book's stance is "have Claude write the code," so choosing something Claude is good at makes sense.

### Why a venv Is Mandatory — PEP 668

First, there is a gate here. Debian 13's system Python is marked "externally managed," and hitting `pip install` directly is **refused**.

```
error: externally-managed-environment
```

This is not a bug. It is **a design to keep the Python the OS runs on separate from the Python for your app** (set down in an agreement called PEP 668). Adding packages to the system Python on a whim could break the very Python foundation Debian itself uses. So you make a separate box of Python just for your app — a **virtual environment (venv)**. This is the thing positioned in Section 1 as "disposable, recreatable."

```bash
# Install the package for creating venvs
sudo apt install python3-venv

# Create .venv inside /srv/myapp (as the myapp user)
cd /srv/myapp
sudo -u myapp python3 -m venv .venv

# Install FastAPI and the PostgreSQL driver into that .venv
sudo -u myapp .venv/bin/pip install "fastapi[standard]" "psycopg[binary]"
```

The point is naming `.venv/bin/pip` — the pip inside `.venv` — explicitly. That way it is not rejected by `externally-managed`. The system Python is never touched; packages land only inside `/srv/myapp/.venv/`. The Python that comes with Debian 13 is **3.13**. `fastapi[standard]` is FastAPI itself plus the set needed for development; `psycopg[binary]` is the driver for connecting to Chapter 7's PostgreSQL.

### A Minimal FastAPI App

Here is `app/main.py` in full. It is a minimal API that just saves and lists notes, connecting to the `myappdb` you made in Chapter 7 via psycopg.

```python
# /srv/myapp/app/main.py
import os
import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

# Receive connection info from .env as an environment variable
# (no secrets written in the code)
DB = os.environ["DATABASE_URL"]

app = FastAPI()


class Note(BaseModel):
    body: str


@app.on_event("startup")
def init_db():
    # Create the table at startup if it does not exist
    with psycopg.connect(DB) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id SERIAL PRIMARY KEY, body TEXT NOT NULL, "
            "created TIMESTAMP DEFAULT now())"
        )


@app.get("/notes")
def list_notes():
    # Return everything, newest first
    with psycopg.connect(DB) as conn:
        rows = conn.execute(
            "SELECT id, body, created FROM notes ORDER BY id DESC"
        ).fetchall()
    return [{"id": r[0], "body": r[1], "created": r[2]} for r in rows]


@app.post("/notes")
def add_note(note: Note):
    # Add one row and return the assigned id
    with psycopg.connect(DB) as conn:
        row = conn.execute(
            "INSERT INTO notes (body) VALUES (%s) RETURNING id",
            (note.body,),
        ).fetchone()
    return {"id": row[0], "body": note.body}
```

About 40 lines. This is **a sample to read and understand**, not something to memorize whole. Secrets (connection info) are not written in the code but received from `os.environ`; values are passed to SQL with `%s` (not string concatenation — this prevents malformed input); the input shape is fixed by pydantic's `Note`. Following just those three with your eyes is enough. For your own app, you may have Claude write it, starting from this sample.

Write the connection info into `.env`. This is the secret file you set to `chmod 600` in Section 1.

```bash
# /srv/myapp/.env  (a secret file only myapp can read)
sudo -u myapp tee /srv/myapp/.env > /dev/null <<'EOF'
DATABASE_URL=postgresql://myapp:your-password@localhost/myappdb
EOF
sudo chmod 600 /srv/myapp/.env
```

### Starting and Checking

To check behavior during development, invoke the uvicorn inside `.venv` (the server that runs FastAPI) by name.

```bash
cd /srv/myapp
# Load .env, then start on 127.0.0.1:8000
sudo -u myapp bash -c 'set -a; . .env; .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000'
```

From another terminal, check with `curl`, no browser needed.

```bash
# Add one
curl -X POST http://127.0.0.1:8000/notes -H "Content-Type: application/json" -d '{"body":"first note"}'

# Get the list
curl http://127.0.0.1:8000/notes
```

A nice thing about FastAPI is that **automatic documentation** grows at `/docs`. Both `GET /notes` and `POST /notes` are listed with descriptions and forms you can try. But the server has no screen, so to view it from your own browser, use a small SSH port-forwarding trick.

```bash
# From your own PC: connect the server's port 8000 to your local 8000
ssh -L 8000:127.0.0.1:8000 your-server
# Keep this open, then open http://127.0.0.1:8000/docs in your local browser
```

Now confirm, in Chapter 5's terms, what `--host 127.0.0.1` means. **Binding to 127.0.0.1** means "reachable only from within the same machine." The app keeps no ears open to the outside world at all. It is the same safe-side posture as PostgreSQL being closed to `127.0.0.1:5432` in Chapter 7. The only route out is Chapter 9's reverse proxy — keep the attack surface minimal with your own hands.

### Ask Claude ②: Rework the Sample into an API for Your Use

> Starting from the following `main.py`, rework it into an API for [your use, e.g. a household budget (record date / item / amount and also return a monthly total) / inventory / reading log]. Assume FastAPI and psycopg, connecting to PostgreSQL 17's `myappdb`.
> ```
> [paste the main.py above as-is]
> ```
> Show the reworked code, then explain what each added or changed part does. Keep the form where secrets (connection info) are not written in the code but read from .env.

The trick is to hand over the sample as-is and ask "rework this as the base." Starting from a working shape, rather than writing from zero, keeps the structure and style from drifting. Read the returned code as you did the unit file in Chapter 6, having each part explained once.

## Section 3 — Making It a systemd Service

Starting uvicorn by hand is only for checking. Close the terminal and it stops. **Apply "the pattern for making a service" you learned in Chapter 6, as-is.** Make it a real service that revives automatically when it falls and comes up on its own when the server reboots.

Write the unit file as `/etc/systemd/system/myapp.service`.

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My FastAPI app
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
User=myapp
Group=myapp
WorkingDirectory=/srv/myapp
EnvironmentFile=/srv/myapp/.env
ExecStart=/srv/myapp/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Chapter 6's three-section structure is alive here. Note just three differences from Chapter 6. **`After=...postgresql.service`** wakes the app only after the database has come up — the app connects to the DB, so order matters. **`EnvironmentFile=/srv/myapp/.env`** is the mechanism by which systemd reads Section 2's `.env` and turns it into environment variables, which is how `DATABASE_URL` reaches the app. **`ExecStart`** names the uvicorn inside `.venv` — using the virtual environment built in Section 2, not the system python. `User=myapp` runs it as Section 1's dedicated user.

Once written, run the flow you joined into one line in Chapter 6.

```bash
# 1. After writing the unit file, have it re-read
sudo systemctl daemon-reload

# 2. Start now, and enable auto-start too
sudo systemctl enable --now myapp

# 3. Confirm it is running
systemctl status myapp

# 4. Follow the logs
journalctl -u myapp -f
```

If `status` shows `active (running)`, it is already up as a service. `curl http://127.0.0.1:8000/notes` should go straight through. If `failed`, don't panic — read the error in `journalctl -u myapp`. As in Chapter 6, **pasting the error straight to Claude** is the basic move.

### The systemd Sandbox — Isolation Without Containers

Let me answer the obvious question here: **"without containers, where does the isolation come from?"** Container isolation is, in fact, a packaging of capabilities the Linux kernel already has (namespaces, cgroups, privilege restrictions). And systemd can use those same kernel capabilities directly, with a few lines in the unit file. Add this to `[Service]`:

```ini
# Add to [Service] — systemd's sandbox
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/srv/myapp/data
```

From the top: "no privilege escalation while running," "mount the OS areas (`/usr`, `/etc`) read-only," "hide other users' homes (`/home`)," "give this service its own private `/tmp`," "allow writes only to `data/`." Now even if the app is taken over, **all it can write is `/srv/myapp/data` and the log lines flowing into journald.** Section 1's ownership was the first wall; this sandbox is the second.

You do not need to memorize all of it at once. Run `systemd-analyze security myapp` and the "exposure" of your service is scored item by item. Paste that output into Claude and ask, "which of these should I add to my app right now, and which might break it?" — the sandbox, too, is something you design through dialogue.

Remember how to re-apply after editing code, too. After changing `app/main.py`, restart the service.

```bash
sudo systemctl restart myapp
```

### Ask Claude ③: Diagnose a Startup Failure

> My FastAPI app myapp is failing to start as a service. `systemctl status myapp` shows failed.
> The output of `journalctl -u myapp -p err -b --no-pager | tail -n 50` is this:
> ```
> [paste the error lines as-is]
> ```
> The unit file is this:
> ```
> [paste the contents of /etc/systemd/system/myapp.service]
> ```
> List candidate causes in order of likelihood, with how to check each. Show the order in which to narrow it down — which of these is suspect: .env loading, the venv path, the database connection, or user permissions.

As in Chapter 6, the trick is to paste **both the unit file and the error log**. With FastAPI apps the common snags are three: `.env` not being read (`DATABASE_URL` missing), a wrong `.venv` path, or a mismatched DB password. Claude cross-checks config against result and shows the way to isolate it.

## Section 4 — Running the Development Loop with Claude

By now the app, the database, and the service are connected. Finally, confirm as a pattern the **development loop** you will use from here on. It is the server version of the craft you picked up in the main series, [Chapter 15](/en/claude-debian/15-claude-development/).

The loop is this. **Put the spec into words → Claude writes the code → you review and run it → paste the error as-is → fix.** Keeping that circle turning is development in 2026. You don't write line by line; you convey accurately what you want to make, then run and protect what comes out.

What matters most in this circle is **how you convey requirements**. Hand over three things together and the quality of the returned code jumps a level.

- **What data** it handles (e.g. a note's body and creation time)
- **Who reads and writes it, and how** (e.g. only I, adding and listing)
- **Chapter 7's schema**, pasted as-is (the `\d notes` output)

And **"it works" is not the end.** After the service is up, always run one pre-publish check. It is the last confirmation before going outside in Chapter 9.

- Are secrets in `.env`? (Not leaked into the code or git.)
- Is the bind `127.0.0.1`? (Confirm with `ss -tlnp | grep 8000`.)
- Is it running as the dedicated user (`myapp`)? (The `User=` line in `systemctl status myapp`.)

These three confirm that Chapter 5's defenses and Section 1's structure are working correctly on top of the app. Pass here and you are ready to place it behind a reverse proxy in Chapter 9.

### Ask Claude ④: Review the Pre-Publish Checklist

> On a Debian 13 server I have placed a FastAPI app, myapp, at /srv/myapp and run it as a systemd service. Before publishing it to the outside in Chapter 9, I want to review the structure.
> Here is some output:
> ```
> [systemctl status myapp output]
> ```
> ```
> [ss -tlnp | grep 8000 output]
> ```
> ```
> [ls -l /srv/myapp output (so the .env permissions are visible)]
> ```
> From these, check whether (1) secrets are isolated in .env outside the code, (2) the app is bound only to 127.0.0.1, and (3) it runs as a dedicated user. If anything should be fixed before publishing, list it with priorities.

Before the irreversible step of publishing, have Claude review your structure once. Just by pasting the output, you'll find at least one hole you overlooked. This is the warm-up for Chapter 9.

## Summary

What you did in this chapter:

1. Confirmed the stance of running the app as "a plain directory plus a venv plus systemd" without a container, and that the directory-layout convention creates order in its place.
2. Split app/, .venv/, .env, and data/ under `/srv/myapp/`, created the dedicated user `myapp`, and drew the "in git / recreatable / back up" mapping table.
3. Grasped the reason for PEP 668 (externally managed), created a virtual environment with `python3-venv`, and installed FastAPI and psycopg into `.venv`.
4. Read the minimal note API `app/main.py`, connected it to Chapter 7's `myappdb`, and checked it with `curl` (plus the `/docs` auto-docs and SSH port forwarding).
5. Wrote `myapp.service` in Chapter 6's pattern and made it a service through daemon-reload → enable --now → status → journalctl.
6. Made a pattern of the development loop — convey the spec, have it written, run and fix — and the pre-publish check (secrets, bind, dedicated user).

What you hold now:
- Your own FastAPI service that runs as a dedicated user and revives when it falls (`myapp.service`).
- A directory layout (`/srv/myapp/`) separating git-tracked code, a disposable venv, and the secret `.env`.
- Your first homemade API, running connected to Chapter 7's `myappdb`.
- The dialogue patterns "hand over the sample and have it reworked" and "have the structure reviewed before publishing."

Your own app ran, on your own server, using your own database. But for now it is still a world inside `127.0.0.1`, your own machine alone. No one can see it from outside — and that is not a weakness; for now it is defense. In the next [Chapter 9 "Opening Up to the Outside World"](/en/claude-debian/server/09-publishing/), you place this app behind a reverse proxy called Caddy, dress it in TLS, and finally bring it out to a place visible from the world. You take the irreversible step of publishing carrying Chapter 5's defenses and the pre-publish check you ran in this chapter.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
