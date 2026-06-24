---
slug: documents
number: "05"
part: "2"
lang: en
title: "Take Documents Back — OnlyOffice Docs on PocketBase"
subtitle: "Add no separate storage app — put documents on the Chapter 3 gate and embed only the editor engine"
description: Word, Excel, and PowerPoint are the input/output tools people write and read with. Rather than add a separate storage app like Nextcloud, keep documents as plain files on your own storage, with auth from the Chapter 3 PocketBase and permissions in xattr, and embed OnlyOffice Docs as the editor engine only — a thin, custom document app. It opens docx, xlsx, and pptx with high fidelity, co-edits, and needs no second permissions DB or login. Avoid the finished DocSpace — it brings Active Directory back. The reference implementation is the public repo kura. Keep the formats; take back only control.
date: 2026.07.04
label: Independence 5
title_html: Keep documents as <span class="accent">files</span>;<br>only auth at the gate.
prev_slug: code
prev_title: "Bring Code In-House — Forgejo and Zed"
next_slug: mail
next_title: "Mail on Your Own Side — Stalwart and Thunderbird"
---

# Take Documents Back — OnlyOffice Docs on PocketBase

Inside the gate (Chapter 3), the first tool to place is **documents.** Word,
Excel, PowerPoint — these are the **input/output tools** people write and
read with, and that role does not change (Chapter 2). What changes is only
**format compatibility and control of the storage.**

So you don't switch to a new document format. You embed, into your own app, an
editor engine that reads and writes **`docx`, `xlsx`, and `pptx` as-is.**

## Why not add a separate storage app

"Documents" tempts you to stand up a whole OneDrive replacement like Nextcloud.
But Nextcloud is a heavyweight PHP monolith — **old-style heavy software** —
that drags in a separate user system and a separate database. It runs against
the **single-binary lightness** this Setup part has chosen (PocketBase,
Stalwart, Forgejo).

In Chapter 3 you already stood up **PocketBase,** which carries auth. For
storage, **make it the gate and keep the rest as files.**

- **The file itself** — plain files on your own storage; no heavy storage app
- **Auth** — the Chapter 3 gate (PocketBase) applies directly (no second login)
- **Permissions / sharing** — carried by the file itself (xattr); the gate verifies identity

What you add is **only the editor engine.** OnlyOffice ships "Docs (the
Document Server)" as a standalone editing engine, leaving storage to any app.
So **lay OnlyOffice Docs over files guarded by the gate (PocketBase)** — this is
the thinnest path.

## Choose Docs — not DocSpace

OnlyOffice also offers a finished platform, **DocSpace.** But **don't choose
it,** for two reasons.

- **It brings Active Directory back** — DocSpace is built around LDAP / AD / SAML SSO. The **Microsoft authentication (AD) you cut in Chapter 3 moves right back in.**
- **The free edition caps at 20 concurrent connections** — DocSpace Community limits simultaneous editing tabs to 20. Grow past it and you are pushed to the paid Enterprise edition — the doorway to lock-in.

What you need is **only the editor engine.** And there is good news — **Docs 9.4
removed the 20-connection limit from the Community edition** (the engine alone is
now unlimited). It also dropped its RabbitMQ and separate-DB dependencies and
became a **single process.** Paired with PocketBase (a single binary),
enterprise-grade co-editing is in hand **for free, and light.**

> The platform (DocSpace) brings AD along in exchange for convenience.
> **Take only the engine (Docs); leave authentication to the Chapter 3 gate.**

## Stand up OnlyOffice Docs

Stand up the editor engine **OnlyOffice Docs.** It only edits; it holds no
files of its own. Set one **JWT secret** to prevent tampering.

```yaml
# compose.yaml — stand up only the editor engine
services:
  onlyoffice:
    image: onlyoffice/documentserver:latest
    environment:
      JWT_SECRET: change-me        # signing key shared with PocketBase
    restart: always
```

It opens `docx`, `xlsx`, and `pptx` without layout breakage, saves in the same
formats, and supports **co-editing** by several people — that engine is now in
hand.

For internal use, the Community edition (AGPLv3) is fine. **Only if you resell it
as your own SaaS** do you need to mind AGPL's copyleft and attribution (naming
ONLYOFFICE in the UI) — there, consider a commercial license.

## Documents are files — auth at the gate, permissions in xattr

A document's body is **just a file** on your own storage. Rather than embed it
as a blob in a PocketBase record, keep `docx`, `xlsx`, and `pptx` as files — so
that machines (Polars, AI) can read them directly later.

