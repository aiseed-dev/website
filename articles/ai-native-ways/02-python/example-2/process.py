#!/usr/bin/env python3
"""100 枚の写真に対して 3 つの処理を一括で行う:

1. リサイズ(長辺 1200px)
2. サムネイル(200x200, 中央クロップ)
3. 透かし(右下に "© aiseed.dev 2026" 半透明)

並列実行(プロセスプール)で速度も計測。
"""
from __future__ import annotations

import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).parent
SRC = HERE / "src"
OUT = HERE / "out"
DIR_RESIZED = OUT / "resized"
DIR_THUMBS = OUT / "thumbs"
DIR_WATERMARKED = OUT / "watermarked"

WATERMARK = "© aiseed.dev 2026"


def process_one(src_path: Path) -> tuple[int, int, int]:
    img = Image.open(src_path)

    # 1. リサイズ(長辺 1200px)
    resized = img.copy()
    resized.thumbnail((1200, 1200))
    rp = DIR_RESIZED / src_path.name
    resized.save(rp, "JPEG", quality=85, optimize=True)
    s_resized = rp.stat().st_size

    # 2. サムネイル(200x200, ImageOps.fit で中央クロップ)
    thumb = ImageOps.fit(img, (200, 200), Image.Resampling.LANCZOS)
    tp = DIR_THUMBS / src_path.name
    thumb.save(tp, "JPEG", quality=80, optimize=True)
    s_thumb = tp.stat().st_size

    # 3. 透かし
    wm = resized.copy().convert("RGBA")
    overlay = Image.new("RGBA", wm.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except Exception:
        font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), WATERMARK, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 16
    pos = (wm.width - tw - pad, wm.height - th - pad - 6)
    d.rectangle(
        [pos[0] - 8, pos[1] - 6, pos[0] + tw + 8, pos[1] + th + 6],
        fill=(0, 0, 0, 140),
    )
    d.text(pos, WATERMARK, fill=(255, 255, 255, 220), font=font)
    wmd = Image.alpha_composite(wm, overlay).convert("RGB")
    wp = DIR_WATERMARKED / src_path.name
    wmd.save(wp, "JPEG", quality=85, optimize=True)
    s_wm = wp.stat().st_size

    return s_resized, s_thumb, s_wm


def main():
    for d in (DIR_RESIZED, DIR_THUMBS, DIR_WATERMARKED):
        d.mkdir(parents=True, exist_ok=True)

    files = sorted(SRC.glob("*.jpg"))
    src_total = sum(p.stat().st_size for p in files)

    t0 = time.perf_counter()
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(process_one, files))
    elapsed = time.perf_counter() - t0

    s_resized = sum(r[0] for r in results)
    s_thumb = sum(r[1] for r in results)
    s_wm = sum(r[2] for r in results)

    def mb(n): return f"{n/1024/1024:.1f} MB"
    print(f"\n=== 一括処理結果 ===")
    print(f"  入力          : {len(files)} 枚 / {mb(src_total)}")
    print(f"  リサイズ後    : {len(files)} 枚 / {mb(s_resized)}")
    print(f"  サムネイル    : {len(files)} 枚 / {mb(s_thumb)}")
    print(f"  透かし入り    : {len(files)} 枚 / {mb(s_wm)}")
    print(f"  並列処理時間  : {elapsed:.2f} 秒")
    print(f"  1 枚あたり    : {elapsed/len(files)*1000:.1f} ms")


if __name__ == "__main__":
    main()
