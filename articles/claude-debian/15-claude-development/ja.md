---
slug: claude-debian-15-claude-development
number: "15"
title: 第15章 Claudeとの開発の実践
subtitle: 小さなアプリを、実データと使い続けられる形に育てる
description: 第14章のダッシュボードを実データに繋ぎ、テストを書き、エラーを扱い、配布可能にする。Claude Codeを使って「動くだけ」から「使えるアプリ」までの一周を体験する。
date: 2026.04.23
label: Claude × Debian 15
prev_slug: claude-debian-14-widget-architecture
prev_title: 第14章 Widget アーキテクチャの実装
next_slug: claude-debian-16-python-flutter-other
next_title: 第16章 Python、Flutter、その他の環境
cta_label: Claudeと学ぶ
cta_title: 動くだけでは、使えない。
cta_text: 実データに繋ぎ、失敗を扱い、テストを添え、配布可能な形にする。これが「動く」から「使える」までの距離。Claudeと一緒に、その距離を歩く。
cta_btn1_text: 第16章へ進む
cta_btn1_link: /claude-debian/16-python-flutter-other/
cta_btn2_text: 第14章に戻る
cta_btn2_link: /claude-debian/14-widget-architecture/
---

## 実アプリへの一周

第14章で作ったダッシュボードは動くが、まだ「玩具」だ。実データに繋がっていない、エラーが起きたらクラッシュする、テストがない、他人に配布できない。

第15章では、この玩具を**毎日使えるアプリ**に育てる。開発の基本サイクルを Claude Code と一緒に一周する。

## 第一節 Claude Code の本格運用

### プロジェクトに入って起動

```bash
cd ~/Projects/my-dashboard
claude
```

起動したら、Claude Code にプロジェクトの状況を伝える。

> このディレクトリには、第14章で作ったFletベースのダッシュボードアプリがあります。
> 今日は次を進めたい：
> (1) WeatherWidgetを実データ（Open-Meteo API）に接続
> (2) 失敗時のエラー表示
> (3) テストの追加
> (4) README と実行用スクリプト
>
> 現在のファイル構成を読み取って、何から始めるか提案してください。

Claude Codeはファイルを読み、現状を把握した上で計画を返す。

### 変更を逐次レビュー

Claude Code は自動で大量のファイルを書き換えることができる。だが**自動承認してはいけない**。

- 一つのファイル変更ごとに、変更内容を確認
- 意図が分からなければ聞き返す
- 「なぜそうしたか」の根拠を必ず確認

これは Copilot 問題（[第12章「MicrosoftのCopilotの課題」](/blog/copilot-correct-looking-but-wrong/)）への対処と同じ姿勢だ。AIが書いたコードの最終責任は、人間が負う。

## 第二節 実データに接続する

### 天気 API の選定

無料で使える天気 API はいくつかある。

- **Open-Meteo**：登録不要、商用もOK、緯度経度指定
- **OpenWeatherMap**：登録要、無料枠あり
- **気象庁のJSON**：公式データ、日本国内限定

本書の推奨は **Open-Meteo**。登録不要で、すぐに試せる。

### Claudeに実装させる

> WeatherWidgetを Open-Meteo APIに接続してください。
>
> 要件：
> - 緯度経度（デフォルト：東京 35.6762, 139.6503）を親から渡せる
> - 30分ごとにデータを更新
> - 取得失敗時はエラーをUIに表示（クラッシュしない）
> - requestsの代わりに標準ライブラリ（urllib）または httpx を使う
>
> コードは既存のクラス構造を崩さないように。

返ってきたコードをレビュー。特に **エラー処理** を注意深く見る。ネットワーク障害、APIダウン、JSONパース失敗——この三つが必ず起こる。

## 第三節 エラーとの付き合い方

### 三つの層

エラーを扱う層は三つある。

**層1：防御的プログラミング**
想定内のエラー（ネットワーク失敗、API形式の変更）を `try / except` で受け止める。

**層2：ユーザーに見せる表示**
UIに「取得失敗」と出して、再試行ボタンを用意。クラッシュさせない。

**層3：ログに残す**
開発者（あなた）が原因を追えるよう、ファイルに書き残す。

