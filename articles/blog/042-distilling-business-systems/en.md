---
slug: distilling-business-systems
title: "Distillation Is Not Only About AI — AI Builds the Business System"
subtitle: "If a cheap model can be built from an expensive one's inputs and outputs, the next system can be built from the current one's — what is copied is not the vendor's code but the behavior of your own business"
date: 2026.07.27
description: The word "distillation" is circulating around Kimi K3 — the technique of putting questions to an expensive model, collecting the answers, and using those input-output pairs to train a cheap model with the same behavior. The internals are not needed; the behavior is enough. The same structure applies directly to business systems, because a test is nothing but putting a question to a system and recording the answer. Once the behavior is in your hands, AI can build another implementation that does the same thing. What is copied is not the vendor's code but how your own business ought to behave — which was yours to begin with. Routine maintenance reduces to security auditing; improvement requires only a reason and test data, and most of the test data the model itself can generate. The reason for an improvement can only come from you, and AI writes the implementation. There is no longer any need to outsource: judgment stays with the company, and the work can be left to AI.
lang: en
label: Blog
category: Structural Analysis Notes
---

# Distillation Is Not Only About AI

## Conclusion

Around Kimi K3, whose weights are scheduled to publish today, the word **distillation** is circulating. It is the technique of putting questions to an expensive model, collecting the answers, and using those input-output pairs as a teacher to train a cheap model with the same behavior. **The internals are not needed. The behavior is enough.**

## Fact — What Distillation Is

Worth stating precisely.

Distillation is the technique of training a small model (the student) using the outputs of a large one (the teacher). It works without holding the teacher's internals — weights or training data — as long as you have **the pairs of inputs and outputs**. This form is called **black-box distillation**, and anyone who can call the API can perform it.

So distillation makes the inheritance of capability radically cheap. Building the teacher takes enormous trial and error; copying the teacher's answers costs only inference.

Around Kimi K3, the word has become a political matter. US administration officials accused Moonshot of large-scale unauthorized distillation of Anthropic's model outputs. In February, Anthropic named more than 3.4 million improper exchanges by Moonshot. Moonshot, for its part, says it caught up through architectural engineering. As this site wrote on 21 July, [which of the two stories is true will be settled by the weights, not by rhetoric](https://aiseed.dev/en/blog/kimi-k3-maker-side-zero-trust/).

## Distilling a Business System — A Test Is a Record of Behavior

Put it back into business systems.

Put questions to the system running today and record the answers that come back. That is a test. **Structurally, this is identical to black-box distillation.** The internals — the source code — are not needed. The behavior is enough.

Enter an order and this document is raised. Close the period and this balance appears. Under this condition, that approval is required. Write enough of it down and the behavior of the business is in your hands. And once the behavior is in your hands, **AI can build another implementation that does the same thing.**

This is not a thought experiment. On 16 July, Anthropic's engineering blog reported that Bun, a JavaScript runtime, was ported from Zig to Rust — **one million lines in under two weeks, with 100% of the existing test suite passing**. The watchword: "Let scripts — a compiler, a diff, a test suite — be the referee." Hand the judgment of correctness to the tests, and AI rebuilds the implementation. Distillation — copying the behavior and swapping the implementation — is already running at industrial scale.

Notice that the order has been inverted. For a long time, the correctness of a business was assumed to live in the code. But AI has made it possible to build the same working implementation from test data alone.

And what is being copied is not the vendor's work product. It is how your own business ought to behave, which was yours to begin with.

The practice of doing this one thread at a time without stopping the running system was covered in [With Fable's release, in-house development wins for business systems](https://aiseed.dev/en/blog/in-house-business-systems/). Using the current system as an "oracle" to check answers against is, in this piece's vocabulary, **using it as the teacher model**.

## Maintenance Splits Into Two Jobs

**Routine maintenance reduces to security auditing.** A system that runs is, as long as it runs, behaving to specification. What arises day to day comes from outside: vulnerabilities in dependencies, runtime and OS updates, the expiry of cryptographic methods, inspection of the ports exposed outward. The work is to update, run the tests, and fix what fails. With tests in place, that confirmation runs automatically. The only human judgment left is **"does this vulnerability apply to us?"**

**Improvement requires exactly two things.** The reason for the improvement, and test data. Write down what is being changed and why; show in data how it should behave afterwards. AI writes the implementation.

And here is what matters most in practice: **the test data, too, can usually be generated by the model.** Give it the specification and it enumerates boundary values, error paths, and combinations. What a human must supply narrows to what the model cannot know — **the quirks of your actual data, and the combinations that are impossible in your business**. The first can be extracted from the current system. The second can only be stated by someone who knows the business.

## There Is Nothing Left to Outsource

Line up the three and something becomes visible.

The reason for an improvement **can only come from you.** The test data is **generated by the model or taken from your own real data.** The implementation **is written by AI.** Nowhere in that list is there room for an outside company.

This is not accidental. **Outsourcing was a transaction that kept judgment in-house and pushed only the work outside.** For it to exist, there must be a middle layer of work that is neither judgment nor something anyone can do — work that requires expertise but not business judgment. Writing the program, drawing up test cases, building the environment. **Outsourcing existed only in that middle layer.**

What is happening now is that the middle is being shaved from both sides. Judgment moves toward the company; work moves toward AI. **Judgment cannot be sent out. Work does not need to be.** The width in between approaches zero.

## Related

- Blog [What Was Kimi K3 Made From — Zero Trust on the Maker's Side](https://aiseed.dev/en/blog/kimi-k3-maker-side-zero-trust/) — the two stories around the distillation dispute, and verification by the weights
- Blog [With Fable's Release, In-House Development Wins for Business Systems](https://aiseed.dev/en/blog/in-house-business-systems/) — the practice of rebuilding with the current system as oracle
- Blog [You Can Build an App Through Dialogue Alone](https://aiseed.dev/en/blog/building-apps-through-dialogue/) — the articulation side
- Blog [The Person the AI Era Needs — When Software Gets Cheap, So Does Attack](https://aiseed.dev/en/blog/three-conditions-ai-era/) — how the basis of the maintenance fee disappears
- Blog [The Open-Weight Dilemma](https://aiseed.dev/en/blog/open-weights-dilemma/) — the industry-scale version of the same structure: exposing behavior invites copying
- Blog [Reading July 2026 Through Hegel](https://aiseed.dev/en/blog/hegel-july-2026/) — the general form of "to sell you must expose, and to expose is to be transcribed"

## References

1. Axios: China's open-weight Kimi model stuns AI world with frontier-level results — https://www.axios.com/2026/07/16/moonshot-kimi-ai-china-model-openai-anthropic
2. Hugging Face: moonshotai/Kimi-K3 — https://huggingface.co/moonshotai/Kimi-K3
3. Anthropic: AI code migration — https://claude.com/blog/ai-code-migration
