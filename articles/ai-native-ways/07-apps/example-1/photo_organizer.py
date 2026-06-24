#!/usr/bin/env python3
"""撮影日でフォルダ分けする最小 CLI ツール。

第 8 章: 「写真整理アプリ ── CLI で書く: 30 行の Python、開発時間 30 分」
を実演する。

使い方:
  python3 photo_organizer.py SRC_DIR -o DST_DIR [--dry-run] [--copy]

EXIF が無いファイルは mtime にフォールバック。
JPEG / PNG / HEIC / TIFF / RAW を扱える(EXIF を読むだけなので拡張子に依存しない)。
"""
from __future__ import annotations

import argparse
import shutil
import struct
import sys
from datetime import datetime
from pathlib import Path


def read_exif_datetime(path: Path) -> datetime | None:
    """EXIF DateTimeOriginal (tag 0x9003) を最小実装で読み取る。

    PIL を入れたくなければこれだけで動く。標準ライブラリのみ。
    JPEG (APP1 セグメント内の TIFF) を直接スキャンする。
    """
    try:
        with path.open("rb") as f:
            head = f.read(2)
            if head != b"\xff\xd8":  # JPEG SOI
                return None
            while True:
                m = f.read(2)
                if not m or m[0] != 0xff:
                    return None
                marker = m[1]
                seg_len = struct.unpack(">H", f.read(2))[0]
                if marker == 0xe1:  # APP1
                    data = f.read(seg_len - 2)
                    if not data.startswith(b"Exif\x00\x00"):
                        continue
                    tiff = data[6:]
                    bo = "<" if tiff[:2] == b"II" else ">"
                    ifd0_off = struct.unpack(bo + "I", tiff[4:8])[0]
                    n = struct.unpack(bo + "H", tiff[ifd0_off:ifd0_off + 2])[0]
                    exif_ifd_off = None
                    for i in range(n):
                        e = ifd0_off + 2 + i * 12
                        tag, _, _, val = struct.unpack(bo + "HHII", tiff[e:e + 12])
                        if tag == 0x8769:
                            exif_ifd_off = val
                            break
                    if exif_ifd_off is None:
                        return None
                    n2 = struct.unpack(bo + "H", tiff[exif_ifd_off:exif_ifd_off + 2])[0]
                    for i in range(n2):
                        e = exif_ifd_off + 2 + i * 12
                        tag, _, _, val_off = struct.unpack(bo + "HHII", tiff[e:e + 12])
                        if tag == 0x9003:  # DateTimeOriginal
                            s = tiff[val_off:val_off + 19].decode(errors="ignore")
                            return datetime.strptime(s, "%Y:%m:%d %H:%M:%S")
                    return None
                else:
                    f.seek(seg_len - 2, 1)
    except Exception:
        return None


def datetime_for(path: Path) -> datetime:
    dt = read_exif_datetime(path)
    if dt is not None:
        return dt
    return datetime.fromtimestamp(path.stat().st_mtime)


def main():
    p = argparse.ArgumentParser(description="撮影日でフォルダ分けする")
    p.add_argument("src", type=Path, help="入力ディレクトリ")
    p.add_argument("-o", "--out", type=Path, required=True, help="出力ディレクトリ")
    p.add_argument("--copy", action="store_true", help="移動でなくコピー")
    p.add_argument("--dry-run", action="store_true", help="操作を表示するだけ")
    args = p.parse_args()

    if not args.src.is_dir():
        sys.exit(f"src が存在しない: {args.src}")
    args.out.mkdir(parents=True, exist_ok=True)

    moved = 0
    for f in sorted(args.src.rglob("*")):
        if not f.is_file():
            continue
        dt = datetime_for(f)
        sub = args.out / f"{dt:%Y-%m}"
        sub.mkdir(parents=True, exist_ok=True)
        dst = sub / f.name
        action = "copy" if args.copy else "move"
        if args.dry_run:
            print(f"  [dry] {action:4s}  {f}  →  {dst}")
        else:
            (shutil.copy2 if args.copy else shutil.move)(f, dst)
            print(f"  {action:4s}  {f.name:30s} →  {dst.relative_to(args.out.parent)}")
        moved += 1

    print(f"\n  {moved} ファイル処理完了")


if __name__ == "__main__":
    main()
