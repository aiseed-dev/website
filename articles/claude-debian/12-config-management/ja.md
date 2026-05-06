---
slug: claude-debian-12-config-management
number: "12"
title: 第12章 設定の理解と管理
subtitle: dotfiles と apt を Git で追跡する
description: Debianの設定ファイルは全て開かれたテキスト。これをGitで管理すれば、あなたの環境は再現可能なドキュメントになる。dotfiles、aptパッケージ一覧、自動復元スクリプトまで、Claudeと設計する。
date: 2026.04.23
label: Claude × Debian 12
prev_slug: claude-debian-11-application-selection
prev_title: 第11章 アプリケーションの選択
next_slug: claude-debian-13-dev-tools
next_title: 第13章 開発ツールの構築
cta_label: Claudeと学ぶ
cta_title: 環境は、ドキュメントとして残せる。
cta_text: 二度目のインストール、新しいPCへの移行、別PCへの複製——全部コマンド一発になる。これがDebianの最大の強みの一つだ。
cta_btn1_text: 第4部 第13章へ進む
cta_btn1_link: /claude-debian/13-dev-tools/
cta_btn2_text: 第11章に戻る
cta_btn2_link: /claude-debian/11-application-selection/
---

## 設定ファイルがテキストである意味

Debianでは、OS・アプリの設定の大半が**テキストファイル**で管理されている。これはWindowsやmacOSとの決定的な違いだ。

レジストリでも、不透明なバイナリでもない。テキストなので：
- 読める（何がどう設定されているか把握できる）
- 変更できる（自分の手で編集できる）
- 差分が取れる（変更前後をdiffで比較できる）
- Git管理できる（履歴を残し、複数PCで共有できる）

この章では、自分の環境をGitで追跡可能なドキュメントにする作法を身につける。

## 第一節 設定ファイルの場所

### 三つの階層

**1. システム全体の設定**：`/etc/` 配下
`/etc/ssh/sshd_config`、`/etc/apt/sources.list`、`/etc/fstab` など。編集には `sudo` が要る。

**2. ユーザー固有の設定**：`~/.config/` と `~/.〇〇` 配下
`~/.config/fcitx5/`、`~/.config/Code/`、`~/.bashrc`、`~/.gitconfig`。ホームディレクトリにある。

**3. アプリ固有の設定**：様々な場所
`~/.mozilla/firefox/` のようにアプリごとに固有。

### よく触る設定ファイル(例)

```
~/.bashrc                       # bash の設定
~/.profile                      # ログインシェルの設定
~/.gitconfig                    # git のユーザー情報
~/.ssh/config                   # SSH 接続の定義
~/.config/fcitx5/               # 日本語入力
~/.config/zed/settings.json     # Zed エディタの設定
~/.config/nvim/                 # Neovim の設定(init.lua / lazy-lock.json)
~/.config/JetBrains/PyCharmCE2026.1/  # PyCharm Community の設定
~/.config/autostart/            # 自動起動アプリ
```

## 第二節 dotfiles を Git で管理する

### dotfiles リポジトリを作る

ホームディレクトリ直下の「ドット始まり」ファイルを総称して dotfiles と呼ぶ。これをGit管理する。

```bash
# dotfilesディレクトリを作る
mkdir ~/dotfiles
cd ~/dotfiles
git init

# 個人用のGitHub/GitLab等にリポジトリを作り、プッシュ
```

### シンボリックリンク方式

元のファイルを dotfiles/ に移して、シンボリックリンクを張る。

```bash
# 例：.bashrc を管理下へ
mv ~/.bashrc ~/dotfiles/bashrc
ln -s ~/dotfiles/bashrc ~/.bashrc

# 例：.gitconfig を管理下へ
mv ~/.gitconfig ~/dotfiles/gitconfig
ln -s ~/dotfiles/gitconfig ~/.gitconfig
```

### 機密情報を分離する

APIキー、アクセストークン、パスワードは dotfiles に含めない。

- `.bashrc` 本体は Git 管理
- `.bashrc.local` に機密項目を書き、`.bashrc` から `source` する
- `.bashrc.local` は `.gitignore` で除外

### Claudeに聞いてみよう①：dotfilesの設計

> 私は自分の Debian 環境を dotfiles として Git 管理したいです。
> 現在、〔bashrc, gitconfig, ssh/config, fcitx5 設定, Zed/Neovim 設定〕を
> 管理対象にしたいです。
>
> (1) 推奨のディレクトリ構造
> (2) シンボリックリンクを自動で張る install スクリプト
> (3) 機密情報の分離方法
> (4) 新しいPCでクローンして復元する手順
>
> を教えてください。スクリプトは POSIX sh で。

返ってきた構造をベースに、自分で調整する。

## 第三節 aptパッケージ一覧を再現可能にする

### 現在入っているパッケージを記録

```bash
# 手動で入れたパッケージの一覧
apt list --manual-installed > ~/dotfiles/apt-manual.txt

# または dpkg で全パッケージ
dpkg --get-selections > ~/dotfiles/packages.txt
```

### 別PCで同じ構成を再現

```bash
# packages.txtから復元
sudo dpkg --set-selections < packages.txt
sudo apt-get dselect-upgrade
```

### 日常的に足したパッケージを追記する習慣

アプリを一つ入れるたびに、`apt-manual.txt` を更新して Git にコミット。面倒なら月一回まとめてやる。

