# 計測結果 — 第 04 章 example-2

実行環境: Linux 6.18 / Python 3.11 / Pillow 12.x / 8 並列

## 一括処理(主目的)

```
=== 一括処理結果 ===
  入力          : 100 枚 / 11.3 MB
  リサイズ後    : 100 枚 / 2.9 MB
  サムネイル    : 100 枚 / 0.3 MB
  透かし入り    : 100 枚 / 3.3 MB
  並列処理時間  : 2.43 秒
  1 枚あたり    : 24.3 ms
```

## 比較

| 方法 | 100 枚処理 |
|------|-----------|
| Photoshop で手作業(リサイズ + サムネ + 透かし) | 約 **2.5 時間** |
| Photoshop アクション(自動化済み) | 約 5 分(1 枚 3 秒 ×100) |
| Python(このスクリプト、8 並列) | **2.4 秒** |

Photoshop 手作業との比は **約 3,700 倍**。

## サイズ削減

| 出力 | 1 枚あたり | 100 枚合計 | 入力比 |
|------|-----------|-----------|--------|
| 入力(1920×1280, q=92) | 約 113 KB | 11.3 MB | 1.0 |
| リサイズ(長辺 1200, q=85) | 約 30 KB | 2.9 MB | **0.26 倍** |
| サムネイル(200×200, q=80) | 約 3 KB | 0.3 MB | **0.03 倍** |
| 透かし入り(同サイズ + WM) | 約 33 KB | 3.3 MB | 0.29 倍 |

Web 公開には **リサイズ + サムネイル + 透かし** の 3 形式があれば足りる。
合計 **6.5 MB**(元の 60% に圧縮)。

## サンプル(`out/sample/`)

100 枚のうち、各処理結果を 2 枚ずつコミット:

```
out/sample/resized-img_000.jpg       (1200×800)
out/sample/resized-img_050.jpg
out/sample/thumbs-img_000.jpg        (200×200)
out/sample/thumbs-img_050.jpg
out/sample/watermarked-img_000.jpg   (1200×800 + © aiseed.dev 2026)
out/sample/watermarked-img_050.jpg
```

ブラウザで開けば処理結果の品質が確認できる。

## 並列処理の効果

```python
with ProcessPoolExecutor() as pool:
    results = list(pool.map(process_one, files))
```

- シリアル実行(参考、推定): 約 18 秒
- 8 コア並列: **2.4 秒**(約 7.5 倍速)

CPU が複数あるなら、繰り返し処理は並列で。
**人間も並列できないが、コードはできる**。

## 来月の運用

```bash
# 1. 新しい写真を src/ に置く
cp ~/Pictures/2026-05/* src/

# 2. 走らせる
python3 process.py

# 3. resized/ と thumbs/ を Web に上げる
rsync -av out/resized/ user@server:/var/www/photos/full/
rsync -av out/thumbs/  user@server:/var/www/photos/thumb/
```

これを cron に登録すれば、写真フォルダに何かが置かれた瞬間から
公開準備まで自動。

## 再現手順

```bash
pip install Pillow
make clean && make all
```
