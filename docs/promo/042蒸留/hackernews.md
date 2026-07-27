<!--
投稿先: Hacker News (news.ycombinator.com/submit)
投稿日時: 2026-07-27(日) 21:00〜23:00 JST(米東部の日曜朝。平日朝より流量は落ちるが競争も少ない。伸びなければ火曜21-23時JSTに一度だけ再投稿可)
方針: URL投稿。タイトルは原題のまま。投稿直後に下のAuthorコメントを自分で付ける
注意: 他人にupvoteを頼まない(投票リング検知でペナルティ)。コメントには全て返信する
-->

## title欄

Distillation is not only about AI – AI builds the business system

## url欄

https://aiseed.dev/en/blog/distilling-business-systems/

## 投稿直後に付けるコメント(Author comment)

Author here. The piece started from the Kimi K3 distillation dispute, but the point that stuck with me is broader: distillation needs no internals, only input-output pairs — and that is exactly what a test suite is. Put questions to the system running today, record the answers, and the behavior of the business is in your hands. The current system becomes the teacher model.

Anthropic's migration post from two weeks ago (https://claude.com/blog/ai-code-migration) shows the same shape at industrial scale — Bun's million-line Zig→Rust port in under two weeks, with the existing test suite as the referee. My argument is that the same mechanics apply one level up, to line-of-business systems, where the test suite is something you can extract from the running system itself.

What I keep going back and forth on is the last section: if the reason for a change can only come from the business, the test data comes from the model or your own records, and the implementation comes from AI, what is actually left to outsource? Curious where people think that argument breaks.

## 補足

- HNのタイトル慣行に合わせ、原題の「—」は「–」に、文中語は小文字に調整済み(HNは文頭以外の大文字タイトルを自動修正することがある)
- 同時にやるとよいこと: 今日のK3スレッド(重み公開のニュース)に1〜2件、宣伝抜きの技術コメントを付けておく。アカウントに履歴ができ、スパム判定の余地が消える
- 反応ゼロでも失敗ではない。HNは大半が沈む。数日後の再投稿は1回まで許容される
