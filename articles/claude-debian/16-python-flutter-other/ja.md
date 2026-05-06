---
slug: claude-debian-16-python-flutter-other
number: "16"
title: 第16章 Python、Flutter、その他の環境
subtitle: 必要になったとき、その言語をClaudeと組み立てる
description: Python は uv を主軸に、データサイエンス・機械学習は miniforge を併用。GUI は Flutter/Dart、Rust は Python の高速化(PyO3)に絞る。Web/CLI など他の選択肢は地図として位置を把握。Claude と組むコツを整理する。
date: 2026.04.23
label: Claude × Debian 16
prev_slug: claude-debian-15-claude-development
prev_title: 第15章 Claudeとの開発の実践
next_slug: claude-debian-17-updates-maintenance
next_title: 第17章 アップデートとメンテナンス
cta_label: Claudeと学ぶ
cta_title: 地図として持っておく。
cta_text: 今すぐ全部を覚える必要はない。必要になったときに戻ってこれる地図として、この章を残す。Claudeがあれば、地図の上でどこへでも行ける。
cta_btn1_text: 第5部 第17章へ進む
cta_btn1_link: /claude-debian/17-updates-maintenance/
cta_btn2_text: 第15章に戻る
cta_btn2_link: /claude-debian/15-claude-development/
---

## この章の読み方

第16章は、**地図**として機能する。今すぐ全部を手を動かすのではなく、各言語・環境の位置関係、Debianでの入れ方、Claudeと組むときの勘所を整理しておく。

必要になったときに戻ってきて、該当部分を読み、Claude Code を開く。**「覚える」ことを目的にしない**。

## 第一節 Python(深掘り)

### 本書は `uv` を採用する

Python のパッケージ管理は **`uv`(Astral 製、Rust 実装)** で統一する。
`pip` + `venv` 比 10〜100 倍速く、`requirements.txt` を捨てて
`pyproject.toml` + `uv.lock` で **完全な再現性** が出る。`poetry` の
代替候補だが、**uv の方が速くシンプル**。第 14 章・第 15 章のすべてが
uv 前提で動く。

```bash
# 初回のみ
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### プロジェクトの基本ループ

```bash
# 新規作成
uv init my-project && cd my-project

# 依存追加(pyproject.toml と uv.lock が自動更新)
uv add requests pandas
uv add --dev pytest ruff

# 実行
uv run python -m my_project
uv run pytest

# 別 PC への移動
git clone <repo> && cd <repo> && uv sync   # ← これだけで完全再現
```

### CLI ツールは `uv tool install`

Python で書かれた CLI ツール(`ruff`、`httpie`、`pre-commit`、`yt-dlp` 等)は
**プロジェクト依存ではないので別系統で管理**する。`pipx` の上位互換が
**`uv tool`**。

```bash
uv tool install ruff
uv tool install httpie
uv tool install pre-commit

# 一覧と更新
uv tool list
uv tool upgrade --all
```

`apt install pipx` も使えるが、**uv 一本で覚えた方が頭が軽い**。

### Python 自体のバージョン管理も `uv`

`pyenv` も不要になった。

```bash
uv python install 3.12
uv python install 3.13
uv python list

