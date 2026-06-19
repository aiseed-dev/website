---
slug: microsoft-365
number: "14"
lang: en
title: "Replacing Microsoft 365 Wholesale — Ten One-to-One Mappings"
subtitle: "Move the foundation of your business out of the vendor's cage and into your own hands"
description: Business Microsoft 365 bundles six layers — identity, documents, sharing, mail, portals, AI — into one vendor. Because they are bundled, one vendor's decisions move all of them. Unbundle the six, one at a time, into open self-hosted tools — Entra ID becomes PocketBase, Word/Excel/PowerPoint becomes OnlyOffice, SharePoint+GitHub becomes Forgejo+Zed, Exchange+Outlook becomes Postfix+Thunderbird, Power Pages becomes Cloudflare Pages, and Copilot (metered) becomes Command A+ (Apache 2.0). Meetings move Teams to Jitsi / BigBlueButton, scheduling to CalDAV + Cal.com. Then the substrate beneath — Azure SQL becomes PostgreSQL, C#/.NET/VBA becomes Python/Ruby + Rust. Ten in all, with the build method for each layer.
date: 2026.05.03
label: AI Native 14
title_html: Dissolve <span class="accent">Microsoft 365</span><br>into <span class="accent">tools you own</span>.
prev_slug: one-plus-ai
prev_title: "One Person + AI — The New Unit of Work"
next_slug:
next_title:
---

# Replacing Microsoft 365 Wholesale — Six One-to-One Mappings

**The real nature of business Microsoft 365 is that it is bundled.**

Chapter 6 moved your paperwork out of Office; Chapter 7 rewrote business
systems by running them in parallel. This chapter widens both to the
**whole company** — it unties identity, documents, sharing, mail,
portals, and AI from a single contract and puts them back on your side.

There is only one thing to do: **untie the bundle into six independent
tools.**

## Being bundled IS the lock-in

Microsoft 365 is convenient because login (Entra ID) connects straight
into documents (Office), documents into sharing (SharePoint), sharing
into mail (Exchange), mail into portals (Power Pages), and AI (Copilot)
into all of them — **all on one account, in one straight line.**

But that straight line is the very shape of the lock-in.

- A price hike hits **all six layers** at once — nowhere to escape
- A data-policy change hits **all six layers** at once
- One vendor's outage stops **all six layers** at once (the prologue's single point of failure)
- Copilot's judgment seeps into **all six layers**

> Bundled means convenient, and bundled means held hostage.
> **Convenience and hostage are two faces of one chain.**

The way out is also one thing: **split the six layers into six
independent tools.** Each can be replaced on its own, and if one falls
the others keep running — this is Chapter 13's "one + AI" at the scale
of the company: **autonomous N beats centralized 1.**

## The six one-to-one mappings

Untie the bundle and each layer maps cleanly. **One-to-one** — replace
the left with the right.

| Microsoft 365 (bundle) | Self-hosted replacement | Role of that layer |
| --- | --- | --- |
| **Entra ID** (identity) | **PocketBase** | user auth, OAuth2, roles |
| **Word / Excel / PowerPoint** | **OnlyOffice** | editing docs, sheets, slides |
| **SharePoint + GitHub** | **Forgejo + Zed** | sharing + versioning, local editing |
| **Exchange + Outlook** | **Postfix + Thunderbird** | mail delivery + reading |
| **Power Pages** | **Cloudflare Pages** | business portals, public sites |
| **Copilot** (metered) | **Command A+** (Apache 2.0) | AI — fully local, open weights |

The six on the right are **separate open tools built by separate
organizations.** So one vendor's decision can't ripple into the others.
Swap any one for something else and the remaining five don't change.
**The bundle is untied** — that is the whole point.