```python
# Pythonの標準ロギング
import logging
from pathlib import Path

log_dir = Path.home() / ".local" / "share" / "my-dashboard"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_dir / "app.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

`logging.basicConfig(filename=...)` に `~` を直書きすると **展開されず
そのまま `~` というディレクトリが作られる**(よくある落とし穴)。
`Path.home()` で先に展開してから渡す。

### Claudeに聞いてみよう①：エラー処理の見直し

> 私のWeatherWidget〔コード貼る〕で、次のエラーケースを扱えているか確認してください：
> (1) ネットワーク切断
> (2) API からの 500 エラー
> (3) API レスポンスの JSON 形式が変わった
> (4) タイムアウト（10秒以上応答がない）
> (5) 正常だが予報データが空
>
> 扱えていないケースについて、最小の変更で対処するコードを示してください。

## 第四節 テストを書く

### テストの最小単位

`pytest` を使う。本書では **`uv add --dev pytest`** で入れる
(プロジェクト固有の dev 依存として `pyproject.toml` に記録される)。
`apt install python3-pytest` はシステム Python 用で、業務プロジェクトでは
使わない。

```python
# tests/test_clock_widget.py
def test_format_time():
    from my_dashboard.clock_widget import format_time
    assert format_time(13, 42, 30) == "13:42:30"
    assert format_time(0, 0, 0) == "00:00:00"
```

### Claudeに書かせる

> 私のClockWidget の時刻フォーマット関数 format_time と、WeatherWidget の JSON パース関数 parse_weather のユニットテストを pytest で書いてください。
>
> - 正常系：3ケースずつ
> - 異常系：無効な入力、空、極端な値——各3ケースずつ
> - テストは独立（お互いに依存しない）
> - モック（ネットワークアクセスをしない）
>
> 既存のコードに合わせて、import パスを正しく。

### テストを回す

```bash
uv run pytest tests/
```

`uv run` を頭に付けると、プロジェクトの `.venv/` にある pytest が走る。
全部パスするのを確認。赤が出たら、コードかテストかどちらが正しいかを判断する。

### テストは生き物

テストは「一度書いて終わり」ではない。新しい機能を追加するたびに、対応するテストも追加する。この習慣が、後々コードに自信を持たせる。

## 第五節 設定を外出しする

### ハードコードを設定ファイルに

アプリ内部に書いている定数（緯度経度、更新間隔、APIエンドポイント）を、外部の設定ファイルに出す。

```toml
# config.toml
[weather]
latitude = 35.6762
longitude = 139.6503
refresh_interval_minutes = 30

[schedule]
source = "~/Documents/schedule.ics"

[theme]
dark = true
accent_color = "#4a7c59"
```

Python標準の `tomllib`（3.11以降）で読める。

### Claudeに聞いてみよう②：設定の設計

> 私のダッシュボードアプリのコードから、設定として外出しできる項目を列挙してください。
> config.toml の例と、それを読み込む最小のコードを書いてください。
> ユーザーが config.toml を書き換えたとき、アプリを再起動すれば反映されることを前提に。

## 第六節 配布できる形にする

### 依存関係はすでに `pyproject.toml`

`uv add` で入れた依存はすべて `pyproject.toml` に記録され、`uv.lock` が
**バージョンを完全固定**する。`requirements.txt` は要らない。

```toml
# pyproject.toml(uv add で自動生成・更新される)
[project]
name = "my-dashboard"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "flet>=0.20",
    "httpx>=0.27",
]

