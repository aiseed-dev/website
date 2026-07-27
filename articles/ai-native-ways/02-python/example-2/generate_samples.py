#!/usr/bin/env python3
"""サンプル写真ファイル(JPEG)を 100 枚生成する。各枚 1920x1280。

簡単なグラデーション + 番号入りで、後段の処理(リサイズ・サムネイル・
透かし)が効いているか目で見て確認できるようにする。
"""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

random.seed(42)
OUT = Path(__file__).parent / "src"
OUT.mkdir(exist_ok=True)

W, H = 1920, 1280


def make_image(n: int) -> Image.Image:
    img = Image.new("RGB", (W, H), (200, 200, 200))
    px = img.load()
    for y in range(H):
        r = (y * 255) // H
        for x in range(W):
            g = (x * 255) // W
            b = ((n * 13) + 64) % 256
            px[x, y] = (r, g, b)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 200)
    except Exception:
        font = ImageFont.load_default()
    d.text((80, 80), f"#{n:03d}", fill=(255, 255, 255), font=font)
    return img


def main():
    for n in range(100):
        img = make_image(n)
        img.save(OUT / f"img_{n:03d}.jpg", "JPEG", quality=92)
    files = sorted(OUT.glob("*.jpg"))
    total = sum(p.stat().st_size for p in files)
    print(f"  生成完了: {len(files)} 枚 / 合計 {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
