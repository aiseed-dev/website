---
slug: claude-debian-08-first-troubleshooting
number: "08"
title: 第8章 最初のトラブルシューティング
subtitle: 画面、Wi-Fi、音、Bluetooth、サスペンド——出がちな七つをClaudeと潰す
description: インストール直後に遭遇しがちな七つのトラブル——画面の解像度・スケーリング、Wi-Fi、Bluetooth、サウンド、サスペンド、日本語入力、外部モニター——を、Claudeと一緒に段階的に解決する。ログの取り方と渡し方を身につける。
date: 2026.04.23
label: Claude × Debian 08
prev_slug: claude-debian-07-installation-execution
prev_title: 第7章 インストール実行の対話
next_slug: claude-debian-09-desktop-environment
next_title: 第9章 デスクトップ環境の選択
cta_label: Claudeと学ぶ
cta_title: 全部動かないのではない。一つずつ動かす。
cta_text: インストール直後に「なんか全部変」と感じても、冷静に一つずつ分解すれば、動かないのは2〜3個だけ。この章で、分解と対処の作法を身につける。
cta_btn1_text: 第3部 第9章へ進む
cta_btn1_link: /claude-debian/09-desktop-environment/
cta_btn2_text: 第7章に戻る
cta_btn2_link: /claude-debian/07-installation-execution/
---

## 「動かない」を分解する

インストール直後に「何か動かない」と感じたら、焦らず分解する。次の七つのカテゴリで、それぞれ動くか動かないかを確認する。

1. ディスプレイ（解像度、スケーリング、外部モニター）
2. Wi-Fi（繋がる、速度、安定性）
3. Bluetooth（マウス、キーボード、イヤホン）
4. サウンド（内蔵スピーカー、ヘッドフォン、マイク）
5. サスペンド／復帰（蓋を閉じて開ける、電源の省電力）
6. 日本語入力（Fcitx5＋Mozc）
7. 周辺機器（プリンタ、ウェブカメラ、USB機器）

**全部動くことは稀だ。2〜3個は何かある。それを一つずつ潰すのが第8章。**

## 第一節 診断の共通作法

### ログを取って渡す

Linux の強みは、何が起きているかが全部ログに残ることだ。トラブル時にClaudeに渡すべき情報は次の三種類。

**1. システムログ**
```bash
journalctl -b -p err        # 今回の起動以降のエラー
journalctl -b --since "10 min ago"   # 直近10分
```

**2. ハードウェア認識状況**
```bash
lspci -nnk                  # PCIデバイスとドライバ
lsusb                       # USBデバイス
dmesg | tail -50            # カーネルメッセージ末尾
```

**3. 特定サービスの状態**
```bash
systemctl status <サービス名>
systemctl --failed          # 失敗したサービス一覧
```

### Claudeに聞いてみよう（定型）：トラブル共通テンプレート

どのトラブルでも使える定型プロンプト。

> 私のDebian 12〔DE名〕で、〔症状〕が起きています。
>
> 機種：〔メーカー・モデル〕
> 直前にやったこと：〔操作〕
>
> 以下は私の環境の情報です：
> ```
> $ uname -a
> 〔出力〕
> $ lspci -nnk | grep -A 2 -i 〔関連キーワード〕
> 〔出力〕
> $ journalctl -b -p err
> 〔出力〕
> ```
>
> 原因候補を可能性の高い順に三つ挙げ、それぞれに対する確認手順を教えてください。
> 破壊的なコマンドは注意書きを付けてください。

このテンプレートがあると、Claudeの答えの質が跳ね上がる。

## 第二節 ディスプレイ系

### 症状：解像度が低い、文字がぼやける

多くはGPUドライバ関連。次を試す。

```bash
# 現在のドライバ確認
lspci -nnk | grep -A 2 VGA

# Intel / AMD は標準ドライバで動くことが多い
# NVIDIA は独立パッケージが要る場合がある
```

NVIDIAの独立GPUの場合、non-free-firmware リポジトリから `nvidia-driver` を入れる。

```bash
# /etc/apt/sources.list に contrib non-free non-free-firmware が入っているか確認
cat /etc/apt/sources.list

# 必要なら追加（Claudeに正確な書式を聞く）
sudo apt update
sudo apt install nvidia-driver
sudo reboot
```

### 症状：外部モニターが表示されない

```bash
# 接続されているディスプレイ
xrandr                      # X11 の場合
gnome-randr                 # Wayland の GNOME の場合（無ければ apt install）

# 解像度の設定
設定 → ディスプレイ → 配置と解像度
```

### 症状：HiDPI（高解像度）でUIが小さすぎる

- GNOME：設定 → ディスプレイ → スケール 125% または 150%
- KDE Plasma：システム設定 → 表示と監視 → グローバルスケール
- Xfce：少し手間。Claudeに`xfconf-query` での設定方法を聞く

## 第三節 Wi-Fi とネットワーク

### 症状：Wi-Fiが全く繋がらない

無線LANチップのファームウェアが入っていない可能性が高い。

```bash
# チップの型を特定
lspci -nnk | grep -A 2 -i net

# 認識状態
dmesg | grep -i firmware
```

`firmware-iwlwifi`（Intel）、`firmware-realtek`、`firmware-atheros` など、必要なファームウェアパッケージを入れる。

```bash
sudo apt install firmware-linux firmware-linux-nonfree
sudo reboot
```

### 症状：繋がるが遅い／切れる

2.4GHz帯が混雑している可能性。5GHz帯のSSIDがあればそちらに。省電力モードが悪さをしていることもある。

```bash
# 省電力の状況
iw dev <インタフェース名> get power_save
```

## 第四節 サウンド

### 症状：音が出ない

