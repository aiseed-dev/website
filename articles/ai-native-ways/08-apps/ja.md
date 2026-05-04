---
slug: apps
number: "08"
title: アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ
subtitle: 段階的にスケールアップする三層構造
description: アプリを作るのに、最初から Flutter は要らない。CLI ツールで書いて動かし、画面が要るなら Flet で Python のまま GUI を作り、本格的なクロスプラットフォームが必要なら Flutter に進む。三層を段階的に登れば、リスクが小さく、AI が書きやすい。
date: 2026.05.02
label: AI Native 08
title_html: アプリは <span class="accent">CLI</span> から始め、<br><span class="accent">Flet</span>、<span class="accent">Flutter</span> へ伸ばす。
prev_slug: web
prev_title: Webを作る ── HTML+CSS+JavaScriptという原点回帰
next_slug: embedded
next_title: 組み込みを作る ── Pythonで考え、Claudeに翻訳させる
---

# アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ

アプリを作るとき、最初から Flutter や React Native や Swift で書き始めない。

**CLI から始める**。動かす。それから画面が要るなら Flet で GUI を載せる。それでも足りなければ Flutter に進む。三層を段階的に登る。これが AI ネイティブな作り方だ。

## 三つの層

アプリを作る道具は、三段階に分けて考える。

| 層 | 道具 | 目的 |
|----|------|------|
| 第一層 | CLI ツール(Python) | 処理本体を書いて、動かして、検証する |
| 第二層 | Flet アプリ(Python) | 画面が要るときに、Python のまま GUI を載せる |
| 第三層 | Flutter アプリ(Dart) | 本格的なクロスプラットフォームアプリ |

新しいアプリは、第一層から始める。第二層に進むのは、CLI で動くものができてから。第三層に進むのは、Flet で足りないと分かってから。

**手戻りは少なく、書く量も少なく済む**。

## 第一層: CLI ツールから始める

アプリの本質は、入力を取って、処理して、出力する、ことだ。

最初に書くべきは、コマンドラインツールだ。

```python
import sys

def main(args):
    input_file = args[0]
    # 処理を書く
    print("done")

if __name__ == "__main__":
    main(sys.argv[1:])
```

これで「コマンドを実行すると何かが起きる」アプリができる。GUI は無い。テストしやすい。デバッグしやすい。Claude が書きやすい。

CLI ツールが正しく動くようになったら、それで配布できる。Mac/Linux/Windows、すべての OS で動く(Python があれば)。Web からダウンロードしてもらう必要すらない。`pip install` で配れる。

**多くのアプリは、CLI で十分**だ。データを処理する、ファイルを変換する、API を叩く ── これらは GUI が無くても困らない。

## 第二層: Flet で GUI を載せる

CLI で十分でない場合 ── 操作する人が技術者ではない、視覚的なフィードバックが要る、入力欄が複数ある ── 画面が要る。

そのとき、Flutter を学ぶ前に Flet を試す。

Flet は Python で書ける GUI フレームワークだ。Flutter のレンダリングエンジンを内側で使うが、書くのは Python。第一層の CLI コードを、ほぼそのまま GUI に載せられる。

```python
import flet as ft

def main(page: ft.Page):
    name = ft.TextField(label="名前")
    result = ft.Text()

    def greet(e):
        result.value = f"こんにちは、{name.value}さん"
        page.update()

    page.add(name, ft.ElevatedButton("挨拶", on_click=greet), result)

ft.app(main)
```

これで、テキストフィールドとボタンと表示領域がある GUI アプリが動く。Mac でも Windows でも Linux でも、Web ブラウザでも、モバイル(iOS/Android)でも動く。**書くのは Python だけ**。

Flet は新しい(2022 年公開)。しかし、すでに業務で使える。Claude も書ける。

## 第三層: Flutter

Flet で足りないとき ── 高度なアニメーションが要る、ネイティブの API を叩く、配布チャネル(App Store、Play Store)で売る ── そのときに初めて Flutter を考える。

Flutter は Dart 言語で書く。Dart は Java や C# に似た静的型付け言語だ。新しく学ぶ必要があるが、Claude が書ける。**自分で Dart を書ける必要はない**。Claude に頼んで書いてもらい、自分は読んで判断する。

