---
slug: ai
number: "10"
part: "2"
lang: en
title: "Stand Up Your Own AI — LLM and RAG"
subtitle: "Lay AI on top of everything — answers grounded in your own data, on your own side"
description: The Independence part closes by laying AI on top of everything. The pgvector enabled in 2-02 finally pays off. Start by holding Cohere's open-weight coding model North Mini Code locally on Ollama (data never leaves), and load a general model and embeddings alongside for RAG. Embed your documents, code, and mail into pgvector for RAG, and use it through Open WebUI. Keep secrets and always-on processing in-house; borrow a frontier model like Claude for hard judgment — control yours, capability borrowed. Cut the Copilot dependency and close the Independence part.
date: 2026.07.16
label: Independence 10
title_html: Lay <span class="accent">your own AI</span><br>on top of everything.
prev_slug: fastapi
prev_title: "Build an API — Expose Core Logic with FastAPI"
next_slug: two-worlds
next_title: "Companies Don't Write Their Own Code — Office and Core, Two Parallel Worlds"
---

# Stand Up Your Own AI — LLM and RAG

The Independence part closes by laying **AI** on top of everything stood up so far.
Foundation, gate, documents, code, mail, meetings — an AI grounded in the data
piled there, on your own side. The **pgvector** enabled back in 2-02
finally pays off here.

## Why your own AI

- **Keep data in** — don't hand confidential internal documents to another company's API
- **Always-on is cheap** — run classification, summarization, and extraction continuously at zero marginal cost
- **Grounded in your data** — answer in light of internal documents, code, and history

## Stand up the model — North Mini Code on Ollama

To start easily, **Ollama.** Stand up an open-weight model in one line and use
it as an API.

The first one to load is **North Mini Code** (Cohere) — an **open-weight
(Apache 2.0) agentic coding model.** It is exactly the tool this sub-series
centers on: "the builder has AI write the code." A 30B MoE with only 3B
active, it is light enough to run with low latency even on local hardware.

```bash
docker run -d -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull north-mini-code    # open-weight, runs on your own side
```

You can hit it free on OpenRouter to try, but **in production run it yourself —
neither code nor data leaves your side.** Cohere is one corner of **sovereign
AI**, alongside Europe's Aleph Alpha (→ [blog 027](/en/blog/autonomy-distribution-diversity/)).

For RAG and chat, separately load a **general model (Qwen and the like) and an
embedding model** on the same Ollama. As volume grows, move to the
higher-throughput **vLLM**, and for always-on processing that needs higher
quality you can choose the privately deployable **Command A** (Cohere,
mentioned in 2-02). **Stand one up first, swap as needed.**

## RAG — put pgvector to work

This is the payoff from 2-02. Turn internal documents, code, and mail into
**embeddings (vectors),** put them in pgvector, pull the fragments closest to a
question, and have the model answer — this is **RAG** (retrieval-augmented
generation).

```python
# 1) embed a document and put it in the 2-02 pgvector
emb = embed(text)                       # a local embedding model
pg.execute("INSERT INTO docs(body, embedding) VALUES (%s, %s)", [text, emb])

# 2) pull the closest fragments and have the model answer
hits = pg.execute(
  "SELECT body FROM docs ORDER BY embedding <=> %s LIMIT 5", [embed(q)])
answer = llm(f"Answer based on the following sources:\n{hits}\n\nQuestion: {q}")
```

The table for which 2-02 "only had the vessel ready" now gets its
contents. **An AI that answers from your own real data, with citations,** stands
up on your side.

## The chat UI — Open WebUI

The window people use is **Open WebUI** — a screen resembling ChatGPT or
Copilot, connected to the model and RAG you stood up. Place it behind the
2-03 gate, beyond the reverse proxy.

```caddy
ai.example.com { reverse_proxy open-webui:8080 }
```

## How much to keep in-house — honestly

Open models have reached practical sufficiency. But **for the hardest judgment
and large-scale code generation, frontier models like Claude are still
stronger.** This is the same shape as the mail relay (2-06) and
Cloudflare (2-08).

- **Keep in-house** — processing of confidential data, always-on classification, summarization, RAG (the real body of control)
- **Borrow** — hard judgment and heavy generation go to a frontier model's API

**Control on your side, capability borrowed as needed.** Keeping everything
in-house is not the goal — hold the data and the daily processing in your own
hands, and send only the hardest parts out.

> The value of your own AI is not maximizing cleverness.
> It is **embedding AI into the everyday without letting go of your data.**

## Summary — closing the Independence part

Your own AI, on top of everything.

- **Ollama / vLLM** — start with North Mini Code (Cohere, an open-weight
  coding model), add a general model alongside for RAG; Command A where quality is needed
- **RAG (pgvector)** — fill the 2-02 vessel with internal data, answer with citations
- **Open WebUI** — a ChatGPT-like window, behind the gate
- **In-house vs. borrowed** — data and always-on in-house, the hard parts to a frontier model

From 2-02 through 2-10, we replaced Microsoft 365 and the vendor
packages under the core systems, one at a time, with OSS. Foundation, gate,
documents, code, mail, meetings, booking, web, AI — none of it was **written;
it was stood up.**

> As written at the start of 2-02 — **the effect of OSS is greater than
> the effect of AI.** The generic is already shared with the world.

That closes **how you build it (the Independence part).** From the next chapter the
viewpoint shifts — **why this changes the industry's structure (the Shift
part).** In an era when you can stand it up yourself, why does the
SIer-commissioned model become structurally uneconomic?

---

## Related articles

- [2-02: Lay the Foundation — SQLite, PostgreSQL, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [3-03: The Structural Uneconomy of the SIer Model](/en/ai-native-ways/software/sier-uneconomic/)
- [2-01: Becoming Independent from Microsoft and Google — The Whole Map](/en/ai-native-ways/software/independence/)
