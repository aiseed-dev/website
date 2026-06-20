---
slug: code
number: "09"
lang: en
title: "Bring Code In-House — Forgejo and Zed"
subtitle: "The builder's workshop, on your own side — repositories and CI, outside Microsoft"
description: A builder's work is to have AI write code, evaluate it, and integrate it. The place that code lives — the repository — gets stood up on your own side. Forgejo is a single Git forge that replaces GitHub and Azure DevOps, with Actions covering CI/CD. It rides on the PostgreSQL from Chapter 6 and sits behind the gate from Chapter 7. The local tools are Zed and Claude. Code is an asset; control of where it lives stays with you.
date: 2026.07.06
label: Software 09
title_html: Put the home of your code<br>on <span class="accent">your own side</span>.
prev_slug: documents
prev_title: "Take Documents Back — Nextcloud and OnlyOffice"
next_slug: sier-uneconomic
next_title: "The Structural Uneconomy of the SIer Model"
---

# Bring Code In-House — Forgejo and Zed

A builder's work is not writing code. It is **having AI write it, evaluating
it, and integrating it** (Chapter 4). But the code that results needs a place
to live — the repository. The more code AI generates, the more **control over
where it lives** matters.

GitHub and Azure DevOps both sit on someone else's servers. Here, that
workshop gets stood up on **your own side.**

## Why keep code on your own side

Code is an asset. The substance of the business itself is written there. The
reason to leave it parked on someone else's platform is now thin.

- **Cut the dependency** — pricing, terms, and availability don't change at another company's convenience
- **Couple it tightly with AI** — generation, review, and CI run by your own rules
- **One with the gate** — code goes inside the Chapter 7 authentication too

Generic Git hosting is already there as OSS. **You don't write it, you stand
it up.**

## Stand up Forgejo

The workshop is **Forgejo.** A single Gitea-family binary carrying
repositories, issues, pull requests, review, and CI in one — a replacement for
GitHub, GitLab, and Azure DevOps. The data rides on the **PostgreSQL from
Chapter 6.**

```yaml
# compose.yaml — stand up Forgejo on the Chapter 6 DB
services:
  code:
    image: codeberg.org/forgejo/forgejo:latest
    environment:
      FORGEJO__database__DB_TYPE: postgres
      FORGEJO__database__HOST: db:5432      # the Chapter 6 PostgreSQL
      FORGEJO__database__NAME: forgejo
      FORGEJO__database__USER: postgres
      FORGEJO__database__PASSWD: change-me
    volumes: ["./forgejo:/data"]
    ports: ["3000:3000", "2222:22"]
    restart: always
```

```bash
docker compose up -d
git remote add origin ssh://git@localhost:2222/team/app.git
git push -u origin main          # already on your own server
```

## CI/CD — Forgejo Actions

Automating tests, builds, and deploys is **Forgejo Actions.** Workflows in the
**same syntax** as GitHub Actions run as-is. Just drop one file in the repo.

```yaml
# .forgejo/workflows/ci.yml
on: [push]
jobs:
  test:
    runs-on: docker
    steps:
      - uses: actions/checkout@v4
      - run: pytest          # on your own runner, at zero marginal cost
```

Step off GitHub Actions' metered billing. **The runner is on your side too,**
so you can verify AI-written code any number of times without watching a meter.

## The local tools — Zed and Claude

If the server is Forgejo, local editing is **Zed.** A Rust-built, lightweight
editor with co-editing and **AI integration.** Call Claude in place to
generate, fix, and explain, while the builder concentrates on **evaluation and
integration.**

```bash
git clone ssh://git@localhost:2222/team/app.git
zed app/          # call Claude, have it write, evaluate, and push
```

AI writes; the human decides. With the workshop (Forgejo) and the tool (Zed) in
place, that division of labor just runs.

## Place it behind the gate, and migrate

Put Forgejo behind the reverse proxy (Chapter 7). Migrating from GitHub,
Forgejo's **"New Migration"** imports a repository together with its issues and
PRs.

```caddy
git.example.com { reverse_proxy code:3000 }
```

No need to switch in one stroke. **Keep GitHub as a mirror and run in
parallel,** then move production onto Forgejo once it feels natural (parent
series, Chapter 7).

> Code is the substance of the business itself.
> Control of where it lives belongs to **you, not another company.**

## Summary

The builder's workshop, on your own side.

- **Forgejo** — repositories, issues, PRs, and review in one (on the Chapter 6 PostgreSQL)
- **Forgejo Actions** — GitHub Actions-compatible CI/CD, the runner on your side
- **Zed + Claude** — call AI into a lightweight editor; write, evaluate, push
- **Behind the gate** — fenced by the reverse proxy, migrate from GitHub gradually

The only code written is configuration. **The generic is already there, as
OSS.** Next, we stand up **mail (Stalwart)** on our own side and cut the
dependency on Exchange and Outlook.

---

## Related articles

- [Chapter 4: The Builder Role](/en/ai-native-ways/software/builder/)
- [Chapter 7: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Parent series, Chapter 9: Building Apps — CLI Tools, Flet Apps, Flutter Apps](/en/ai-native-ways/apps/)