```bash
# サウンドデバイスの確認
pactl list sinks short

# ミキサー
pavucontrol             # GUIミキサー。無ければ apt install pavucontrol
```

よくある原因：
- デフォルトの出力が間違っている（HDMIに出ている、ミュート）
- ヘッドホン検出の自動切り替えが誤作動
- Bluetoothデバイスが優先されている

### 症状：マイクが拾わない

`pavucontrol` の「入力デバイス」タブで、入力レベルをチェック。ミュートされていないか、ゲインが0になっていないか。

## 第五節 Bluetooth

### 症状：Bluetoothデバイスが見つからない

```bash
# Bluetoothサービス
systemctl status bluetooth

# 起動していなければ
sudo systemctl enable --now bluetooth
```

一部のチップはファームウェアが要る。`dmesg | grep -i bluetooth` で確認。

## 第六節 サスペンド／復帰

### 症状：蓋を閉じて開いたら起動しない

この問題はノートPCで最も厄介。原因はカーネル・ドライバ・UEFI設定の組み合わせ。

**まず試す：**
- BIOS/UEFI設定で `S3 sleep` と `Modern Standby (S0ix)` の切り替え（あれば）
- GRUBのカーネルパラメータに `mem_sleep_default=deep` を追加

**Claudeに聞いてみよう：**

> 私の機種〔モデル〕で、サスペンドからの復帰に失敗します。
> 症状：蓋を閉じて5分以上経ってから開くと、画面が真っ黒のまま
> カーネル：〔uname -a の結果〕
>
> 試すべき手順を、効果が高い順に五つ教えてください。各手順の副作用と、戻し方も添えてください。

### 症状：バッテリーの減りが速い

```bash
# 電力消費の状況
sudo apt install powertop
sudo powertop
```

`powertop --auto-tune` で自動最適化を試す（ただし一部の最適化は使い勝手を下げるので注意）。

## 第七節 日本語入力

### Fcitx5＋Mozcの標準構成

```bash
sudo apt install fcitx5 fcitx5-mozc fcitx5-config-qt
```

インストール後、`im-config -n fcitx5` を実行。再ログイン。

キーバインド：半角/全角キー、またはCtrl+Space（設定で変更可）。

### 症状：特定アプリで日本語入力ができない

ElectronベースのアプリやSnapパッケージは、入力メソッドの仕組みが標準と違うことがある。

Claudeに聞いてみよう：

> Fcitx5＋Mozc の構成で、〔アプリ名〕だけ日本語入力ができません。
> 起動コマンドと環境変数：〔 env | grep -i xim や GTK_IM_MODULE 等の出力〕
>
> アプリ側で必要な環境変数、または設定を教えてください。

## 第八節 周辺機器

### プリンタ

Debianは CUPS 経由で多くのプリンタに対応。

```bash
sudo apt install cups
sudo systemctl enable --now cups
```

ブラウザで http://localhost:631 を開いてプリンタ追加。Canon / Epson / Brother は日本向けの別ドライバがメーカーサイトで提供されることがある。

### ウェブカメラ

```bash
# 認識確認
v4l2-ctl --list-devices

# テスト
sudo apt install cheese
cheese
```

## 第九節 「動かない」の優先順位

複数のトラブルが同時に出ているとき、次の順で潰す。

1. **Wi-Fi**（これが動かないと何も調べられない）
2. **ディスプレイ**（毎日使うもの）
3. **サウンド**（会議で困る）
4. **日本語入力**（日常業務の大半に影響）
5. **サスペンド／バッテリー**（常用で支障）
6. **Bluetooth**（無くても代替は多い）
7. **プリンタ、ウェブカメラ**（必要なときに対処）

一度に全部解決しようとしない。Wi-Fiが動けば、あとはClaudeと対話しながら順に潰せる。

### Claudeに聞いてみよう⑥：私のトラブル一覧を優先付け

> インストール直後の今、次のトラブルが起きています：
> - 〔症状1〕
> - 〔症状2〕
> - 〔症状3〕
>
> 上記を潰していく順番と、それぞれの想定所要時間、私がまず試すべき一歩を教えてください。

## 第十節 トラブル解決ログを残す

潰したトラブルは、必ずテキストファイルに記録する。

```markdown
# 私のDebianトラブル解決ログ

## 2026-04-24 Wi-Fi が繋がらなかった
- 症状：インストール直後、Wi-Fi一覧が空
- 原因：firmware-iwlwifi が未インストール
- 解決：sudo apt install firmware-iwlwifi; sudo reboot
- 参考：Claudeとの対話（保存先：〇〇）

## 2026-04-25 蓋を閉じて開くと画面が真っ黒
- 症状：サスペンド復帰失敗
- 原因：Modern Standby と Linux の相性
- 解決：BIOS で「Linux」モードに変更 + GRUB に mem_sleep_default=deep
```

このログが、将来あなたを助ける。同じ問題が再発したとき、同じ問題を他の人に相談されたとき、再インストールするとき。

## まとめ

この章でやったこと：

1. 共通の診断コマンド（journalctl, lspci, dmesg）を身につけた
2. ディスプレイ、Wi-Fi、音、Bluetooth、サスペンド、日本語入力、周辺機器の代表的トラブルを押さえた
3. 優先順位で潰していく作法を確立した
4. `troubleshooting-log.md` を作った

手元の状態：
- 日常で使えるDebian環境
- 躓いたときの自分専用のログ

ここで第2部（インストール）が終わる。次の第3部（第9〜12章）では、**日常環境の構築**に入る。デスクトップ環境の深い使いこなし、日本語入力の仕上げ、日常アプリケーションの選択、設定ファイルの管理を Claude と一緒に進める。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