第一層・第二層で Python のロジックを書いて検証してから、Flutter に移植する。**処理の正しさは Python で確認済み**なので、Dart 側は UI と OS 連携だけに集中できる。

これで、Flutter プロジェクトの複雑さの半分が消える。

## なぜ Swift / Kotlin を勧めないか

iOS 専用、Android 専用のアプリは、Swift や Kotlin で書ける。しかし、最初の選択肢としては勧めない。

理由は二つだ。

一: クロスプラットフォームのコスト。同じアプリを iOS と Android の両方に作るなら、Flutter の方が圧倒的に安い。Swift と Kotlin で別々に作ると、コードの量が 2 倍、保守の負担も 2 倍になる。

二: AI の書きやすさ。Swift と Kotlin も Claude は書ける。しかし、Python と Dart の方が、Claude の出力品質が安定している。`SwiftUI` や `Jetpack Compose` の最新仕様は変化が速く、AI のトレーニングデータが追いついていないことがある。

iOS にしか出さない明確な理由(Apple Watch 連携、Vision Pro 専用、など)があれば Swift を選ぶ。それ以外なら Flutter で良い。

## React Native も勧めない

「React で書けるから React Native」という考えは、Web の章で書いた通り、もう積極的に勧めない。

Flutter のほうが描画品質が高く、依存も少なく、Dart は JavaScript より AI が書きやすい。**React のエコシステムから離れる**ことが、Mythos 時代の安全策だ。

## 何で配るか

CLI ツール: PyPI(`pip install`)、GitHub リリース、自分の Web サイトで配布。

Flet アプリ: Flet 単体で配布できる(各 OS の実行ファイルにビルド)。Web 版は Web サイトに置くだけ。

Flutter アプリ: App Store、Play Store、Web、デスクトップアプリ ── 全部できる。

**段階を上がるほど配布手段が増えるが、ハードルも上がる**。最初から最高層を目指す必要はない。CLI で十分配布できることが多い。

## 例: 自分のための写真整理アプリ

例を挙げる。「カメラで撮った写真を、撮影日でフォルダ分けする」アプリを作りたい。

第一層(CLI)で書く:

```python
# python organize.py /path/to/photos
import sys, shutil, os
from PIL import Image
from PIL.ExifTags import TAGS

def main(folder):
    for f in os.listdir(folder):
        if not f.lower().endswith(('.jpg', '.jpeg')):
            continue
        path = os.path.join(folder, f)
        img = Image.open(path)
        exif = img._getexif() or {}
        date = next((v for t, v in exif.items() if TAGS.get(t) == 'DateTimeOriginal'), None)
        if date:
            ymd = date[:10].replace(':', '-')
            target = os.path.join(folder, ymd)
            os.makedirs(target, exist_ok=True)
            shutil.move(path, os.path.join(target, f))

if __name__ == "__main__":
    main(sys.argv[1])
```

このコード、Claude に「写真を撮影日でフォルダ分けする Python を書いて」と頼めば 30 秒で出てくる。実行すれば動く。

これで配布できる(自分が使うだけならこれで終わり)。

家族や友人にも使ってほしいと思ったら、第二層に上がる。Flet で GUI を被せる。「フォルダを選ぶ」ボタンと「実行」ボタンがあるアプリになる。

App Store で売りたい(本当に?)と思ったら、第三層に上がる。Flutter で書き直す。Python のロジックは Claude に Dart に変換させる。

**多くの場合、第一層で終わる**。これで困らない。

## 実例: 数字で見る

写真整理アプリ(撮影日でフォルダ分け):

- CLI で書く: 30 行の Python、開発時間 **30 分**、配布は GitHub に置くだけ
- iOS アプリで作る: Swift で 200 行、Xcode 環境 50 GB、App Store 審査 1 週間、年会費 $99

開発環境のディスク使用量:

- Flutter: Android Studio + Flutter SDK + Xcode で **約 50 GB**
- Flet: Python 環境だけで **約 100 MB**(Flutter 配布が必要なときのみ展開)
- CLI ツール: **20 MB**

