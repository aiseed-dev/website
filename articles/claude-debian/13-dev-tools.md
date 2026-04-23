---
slug: claude-debian-13-dev-tools
number: "13"
title: 第13章 開発ツールの構築
subtitle: ターミナル、シェル、エディタ、Git——ビルダーの道具を揃える
description: Debianに開発のための基盤を整える。ターミナルエミュレータ、シェル（bash/zsh/fish）、エディタ（Vim/VSCode/Neovim）、Git、SSH鍵。Claudeと一緒に、自分のワークフローに合った道具立てを決める。
date: 2026.04.23
label: Claude × Debian 13
prev_slug: claude-debian-12-config-management
prev_title: 第12章 設定の理解と管理
next_slug: claude-debian-14-widget-architecture
next_title: 第14章 Widget アーキテクチャの実装
cta_label: Claudeと学ぶ
cta_title: 開発は、道具から始まる。
cta_text: 一番使うツールが一番手に馴染むことが、生産性の土台になる。派手な機能より、キー一つの反応速度が効く。
cta_btn1_text: 第14章へ進む
cta_btn1_link: /claude-debian/14-widget-architecture/
cta_btn2_text: 第12章に戻る
cta_btn2_link: /claude-debian/12-config-management/
---

## この部の位置づけ

第3部までで Debian を日常業務に使える状態にした。第4部は、その環境の上に**自分でものを作るための基盤**を組む。

第4部は開発の話だが、「プログラマ向け」ではない。Claudeと一緒にコードを書く時代、**誰もが少しずつビルダーになれる**。この教科書を読んでいるあなたが、一行もコードを書いたことがなくても問題ない。ただ、道具立てだけは揃えておく。必要になったときに動ける状態にする——それが第13章の目的だ。

## 第一節 ターミナルエミュレータ

### 候補

- **GNOME Terminal**（GNOMEの標準）
- **Konsole**（KDEの標準）
- **Xfce Terminal**（Xfceの標準）
- **Alacritty**：GPU描画で高速
- **WezTerm**：高機能、設定はLua
- **Kitty**：GPU描画、設定は独自形式

### 選び方

最初は DE の標準ターミナルで十分。しばらく使って不満が出たら、Alacritty か WezTerm を試す。差は**描画速度と設定の柔軟さ**だ。

### 設定

- フォント：等幅の日本語対応（Source Han Code JP、HackGen、BIZ UDゴシックなど）
- フォントサイズ：普段は 11〜13pt、疲れた日は大きく
- 配色：ダーク系（Solarized Dark、Dracula、Gruvbox）が疲れにくい
- 透明度：低め（5〜15%）で背景がうっすら見える程度

### Claudeに聞いてみよう①：ターミナル選びとテーマ

> 私は〔DE名〕を使っていて、開発は〔コーディング頻度／主に何をする〕です。
> ターミナルエミュレータを選ぶとしたら、標準／Alacritty／WezTerm のどれが適切か理由付きで推薦してください。
> また、目が疲れない配色スキーム（ダーク系）を、モニタの色温度と時間帯別に提案してください。

## 第二節 シェル：bash か zsh か fish か

### 三つの候補

- **bash**：Debianのデフォルト。全環境で動く
- **zsh**：補完と履歴が強力、カスタマイズ性が高い
- **fish**：補完とシンタックスハイライトが即時、学習曲線が緩やか

### 本書の推奨

**初心者は bash のまま、しばらく使ってから zsh に移行**。fish も選択肢だが、POSIX 互換でない書き方があるので、業務スクリプト環境としては慎重に。

### bashの最低限のカスタマイズ

`~/.bashrc` に次を足すと、体感が変わる。

```bash
# 履歴を豊富に
export HISTSIZE=50000
export HISTFILESIZE=100000
export HISTCONTROL=ignoreboth:erasedups

# カラフルな ls
alias ll='ls -alFh --color=auto'
alias la='ls -A --color=auto'

# プロンプトをGit対応に（最小版）
parse_git_branch() {
    git branch 2>/dev/null | sed -n '/\* /s///p'
}
PS1='\[\e[32m\]\u@\h\[\e[m\] \[\e[34m\]\w\[\e[m\] \[\e[33m\]$(parse_git_branch)\[\e[m\]\n$ '
```

### zshに移行する場合

```bash
sudo apt install zsh
chsh -s $(which zsh)     # ログインシェルを zsh に
```

フレームワークは `oh-my-zsh` が有名だが、重いので `starship`（プロンプト）+ 最小限のプラグインで足りる。

### Claudeに聞いてみよう②：シェル選択と最小設定

> 私は〔コマンドライン経験〕です。bash、zsh、fish の三者から選ぶとしたら？
> 選んだシェルの `.〇〇rc` を、実用的な最小構成で書いてください。
> 履歴管理、補完、プロンプト、alias の主要部分を含めて。

## 第三節 エディタ

### 三つの路線

**路線A：軽量テキストエディタ**
- **gedit / GNOME Text Editor / Kate**：GUIの素朴なエディタ
- 普段のメモやMarkdown書きに

**路線B：Vim / Neovim**
- キーボードのみで操作
- 習熟すれば圧倒的に速いが、学習曲線が急
- 最低限の操作（挿入・保存・終了）は覚える価値がある

**路線C：VSCode / Cursor / Neovim + LSP**
- 機能豊富なIDE的エディタ
- AI補完との相性が良い
- 本書の推奨

### VSCode をDebianに入れる

Microsoft公式リポジトリから、または `code` deb パッケージ。

```bash
# Microsoft公式リポジトリを追加（Claudeに最新の手順を確認）
# その後
sudo apt install code
```

