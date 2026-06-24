#!/usr/bin/env python3
"""サンプル写真ファイル(EXIF 付き JPEG)を 50 枚生成する。

撮影日を 6 ヶ月分(2026-01〜2026-06)にバラし、photo_organizer.py で
正しく月別フォルダに振り分けられるかを確認するための入力。
"""
from __future__ import annotations

import os
import random
import struct
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path

random.seed(42)

# 1x1 ピクセルの最小 JPEG(色は無関係)
_MIN_JPEG = bytes.fromhex(
    "ffd8ffe000104a46494600010100000100010000ffdb004300080606070605080707"
    "070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c"
    "1c2837292c30313434341f27393d38323c2e333432ffdb0043010909090c0b0c180d"
    "0d1832211c213232323232323232323232323232323232323232323232323232323232"
    "32323232323232323232323232323232323232323232323232ffc00011080001000103"
    "012200021101031101ffc4001f0000010501010101010100000000000000000102030"
    "405060708090a0bffc400b5100002010303020403050504040000017d010203000411"
    "05122131410613516107227114328191a1082342b1c11552d1f02433627282090a161"
    "718191a25262728292a3435363738393a434445464748494a535455565758595a6364"
    "65666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5"
    "a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2"
    "e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffc4001f01000301010101010101010101"
    "0000000000000102030405060708090a0bffc400b51100020102040403040705040400"
    "010277000102031104052131061241510761711322328108144291a1b1c109233352f0"
    "156272d10a162434e125f11718191a262728292a35363738393a434445464748494a53"
    "5455565758595a636465666768696a737475767778797a82838485868788898a929394"
    "95969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3"
    "d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9faffda000c03010002110"
    "3110000003f00fbfcffd9"
)


def jpeg_with_exif(dt: datetime) -> bytes:
    """1x1 JPEG に EXIF DateTimeOriginal を埋め込む。"""
    s = dt.strftime("%Y:%m:%d %H:%M:%S\x00").encode()
    # 最小 TIFF + IFD0 (1 entry: ExifIFDPointer) + ExifIFD (1 entry: DateTimeOriginal)
    bo = b"II"  # little-endian
    tiff = bytearray()
    tiff += bo + struct.pack("<HI", 0x002a, 8)  # TIFF header
    # IFD0: 1 entry
    tiff += struct.pack("<H", 1)
    # tag=0x8769 (ExifIFDPointer), type=4 (LONG), count=1, value = offset to next IFD
    ifd0_end = 2 + 12 + 4  # entry count + 12-byte entry + 4-byte next-IFD offset
    exif_ifd_off = 8 + ifd0_end
    tiff += struct.pack("<HHII", 0x8769, 4, 1, exif_ifd_off)
    # next IFD offset = 0
    tiff += struct.pack("<I", 0)
    # ExifIFD: 1 entry (DateTimeOriginal, ASCII length 20)
    tiff += struct.pack("<H", 1)
    val_off = exif_ifd_off + 2 + 12 + 4
    tiff += struct.pack("<HHII", 0x9003, 2, 20, val_off)
    tiff += struct.pack("<I", 0)  # next IFD = 0
    tiff += s

    exif_data = b"Exif\x00\x00" + bytes(tiff)
    app1 = b"\xff\xe1" + struct.pack(">H", len(exif_data) + 2) + exif_data
    return _MIN_JPEG[:2] + app1 + _MIN_JPEG[2:]


def main():
    out = Path(__file__).parent / "photos"
    out.mkdir(exist_ok=True)
    start = datetime(2026, 1, 1, 9, 0, 0)
    for n in range(50):
        days = random.randint(0, 180)  # ~6 months
        dt = start + timedelta(days=days, hours=random.randint(0, 23))
        path = out / f"IMG_{n:04d}.jpg"
        path.write_bytes(jpeg_with_exif(dt))
        # mtime も合わせておく
        ts = dt.timestamp()
        os.utime(path, (ts, ts))
    print(f"  {len(list(out.glob('*.jpg')))} 枚のサンプル JPEG を生成 ({out})")


if __name__ == "__main__":
    main()