# プロジェクトで Python 3.13 を要求
echo '3.13' > .python-version
uv sync   # 必要なら自動でインストール
```

### 日本語のデータ処理

pandas、polars、numpy は apt より `uv add` で最新を入れる。

- 大容量 CSV → **polars**(pandas より速い)
- 統計 → scipy、statsmodels
- 可視化 → matplotlib、plotly

ただし **GPU を使う深層学習や、GDAL / OpenCV / R / Julia を絡める
科学計算** では uv だけだと厳しい。次の節 **「DS / ML には miniforge」**
を参照。

### Claudeに聞いてみよう①:現代的な Python プロジェクトの叩き台

> 私は Python で〔データ整理 / Web スクレイピング / GUI / ML / スクリプト〕を
> 書きます。`uv` を前提に、次を含むプロジェクトの雛形を作ってください:
> (1) `pyproject.toml`(依存・dev 依存・scripts エントリ)
> (2) `.python-version` と `uv.lock`
> (3) `ruff` と `pytest` の設定
> (4) `tests/` ディレクトリの最小例
> (5) `README.md` に `git clone && uv sync && uv run` の手順

## 第二節 データサイエンス / 機械学習には miniforge

`uv` は Python プロジェクトの 9 割をカバーするが、**データサイエンス /
機械学習** では足りない場面がある:

- PyTorch + **CUDA / cuDNN**、TensorFlow + GPU
- **R / Julia** との連携(rpy2 / PyJulia)
- **GDAL / OpenCV / FFmpeg** のような Python 以外のネイティブ依存
- RAPIDS、scikit-image、GeoPandas、PyMC 等の重い科学計算スタック
- Apple Silicon の最初期サポート

これらは PyPI のホイールでは不十分なことが多く、**conda-forge 経由で
ビルド済みバイナリを取る**のが現実的。本書では **miniforge** を入れる。

### なぜ miniforge であって Anaconda ではないのか

Anaconda 公式インストーラ(Anaconda Distribution)には **商用ライセンス
縛り**がある(2020 年以降、200 名超の組織は有料化、デフォルト `defaults`
チャンネルも同条件)。**miniforge はそれを避けて**、

- インストーラが小さい(150 MB 程度)
- デフォルトチャンネルが **conda-forge 固定**(コミュニティ運営、
  ライセンス安心、パッケージ数も最大)
- 商用・個人問わず無料

の 3 点で安心して使える。

### インストール

```bash
# Debian 13 / 12 (x86_64)
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
  -o ~/miniforge.sh
bash ~/miniforge.sh -b -p ~/miniforge3

# シェル統合(.bashrc / .zshrc を書き換える、初回のみ)
~/miniforge3/bin/conda init bash    # bash を使うなら
~/miniforge3/bin/conda init zsh     # zsh を使うなら
```

ターミナルを一度開き直す。

**重要**: 既定では `base` 環境が **シェル起動時に自動 activate** される。
これは uv プロジェクトの `.venv` と干渉するので、最初に切る。

```bash
conda config --set auto_activate_base false
```

これで「conda env を使うときだけ `conda activate` する」運用になる。

### 基本のループ

```bash
# 環境作成(Python バージョン + 主要ライブラリを指定)
conda create -n ds python=3.12 \
  numpy pandas polars scipy scikit-learn jupyterlab matplotlib seaborn

conda activate ds

# あとから追加
conda install -c conda-forge gdal opencv

# 環境のエクスポート(チームで共有)
conda env export --from-history > environment.yml

# 別 PC で再現
conda env create -f environment.yml
```

`--from-history` を付けると **明示的に入れたパッケージだけ** が記録される
(自動依存は除外)。これがチーム配布で読みやすい。

### GPU(CUDA)を使う場合

```bash
conda create -n dl python=3.12 \
  pytorch torchvision pytorch-cuda=12.1 \
  -c pytorch -c nvidia

conda activate dl
python -c "import torch; print(torch.cuda.is_available())"   # True が出れば OK
```

CUDA toolkit を **conda env 内に閉じ込められる** のが大きい。Debian の apt で
システム全体の CUDA を入れて他を壊す事故が起きない。プロジェクトごとに
CUDA バージョンを変えることもできる。

### Jupyter Lab を立ち上げる

```bash
conda activate ds
jupyter lab --no-browser --port 8888
```

ブラウザで `http://localhost:8888/?token=…` を開く。Jupyter は
conda-forge 版が最も安定している。

### uv と miniforge の使い分け

| 用途 | 道具 |
|------|-----|
| Web アプリ、API、CLI、業務スクリプト | **uv** |
| データ分析(pandas / polars 中心、CPU のみ) | **uv で十分** |
| 機械学習 / ディープラーニング(GPU)| **miniforge** |
| 科学計算(GDAL / OpenCV / R / Julia 連携)| **miniforge** |
| Jupyter ノートブック中心の探索 | **miniforge**(conda-forge の jupyterlab + ipykernel が安定) |
| Apple Silicon でビルドが通らない時 | **miniforge** |

