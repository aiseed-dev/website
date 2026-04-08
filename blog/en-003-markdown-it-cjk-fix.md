---
slug: markdown-it-cjk-fix
lang: en
title: "Claude Fixed a Bold Rendering Bug in markdown-it and Submitted the Pull Request"
subtitle: "No need to outsource to contractors anymore"
description: "Found a bug in markdown-it-py where bold fails in mixed CJK/ASCII text. Claude Code identified the root cause, wrote a 6-line fix, forked the repo, and submitted a PR — all in a single session."
date: 2026.04.06
label: Blog
category: AI Development Notes
---

## What Happened

While writing a blog post, I noticed broken rendering:

```
ホルムズ海峡は世界の海上石油輸送の**20〜25%**が通過する。
```

The `**` markers were displayed as plain text instead of rendering bold.

Adding spaces around the markers fixed it — but inserting spaces in Japanese text is unnatural. This was a bug.

## Root Cause

The `scanDelims` function in [markdown-it-py](https://github.com/executablebooks/markdown-it-py).

In the CommonMark spec, `**` must be a **right-flanking delimiter** to close bold. The check:

`right_flanking = not (isLastPunctChar and not (isNextWhiteSpace or isNextPunctChar))`

For the closing `**` in `**46%**を`:
- `lastChar='%'` → punctuation → `isLastPunctChar=True`
- `nextChar='を'` → CJK character → neither whitespace nor punctuation

Result: `right_flanking = False`. The closing `**` is rejected.

**CJK characters after ASCII punctuation break bold rendering.** This affects Japanese, Chinese, and Korean text.

## The Fix

6 lines added to `scanDelims` in `state_inline.py`. Treat CJK characters (U+2E80+) as punctuation so they are recognized as word boundaries:

```python
# Treat CJK ideographs as punctuation for flanking delimiter checks
if not isNextPunctChar and ord(nextChar) > 0x2E7F:
    isNextPunctChar = True
if not isLastPunctChar and ord(lastChar) > 0x2E7F:
    isLastPunctChar = True
```

Test results:

| Input | Before | After |
|-------|--------|-------|
| `湾岸の**46%**を供給` | ** remains as text | **46%** renders bold |
| `の**20〜25%**が通過する` | ** remains as text | **20〜25%** renders bold |
| `日本語の**太字**テスト` | works | works |
| `English **bold** test` | works | works |

No impact on English-only text.

## What Claude Code Did

From bug discovery to PR submission — everything in one Claude Code session:

1. **Found the bug** — noticed broken rendering in blog build output
2. **Identified the cause** — read markdown-it-py source, analyzed `scanDelims` flanking delimiter logic
3. **Wrote the fix** — 6 lines treating CJK characters as punctuation
4. **Tested** — 8 test patterns in both Japanese and English
5. **Created a fork** — `aiseed-dev/markdown-it-py` with `fix/cjk-emphasis` branch
6. **Submitted a PR** — [executablebooks/markdown-it-py#387](https://github.com/executablebooks/markdown-it-py/pull/387)
7. **Updated the project** — switched `requirements.txt` to the fork, rebuilt all pages

## No Need to Outsource

Traditionally, this kind of work would require:
- Filing a bug report and commissioning investigation
- External library research and fix strategy review
- Fork management and PR creation
- Test creation and execution

Outsourcing this would cost days to weeks and thousands of dollars.

Claude Code found the bug while writing a blog post, identified the root cause, wrote the fix, tested it, and submitted the PR — **all in a single session**.

:::highlight
**There is no longer any need to outsource to contractors.**

All you need is the ability to describe the problem accurately and judge the results. The ability to write code is no longer required on the human side.
:::

## Links

- [Pull Request: Fix CJK emphasis delimiter detection](https://github.com/executablebooks/markdown-it-py/pull/387)
- [aiseed-dev/markdown-it-py (fork)](https://github.com/aiseed-dev/markdown-it-py/tree/fix/cjk-emphasis)
