"""canon-search CLI。

  canon-search add rfc 9110
  canon-search add law 著作権法
  canon-search add pdf <URL> --title "..." --key "..."
  canon-search search "軽微 利用"
  canon-search context "ゼロトラスト" -k 5   # AI に貼るコンテキストを出力
  canon-search list
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from . import fetchers
from .store import Store
from .verify import verify_article

DEFAULT_DB = Path(
    os.environ.get("CANON_DB", Path(__file__).resolve().parents[2] / "data" / "canon.db")
)


def _store() -> Store:
    return Store(DEFAULT_DB)


def cmd_add(args) -> None:
    if args.kind == "rfc":
        doc = fetchers.fetch_rfc(int(args.target))
    elif args.kind == "law":
        doc = fetchers.fetch_law(args.target)
    elif args.kind == "pdf":
        if not (args.title and args.key):
            raise SystemExit("add pdf には --title と --key が必要です")
        doc = fetchers.fetch_pdf(args.target, args.title, args.key, args.license or "")
    elif args.kind == "url":
        doc = fetchers.fetch_url(args.target, args.title or "",
                                 args.key or "", args.license or "")
    else:
        raise SystemExit(f"未知の種別: {args.kind}")
    n = _store().add_doc(doc["source"], doc["doc_key"], doc["title"],
                         doc["url"], doc["license"], doc["chunks"])
    print(f"登録: [{doc['source']}] {doc['title']} — {n} チャンク")


def cmd_search(args) -> None:
    hits = _store().search(args.query, k=args.k)
    if not hits:
        print("該当なし(注: trigram 索引のため3文字未満の語は照合できません)")
        return
    for i, h in enumerate(hits, 1):
        head = f" §{h['heading']}" if h["heading"] else ""
        body = " ".join(h["text"].split())
        print(f"[{i}] {h['title']}{head}  (score {h['score']:.2f})")
        print(f"    {body[:160]}")
        print(f"    {h['url']}")


def cmd_context(args) -> None:
    hits = _store().search(args.query, k=args.k)
    if not hits:
        print("該当なし")
        return
    print(f"## 参考資料(canon-search: {args.query})\n")
    print("以下の一次資料を踏まえて答えてください。\n")
    for i, h in enumerate(hits, 1):
        head = f" — {h['heading']}" if h["heading"] else ""
        print(f"### [{i}] {h['title']}{head}")
        print(f"出典: {h['url']}\n")
        print(h["text"])
        print()


def cmd_ask(args) -> None:
    """記事生成のための grounding pack を出力する。

    各チャンクに [n] を振る。この n が引用ID。生成AIには『この pack の
    範囲だけで書き、各文末に根拠チャンクの [n] を付けよ』と指示する。
    checkcite が同じ query/-k で pack を再構成して照合する。
    """
    if args.doc:
        hits = _store().doc_chunks(args.doc)
        header = f"# grounding pack — doc: {args.doc!r}  ({len(hits)} chunks)\n"
    else:
        hits = _store().search(args.query, k=args.k)
        header = f"# grounding pack — query: {args.query!r}  (k={args.k})\n"
    if not hits:
        print("該当なし")
        return
    print(header)
    print("以下の正典の範囲だけで記述し、各文末に根拠の [n] を付けること。")
    print("pack に無い事実は書かないこと。\n")
    for i, h in enumerate(hits, 1):
        head = f" — {h['heading']}" if h["heading"] else ""
        print(f"## [{i}] {h['title']}{head}")
        print(f"出典: {h['url']}")
        print(" ".join(h["text"].split()))
        print()


def cmd_checkcite(args) -> None:
    """草稿(各文末に [n])を、同じ pack と照合して裏取り検証する。"""
    if args.doc:
        hits = _store().doc_chunks(args.doc)
    else:
        hits = _store().search(args.query, k=args.k)
    id_to_text = {i: h["text"] for i, h in enumerate(hits, 1)}
    lines = Path(args.draft).read_text(encoding="utf-8").splitlines()
    results = verify_article(lines, id_to_text, threshold=args.threshold)
    checked = [r for r in results if r["ok"] is not None]
    ok = [r for r in checked if r["ok"]]
    bad = [r for r in checked if not r["ok"]]
    for r in results:
        if r["ok"] is None:
            mark = "·"
        elif r["ok"]:
            mark = "✔"
        else:
            mark = "✘"
        score = "" if r["score"] is None else f" {r['score']:.2f}"
        cite = "" if r["cite"] is None else f" [{r['cite']}]"
        print(f"{mark}{cite}{score}  {r['sentence'][:70]}")
        if r.get("span"):
            print(f"      〔{r['span'][:70]}〕")
        if r["ok"] is False:
            print(f"      → {r['reason']}")
    print(f"\n検証: 裏取りOK {len(ok)} / 要修正 {len(bad)} / 対象外 "
          f"{len(results) - len(checked)}")
    if bad:
        raise SystemExit(1)


def cmd_list(_args) -> None:
    docs = _store().list_docs()
    if not docs:
        print("索引は空です。`canon-search add rfc 9110` などで正典を登録してください。")
        return
    for d in docs:
        print(f"[{d['source']}] {d['doc_key']}  {d['title']}"
              f"  ({d['chunks']} チャンク, {d['fetched_at']})")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="canon-search", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="正典を取得して索引に追加")
    a.add_argument("kind", choices=["rfc", "law", "pdf", "url"])
    a.add_argument("target", help="RFC番号 / 法令名・法令ID / PDF・HTMLのURL")
    a.add_argument("--title")
    a.add_argument("--key")
    a.add_argument("--license")
    a.set_defaults(func=cmd_add)

    s = sub.add_parser("search", help="索引を検索")
    s.add_argument("query")
    s.add_argument("-k", type=int, default=8)
    s.set_defaults(func=cmd_search)

    c = sub.add_parser("context", help="AI に貼るコンテキストブロックを出力")
    c.add_argument("query")
    c.add_argument("-k", type=int, default=5)
    c.set_defaults(func=cmd_context)

    k = sub.add_parser("ask", help="記事生成用の grounding pack を出力")
    k.add_argument("query", nargs="?", default="")
    k.add_argument("-k", type=int, default=5)
    k.add_argument("--doc", help="この文書(doc_key)の全チャンクを pack にする")
    k.set_defaults(func=cmd_ask)

    v = sub.add_parser("checkcite", help="草稿([n]付き)を正典と照合検証")
    v.add_argument("draft", help="検証する草稿ファイル(各文末に [n])")
    v.add_argument("query", nargs="?", default="", help="ask に使ったクエリと同じもの")
    v.add_argument("-k", type=int, default=5)
    v.add_argument("--doc", help="ask --doc と同じ文書 doc_key")
    v.add_argument("--threshold", type=float, default=0.55)
    v.set_defaults(func=cmd_checkcite)

    l = sub.add_parser("list", help="登録済み文書の一覧")
    l.set_defaults(func=cmd_list)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
