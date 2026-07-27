#!/usr/bin/env python3
"""Markdown 記事ツリー → シリーズ単位 AsciiDoc への一括変換。

旧リポジトリ(--src)の articles/<series>/<NN-slug>/{ja,en}.md を読み、
新レイアウト

    articles/<series>.adoc                     … シリーズ全記事(日英)を1ファイルに
    articles/assets/<series>/<記事ID>/…        … 画像・PDF等の資産
    articles/examples/<series>/<章ID>/…        … ai-native-ways の example コード
    docs/series-notes/…                        … 旧シリーズ直下の README(ビルド対象外)

を生成する。ソース側は一切変更しない(何度でも再実行できる)。既存の
シリーズファイルがある場合は --force が無い限り上書きしない。

変換規約(tools/build/series.py のフォーマット):
  - 記事区切り: `// ===== article: <記事ID> =====`
  - フロントマター: 日英で同値のキーは裸、異なるキーは key.ja / key.en。
    lang と prev/next 連鎖は捨てる(展開時に合成・文書順から導出)。
    捨てた連鎖がフォルダ順と食い違う場合は不整合として報告し失敗する。
  - 本文: ifdef::lang-ja[] / ifdef::lang-en[] の2ブロック。

本文の Markdown → AsciiDoc(pyasciidoc 語彙)変換は行ベース:
  見出し #→=、リスト(入れ子はマーカー反復)、引用 > → ____、罫線 → '''、
  リンク [t](u) → u[t]/link:u[t]、画像 ![a](s) → image::s[a]、
  表 → |===、強調 **→* / *→_、``` フェンスは素通し(mermaid含む)、
  独自ブロック :::quote/:::chain/:::highlight/:::compare →
  ____ / [.chain-diagram]+-- / [.highlight-box]+-- / |===。

機械変換で意味が保てない箇所(太字リンク、生HTML等)は変換レポートに
書き出す。検証は tools/verify_migration.py(新旧ビルドのHTML突き合わせ)。

使い方:
    python3 tools/convert_md_to_adoc.py --src /home/dev/dev/website [--force]
    python3 tools/convert_md_to_adoc.py --src … --series blog   # 1シリーズのみ
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build.markdown import parse_frontmatter  # noqa: E402
from build.series import SERIES_MAP  # noqa: E402

NEW_ROOT = Path(__file__).parent.parent

# シリーズファイル名 → 旧リポジトリでの記事フォルダ位置(articles/ 相対)と
# part-*/ 再帰の有無
OLD_LAYOUT = {
    "insights.adoc": ("insights", True),
    "blog.adoc": ("blog", False),
    "claude-debian.adoc": ("claude-debian", False),
    "claude-debian-server.adoc": ("claude-debian/server", False),
    "ai-native-ways.adoc": ("ai-native-ways", False),
    "ai-native-ways-software.adoc": ("ai-native-ways/software", False),
    "phosphorus-and-farming.adoc": ("phosphorus-and-farming", False),
    "fable.adoc": ("fable", False),
}

report_lines = []


def report(msg):
    report_lines.append(msg)
    print(f"  [報告] {msg}")


# ---------------------------------------------------------------------------
# インライン変換
# ---------------------------------------------------------------------------

_CODE_SPAN_RE = re.compile(r"`[^`\n]+`")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")
_AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
_BOLD_LINK_RE = re.compile(r"\*\*(\[[^\]]+\]\([^)]+\))\*\*")
# 強調は「単一 * の em → _ _」を先に変換してから「** の strong → * *」を
# 変換する。em の正規表現は ** の対を素通しする(開き直後・閉じ直前の
# 非空白条件と、* の連続を除外する lookaround)ので、順序さえ守れば
# 退避なしで安全に共存できる。strong の中身は単一 * を許す
# (`**bold *em* bold**` → em 先行変換で `**bold _em_ bold**` になるため)。
_STRONG_RE = re.compile(r"\*\*(?=\S)((?:[^*]|\*(?!\*))+?)(?<=\S)\*\*")
_EM_STAR_RE = re.compile(r"(?<![\w*])\*(?=[^\s*])([^*\n]+?)(?<=[^\s*])\*(?![\w*])")
_RAW_HTML_RE = re.compile(r"</?[a-zA-Z][^>]*>")


def _adoc_link(text, url):
    if url.startswith(("http://", "https://")):
        return url if text == url else f"{url}[{text}]"
    return f"link:{url}[{text}]"


def _attr_quote(s):
    """属性リスト([alt] 等)に入れる値。カンマや ] を含むときは引用する。"""
    if "," in s or "]" in s:
        return '"' + s.replace('"', "'") + '"'
    return s


def convert_inline(text, where=""):
    """1行分(またはセル1つ分)のインライン Markdown を AsciiDoc に変換。"""
    # インラインコードを退避(コード内は一切変換しない)
    codes = []

    def _stash(m):
        codes.append(m.group(0))
        return f"\x00{len(codes) - 1}\x00"

    text = _CODE_SPAN_RE.sub(_stash, text)

    # 太字リンク **[t](u)** は AsciiDoc(pyasciidoc)では表現できない。
    # リンクを残して太字を落とし、レポートする。
    if _BOLD_LINK_RE.search(text):
        report(f"太字リンクを非太字リンクに変更: {where}: {text.strip()[:80]}")
        text = _BOLD_LINK_RE.sub(r"\1", text)

    text = _IMAGE_RE.sub(lambda m: f"image:{m.group(2)}[{_attr_quote(m.group(1))}]", text)
    text = _LINK_RE.sub(lambda m: _adoc_link(m.group(1), m.group(2)), text)
    text = _AUTOLINK_RE.sub(r"\1", text)

    # 強調: em(単一*)→ _ _ を先に、strong(**)→ * * を後に(上の定義コメント参照)
    text = _EM_STAR_RE.sub(r"_\1_", text)
    text = _STRONG_RE.sub(r"*\1*", text)

    # 表セル内などの <pre>…<br/>…</pre> はインラインコードに落とす
    # (pyasciidoc は生HTMLを出さないため。可視テキストは旧と同じになる)
    text = re.sub(
        r"<pre>(.*?)</pre>",
        lambda m: "`" + re.sub(r"<br\s*/?>", " ", m.group(1)).strip() + "`",
        text,
    )

    # 生HTMLの検査はコード復元より前に行う(`<app>` のようなコード内の
    # 山括弧を誤検出しないため)
    if _RAW_HTML_RE.search(text):
        report(f"生HTMLが残っています(要手当て): {where}: {text.strip()[:80]}")

    for i, c in enumerate(codes):
        text = text.replace(f"\x00{i}\x00", c)
    return text


# ---------------------------------------------------------------------------
# ブロック変換
# ---------------------------------------------------------------------------

_FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# 罫線は - と * のみ(_ を含めると引用正規化が出力する ____ デリミタに
# 誤マッチする。コーパスの罫線は実測 --- のみ)
_HR_RE = re.compile(r"^ {0,3}([-*])(?:\s*\1){2,}\s*$")
_UL_RE = re.compile(r"^(\s*)([-*+])\s+(.*)$")
_OL_RE = re.compile(r"^(\s*)(\d{1,3})[.)]\s+(.*)$")
_QUOTE_RE = re.compile(r"^\s{0,3}>\s?(.*)$")
_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_SEP_RE = re.compile(r"^\s*\|(\s*:?-+:?\s*\|)+\s*$")


def _split_md_row(line):
    parts = [c.strip() for c in line.strip().split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def _convert_table(rows, where):
    """Markdown の | 行の並び(セパレータ含む)→ |=== ブロック。"""
    out = ["|==="]
    for row in rows:
        if _TABLE_SEP_RE.match(row):
            continue
        cells = _split_md_row(row)
        cells = [convert_inline(c, where).replace("|", "\\|") if "|" in c
                 else convert_inline(c, where) for c in cells]
        out.append("| " + " | ".join(cells))
    out.append("|===")
    return out


def _list_depth(indent_stack, indent):
    """インデント幅からリストの深さを決める(幅のスタックで管理)。"""
    while indent_stack and indent < indent_stack[-1]:
        indent_stack.pop()
    if not indent_stack or indent > indent_stack[-1]:
        indent_stack.append(indent)
    return len(indent_stack)


# 行をまたぐ **強調**(散文の折返し)。単一の改行のみ許し、空行(段落境界)は
# またがない。旧パイプラインでは強調の中の softbreak が cjk_friendly の
# 空白抑制付きで結合されていたので、変換では同じ規則(改行の両側が CJK なら
# 空白なし、それ以外は空白1つ)で1行に結合する。
_ML_STRONG_RE = re.compile(
    r"\*\*(?=\S)((?:[^*\n]|\*(?!\*)|\n(?![ \t]*\n))+?)(?<=\S)\*\*"
)
# 単一 * は行頭のリストマーカーと紛れやすいので、開き直後・閉じ直前が
# 非空白のものだけを対象にする(リスト項目 `* item` は直後が空白なので不成立)
_ML_EM_RE = re.compile(
    r"(?<![\w*])\*(?=[^\s*])((?:[^*\n]|\n(?![ \t]*\n))+?)(?<=[^\s*])\*(?![\w*])"
)


def _is_cjk(ch):
    o = ord(ch)
    return (
        0x3000 <= o <= 0x30FF      # CJK記号・約物・かな
        or 0x3400 <= o <= 0x9FFF   # 漢字
        or 0xF900 <= o <= 0xFAFF   # 互換漢字
        or 0xFF00 <= o <= 0xFF60   # 全角形
        or 0x20000 <= o <= 0x2FFFF
    )


def _join_lines_cjk(text):
    """改行を1行に結合。両側が CJK なら空白なし、そうでなければ空白1つ
    (mdit-py-cjk-friendly の softbreak 挙動の再現)。"""
    def _join(m):
        a, b = m.group(1), m.group(2)
        sep = "" if _is_cjk(a) and _is_cjk(b) else " "
        return a + sep + b
    return re.sub(r"(\S)[ \t]*\n[ \t]*(\S)", _join, text)


# 行をまたぐリンク・画像。テキスト部は CJK 考慮で結合、URL 部は無条件に
# 詰めて結合する(URL に空白は入れられない)。
_ML_LINK_RE = re.compile(
    r"(!?)\[((?:[^\]\n]|\n(?![ \t]*\n))+?)\]\(((?:[^)\n]|\n(?![ \t]*\n))+?)\)"
)


def _join_multiline_emphasis(md_text):
    def _fix_link(m):
        if "\n" not in m.group(0):
            return m.group(0)
        text = _join_lines_cjk(m.group(2))
        url = re.sub(r"\s*\n\s*", "", m.group(3))
        return f"{m.group(1)}[{text}]({url})"

    def _fix(m, marker):
        inner = m.group(1)
        if "\n" not in inner:
            return m.group(0)
        return marker + _join_lines_cjk(inner) + marker

    # フェンス(```)内は触らない
    out = []
    buf = []
    in_fence = False
    fence_ch = ""

    def _flush():
        text = "\n".join(buf)
        # 「… +」で行が折り返している散文(例: apt + Flatpak +⏎conda)は
        # AsciiDoc のハード改行 ` +` と誤解釈されるので、ここで1行に結合する
        text = re.sub(r"[ \t]\+\n(?![ \t]*\n)[ \t]*", " + ", text)
        text = _ML_LINK_RE.sub(_fix_link, text)
        text = _ML_STRONG_RE.sub(lambda m: _fix(m, "**"), text)
        text = _ML_EM_RE.sub(lambda m: _fix(m, "*"), text)
        out.append(text)

    for line in md_text.split("\n"):
        fm = _FENCE_RE.match(line)
        if fm and not in_fence:
            _flush()
            buf = []
            out.append(line)
            in_fence, fence_ch = True, fm.group(2)[0]
            continue
        if in_fence:
            out.append(line)
            if re.match(rf"^\s*{re.escape(fence_ch)}{{3,}}\s*$", line):
                in_fence = False
            continue
        buf.append(line)
    _flush()
    return "\n".join(out)


def _normalize_quotes(md_text):
    """`> ` 引用のまとまりを ____ ブロックに正規化する(フェンス外のみ)。
    行またぎ強調の結合より先に行う——引用の継続行の `> ` プレフィックスが
    強調の中に紛れ込まないように。中身の行は `> ` を剥がしてそのまま出し、
    後段の変換(見出し・リスト・インライン)に任せる。"""
    lines = md_text.split("\n")
    out = []
    i = 0
    n = len(lines)
    in_fence = False
    fence_ch = ""
    while i < n:
        line = lines[i]
        fm = _FENCE_RE.match(line)
        if fm and not in_fence:
            in_fence, fence_ch = True, fm.group(2)[0]
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            if re.match(rf"^\s*{re.escape(fence_ch)}{{3,}}\s*$", line):
                in_fence = False
            i += 1
            continue
        if line.lstrip().startswith(">"):
            out.append("____")
            while i < n and lines[i].lstrip().startswith(">"):
                stripped = re.sub(r"^\s{0,3}>\s?", "", lines[i])
                out.append(stripped)
                i += 1
            out.append("____")
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def convert_body(md_text, where):
    """Markdown 本文全体 → AsciiDoc 本文。"""
    md_text = _normalize_quotes(md_text)
    md_text = _join_multiline_emphasis(md_text)
    lines = md_text.split("\n")
    out = []
    i = 0
    n = len(lines)
    indent_stack = []

    def close_lists():
        indent_stack.clear()

    while i < n:
        line = lines[i]
        prev_blank = i == 0 or lines[i - 1].strip() == ""

        # ``` フェンス(mermaid 含む): 閉じフェンスまで素通し
        fm = _FENCE_RE.match(line)
        if fm:
            out.append(line)
            marker = fm.group(2)
            i += 1
            while i < n:
                out.append(lines[i])
                if re.match(rf"^\s*{re.escape(marker[0])}{{{len(marker)},}}\s*$", lines[i]):
                    i += 1
                    break
                i += 1
            close_lists()
            continue

        stripped = line.strip()

        # 独自 ::: ブロック
        if stripped.startswith(":::"):
            kind = stripped[3:].strip()
            block = []
            i += 1
            while i < n and lines[i].strip() != ":::":
                block.append(lines[i])
                i += 1
            i += 1  # closing :::
            out.extend(_convert_custom_block(kind, block, where))
            close_lists()
            continue

        # 引用: 連続する > 行をまとめて ____ ブロックに
        qm = _QUOTE_RE.match(line)
        if qm and stripped.startswith(">"):
            quote = []
            while i < n:
                q = _QUOTE_RE.match(lines[i])
                if not q or not lines[i].strip().startswith(">"):
                    break
                quote.append(convert_inline(q.group(1), where))
                i += 1
            out.append("____")
            out.extend(quote)
            out.append("____")
            close_lists()
            continue

        # 表
        if _TABLE_ROW_RE.match(line) and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
            rows = []
            while i < n and _TABLE_ROW_RE.match(lines[i]):
                rows.append(lines[i])
                i += 1
            out.extend(_convert_table(rows, where))
            close_lists()
            continue

        # 罫線
        if _HR_RE.match(line):
            out.append("'''")
            i += 1
            close_lists()
            continue

        # 見出し
        hm = _HEADING_RE.match(line)
        if hm:
            out.append("=" * len(hm.group(1)) + " " + convert_inline(hm.group(2), where))
            i += 1
            close_lists()
            continue

        # リスト項目(入れ子はインデント幅→マーカー反復)
        um = _UL_RE.match(line)
        om = None if um else _OL_RE.match(line)
        if om and not indent_stack and not prev_blank and om.group(2) != "1":
            # CommonMark と同じく、段落に割り込める番号付きリストは 1. だけ
            # (「…Chapters 7 and\n8. The concrete…」のような折返しの数字を
            # リストにしない)
            om = None
        if um or om:
            m = um or om
            indent = len(m.group(1).replace("\t", "    "))
            depth = _list_depth(indent_stack, indent)
            marker = ("*" if um else ".") * depth
            out.append(f"{marker} {convert_inline(m.group(3), where)}")
            i += 1
            continue

        if stripped == "":
            close_lists()
            out.append(line)
            i += 1
            continue

        # 生の <pre>…</pre> 1行ブロック → リストブロック(----)へ
        pm = re.match(r"^<pre>(.*)</pre>\s*$", stripped)
        if pm:
            content = re.sub(r"<br\s*/?>", "\n", pm.group(1))
            out.extend(["----", *content.split("\n"), "----"])
            i += 1
            close_lists()
            continue

        # 過去のAI編集事故の残骸タグは出力しない(旧パイプラインでは生HTML
        # としてブラウザに無視されていた)
        if stripped in ("</content>", "</invoke>", "<content>", "<invoke>"):
            report(f"残骸タグを除去: {where}: {stripped}")
            i += 1
            continue

        # 行頭が AsciiDoc の構文文字(= // ''')になる地の文は、直前の行に
        # 連結して誤解釈を防ぐ(Markdown では段落の折返しだった行)
        if stripped.startswith(("=", "//", "'''")) and not prev_blank:
            prev_out = out[-1].strip() if out else ""
            if prev_out and not re.match(
                r"^(={1,6} |-{2,}|_{4,}|\|===|'''|//|\[|\*+ |\.+ |image::|`{3,})",
                prev_out,
            ):
                out[-1] = _join_lines_cjk(
                    out[-1] + "\n" + convert_inline(stripped, where)
                )
                i += 1
                continue
            report(f"行頭の構文文字を連結できません(要確認): {where}: {stripped[:60]}")

        # リスト項目の折返し行(インデントあり)はそのまま出す——pyasciidoc が
        # 直前項目の principal text 継続として連結する
        out.append(convert_inline(line, where))
        i += 1

    # 連続空行を1つに(見た目のノイズ削減。意味は変わらない)
    cleaned = []
    for line in out:
        if line.strip() == "" and cleaned and cleaned[-1].strip() == "":
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def _hard_break_lines(lines_):
    """グループ内の改行を保つ——次の行が非空なら行末に ` +`(ハード改行)。
    旧 ::: ブロックは全ての改行を <br> にしていたことに対応する。"""
    body = []
    for j, l in enumerate(lines_):
        nxt = lines_[j + 1] if j + 1 < len(lines_) else ""
        body.append(l + " +" if l.strip() and nxt.strip() else l)
    return body


def _convert_custom_block(kind, block_lines, where):
    content = "\n".join(block_lines).strip()
    if kind.startswith("quote"):
        lines_ = [convert_inline(l, where) for l in content.split("\n")]
        return ["____", *_hard_break_lines(lines_), "____"]
    if kind.startswith("chain"):
        # 行分けは意図的なもの(工程の連鎖図)。CJK 隣接では softbreak が
        # 消えるので、グループ内の改行は AsciiDoc のハード改行 ` +` で保つ
        lines_ = [convert_inline(l, where) for l in content.split("\n")]
        return ["[.chain-diagram]", "--", *_hard_break_lines(lines_), "--"]
    if kind.startswith("highlight"):
        inner = convert_body(content, where)
        return ["[.highlight-box]", "--", *inner.split("\n"), "--"]
    if kind.startswith("compare"):
        rows = [l for l in content.split("\n") if l.strip()]
        return _convert_table(rows, where)
    report(f"未知の:::ブロック '{kind}' をそのまま出力: {where}")
    return block_lines


# ---------------------------------------------------------------------------
# フロントマター統合
# ---------------------------------------------------------------------------

_DROP_KEYS = {"lang", "prev_slug", "prev_title", "next_slug", "next_title"}


def merge_meta(meta_ja, meta_en):
    """日英のフロントマターを統合。同値→裸キー、異なる→key.ja/key.en。"""
    merged = {}
    keys = list(meta_ja.keys()) + [k for k in meta_en.keys() if k not in meta_ja]
    for k in keys:
        if k in _DROP_KEYS:
            continue
        vj = meta_ja.get(k)
        ve = meta_en.get(k)
        if vj is not None and ve is not None:
            if vj == ve:
                merged[k] = vj
            else:
                merged[f"{k}.ja"] = vj
                merged[f"{k}.en"] = ve
        elif vj is not None:
            merged[f"{k}.ja" if k in ("title", "subtitle", "description") else k] = vj
        else:
            merged[f"{k}.en"] = ve
    return merged


# ---------------------------------------------------------------------------
# 記事フォルダの走査と変換
# ---------------------------------------------------------------------------


def iter_article_dirs(series_dir, recurse):
    """旧 _iter_article_files と同じ順序で (記事ID, フォルダ) を返す。"""
    for sub in sorted(series_dir.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name[:1].isdigit():
            yield sub.name, sub
        elif recurse:
            for ch in sorted(sub.iterdir()):
                if ch.is_dir() and ch.name[:1].isdigit():
                    yield f"{sub.name}/{ch.name}", ch


def convert_article(article_id, folder, stem, where, nav_overrides=None):
    """1記事分の節テキストと、資産コピーの一覧を返す。

    nav_overrides: {"ja": {"prev_title": …}, …} — 著者が意図的に短縮した
    nav 表記(隣の記事の実タイトルと異なる prev/next タイトル)を明示キー
    として残す。無指定のものは展開時に隣の実タイトルから導出される。"""
    src = {}
    meta = {}
    for lang in ("ja", "en"):
        f = folder / f"{lang}.md"
        if f.exists():
            m, body = parse_frontmatter(f.read_text(encoding="utf-8"))
            meta[lang] = m
            src[lang] = body
    if not src:
        return None, []

    merged = merge_meta(meta.get("ja", {}), meta.get("en", {}))
    for lang, kv in (nav_overrides or {}).items():
        for k, v in kv.items():
            merged[f"{k}.{lang}"] = v

    section = [f"// ===== article: {article_id} =====", "---"]
    section += [f"{k}: {v}" for k, v in merged.items() if str(v).strip() != ""]
    section.append("---")
    for lang in ("ja", "en"):
        if lang in src:
            section.append(f"ifdef::lang-{lang}[]")
            section.append(convert_body(src[lang], f"{where}/{lang}.md"))
            section.append("endif::[]")

    # 資産: ja.md/en.md 以外の全ファイル(example-N は別扱い)
    assets = []
    for f in sorted(folder.iterdir()):
        if f.name in ("ja.md", "en.md"):
            continue
        if f.is_dir():
            if f.name.startswith("example-"):
                assets.append(("example", f))
            else:
                report(f"記事フォルダ内の想定外ディレクトリ(資産として扱わない): {where}/{f.name}")
            continue
        assets.append(("asset", f))
    return "\n".join(section), assets


def check_nav(units_meta, series_name):
    """旧フロントマターの prev/next 連鎖が、フォルダ順から導出される連鎖と
    一致するかを言語ごとに確認する。不一致は変換を止める(黙って順序を
    変えて公開しないため)。units_meta: [(article_id, {"ja": meta, "en": meta})]"""
    problems = []
    for lang in ("ja", "en"):
        chain = [
            (aid, metas[lang]) for aid, metas in units_meta
            if lang in metas and metas[lang].get("number")
        ]
        for idx, (aid, m) in enumerate(chain):
            want_prev = chain[idx - 1][1].get("slug", "") if idx > 0 else ""
            want_next = chain[idx + 1][1].get("slug", "") if idx + 1 < len(chain) else ""
            got_prev = m.get("prev_slug", "")
            got_next = m.get("next_slug", "")
            if got_prev != want_prev:
                problems.append(
                    f"{series_name}/{aid} [{lang}] prev_slug: 旧={got_prev!r} フォルダ順={want_prev!r}"
                )
            if got_next != want_next:
                problems.append(
                    f"{series_name}/{aid} [{lang}] next_slug: 旧={got_next!r} フォルダ順={want_next!r}"
                )
    return problems


def convert_series(src_root, name, force):
    rel, recurse = OLD_LAYOUT[name]
    stem = name[: -len(".adoc")]
    series_dir = src_root / "articles" / rel
    out_file = NEW_ROOT / "articles" / name
    if not series_dir.exists():
        print(f"スキップ({series_dir} がありません): {name}")
        return False
    if out_file.exists() and not force:
        raise SystemExit(f"{out_file} が既にあります。上書きするには --force を付けてください")

    print(f"変換中: {rel} → articles/{name}")

    # 1周目: フロントマターだけ読んで、nav タイトルの明示保存の要否を決める
    # (隣の記事の実タイトルと異なる prev/next タイトルは著者の意図的な
    # 短縮表記なので、落とさずに明示キーで残す)
    entries = []
    for article_id, folder in iter_article_dirs(series_dir, recurse):
        metas = {}
        for lang in ("ja", "en"):
            f = folder / f"{lang}.md"
            if f.exists():
                metas[lang], _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        entries.append((article_id, folder, metas))

    overrides = {aid: {} for aid, _, _ in entries}
    for lang in ("ja", "en"):
        chain = [
            (aid, m[lang]) for aid, _, m in entries
            if lang in m and m[lang].get("number")
        ]
        for idx, (aid, m) in enumerate(chain):
            ov = {}
            if idx > 0:
                stored = m.get("prev_title", "")
                if stored and stored != chain[idx - 1][1].get("title", ""):
                    ov["prev_title"] = stored
            if idx + 1 < len(chain):
                stored = m.get("next_title", "")
                if stored and stored != chain[idx + 1][1].get("title", ""):
                    ov["next_title"] = stored
            if ov:
                overrides[aid][lang] = ov

    sections = []
    units_meta = []
    asset_jobs = []
    for article_id, folder, metas in entries:
        where = f"{rel}/{article_id}"
        section, assets = convert_article(
            article_id, folder, stem, where, overrides[article_id]
        )
        if section is None:
            report(f"ソースなしでスキップ: {where}")
            continue
        sections.append(section)
        units_meta.append((article_id, metas))
        for kind, f in assets:
            asset_jobs.append((kind, article_id, f))

    problems = check_nav(units_meta, rel)
    if problems:
        print("\nprev/next 連鎖がフォルダ順と一致しません:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        raise SystemExit(f"{name}: 連鎖の不一致が {len(problems)} 件。修正するか順序を確認してください")

    header = [
        f"// {stem} — シリーズ全記事(このファイル1つで管理)",
        "// 記事の区切り: // ===== article: <記事ID> =====",
        "// フロントマター: 日英共通は裸キー、異なる値は key.ja / key.en",
        "// 本文: ifdef::lang-ja[] / ifdef::lang-en[] で言語別",
        "// prev/next 連鎖は書かない(記事の並び順から自動導出)",
        "",
    ]
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(header) + "\n".join(s + "\n" for s in sections), encoding="utf-8")

    # 資産コピー
    for kind, article_id, f in asset_jobs:
        if kind == "asset":
            dest = NEW_ROOT / "articles" / "assets" / stem / article_id / f.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
        else:  # example ディレクトリ
            dest = NEW_ROOT / "articles" / "examples" / stem / article_id / f.name
            if dest.exists():
                shutil.rmtree(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(f, dest)

    # シリーズ直下のファイル: README はビルド対象外なので docs/series-notes/
    # へ退避、それ以外(template-example.html 等のビルド入力)は
    # assets/<stem>/_root/ へ——展開時にシリーズルートへ symlink される
    for f in sorted(series_dir.iterdir()):
        if not f.is_file():
            continue
        if f.name.lower().startswith("readme"):
            dest = NEW_ROOT / "docs" / "series-notes" / f"{stem}-{f.name}"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
            report(f"シリーズ直下のREADMEを docs/series-notes/ へ退避: {rel}/{f.name}")
        else:
            dest = NEW_ROOT / "articles" / "assets" / stem / "_root" / f.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
            report(f"シリーズ直下のビルド入力を assets/{stem}/_root/ へ: {rel}/{f.name}")

    n_articles = len(sections)
    print(f"  {n_articles} 記事 / 資産 {sum(1 for k, _, _ in asset_jobs if k == 'asset')} 件")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", required=True, help="旧リポジトリのルート")
    ap.add_argument("--series", help="1シリーズだけ変換(例: blog)")
    ap.add_argument("--force", action="store_true", help="既存シリーズファイルを上書き")
    args = ap.parse_args()

    src_root = Path(args.src).resolve()
    names = list(OLD_LAYOUT)
    if args.series:
        names = [n for n in names if n.startswith(args.series)]
        if not names:
            raise SystemExit(f"--series {args.series} に該当するシリーズがありません")

    for name in names:
        convert_series(src_root, name, args.force)

    report_file = NEW_ROOT / "conversion-report.txt"
    report_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"\n変換レポート: {report_file} ({len(report_lines)} 件)")


if __name__ == "__main__":
    main()
