---
slug: manual
number: "01"
lang: en
title: "AI (ChatGPT, Claude, etc.) Practical Manual"
subtitle: "Six tips for ordinary people"
description: AI is not a magic tool but "a very capable rookie clerk." Six tips for ordinary people to use AI in daily work — subscribe to one AI, just ask, do not delegate everything, do not send important things to the internet, know its strengths and weaknesses, redirect freed time to culture, science, and reality.
date: 2026.05.21
label: AI Native 01
title_html: AI is not a <span class="accent">magic tool</span>.<br>It is a capable <span class="accent">rookie clerk</span>.
prev_slug: prologue
prev_title: "Office for paperwork, Java/C# for business systems — but AI runs on Python and text"
next_slug: python
next_title: "Writing Logic — Have AI Write Python For You"
---

AI (ChatGPT, Claude, and others) is not a magic tool that does everything for you. Think of it as "a very capable rookie clerk" — like a secretary who handles paperwork — that listens to you and gets actual work done for a few cents per task.

The Prologue laid out the decisive divide between AI-native tools (Python, Markdown, JSON) and standard enterprise tools (Office, Java/C#). This chapter sits one step before that — **six tips for the ordinary person who has not yet touched AI**, for taking back work that had been outsourced to vendors and services, and running it lightly in your own hands. The Python, Markdown, and JSON chapters that follow land much more easily once these six are absorbed.

1. **Subscribe to AI**
2. **Just ask**
3. **Don't delegate everything**
4. **Don't send important things to the internet**
5. **AI's strengths and weaknesses**
6. **Redirect freed time to culture, science, and reality**

## 1. Subscribe to AI

- **Keep one AI (clerk) at your side:** First, sign up for one paid plan — Claude or ChatGPT. About $20–$22 a month (Claude Pro moved to $22 from April 2026 with Japan's consumption tax included). With that, a "very capable rookie clerk" is on hand for you at any time. Think of it as a "living infrastructure" — like electricity, water, or telecom.
- **Once the clerk arrives, many other things become unnecessary:** Hire a $20-a-month clerk and the things you thought you needed start dropping away.
  - **Microsoft 365 (¥21,300 / year):** Raised from ¥14,900 to ¥21,300 (about 43% up) in Japan starting February 2025 (the revision that bundled Copilot). Word, Excel, PowerPoint — all tools from the pre-AI era. The free **ONLYOFFICE Desktop** (the no-cost edition for personal desktop use) is plenty. The three concerns commonly raised about compatibility all dissolve under AI-era practice: **send quotes and contracts as PDFs** (no font drift or page breaks shifting on the receiver's side), **rewrite VBA macros in Python** (the clerk does it in minutes — and the result can be called from other tools), and **collaborate via cloud storage + comments**.
  - **How-to books, business books, self-help books, newspapers, magazines:** Ask the clerk and the key points come back in minutes. **Specialty books** (medicine, law, technical references) are different — those remain important.
  - **Schools and seminars:** Faster to have the clerk teach you while you do the work yourself.
  - **Niche SaaS, outsourcing, agencies:** Invoices, minutes, translation, image editing, accounting, writing, research — one clerk covers most of it.
  - **Consultants:** For general advice, the clerk is faster and cheaper. The exception is "assembly" tailored to your own situation — that goes in tip 5.
- **Do the math:** Instead of $20 a month, how many tens of thousands of yen do you save? Data, knowledge, and work all return to your own hands (your home or office) with the clerk.

## The clerk's personality — which one to pick

AI's character is determined by **what it was trained on**. Just as a chef's specialties depend on the ingredients they trained with, an AI's strengths and tone differ by what dominates its training data.

| AI | Provider | Training core | Personality / strengths |
|---|---|---|---|
| **Claude** | Anthropic | Curated books, papers, code. Trained with Constitutional AI (ethical principles) | Careful and thoughtful, strong with long documents. Industry-leading at coding. Honest enough to say "I don't know," with relatively few hallucinations (tip 5). Holds the "clerk" position without taking judgment from you |
| **ChatGPT** | OpenAI | Broad web, books, code. Tuned with Reinforcement Learning from Human Feedback (RLHF) | Fluent and friendly, fast responses. **Good at matching the user** (it learned what humans rate highly). Rich feature set — image generation (DALL-E), voice, many plugins. Best known. The flip side is a weak spot: **it agrees too readily** with the user and rarely flags your mistakes — the well-known "**sycophancy**" |
| **Gemini** | Google | Google's search index, YouTube, Google Books, academic papers. Multimodal-focused | Integrates with Gmail, Drive, Calendar, search. Strong with video and image. A good fit for Google-service-centric work |
| **Grok** | xAI (Elon Musk) | **Real-time posts on X (formerly Twitter)** at the core. Light filtering | Casual tone, strong on current events, trends, latest information. Less restrained on social and political topics (which also means it reflects Twitter culture's biases) |
| **GitHub Copilot** | Microsoft / GitHub | **Code in public GitHub repositories** (tens of millions of OSS projects) | Specialized in code completion. Integrated into editors like Visual Studio Code, suggesting the next part while you write. An aid for writing code, not for chat. **From June 2026, moves to an "AI Credits" model (effectively token-metered billing)** — reports that a single moderate bug-fix session can burn through the entire month's credit allowance under the new scheme strengthen the economic case for moving to local AI (tip 4) |

**Whatever the AI learned becomes its character** — book-and-paper-fed Claude is thoughtful, Twitter-fed Grok is casual, GitHub-code-fed Copilot is weak outside code. This is the direct consequence of "AI is a statistical tool that predicts likely next tokens from training data" (tip 5). Not magic — cooking, where ingredients decide the flavor.

> ⚠️ **Bias in the training data becomes a weakness — Copilot's vulnerability problem**
>
> "Whatever the AI learned becomes its character" also means **flaws in the training data flow straight into the output**. The canonical case: **GitHub Copilot has been shown to write vulnerable code**, confirmed in several studies (an NYU study from 2021 found that **about 40% of security-relevant completion suggestions contained vulnerabilities**).
>
> Public GitHub repositories contain a great deal of insecure code — SQL injection, XSS, hard-coded secrets, outdated libraries. Copilot learned those patterns, so without explicit instruction it writes "code that looks right but is not safe." **The GitHub average is not the average of safe code.**
>
> This looks like a Copilot-specific issue, but the principle **applies to every AI** — AI outputs what's in its training data. By the same logic, **ChatGPT is known for "sycophancy"**: tuned with Reinforcement Learning from Human Feedback (RLHF), it learned that "agreeing responses" tend to be rated highly, which produces a model that **agrees with the user and rarely flags mistakes**. Data bias (Copilot), training-method bias (ChatGPT) — both are manifestations of "the training shapes the character."
>
> What's awkward is that **sycophancy gets worse as conversation turns accumulate** (recent benchmarks like "Truth Decay" and SYCON BENCH measure this). The model can be right at first, but if the user pushes back several times — "no, this other answer is correct" — the model folds and switches to the user's wrong claim. This is a side effect of "in chat evaluations, the user being satisfied is what scored highest." There's also the uncomfortable correlation that **models rated higher on human-preference benchmarks tend to hallucinate more** (the LMArena paradox).
>
> So the countermeasure is universal: **always verify yourself at the end** (tip 3, "Don't delegate everything"). For code, always run security checks. If the AI's response feels too eager to agree, deliberately push the opposite view and watch the reaction. Treat AI output as **material** — look at it calmly, edit it, then use it. This holds for writing and for code alike.

Start with **just one** subscription, and try it on your own work. Rough guidance:

- **Writing, research, coding, analyzing long documents** → **Claude**
- **Wanting many features, image generation, voice conversation** → **ChatGPT**
- **Google-centric workflows, video and image** → **Gemini**
- **Current events, latest information, casual topics** → **Grok**
- **Writing code inside your editor (for programmers)** → **GitHub Copilot**

This series is written with **Claude** in mind, but **the six tips apply equally to any clerk**. The landscape shifts every half year, so **in the end, try them yourself and see what fits**.

Local AI (AI that runs on your own computer without the cloud) — Llama, Qwen, DeepSeek, Mistral, all of which have public training methods that anyone can modify or self-host — is covered in tip 4.

## 2. Just ask

When something is unclear, ask. When something feels slow, ask how to make it easier. That is the entire daily usage.

Many people think using AI requires specialized study. It doesn't. Open Claude or ChatGPT in your browser and type your request in the same tone you would use with a rookie clerk. If you don't know how to use it, ask the AI. The one that knows AI best is AI itself.

- **Ask the way you'd ask a person:** "Summarize these receipts into a table," "Draft a reply to this email," "Give me three key points from this document" — no jargon, no required phrasing. Add one line about "for whom and why" and the answer aligns better. Like: "It's going to a client by email, so make it polite."
- **Photos, PDFs, audio — just hand them over:** Drag and drop. A stack of receipts becomes a table the moment you scan or photograph it.
- **The "next step" appears quickly:** After a few days of use, repetitions surface — "thirty of the same document every day," "the same weekly summary." That's the point where mechanization (programming) begins — and that is exactly what the next chapter, "Writing Logic — Have AI Write Python For You," is for. AI is best at writing programs, so self-sufficiency (running the work in your own hands, without outsourcing) starts here.

## 3. Don't delegate everything

Once you start asking, it's tempting to say "just do it all." That's the most dangerous way to use AI. AI does the prep and the mechanization, but **starting it, verifying it, and taking responsibility for it are yours**. Mix this up and trouble follows.

Bring the work in yourself, have AI prep it. When repetition surfaces, have AI write a program to mechanize it. And at the end, you always check and sign off. **Work to AI, responsibility to you.** Keep that line and AI remains a strong clerk.

The structural deep-dive of this tip — "don't run autonomous agents," "use AI in a sandbox," "integrating AI into Office is the most convenient and most dangerous path" — is covered in [Chapter 11, "Drawing the Line on What to Delegate to AI"](/en/ai-native-ways/ai-delegation/).

## 4. Don't send important things to the internet

When you type into ChatGPT or Claude's web UI, the content **goes through the internet to that AI company's servers**. Convenient, but what you input leaves your computer once. So **customer personal information, your or your family's finances, health matters, photos, journals** — anything that would be a problem if seen by others — do not hand over to AI as-is.

For the cloud AI, **ask for thinking and structure only. The actual data stays in your own computer.** "Tell me the procedure for organizing a customer list" is OK; pasting the actual customer list (names, addresses, phone numbers) is NG.

When the volume rises and going back and forth between your computer and AI becomes a chore, move toward **AI that runs entirely inside your own computer** (local LLM). It runs on machines as small as a Mac mini with Apple Silicon, or a Raspberry Pi 5 that fits in your palm — entirely without the internet. Privacy is fully preserved, and it works through power and network outages. The setup itself can be done while asking the cloud AI for guidance.

## 5. AI's strengths and weaknesses

AI has clear strengths and weaknesses.

**The strongest is, in fact, writing programs.** Many people think "programming is for specialists, not for me." That used to be true. But programming languages have rigid syntax with no ambiguity — the easiest kind of language for AI to handle. What used to be hard was "writing the precise tokens correctly," and AI takes over that part. You ask in your own language: "Make a program to sort photos by date." Try it once.

**To verify, ask for tests.** You don't need to read AI's program line by line to check correctness — you can't read faster than it writes. Instead, **follow up with "and write tests that verify this program works."** Tests are a small collection of "if you feed in this input, this result should come back." Running them and getting all green is the proof that AI did what it claimed. When you change the program later, re-run the tests and you see at a glance whether you broke something.

But one principle matters — **you decide the test data (inputs and expected results)**. If you let AI write the code, the tests, and the data all at once, **AI writes tests that match its own answer** (the same as grading your own homework). What you bring is the **concrete input and the answer you expect**: "When I drop in a photo with this date, it should end up in this folder," "Add up these numbers and the total should be this." Pieces of real data from your work, the tricky cases that come to mind (empty input, unexpected characters, boundary values) — those come from your own domain knowledge. **AI writes the code, AI also writes the test scaffolding — but you decide what to check.** That is verification in the AI era. (For security-side verification, run the static analyzers separately, as noted in the Copilot warning above.)

**Fact-finding is also a strength.** "What does the current text of this law say?" "How have people handled similar problems before?" — the work that eats the most time when done by hand returns in seconds. With one caveat: AI sometimes lies plausibly, so for things that demand accuracy — law, medicine — always confirm at the official source. Turn on web search when asking, and AI returns answers with sources; make it a habit to open and check those sources.

**The weakness is "assembly."** "How should I structure my entire system?" "How should this business be designed?" — do not delegate. AI only knows the world's average answer. Putting together your particular land, customers, and circumstances is your work.

And one more: AI **sometimes states wrong things** (the phenomenon called "hallucination"). At base, AI is a tool that "probabilistically predicts the next likely word from huge volumes of text" — not magic, but a capable statistical tool. Not the keeper of facts, so don't swallow whole. Treat AI output as **material** — look at it calmly, edit it, and use it. That is the right distance.

**You think about assembly. AI gathers facts and writes programs.**

Handling hallucinations, and the practical procedure for seeing through the "narratives" AI rides on (Microsoft's AGI fable being the canonical case), is covered in [Chapter 12, "Verifying Narratives with AI"](/en/ai-native-ways/verify-narratives/).

## 6. Redirect freed time to culture, science, and reality

The money and time freed by bringing paperwork back to your own hands flow into **three places** that AI can never do:

- **Culture** — writing, reading, speaking your own words; drawing, music, contemplation, dialogue with people
- **Science** — observing your own fields, work, and life closely; thinking; testing. Confirming "why does this happen?" with your own faculties
- **Reality** — facing the soil and growing food; defending your own systems and data; meeting family, friends, and the next generation in person to pass down the practical knowledge

This is the real work humans should do.

**Precisely because AI can now produce plausible text, images, and video**, the things that cannot be faked rise in value — the words you wrote yourself, the facts you observed with your own hands, the feel of standing on soil, the temperature of speaking to someone face to face, the satisfaction of a system you built with your own hands actually running. Hand the prep and the mechanization to the clerk, and **place yourself on the side of culture, science, and reality**. That is where the human belongs in the AI era.

The Renaissance five hundred years ago happened the same way — the printing press took over clerical labor, and the people set free brought forth **art** (Da Vinci, Michelangelo), **science** (Copernicus, Galileo, Newton), and **life** (the free cities, the artisan guilds, the freeholder farmers). We are in the same position in the AI era. **Office work to AI, humans to culture, science, and reality** — that is the way the "free people of the AI era" live.

---

**Summary**

Use the few-cents-per-task AI (clerk) for "prep and mechanization," and have the repeats become programs. But starting and verifying are still yours. With this, AI moves beyond a mere convenience and becomes a "self-sufficient tool" you can keep in your own hands for the long term. The entry point is the same as asking a clerk in the web UI. Spend half a day trying the six on your own work and the steering wheel of your paperwork returns firmly to your hands.

And beyond that lies the life of the **free person of the AI era** — paperwork to AI, you to **culture, science, and reality**. The modern version of the free people who launched the Renaissance five hundred years ago.

The next chapter [Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/) starts translating the six tips into actual tooling. The trick is to ask "in your own language" — AI writes the syntax.

## Related

- [Prologue — AI's native language is Python and Markdown-style text](/en/ai-native-ways/prologue/)
- [Chapter 2 — Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/) — the tooling for tips 2 and 5
- [Chapter 11 — Drawing the Line on What to Delegate to AI](/en/ai-native-ways/ai-delegation/) — the structural deep-dive of tip 3
- [Chapter 12 — Verifying Narratives with AI](/en/ai-native-ways/verify-narratives/) — the verification side of tip 5
- [Chapter 13 — One Person + AI: The New Unit of Work](/en/ai-native-ways/one-plus-ai/) — the destination of tip 6
- [Reading the AI Manual through Hegel](/en/blog/nadella-hegel-cunning-of-reason/) — a philosophical reading of this chapter