CLI ツールの作成と配布: 1 時間で書いて、`pip install` で世界中の Python ユーザーに即配布。同じ機能を「アプリ」として配るには、3 つの App Store の審査と 2 つの SDK が要る。**2 週間以上の差**。

CLI で動く処理を Flet で GUI 化する追加コスト: Flet ライブラリのインストールと数十行の追加コード、**1 時間**。Flutter で書き直すなら 1 ヶ月。

## 実例: 写真整理 CLI を作って PyPI で世界配布する

撮影日でフォルダ分けする CLI ツールを作って、PyPI で公開、世界の Python ユーザーに `pip install` で配る。

**手順 1: Claude にコードを書かせる**

```
あなた: jpg/jpeg を EXIF の撮影日でフォルダ分けする CLI を Python で。
        引数で対象フォルダを受け取る。pyproject.toml も含めて
```

返ってくる構造:

```
photo-sort/
├── pyproject.toml
├── src/photo_sort/
│   ├── __init__.py
│   └── cli.py
└── README.md
```

**手順 2: コードを確認・実行**

```python
# src/photo_sort/cli.py
import sys, shutil, os, argparse
from PIL import Image
from PIL.ExifTags import TAGS

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()

    for f in os.listdir(args.folder):
        if not f.lower().endswith(('.jpg', '.jpeg')):
            continue
        path = os.path.join(args.folder, f)
        img = Image.open(path)
        exif = img._getexif() or {}
        date = next((v for t, v in exif.items() if TAGS.get(t) == 'DateTimeOriginal'), None)
        if date:
            ymd = date[:10].replace(':', '-')
            target = os.path.join(args.folder, ymd)
            os.makedirs(target, exist_ok=True)
            shutil.move(path, os.path.join(target, f))

if __name__ == "__main__":
    main()
```

ローカルで動作確認:

```bash
pip install -e .
photo-sort ~/Pictures/2026/
```

**手順 3: pyproject.toml**

```toml
[project]
name = "photo-sort"
version = "0.1.0"
description = "Sort photos into folders by capture date"
dependencies = ["Pillow"]

[project.scripts]
photo-sort = "photo_sort.cli:main"
```

**手順 4: PyPI に公開**

```bash
pip install build twine
python3 -m build
twine upload dist/*
```

**5 分で世界の PyPI に登録完了**。

**手順 5: 世界中から使われる**

その日のうちに、誰でもこれが動く:

```bash
pip install photo-sort
photo-sort ~/Pictures/
```

GitHub に置けば、Star がつき、Issue が来て、Pull Request が来る。**App Store の審査も年会費 $99 もなしで、世界規模の配布**。

**手順 6: GUI が要れば Flet で被せる**

```python
# src/photo_sort/gui.py
import flet as ft
from .cli import sort_folder  # CLI のロジックを再利用

def main(page: ft.Page):
    folder = ft.TextField(label="フォルダ")
    result = ft.Text()
    def run(e):
        sort_folder(folder.value)
        result.value = "完了"
        page.update()
    page.add(folder, ft.ElevatedButton("整理", on_click=run), result)

ft.app(main)
```

**第一層(CLI)の処理ロジックがそのまま使える**。30 行追加で GUI アプリが手元に来る。Flutter で書き直すなら 1 ヶ月、Flet なら 1 時間。

## まとめ

アプリは、CLI から始める。

CLI で動くものを作って、検証する。GUI が要れば Flet で載せる。クロスプラットフォーム配布が要れば Flutter に進む。

**段階を上がるたびに、CLI で書いた処理コードが活きる**。AI が書きやすい層から始めて、必要に応じて広げる。これが AI ネイティブなアプリ開発だ。

次の章では、組み込みを作る話に進む。「Python で考え、Claude に C に翻訳させる」── ハードウェアと AI のはなし。

---

## 関連記事

- [第7章: Webを作る ── HTML+CSS+JavaScriptという原点回帰](/ai-native-ways/web/)
- [第4章: 処理を書く ── AIにPythonで書いてもらう](/ai-native-ways/python/)
- [構造分析15: Mythos時代のセキュリティ設計](/insights/security-design/)
