"""名刺 PDF を ReportLab で生成する.

card-data.json から名前・肩書などを読み、日本の標準名刺サイズ
(91mm × 55mm) の PDF を 2 種類書き出す:

- `out/business-card-python.pdf`    ── 1 ページ 1 枚 (画面確認用)
- `out/business-card-sheet-python.pdf` ── A4 に 10 枚タイル
                                          (家庭プリンタで印刷 → カット)

日本語は ReportLab 内蔵の CID フォント (HeiseiKakuGo-W5 / HeiseiMin-W3)
を使うので、外部フォントファイル不要。"""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

# ── 規格 ──
CARD_W = 91 * mm
CARD_H = 55 * mm

# A4 上の 10 枚配置 (Elecom MT-JM 系などの標準レイアウト)
SHEET_MARGIN_LEFT = 14 * mm
SHEET_MARGIN_TOP = 11 * mm
COLS = 2
ROWS = 5

# ── 色 ──
ACCENT = HexColor("#c8442a")  # aiseed.dev 朱色
INK = HexColor("#1a1a1a")
WHISPER = HexColor("#6b665a")


def _register_fonts() -> None:
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))


def _draw_card(c: canvas.Canvas, data: dict, x: float, y: float) -> None:
    """カード 1 枚を (x, y) = 左下原点で描画."""
    margin = 8 * mm

    # 名前 (JA, 明朝・大)
    c.setFillColor(INK)
    c.setFont("HeiseiMin-W3", 14)
    c.drawString(x + margin, y + CARD_H - margin - 14 * 0.85, data["name_ja"])

    # Name (EN, helvetica・小)
    c.setFillColor(WHISPER)
    c.setFont("Helvetica", 9)
    c.drawString(x + margin, y + CARD_H - margin - 14 * 0.85 - 12, data["name_en"])

    # 肩書 (JA · EN)
    c.setFillColor(ACCENT)
    c.setFont("HeiseiKakuGo-W5", 9)
    c.drawString(
        x + margin,
        y + CARD_H - margin - 14 * 0.85 - 12 - 16,
        f"{data['title_ja']}  ·  {data['title_en']}",
    )

    # アクセント線
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.6)
    c.line(x + margin, y + 18 * mm, x + margin + 16 * mm, y + 18 * mm)

    # 連絡先
    c.setFillColor(INK)
    c.setFont("Helvetica", 9)
    c.drawString(x + margin, y + 12 * mm, data["email"])
    c.setFillColor(WHISPER)
    c.drawString(x + margin, y + 7 * mm, data["url"])


def make_single(data: dict, out_path: Path) -> None:
    """1 枚 / 1 ページの PDF."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path), pagesize=(CARD_W, CARD_H))
    _draw_card(c, data, 0, 0)
    c.showPage()
    c.save()


def make_sheet_a4(data: dict, out_path: Path) -> None:
    """A4 に 10 枚タイル."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path), pagesize=A4)
    sheet_w, sheet_h = A4
    for col in range(COLS):
        for row in range(ROWS):
            x = SHEET_MARGIN_LEFT + col * CARD_W
            # y は上から下に並べる
            y = sheet_h - SHEET_MARGIN_TOP - (row + 1) * CARD_H
            _draw_card(c, data, x, y)

            # カット用の薄いガイド線 (印刷後にカッターで切る目印)
            c.setStrokeColor(HexColor("#cccccc"))
            c.setLineWidth(0.2)
            c.rect(x, y, CARD_W, CARD_H, stroke=1, fill=0)

    c.showPage()
    c.save()


def main() -> None:
    here = Path(__file__).parent
    data = json.loads((here / "card-data.json").read_text(encoding="utf-8"))
    _register_fonts()

    single = here / "out" / "business-card-python.pdf"
    sheet = here / "out" / "business-card-sheet-python.pdf"
    make_single(data, single)
    make_sheet_a4(data, sheet)
    print(f"  wrote {single.relative_to(here)}")
    print(f"  wrote {sheet.relative_to(here)}")


if __name__ == "__main__":
    main()
