---
slug: claude-debian-14-widget-architecture
number: "14"
title: 第14章 Widget アーキテクチャの実装
subtitle: 小さな再利用可能な部品から、自分のアプリを組み立てる
description: Widgetアーキテクチャ——独立した小さな部品を組み合わせてアプリを作る設計——をClaudeと一緒に学ぶ。小さな時計アプリを題材に、Widget分割、状態管理、レイアウト、再利用の原則を実装してみる。
date: 2026.04.23
label: Claude × Debian 14
prev_slug: claude-debian-13-dev-tools
prev_title: 第13章 開発ツールの構築
next_slug: claude-debian-15-claude-development
next_title: 第15章 Claudeとの開発の実践
cta_label: Claudeと学ぶ
cta_title: 大きな機能は、小さな部品の和。
cta_text: 一つのWidgetを、独立した小さな単位として作る。それを組み合わせる。このパターンを身につければ、あらゆるUIが手の届く範囲に入る。
cta_btn1_text: 第15章へ進む
cta_btn1_link: /claude-debian/15-claude-development/
cta_btn2_text: 第13章に戻る
cta_btn2_link: /claude-debian/13-dev-tools/
---

## Widgetとは何か

Widgetは、**独立して動く小さなUIの部品**のことだ。ボタン、入力欄、リスト、カード、時計、グラフ——一つ一つが自分の状態と見た目を持ち、他から切り離しても動く。

大きなアプリは、Widgetを組み合わせて作る。階層的に重ねて、全体を構成する。ReactのComponent、Flutterの Widget、VueのComponent、FletのControl——呼び方は違っても、考え方は共通だ。

この章では、小さな時計アプリを題材に、Widgetアーキテクチャを体得する。**コードそのものはClaudeが書く**。あなたが身につけるのは、**設計の考え方**と**Claudeへの指示の仕方**だ。

## 第一節 題材：シンプルなダッシュボード

作るのは次のようなアプリだ。

```
+-------------------------------+
|   時計（13:42:30）             |
+-------------------------------+
|   今日の予定（3件）            |
|   - 10:00 ミーティング          |
|   - 14:00 資料提出             |
|   - 18:00 夕食                 |
+-------------------------------+
|   天気（晴れ、18°C）            |
+-------------------------------+
```

三つのWidgetが積み重なる構造。各Widgetは独立して動き、それぞれ別のデータ源を持つ。

### 使う言語とフレームワーク

本書の推奨は **Python + Flet**（Flutterベース、Pythonから扱える）。Dart/Flutterの準備が要らず、最短で動く。

```bash
sudo apt install python3-pip python3-venv
python3 -m venv ~/envs/flet
source ~/envs/flet/bin/activate
pip install flet
```

## 第二節 Widgetに分割する

### 設計の第一歩

書き始める前に、**どのWidgetに分けるか**を決める。

- **ClockWidget**：現在時刻を1秒ごとに更新
- **ScheduleWidget**：今日の予定を表示
- **WeatherWidget**：現在の天気を表示
- **DashboardApp**：上の三つを並べる親

分けるときの原則：
1. **一つのWidgetは、一つの関心事しか持たない**（時計は時計、天気は天気）
2. **Widget間で直接データをやり取りしない**（親経由でのみ渡す）
3. **Widgetは外から使うAPIを最小限にする**（初期化と更新だけ）

### Claudeに聞いてみよう①：Widget分割の相談

> Fletで、時計・予定・天気を並べたダッシュボードアプリを作ります。
> 次の三つのWidgetに分けようと思います：
> - ClockWidget：時刻を1秒ごとに更新
> - ScheduleWidget：その日の予定リスト
> - WeatherWidget：現在の天気
>
> この分割は妥当か、改善案があるか、教えてください。
> 各Widgetの責務（何を知り、何を表示し、外とどう通信するか）を表にしてください。

Claudeとの往復で、設計を固める。この段階ではコードは書かない。**設計だけで30分〜1時間使う価値がある。**

## 第三節 一つ目のWidget：時計

### Claudeに書かせる指示

最初のWidgetをClaudeに書かせる。

> Flet で ClockWidget を書いてください。
>
> 要件：
> - 現在時刻を `HH:MM:SS` 形式で表示
> - 1秒ごとに更新
> - 文字は大きく、中央揃え
> - 独立したクラスとして実装（main関数とは分離）
>
> コード全体を一ファイルで。実行するとClockWidget 単独で動くサンプルも添えてください。
> Python 3.11以上、Flet 最新版で動くことを前提に。

Claudeが返したコードを読む。**全部理解できなくてよい**。次の三点だけ確認する。

1. クラスの名前が `ClockWidget` になっているか
2. 時刻を更新するロジックがクラスの中にあるか
3. main関数でそのクラスを使うサンプルが動きそうか

### 実行してみる

```bash
cd ~/Projects/my-dashboard
# Claudeのコードを clock_widget.py として保存
python3 clock_widget.py
```

ウィンドウが開いて、時計が動けば成功。動かなければ、エラーをそのままClaudeに貼って聞く。

### Claudeに聞いてみよう②：エラー対応

> 次のコードを実行したところ、エラーが出ました：
> ```
> 〔コード〕
> ```
> ```
> 〔エラーメッセージ全文〕
> ```
>
> 原因と修正方法を教えてください。修正後のコード全文を示してください。

## 第四節 Widget同士の組み合わせ

### 親 Widget を作る

三つのWidgetを並べる親を作る。