```mermaid
flowchart TB
  subgraph Bundle["Microsoft 365 — one vendor bundles six layers"]
    direction TB
    E1["Entra ID"]
    O1["Word / Excel / PowerPoint"]
    S1["SharePoint + GitHub"]
    X1["Exchange + Outlook"]
    P1["Power Pages"]
    C1["Copilot (metered)"]
    E1 --- O1 --- S1 --- X1 --- P1 --- C1
  end

  subgraph Unbundled["Self-hosted — six independent tools"]
    direction TB
    E2["PocketBase"]
    O2["OnlyOffice"]
    S2["Forgejo + Zed"]
    X2["Postfix + Thunderbird"]
    P2["Cloudflare Pages"]
    C2["Command A+"]
  end

  Bundle ==>|untie the bundle = hikes, outages, policy stop crossing layers| Unbundled

  classDef bad fill:#fef3e7,stroke:#c89559,color:#5a3f1a
  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  class E1,O1,S1,X1,P1,C1 bad
  class E2,O2,S2,X2,P2,C2 good
```

Below is the **build method** for each of the six, in turn. They all run
on a small miniPC, a single VPS, or your own machine. The order doesn't
matter — start with the easiest layer and pull one out of the bundle at
a time.

First, set up one place to put things: **one Linux box** (a Debian/Ubuntu
VPS, or a miniPC on the office LAN). Put Docker on it.

```bash
# Install Docker on Debian/Ubuntu (the foundation)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"   # re-login to apply the group
docker compose version            # check
```

## Entra ID → PocketBase — hold your own authentication

**Entra ID hands "who is allowed to log in" to Microsoft.** Cut it, and
the top of the bundle is severed.

PocketBase packs SQLite, authentication, and an admin UI into **a single
executable** (a ~15 MB Go binary). Email+password auth, 15+ OAuth2
providers (Google, GitHub, Microsoft …), user roles, an admin dashboard
— everything an identity layer needs.

### Build it

```bash
# Drop one binary and run
mkdir -p ~/pb && cd ~/pb
wget https://github.com/pocketbase/pocketbase/releases/latest/download/pocketbase_linux_amd64.zip
unzip pocketbase_*.zip
./pocketbase serve --http=0.0.0.0:8090
```

Once running, open `http://<server>:8090/_/`. Create the admin, open the
`users` auth collection, and register staff accounts. For OAuth2, enter a
provider's Client ID / Secret in the settings and people log in with
their Google or GitHub account.

Each app (OnlyOffice, the internal web, the portal below) **asks this
PocketBase over its API** to log a user in. `POST /api/collections/users/
auth-with-password` returns a JWT — that becomes the shared company pass.
The auth logic lives in your own SQLite and never routes through
Microsoft.

> Whoever holds authentication holds the foundation.
> **Take that foundation back into a single 15 MB file.**

## Word / Excel / PowerPoint → OnlyOffice

**The substance of Office is not the app — it is the .docx / .xlsx /
.pptx format.** OnlyOffice reads and writes those three formats **as-is**,
with high fidelity. So even when the organization keeps demanding Office
formats, your exit hurts nothing (Chapter 6's "convert at the exit,"
minus even the conversion).

Two options: a **desktop editor** for individual work, a **Document
Server** for **in-browser collaboration.**

### Desktop (on each machine)

```bash
# Debian/Ubuntu
wget https://download.onlyoffice.com/install/desktop/editors/linux/onlyoffice-desktopeditors_amd64.deb
sudo apt install ./onlyoffice-desktopeditors_amd64.deb
```

Windows / macOS use the official installer; on Flatpak,
`flatpak install flathub org.onlyoffice.desktopeditors`. Now a `.docx`
double-click opens here instead of Word.

### Browser collaboration (Document Server)

```bash
# When several people edit the same document at once
docker run -d --name onlyoffice -p 8081:80 \
  -e JWT_ENABLED=true -e JWT_SECRET=change-me \
  onlyoffice/documentserver
```

