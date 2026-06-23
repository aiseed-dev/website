---
slug: foundation
number: "01"
part: "2"
lang: en
title: "Lay the Foundation — PostgreSQL, SQLite, pgvector, DuckDB, Polars"
subtitle: "Stand up the data layer everything sits on, first, on your own side"
description: The Setup part starts with the data layer everything sits on. Shared data goes in PostgreSQL; local data in SQLite. Enable pgvector for semantic search; analyze with columnar DuckDB and Polars — Excel stays the human's I/O while machines crunch the data behind it; pull far ahead of Power BI. Stand it up with Docker, migrate from Azure SQL with pgloader. The generic is already shared as OSS — you don't write it, you stand it up.
date: 2026.07.01
label: Independence 1
title_html: Stand up the <span class="accent">data layer</span><br>first, on your own side.
prev_slug: embedded
prev_title: "Build Embedded — Think in Python, Have Claude Translate"
next_slug: auth
next_title: "Stand Up the Gate — One Login with PocketBase"
---

# Lay the Foundation — PostgreSQL, SQLite, pgvector, DuckDB, Polars

**A builder's work does not begin with writing code. It begins with
standing up proven OSS** (Chapter 5). Generic functionality is
already shared with the world — so you don't "write" it, you "stand it up."

This Setup part (from Chapter 6) stands up, one by one, the OSS that replaces
Microsoft 365 and the vendor packages under the core systems. First is the
**data layer.**
Analysis, the AI's RAG, course booking, the core systems —
**all of the shared data sits on top of this.** So you lay it first.

## Why start from the data layer

The order has a reason. Much of what later chapters stand up depends on the
database:

- **Analysis** (DuckDB) reads the tables and Parquet here
- **The AI's RAG** (Command A+) does similarity search with `pgvector`
- **Course booking** (Cal.com) and the **core systems** read and write here

With the foundation in place first, everything above is just "put it on the
DB that already exists." **The earlier you lay it, the lighter everything
after.**

## Stand up PostgreSQL

The database is **PostgreSQL** — open source, free, commercial-OK. It
matches or exceeds Oracle and SQL Server, and it is the dialect Claude
handles best (Chapter 5; parent series Chapter 14).

One `compose.yaml` stands it up.

```yaml
# compose.yaml — PostgreSQL image with pgvector bundled
services:
  db:
    image: pgvector/pgvector:pg17
    environment:
      POSTGRES_PASSWORD: change-me
      POSTGRES_DB: app
    ports: ["5432:5432"]
    volumes: ["./pgdata:/var/lib/postgresql/data"]
    restart: always
```

```bash
docker compose up -d            # start
docker compose exec db psql -U postgres -d app -c '\l'   # check
```

Using the `pgvector/pgvector` image means the **vector extension you'll need
later is already in.** The plain `postgres` image works too, but then you
add the extension separately (next section).

## Enable pgvector

Enable now the **vector search** the AI's RAG (a later Setup chapter) will
use. It is a one-line extension.

```sql
-- run once on the database
CREATE EXTENSION IF NOT EXISTS vector;

-- example table holding embeddings (1024 dims, e.g. bge-m3)
CREATE TABLE docs (
  id    bigserial PRIMARY KEY,
  body  text,
  embedding vector(1024)
);
```

Now you have the foundation for searching documents by **meaning.** Put
embeddings in `embedding` and pull the nearest with
`ORDER BY embedding <=> :query` — the real RAG pipeline gets built in the AI
chapter. **For now, just have the vessel ready.**

## Hold it in a single file — SQLite

Not everything belongs on the shared server (PostgreSQL). For settings a
single app keeps to itself, or small data that lives on the device, **SQLite**
fits. No server to run — it fits in **one file.** It is the most widely
deployed database in the world; it ships inside every phone and browser.

```bash
# no library needed — it's in the standard install
sqlite3 app.db 'CREATE TABLE memo(id integer primary key, body text)'
```

