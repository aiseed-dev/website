---
slug: claude-debian-18-when-things-break
number: "18"
title: 第18章 問題が起きた時の対処
subtitle: 起動しない、画面が出ない、アプリが動かない——段階的に戻す
description: Debianが起動しない、ログインできない、画面が真っ黒、アプリが落ちる——こうした危機をClaudeと段階的に切り分けて解決する。リカバリーモード、レスキューUSB、chroot 復旧の実践。
date: 2026.04.23
label: Claude × Debian 18
prev_slug: claude-debian-17-updates-maintenance
prev_title: 第17章 アップデートとメンテナンス
next_slug: claude-debian-19-growing-environment
next_title: 第19章 自分の環境を育てる
cta_label: Claudeと学ぶ
cta_title: 壊れた日ほど、冷静に。
cta_text: 最もまずい判断は「焦って再インストール」。この章の手順で段階的に切り分ければ、9割のトラブルはデータを保ったまま戻せる。
cta_btn1_text: 第19章へ進む
cta_btn1_link: /claude-debian/19-growing-environment/
cta_btn2_text: 第17章に戻る
cta_btn2_link: /claude-debian/17-updates-maintenance/
---

## 危機の段階

トラブルは次の段階で深刻化する。手前で止めれば、戻すのが楽だ。

1. **アプリが落ちる**：個別アプリの問題
2. **DEの一部が動かない**：パネルが出ない、アイコンが動かない
3. **ログインできない**：パスワード後に黒画面
4. **起動しない**：GRUBから進まない、カーネルパニック
5. **BIOSから先へ進まない**：ハードウェア疑い

各段階で、対処の道具が違う。

## 第一節 アプリが落ちる

### まず症状を特定

```bash
# コマンドラインから起動して、エラーメッセージを見る
アプリ名

# 例:Zed が落ちるなら
zed --foreground

# Flatpak アプリ(例: Chrome)なら
flatpak run --verbose com.google.Chrome
```

### よくある原因

- 拡張機能の衝突 → 一個ずつ無効化
- 設定ファイルの破損 → `~/.config/<アプリ名>/` をリネーム、デフォルトで起動
- メモリ不足 → `htop` でメモリ残量
- GPUアクセラレーションの問題 → `--disable-gpu` 等のフラグ

### Claudeに聞いてみよう①：アプリクラッシュの切り分け

> 次のアプリが起動直後に落ちます：〔アプリ名、バージョン〕
>
> コマンドラインから起動した出力：
> ```
> 〔エラー全文〕
> ```
>
> 原因の可能性を優先度付きで3つ挙げてください。
> 一つずつ試す手順を、破壊的でないものから順に。

## 第二節 DEの一部が動かない

### 症状例

- パネル／タスクバーが出ない
- アイコンをクリックしても反応しない
- アニメーションがカクつく
- 画面がちらつく

### 対処

```bash
# GNOMEの場合、Wayland 上で X11 キーを押せないので Tty に切り替え
# Ctrl + Alt + F3 でTTY3 にログイン

# DEを再起動
systemctl --user restart gnome-shell
# または
sudo systemctl restart gdm     # GNOMEのログインマネージャ
sudo systemctl restart sddm    # KDEの
sudo systemctl restart lightdm # Xfceの
```

### セッションを捨ててやり直す

`~/.config/` 内の特定アプリ設定、`~/.cache/` を削除して再ログイン。設定がリセットされるが、日常業務は戻る。

## 第三節 ログインできない

### 症状：パスワード入力後、画面が真っ黒

ログインマネージャからセッションに入れない場合、多くはセッションの設定かホームの権限の問題。

### 対処

1. **Ctrl + Alt + F3** でTTY（テキストコンソール）へ
2. テキストベースでログイン
3. `~/.xsession-errors` を見る

```bash
# エラーログ確認
less ~/.xsession-errors

# ホーム直下の設定ディレクトリを疑う
ls -la ~/ | grep -E "\.(config|cache|local)"

# キャッシュクリア
rm -rf ~/.cache/*
```

### Claudeに聞いてみよう②：ログイン不能の切り分け

> Debian の GUI にログインできません。パスワード入力後、画面が真っ黒になります。
> TTYには入れます。
>
> `~/.xsession-errors` の末尾：
> ```
> 〔最後の50行〕
> ```
>
> 原因と、次に試すべき手順を5つ、リスク順に提示してください。

## 第四節 起動しない

ここからが本番。**落ち着いて、一つずつ**。

### GRUBが出ない、またはGRUBで止まる

BIOSから起動順序を確認。誤って別のディスクを優先にしていないか。

### カーネルパニック

画面が真っ赤、または大量のエラーで止まる。

1. 再起動して、GRUBメニューが出たら `e` を押してエディットモード
2. `linux` で始まる行を探し、末尾に `nomodeset` を追加（GPU関連の問題回避）
3. Ctrl+X で起動

これで起動できれば、GPUドライバの問題が濃厚。`sudo apt install --reinstall <該当ドライバ>` を試す。

### 一つ前のカーネルで起動

GRUBメニューで「Advanced options for Debian」を選ぶと、過去のカーネルが並ぶ。一つ古いカーネルで起動してみる。

