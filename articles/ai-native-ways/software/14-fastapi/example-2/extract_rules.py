#!/usr/bin/env python3
"""既存の Java / C# コードから「業務ルール」を Markdown に抽出する。

抽出対象:
  - 定数(`final` / `const` / `static readonly`)── 閾値・上限・税率
  - JavaDoc / DocString コメント
  - if/else 分岐の条件(主要な業務判定)

これは「コードに業務知識が埋まっている、それを Markdown に出す」を
形にする最小ツール。実プロジェクトでは Claude にコードを渡して
詳細を補ってもらうが、まず機械抽出できる部分を集める。
"""
from __future__ import annotations

import re
import time
from pathlib import Path

HERE = Path(__file__).parent
LEGACY = HERE / "legacy"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


# 定数定義のパターン
JAVA_CONST = re.compile(
    r"(?:private|public|protected)?\s+static\s+final\s+\w+\s+(\w+)\s*=\s*([^;]+);"
)
CSHARP_CONST = re.compile(
    r"(?:private|public|protected)?\s+(?:const|static\s+readonly)\s+\w+\s+(\w+)\s*=\s*([^;]+);"
)

# 行コメント
LINE_COMMENT = re.compile(r"^\s*//\s*(.+)$")

# JavaDoc / C# XML コメント (/** ... */ or /// ...)
DOC_BLOCK = re.compile(r"/\*\*(.*?)\*/", re.DOTALL)


def extract_constants(text: str, lang: str) -> list[tuple[str, str, str]]:
    """(name, value, comment) を返す。コメントは直前の行コメント。"""
    pattern = JAVA_CONST if lang == "java" else CSHARP_CONST
    rules = []
    lines = text.splitlines()
    pending_comment = []
    for i, line in enumerate(lines):
        m = LINE_COMMENT.match(line)
        if m:
            pending_comment.append(m.group(1).strip())
            continue
        # 定数の宣言
        m2 = pattern.search(line)
        if m2:
            name, value = m2.group(1), m2.group(2).strip()
            comment = " / ".join(pending_comment) if pending_comment else ""
            rules.append((name, value, comment))
            pending_comment = []
        elif line.strip() and not line.strip().startswith("/*"):
            pending_comment = []
    return rules


def extract_docblocks(text: str) -> list[str]:
    """/** ... */ 形式のブロックコメントを抽出。"""
    blocks = []
    for m in DOC_BLOCK.finditer(text):
        body = m.group(1)
        # * を除去
        cleaned = re.sub(r"^\s*\*\s?", "", body, flags=re.MULTILINE).strip()
        if cleaned:
            blocks.append(cleaned)
    return blocks


def main():
    files = sorted(LEGACY.iterdir())
    out_md = ["# 抽出された業務ルール\n",
              "下記は `legacy/` のコードから機械抽出したもの。",
              "コードの定数・コメント・JavaDoc から業務ルールを取り出している。",
              "**実際の運用では、これを Claude に渡して詳細補完するのが第 2 段階**。\n"]

    t0 = time.perf_counter()
    total_consts = 0
    for f in files:
        text = f.read_text()
        lang = "java" if f.suffix == ".java" else "csharp"
        consts = extract_constants(text, lang)
        docs = extract_docblocks(text)
        total_consts += len(consts)

        out_md.append(f"\n## `{f.name}` から抽出\n")

        if consts:
            out_md.append("### 定数(閾値・上限・税率など)\n")
            out_md.append("| 名前 | 値 | 業務上の意味(コメント由来) |")
            out_md.append("|------|-----|---------------------------|")
            for name, value, comment in consts:
                v = value.replace("|", "\\|")
                c = comment.replace("|", "\\|") if comment else "(コメントなし)"
                out_md.append(f"| `{name}` | `{v}` | {c} |")
            out_md.append("")

        if docs:
            out_md.append("### JavaDoc / DocString からの仕様\n")
            for d in docs:
                # 先頭の Returns / Parameters は省略
                short = d.split("\n\n")[0]
                out_md.append("> " + short.replace("\n", "  \n> "))
                out_md.append("")

    elapsed = time.perf_counter() - t0
    out_md.append("\n---\n")
    out_md.append(f"**抽出時間**: {elapsed*1000:.1f} ms")
    out_md.append(f"**抽出した定数**: {total_consts} 個")
    out_md.append(f"**処理ファイル**: {len(files)} 個")

    output = OUT / "RULES.md"
    output.write_text("\n".join(out_md))

    print(f"\n=== 業務ルール抽出 ===")
    print(f"  処理ファイル : {len(files)} 個")
    print(f"  抽出した定数 : {total_consts} 個")
    print(f"  抽出時間     : {elapsed*1000:.1f} ms")
    print(f"  → {output}")


if __name__ == "__main__":
    main()
