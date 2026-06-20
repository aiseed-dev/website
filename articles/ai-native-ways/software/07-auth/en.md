---
slug: auth
number: "07"
lang: en
title: "Stand Up the Gate — One Login with PocketBase"
subtitle: "One front door for every app — email, OAuth, and one-time codes from a single binary"
description: Authentication is not something each app builds on its own. It is a gate you stand up once and share. PocketBase is a single binary with email auth, OAuth2, one-time codes, MFA, an admin UI, and a REST API. Identity lives in the gate; business data lives in PostgreSQL — separate the gate from the warehouse. Step off Microsoft Entra ID's per-seat monthly bill.
date: 2026.07.02
label: Software 07
title_html: One front door,<br>a <span class="accent">gate</span> from a single binary.
prev_slug: foundation
prev_title: "Lay the Foundation — PostgreSQL, SQLite, pgvector, DuckDB, Polars"
next_slug: documents
next_title: "Take Documents Back — OnlyOffice Docs on PocketBase"
---

# Stand Up the Gate — One Login with PocketBase

On top of the foundation (PostgreSQL, SQLite), the first thing to stand up is
the **gate** — authentication. Every app checks "who is this?" at the door.
Building that check **per app is the prime case of reinventing the wheel** —
and the easiest to get wrong, because it sits at the center of security.

So authentication, too, you don't write. You **stand it up.** The most
generic of the generic is already there as OSS.

## Why authentication goes up first

The reason the gate follows the foundation is simple: **every app you stand
up after this passes through the same door.** Documents, course booking, the
core systems, the small in-house tools — when there is one entrance, users
log in once and operators guard one place.

A homegrown login means hashing, sessions, token revocation, two-factor,
password reset, social login — not one of them can be skimped. **Standing up
one gate and sharing it** is faster, safer, and cheaper.

## Stand up PocketBase

The gate is **PocketBase**. A single **Go binary** carries authentication, an
admin UI, REST / realtime APIs, and file storage. It **runs on the SQLite**
introduced in Chapter 6, so there is no separate server to run. One
`compose.yaml` stands it up.

```yaml
# compose.yaml — just place the single-binary gate
services:
  auth:
    image: ghcr.io/muchobien/pocketbase:latest
    ports: ["8090:8090"]
    volumes: ["./pb_data:/pb_data"]
    restart: always
```

```bash
docker compose up -d
# create one superuser
docker compose exec auth pocketbase superuser create admin@example.com 'change-me'
```

The admin UI is at `http://localhost:8090/_/`. Users, login methods, token
lifetimes — all configured from here. Not a line of code yet.

## Open email, OAuth, and one-time codes

On PocketBase's `users` collection, enable the doors you need.

- **Email + password** — default, with verification and reset built in
- **OAuth2** — add Google, Microsoft, GitHub as "log in" buttons
- **One-time code (OTP)** — passwordless entry with a number sent by email
- **MFA** — enforce two-factor for everyone, or just for administrators

Even mid-migration from Entra ID (formerly Azure AD), **keep Microsoft in
OAuth2** and users sign in with their existing Microsoft account. Move only
the gate to your side; leave the user's experience unchanged.

## Identity in the gate, business data in the warehouse

This is the crux of the design. **Identity (who) lives in the gate; business
data (what they did) lives in PostgreSQL** (Chapter 6). Separate the gate
from the warehouse.

An app **verifies the gate's token, pulls out `user.id`,** and reads and
writes PostgreSQL keyed by that id.

```python
# app side — verify the gate's token, query the warehouse (PostgreSQL)
user_id = verify_token(request.headers["Authorization"])   # issued by PocketBase
orders  = pg.execute("SELECT * FROM orders WHERE user_id = %s", [user_id])
```

Zero auth machinery to build. All an app carries is one line that asks the
gate "is this token valid?" **Don't multiply gates — share one.**

> Authentication is not something each app builds on its own.
> It is a gate you **stand up once and share.**

## Stand it in front — the reverse proxy

Apps you build yourself are guarded directly by the PocketBase SDK. Packaged
OSS like documents (OnlyOffice) or code (Forgejo), on the other hand, **each
carry their own login.** Put a **reverse proxy (Caddy)** in front and let the
outside reach them only through the gate.

```caddy
# Caddyfile — line up each app behind the gate
auth.example.com   { reverse_proxy auth:8090 }
docs.example.com   { reverse_proxy onlyoffice:80 }
git.example.com    { reverse_proxy forgejo:3000 }
```

To later bind these into **one login (SSO)**, add a layer that speaks OIDC in
front — but for most in-house use, the gate plus each app's own login is
enough. **Making the entrance one comes first;** full unification can wait.

## Step off Entra ID

Microsoft Entra ID bills monthly, stacking with every user. Stand the gate up
on your own side and step off that meter. The move can be gradual.

1. Stand up PocketBase, keep Microsoft in OAuth2 (existing accounts still work)
2. Build new apps against PocketBase tokens
3. Move users into PocketBase's `users` in batches (bulk-import by CSV)
4. Once everyone is across, remove Microsoft from OAuth2 — the Entra dependency is cut

You don't cut over in one stroke. **Run both in parallel, and close the old
gate only after the move is done** (parent series, Chapter 7).

## Summary

On the foundation, the first gate.

- **PocketBase** — auth, admin UI, API, and file storage in a single binary (on SQLite)
- **Email / OAuth2 / OTP / MFA** — open only the doors you need, from the admin UI
- **Separate gate from warehouse** — identity in PocketBase, business data in PostgreSQL
- **Reverse proxy** — line packaged OSS up behind the gate
- **Step off Entra ID** — bridge with OAuth2, then cut once the move is done

The only code written is one line that checks a token. **A gate is stood up
and shared.** Next, inside that gate, we set up **documents (OnlyOffice)** and
bring Word, Excel, and PowerPoint to our own side.

---

## Related articles

- [Chapter 6: Lay the Foundation — PostgreSQL, SQLite, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [Reference implementation kura — a self-hosted workspace using PocketBase as the gate](https://github.com/aiseed-dev/workspace)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
- [Parent series, Chapter 7: Living with Business Systems — Rewrite by Running in Parallel](/en/ai-native-ways/business-systems/)
