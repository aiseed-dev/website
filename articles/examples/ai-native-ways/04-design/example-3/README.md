# 実例 3 — 名刺を二経路で生成する

第 04 章「デザインをする」の主張 ── **テキストと AI と最小限のスクリプトで
専門ツールに匹敵するものが作れる** ── を、**名刺** という小さな印刷物で実演する。

## 章のどの主張に対応するか

> Word / Illustrator / 専用デザインソフトを開かなくても、テキスト形式の
> ソースから「印刷に出せる体裁」が作れる。AI と相談しながら作るので、
> レイアウトの調整も自然言語で済む。

名刺は印刷物のなかで最も寸法が厳しい (91×55mm、フォント 9pt 前後)。
ここで成立すれば、チラシ・案内状・封筒の宛名印刷など、より大きな
印刷物はすべて同じ枠組みで作れる。

## やること

**1 つの `card-data.json`** から、二つの経路で同じ名刺 PDF を生成する。

```
       card-data.json (氏名・肩書・連絡先)
              │
       ┌──────┴──────┐
       ▼             ▼
  business_card.py   business-card{.html,.css}
  (ReportLab)         (HTML + Print CSS)
       │                   │
       ▼                   ▼
  91×55mm 1枚 PDF      ブラウザで Ctrl+P → PDF
  A4 10枚タイル PDF    (or WeasyPrint で自動)
```

| 経路 | 出力 |
|---|---|
| **A. Python (ReportLab)** | `out/business-card-python.pdf` (1 枚) + `out/business-card-sheet-python.pdf` (A4 × 10 枚) |
| **B. HTML + CSS** | `out/business-card-html.pdf` (1 枚) + `out/business-card-sheet-html.pdf` (A4 × 10 枚) |

`make all` 一発で全 4 PDF が生成される。

## なぜ二経路か

- **A (Python)**: 100 人分の名刺を一括生成する、データベースから動的に作る、
  自動化する ── というスケール用途。コードは 100 行台。
- **B (HTML)**: ブラウザで見た目を即確認できる。CSS の調整が直感的。
  プログラミングを知らない人でもデザインを触れる。本番では Web ブラウザの
  「PDF として保存」で完結する (WeasyPrint はその自動化版)。

**どちらも同じ寸法・同じデザインの PDF を出す** ── これが「テキストから印刷物」の
方法論の核心 (本章「業務資料は構造を保ったまま組み立てる」節)。

## 構成

```
example-3/
├── README.md                     ── このファイル
├── card-data.json                ── 共有データ (氏名・肩書・連絡先)
├── business_card.py              ── 経路 A: ReportLab で PDF を組む
├── business-card.html            ── 経路 B: 1 枚カードの HTML
├── business-card.css             ──         同じ CSS (印刷用)
├── business-card-sheet.html      ──         A4 × 10 枚タイルの HTML
├── business-card-sheet.css       ──         同じ CSS (タイル用)
├── Makefile                      ── make all で両経路を実行
├── results.md                    ── 実測値
└── out/                          ── 生成された PDF
    ├── business-card-python.pdf
    ├── business-card-sheet-python.pdf
    ├── business-card-html.pdf
    └── business-card-sheet-html.pdf
```

## 必要なツール

```bash
pip install reportlab weasyprint
# 任意: Linux で日本語フォントを補強
sudo apt install fonts-noto-cjk
```

ReportLab は内蔵の CID フォント (HeiseiKakuGo-W5 / HeiseiMin-W3) を使うので、
外部フォントなしでも日本語が出る。HTML + CSS 側はシステムの「明朝」「ゴシック」を
フォールバックで呼ぶ (Mac: ヒラギノ / Windows: 游 / Linux: Noto CJK)。

## 使い方

```bash
make all          # 4 つの PDF を一気に生成 + 計測
make python       # 経路 A だけ
make html         # 経路 B だけ
make clean        # out/ をクリア
```

## デザインの中身

- **氏名 (JA, 明朝・14pt)** ── 名刺で一番大きな情報
- **Name (EN, Sans 9pt, グレー)** ── ローマ字併記
- **肩書 (JA · EN, ゴシック 9pt, 朱色 `#c8442a`)** ── aiseed.dev のアクセント
- **朱色の細い罫線** ── 上下を分ける
- **email / URL (Sans 9pt)** ── 連絡先

aiseed.dev の「AI 時代の自由人」「ビルダー」というキーワードを **肩書欄** に
収め、シリーズと整合的なミニマルなデザインにしてある。デザインを変えたい場合は
`business_card.py` の色定数 / 配置値、または `business-card.css` の CSS 変数を
触れば良い。

## 応用

- **100 人分の名刺**: `card-data.json` を `card-data.csv` にして、
  Python ループで全員分を 1 PDF に書き出す (本章「業務資料は構造を保った
  まま組み立てる」節と同じ流儀)
- **両面**: `business_card.py` の `make_single()` を 2 ページ書く形に拡張、
  裏面に QR コード (`pip install qrcode`) を貼る
- **入稿用**: 上下左右 3mm のドブ (bleed) を加えて 97 × 61mm にし、
  トンボを描くオプションを足す
- **ローカライズ**: `card-data.json` を複数置く (`card-data-jp.json` /
  `card-data-en.json`)。引数で切替

これらの拡張は、すべて **同じ枠組みのまま** できる。商用名刺サービスや
Illustrator を開く必要はない。
