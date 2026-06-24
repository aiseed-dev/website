---
slug: fastapi
number: "09"
part: "2"
lang: en
title: "Build an API — Expose Core Logic with FastAPI"
subtitle: "Gather your own business logic into one API that every app can call"
description: The Independence part's OSS covers the generic. What remains is your own business logic — the core systems. Expose it as an API with FastAPI so the public-web form and the in-house apps call the same thing. It reads and writes the Chapter 2 PostgreSQL and verifies identity with the Chapter 3 gate's token — no new foundation needed. Not all the core at once, but the most-used operations one at a time, with the running version as the answer key, in dialogue. The reference implementation is kura.
date: 2026.07.15
label: Independence 9
title_html: Your own logic,<br>in one <span class="accent">API</span>.
prev_slug: web
prev_title: "Publish the Web — Cloudflare Pages (a WordPress Replacement)"
next_slug: ai
next_title: "Stand Up Your Own AI — LLM and RAG"
---

# Build an API — Expose Core Logic with FastAPI

The Independence part's OSS covers the generic — auth, documents, mail,
meetings, the public web. What remains is **your own business logic,** the
substance of the core systems. Expose it as an API with **FastAPI** so every app
can use it.

## Why make it an API

- Don't scatter core logic (inventory, ordering, pricing…) across screens —
  **gather it into one API**
- The public-web form (Chapter 8) and the in-house apps call the same API —
  duplication disappears
- In Python (FastAPI), AI writes it fast, with types and automatic docs (OpenAPI)

## On top of the foundation and the gate

The API reads and writes the Chapter 2 **PostgreSQL** and verifies identity with
the Chapter 3 **gate (PocketBase)** token. No new foundation — it rides on what
already exists.

```python
# FastAPI — verify the gate's token, query the foundation (DB)
from fastapi import FastAPI, Depends
app = FastAPI()

@app.get("/orders")
def orders(user=Depends(verify_token)):       # the Chapter 3 gate verifies who
    return db.query("SELECT * FROM orders WHERE user_id=%s", [user.id])  # the Chapter 2 DB
```

## In dialogue, thin

Not all the core at once. **The most-used operations, one at a time.** Write it
with AI in dialogue and check against the running version (the same way as
Introduction, Chapter 6, VBA → Python). Heavy work runs in Python behind it,
returning only the result.

## Reference implementation — kura

The public repo **kura** (`aiseed-dev/workspace`) is this setup — PocketBase
auth + **FastAPI** + a Flet front end. The code lives in the Chapter 4 Forgejo,
called from the Chapter 8 public web and the in-house apps.

## Summary

- Put your own logic into **one API** with FastAPI
- It rides on the **Chapter 2 DB and the Chapter 3 gate** — no new foundation
- The most-used operations one at a time — **running version as answer key, thin, in dialogue**

Next, we lay **AI (a self-hosted LLM and RAG)** on top of all of this and cut the
dependency on Copilot.

---

## Related articles

- [Chapter 2: Lay the Foundation — PostgreSQL, SQLite, and more](/en/ai-native-ways/software/foundation/)
- [Chapter 3: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Reference implementation kura — a self-hosted Microsoft 365 / Google Workspace alternative](https://github.com/aiseed-dev/workspace)
