---
slug: software-three-transitions
title: "\"Become a specialized engineer\" misreads the structure"
subtitle: The Second Renaissance has begun — software engineer → builder, software engineering → liberal arts, employment → free person
date: 2026.05.21
description: "The widely circulated advice — \"in the AI era, become a specialized engineer; hold a deep specialty AI cannot take, like security or ML\" — misreads the structure. AI is absorbing the whole layer of software engineering, not a particular subdomain. The medieval analogue: telling a serf, \"become a more specialized serf and you will be free.\" Freedom comes from stepping out of the lord's structure of control, not from deeper specialization. Software engineer → builder, software engineering → liberal arts, employment → free person — these three transitions are unfolding inside the Second Renaissance (the historical turning point of the AI era, with the LLM playing the role of the printing press). Creation and upheaval are two faces of the same time, and Trump is the canonical figure on the upheaval side. The article compresses aiseed.dev's eleven-chapter \"AI-Native Ways of Working — Software\" sub-series into three pairs of words."
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3285.jpg
---

# "Become a specialized engineer" misreads the structure

There is a widely circulated piece of advice — "in the AI era, become a specialized engineer; hold a deep specialty AI cannot take, like security or ML."

This **misreads the structure**.

What AI is absorbing is **the whole layer** of software engineering, not a particular subdomain inside it. Going deeper into a specialty only shifts the date by which the specialty itself is overtaken. The medieval analogue would be telling a serf, "become a more specialized serf and you will be free." Freedom does not come from going deeper into the specialty; it comes from **stepping out of the lord's structure of control**.

The structural change argued in aiseed.dev's [AI-Native Ways of Working — Software](/en/ai-native-ways/software/) sub-series (eleven chapters) compresses into three transitions:

| Before | After |
|---|---|
| Software engineer | **Builder** |
| Software engineering | **Liberal arts** |
| Employment | **Free person** |

We look at why each one happens.

## Transition 1: Software engineer → builder

**The software engineer's work was writing code.** Specs come down, someone fluent in languages, frameworks, and patterns implements them. Adding people to the team raises writing speed; output scales as "head count × writing speed" — this has been the structure for the past thirty years.

**The builder's work is deciding what to build.** Concretely, four moves in a loop:

- **Decide** — from the customer, the field, your own context, judge what to build and how to divide it
- **Delegate** — hand AI the intent, constraints, acceptance criteria. AI writes the code
- **Evaluate** — judge whether the returned output runs, fits the design, and holds up in the intended context
- **Integrate** — fold the part into the whole, keep the whole consistent, return to the next "decide"

The loop turns dozens of times in a day. Code-writing time is minimized inside it — because AI is the one writing.

> An engineer's output is set by **head count × writing speed**.
> A builder's output is set by **judgment quality × loop turnover**.

In numbers: aiseed.dev's code base (about 6,000 lines — the build tool, templates, image generation, sitemap, and so on that carry five independent series and ~150 bilingual articles) was stood up by **one person + AI in 24 hours**. The same scope handed to an SIer would burn that much time on the proposal and quote alone.

"Add people and it goes faster" held in the engineer's world (with a ceiling). In the builder's world, **adding people does not make it faster** — the chain of judgment cannot be parallelized across heads.

See [Chapter 4: The Builder Role](/en/ai-native-ways/software/builder/).

## Transition 2: Software engineering → liberal arts

"What skills should a builder develop?" — the answer differs from what the industry expects.

What the builder cultivates is **structural decomposition, verbalization, evaluative eye, integration judgment, selection**. All of these have been called **the liberal arts** (the *artes liberales*, the "seven liberal arts") for two thousand years.

