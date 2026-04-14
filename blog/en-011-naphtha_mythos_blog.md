# Two Bombs Hitting America at Once: Naphtha and Mythos

In April 2026, America is holding two bombs simultaneously. One: the raw materials for medical supplies, semiconductors, and jet fuel have stopped arriving due to the Strait of Hormuz blockade. Two: AI can now find security vulnerabilities that went undetected for decades and automatically generate attack code in hours. These two appear unrelated. They are connected at the root.

## Oil is finite. Energy obeys the laws of physics. Computing depends on electricity.

These three facts explain everything that is happening now.

## The Hidden Dependency Called Naphtha

The Strait of Hormuz has been effectively blocked since late February. Before the blockade, approximately 135 vessels transited daily. Now it's down to about 8. Most people understand this as "rising oil prices." Brent crude broke through $120 per barrel by mid-March. But the real problem isn't price — it's the physical depletion of materials.

Naphtha is a light petroleum distillate obtained from crude oil refining. It is the feedstock from which ethylene, propylene, and benzene are produced. These are the starting point for virtually every modern product — food packaging, medical devices, semiconductors, clothing, automotive parts.

The range of products dependent on naphtha is far broader than most people realize.

The United States is the world's largest oil producer, but that alone isn't enough. American shale gas-derived ethane crackers are suitable for producing commodity polyethylene, but they cannot manufacture the high-grade medical polymers or ultra-pure chemicals required for semiconductor fabrication. The supply chains for these specialty materials are concentrated in East Asian (South Korea, Taiwan, Japan) petrochemical complexes that depend on Middle Eastern naphtha. Even with domestic crude production, America cannot produce the necessary chemicals on its own.

### Semiconductors Can't Be Made with American Naphtha

Photoresists — the light-sensitive resins essential for patterning semiconductor circuits — are manufactured from naphtha-derived aromatic compounds. Ultra-high-purity solvents used in wafer cleaning are also naphtha-based. South Korea's Ministry of Trade, Industry and Energy has identified 14 semiconductor supply chain items severely affected by the Middle East crisis.

These high-purity chemicals are produced at a limited number of petrochemical plants in East Asia. Soaring naphtha prices have created "negative spreads" — where manufacturing costs exceed selling prices — forcing plants like LG Chem and Lotte Chemical to shut down. Raw material supply to Japan's photoresist manufacturers (Shin-Etsu Chemical, JSR, Tokyo Ohka Kogyo) has been directly impacted.

On March 18-19, Iranian retaliatory ballistic missiles struck Qatar's Ras Laffan LNG facility, instantly eliminating 30-40% of the world's helium supply. Helium is extracted only through cryogenic distillation as a byproduct of natural gas production, so the destruction of the facility means immediate evaporation of supply. Restoration of the Ras Laffan facility is estimated to take 3-5 years.

Helium is an irreplaceable coolant for EUV (extreme ultraviolet) lithography equipment. Every cutting-edge AI chip — including NVIDIA's GPUs — is manufactured using these EUV machines. The semiconductor industry accounts for 20-25% of global helium consumption.

TSMC in Taiwan faces helium stockpile depletion risk by mid-May. Samsung Electronics and SK Hynix in South Korea, which depended on Qatar for approximately 65% of their helium imports, have strategic reserves lasting only until around June. When those reserves run out, new production of high-end AI chips becomes physically impossible.

### Medical Supplies Can't Be Made in America Alone

Modern healthcare depends on medical-grade polypropylene and polyethylene. IV bags, syringes, catheters, sterile pharmaceutical packaging — all naphtha-derived. These specialty polymers require strict quality controls and are produced only at limited chemical plants in East Asia and Europe. American shale gas-derived facilities cannot manufacture materials of this grade.

Inventories at major U.S. medical supply wholesalers typically cover only 30 to 45 days. These medical plastics must meet FDA's stringent biocompatibility standards (21 CFR Part 820, ISO 10993). Even when supply is cut off, switching to alternative materials requires months to years of validation and approval.

