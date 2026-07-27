---
slug: claude-debian-13-dev-tools
number: "13"
title: 第13章 開発ツールの構築
subtitle: ターミナル、シェル、エディタ、Git——ビルダーの道具を揃える
description: Debianに開発のための基盤を整える。ターミナルエミュレータ、シェル（bash/zsh/fish）、エディタ（Zed/Neovim/PyCharm Community）、Git、SSH鍵。Claudeと一緒に、自分のワークフローに合った道具立てを決める。
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

### 本書の三つの推奨

VS Code は人気だが、本書では **あえて選ばない**。Microsoft 製で、テレメトリ
の挙動・拡張機能の肥大・「全部入り」の重さが、Markdown と Python と
テキストで仕事をする AI ネイティブな道具立てと噛み合わない。

代わりに、**用途と気質で選べる三つ** を推す。

#### 1. Zed ── 余計な機能が一切ない超高速 GUI

VS Code からノイズと重さだけを完全に消し去り、**純粋にテキストと向き合いたい**
ならこれ。Rust + GPU レンダリングで起動から入力反応までが圧倒的に速い。
LSP・Copilot/Claude 連携も最初から入っているので、機能で困らない。
拡張地獄から抜けたい人向け。

```bash
# Flatpak が一番楽
flatpak install flathub dev.zed.Zed
```

#### 2. Neovim ── ターミナル完結の極致

マウスすら不要になる。**画面の左にエディタ、右に Claude(または `tmux` で
分割)を置き、手元(キーボード)の操作だけで全てを最速で完結させたい**ならこれ。
SSH 越しのサーバ作業もそのまま同じ操作で続く。

```bash
sudo apt install neovim
```

最低限の設定(LSP, treesitter, Telescope) は LazyVim や AstroNvim を使えば
1 分で完了。Vim キーバインドは一度覚えると 10 年 20 年使い続けられる。

#### 3. PyCharm Community ── 圧倒的なコード解析力を持つ堅牢な要塞

無料の Community 版で十分。**AI が書いたコードの構造的なミスを許さず、
自社プロダクトのロジックを安全に守り抜く** ならこれ。型推論・リファクタ・
デバッガの完成度は Zed と Neovim を圧倒する。Python が主な業務なら第一選択。

```bash
# Flatpak から
flatpak install flathub com.jetbrains.PyCharm-Community
```

### どう選ぶか

| 気質・用途 | 選ぶ |
|----------|-----|
| 静寂と速度、UI の美しさを優先 | **Zed** |
| キーボード完結、SSH 越しでも同じ操作、長期投資 | **Neovim** |
| 大規模 Python コード、リファクタ多発、業務責任 | **PyCharm Community** |

迷ったら **Zed から始める**。学習コストが一番低い。Vim キーバインドが
気に入れば Neovim に降りていけばいいし、Python の業務が増えたら
PyCharm を併用すればいい。

### Vim 最低限は別途身につける

主エディタが Zed でも PyCharm でも、**サーバーに入ったときに `vim` が触れる**
のは最低限の基礎教養。

```
hjkl        カーソル移動
i           挿入モード
Esc         ノーマルモードに戻る
:w          保存
:q          終了
:wq         保存して終了
:q!         保存せず終了
```

これだけ覚えれば `sudo vim /etc/〇〇` の場面で困らない。
Neovim を主にすれば、これも自然に身につく。

### Claudeに聞いてみよう③:エディタ構成

> 私は〔現在の主力エディタ:Word / メモ帳 / VS Code / その他〕で、
> 書くのは〔日本語の文書 / Python / Markdown / その他〕が中心です。
> Zed / Neovim / PyCharm Community の三つから、私の用途に合うのは
> どれか、選定の根拠と最初の 30 分で何を設定すべきかを教えてください。
> 副・緊急時用に何を併用するかも提案してください。

## 第四節 Git

### 初期設定

```bash
sudo apt install git

# ユーザー情報
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# エディタ(コミットメッセージなどを開く既定エディタ)
git config --global core.editor "zed --wait"    # Zed の場合
# git config --global core.editor "nvim"        # Neovim の場合
# git config --global core.editor "charm"       # PyCharm の場合(JetBrains Toolbox から)

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

Claude Code は、ターミナル上で Claude と対話しながらコードを読み書きする
ツール。この教科書の第 4 部の核だ。

### 推奨: ネイティブインストーラ

2025 年以降、**ネイティブインストーラが推奨**になった。Node.js / npm に
依存せず、**バックグラウンドで自動更新**される。

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

これだけで `~/.local/bin/claude` 等に配置される。インストール後、
新しいシェルで `claude --version` が通ることを確認。

> 補足: macOS / Linux / WSL すべて同じスクリプトで入る。
> Debian / Fedora / RHEL / Alpine では `apt` `dnf` `apk` 経由でも入る
> (Anthropic の公式リポジトリを案内に従って追加する形)。
> 古い「`npm install -g @anthropic-ai/claude-code`」方式は今でも動くが、
> **ネイティブ版に乗り換える**のが今後の正解。

### 初回ログインと起動

```bash
# 初回:ブラウザが開いて Anthropic アカウントでログイン
claude

# プロジェクトディレクトリに入って起動
cd ~/Projects/my-project
claude
```

これで対話が始まる。プロジェクトのファイルが Claude から見える状態。

### Claude Code の勘所

- **プロジェクトディレクトリで起動する**: そのディレクトリ配下のファイルを読める
- **明確に指示する**: 「この関数を書き換えて」「この機能を追加して」のように
- **変更は確認する**: Claude Code は変更前に確認を求める。常に中身を見てから承認
- **`/help` で機能を覚える**: 起動中に `/` を打つとスラッシュコマンド一覧
- **CLAUDE.md でプロジェクト文脈を残す**: ルートに置くと毎回読み込まれる

### Claudeに聞いてみよう⑥:Claude Code 運用の原則

> Claude Code を使う際の、初心者が気を付けるべき原則を五つ教えてください:
> (1) 始め方(プロジェクトの組み方)
> (2) 指示の仕方
> (3) 変更の承認の判断
> (4) トラブル時の対処
> (5) 使ってはいけない場面

## まとめ

この章でやったこと：

1. ターミナルエミュレータを選び、フォントと配色を整えた
2. シェル（bash か zsh）を決め、`.bashrc` / `.zshrc` を整えた
3. エディタ（Zed / Neovim / PyCharm Community のいずれか + Vim 最低限）を構築した
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
