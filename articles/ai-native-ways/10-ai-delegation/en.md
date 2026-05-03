---
slug: ai-delegation
number: "10"
lang: en
title: "Knowing What Work to Hand to AI"
subtitle: "What to delegate, what to keep"
description: There is a line between work AI can take and work humans must keep. AI is good at clear inputs and outputs, repetition, and transformation. AI is bad at the responsibility of judgment, the weight of context, and first-time design. Mistake the line, and convenience turns into dependency.
date: 2026.05.02
label: AI Native 10
title_html: Separate the work to delegate from<br>the work <span class="accent">humans must keep</span>.
prev_slug: embedded
prev_title: "Building Embedded — Think in Python, Have Claude Translate"
next_slug: one-plus-ai
next_title: "One Person + AI — The New Unit of Work"
---

# Knowing What Work to Hand to AI

AI cannot do everything.

There is a line between work you can give to AI and work humans must keep. Mistake the line, and convenience turns into dependency. People make wrong decisions because "AI said so." Organizations use "the number AI produced" without verifying, and no one can take responsibility.

This chapter is about that line.

## What AI is good at

AI is good at work where **inputs and outputs are clear, repetition is possible, and transformation is the core**.

Specifically:

- Converting Word to Markdown
- Converting CSV to JSON
- Translating English to Japanese
- Summarizing long text
- Cleaning up meeting notes
- Translating code from one language to another
- Bulk-renaming files
- Extracting information from many files
- Producing known solutions to known problems
- Generating implementation code from a spec
- Classifying, grouping, sorting data

These are tasks where "the right answer is mostly defined" and "the method is standardized." **Hand them to AI, and it does them faster and more accurately than a human.**

It is wasteful for humans to spend time here. Hand them to AI.

## What AI is bad at

AI is bad at work where **responsibility for judgment is borne, the weight of context is heavy, or the design is first of its kind**.

Specifically:

- The final call on "should this drug be prescribed for this patient"
- The final call on "should this candidate be hired"
- The final call on "should this investment be made"
- Strategic decisions about what to build
- Setting organizational direction
- Adjusting human relationships, reading emotional nuance
- Resolving ethically difficult problems
- The first design of a problem with no precedent
- Drawing out a customer's true needs through dialogue
- Hard negotiations

These are tasks where "the right answer is not defined," "responsibility is attached," or "context runs deep." **Let AI decide, and it may look surface-correct while missing the essence.**

This is where humans should spend time. Don't delegate it to AI.

## Criteria for the line

When unsure, ask the following.

**One: who is responsible for the output?**

There is no work where responsibility lies with AI. A human always carries it. So the heavier the responsibility, the less you should use AI's output as is. AI is the draft; the human finalizes.

**Two: can the result be verified later?**

If a human can verify with a formula what AI produced, you can delegate. If you cannot (too vast, outside expertise, intuitive), you cannot delegate.

**Three: how big is the damage if it fails?**

Small damage (a little wasted time), feel free to delegate. Large damage (customer trust, lives, property), use AI but the final call is human.

**Four: is the same task repeated many times?**

Repeated → delegate (target for automation). One-time, first-time judgment → human.

## "Convenience" vs "dependency"

Using AI as a convenient tool and depending on AI are different things.

Convenience: you could think it through yourself, but it is faster to ask AI. You read the output, fix it if needed. Judgment stays with you.

Dependency: you cannot think it through yourself, you cannot verify AI's output, you cannot notice when AI is wrong. Judgment has migrated to AI.

The dependency state is dangerous. When AI is wrong, the whole organization fails to notice. **"AI said so" becomes the reason for stopping thought.**

> Use AI, but do not lean on AI.

That is the principle.

## Example: editing prose

Example: have AI edit a long piece of writing you produced.

This is work AI is good at. Typos, grammar errors, expression improvements — AI finds them faster and more accurately.

But the final "this is good" is decided by a human. If AI suggests "this should be changed," and that contradicts your intent, you don't take it. **Whether to accept AI's suggestion is your decision.**

This is the concrete picture of "use AI, do not depend." Without AI, it would have taken longer. Leaving it entirely to AI, the writing is no longer yours. **Find the middle.**

## Example: a job interview

Example: a candidate interview.

Have AI organize the materials submitted in advance (good). Have AI build a list of questions (good). Have AI summarize the meeting transcript (good).

But the interview itself is done by a human. **Look the candidate in the eye, listen to word choice, feel the pauses.** That does not transmit to AI.

The hiring decision is also human. You can ask AI "what do you think?" but the final decision is human. **The one who can carry responsibility decides.**

## Example: medical diagnosis

Example: thinking through a diagnosis from a patient's symptoms.

Past case patterns, abnormal lab values, known drug side effects — having AI search and organize these is useful (good). AI flagging a differential the doctor might have missed is also useful.

But diagnosis and treatment plan are decided by the doctor. AI's candidates are treated as "list to consider." **The doctor is in front of the patient; responsibility lies with the doctor.**

If a doctor passes AI's output verbatim to the patient and starts treatment, that is dependency. A dangerous state.

## Personal lines too

This isn't just about organizations. Individuals also need lines.

- Don't let AI decide your life choices (career, marriage, moving)
- Don't let AI replace the essential parts of your creation (writing, art, music)
- Don't let AI set your child's education direction
- Don't replace relationships with friends and family with AI

AI is convenient, so you'll be tempted to delegate even these. But these are things **you carry responsibility for**. AI can advise. You decide.

## Organizational lines too

Organizations should draw lines explicitly.

"Don't treat AI output as a primary source" — make it a rule. Numbers and facts AI produces must be verified by humans against primary sources (originals, original data, expert opinion) before use.

"Keep the history of AI questions" — what was asked, what was returned, how the decision was made. Keep this, and audits become possible later.

"Require review of AI output" — for important decisions, another human reviews AI's output.

Without these, organizations slip into silent dependency on AI. Before they notice, they become organizations where no one can decide.

## In summary

Separate the work to delegate from the work humans must keep.

AI is good at "transformations with clear inputs/outputs and repetition." AI is bad at "responsibility, context, first-time design." Be conscious of the line.

Using as convenience is different from depending. Keep using as convenience. Be careful not to depend. This is, of all the practices in AI-native work, the most important practice.

The next chapter — the final chapter — synthesizes everything into "one person + AI as the new unit of work."

---

## Related

- [Chapter 09: Building Embedded — Think in Python, Have Claude Translate](/en/ai-native-ways/embedded/)
- [Chapter 04: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Structural Analysis 12: AI and the Individual Business](/en/insights/ai-and-individual/)
- [Structural Analysis 15: Security Design for the Mythos Era](/en/insights/security-design/)
