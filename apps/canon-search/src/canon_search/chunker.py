"""テキストを検索・引用に適した断片(チャンク)に分割する。"""

from __future__ import annotations

import re

_SECTION_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+\S")


def chunk_paragraphs(text: str, max_chars: int = 1200) -> list[tuple[str, str]]:
    """空行区切りの段落を ~max_chars に詰める。(heading, text) のリストを返す。

    「1.2.3 Title」形式の行を節見出しとして追跡し、各チャンクに付ける。
    """
    chunks: list[tuple[str, str]] = []
    heading = ""
    buf: list[str] = []
    buf_len = 0

    def flush():
        nonlocal buf, buf_len
        if buf:
            chunks.append((heading, "\n\n".join(buf)))
            buf, buf_len = [], 0

    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        first_line = para.splitlines()[0].strip()
        if _SECTION_RE.match(first_line) and len(first_line) < 90:
            flush()
            heading = first_line
        if buf_len + len(para) > max_chars:
            flush()
        # 単独で max_chars を超える巨大段落はそのまま1チャンクにする
        buf.append(para)
        buf_len += len(para)
        if buf_len > max_chars:
            flush()
    flush()
    return chunks
