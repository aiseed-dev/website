# 実例 1 — 写真を撮影日でフォルダ分けする CLI ツール

第 08 章「アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ」の主張を裏付ける。

## 章のどの主張に対応するか

> 写真整理アプリ(撮影日でフォルダ分け):
> - **CLI で書く**: 30 行の Python、開発時間 30 分、配布は GitHub に置くだけ
> - iOS アプリで作る: Swift で 200 行、Xcode 環境 50 GB、App Store 審査 1 週間、年会費 $99

(章本文「実例: 数字で見る」より)

実際に書いてみると **約 90 行** の Python(EXIF を自前で読む実装込み)。
50 枚を **0.044 秒** で振り分けた。

## やること

1. **入力を作る**: `generate_samples.py` で EXIF 入りの 1×1 JPEG を 50 枚生成
   (撮影日を 2026-01〜2026-06 にバラす)
2. **整理する**: `photo_organizer.py photos -o out/by-month --copy`
3. **検算する**: 結果フォルダのファイル数を月別に表示

すべて `make all` 一発。

## 構成

```
example-1/
├── README.md
├── photo_organizer.py    ── 本体 CLI(EXIF 読み + フォルダ振り分け)
├── generate_samples.py   ── サンプル JPEG 生成(EXIF DateTimeOriginal を埋め込む)
├── Makefile
├── results.md
├── photos/               ── 入力(50 枚の JPEG)
└── out/by-month/
    ├── 2026-01/   ── 11 枚
    ├── 2026-02/   ── 8 枚
    ├── 2026-03/   ── 10 枚
    ├── 2026-04/   ── 3 枚
    ├── 2026-05/   ── 5 枚
    └── 2026-06/   ── 13 枚
```

## 実行

```bash
# 標準ライブラリだけで動く(Pillow 不要)
python3 generate_samples.py
python3 photo_organizer.py photos -o out/by-month --copy

# あるいは
make clean && make all
```

## なぜこれが「実例」になるのか

「撮影日で写真を分ける」── これを Swift / Xcode で iOS アプリとして作ると:

- Xcode + iOS SDK = **約 50 GB** の開発環境
- Apple Developer Program **年会費 $99**
- 200 行の Swift + UI 実装
- App Store 審査 **1 週間以上**
- ユーザは App Store からインストール、iOS 限定

CLI で書くと:

- Python だけ(**Pillow すら不要**、EXIF を 50 行で自前パース)
- ファイル 1 個 (`photo_organizer.py` 約 90 行)
- 配布は GitHub に置くか pip パッケージ
- 即実行可能、Mac / Windows / Linux どこでも動く
- 1,000 枚処理しても **数秒**

しかも、**他のシェルツールと組み合わせられる**:

```bash
# 1 年分のスマホ写真を整理して NAS に同期
python3 photo_organizer.py ~/Pictures/iphone -o /nas/photos

# RAW + JPEG の組み合わせも対応
find . -name "*.CR3" -o -name "*.jpg" | xargs python3 photo_organizer.py ...

# 古い写真を 1 年単位の zip にする
python3 photo_organizer.py photos -o /tmp/sorted
for d in /tmp/sorted/*/; do zip -r "$(basename $d).zip" "$d"; done
```

GUI が要らない処理に GUI を被せると、**他のものと組み合わせるとき
GUI が壁になる**。CLI のままなら、cron に入れて毎晩走らせることもできる。
これが章で言う「**まず CLI から**」の意味。

GUI が必要になったら(Flet で Python のまま GUI 化、それでも足りなければ Flutter)。
ステップを上げる順序がある。

## EXIF を自前で読む

このスクリプトの面白いところは、Pillow を使わずに **EXIF DateTimeOriginal
(tag 0x9003)** を 50 行で読んでいる点。標準ライブラリ `struct` だけで
JPEG → APP1 → TIFF → IFD → ExifIFD を辿る。

「まず Claude にアウトラインを書いてもらって、自分で詰める」── このサイズの
コードはまさに章 04 で言う「**Claude が書く、人間が読む**」の対象。
