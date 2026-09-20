#!/usr/bin/env python3
"""新連載「AI ネイティブなソフトウェア開発」の HTML を作る。

置く場所と使い方:

    website/tools/build_new_series.py   に置いて
    python3 tools/build_new_series.py   と走らせる

先に、足りない物が無いかを調べて、名指しで知らせる。揃っていれば
tools/build_article.py --all を走らせて、できた頁を数えて出す。

どこに置いても動く(website の中であれば、上へ遡ってリポジトリを探す)。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SERIES_FILE = "ai-native-software.adoc"
URL_BASE = "/ai-native-software"


def find_repo() -> Path | None:
    """website のルートを探す。このファイルの位置から上へ遡る。"""
    for start in (Path(__file__).resolve().parent, Path.cwd().resolve()):
        for d in (start, *start.parents):
            if (d / "tools" / "build_article.py").is_file() and (d / "articles").is_dir():
                return d
    return None


def check(repo: Path) -> list[str]:
    """足りない物を並べて返す。空なら準備ができている。"""
    missing: list[str] = []

    adoc = repo / "articles" / SERIES_FILE
    if not adoc.is_file():
        missing.append(
            f"articles/{SERIES_FILE} がありません。\n"
            f"    受け取った {SERIES_FILE} を {repo / 'articles'} に置いてください。"
        )

    sjson = repo / "site.json"
    if not sjson.is_file():
        missing.append("site.json がありません。リポジトリの直下に置いてください。")
    else:
        try:
            cfg = json.loads(sjson.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            missing.append(f"site.json が壊れています: {exc}")
        else:
            series = cfg.get("builder", {}).get("series", []) or []
            if not any(s.get("file") == SERIES_FILE for s in series):
                missing.append(
                    "site.json に連載の登録がありません。\n"
                    "    builder.series の先頭に、次の行を足してください。\n"
                    '    {"file": "ai-native-software.adoc", '
                    '"label": "AI ネイティブなソフトウェア開発", '
                    '"url_base": "/ai-native-software"},\n'
                    "    (受け取った site.json をそのまま置き換えても構いません)"
                )

    try:
        import pyasciidoc  # noqa: F401
    except ImportError:
        missing.append(
            ".adoc を読む pyasciidoc が入っていません。\n"
            "    pip install pyasciidoc"
        )

    return missing


def build(repo: Path) -> int:
    """サイト全体をビルドする。build_article.py の終了コードを返す。"""
    cmd = [sys.executable, str(repo / "tools" / "build_article.py"), "--all"]
    print(f"$ {' '.join(cmd)}\n")
    return subprocess.run(cmd, cwd=repo).returncode


def report(repo: Path) -> None:
    """できた頁を数えて出す。"""
    for label, rel in (("日本語", "html/ai-native-software"),
                       ("英語", "html/en/ai-native-software")):
        d = repo / rel
        if not d.is_dir():
            print(f"  {label}: できていません({rel} がありません)")
            continue
        pages = sorted(p.parent.name for p in d.glob("*/index.html"))
        index = "あり" if (d / "index.html").is_file() else "なし"
        print(f"  {label}: 索引 {index}、章 {len(pages)} 頁")


def main() -> int:
    repo = find_repo()
    if repo is None:
        print("website のリポジトリが見つかりません。")
        print("website の中でこのファイルを走らせてください。")
        return 1
    print(f"リポジトリ: {repo}\n")

    missing = check(repo)
    if missing:
        print("足りない物があります。\n")
        for i, m in enumerate(missing, 1):
            print(f"  {i}. {m}\n")
        print("直してから、もう一度このファイルを走らせてください。")
        return 1

    print("準備はできています。ビルドします。\n")
    code = build(repo)
    if code != 0:
        print(f"\nビルドが失敗しました(終了コード {code})。上の出力を見てください。")
        return code

    print("\nできた頁:")
    report(repo)
    print(f"\n手元で見るには、プレビューを立ててから開いてください。")
    print(f"  python3 tools/serve.py --port 8000")
    print(f"  http://localhost:8000{URL_BASE}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