**プロジェクトは uv で始めて、必要になったら miniforge を併用**が現実的。
両者は別ディレクトリ(`~/miniforge3/envs/` と `<project>/.venv/`)に環境を
作るので衝突しない。**強制 activate を切ってある限り、どちらの環境にも
明示的に入る運用**で問題は出ない。

### Claudeに聞いてみよう②:DS / ML 環境を立ち上げる

> 私の用途は〔画像分類 / 自然言語処理 / 時系列分析 / 統計解析〕で、
> 〔GPU あり / CPU のみ〕です。miniforge で環境を作るための
> `environment.yml` を、最低限のパッケージで雛形化してください。
> Jupyter Lab を立ち上げる手順、Python と R を併用する場合の組み合わせ、
> 既存の uv プロジェクトと衝突させない運用も示してください。

## 第三節 Flutter / Dart

### Flet から Flutter へ

第14・15章で Flet を使ったが、Flet は内部で Flutter を動かしている。**本格的なクロスプラットフォームアプリを作るなら Flutter 直接**も選択肢。

### Flutter のインストール

Debian では公式の手順で。

```bash
# 必要な依存
sudo apt install git curl unzip xz-utils clang cmake ninja-build pkg-config libgtk-3-dev

# Flutter SDK を取得
git clone https://github.com/flutter/flutter.git -b stable ~/flutter
export PATH="$PATH:$HOME/flutter/bin"

# 確認
flutter doctor
```

### Flutter の特徴

- 一つのコードで、Linux・Windows・macOS・iOS・Android・Webの全てに出せる
- 描画は Skia/Impeller で OS ネイティブ UIに依存しない
- Dart 言語（TypeScript に似た記法）
- **モバイルアプリを作りたい人には最適**

### Claudeに聞いてみよう③：Flet か Flutter か

> 私は〔目的〕のために GUI アプリを作りたいです。
> Flet（Python）と Flutter（Dart）のどちらが適切か、次の観点で比較してください：
> (1) 学習コスト
> (2) モバイル配布（iOS/Android）の必要性
> (3) パフォーマンス
> (4) AI補完（Claude/Copilot）の恩恵の大きさ
> (5) 長期保守性

## 第四節 Rust(Python の高速化のために)

Rust は素晴らしい言語だが、本書では **単独では使わない**。日常のスクリプト・
業務ロジック・GUI・Web ── これらは Python(+ uv)で書く方が速く、
保守も楽で、AI が並走しやすい。

Rust を使うのは **「Python のホットスポットを Rust に置き換える」** 場面だ。

### あなたは既に Rust の恩恵を受けている

実は本書の主要ツールの多くは **中身が Rust 製**:

| 道具 | 実装言語 | 効果 |
|---|---|---|
| **uv** | Rust | pip + venv の 10〜100 倍速 |
| **ruff** | Rust | flake8 + black + isort より 10〜100 倍速 |
| **polars** | Rust | pandas より数倍〜十倍速い DataFrame |
| **pydantic v2** | Rust(コア部分) | データバリデーションが桁違いに速い |
| **fnm** | Rust | Node.js バージョン管理 |
| **Zed** | Rust | エディタ(第13章で採用) |

つまり Rust を **書かなくても**、書かれた成果は享受できている。これが
2026 年現在の Rust の主戦場 ── 「**裾野は Python が広く、底は Rust が
速い**」という構造。

### 自分で Rust に降りるとき

Python のプロファイラ(`cProfile` / `py-spy`)で計測して、**1 関数が
処理時間の半分以上**を占めていたら、そこを Rust 化する候補。

