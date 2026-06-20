---
slug: documents
number: "08"
lang: en
title: "Take Documents Back — OnlyOffice Docs on PocketBase"
subtitle: "Add no separate storage app — put documents on the Chapter 7 gate and embed only the editor engine"
description: Word, Excel, and PowerPoint are the input/output tools people write and read with. Rather than add a separate storage app like Nextcloud, use the PocketBase stood up in Chapter 7 as the document store (storage, auth, sharing) and embed OnlyOffice Docs as the editor engine only — a thin, custom document app. It opens docx, xlsx, and pptx with high fidelity, co-edits, and sits inside the gate from the start. Keep the formats; take back only control.
date: 2026.07.04
label: Software 08
title_html: Put documents<br>right <span class="accent">inside the gate</span>.
prev_slug: auth
prev_title: "Stand Up the Gate — One Login with PocketBase"
next_slug: code
next_title: "Bring Code In-House — Forgejo and Zed"
---

# Take Documents Back — OnlyOffice Docs on PocketBase

Inside the gate (Chapter 7), the first tool to place is **documents.** Word,
Excel, PowerPoint — these are the **input/output tools** people write and
read with, and that role does not change (Chapter 6). What changes is only
**format compatibility and control of the storage.**

So you don't switch to a new document format. You embed, into your own app, an
editor engine that reads and writes **`docx`, `xlsx`, and `pptx` as-is.**

## Why not add a separate storage app

"Documents" tempts you to stand up a whole OneDrive replacement like Nextcloud.
But Nextcloud is a heavyweight PHP monolith — **old-style heavy software** —
that drags in a separate user system and a separate database. It runs against
the **single-binary lightness** this Setup part has chosen (PocketBase,
Stalwart, Forgejo).

In Chapter 7 you already stood up **PocketBase,** which carries auth, storage,
and REST. As a document store, **that is enough.**

- **Storage** — put documents in PocketBase file-bearing records
- **Auth** — the Chapter 7 gate applies directly (no second login)
- **Sharing** — issue internal and external links with PocketBase access rules

What you add is **only the editor engine.** OnlyOffice ships "Docs (the
Document Server)" as a standalone editing engine, leaving storage to any app.
So **embed OnlyOffice Docs into PocketBase** — this is the thinnest path.

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

## Put documents in PocketBase

Documents go into a `documents` collection on the Chapter 7 **PocketBase,** held
in a file field. Owner, share targets, and timestamps live on the same record.

```js
// save one document into the gate (PocketBase)
await pb.collection('documents').create({
  title: 'quote_2026.xlsx',
  owner: pb.authStore.model.id,   // the Chapter 7 gate already knows who this is
  file:  xlsxBlob,                // PocketBase stores the file itself
})
```

No new database, no new login. **The document is inside the gate from the
start.**

## Connect — open and save

Opening a document from the list launches the OnlyOffice editor in the browser.
The app passes only **where the file is** and **where to save (the callback),**
signed with JWT, to the engine.

```js
// open the editor — hand the engine a signed config
new DocsAPI.DocEditor("editor", {
  document:     { url: fileUrl, key: docId },          // the file on PocketBase
  editorConfig: { callbackUrl: saveBackUrl },          // save target is PocketBase too
  token:        jwt,                                    // signed with JWT_SECRET
})
```

When a person finishes editing, OnlyOffice Docs **returns the edited file to the
callback,** and you write it back to the PocketBase record. The engine handles
co-editing reconciliation. All the app writes is these few lines of hand-off.

## The gate stays — no second login

This is the biggest win of building it your own way. The document is **inside
the Chapter 7 gate from the start,** so there is no second account like
Nextcloud's and no front-door auth proxy. Who can open which document is decided
by a single PocketBase access rule.

## Migrate existing documents

Documents piled in OneDrive and SharePoint move **without a format change.**
OnlyOffice Docs opens `docx`, `xlsx`, and `pptx` as-is, so no conversion is
needed.

```bash
# pull down with rclone, then import into PocketBase records
rclone copy onedrive:Documents ./inbox --progress
# register each file in inbox/ into the documents collection (one script)
```

Migrate gradually. **Run both in parallel and cancel the old storage once the
move is done** (parent series, Chapter 7).

## People use OnlyOffice; machines use Polars

Here is the link back to Chapter 6. **People enter and read in OnlyOffice (Excel
format); machines crunch the data behind it with Polars and DuckDB.** The same
`.xlsx` is an editing tool to a person and an input to a machine — split by role.

- Summary sheets, request forms, proposals people make — open and store in OnlyOffice Docs
- Million-row reconciliations, company-wide rollups — Polars reads the `.xlsx`, writes PostgreSQL

The spreadsheet returns to being "the human's tool," and heavy processing moves
to "the machine's tool."

> Don't add separate apps for either the format or the storage.
> **Put it right inside the gate and embed only the editor engine.**

## Summary

Documents, right inside the gate.

- **OnlyOffice Docs** — an editor engine for `docx`, `xlsx`, `pptx` with high fidelity (holds no storage)
- **PocketBase** — reuse the Chapter 7 gate as document storage, auth, and sharing
- **Embedding is a few lines** — hand over the file location and save target, signed with JWT
- **No second login** — documents are inside the gate from the start, access by one rule
- **People vs. machines** — people use OnlyOffice Docs, machines use Polars / DuckDB

No separate storage app — **embedded into the gate you already have.** Next, we
stand up the builder's workshop — **code sharing (Forgejo)** — and bring GitHub
and Azure DevOps to our own side.

---

## Related articles

- [Chapter 6: Lay the Foundation — PostgreSQL, SQLite, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [Chapter 7: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