| What a builder needs | Its liberal-arts counterpart |
|---|---|
| Structural decomposition | Logic, analysis (the *trivium*'s dialectic) |
| Verbalization (turning implicit intent into explicit description) | Grammar, rhetoric (the *trivium*) |
| Evaluative eye (separating "merely runs" from "fits the design") | Aesthetics, ethics |
| Integration judgment (seeing whether parts preserve the whole) | Systems thinking (geometry and the constructive sense of music) |
| Selection (picking "this one" from three options) | Ethics, theory of judgment |
| Reading context (cutting it out of customer and field) | History, social science, political philosophy |

**What AI took over is the core of software engineering** — algorithms, language specifications, frameworks, design patterns, how to write tests. The work that remains looks liberal-arts–shaped because, structurally, **it has to**.

To be clear, **computer science (CS) is a different thing**. Computability, algorithms, formal logic, discrete mathematics sit inside the liberal arts as a modern extension of the *quadrivium*'s mathematics and logic. Historically CS emerged from mathematics; Turing, Church, and von Neumann were mathematicians and logicians. **CS does not need to be discarded, and it does not need a special category** — it is folded into the builder's scaffold for judgment.

The etymology lines up, too. The medieval *artes liberales* were defined as **the arts a free person — one who is not enslaved — should learn**, set explicitly against the *artes mechanicae*, the slave's arts. The builder is the person who **does not hand judgment over to AI** — the contemporary form of the free person's arts.

See [Chapter 4: The Builder Role — "A builder's foundation is liberal arts"](/en/ai-native-ways/software/builder/).

## Transition 3: Employment → free person

One more transition is easily missed. **Modern employment, examined structurally, sits in the same position as medieval serfdom.**

| Dimension | Medieval serf | Modern employee |
|---|---|---|
| Ownership of the means of production | Lord's land and tools | Employer's office, equipment, IP, data, infrastructure |
| Self-determination of labor | Cultivating at the lord's direction | Working at the supervisor's direction |
| Freedom of movement | Tied to the land | Tied by employment contract, mortgage, in-company career |
| Income predictability | Stable under the lord's protection | Trading freedom for salary stability |
| Locus of judgment | The lord | The employer |
| What is received in exchange | Food and protection | Salary and benefits |

This is not a claim of moral equivalence (modern employment has legal protections and contractual freedom). It is an analytical observation that **on the three axes of ownership, judgment, and mobility, the structure matches**.

And the reasons employment **stops fitting in the AI era** are structurally clear:

1. **The means of production are now individually ownable** — a few-thousand-yen-a-month AI, local LLMs, open source, one's own server. The employer no longer needs to monopolize them.
2. **One person + AI = a ten-person team** — the payoff of concentration disappears.
3. **The boundary between judgment and execution closes within one person** — the overhead of aggregation, coordination, and management becomes pure waste.
4. **Judgment-centered professions are intrinsically inclined to independence** — lawyers, doctors, accountants prefer solo practice and partnerships, not by accident.

**The rise of self-employment is structural necessity, not a policy or lifestyle question.** The same structure under which medieval free citizens, free farmers, and craftsmen were all "self-employed" returns in the AI era.

> Employment is the contemporary form of medieval serfdom.
> **Self-employment is the contemporary form of being a free person.**

See [Chapter 11: "Employment is the AI era's serfdom"](/en/ai-native-ways/software/five-years/).

## This is the Second Renaissance

Lay the three transitions out — engineer → builder, software engineering → liberal arts, employment → free person — and they line up, item by item, with the structural change of the First Renaissance (14th–17th centuries).

| Element | First Renaissance | Second Renaissance (AI era) |
|---|---|---|
| The polymath ideal | Leonardo da Vinci | The builder, one person + AI |
| The classics being recovered | Greek and Roman classical learning | The liberal arts |
| Vernacular liberation | Dante's Italian, Luther's German | Natural language becomes "the programming language" |
| Free cities and guilds | Florence, Venice, the craft guilds | The AI-era free person, professional guilds |
| **The accelerator** | **The printing press (1450s) — democratized reading** | **The LLM — democratizes making** |
| New rising class | The bourgeoisie | The AI-native builder, the self-employed judgment professional |

History textbooks credit the printing press with preparing the ground for the Reformation, the scientific revolution, and the modern nation-state **over two hundred years**. The LLM holds **incomparably greater intensity** — what the printing press democratized was "reading" (access to existing knowledge), while what the LLM democratizes is "**making**" (knowledge generation, judgment, implementation). There is no literacy wall to clear first; natural language works for anyone.

The speed of diffusion is on another order. What took the printing press decades, the AI era achieves **in years**. The five-year horizon this sub-series draws is, against this difference in intensity, **a conservative estimate**.

### The AI revolution is the completion of the IT revolution

Treating "the AI revolution" as a separate, new revolution is another misreading. **The AI revolution is the completion of the IT revolution** — seventy years of IT revolution finally fulfilling its original promise.

Think about it — the IT industry, until now, has had **humans hand-writing the code that automates work**. The IT revolution's original promise was "computers do the work, humans are freed." Yet for seventy years, **the side that implements the automation has been doing it by hand** — a strange structure. The consequences:

- "Programmer" became one of the highest-paid professions
- The cost of automation often exceeded the cost of doing the work manually
- A massive industry of "manual labor for automation" emerged — SIers, consultancies, SaaS

Logically, this is odd. **If automation is the goal, the work of making the automation should be automated too.**

The LLM dissolves this twist. AI writes the code — and only then is the IT revolution's original promise (humans freed from execution, turning to judgment and creation) literally fulfilled. **The AI revolution is not the beginning of a new revolution; it is the completion of the IT revolution.**

> For 70 years the IT revolution promised automation while implementing
> that automation by hand. That era ends. **With AI writing the
> automation code**, the IT revolution is, 70 years late, fulfilling
> its own promise.

That completion functions as the strongest accelerator of the Second Renaissance. Read through the frame of "IT revolution completion," the contraction of the SIer industry and the replacement of the software-engineer role by the builder are **inevitable consequences**, not sudden shocks.

### The LLM is a powerful statistical-processing tool, not a superintelligence

Looked at coolly, the LLM (Claude, GPT, Gemini, and the rest) is **large-scale statistical processing of data**. A mechanism that, given enormous text — textbooks, papers, the web — predicts the most probable next token in context. An overwhelmingly powerful tool, but it is not, in itself, becoming "superintelligence."

The pitch that "AGI is coming, white-collar work will be fully automated in 12–18 months" (Microsoft AI's CEO Suleyman and others) deliberately stages this nature as a **superintelligence parable**, in order to push "so hand judgment over to AI" and "so buy Copilot" (see [Microsoft's Nadella and Hegel's Philosophy](/en/blog/nadella-hegel-cunning-of-reason/)).

Handing "judgment and responsibility" to a statistical-processing tool is structurally wrong. The LLM makes **writing, looking up, organizing** orders of magnitude faster, but **deciding what to build, evaluating whether it is right, taking responsibility** stay on the human side. This is the logical basis of the role this article has been calling "the builder."

If the essence of the AI revolution is read as "the arrival of superintelligence," the picture goes hazy. Read it as "**a powerful statistical-processing tool finally made the IT revolution's automation promise implementable**," and the picture becomes clear. The contraction of the SIer industry, the rise of the builder, the foundational shift from software engineering to the liberal arts — all of these are explained by the simple structure "**the tool got strong, so the human role shifts to the judgment side**." Talk of an AGI arrival, or the anthropomorphization of superintelligence, only obscures the structure.

> The LLM is a powerful statistical-processing tool, not a superintelligence.
> **Judgment and responsibility stay with the human** — this is the
> logical ground beneath all three of this article's transitions.

### App-making comes to resemble film-making

"Software development as an independent process disappears — but apps do not disappear." The most precise analogy for this is **film-making**.

A film is made when many independent specialist roles converge — cinematography, editing, sound, lighting, costume, set design, VFX, scoring, acting. The audience is not aware of any of these. **Only one artifact — the film — appears.** At the center are not the people who handle each technical task but the **director and the screenwriter** — the carriers of creative judgment.

App-making in the AI era takes on the same structure.

| Film-making | App-making in the AI era |
|---|---|
| Director — overall vision and judgment | User / author / master builder — judging what to build |
| Script (manuscript) — written in natural language | Natural-language source — what, for whom, how it behaves |
| Cinematography, editing, sound, VFX — specialist crew | AI — picks up the engineering layer as a whole |
| Cast, set, costumes | AI-generated UI, logic, data structures |
| The film (artifact) | The app (artifact) |

**A director does not learn how to operate the camera. A screenwriter does not learn lighting. The audience does not know how the film was made.** Even so, the film exists and carries value.

Apps will take the same shape — **the user / author does not learn engineering. AI picks up the engineering work. The end user does not know how it was made.** Apps still exist.

The independent role of "software engineer" shrinks in the same way that "a staff cinematographer on permanent payroll" no longer fits an independent filmmaker. But **directors remain, screenwriters remain, films remain** — and equivalently, **builders (the people who write the source, who judge) remain, the natural-language manuscript remains, the app remains**.

Just as the printing press eliminated the scribe but not the book, the LLM shrinks the software engineer but not the app. **Only the way of making changes** — and the new way is closer to making a film than to printing a book.

> Engineering-as-craft for software disappears; apps do not.
> **App-making comes to resemble film-making, not book-printing** —
> creative judgment at the center, with the technical crew (= AI)
> gathered around it.

#### Both Hollywood blockbusters and YouTube videos hold

Film-making, however, has an enormous range. **A Hollywood blockbuster still requires massive crews, hundreds of millions of dollars, and years of work**. A **YouTube video can be made by one person with a smartphone in a few hours**. Both extremes coexist inside the single category of "video content."

AI-era apps will have the same range.

| Scale | Video production | AI-era app-making |
|---|---|---|
| **Blockbuster** | Hollywood film — director + huge crew + hundreds of millions + years | OS, large infrastructure, core business systems — master builder + heavy AI output + sustained development |
| **Mid-scale** | Television drama, documentary, theatrical film | Industry-wide systems, SaaS, specialized apps — 1–few builders + AI |
| **Personal** | YouTube, TikTok — one person + phone + a few hours | Everyday personal tools — the user + natural-language instruction + a few hours |

**Blockbusters need master builders (= directors)**. Not everyone can shoot a Hollywood film; not everyone can build an OS or a core business system. The quality of judgment, the maintenance of integrity, long-term stewardship, safety — these stay the domain of highly skilled professionals (this is where the lawyer/doctor analogy of Chapter 9 applies).

**But YouTube-scale apps need no specialist**. The user is both director and crew. "A small tool that makes my work easier," "a household budget app," "a shared calendar for the family" — these become things anyone can produce with natural-language instructions.

The shrinkage of the "software engineer" role therefore plays out differently at the two ends:
- **Blockbuster side**: consolidation toward master builders. Whether most engineers can graduate into the judgment side is the dividing line.
- **Personal side**: the specialist disappears entirely. The user becomes the author of their app directly.

The middle — **industry-wide systems and SaaS** — is where the contraction is most violent, because this is exactly the territory the SIer industry has occupied (the structure handled in Chapters 6 and 7).

This follows naturally from concepts 11 (IT revolution completion) and 12 (LLM as tool). The 70-year-delayed completion of the IT revolution takes the form of a shift from "humans handle the technology" to "humans focus on judgment and the manuscript; AI handles the technology" — that is, **software development moves closer to film-making**. And that "film-making" holds across **the full range, from Hollywood to YouTube**.

### Not only the AI revolution

We have been calling this "the AI era," but trying to capture the current structural change through AI alone **misses half of it**. The transitions running in parallel:

- **The end of fossil resources** — collapse of the premises of an oil-dependent society ([Structural Analysis 02](/en/insights/fossil-materials/), [14](/en/insights/subtraction-design/))
- **Geopolitical multipolarity** — the end of US unipolarity, Trump, Ukraine, Iran, China
- **A generational shift in the defense industry** — from large platforms to drones + AI; the boundary of "who can have a defense industry" gets rewritten ([Structural Analysis 11](/en/insights/healthcare-fiscal/))
- **The reconstruction of agriculture** — limits of chemical fertilizer and industrial-scale farming; rise of regenerative agriculture ([Structural Analysis 03](/en/insights/agriculture/))
- **The collapse of the premises of finance and trade** — the dollar standard, the global supply chain
- **Simultaneous breakdown of demographics, cities, healthcare, and pensions** — institutions premised on desk work no longer fit the new society ([Structural Analysis 11](/en/insights/healthcare-fiscal/))
- And the **AI revolution** — the **accelerator** for all of the above

Just as the First Renaissance must be understood as a **composite** of the printing press, the age of discovery, the Reformation, the scientific revolution, the rise of the nation-state, the rise of the commercial bourgeoisie, and the labor shifts after the Black Death, the Second Renaissance cannot be captured by **the AI revolution alone**.

Multiple independent transitions are running in parallel; their convergence point is what makes "an era that is no longer the same." AI is the strongest accelerator among them, but it is not the cause of all of them.

> Calling this "the AI revolution era" sees the present too narrowly.
> Unless you frame it as **the Second Renaissance** — a transitional period
> in which multiple independent transitions unfold at once — you see only
> half of what is happening.

### An age of creation, and an age of upheaval

The Renaissance is in the textbooks as a luminous age of creation — Leonardo, Michelangelo, Galileo, Gutenberg. The same age was also an **age of violent upheaval**. The Reformation and the wars of religion (the Thirty Years' War cut Central Europe's population by roughly a third), the corruption and schism of the papacy, recurring plague, *populist demagogues* like Savonarola staging the "bonfire of the vanities" in Florence, strongman politicians like Cesare Borgia who became Machiavelli's model in *The Prince*. **While the old order is collapsing and the new one has not yet stood up, people seek refuge in strong men and extreme words.**

The upheaval side of the Second Renaissance is already unfolding in front of us. **President Trump** is the canonical figure on that side:

- Direct attack on the expert class, on the judiciary, on the scientific consensus
- Ad-hoc swings on tariffs, immigration, science budgets, federal staffing
- Streams of executive orders that override congressional checks
- A style of governance built on "I decide everything, alone"

Placed next to Nadella's Copilot strategy, the structure becomes visible. Nadella moves to "**concentrate corporate judgment into a single AI (Copilot)**"; Trump moves to "**concentrate national judgment into a single president**." The means differ, but both **push the old era's logic of judgment-concentration to its absolute limit** (see [Microsoft's Nadella and Hegel's Philosophy](/en/blog/nadella-hegel-cunning-of-reason/)).

Just as the Renaissance-era *populist demagogues* in the end disappeared, the figures pushing judgment-concentration to the extreme will not fit the structure of the new era (distribution, the free person, judgment held by the individual) and will exit. But the interim is turbulent — this too is the same pattern as the First Renaissance.

> The Renaissance is an age of creation and an age of upheaval at the same time.
> Looking only at the creation side — the builder, the liberal arts, the free person —
> is to misread the era. The upheaval side — Trump, Nadella, the runaway
> concentration of judgment — is also a symptom of the same transition.
> Both sides have to be read together.

## The alternative path to "specialized engineer" advice

Back to the opening question. "How do you move in the AI era?" — the answer is not deeper specialization. It is **stepping sideways**.

There are two paths:

1. **Sideways onto the liberal-arts axis** — sharpen judgment, verbalization, ethics, systems thinking. Become a builder.
2. **Sideways into builders who hold physical reality** — makers, embedded engineers, robotics, precision agriculture, carpenters using AI design tools. The middle layer that bridges pure software's abstraction with pure physical work's directness.

Both are roads out of the lord's manor.

## More in the Software sub-series

This article compresses aiseed.dev's **[AI-Native Ways of Working — Software](/en/ai-native-ways/software/)** sub-series (eleven chapters) into three pairs of words. The arguments across the chapters:

- [Chapter 1: AI Solves the World's Hardest Coding Problems](/en/ai-native-ways/software/coder-top/) — Codeforces 2700 tier; the top layer for $200/month
- [Chapter 2: The Real Shift Is in Maintenance](/en/ai-native-ways/software/maintenance-shift/) — the unit of maintenance moves from code to design
- [Chapter 3: The Coder's Job Goes Away](/en/ai-native-ways/software/coder-end/) — same structure as abacus → calculator
- [Chapter 4: The Builder Role](/en/ai-native-ways/software/builder/) — decide, delegate, evaluate, integrate
- [Chapter 5: Customers Co-develop with AI](/en/ai-native-ways/software/customer-codev/) — 90% is the customer; 10% goes to a specialist
- [Chapter 6: The SIer Commission Model Is Structurally Uneconomic](/en/ai-native-ways/software/sier-uneconomic/)
- [Chapter 7: An Order-of-Magnitude Price Gap](/en/ai-native-ways/software/price-gap/) — 10×–100× is market displacement, not competition
- [Chapter 8: The Lock-In Problem](/en/ai-native-ways/software/lockin/) — Palantir FDE as the canonical case
- [Chapter 9: The Master Builder Is a Profession That Sells Judgment](/en/ai-native-ways/software/hiring-builders/) — same position as lawyers and doctors
- [Chapter 10: Japan's SIer Industry Transition](/en/ai-native-ways/software/japan-transition/) — multi-tier subcontracting paradoxically eases the transition
- [Chapter 11: The Transition Completes in a Few Years](/en/ai-native-ways/software/five-years/) — irreversibility; the Second Renaissance

"**From software engineering to the liberal arts — the foundational shift of the technical profession**" is the subtitle of the sub-series and one axis for reading the structure of the AI era.

---

## Related

- [AI-Native Ways of Working — Prologue](/en/ai-native-ways/prologue/) — the contour of the AI-era free person
- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/) — the structural change on the company side
- [Structural Analysis 09: AI and the Individual Business](/en/insights/ai-and-individual/) — the structural change on the individual side
- [Microsoft's Nadella and Hegel's Philosophy](/en/blog/nadella-hegel-cunning-of-reason/) — the worldview on the opposite side