Combine `JWT_SECRET` with the pass issued by PocketBase above so only
logged-in staff can open a document. Store the documents themselves in
Forgejo (next section) or shared storage; OnlyOffice acts as their
**editing surface.** **Keep the substance in Markdown / SQLite as in
Chapter 6, and let Office formats be only the "exit to other people"** —
OnlyOffice serves that exit with no conversion at all.

## SharePoint + GitHub → Forgejo + Zed

**SharePoint is "sharing and versioning"; GitHub is also "sharing and
versioning."** What was split into internal and external **folds into a
single Forgejo.** Forgejo is a lightweight self-hosted Git forge derived
from Gitea — repositories, issues, wikis, pull requests, and CI, all on
one miniPC. Documents, spreadsheets, code: everything versioned in Git.

The tool in your hands is **Zed** — a fast editor that writes Markdown
and code and has AI integration. Instead of SharePoint's "open in the
browser, lock, edit," you **open in Zed and push to Forgejo.**

### Build Forgejo

```yaml
# compose.yaml — stand up Forgejo on a miniPC/VPS
services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:9
    ports: ["3000:3000", "222:22"]
    volumes: ["./forgejo:/data"]
    environment:
      - FORGEJO__server__DOMAIN=git.example.com
    restart: always
```

```bash
docker compose up -d              # start
# open http://<server>:3000 → create the admin
```

Open it in a browser, create the admin, and make one Organization. That
becomes the company's "shared place." Minutes (Chapter 3's Markdown),
customer data (Chapter 5's JSON / SQLite), business code (Chapter 2's
Python) — put it all in repositories and push, and **who changed what,
and when, is all recorded.** SharePoint's "which is the latest version?"
problem disappears.

### Install Zed

```bash
curl -f https://zed.dev/install.sh | sh   # Linux / macOS
```

Open the document folder in Zed, edit, `git push`. Collaboration comes
through Forgejo pull requests — prose review and code review run on the
same mechanism.

> Merge internal SharePoint and external GitHub into **one Forgejo.**
> Sharing and versioning were always the same problem.

## Exchange + Outlook → Postfix + Thunderbird

**Mail is the hardest of the six layers.** Let me be honest here.

Exchange is the mail server (delivery, storage); Outlook is the mail
client (reading). The client swap is easy — install **Thunderbird**,
configure an IMAP/SMTP account, and you replace Outlook today.

```bash
sudo apt install thunderbird       # Debian/Ubuntu
# Windows/macOS use the thunderbird.net installer
```

The server side is the hard part. A complete mail server is not Postfix
(SMTP) alone; in practice it is **Postfix + Dovecot (IMAP) + Rspamd
(spam) + OpenDKIM (signing).** And unless you set the DNS **MX / SPF /
DKIM / DMARC** correctly, your mail won't reach other companies (it gets
marked as spam).

So in practice, stand all of it up at once with **mailcow** or
**Mail-in-a-Box.**

```bash
# mailcow — Postfix+Dovecot+Rspamd etc. in one docker stack
git clone https://github.com/mailcow/mailcow-dockerized && cd mailcow-dockerized
./generate_config.sh              # it asks for your domain
docker compose up -d
```

Then add the DNS records (the admin UI shows the values you need).

- **MX** → points to your mail server
- **SPF / DKIM / DMARC** → anti-spoofing, raises deliverability
- **PTR (reverse DNS)** → set on the VPS provider side (matters for delivery)

Once configured, connect Thunderbird over IMAP/SMTP. Now **the substance
of your mail sits on your own disk, not in Microsoft's cloud.**

> Mail is hard. But keep "outsource it because it's hard" and
> **one vendor keeps holding the content of your communication.**
> Stand it up once, and it runs.

## Power Pages → Cloudflare Pages

**Power Pages is "build a business portal or public site low-code and let
Microsoft host it."** That, too, counts as part of the bundle's lock-in.

The replacement is **Cloudflare Pages.** Take the static site you built
in Chapter 8 ("back to HTML+CSS+JavaScript") and a single Git push
delivers it worldwide. Need dynamic logic? Add **Pages Functions**
(Workers). The free tier is generous, custom domains are free, and SSL
is automatic.