> ClockWidget、ScheduleWidget、WeatherWidget の三つを縦に並べて表示する DashboardApp を書いてください。
> 各Widgetは既に別ファイル（clock_widget.py, schedule_widget.py, weather_widget.py）にあるとします。
>
> 要件：
> - 各Widgetは独立したクラス
> - DashboardAppはそれらを import して配置するだけ
> - 画面サイズはウィンドウ幅に追従
> - 縦スクロール可能

これがWidgetアーキテクチャの核：**親は子を配置するだけ**。子の中身には口を出さない。

### ScheduleWidgetとWeatherWidget

同じ流れで、残り二つもClaudeに書かせる。Scheduleは一旦ハードコードした予定を表示、Weatherはダミーデータで始める。

**大事なのは：最初は動く最小版を作って、その後で本物のデータに繋ぐ**。いきなり外部APIに繋ぐと、デバッグが大変になる。

## 第五節 状態管理の入り口

### Widget 内部の状態

ClockWidgetは「現在時刻」という状態を持つ。Flet では次のように扱う。

```python
# Claudeに書かせた例（概念）
class ClockWidget(ft.UserControl):
    def build(self):
        self.time_text = ft.Text(size=48)
        return self.time_text

    def did_mount(self):
        # 1秒ごとに更新するタイマーを開始
        ...
```

### 親から子にデータを渡す

WeatherWidget に「地名」を親から渡したいとき。

```python
class WeatherWidget(ft.UserControl):
    def __init__(self, city: str):
        super().__init__()
        self.city = city
```

親が `WeatherWidget(city="Tokyo")` のように初期化する。

### Claudeに聞いてみよう③：状態管理の質問

> Fletでの状態管理について教えてください：
> (1) Widget内部で持つべき状態（時計の現在時刻、天気の最新データ）
> (2) 親から子に渡すべきもの（表示地名、テーマ色）
> (3) 親子を跨ぐ状態の扱い（複数Widgetが共有する設定）
>
> 初心者向けの単純な方針を、ダッシュボードアプリの例で示してください。
> 過度に複雑な状態管理ライブラリは避けてください。

## 第六節 見た目を整える

### 色、フォント、余白

一旦動いたら、見た目を整える。Claudeに指示する。

> 現在のDashboardAppの見た目を、次の原則で整えてください：
> - ダークテーマ（背景 #1a1a1a、前景 #e0e0e0）
> - 各Widget間の余白 16px
> - 角丸のカード風 (border_radius=12)
> - 時計は大きめ（72pt）、他は中くらい
> - 日本語対応フォント（Noto Sans JP）
>
> コード全体を書き換えるのではなく、スタイルをまとめた定数セクションを追加してください。

**見た目を整える過程で、コードの読みやすさも上がる**。色や大きさを定数にまとめる設計は、後の変更を楽にする。

## 第七節 Widget の再利用

### 応用：タイマーWidget

ClockWidgetができたので、同じ構造で「カウントダウンタイマー」も作れる。

> ClockWidgetと同じ構造で、指定した分数をカウントダウンするTimerWidgetを作ってください。
> 共通できる部分があれば、基底クラス BaseTimeWidget を作って両方を派生させてください。

ここで**コードの共通化**が起きる。同じ構造のWidgetが複数あるとき、共通部分をまとめる——これがソフトウェアの成長の仕方だ。

### 重要な禁じ手

共通化を**やりすぎない**。最初から抽象化すると、後の変更が難しくなる。

- 2回同じコードが出たら：まだコピペ
- 3回目に出たら：共通化を検討
- 4回以上出る予感：共通化する

この感覚は、Claudeに相談しながら身につける。

### Claudeに聞いてみよう④：過剰設計の回避

> 私は Widget を作っています。今、ClockWidget と TimerWidget で似たコードが出てきました。
> 次のどれが今の段階で適切ですか：
> (1) そのまま二つの独立したWidgetで置いておく
> (2) 共通部分を関数に抽出する
> (3) 基底クラス BaseTimeWidget を作って派生させる
> (4) イベントドリブンなアーキテクチャに作り変える
>
> 現状のコード〔貼る〕と、今後の見通し〔Claude対話UIも作るかも〕を踏まえて判断してください。

## 第八節 この章で学んだ「考え方」

コード以上に、次の考え方が残れば成功だ。

1. **書き始める前に分割を決める。** Widgetに分ける境界が、そのまま設計の品質になる
2. **まず動く最小版を。** 機能を足すのは後。最初は空のカードでもいい
3. **親は子を配置するだけ。** 子の中身に口を出さない
4. **状態は持つWidgetの中に閉じる。** 親子を跨いで状態を引き回さない
5. **共通化は3回目から。** 早すぎる抽象化はバグの温床

これは Web、モバイル、GUI、全てに共通する。Python/Fletから入ったが、考え方は React や Flutter にも直接転用できる。

## まとめ

この章でやったこと：

1. 小さなダッシュボードアプリを題材に選んだ
2. Widget分割の設計をClaudeと議論した
3. 一つずつWidgetを Claude に書かせ、動かした
4. 親に組み上げて、全体像を作った
5. 状態管理の最小構成を身につけた
6. 見た目を整え、再利用（共通化）の感覚を掴んだ

手元に残ったもの：
- 動作するダッシュボードアプリ（Python/Flet）
- Widget分割の設計メモ
- 「小さく作って組み合わせる」という考え方

次の第15章では、Claude Code を使って、**このアプリをもっと実用的な形に育てる実践**に入る。実データへの接続、エラー処理、テスト、ビルドと配布——本格的なアプリ開発の最初の一周を体験する。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