```bash
# Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Python から呼ぶ Rust 拡張は **maturin + PyO3** が最も簡単:

```bash
uv tool install maturin
maturin new --bindings pyo3 my_fastlib
cd my_fastlib
maturin develop   # ビルドして同一プロジェクトの uv 環境にインストール
```

これで Python 側で `import my_fastlib` できる。Rust の関数を Python の
関数として呼び出せる。

### Rust を「書く」のではなく「使う」原則

- 既製の Rust 製ツール(uv / ruff / polars 等)を選ぶ
- 自分で Rust を書くのは **計測で詰まったホットスポットだけ**
- 書く前に Python のテストで境界を固めてから、Rust に翻訳する
- **Claude に「この Python 関数を maturin/PyO3 で Rust 化して」**で十分通る

「Rust を勉強してから何か作ろう」と思わない。**Python で困ってから Rust** が
正しい順番。

### Claudeに聞いてみよう④:Python のホットスポットを Rust に

> 私の Python コード〔貼る〕を `cProfile` で計測したところ、
> 〔関数名〕が全体時間の〔割合〕を占めていました。この関数を
> maturin + PyO3 で Rust 化する手順を、最小サンプルで示してください。
> Python 側のインターフェースは変えない前提で。

## 第五節 データベース

### SQLite

Debianに最初から入っている。単一ファイルのDB、個人用途のほとんどに十分。

```bash
# 使い始める
sqlite3 ~/data/my.db
```

Pythonからは標準ライブラリの `sqlite3`。

### PostgreSQL

本格的にやるなら PostgreSQL。

```bash
sudo apt install postgresql
sudo -u postgres createuser $USER
sudo -u postgres createdb $USER
psql
```

### どちらを選ぶか

- 一人で使う、ファイル一個で完結したい → **SQLite**
- 複数人、複数アプリ、本番運用 → **PostgreSQL**

[第15章「Mythos時代のセキュリティ設計」](/insights/security-design/)で書いた通り、**本番環境にはDBを置かない**設計が最強。個人開発では SQLite で足りることが多い。

## 第六節 環境を切り替える習慣

### プロジェクトごとに隔離

- Python:`uv`(プロジェクト直下の `.venv/`)
- Node:`fnm`
- Rust:`rustup` の toolchain
- Docker:コンテナ単位

**システムの Python や npm に直接インストールしない**。プロジェクトごとに
独立した環境を持つことで、一つが壊れても他に波及しない。

### npm は構造的に脆弱である ── サプライチェーンに気をつける

ここで一つ、強く意識しておく必要がある事実がある。

> **npm は、サプライチェーンの観点でとても脆弱なエコシステムである**。

2026 年に **SAP の npm 公式パッケージ 4 種が汚染** され、**1,100 を
超える GitHub リポジトリのデータが流出** した事件があった
`[要検証:具体的な日付・パッケージ名]`。これは特殊例ではない。

過去にも、

- `event-stream`(2018):暗号通貨ウォレット狙撃
- `ua-parser-js`(2021):マイナーや RAT を仕込み
- `colors` / `faker`(2022):メンテナーによる意図的破壊
- 多数のタイポスクワッティング(似た名前のパッケージで誤インストールを誘う)

など、**ほぼ毎年大規模事件が起きている**。

### なぜ npm は構造的に危ないのか

- 一つのプロジェクトが **数百〜数千** のパッケージを推移的に依存する
- それらは **世界中の個人メンテナー** が管理する野良パッケージ
- `npm install` は依存ツリー全体を **無検査で取得・実行** する
- `postinstall` フックで任意コードが走る
- 依存先のうち 1 つが乗っ取られれば、依存しているプロジェクト全体が侵害される

これは Debian の `apt` モデル ── **メンテナーが署名付きパッケージを
レビュー・配布する** 体制 ── とは対極にある。Debian は遅いと言われる
が、その遅さは **検証の遅さ** であり、安全性のコストである。

> Debian の `apt install` と、npm の `npm install` は、似て非なる
> ものである。前者は **検証されたコード** を取得する。後者は **検証
> されていない他人のコード** を、推移的に数千個取得する。

### Claude Code を使うなら、なおさら警戒する

Claude Code は、エディタの裏でファイルを読み、コマンドを実行する。
もし開発機の `node_modules` のどこかに悪意のあるパッケージが潜んで
いれば、**AI 経由でその実行が引き起こされる** 可能性がある。

依存を 1,000 個抱えるプロジェクトに Claude を入れることは、
**信頼できない 1,000 人の他人を、自分の作業空間に招き入れること**
と同じだ。

### 実用的な対策

- **npm 依存の総数を把握する**:`npm ls --all | wc -l` で確認。数百
  超えなら、依存を減らすことを真剣に考える
- **lockfile をコミットする**:`package-lock.json` で正確なバージョン
  を固定。**latest を勝手に拾わせない**
- **`npm audit` を CI に組み込む**:既知脆弱性を自動チェック
- **`postinstall` を信用しない**:`npm install --ignore-scripts` を
  デフォルトにする習慣
- **使い捨てコンテナで開発する**:Docker / podman の中で `npm install`
  すれば、ホスト環境への波及を絶てる
- **可能な限り、npm を使わない選択肢を検討する**:本書(と
  「[AI ネイティブな仕事の作法](/ai-native-ways/web/)」シリーズ)
  が推す Markdown + HTML + Python のスタックなら、フロントエンド
  ビルドの大半は npm 抜きで済む

> 「便利だから使う」ではなく、「**使う必要がなければ使わない**」
> ── これがサプライチェーンセキュリティの基本である。

### 使っていない環境は消す

使わないプロジェクト、使わない言語環境は、定期的に掃除する。
ディスクが膨れる最大要因はこれだ。

```bash
# node_modules 一括削除
find ~/Projects -name node_modules -type d -exec rm -rf {} +

