<!--
投稿先: Quora (英語) — 既存の質問への回答として投稿する。記事の転載ではなく回答が流通単位
狙う質問の型(検索して見つける):
  - "Will AI replace IT outsourcing / software consultants?"
  - "Can AI migrate or rewrite legacy code/systems?"
  - "How can a small business afford custom software?"
方針: 回答単体で完結させ、リンクは末尾に1本。同一文面を複数の質問に貼らない(スパム判定で折りたたまれる)。質問ごとに冒頭1〜2文を質問に合わせて書き換える
長さ: 300 words前後
-->

Something concrete happened this July that changes this answer.

Anthropic's engineering blog documented two migrations. Bun — a JavaScript runtime — had one million lines of Zig ported to Rust in under two weeks, with 100% of the existing test suite passing, for about $165,000 in API costs. In the same article, a single developer moved a 165,000-line Python project to TypeScript over one weekend. The method in both cases: don't fix the code, fix the loop that produces the code, and "let scripts — a compiler, a diff, a test suite — be the referee."

Now scale that down. The custom portion of a typical small-business system — sales, inventory, invoicing — is a few thousand to a few tens of thousands of lines. At the demonstrated cost of roughly $0.17 per line, fifty thousand lines converts to a few thousand dollars and a weekend. Not a multi-year, seven-figure project.

The one real difference from the Bun case: Bun had a test suite, and business systems usually don't. But that turns out to be solvable, because a test is nothing but putting a question to a system and recording the answer — enter an order, this document is raised; close the period, this balance appears. Your current system becomes the teacher, exactly the way an expensive AI model gets "distilled" into a cheap one from its input-output pairs alone. And what you're copying isn't the vendor's code. It's how your own business ought to behave — which was yours to begin with.

What remains for humans: deciding what to change and why, and supplying the test cases only someone who knows the business can state. What disappears: the reason to outsource the implementation.

I wrote up the full argument, with the numbers and the procedure, here: https://aiseed.dev/en/blog/large-proves-small/
