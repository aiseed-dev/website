# 計測結果 — 第 08 章 example-1

実行環境: Linux 6.18 / Python 3.x(標準ライブラリのみ)

## 規模と性能(主目的)

| 項目 | 数値 |
|------|------|
| `photo_organizer.py` 行数 | **約 90 行**(EXIF 読み込み込み) |
| 依存 | **標準ライブラリのみ** |
| 処理対象 | 50 枚の JPEG |
| 処理時間 | **0.044 秒** |
| 1 枚あたり | 約 0.9 ms |
| 1,000 枚処理(推定) | 約 0.9 秒 |

## 章本文との比較

| 項目 | iOS アプリ | この CLI |
|------|-----------|---------|
| 開発環境のディスク | Xcode + iOS SDK = 50 GB | **0**(Python が入っていれば終わり) |
| 年会費 | Apple Developer $99 | **0** |
| コード行数 | Swift で約 200 行 + UI | **約 90 行** |
| 配布までの時間 | App Store 審査 1 週間以上 | **GitHub に push して終わり** |
| 動く OS | iOS のみ | **macOS / Windows / Linux** |
| 1 ヶ月後の修正 | 再ビルド + 再審査 | **エディタで直して終わり** |

## 実行ログ(`make all`)

```
=== 撮影日でフォルダ分け ===
  copy  IMG_0001.jpg → by-month/2026-04/IMG_0001.jpg
  copy  IMG_0002.jpg → by-month/2026-02/IMG_0002.jpg
  ...
  50 ファイル処理完了

real    0m0.044s
user    0m0.037s
sys     0m0.008s

=== 結果 ===
  2026-01 : 11 枚
  2026-02 : 8 枚
  2026-03 : 10 枚
  2026-04 : 3 枚
  2026-05 : 5 枚
  2026-06 : 13 枚
  ── 合計 50 枚を 6 フォルダに振り分け
```

## 配布

```bash
# 1. GitHub に push して終わり
git add photo_organizer.py
git commit -m "Photo organizer CLI"
git push
```

ユーザは:

```bash
curl -O https://raw.githubusercontent.com/you/repo/main/photo_organizer.py
python3 photo_organizer.py ~/Pictures -o ~/sorted-photos
```

これで完了。**App Store も Google Play も要らない**。

PyPI に上げるなら:

```bash
# pyproject.toml を 1 個作って
pip install build twine
python3 -m build
twine upload dist/*
```

これで `pip install photo-organizer` で世界中に配布される。

## CLI から GUI に上げる(必要があれば)

CLI で動くものを、`Flet` で 30 行追加するだけで GUI 化できる:

```python
import flet as ft
import photo_organizer

def main(page: ft.Page):
    src = ft.TextField(label="入力")
    dst = ft.TextField(label="出力")
    def run(e): photo_organizer.organize(src.value, dst.value)
    page.add(src, dst, ft.ElevatedButton("整理", on_click=run))

ft.app(target=main)
```

**Flutter で書き直すなら 1 ヶ月、Flet なら 1 時間**。CLI のロジックは
そのまま再利用される。これが章で言う「**CLI を一段ずつ昇格させる**」。

## 再現手順

```bash
# Pillow も python-docx も不要、Python 3 だけ
make clean && make all
```
