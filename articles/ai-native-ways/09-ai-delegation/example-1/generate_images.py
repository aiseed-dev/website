#!/usr/bin/env python3
"""1,000 枚のサンプル画像 (PNG) を生成する。

各画像は 1200×800 のカラフルなグラデーション。AI 利用料ゼロでサイズ計測の
入力にする。
"""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

OUT = Path(__file__).parent / "src"
OUT.mkdir(exist_ok=True)

W, H = 1200, 800


def png_gradient(seed: int) -> bytes:
    """seed をシードに、シンプルな水平グラデーション PNG を返す。"""
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter byte (None)
        for x in range(W):
            r = (x * 255 // W + seed) % 256
            g = (y * 255 // H + seed * 3) % 256
            b = ((x + y) * 128 // (W + H) + seed * 7) % 256
            raw.extend([r, g, b])

    def chunk(name: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + name + data
            + struct.pack(">I", zlib.crc32(name + data) & 0xffffffff)
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)  # 8-bit RGB
    idat = zlib.compress(bytes(raw), 6)
    iend = b""
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", iend)


def main():
    n = 1000
    for i in range(n):
        path = OUT / f"img_{i:04d}.png"
        path.write_bytes(png_gradient(i))
    files = list(OUT.glob("*.png"))
    total = sum(p.stat().st_size for p in files)
    print(f"  生成完了: {len(files)} ファイル / 合計 {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