Approximately half of generic drugs used in America, and 32% of active pharmaceutical ingredients (APIs), are imported from India. India's pharmaceutical infrastructure depends on Middle Eastern energy, and its transport routes rely on the Strait of Hormuz and Middle Eastern aviation hubs. Since the blockade, Gulf region air cargo capacity has dropped 79%, and global air cargo capacity has fallen 22%. For the thin-margin generic drug business model, maritime insurance premiums surging over 1,000% and rerouting costs are fatal.

Pharmaceutical wholesaler inventories stand at 25-30 days. From late April through May, this buffer begins to disappear.

### Jet Fuel Is Not Enough from America Alone

The Hormuz blockade has cut off approximately 21% of global seaborne jet fuel supply. American refineries can process domestic crude, but a refinery produces gasoline, diesel, jet fuel, and naphtha simultaneously from the same crude. You cannot increase jet fuel production in isolation. Increasing one changes the ratios of everything else. And there is no spare capacity to simultaneously serve domestic demand, military needs, and allied nations.

Europe depends on the Persian Gulf for 25-30% of its jet fuel demand, with inventories covering just over one month. The second half of April is identified as the critical period when aviation impacts become severe.

Airlines in Southeast Asia and Oceania have begun adding fuel surcharges and cutting flights. Australia's jet fuel reserves stand at 30 days. South Korea, dependent on Gulf crude, is considering restricting jet fuel exports.

Military operations are equally dependent on jet fuel. U.S. military aerial refueling operations over the Middle East alone have consumed an estimated $54 million or more in fuel. Combined with interceptor missile depletion, the sustainability of U.S. military presence in the region is in question.

## Mythos Has Changed the Premises of Cyber Defense

On April 7, Anthropic released Claude Mythos, fundamentally altering the assumptions underlying cybersecurity.

Mythos discovered a vulnerability in OpenBSD's TCP stack that had remained hidden for 27 years. In FFmpeg, it identified a 16-year-old bug that automated testing tools had failed to detect after over 5 million fuzzing runs.

The previous top-tier model (Claude Opus 4.6) had near-zero success in autonomous exploit creation. Mythos achieved a 72.4% success rate. In Firefox vulnerability exploitation tests, Opus 4.6 succeeded twice. Mythos succeeded 181 times.

The cost of achieving root privilege escalation on a Linux kernel was under $2,000. Finding and weaponizing the 27-year-old OpenBSD bug cost less than $50. Cyber weapons that nation-state hacking groups spent months and millions of dollars developing can now be mass-produced for pocket change.

The fundamental model of cyber defense — "vulnerability disclosure → patch creation → testing → deployment" — no longer functions. With the median time for organizations to apply patches sitting at approximately 70 days, and AI able to generate exploits in hours, defenders have no time buffer.

### The Standoff Between Anthropic and the Pentagon

Anthropic has maintained two principles: no use of its AI for autonomous lethal weapons, and no use for mass domestic surveillance. When the Department of Defense demanded these principles be removed, and Anthropic refused, the company was designated a "Supply Chain Risk."

As a result, the world's most capable cyber defense tool — Mythos — cannot be used by U.S. national defense infrastructure. Anthropic withheld Mythos from general release and launched "Project Glasswing," a defensive initiative joined by approximately 50 major organizations including AWS, Apple, Google, Microsoft, and NVIDIA, with $100 million in usage credits. Wall Street financial institutions adopted Mythos at the urgent request of the Fed Chair.

Yet the military and government agencies are legally barred from using this "strongest shield." Private companies defend themselves with Mythos while the nation's defense infrastructure remains exposed. Regulations meant to protect national security are leaving national security most vulnerable.

### The Copilot Problem in Windows and Microsoft 365

The collapse of cyber defense demonstrated by Mythos extends beyond targeted attacks. A far more widespread vulnerability is already embedded in offices and homes worldwide.

Microsoft has deeply integrated Copilot into Windows and Microsoft 365. Copilot can access user files, read emails, manipulate calendars, and modify system settings. The more convenient it becomes, the greater the permissions granted to the AI.

But AI has a structural vulnerability called prompt injection. Malicious instructions can be embedded in documents or emails, causing Copilot to execute hidden commands. The "Reprompt" attack demonstrated in early 2026 showed that a single click on a legitimate-looking link enables Copilot to silently establish persistent communication with an attacker's server, exfiltrating session data and sensitive information. Techniques using notifications from trusted platforms like GitHub and Jira to deliver these injections completely bypass conventional email security filters.