### Build it

The simplest path is to connect the Forgejo (or GitHub) repository from
earlier, or deploy directly with `wrangler`.

```bash
npm i -D wrangler                 # Cloudflare's CLI
npx wrangler pages deploy ./public --project-name=portal
```

That publishes instantly to `https://portal.pages.dev`; assign a custom
domain in the dashboard. For a portal that needs login, **have the auth
call back to PocketBase** — hit the PocketBase API from a Pages Function
so only staff can enter.

Cloudflare is a vendor too. But unlike Power Pages, **the substance is
standard HTML / JavaScript.** If you dislike it, the same files serve
just as well from Netlify, or your own Nginx — **no lock-in.** That is
the difference between "using a vendor" and "being held by one."

## Copilot (metered) → Command A+ (fully local, Apache 2.0)

The last layer, AI. **Copilot is designed to seep one AI into all six
layers, priced per seat per month.** Price hikes and a flattening of
judgment spread from here to every layer (Chapter 6, "Copilot — even the
AI is held hostage").

Replace it with an **open-weights AI you run entirely inside your own
walls.** The pick is **Command A+** (released May 2026 by Cohere) — a
218B sparse MoE (25B active parameters) you **download from Hugging Face
and run whole on your own servers, or even an air-gapped internal
network.** It does cited output, reasoning, vision input, and many
languages, and **runs on as few as two H100 GPUs.**

**The decisive part is that it runs fully local.** Copilot always routes
your input through Microsoft's cloud — confidential data, personal data,
all of it leaves the building. Command A+ is the opposite: **your
business data never leaves your premises.** No metered cloud either — on
your own GPU, **calling it any number of times costs nothing extra,** and
you're untethered from vendor price changes and API outages.

What makes that work for business is the license. **Command A+ is
Cohere's first Apache 2.0 model** — commercial use is free and
unconditional. The earlier Command R+ / Command A were CC-BY-NC
(non-commercial), so even run locally you **couldn't use them in
business.** That last shackle is off. **The more confidential data a
company holds, the more a locally-run Command A+ pays off.**

### Build it

For the pick (Command A+), pull a quantized build from Hugging Face and
serve it with vLLM. To get a feel first with the lighter Command R,
Ollama is the shortest path.

```bash
# Get a feel first with the lighter Command R (35B)
curl -fsSL https://ollama.com/install.sh | sh
ollama run command-r

# Command A+: pull a quantized build (w4a4 / fp8) from HF, serve with vLLM
pip install vllm
vllm serve CohereLabs/command-a-plus-05-2026-fp8   # ~2× H100
```

As an always-on in-house AI, **generation tasks** — summarizing minutes,
classification, drafting — just hit the OpenAI-compatible API
(`/v1/chat/completions`) directly, at zero marginal cost.

```bash
# This is "generation" — a summary. Not RAG (RAG is below, a different thing)
curl http://localhost:8000/v1/chat/completions -d '{
  "model": "command-a-plus",
  "messages": [{"role":"user","content":"Summarize these minutes in three points: ..."}]
}'
```

One note on the division of labor. For tangled judgment or design
discussions, keep using a frontier model like Claude as a "colleague"
(Chapter 11). The point is to **drop the Copilot pattern that hard-wires
one AI into all six layers and stand on the side that can choose** —
routine to your own Command A+ (or other commercially-usable open models:
Llama / Qwen / gpt-oss), judgment to a colleague you picked. Because it
is Apache 2.0, **you hold the AI you chose as a company asset.**

> Copilot routes your input out to the cloud.
> An Apache 2.0 local model keeps **data and judgment inside the company.**
> Choose it, own it, and never send it out — **that is autonomy.**

### Performance — frontier on raw reasoning, even or better on RAG

Be honest in the comparison. **Copilot is a "product," not a "model"** —
inside, it routes to frontier models like GPT-5.x and Claude and grounds
on your data through Microsoft Graph. So there is no single "Copilot
score." What you can compare is **Command A+ against the frontier model
Copilot runs inside.**

On that ground, **raw reasoning and coding go to the frontier** (Copilot's
insides). No need to hide it — on benchmarks that measure in-the-head
knowledge and reasoning (GPQA, hard coding), it doesn't reach the GPT-5.x
tier.

But **most business AI is RAG** — internal FAQs, Q&A over policies,
contracts, and manuals, knowledge search. That is not about raw
intelligence; it is **grounding answers in your own retrieved documents
and citing them**, where the frontier's reasoning edge barely applies. And
the Command family is **built precisely for RAG**:

- **Native span-level inline citations** — per sentence, "which document,
  which span is the basis"
- **Citation fidelity beats GPT-4-turbo** (Cohere human eval) — it cites
  the relevant spans, short and grounded
- **Low hallucination** (grounding-first design); ~1.75× GPT-4o speed

| | Raw reasoning / coding | RAG (grounded Q&A, citations) |
| --- | --- | --- |
| Copilot (GPT-5.x) | ahead | good, but data goes through the cloud |
| Local Command A+ | doesn't reach | **even or better, higher citation fidelity, fully local** |

And what finally decides RAG accuracy is less the model than **the quality
of what you retrieve.** That is yours to design and improve — your own data
in PocketBase / Forgejo / PostgreSQL plus embedding search.

Answers that come back **with citations** mean **a human can verify the
output** — exactly the verification layer of Chapter 12 ("Verifying
Narratives with AI"). A local RAG that returns grounded, linked answers
is, for business, more trustworthy than a frontier black box.

> On raw intellect, concede to the frontier.
> But on business's main battlefield — RAG — **cited, low-hallucination,
> fully local.** No need to match it on raw performance — **win on the
> ground where you win.**

### Local RAG: you build the retrieval

Be clear about one thing. **RAG is not one API call.** Throwing a prompt
at `/v1/chat/completions` is generation, not RAG. RAG quality is decided
less by the generation model than by **retrieval** — and that you build
yourself.

The minimal fully-local stack (all on your own box):

- **Embeddings**: `bge-m3` (multilingual) via Ollama (`ollama pull bge-m3`)
- **Store + search**: **pgvector** (an extension on the PostgreSQL you
  already stood up). On the PocketBase side, `sqlite-vec`
- **Hybrid search**: semantic (pgvector) + keyword (BM25 / full-text)
  together — that alone lifts accuracy 20–30%
- **Rerank**: `bge-reranker-v2-m3` reorders the top hits (another 15–30%)
- **Grounded generation (with citations)**: pass the retrieved chunks as
  **`documents[]`**; Command A+ returns `[1] [2]` span citations

```sql
-- pgvector: semantic search (just add the extension to your PostgreSQL)
CREATE EXTENSION IF NOT EXISTS vector;
SELECT id, body FROM docs ORDER BY embedding <=> :query_vec LIMIT 20;
```

The **citations** don't appear if you paste the text into the prompt. You
must use Command's **grounded generation template** (passing `documents`)
— when self-serving, `vllm>=0.21` plus Cohere's `melody` (`cohere_melody`)
to parse the citations correctly.

In short, **you build, on your own side, the "retrieve + ground" that
Copilot hid behind Microsoft Graph.** It is more work. But holding the
retrieval is holding the **accuracy** — and keeping the **data inside.**

> RAG is not "call a smart model over an API."
> It is **searching your own data and answering with the grounds attached.**
> You build the search — that is the real body of business AI.

## Meetings and courses — untie Teams and the calendar

The six-layer bundle has one more everyday collaboration face — **meetings
(Teams) and scheduling (the calendar)**. You need it especially **to run
courses.** Gather attendees, let them book a slot, and teach in a room —
provide those three yourself.

| Microsoft 365 | Self-hosted replacement | Role of that layer |
| --- | --- | --- |
| **Teams** (video meetings) | **Jitsi Meet** (BigBlueButton for courses) | meetings, online classes |
| **Outlook / Bookings** (calendar, scheduling) | **CalDAV (Radicale) + Cal.com** | calendar + course booking |

### Teams → Jitsi Meet (BigBlueButton for courses)

For ordinary meetings, **Jitsi Meet.** Stand it up on one box with Docker
and hand out a URL — a room opens, no account signup needed.

```bash
# Self-host Jitsi Meet with Docker
git clone https://github.com/jitsi/docker-jitsi-meet && cd docker-jitsi-meet
cp env.example .env && ./gen-passwords.sh
docker compose up -d        # a room opens at https://<domain>
```

For **courses**, use **BigBlueButton.** It was **built from the start as a
virtual classroom for online teaching** — real-time whiteboard, slide
sharing, breakout groups, polls, and **recording.** The attendee
experience is close to a real classroom. It's heavier than Jitsi (wants a
16 GB-class server), but **if you're serious about courses, this is the
pick.** Attendee data goes to no third party — it stays entirely inside
your own server.

### Outlook / Bookings → CalDAV + Cal.com

A calendar is really **CalDAV.** Stand up **Radicale** (a few-MB Python
server, up in 5 minutes) and the **Thunderbird** you already have becomes
your calendar — the Thunderbird from the mail layer doubles as mail and
calendar.

```bash
# Radicale — the minimal CalDAV server
pip install radicale
python3 -m radicale --storage-filesystem-folder ~/radicale/collections
# Add CalDAV in Thunderbird: http://<server>:5232/
```

For **course booking** (attendees pick their own slot), use **Cal.com** —
the open-source Calendly. Stand it up with Docker and hand out the public
page; attendees pick an open slot and book. What Microsoft Bookings did,
done **on your own domain, at zero commission.**

> A course can open without renting a venue.
> **The classroom (BigBlueButton) and the booking page (Cal.com) can both
> sit on your side.**

## The substrate beneath — untie Azure SQL and .NET too

Beneath the six-layer bundle sits one more Microsoft foundation — **the
database (Azure SQL) and the runtime for business apps (C# / .NET /
VBA)**. This is the layer Chapter 7 ("rewrite by running in parallel")
covers in depth. Add **the two substrate rows**, and the Microsoft
dependency comes untied almost entirely, one-to-one.

| Microsoft foundation | Self-hosted replacement | Role of that layer |
| --- | --- | --- |
| **Azure SQL** | **PostgreSQL** | the database |
| **C# / .NET / VBA** | **Python / Ruby + Rust** | the business-logic runtime |

### Azure SQL → PostgreSQL

Azure SQL is SQL Server in the cloud. Keep standard SQL (`SELECT`,
`JOIN`, window functions) as-is and **drop only the vendor dialect,
T-SQL** (Chapter 7). For the move, `pgloader` carries schema and data in
one pass.

```bash
# Stand up PostgreSQL
docker run -d --name pg -p 5432:5432 \
  -e POSTGRES_PASSWORD=change-me -v ./pg:/var/lib/postgresql/data postgres:17

# Migrate Azure SQL → PostgreSQL in one pass (schema + data)
pgloader mssql://user:pass@azure-host/db postgresql://postgres:change-me@localhost/db
```

Business logic buried in T-SQL stored procedures gets extracted by Claude
and translated into Python / Ruby — **the invisible stored proc becomes
readable code** (Chapter 7). Then, as in Chapter 7, run it in parallel
with the old Azure SQL, reconcile the output, and stop the old when the
difference is gone. License and metered fees vanish entirely.

### C# / .NET / VBA → Python / Ruby + Rust

Think of the runtime in three layers.

- **The glue is Python / Ruby** — thin languages for writing business
  logic. Replace C# / .NET apps with Python (FastAPI) or Ruby (Sinatra +
  raw SQL), and **externalize Excel / Access VBA into Python** (Chapters
  2 and 6)
