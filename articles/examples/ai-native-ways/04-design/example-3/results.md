# 実測値

## 環境

- OS: Linux 6.18.5 (x86_64)
- Python: 3.11.15
- reportlab: 4.5.1
- weasyprint: 68.1

## 生成物の寸法 (pypdf で検証)

| ファイル | ページ | 寸法 (pt) | 寸法 (mm) |
|---|---|---|---|
| `out/business-card-python.pdf` | 1 | 258.0 × 155.9 | **91.0 × 55.0** (日本標準名刺) |
| `out/business-card-html.pdf` | 1 | 258.0 × 155.9 | **91.0 × 55.0** (日本標準名刺) |
| `out/business-card-sheet-python.pdf` | 1 | 595.3 × 841.9 | **210.0 × 297.0** (A4 横) |
| `out/business-card-sheet-html.pdf` | 1 | 595.3 × 841.9 | **210.0 × 297.0** (A4 横) |

両経路で寸法が完全一致 ── 同じ印刷物が、Python からも HTML からも出る。

## ファイルサイズ

| ファイル | サイズ |
|---|---|
| `out/business-card-python.pdf` | 4,077 bytes (4.0 KiB) |
| `out/business-card-sheet-python.pdf` | 4,646 bytes (4.5 KiB) |
| `out/business-card-html.pdf` | 9,476 bytes (9.3 KiB) |
| `out/business-card-sheet-html.pdf` | 10,819 bytes (10.6 KiB) |

ReportLab 版が約 2 倍軽い。これは ReportLab が CID フォントで日本語を扱い、
PDF 内部にグリフを埋め込まないため。WeasyPrint は (使用したグリフだけだが)
フォントを PDF に埋め込むため少し重くなる。

入稿サービスに渡す場合は **HTML 経路 (フォント埋め込み)** の方が確実
(印刷側のフォント環境に依存しない)。社内で配るだけなら **Python 経路 (軽い)**
で十分。

## 生成時間 (参考)

```
$ time make all
```

それぞれの所要時間は環境による (ホスト性能・初回フォントキャッシュ等) が、
両経路とも **1 秒未満〜数秒** で完了する。Illustrator を起動して 1 枚作る
時間 (数分) と比較するとほぼ瞬時。

## デザインの精度確認

両 PDF を Acrobat / Preview / Evince で開いて目視確認:

- 氏名 (明朝 14pt) ── 鮮明
- 肩書 (朱色 `#c8442a`) ── 色が正しく出ている
- 朱色罫線 ── 0.6pt の細線が出ている
- 連絡先 (Helvetica 9pt) ── 鮮明

WeasyPrint 版でシステムフォントが見つからない場合、フォールバックで
DejaVu / Liberation 系になることがあるが、Noto CJK が入っている環境では
意図通りの明朝・ゴシックで描画される。

## 印刷との関係

- **家庭用プリンタ + A4 普通紙**: `business-card-sheet-*.pdf` を A4 で
  印刷 → カッターで切る。10 枚で約 30 秒。
- **市販の名刺用紙 (Elecom MT-JM 等)**: 同上、上下マージン 11mm /
  左右マージン 14mm が一致するように設計してある。
- **入稿 (印刷会社)**: `business-card-{python,html}.pdf` (1 枚版) を
  そのまま渡せる場合が多い。ドブ (塗り足し) や CMYK 要件は印刷会社の
  仕様に合わせて Python 側で再生成すれば良い。