The **gate (PocketBase) stood up next chapter also runs on this SQLite.** The
rule of thumb is one line. **If several apps or people write at the same time,
PostgreSQL; if a single app just keeps it locally, SQLite.** Both speak
standard SQL, and Claude writes it as-is. **Use the warehouse (PostgreSQL) and
the notebook (SQLite) for what each is for.**

## Migrate from Azure SQL

If you have an existing Azure SQL / SQL Server, `pgloader` carries schema and
data in one pass.

```bash
pgloader mssql://user:pass@azure-host/db \
         postgresql://postgres:change-me@localhost/app
```

Standard SQL (`SELECT`, `JOIN`, window functions) runs as-is. You drop only
**the vendor dialect, T-SQL.** Business logic buried in stored procedures
gets extracted by Claude and translated into Python / Ruby (Chapter 5).
Then run in parallel with the old DB, reconcile the output, and stop the old
when the difference is gone (parent series Chapter 7).

> Migration is not "rewrite everything."
> It is **move onto the standard and drop only the dialect.**

## Analyze with DuckDB — pull far ahead of Excel and Power BI

For aggregation and analysis, layer **DuckDB** on top of PostgreSQL. A
columnar analytics engine — one file, no server. Where Excel caps at about
1.05 million rows, **one laptop aggregates hundreds of millions of rows in
seconds.**

```bash
pip install duckdb polars       # that's it
```

```python
import duckdb
# Aggregate across Parquet, PostgreSQL, and CSV in place, with SQL
duckdb.sql("INSTALL postgres; LOAD postgres;")
duckdb.sql("ATTACH 'dbname=app user=postgres host=localhost' AS pg (TYPE postgres)")
duckdb.sql("SELECT dept, sum(sales) FROM pg.sales GROUP BY dept ORDER BY 2 DESC")
```

You analyze **where the data already sits**, without copying it. Claude
writes the SQL — "which department is anomalous versus last month?" asked
against your own real data, any number of times, at zero marginal cost. Seen
from Power BI's metered, per-seat cloud, this is another dimension.

### Handle Excel data — Polars

Excel is the **input/output tool** where people enter numbers and read
results. That role does not change — which is why the next chapter stands up
the Excel-compatible **OnlyOffice** on your own side. What changes is **the
side that crunches the data behind it.**

The `.xlsx` files piled up on disk are read directly by **Polars** — a fast,
Rust-built dataframe. It handles row counts that freeze Excel in an instant,
and writes the result back to Excel, PostgreSQL, or Parquet alike.

```python
import polars as pl
df  = pl.read_excel("sales_2025.xlsx")               # read the Excel people made
agg = df.group_by("dept").agg(pl.col("sales").sum()) # heavy aggregation in one line
agg.write_excel("dept_summary.xlsx")                 # write back to Excel people read
```

People enter and read in Excel; machines crunch with Polars and DuckDB.
**Split the human's tool from the machine's tool by role.** SQL-shaped work
goes to DuckDB, dataframe-shaped work to Polars — the same data, touched with
whichever tool you like.

For huge, always-on aggregation, move it onto the columnar DB server
**ClickHouse.** But most in-house analysis needs only DuckDB and Polars.

## Summary

The data layer, onto your own side, first.

- **PostgreSQL** (+ pgvector) — the shared warehouse booking, the core, and RAG sit on
- **SQLite** — a serverless single file, for local, device, and small-tool data (the gate runs on it too)
- **pgvector** — the foundation for semantic search (RAG comes in the AI chapter)
- **pgloader** — one-pass migration from Azure SQL, dropping only the dialect
- **DuckDB / Polars** — columnar analysis and a fast dataframe; Excel stays the human's I/O, heavy crunching moves machine-side, pulling far ahead of Power BI

Almost no code was written. **The generic is already there, as OSS.** The
builder stands it up. The next chapter lays **authentication (PocketBase)**
on top of this, as the shared gatekeeper across the apps.

---

## Related articles

- [Chapter 5: Customers Co-Develop with AI](/en/ai-native-ways/software/customer-codev/)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
- [Chapter 7: Living with Business Systems — Rewrite by Running in Parallel](/en/ai-native-ways/business-systems/)