In a world where AI can find decades-old vulnerabilities in hours and autonomously generate attack code, having AI deeply integrated into hundreds of millions of Windows machines creates an attack surface of unprecedented scale.

Microsoft cannot remove Copilot. Without it, users would simply access Claude directly through a browser, eliminating the need for Windows and Office. With Copilot embedded, vulnerabilities multiply. Without it, competitiveness vanishes. There is no exit.

A simpler architecture — Linux with browser-based AI access — eliminates this risk entirely. When the OS and AI are separated, there is no pathway for prompt injection to compromise the operating system.

## The AI Industry's Business Model Is Collapsing Simultaneously

The naphtha bomb and the Mythos bomb are also hitting the AI industry's business foundations.

In March 2026, OpenAI completed a $122 billion fundraise at an $852 billion valuation. SoftBank, Amazon, and NVIDIA were the largest contributors. But OpenAI cannot run its models on anything other than NVIDIA GPUs. NVIDIA GPUs are manufactured by TSMC using EUV equipment cooled by Qatari helium. When helium stockpiles run out, new GPU production stops, and OpenAI's business foundation physically ceases to exist.

In March, SoftBank signed a $40 billion loan agreement with five financial institutions in Japan and the U.S. to fund a $30 billion additional investment in OpenAI. Repayment is due March 2027. This is borrowing money to invest at the peak of an AI bubble. If OpenAI's valuation drops, the investment is impaired and the $40 billion debt remains. If SoftBank falters, its consolidated subsidiary LINEYahoo is also affected.

Microsoft invested trillions of yen in OpenAI and integrated its technology as Copilot into Windows and Office. But Copilot carries prompt injection vulnerabilities, while Mythos-level AI is beginning to replace Office functionality entirely. OpenAI — Microsoft's investment — can't escape NVIDIA dependency. Copilot — Microsoft's product — creates security vulnerabilities. Claude — the competitor — makes Office unnecessary.

Meanwhile, Anthropic's Claude runs on three different chip architectures: Google TPU, Amazon Trainium, and NVIDIA GPU. It is not dependent on any single hardware vendor. If NVIDIA stops, Claude continues running on TPUs and Trainium. This technical difference determines who survives the helium depletion caused by the naphtha bomb.

Q1 earnings beginning in April will bring these structural problems into the open as numbers. Deteriorating AI company performance, surging energy costs, severed supply chains. This will be the first earnings season where the premises of the AI bubble begin to crack.

## The Two Crises Intersect

Physical supplies are depleting due to naphtha exhaustion. The digital systems needed to optimally allocate those dwindling supplies are vulnerable to AI cyberattack. And the business platform used by corporations and financial institutions worldwide — Microsoft 365 — has Copilot embedded, giving AI access to emails, spreadsheets, and internal documents. Financial trading data, patient medical records, logistics delivery plans. All potentially exposed through a single prompt injection.

Modern supply chains operate on just-in-time principles, with inventories stripped to the minimum. Allocating remaining supplies requires cloud systems, IoT, and digital logistics networks to function flawlessly. But in a world where patches can't keep up, every one of these systems is a target.

The physical "blood" is draining from the system while the digital "nerves" are being paralyzed. Both happening at once is the essence of this crisis.

## What Is Being Asked of the Trump Administration

Both bombs are directly tied to the Trump administration's decisions.

The naphtha bomb's fuse was lit by the February 28 attack on Iran. The Strait of Hormuz blockade began as retaliation for that attack. After the Islamabad talks collapsed on April 12, President Trump did not seek to open the strait — he declared a "counter-blockade," making the situation worse. Medical supply shortages, jet fuel depletion, and semiconductor supply disruption will continue as long as the blockade persists.

On the Mythos bomb, the Department of Defense designated Anthropic a "Supply Chain Risk" in retaliation for the company's refusal to compromise its safety principles. As a result, the world's most advanced cyber defense capability is unavailable to national infrastructure. Private companies can defend with Mythos. The military and government agencies cannot.

The Trump administration is simultaneously severing the physical supply chain and stripping the digital defense network. It is the actor making both bombs worse.