[dependency-groups]
dev = ["pytest>=8.0"]
```

別 PC への移行は `git clone && uv sync` の **2 コマンド**で終わる。

### 実行スクリプト

シェルスクリプトを書く必要はあまりない。`uv run` で直接動く。

```bash
# プロジェクト直下で
uv run python -m my_dashboard
```

それでも 1 コマンドで呼びたい場合は、`uv tool install` で世界に
公開できる:

```bash
# 自分のプロジェクトをツールとして PATH に登録
uv tool install --editable .
# あとはどこからでも
my-dashboard
```

`pyproject.toml` の `[project.scripts]` でエントリポイントを定義しておくと、
`uv tool install` が自動でコマンドを `~/.local/bin/` に置く。

```toml
[project.scripts]
my-dashboard = "my_dashboard.__main__:main"
```

### デスクトップエントリ

メニューから起動できるように。

```ini
# ~/.local/share/applications/my-dashboard.desktop
[Desktop Entry]
Type=Application
Name=My Dashboard
Exec=my-dashboard
Icon=/home/you/Projects/my-dashboard/assets/icon.png
Categories=Utility;
```

`uv tool install` 済みなら `Exec=my-dashboard` で動く。

### Claudeに聞いてみよう③：配布の仕上げ

> 私のダッシュボードアプリを、次の三段階で使えるようにしたいです：
> (1) 自分で日常起動（デスクトップエントリ、メニューから一発）
> (2) 別PCに持っていける（git clone + 1 コマンドで動く）
> (3) 友人に配れる（手順書つき）
>
> 各段階で必要なファイル（README、requirements、desktop entry、install.sh等）を作成してください。

## 第七節 Gitで育てる

### コミットの粒度

機能追加・修正ごとに一コミット。メッセージは「何をしたか」と「なぜしたか」を一行で。

```
feat(weather): Open-Meteo API への接続を追加
fix(clock): 午前0時の表示バグを修正
test: format_time の異常系テストを追加
refactor(config): 定数を config.toml に外出し
docs: README に起動手順を追加
```

### ブランチの使い方

小さい個人プロジェクトでは、`main` だけで始めて問題ない。大きな変更を試すときだけ、ブランチを切る。

```bash
git checkout -b experiment/dark-theme
# 試す
# うまくいけば main に merge、ダメなら捨てる
```

## 第八節 「動く」から「使える」までの距離を振り返る

第14章の「玩具」から、第15章の「実アプリ」まで、次を進めた。

| 観点 | 玩具（Ch14） | 実アプリ（Ch15） |
| --- | --- | --- |
| データ | ハードコード | 実API |
| エラー | クラッシュ | UI表示＋ログ |
| テスト | なし | ユニットテスト |
| 設定 | コード内 | 外部ファイル |
| 起動 | python file.py | desktop entry |
| 配布 | 不可 | git clone で動く |

「動くだけ」から「使える」までの距離を、数字にすればコード行数は2倍以上に膨らむ。**この距離を正直に踏むのが、エンジニアリングだ**。AIは、この各段階を補助してくれる。

## 第九節 Claudeとの開発で気を付けること

### 小さく刻む

「全部一気にやってください」と頼むと、Claudeは大量のコードを返す。読みきれず承認ミスが起きる。

**指示は小さく刻む。** 一つの目的（天気APIを繋ぐ、エラー処理を追加する、テストを書く）ごとに一つの対話。

### 自分が理解できない範囲には進まない

Claudeが返したコードで、ひとつも理解できない関数が出てきたら、それは**あなたが判断できない範囲**に入った合図だ。

そのときは、Claude に「このコードの各行を説明してください。初心者向けに、何をしているかと、なぜそうするかを」と頼む。理解できない状態で本番に入れない。

### Claudeに聞いてみよう④：自己評価

> 私はこの章で、第14章から第15章までの一周を進めました。
> 現在のコード〔最終版を貼る〕を見て、次を評価してください：
> (1) 保守性（半年後の私が読んで理解できるか）
> (2) 拡張性（新しいWidgetを足しやすいか）
> (3) 堅牢性（想定外のエラーで止まらないか）
> (4) テスト網羅（重要な挙動をカバーしているか）
> (5) 配布品質（別のPCで動くか）
>
> 各項目を10点満点で評価し、改善点を優先順に3つ挙げてください。

## まとめ

この章でやったこと：

1. Claude Code をプロジェクトで起動し、逐次レビューの作法を確立
2. 実データ（Open-Meteo API）に接続
3. エラー処理を三層（防御・UI・ログ）で整えた
4. pytestでユニットテストを書いた
5. 設定を config.toml に外出しした
6. デスクトップエントリで起動可能にした
7. Gitで育てるリズムを整えた

手元に残ったもの：
- 毎日使える自作ダッシュボードアプリ
- Claude Code とのまっとうな協業パターン
- 「動く」から「使える」までのエンジニアリングの一周の経験

次の第16章では、Python と Flet 以外の環境——Flutter / Dart、Node.js、Rust、Docker——へ視野を広げる。必要になったときにClaudeと組み立てられる状態にする。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
