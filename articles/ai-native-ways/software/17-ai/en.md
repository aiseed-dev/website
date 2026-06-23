---
slug: ai
number: "09"
part: "2"
lang: en
title: "Stand Up Your Own AI — LLM and RAG"
subtitle: "Lay AI on top of everything — answers grounded in your own data, on your own side"
description: The Setup part closes by laying AI on top of everything. The pgvector enabled in Chapter 6 finally pays off. Stand up an open model with Ollama or vLLM, embed your documents, code, and mail into pgvector for RAG, and use it through Open WebUI. Keep secrets and always-on processing in-house; borrow a frontier model like Claude for hard judgment — control yours, capability borrowed. Cut the Copilot dependency and close the Setup part.
date: 2026.07.16
label: Independence 9
title_html: Lay <span class="accent">your own AI</span><br>on top of everything.
prev_slug: fastapi
prev_title: "Build an API — Expose Core Logic with FastAPI"
next_slug: sier-uneconomic
next_title: "The Structural Uneconomy of the SIer Model"
---

# Stand Up Your Own AI — LLM and RAG

The Setup part closes by laying **AI** on top of everything stood up so far.
Foundation, gate, documents, code, mail, meetings — an AI grounded in the data
piled there, on your own side. The **pgvector** enabled back in Chapter 6
finally pays off here.

## Why your own AI

- **Keep data in** — don't hand confidential internal documents to another company's API
- **Always-on is cheap** — run classification, summarization, and extraction continuously at zero marginal cost
- **Grounded in your data** — answer in light of internal documents, code, and history

## Stand up the model — Ollama and vLLM

To start easily, **Ollama.** Stand up an open model (Qwen, Llama, and the like)
in one line and use it as an API.

```bash
docker run -d -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull qwen2.5    # pull a model and use it at once
```

As volume grows, move to the higher-throughput **vLLM.** For always-on
processing that needs higher quality, you can choose the privately deployable
**Command A** (mentioned in Chapter 6). **Stand one up first, swap as needed.**

## RAG — put pgvector to work

This is the payoff from Chapter 6. Turn internal documents, code, and mail into
**embeddings (vectors),** put them in pgvector, pull the fragments closest to a
question, and have the model answer — this is **RAG** (retrieval-augmented
generation).

```python
# 1) embed a document and put it in the Chapter 6 pgvector
emb = embed(text)                       # a local embedding model
pg.execute("INSERT INTO docs(body, embedding) VALUES (%s, %s)", [text, emb])

# 2) pull the closest fragments and have the model answer
hits = pg.execute(
  "SELECT body FROM docs ORDER BY embedding <=> %s LIMIT 5", [embed(q)])
answer = llm(f"Answer based on the following sources:\n{hits}\n\nQuestion: {q}")
```

The table for which Chapter 6 "only had the vessel ready" now gets its
contents. **An AI that answers from your own real data, with citations,** stands
up on your side.

## The chat UI — Open WebUI

The window people use is **Open WebUI** — a screen resembling ChatGPT or
Copilot, connected to the model and RAG you stood up. Place it behind the
Chapter 7 gate, beyond the reverse proxy.

```caddy
ai.example.com { reverse_proxy open-webui:8080 }
```

## How much to keep in-house — honestly

Open models have reached practical sufficiency. But **for the hardest judgment
and large-scale code generation, frontier models like Claude are still
stronger.** This is the same shape as the mail relay (Chapter 10) and
Cloudflare (Chapter 12).

- **Keep in-house** — processing of confidential data, always-on classification, summarization, RAG (the real body of control)
- **Borrow** — hard judgment and heavy generation go to a frontier model's API

**Control on your side, capability borrowed as needed.** Keeping everything
in-house is not the goal — hold the data and the daily processing in your own
hands, and send only the hardest parts out.

> The value of your own AI is not maximizing cleverness.
> It is **embedding AI into the everyday without letting go of your data.**

## Summary — closing the Setup part

Your own AI, on top of everything.

- **Ollama / vLLM** — stand up an open model; Command A where quality is needed
- **RAG (pgvector)** — fill the Chapter 6 vessel with internal data, answer with citations
- **Open WebUI** — a ChatGPT-like window, behind the gate
- **In-house vs. borrowed** — data and always-on in-house, the hard parts to a frontier model

From Chapter 6 through Chapter 13, we replaced Microsoft 365 and the vendor
packages under the core systems, one at a time, with OSS. Foundation, gate,
documents, code, mail, meetings, booking, web, AI — none of it was **written;
it was stood up.**

> As written at the start of Chapter 6 — **the effect of OSS is greater than
> the effect of AI.** The generic is already shared with the world.

That closes **how you build it (the Setup part).** From the next chapter the
viewpoint shifts — **why this changes the industry's structure (the Shift
part).** In an era when you can stand it up yourself, why does the
SIer-commissioned model become structurally uneconomic?

---

## Related articles

- [Chapter 6: Lay the Foundation — PostgreSQL, SQLite, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [Chapter 14: The Structural Uneconomy of the SIer Model](/en/ai-native-ways/software/sier-uneconomic/)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
