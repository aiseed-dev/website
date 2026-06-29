---
slug: auth
number: "03"
part: "2"
lang: en
title: "Stand Up the Gate — One Login with PocketBase"
subtitle: "Share only identity (authentication) — each server enforces its own access control. Central minimal, defense in depth"
description: Authentication is not something each app builds on its own. It is a gate you stand up once and share. But the gate holds only the minimal common thing — identity. Authorization ("what you can do") is held by each app, each server, itself (defense in depth); the single-perimeter idea that "whoever passed the gate goes anywhere inside" is not the design. PocketBase is a single binary with email auth, OAuth2, one-time codes, MFA, an admin UI, and a REST API. Identity lives in the gate; business data lives in PostgreSQL. Step off Microsoft Entra ID's per-seat monthly bill.
date: 2026.07.02
label: Independence 3
title_html: One <span class="accent">identity</span>,<br>defense at <span class="accent">every server</span>.
prev_slug: foundation
prev_title: "Lay the Foundation — SQLite, PostgreSQL, pgvector, DuckDB, Polars"
next_slug: code
next_title: "Bring Code In-House — Forgejo and Zed"
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
up after this shares the same identity (who).** Documents, course booking,
the core systems — users log in once.

But settle one principle here. **The gate holds only the minimal common
thing — identity (authentication).** Authorization — "what you can do" — is
held by **each app, each server, itself.** The idea that "whoever passed the
gate goes anywhere inside" — a single perimeter — is not the design here:
breach one place and everything falls. **Central minimal, defense
distributed across each server.** That is the form that is distributed and
strong.

A homegrown login means hashing, sessions, token revocation, two-factor,
password reset, social login — not one of them can be skimped. **Standing up
the identity check once and sharing it, while leaving the permission
decision to each app,** is faster, safer, and stronger.

## Stand up PocketBase

The gate is **PocketBase**. A single **Go binary** carries authentication, an
admin UI, REST / realtime APIs, and file storage. It **runs on the SQLite**
introduced in 2-02, so there is no separate server to run. One
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
data (what they did) lives in PostgreSQL** (2-02). Separate the gate
from the warehouse.

An app **verifies the token's signature locally and pulls out `user.id`**
(no per-request call to the gate — it keeps working even if the gate blinks).
Then **whether this user may do this operation is decided by the app itself.**

```python
# app side — verify the signature locally, decide permission yourself
user_id = verify_token(request.headers["Authorization"])   # signature-checked with the gate's public key (no per-request call)
require(can_read_orders(user_id))                          # "what you can do" is decided by this app
orders  = pg.execute("SELECT * FROM orders WHERE user_id = %s", [user_id])
```

Identity verification is concentrated in the gate; **the permission decision
stays in each app.** Share identity, but distribute defense across every
server — that is defense in depth.

> Identity is not something each app builds on its own — stand it up once and
> share it. **But "what you can do" is guarded by each server itself.**

## Stand it in front — the reverse proxy

Apps you build yourself are guarded directly by the PocketBase SDK. Packaged
OSS like documents (OnlyOffice) or code (Forgejo), on the other hand, **each
carry their own login.** Put a **reverse proxy (Caddy)** in front and let the
outside reach them only through the gate — but this is the **first layer**,
not the only one: each app still verifies identity and permission itself
(don't trust the inside of the perimeter either — defense in depth).

```caddy
# Caddyfile — line up each app behind the gate
auth.example.com   { reverse_proxy auth:8090 }
docs.example.com   { reverse_proxy onlyoffice:80 }
git.example.com    { reverse_proxy forgejo:3000 }
```

To later bind these into **one login (SSO)**, add a layer that speaks OIDC in
front — but for most in-house use, the gate plus each app's own login is
enough. **Sharing one identity comes first;** full unification can wait.

## Step off Entra ID

Microsoft Entra ID bills monthly, stacking with every user. Stand the gate up
on your own side and step off that meter. The move can be gradual.

1. Stand up PocketBase, keep Microsoft in OAuth2 (existing accounts still work)
2. Build new apps against PocketBase tokens
3. Move users into PocketBase's `users` in batches (bulk-import by CSV)
4. Once everyone is across, remove Microsoft from OAuth2 — the Entra dependency is cut

You don't cut over in one stroke. **Run both in parallel, and close the old
gate only after the move is done** (2-09).

## Summary

On the foundation, the first gate.

- **PocketBase** — auth, admin UI, API, and file storage in a single binary (on SQLite)
- **Email / OAuth2 / OTP / MFA** — open only the doors you need, from the admin UI
- **Separate gate from warehouse** — identity in PocketBase, business data in PostgreSQL
- **Central minimal, defense at every server** — the gate holds only identity; access control lives in each app (defense in depth)
- **Reverse proxy** — line packaged OSS up behind the gate (the first layer, not the only wall)
- **Step off Entra ID** — bridge with OAuth2, then cut once the move is done

The only code written is a few lines that check a signature and decide a
permission. **Share identity; defend at every server.** Next, inside that gate, we set up **documents (OnlyOffice)** and
bring Word, Excel, and PowerPoint to our own side.

---

## Related articles

- [2-02: Lay the Foundation — SQLite, PostgreSQL, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [Reference implementation kura — a self-hosted workspace using PocketBase as the gate](https://github.com/aiseed-dev/workspace)
- [2-01: Becoming Independent from Microsoft and Google — The Whole Map](/en/ai-native-ways/software/independence/)
- [2-09: Build an API — Expose Core Logic with FastAPI](/en/ai-native-ways/software/fastapi/)
