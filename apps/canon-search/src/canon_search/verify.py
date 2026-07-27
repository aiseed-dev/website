"""幻覚検証 — 生成文が引用元の正典に実際に裏打ちされているかを機械判定する。

AI百科事典の最大の失敗は「それらしい出典」の捏造(引用先に書いていないこと
を書く)である。ここでは各生成文について、引用したチャンク本文との
文字 3-gram 被覆率を測り、しきい値未満の文を「裏取り不成立」として弾く。

NLI ではないので万能ではないが、
  * 引用元に無い固有名詞・数値を持ち込む(=捏造)
  * 引用を取り違える
を安価に検出でき、「正典に近い記述に留めさせる」圧力として働く。
"""

from __future__ import annotations

import re
import unicodedata

_WS = re.compile(r"\s+")
# 引用元と草稿でゆれる約物(スマートクォート等)を吸収する
_PUNCT = str.maketrans({
    "’": "'", "‘": "'", "‛": "'", "‚": "'",
    "“": '"', "”": '"', "„": '"', "″": '"',
    "–": "-", "—": "-", "―": "-", "‐": "-", "‑": "-",
})


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).translate(_PUNCT)
    return _WS.sub("", s).lower()


def span_in_source(span: str, source_text: str) -> bool:
    """逐語スパンが引用元に(空白・約物のゆれを無視して)実在するか。

    クロスリンガルな捏造引用の検出はこれで行う: 本物の引用は原文の
    部分文字列として存在し、捏造した引用は存在しない。文字n-gram被覆率と
    違い、言語間で共通する機能語のノイズに惑わされない。
    """
    return _norm(span) in _norm(source_text)


def _ngrams(s: str, n: int = 3) -> set[str]:
    s = _norm(s)
    if len(s) < n:
        return {s} if s else set()
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def support_score(sentence: str, source_text: str, n: int = 3) -> float:
    """文の n-gram のうち、引用元にも現れる割合(0..1)。"""
    sent = _ngrams(sentence, n)
    if not sent:
        return 0.0
    src = _ngrams(source_text, n)
    return len(sent & src) / len(sent)


_CITE = re.compile(r"\[(\d+)\]\s*$")
# 〔...〕内は引用元言語の逐語スパン(クロスリンガル照合用)
_SPAN = re.compile(r"〔(.+?)〕")


def verify_article(lines: list[str], id_to_text: dict[int, str],
                   threshold: float = 0.55) -> list[dict]:
    """各行末の [n] 引用を対応チャンクと照合する。

    通常は文そのものを引用元と照合する(同一言語)。
    行に 〔逐語スパン〕 があれば、そのスパンを引用元と照合する。これにより
    「日本語の主張＋伊語正典の逐語引用」を、言語を跨いで機械検証できる
    (捏造された引用=正典に存在しないスパンを弾く)。日本語↔原語の忠実性は
    対訳を並べて人間が監査する二段構え。

    戻り値: {sentence, span, cite, score, ok, reason} のリスト。
    引用が無い文は ok=None(検証対象外の地の文)として素通しする。
    """
    out = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _CITE.search(line)
        if not m:
            out.append({"sentence": line, "span": None, "cite": None,
                        "score": None, "ok": None, "reason": "引用なし(対象外)"})
            continue
        cite = int(m.group(1))
        body = _CITE.sub("", line).strip()
        span_m = _SPAN.search(body)
        span = span_m.group(1).strip() if span_m else None
        sentence = _SPAN.sub("", body).strip()

        if span is not None:
            # クロスリンガル: 逐語スパンが正典のどこかに実在するかを部分文字列で
            # 判定する(引用IDの取り違えに強く、機能語ノイズにも惑わされない)。
            hit_id = next((i for i, t in id_to_text.items()
                           if span_in_source(span, t)), None)
            ok = hit_id is not None
            out.append({
                "sentence": sentence, "span": span,
                "cite": hit_id if ok else cite,
                "score": 1.0 if ok else 0.0, "ok": ok,
                "reason": ("裏取りOK(逐語一致)" if ok
                           else "引用スパンが正典に見当たらない(捏造引用の疑い)"),
            })
            continue

        src = id_to_text.get(cite)
        if src is None:
            out.append({"sentence": sentence, "span": None, "cite": cite,
                        "score": 0.0, "ok": False,
                        "reason": f"引用[{cite}]が正典に存在しない"})
            continue
        score = support_score(sentence, src)
        ok = score >= threshold
        out.append({"sentence": sentence, "span": None, "cite": cite,
                    "score": score, "ok": ok,
                    "reason": "裏取りOK" if ok else "引用元に十分な根拠なし"})
    return out