```bash
# 月次更新スクリプトの雛形
apt list --manual-installed > ~/dotfiles/apt-manual.txt
cd ~/dotfiles
git add apt-manual.txt
git commit -m "apt: $(date +%Y-%m) $(wc -l < apt-manual.txt) packages"
```

### Claudeに聞いてみよう②：再現スクリプト

> 私のdotfiles/配下に `apt-manual.txt` があり、そこに入れたパッケージ名が並んでいます。
> 新しいDebian 12に、このリストを元に全パッケージを入れるシェルスクリプトを書いてください。
> エラー処理（パッケージが存在しない場合の継続、権限確認、ミラー到達確認）を含めて、POSIX shで。

## 第四節 /etc の変更を追跡する

### etckeeper で自動追跡

```bash
sudo apt install etckeeper
```

`etckeeper` は `/etc/` 配下をGitリポジトリとして自動管理する。apt でパッケージを入れると、その時点の `/etc/` 全体がコミットされる。手動編集もコミットできる。

```bash
# /etc/ssh/sshd_config を編集したあと
sudo etckeeper commit "sshd: PermitRootLogin no に変更"
```

これで、システム設定の全変更履歴が残る。「いつ、何を変えたか」が全部分かる。

## 第五節 ホームディレクトリのバックアップ

dotfiles は設定だけ。写真、書類、プロジェクトなどのデータは別途バックアップが必要。

### rsyncで外付けSSDへ

```bash
# 外付けSSDに /mnt/backup としてマウント
rsync -av --delete --exclude='.cache' --exclude='node_modules' \
  ~/ /mnt/backup/home-$(hostname)/
```

- `--delete`：元で消したファイルをバックアップ先からも消す
- `--exclude`：キャッシュや再生成可能なものは除外

### Timeshift でシステムスナップショット

```bash
sudo apt install timeshift
```

Timeshift は**システム領域**のスナップショットを取る。`/home/` は通常対象外。アップデートで何か壊れたときの復旧に使える。

ホームのバックアップは rsync または Syncthing、システムのスナップショットは Timeshift、という二重構成が実用的。

### Claudeに聞いてみよう③：バックアップ戦略

> 私の Debian PC の構成：
> - 主データ場所：~/Documents, ~/Pictures, ~/Projects
> - 保存先候補：外付けSSD 2TB、NAS、クラウド（〇〇）
>
> 次の要件を満たすバックアップ戦略を立ててください：
> - 日次の自動バックアップ
> - 週次の完全コピー
> - 月次のオフサイト保管
> - 1ファイル誤削除からの復旧
> - OS全損からの復旧
>
> 必要なツール、cron設定、手順を具体的に。

## 第六節 再インストールのシミュレーション

### 一度やってみる

この章の仕上げとして、**もう一台のPCまたは仮想マシンで、dotfilesからの復元を試す**。

```bash
# 新しいDebianに初回ログイン後
cd ~
git clone https://github.com/あなた/dotfiles.git
cd dotfiles
./install.sh          # リンクを張る
./apt-restore.sh      # パッケージを入れる
./post-install.sh     # DE設定、fcitx5、等
```

この一連が**成功してこそ、あなたの環境はドキュメント化された**と言える。やってみて詰まった箇所を修正する。

### 成功の定義

- 新規PCでクローン＋スクリプト実行で、日常作業ができる状態になる
- 完璧でなくていい。9割復元できて、残り1割は手で調整できる程度
- スクリプトの所要時間は合計30〜60分を目標

## 第七節 Claudeを設定管理の相棒にする

### 変更をClaudeに要約させる

定期的に、dotfiles の変更履歴を Claude に要約させる。

> 次のgit logを要約してください：
> ```
> 〔git log --oneline -n 30 の出力〕
> ```
> 私の Debian 環境が過去一ヶ月でどう変化したか、傾向を教えてください。

意識していなかった変化の方向性が見える。

### エラー時に全環境を渡す

何かトラブったとき、dotfiles 一式とシステム情報を Claude に渡す。

> 私の環境は次の通りです：
> - `my-system.md` 〔貼る〕
> - `~/.bashrc` 〔貼る〕
> - `~/.config/fcitx5/` の主要ファイル 〔貼る〕
>
> 次の症状について、原因を特定してください：〔症状〕

情報量が多いほど、Claudeの判断は具体的になる。

## まとめ

この章でやったこと：

1. 設定ファイルの三階層（system / user / app）を把握した
2. dotfilesをGit管理に乗せ、シンボリックリンクで運用を始めた
3. aptパッケージ一覧を `apt-manual.txt` として記録・復元可能にした
4. `/etc/` の変更を `etckeeper` で自動追跡するようにした
5. rsync と Timeshift でバックアップ戦略を組んだ
6. dotfilesからの復元を実際に試した（または計画した）

手元に残ったもの：
- `dotfiles/` リポジトリ（GitHub/GitLab 等でバックアップ）
- 再現可能な環境のドキュメント
- 月次で更新する習慣

ここで第3部が終わる。**あなたのDebian環境は「作って使うだけ」から「再現可能な設計図」に進化した**。これは Windows では構造的に難しかったことだ。

次の第4部（第13〜16章）では、開発環境の構築に入る。ターミナル、エディタ、Git、言語環境、そして Claude Code——これらを Debian 上で組み合わせて、ビルダーとしての一歩を踏み出す。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