- 古いカーネルで起動できれば、最新カーネルの問題
- 古いカーネルも動かないなら、それ以外の問題

### Claudeに聞いてみよう③：起動不能の段階的診断

> Debianが起動しません。症状：
> ```
> 〔できれば画面を撮影した内容を文字で〕
> ```
>
> 次の順で切り分けたいです：
> (1) BIOS の起動順序
> (2) GRUB からカーネルオプションを追加（nomodeset等）
> (3) 一つ古いカーネルでの起動
> (4) レスキューモード
> (5) ライブUSBからのchroot
>
> 各段階の具体的な操作と、成功判定の仕方を教えてください。

## 第五節 ライブUSBからのchroot復旧

起動が全く不能になったときの最終手段。

### 準備

1. 第7章で使ったDebianインストーラのUSB（まだ持っているはず）を挿す
2. UEFIでUSB起動
3. インストーラの選択肢から「Rescue mode」または別PCで作った Debian Live USB

### 手順

```bash
# Rescueモードまたは Live USB で起動したら
# ディスクを確認
lsblk

# 暗号化されている場合は解除
sudo cryptsetup open /dev/nvme0n1p3 root_dm
# パスフレーズ入力

# 論理ボリュームを有効化（LVMの場合）
sudo vgchange -ay

# ルートをマウント
sudo mount /dev/mapper/<ルートLV> /mnt
sudo mount /dev/nvme0n1p2 /mnt/boot      # /boot が別パーティションの場合
sudo mount /dev/nvme0n1p1 /mnt/boot/efi

# 必要な仮想ファイルシステムを bind
for d in dev proc sys run; do
  sudo mount --bind /$d /mnt/$d
done

# chroot で本環境に入る
sudo chroot /mnt
```

ここから中で `apt`、`dpkg`、`update-initramfs`、`update-grub` などを叩いて復旧する。

### Claudeに聞いてみよう④：chroot後の復旧コマンド

> Debian Live USB から chroot で既存システムに入りました。
> 問題：〔カーネル更新後に起動しなくなった／GRUBが壊れた／/etc/fstabを壊した〕
>
> chroot内で実行すべき復旧コマンドを、順に示してください。
> 各コマンドの意味と、失敗したら次に何をするかも。

## 第六節 データを救う

最悪、システムを諦めて再インストールする場合でも、**データは救う**。

### ライブUSBからのマウント

```bash
# Live USBで起動
sudo mkdir /mnt/rescue
sudo mount /dev/mapper/<ルートLV> /mnt/rescue
cd /mnt/rescue/home/<あなた>

# 外付けSSDをマウント
sudo mkdir /mnt/backup
sudo mount /dev/sdc1 /mnt/backup

# コピー
sudo rsync -av . /mnt/backup/rescued-home/
```

これで、OSを再インストールしてもデータは守られる。

**この作業は第4章の「完全バックアップ」が事前にあれば不要**。事前の備えが、いざというときの安心になる。

## 第七節 再インストールという選択

どうしても復旧できない場合、**再インストールは失敗ではない**。

第12章で dotfiles と apt-manual.txt を Git 管理にしていれば、再インストール後は：

```bash
# 新Debian で
git clone https://github.com/あなた/dotfiles.git
cd dotfiles
./install.sh
./apt-restore.sh
```

これで数時間で元の環境が戻る。**「再インストールできる」こと自体が、Debianの強み**だ。

## 第八節 トラブル対処の心得

### 冷静を保つ

パニックになると、余計に壊す。コーヒーを淹れる、深呼吸する、紙に症状を書く——数分でも離れて戻ると、見える景色が変わる。

### 変更は一つずつ

復旧中に「これも」「あれも」とやると、何が効いたか分からない。**一つ試して、結果を見て、次に進む**。

### ログを取る

画面を撮影、コマンドの出力を保存、エラーメッセージをメモ。Claudeに渡す材料が、そのまま自分の将来の参考になる。

### 時間を区切る

「今晩で直す」と決めたら、ダメなら寝る。寝て起きると、答えが見えることが実に多い。

### Claudeに聞いてみよう⑤：トラブル時のテンプレ

> 私は次のトラブルに遭遇しています：〔症状〕
>
> これまで試したこと：〔箇条書き〕
> 現在の状況：〔箇条書き〕
> 手元にある道具：〔ライブUSB、別PC、スマホ、等〕
>
> 次に試すべき手順を、リスク順で3つ。各手順の所要時間の見込み、失敗時の次の一手を。
> 私が疲れてきたら、安全に一時停止する方法も添えてください。

## まとめ

この章でやったこと：

1. トラブルの五段階を分類した
2. アプリ／DE／ログイン／起動／BIOS段階の対処を整理した
3. ライブUSBからのchroot復旧を覚えた
4. データ救出の手順を用意した
5. 再インストールを最終選択として位置付けた
6. トラブル時の心得（冷静・一つずつ・ログ・時間）を確認した

手元に残ったもの：
- ライブUSBと外付けSSD（常備）
- トラブル時のテンプレプロンプト
- dotfiles + apt-manual.txt による「再インストールでも戻せる」安心

次の第19章では、**育てる**視点に入る。目の前を回すだけでなく、あなたのDebian環境を長期的に自分色に変えていく方法を扱う。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