- **Heavy work and type safety go to Rust (the lower layer)** — where
  speed and rigor are needed, don't write it by hand; **push it down into
  Rust-built packages** (Polars, Pydantic's core). Type safety is the
  lower layer's job — the series' standing principle
- **Claude writes, you run locally** — the dependency on the vendor
  runtime (.NET CLR) disappears, and the code becomes readable and
  testable

The more you're used to C#'s static types, the more "Python is loosely
typed" worries you. But the point is to **not guarantee type safety in
human code** — leave that to the Rust-built lower layer (Polars /
Pydantic) and let Python / Ruby be **the glue that writes judgment.**
This too goes through Chapter 7's **parallel operation**, reconciling
output against the old .NET as you replace it piece by piece.

> Six in the bundle, two for meetings and calendar, two in the substrate. **Ten in all, every one
> one-to-one.** With that, the Microsoft dependency comes nearly
> completely untied.

## What changes — cost and autonomy

Untie it and the monthly structure changes. Microsoft 365 is
**seats × monthly fee** (Business Standard runs roughly ¥1,500–2,500 per
person per month, plus several thousand more per person for Copilot) —
it grows linearly as headcount grows. The self-hosted toolset is **the
fixed cost of one server** (a VPS at ¥1,000–a few thousand a month, or
just electricity for an office miniPC) — barely moving as headcount
grows.

But the substance is not cost (same as Chapter 6). The substance is that
**the bundle is untied.**

- A vendor raises prices — swap only that one layer
- A vendor has an outage — the other five keep running
- A vendor changes its data policy — the impact stays in that layer
- The company gets to choose the AI's judgment

```mermaid
flowchart LR
  Q["want to replace<br>this one layer"]
  Bundle["Microsoft 365<br>(bundle)"]
  Unb["self-hosted<br>(six)"]
  R1["migrate all six<br>= effectively impossible"]
  R2["swap just that one<br>= the rest untouched"]

  Q --> Bundle ==>|bundled| R1
  Q --> Unb ==>|untied| R2

  classDef bad fill:#fef3e7,stroke:#c89559,color:#5a3f1a
  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  class Bundle,R1 bad
  class Unb,R2 good
```

## In what order to untie

You don't have to do it all at once (same practice as Chapter 6). Pull
out **whatever leaves the bundle most easily**, one at a time.

1. **Thunderbird** (client first) — leave the server as Exchange, move
   reading off Outlook. Zero-risk start.
2. **OnlyOffice desktop** — move individual editing off Office.
3. **Forgejo + Zed** — move sharing and versioning off SharePoint. Here
   "which is the latest?" disappears.
4. **Cloudflare Pages** — move the public site and portal.
5. **Command A+ (an Apache 2.0 open model)** — move routine
   AI work off Copilot.
6. **PocketBase / mail server** — authentication and mail delivery. Set
   these last, as the foundation under every app.

Run each step with Chapter 7's **parallel operation.** Don't stop the old
(Microsoft); run the new beside it, confirm the same work flows, then
cancel the old. **Time it to the contract renewal** — also per Chapter 7.

## One person + AI can run this

The obvious question: **who maintains ten self-hosted things?** The answer
is **one person + AI** — Chapter 13's new unit of work, applied straight to
company infrastructure.

Why one person is enough. Three reasons.

- **They're all standard, boxed, open tools** — PocketBase is one file, the
  rest are a single docker compose. Claude writes the compose, sets up DNS
  and DKIM, reads the logs, isolates faults. **AI is the co-admin.**
- **Because the bundle is untied, failures don't cascade** — with M365 one
  vendor's trouble drags in everything; here, if Forgejo goes down mail
  still lives, and if the AI stops the meetings go on. **Fix each one
  independently.**
- **Visible, readable, testable** — config and logs sit in your own hands.
  Unlike the Copilot black box, you **read the inside and fix it, with AI.**

Honestly, the heavy parts: **the load concentrates in two — mail and
BigBlueButton.** Mail's delivery (DKIM / SPF / reputation) is delicate, so
you can offload just outbound through an external relay. BigBlueButton is
heavy, so **stand it up only for the course season and tear it down after**
(rent cloud GPU by the hour if you like). The other eight, once up, mostly
run themselves.

This is exactly Chapter 13. **No siloed IT department needed.** One person
who understands the business, with AI as partner, holds everything from
identity to mail, courses, AI, and the database across the board.
**Individual autonomy holds at the level of company infrastructure.**

> One person + AI runs ten open tools.
> Versus handing Microsoft 365 to one vendor, **the effort is about the
> same — only the control moves to your side.**

## And then, the core systems

What you've assembled here doubles as **the foundation for rewriting your
core systems.** The parallel-operation rewrite of Chapter 7 ("Living with
Business Systems") actually **assumed a platform to stand on** — and that
platform is now fully in place.

- **A database the new core runs on** — PostgreSQL + pgvector (above)
- **The runtime** — Python / Ruby + Rust (above)
- **Version control and CI** — Forgejo (above)
- **Authentication** — PocketBase takes the new system's logins in one place
- **Extracting business logic** — read the legacy code, SQL, and runbooks
  with **local Command A+ + RAG** and emit Markdown. Chapter 7's "dump the
  business knowledge into Markdown at once," done **without the source ever
  leaving the building.**

So rewriting SAP, Oracle, or a 20-year-old legacy core becomes **just
standing up one more app on the same foundation.** The hard part was the
foundation — and it's already in your hands. The rest is Chapter 7: don't
stop the old, run the new beside it, reconcile the output, and kill the old
when the difference is gone.

> The foundation you built by untying Microsoft 365 is also **the
> foundation for untying your core systems.** Once the platform is on your
> side, the replacement is only "one more step."

## Summary

Business Microsoft 365 is six layers bundled into one vendor.
Convenience and hostage were two faces of one chain.

- **Entra ID → PocketBase** (authentication in a single 15 MB file)
- **Word/Excel/PowerPoint → OnlyOffice** (Office formats as-is)
- **SharePoint + GitHub → Forgejo + Zed** (sharing and versioning in one)
- **Exchange + Outlook → Postfix + Thunderbird** (communication in your hands)
- **Power Pages → Cloudflare Pages** (hosting with no lock-in)
- **Copilot (metered) → Command A+ (fully local, Apache 2.0)** (hold the AI without sending data out)
- **Teams → Jitsi Meet / BigBlueButton** (meetings and online courses)
- **Outlook / Bookings → CalDAV (Radicale) + Cal.com** (calendar and course booking)
- **Azure SQL → PostgreSQL** (the substrate beneath — the database)
- **C# / .NET / VBA → Python / Ruby + Rust** (the substrate beneath — the runtime)

One-to-one — replace the left with the right. The ten on the right are
separate open tools from separate organizations, so **one vendor's
decision can't ripple into the others.** This is not about efficiency —
it is Chapter 13's "one + AI" restated at the height of the company's
foundation. **Autonomous N beats one centralized.**

Untie the bundle. One tool at a time, at your own pace. As far as it
comes untied, the company stops being a vendor's hostage and **starts
moving on its own judgment.**

---

## Related articles

- [Chapter 6: Changing Paperwork — A Realistic Path Away from Office](/en/ai-native-ways/office-replacement/)
- [Chapter 7: Living with Business Systems — Rewrite by Running in Parallel](/en/ai-native-ways/business-systems/)
- [Chapter 8: Building the Web — Back to HTML+CSS+JavaScript](/en/ai-native-ways/web/)
- [Chapter 13: One Person + AI — The New Unit of Work](/en/ai-native-ways/one-plus-ai/)
- [Insights 08: Subtracting the Enterprise IT Tax](/en/insights/enterprise-tax/)