# uv のキャッシュ整理(`.venv` は各プロジェクト内なので Project ごと消せばよい)
uv cache prune
du -sh ~/.cache/uv ~/.local/share/uv

# Flatpak Runtime の整理
flatpak uninstall --unused -y
```

### Claudeに聞いてみよう⑤：環境ダイエット

> 私のホームディレクトリを次のように消費しています：〔du -sh の出力〕。
> 安全に削除できるもの、削除してはいけないもの、定期的に掃除すべきキャッシュを分類してください。
> シェルスクリプトで定期実行する場合の雛形もお願いします。

## 第七節 地図の読み方

この章で挙げた環境は、全て必要になったときに読み返せばいい。**目次として次を覚えておく**だけで十分。

| 用途 | 第一候補 | 第二候補 |
| --- | --- | --- |
| Python プロジェクト管理 | **uv** | — |
| データサイエンス / 機械学習 / GPU | **miniforge** | — |
| Jupyter ノートブック中心の探索 | **miniforge** | uv + jupyter も可 |
| データ整理、スクリプト | Python(uv) | — |
| GUI アプリ | Flet / Flutter | — |
| Web フロントエンド | TypeScript + Vite | — |
| バックエンド / API | Python(uv + FastAPI) / Node.js / Go | — |
| CLI ツール | Rust / Go | Python |
| システム寄り、性能 | Rust | Go |
| データベース | SQLite | PostgreSQL |
| 隔離環境 | Docker | — |

第16章の最大の目的は、**この表が頭に入った状態**にすること。個々の技術の習熟は、必要になってから Claude と進めればよい。

## まとめ

この章でやったこと：

1. Python の現代的スタックを `uv` に統一(プロジェクト管理 + tool + Python バージョン)
2. データサイエンス / 機械学習用に **miniforge** を導入、uv と併用する運用を整理
3. Flutter / Dart の位置づけを把握
4. Rust は単独では使わず、**Python のホットスポット高速化**(maturin + PyO3)に絞る、と決めた
5. データベース(SQLite / PostgreSQL)の選び方
6. 環境を隔離し、掃除する習慣を仕込んだ

ここで第4部が終わる。**あなたの Debian は、いつでも手を動かせる開発基盤になった**。何か作りたくなったとき、その言語の環境を30分で整えられる状態にある。

第5部（第17〜20章）では、**運用と成長**に入る。アップデート、トラブル、育てる、コミュニティとの関わり——日常を回しながら、環境を長く保つ作法を身につける。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
