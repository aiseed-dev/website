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

import argparse
import json
import os
import subprocess
import sys
import time
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


def add_site_json_entry(sjson: Path) -> None:
    """site.json に連載の登録が無ければ、先頭に足す。

    .adoc を置いただけでは、ビルドは連載の存在を知らない。登録は
    builder.series の1行で、URL と表示名と編の見出しを決める。
    """
    import collections

    cfg = json.loads(sjson.read_text(encoding="utf-8"),
                     object_pairs_hook=collections.OrderedDict)
    entry = collections.OrderedDict([
        ("file", SERIES_FILE),
        ("label", "AI ネイティブなソフトウェア開発"),
        ("label_en", "AI-Native Software Development"),
        ("url_base", URL_BASE),
        ("subtitle", "SIer に頼まない ── 自分で立てて、自分で動かす"),
        ("subtitle_en",
         "Don't commission an SIer — stand it up yourself, and run it yourself"),
        ("parts", [
            collections.OrderedDict([
                ("key", "1"), ("name_ja", "導入編 ── なぜ変わるのか"),
                ("name_en", "Introduction — what changed")]),
            collections.OrderedDict([
                ("key", "2"),
                ("name_ja", "自立編 ── AI に読ませて、そのとおりに立てる"),
                ("name_en", "Independence — a specification the AI can execute")]),
            collections.OrderedDict([
                ("key", "3"), ("name_ja", "転換編 ── なぜ産業構造が変わるのか"),
                ("name_en", "Shift — why the industry structure changes")]),
        ]),
    ])
    cfg.setdefault("builder", collections.OrderedDict())
    cfg["builder"].setdefault("series", [])
    cfg["builder"]["series"].insert(0, entry)
    sjson.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")
    print(f"site.json に連載の登録を足しました({URL_BASE})\n")


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
                add_site_json_entry(sjson)

    try:
        import pyasciidoc  # noqa: F401
    except ImportError:
        missing.append(
            ".adoc を読む pyasciidoc が入っていません。\n"
            "    pip install pyasciidoc"
        )

    return missing


def preview_running() -> list[str]:
    """走っているプレビューサーバー(tools/serve.py)の PID を返す。

    serve.py はファイルの変更を見張って自動でビルドし直す。手動のビルドと
    重なると、両方が .build/ を消して作り直すので、片方のファイルが途中で
    消えて FileNotFoundError になる。だから先に調べる。
    """
    try:
        out = subprocess.run(
            ["pgrep", "-f", "serve.py"],
            capture_output=True, text=True, check=False,
        ).stdout
    except FileNotFoundError:
        return []          # pgrep が無い環境では調べない
    me = str(os.getpid())
    return [pid for pid in out.split() if pid != me]


def wait_for_build_root(repo: Path, seconds: int = 30) -> bool:
    """.build/ の作り直しが落ち着くまで待つ。落ち着けば True。"""
    build_root = repo / ".build"
    last, stable = None, 0
    for _ in range(seconds * 2):
        now = sum(1 for _ in build_root.rglob("*")) if build_root.is_dir() else -1
        stable = stable + 1 if now == last else 0
        if stable >= 4:        # 2 秒変わらなければ落ち着いたとみなす
            return True
        last = now
        time.sleep(0.5)
    return False


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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="プレビューサーバーが走っていてもビルドする")
    args = ap.parse_args()

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

    pids = preview_running()
    if pids:
        print(f"プレビューサーバーが走っています(PID {', '.join(pids)})。")
        print("このサーバーもファイルの変更でビルドし直します。重なると"
              ".build/ を取り合って落ちるので、落ち着くまで待ちます。")
        if wait_for_build_root(repo):
            print("落ち着きました。\n")
        else:
            print("まだ動いています。止めてからやり直すほうが確実です。")
            print(f"  kill {' '.join(pids)}\n")

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
