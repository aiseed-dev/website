"""`cf-publish` CLI エントリポイント。"""

from __future__ import annotations

import argparse
import sys

from .pages import PagesError, deploy


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="cf-publish",
        description="Cloudflare Pages へフォルダを直接アップロードする（wrangler/npm 不要）",
    )
    ap.add_argument("directory", help="公開ディレクトリ（この中身がサイトになる）")
    ap.add_argument("--project", required=True, help="Pages プロジェクト名")
    ap.add_argument("--branch", default="main",
                    help="main = 本番、それ以外はプレビュー URL")
    ap.add_argument("--no-create", action="store_true",
                    help="プロジェクトがないときに作らずエラーにする")
    args = ap.parse_args(argv)

    try:
        url = deploy(
            args.directory,
            args.project,
            branch=args.branch,
            create=not args.no_create,
            on_progress=lambda m: print(m, flush=True),
        )
    except PagesError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
