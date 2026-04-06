#!/usr/bin/env python3
"""
Patch markdown-it-py to fix CJK emphasis delimiter detection.

Problem: In CommonMark spec, **46%** adjacent to CJK characters (e.g. 湾岸の**46%**を)
fails to render as <strong> because the closing ** is not recognized as a
right-flanking delimiter when the character before ** is ASCII punctuation (%)
and the character after ** is CJK.

Fix: Treat CJK characters (U+2E80+) as punctuation in flanking delimiter checks,
so they behave like word boundaries.

Usage:
    python3 tools/patches/markdown_it_cjk_emphasis.py

This patches the installed markdown_it package in-place.
"""

import re
from pathlib import Path
import markdown_it

state_inline = Path(markdown_it.__file__).parent / "rules_inline" / "state_inline.py"
content = state_inline.read_text(encoding="utf-8")

PATCH_MARKER = "# CJK emphasis fix"

if PATCH_MARKER in content:
    print("Already patched.")
    exit(0)

# Insert CJK-as-punctuation fix before left_flanking calculation
old = "        left_flanking = not ("
new = f"""        {PATCH_MARKER}: treat CJK ideographs as punctuation for flanking checks
        if not isNextPunctChar and ord(nextChar) > 0x2E7F:
            isNextPunctChar = True
        if not isLastPunctChar and ord(lastChar) > 0x2E7F:
            isLastPunctChar = True

        left_flanking = not ("""

content = content.replace(old, new, 1)
state_inline.write_text(content, encoding="utf-8")
print(f"Patched: {state_inline}")