- **The body** — a file on the filesystem (your own storage)
- **Auth** — the Chapter 3 gate (PocketBase) verifies who
- **Permissions** — carried by the file itself — extended attributes (xattr)

```bash
# permissions ride on the file itself, not a separate DB
setfattr -n user.ws.perm    -v 'team:rw' quote_2026.xlsx
setfattr -n user.ws.creator -v 'alice'   quote_2026.xlsx
```

No separate database just for permissions. **The gate holds identity; the file
holds permission** — split by role.

## Connect — open and save

Opening a document from the list launches the OnlyOffice editor in the browser.
The app passes only **where the file is** and **where to save (the callback),**
signed with JWT, to the engine.

```js
// open the editor — hand the engine a signed config
new DocsAPI.DocEditor("editor", {
  document:     { url: fileUrl, key: docId },          // where the file is
  editorConfig: { callbackUrl: saveBackUrl },          // save target (write back to the file)
  token:        jwt,                                    // signed with JWT_SECRET
})
```

When a person finishes editing, OnlyOffice Docs **returns the edited file to the
callback,** and you write it back to the **original file.** The engine handles
co-editing reconciliation. All the app writes is these few lines of hand-off.

## The gate stays — no second login

This is the biggest win of building it your own way. **Auth comes straight from
the Chapter 3 gate, and permissions ride on the file (xattr),** so there is no
second account like Nextcloud's and no separate permissions database. Who can
open which document is decided by the identity the gate verifies and the
permission stamped on the file.

## Migrate existing documents

Documents piled in OneDrive and SharePoint move **without a format change.**
OnlyOffice Docs opens `docx`, `xlsx`, and `pptx` as-is, so no conversion is
needed.

```bash
# pull down with rclone and lay the files on your own storage
rclone copy onedrive:Documents ./inbox --progress
# stamp permissions on each file in inbox/ with xattr (one script)
```

Migrate gradually. **Run both in parallel and cancel the old storage once the
move is done** (parent series, Chapter 7).

## People use OnlyOffice; machines use Polars

Here is the link back to Chapter 2. **People enter and read in OnlyOffice (Excel
format); machines crunch the data behind it with Polars and DuckDB.** The same
`.xlsx` is an editing tool to a person and an input to a machine — split by role.

- Summary sheets, request forms, proposals people make — open and store in OnlyOffice Docs
- Million-row reconciliations, company-wide rollups — Polars reads the `.xlsx`, writes PostgreSQL

The spreadsheet returns to being "the human's tool," and heavy processing moves
to "the machine's tool."

> Don't add separate apps for either the format or the storage.
> **Keep it as a file, leave only auth to the gate, and embed only the editor engine.**

## Reference implementation — kura

This setup is actually built in the public repo **kura** (`aiseed-dev/workspace`)
— a self-hosted Microsoft 365 / Google Workspace alternative aimed at serious
SME use (about 100 users per instance, distributed for more). It maps straight
onto this chapter:

- **Auth** — PocketBase (pluggable token validation + short-lived cache)
- **Permissions** — file xattr (`user.ws.perm` / `user.ws.creator`), no permissions DB
- **The body** — the file itself ("the AI interface is files")
- **Editing** — OnlyOffice Docs over JWT and callbacks (FastAPI + Flet)

This chapter is that design put into words. To see the code, read kura.

## Summary

Files as they are, only auth at the gate.

- **OnlyOffice Docs** — an editor engine for `docx`, `xlsx`, `pptx` with high fidelity (holds no storage)
- **The body is a file** — on your own storage, readable directly by machines (Polars, AI)
- **Auth at the gate (PocketBase) / permissions in xattr** — no separate permissions DB
- **Embedding is a few lines** — hand over the file location and save target, signed with JWT
- **People vs. machines** — people use OnlyOffice Docs, machines use Polars / DuckDB

No separate storage app — **files as they are, embedded into the gate you already
have.** Next, we stand up the builder's workshop — **code sharing (Forgejo)** —
and bring GitHub and Azure DevOps to our own side.

---

## Related articles

- [Chapter 2: Lay the Foundation — SQLite, PostgreSQL, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [Chapter 3: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Reference implementation kura — a self-hosted Microsoft 365 / Google Workspace alternative](https://github.com/aiseed-dev/workspace)
- [Chapter 1: Becoming Independent from Microsoft and Google — The Whole Map](/en/ai-native-ways/software/independence/)
