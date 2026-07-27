#!/usr/bin/env python3
"""Initialize a sample static site in the target directory.

Copies the default scaffold (articles, html, tools/templates, CLAUDE.md,
README.md) from tools/scaffolds/default/ into the target directory so that a
fresh site is immediately buildable with:

    python3 tools/build_article.py --site <target> --all
    python3 tools/serve.py --site <target>

Usage:
    python3 tools/init_site.py /path/to/new-site
    python3 tools/init_site.py .                     # current dir
    python3 tools/init_site.py --force <existing>    # overwrite existing files
    python3 tools/init_site.py --list                # show what would be copied
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SCAFFOLD_ROOT = Path(__file__).resolve().parent / "scaffolds"
DEFAULT_SCAFFOLD = "default"


def available_scaffolds() -> list[str]:
    if not SCAFFOLD_ROOT.exists():
        return []
    return sorted(p.name for p in SCAFFOLD_ROOT.iterdir() if p.is_dir())


def iter_scaffold_files(scaffold_dir: Path):
    """Yield (source, relative) for each file under scaffold_dir."""
    for src in scaffold_dir.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(scaffold_dir)
        yield src, rel


def init_site(target: Path, scaffold: str = DEFAULT_SCAFFOLD, *, force: bool = False,
              dry_run: bool = False) -> int:
    """Copy scaffold files into target. Returns number of files written."""
    scaffold_dir = SCAFFOLD_ROOT / scaffold
    if not scaffold_dir.is_dir():
        choices = ", ".join(available_scaffolds()) or "(none)"
        raise SystemExit(
            f"Unknown scaffold '{scaffold}'. Available: {choices}"
        )

    target = target.resolve()
    target.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped: list[Path] = []
    for src, rel in iter_scaffold_files(scaffold_dir):
        dest = target / rel
        if dest.exists() and not force:
            skipped.append(rel)
            continue
        if dry_run:
            print(f"  would write {rel}")
            written += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  + {rel}")
        written += 1

    if skipped:
        print(
            f"\n{len(skipped)} existing file(s) skipped (re-run with --force to overwrite):",
            file=sys.stderr,
        )
        for rel in skipped:
            print(f"  · {rel}", file=sys.stderr)

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", nargs="?", help="Target directory (pass '.' for cwd).")
    parser.add_argument("--scaffold", default=DEFAULT_SCAFFOLD,
                        help=f"Scaffold template name (default: {DEFAULT_SCAFFOLD}).")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite files that already exist in the target.")
    parser.add_argument("--dry-run", action="store_true",
                        help="List what would be written without touching the filesystem.")
    parser.add_argument("--list", action="store_true",
                        help="List available scaffolds and exit.")
    args = parser.parse_args()

    if args.list:
        for name in available_scaffolds():
            print(name)
        return

    if not args.target:
        parser.error("target directory is required (pass '.' for cwd)")

    target = Path(args.target)
    print(f"Initializing site in {target.resolve()} (scaffold: {args.scaffold})")
    count = init_site(target, scaffold=args.scaffold, force=args.force, dry_run=args.dry_run)
    verb = "would write" if args.dry_run else "wrote"
    print(f"\n{verb} {count} file(s).")
    if not args.dry_run and count:
        print(
            "\nNext steps:\n"
            f"  pip install jinja2 markdown-it-py Pillow watchdog\n"
            f"  python3 {Path(__file__).parent / 'build_article.py'} --site {target} --all\n"
            f"  python3 {Path(__file__).parent / 'serve.py'} --site {target}"
        )


if __name__ == "__main__":
    main()