拡張機能は「入れすぎない」。最初は次くらいで十分。

- Japanese Language Pack
- GitLens
- Markdown All in One
- EditorConfig
- 各言語の拡張（必要になってから）

### Vim最低限

エディタがVSCodeであっても、**サーバーに入ったときにVimが触れる**のは最低限の基礎教養だ。

```
hjkl        カーソル移動
i           挿入モード
Esc         ノーマルモードに戻る
:w          保存
:q          終了
:wq         保存して終了
:q!         保存せず終了
```

これだけ覚えれば、`sudo vim /etc/〇〇` の場面で困らない。

### Claudeに聞いてみよう③：エディタ構成

> 私は〔現在の主力エディタ：Word/メモ帳/VSCode/その他〕で、書くのは〔日本語の文書／コード／Markdown〕が中心です。
> Debianで使うエディタの組み合わせ（主・副・緊急時）を提案してください。
> VSCode を主にする場合、最低限入れるべき拡張機能を5つに絞って列挙してください。

## 第四節 Git

### 初期設定

```bash
sudo apt install git

# ユーザー情報
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# エディタ
git config --global core.editor "code --wait"   # VSCode の場合

# デフォルトブランチ名
git config --global init.defaultBranch main

# pull戦略
git config --global pull.rebase false
```

### SSH鍵を作る

GitHubやGitLabに安全に接続するため、SSH鍵を作る。

```bash
ssh-keygen -t ed25519 -C "you@example.com"
# パスフレーズを設定
cat ~/.ssh/id_ed25519.pub
# 出力をコピーして、GitHub → Settings → SSH and GPG keys に貼る
```

### 最初の一連の操作

```bash
mkdir ~/my-project
cd ~/my-project
git init
echo "# My Project" > README.md
git add README.md
git commit -m "initial commit"
```

GitHubにリポジトリを作って、リモート追加。

```bash
git remote add origin git@github.com:あなた/my-project.git
git push -u origin main
```

### Claudeに聞いてみよう④：Git の自分用チートシート

> 私は Git 初心者です。日常で使う操作を、次の分類で一枚にまとめたチートシートを作ってください：
> (1) 始める（init, clone）
> (2) 記録する（add, commit, log）
> (3) 送る／受ける（push, pull, fetch）
> (4) ブランチ（branch, checkout, merge）
> (5) 間違いを戻す（reset, restore, stash, revert）
> (6) 共同作業（pull request の基本フロー）
>
> 各コマンドに、最小の例と「このときに使う」を添えてください。

## 第五節 開発者向けのシステム調整

### 重要なディレクトリ

```
~/Projects/           # プロジェクト置き場
~/bin/                # 自作スクリプト（PATHに追加）
~/.local/bin/         # pipx や cargo がここに入れることが多い
```

`~/.bashrc` に次を足して PATH を通す。

```bash
export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
```

### 基本の開発パッケージ

```bash
sudo apt install build-essential curl wget jq ripgrep fd-find tree htop
```

- `build-essential`：gcc等。多くのソフトのビルドに必要
- `jq`：JSON整形
- `ripgrep`（コマンド：`rg`）：grepの高速版
- `fd-find`（`fd`）：findの高速版
- `htop`：プロセス監視

### Claudeに聞いてみよう⑤：私の開発向けセットアップ

> 私の用途は〔Webフロントエンド／データ分析／スクリプト／その他〕です。
> Debian で開発を始めるための共通パッケージを、apt、pipx、npm、cargo のどれで入れるべきか、優先順にリストしてください。
> 各パッケージの用途を一行で添えてください。

## 第六節 Claude Code のセットアップ

Claude Code は、ターミナル上でClaudeと対話しながらコードを読み書きするツール。この教科書の第4部の核だ。

```bash
# Node.js と npm が必要
sudo apt install nodejs npm

# Claude Codeのインストール（最新の手順はClaudeに確認）
npm install -g @anthropic-ai/claude-code
```

初回起動時にブラウザでログインを求められる。Anthropicのアカウントでログイン。

```bash
cd ~/Projects/my-project
claude
```

これで対話が始まる。

### Claude Codeの勘所

- **プロジェクトディレクトリで起動する**：そのディレクトリ配下のファイルを読める
- **明確に指示する**：「この関数を書き換えて」「この機能を追加して」のように
- **変更は確認する**：Claude Codeは変更前に確認を求める。常に中身を見てから承認

### Claudeに聞いてみよう⑥：Claude Code運用の原則

> Claude Code を使う際の、初心者が気を付けるべき原則を五つ教えてください：
> (1) 始め方（プロジェクトの組み方）
> (2) 指示の仕方
> (3) 変更の承認の判断
> (4) トラブル時の対処
> (5) 使ってはいけない場面

## まとめ

この章でやったこと：

1. ターミナルエミュレータを選び、フォントと配色を整えた
2. シェル（bash か zsh）を決め、`.bashrc` / `.zshrc` を整えた
3. エディタ（主にVSCode + Vim最低限）を構築した
4. Git を初期設定し、SSH鍵を作ってGitHubに繋いだ
5. 開発向け基本パッケージを入れた
6. Claude Code をインストールした

手元の状態：
- 手に馴染むターミナルとシェル
- Git が使えるエディタ環境
- Claudeとコードで対話できる環境

次の第14章では、具体的に**Widgetアーキテクチャ**——シンプルで再利用可能なUIコンポーネントの作り方——を題材に、Claude と一緒にコードを書く実例を進める。題材は小さなGUIアプリだが、考え方は別の領域にも転用できる。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
