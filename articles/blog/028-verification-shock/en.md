---
slug: verification-shock
title: "When Fable 5 Returns, Do This First — Verify Every System You Run"
subtitle: "An AI that can attack can design and verify too — and the SIer and Microsoft, both built on never being verified, break by the same logic"
date: 2026.06.28
description: In June 2026, Axios reported the Trump administration moving to restore access to Fable 5. During the halt, companies switched to Chinese models, so the administration cannot keep it shut. The day Fable 5 returns, a company should do one thing — run every system it operates through Fable to verify it. An AI that can attack can also design and verify. And whatever was optimized on the premise of never being verified — the SIer's deliverables, Microsoft's vast opaque products (Entra ID CVE-2025-55241, EchoLeak) — is exposed whole the moment verification becomes free.
lang: en
label: Blog
category: Structural Analysis Notes
---

# When Fable 5 Returns, Do This First

On June 27, 2026, Axios reported that the Trump administration was moving to restore access to Anthropic's top model, Fable 5, and that the 15-day halt could lift "as soon as next week." That same week, the Commerce Department restarted the company's strongest cybersecurity model, Mythos 5, for a limited set of trusted organizations.

When and how Fable 5 resumes is not yet confirmed. But that it resumes in the near future is certain. During the halt, companies began switching to Chinese models. Once that switch is underway, the administration cannot keep the halt in place.

So when Fable 5 returns, what should a company do? This piece has one conclusion. On the day it returns, run every system you operate through Fable 5 and verify it. Why this is the highest priority, urgent, and unavoidable — let me take it in order.

## To be able to attack is to be able to design and verify

The one to watch is Mythos. Mythos became capable of cyberattack. What does that mean? To attack is to understand a system's structure more deeply than its own designer, find the weak point, and strike it. The power to understand structure that deeply is, as such, the power to design and the power to verify. That it became able to attack means it became able to design and verify. Attack, design, and verification are not separate capabilities. They are three faces of one power — "understanding structure deeply."

## What to do now — cyberattack defense with Fable 5

That an AI which can attack exists means the attacker can use it too. Cyberattacks from here on will have AI find and strike an organization's system flaws — automatically, in volume, at speed.

So the thing to do now is one thing. Run every system you operate through Fable 5 and verify it for vulnerabilities. Before the attacker's AI strikes, find the holes with your own AI and close them. Find them first, or get struck first — that is all it comes down to. Not next month, not next year's plan. Now.

This is not a matter of new business custom. It is emergency defense. Once the attacking side holds AI, old holes that were never found can be struck tomorrow. The more a system runs in production, the more it connects externally, the more it handles secrets — the sooner it must be verified.

## Who does it — the SIer, or yourself

So how does a company actually run this verification? There are only two roads. Have an SIer do it, or do it yourself.

### The problem with having an SIer do it

First, an SIer cannot design verification that withstands the attacking AI. The attacking AI's capability exceeds the SIer's defensive capability, and it keeps evolving. When you are attacked with a capability you do not possess, you cannot guarantee verification that holds against it.

Second, it cannot bear the responsibility. An attack at the Fable 5 level cannot be fully anticipated at contract time. Even if you commission "with countermeasures included," when a stronger AI breaks through, the SIer can only say "that was unforeseen." Responsibility for an evolving attack cannot be assumed by a contract fixed at one point in time.

Third, if the SIer verifies with Fable, the company may as well use Fable itself from the start. The reason to interpose an SIer disappears. The more efficiently the SIer verifies, the less point there is in interposing one.

Here the SIer can only say: "We'll check with Fable too, and fix with Fable." But this is self-negation. If both verification and fixing are done by Fable, the company can use that same Fable directly. What the SIer does becomes exactly what the company can do itself. The SIer's work reduces to issuing instructions to Fable and receiving the output — and there is no reason to pay an outside party for that. The moment it says it will use Fable, the SIer admits it is unnecessary.

Even before that, it does not work economically. If the company verifies with Fable, the holes in the SIer's deliverables get pointed out endlessly, at near-zero cost. The SIer answers those findings and fixes them. With Fable, that work itself is easy. But that is not where the problem lies.

If you verify and fix efficiently with Fable, that work no longer generates much revenue. The person-months once stacked up are compressed by Fable. The work goes around, but it does not earn. And on thin revenue, a large organization carrying multi-tier subcontractors cannot be sustained.

This is the SIer's real problem. It is not that they go bankrupt in the red. It is that large revenue no longer stands up, and an organization of that scale can no longer be supported. The more they use Fable, the more efficiency rises but revenue thins. Being large stops working.

And multi-tier subcontracting becomes unnecessary. What made it work until now was that coding and testing needed large amounts of manpower. The prime receives, passes to subcontractors, who pass further down. Each layer took a margin by supplying manpower. If Fable handles both implementation and verification, that mass of manpower is no longer needed. The very work to be passed down disappears. Multi-tier subcontracting stood on the scarcity of manpower. Fable erases that scarcity.

### The problem with doing it yourself

The problem with doing it yourself is just one: whether you have, in-house, people who can verify using Fable.

