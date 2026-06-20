---
slug: documents
number: "08"
lang: en
title: "Take Documents Back — Nextcloud and OnlyOffice"
subtitle: "Open Word, Excel, and PowerPoint on your own side — same formats, the storage in your own hands"
description: Word, Excel, and PowerPoint are the input/output tools people write and read with. OnlyOffice opens and saves docx, xlsx, and pptx as-is, with co-editing. Nextcloud holds them, bringing OneDrive and SharePoint to your own side. It rides on the PostgreSQL from Chapter 6 and sits behind the gate from Chapter 7. Keep the formats; take back only control of the data.
date: 2026.07.04
label: Software 08
title_html: Open and store documents<br>on <span class="accent">your own side</span>.
prev_slug: auth
prev_title: "Stand Up the Gate — One Login with PocketBase"
next_slug: sier-uneconomic
next_title: "The Structural Uneconomy of the SIer Model"
---

# Take Documents Back — Nextcloud and OnlyOffice

Inside the gate (Chapter 7), the first tool to place is **documents.** Word,
Excel, PowerPoint — these are the **input/output tools** people write and
read with, and that role does not change (Chapter 6). What changes is only
**format compatibility and control of the storage.**

So you don't switch to a new document format. You stand up, on your own side,
OSS that reads and writes **`docx`, `xlsx`, and `pptx` as-is.**

## Why OnlyOffice

Document editing is **OnlyOffice**, for one reason: **high compatibility with
Microsoft Office formats.** It opens `docx`, `xlsx`, and `pptx` without layout
breakage, saves in the same formats, and supports **co-editing** by several
people. A human input/output tool is pointless unless it keeps the format
people already know — so compatibility comes first.

Storage and sharing are **Nextcloud.** In place of OneDrive and SharePoint, it
handles file storage, sharing, versioning, and external links. OnlyOffice
opens inside this Nextcloud.

## Stand up Nextcloud

Stand it up with `compose.yaml`. The data rides directly on the **PostgreSQL
from Chapter 6.**

```yaml
# compose.yaml — stand up storage (Nextcloud) on the Chapter 6 DB
services:
  files:
    image: nextcloud:apache
    environment:
      POSTGRES_HOST: db          # the PostgreSQL stood up in Chapter 6
      POSTGRES_DB: nextcloud
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: change-me
    volumes: ["./nc_data:/var/www/html"]
    restart: always
```

```bash
docker compose up -d
# create the admin and finish setup (just open it in a browser)
```

The warehouse (PostgreSQL) already exists. Nextcloud merely **adds a file
layer on top** — no new database server.

## Connect OnlyOffice

To edit documents inside Nextcloud, stand the **OnlyOffice Document Server**
beside it and join them with a connector.

```yaml
  # append to the same compose.yaml
  onlyoffice:
    image: onlyoffice/documentserver:latest
    restart: always
```

Then, in Nextcloud's admin, install the **OnlyOffice connector** app and point
it at the Document Server. Now opening an `.xlsx` from the file list launches a
spreadsheet in the browser and **saves straight back in Excel format.**

## Place it behind the gate

Nextcloud carries its own accounts. Per Chapter 7's approach, place it **behind
the reverse proxy** and let the outside through only after the gate.

```caddy
docs.example.com { reverse_proxy files:80 }
```

To later bind it into one login, add Nextcloud's OIDC app and tie it to the
gate — but first, move the storage onto your own side.

## Migrate existing documents

Documents piled in OneDrive and SharePoint move **without a format change.**
OnlyOffice opens `docx`, `xlsx`, and `pptx` as-is, so no conversion is needed.

```bash
# bulk-copy from OneDrive / SharePoint into Nextcloud with rclone
rclone copy onedrive:Documents nextcloud:Documents --progress
```

Migrate gradually. **Run both in parallel and cancel the old storage once the
move is done** (parent series, Chapter 7). Re-pointing links can wait, too.

## People use OnlyOffice; machines use Polars

Here is the link back to Chapter 6. **People enter and read in OnlyOffice
(Excel format); machines crunch the data behind it with Polars and DuckDB.**
The same `.xlsx` is an editing tool to a person and an input to a machine —
split by role.

- Summary sheets, request forms, proposals people make — open and store in OnlyOffice
- Million-row reconciliations, company-wide rollups — Polars reads the `.xlsx`, writes PostgreSQL

The spreadsheet returns to being "the human's tool," and heavy processing moves
to "the machine's tool." **Both share the same format and the same storage.**

> Don't change the document format. Change **where it sits.**
> The human's tool stays; only control moves to your own side.

## Summary

Behind the gate, a place for documents.

- **OnlyOffice** — opens `docx`, `xlsx`, `pptx` with high fidelity, co-editing
- **Nextcloud** — storage and sharing in place of OneDrive / SharePoint (on the Chapter 6 PostgreSQL)
- **Behind the gate** — fenced by the reverse proxy, bound later via OIDC
- **rclone** — migrate existing documents format-intact, switch over by parallel run
- **People vs. machines** — people use OnlyOffice, machines use Polars / DuckDB

Almost no code was written. **The generic is already there, as OSS.** Next, we
stand up the builder's workshop — **code sharing (Forgejo)** — and bring GitHub
and Azure DevOps to our own side.

---

## Related articles

- [Chapter 6: Lay the Foundation — PostgreSQL, SQLite, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [Chapter 7: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