That barrier, though, is lower than it looks. What verification needs is not the power to write large amounts of code. It is the power to run your own systems through Fable, read the findings that come back, and judge which are truly dangerous. And the people who best understand what your systems do are the staff already inside. As long as they become able to use Fable, the verification can be done.

The question is whether you can secure those people right now. Since this is emergency defense, there is no time to grow them at leisure. But since you cannot rely on an outside SIer, you have to run the first verification while, at the same time, growing people who can use it in-house.

## Can the SIer withstand this verification?

So far the question was who verifies. But there is a more fundamental question. Can what the SIer delivered in the past withstand this verification at all?

Until now, SIers developed on the premise of not being verified. The commissioning side had no means to verify the delivered code. They could not read it, and even if they could, they could not evaluate its quality. So "appearing to work" was the only standard for passing. However complex the interior, however fragile, as long as it was not verified, it never surfaced.

If not being verified is the premise, there is no need to withstand verification. So you could cut corners in the unseen parts. In the vague parts of the spec, the parts where quality could not be measured, the parts unlikely to become a problem later, you could save cost. That was also the hidden margin of the person-month business.

Fable overturns that premise at the root. Code built on the premise of not being verified is now verified. The parts no one ever looked at are all seen. What was not built to withstand is required to withstand.

This is not a story of SIers suddenly cutting corners. It is that the result of optimizing under the long-standing premise of not being verified is exposed whole the instant that premise disappears.

## The same blow comes for Microsoft

This blow is not the SIer's alone. The same logic applies, intact, to Microsoft.

Microsoft's products are vast, interdependent, and keep carrying old structures for the sake of backward compatibility. The interior is now so complex that no one grasps the whole. And users had no means to verify that interior. They could only trust and use what runs on the far side of the cloud. Here too, not being verified was the premise.

In fact, in Microsoft 365 Copilot, vulnerabilities that leak confidential information with zero clicks (EchoLeak, SearchLeak, and others) were reported one after another across 2025–2026. In an age when the attacking side searches for system flaws with AI, a vast, complex product carries that many more holes. Complexity is the breadth of the attack surface.

The most symbolic is the vulnerability in the authentication foundation Entra ID, CVE-2025-55241 (disclosed September 2025, CVSS score 10.0, rated Critical). Per reporting, this was a flaw by which an attacker, using a token generated in their own tenant, could impersonate a global administrator in nearly every Entra ID tenant in the world. It bypassed MFA and conditional access, and left almost no logs. And its cause was that the legacy Azure AD Graph API failed to properly validate the token's issuing tenant — that is, an old component left in place for backward compatibility.

This embodies the thesis of this piece directly. A flaw in the authentication foundation — the deepest, most important part — lay hidden in old code left for backward compatibility. And it went unverified until it was found at global scale. In an age when the attacking side holds AI, such old holes are found faster and more surely than before. Microsoft has announced it will phase out Entra ID's legacy components — but that, too, is a step in the painful direction of abandoning backward compatibility.

Microsoft will say it finds and fixes holes with its own AI. But this enters the same dead end as the SIer. If both verification and fixing are done by AI, why would users use that AI while still bound to a vast, opaque product? If a verifying AI exists, it becomes more rational to hold a verifiable form yourself — a simple configuration whose interior is visible and which you can fix when it stops.

And for Microsoft to truly address its flaws, it has to abandon backward compatibility, the root of the complexity. But backward compatibility is the very weapon by which Microsoft has bound its customers. Abandon it and it becomes healthy, but it loses the power to bind. Becoming healthy and losing dominance become one and the same act. So it cannot abandon it. Unable to abandon it, it keeps being verified, its holes kept visible.

What has stood on the premise of not being verified is not only the SIer's deliverables. It is everything vast, complex, and opaque inside. Microsoft is one of the largest of them.

---

## Related

- Software sub-series [3-03 The Structural Uneconomy of the SIer Model](https://aiseed.dev/en/ai-native-ways/software/sier-uneconomic/) — commissioning breeds de-responsibilization and hollowing-out, the premise of this piece
- Software sub-series [3-04 The Lock-In Problem](https://aiseed.dev/en/ai-native-ways/software/lockin/) — backward compatibility as the "cage with no exit"
- Blog [The IT Industry's Structural Shift — Toward Autonomy, Distribution, and Diversity](https://aiseed.dev/en/blog/autonomy-distribution-diversity/) — the Fable 5 export ban and sovereign AI

## References

1. Trump administration moves to restore access to Anthropic's Fable 5 (Axios, 2026-06-27)
2. Statement on the US government directive (Anthropic) — https://www.anthropic.com/news/fable-mythos-access
3. Zero-Click AI Vulnerability Exposes Microsoft 365 Copilot Data (EchoLeak / CVE-2025-32711, The Hacker News) — https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html
4. One Token to rule them all — obtaining Global Admin in every Entra ID tenant via Actor tokens (dirkjanm.io / CVE-2025-55241) — https://dirkjanm.io/obtaining-global-admin-in-every-entra-id-tenant-with-actor-tokens/
5. Death by Token: Understanding CVE-2025-55241 (Practical 365) — https://practical365.com/death-by-token-understanding-cve-2025-55241/
