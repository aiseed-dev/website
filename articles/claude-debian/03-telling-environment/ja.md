---
slug: claude-debian-03-telling-environment
number: "03"
title: 第3章 自分の環境を Claude に伝える方法
subtitle: ハードウェア・ソフトウェアの情報を取り、構造化してClaudeに渡す
description: Claudeに的確な答えをもらうには、自分の環境を正確に伝える必要がある。Windows/macOS/Linux それぞれで環境情報を取り出す方法、出力の中から何を渡すかの取捨選択、Claudeが読みやすい形式にまとめる技術を扱う。
date: 2026.04.23
label: Claude × Debian 03
prev_slug: claude-debian-02-starting-conversation
prev_title: 第2章 Claude との対話の始め方
next_slug: claude-debian-04-dependency-inventory
next_title: 第4章 依存関係の棚卸し
cta_label: Claudeと学ぶ
cta_title: Claudeはエスパーではない。
cta_text: あなたのPCで何が動いているかを、Claudeに「見せる」方法が要る。その見せ方を身につけるのがこの章。一度身につけば、今後の全てのトラブル対応が速くなる。
cta_btn1_text: 第4章へ進む
cta_btn1_link: /claude-debian/04-dependency-inventory/
cta_btn2_text: 第2章に戻る
cta_btn2_link: /claude-debian/02-starting-conversation/
---

## なぜ「環境を伝える」専用の章があるか

第2章で「文脈を渡す」ことの重要さを書いた。第3章は、その文脈のうち最も具体的な部分——ハードウェアとソフトウェアの情報——を、どう取り出して、どう整えてClaudeに渡すかを扱う。

Debianのインストールに入る前に、今使っているPCの素性を把握しておく必要がある。CPUは64ビットか、メモリは何GBか、ストレージは何で、無線LANチップは何か、入っているソフトは何か。これらが分からないと、Claudeは一般論しか返せない。

この章の終わりに、あなたの手元には `my-system.md` という一枚のファイルが残る。これが第4章以降の全ての議論の土台になる。

## 第一節 今のOSから情報を取り出す

### Windowsからの情報取得

Windowsを使っているなら、PowerShell（スタート→「PowerShell」と打って起動）で次のコマンドを一つずつ実行する。

```powershell
# システム情報
Get-ComputerInfo | Select-Object CsName, CsManufacturer, CsModel, OsName, OsVersion, CsProcessors

# メモリ総量
(Get-CimInstance Win32_PhysicalMemory | Measure-Object Capacity -Sum).Sum / 1GB

# ストレージ
Get-CimInstance Win32_DiskDrive | Select-Object Model, Size, InterfaceType

# ネットワークアダプタ
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed

# グラフィックス
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion

# インストール済みソフト（抜粋）
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
  Select-Object DisplayName, DisplayVersion, Publisher |
  Where-Object { $_.DisplayName -ne $null } |
  Sort-Object DisplayName
```

### macOSからの情報取得

macOSを使っているなら、ターミナル（Spotlightで「terminal」）で次を実行する。

```bash
# ハードウェア概要
system_profiler SPHardwareDataType

# ストレージ
diskutil list

# ネットワーク
networksetup -listallhardwareports

# アプリ一覧
ls /Applications

# Homebrewで入れたもの（使っていれば）
brew list
```

### Linux（既にLinuxを使っている場合）からの情報取得

既にLinuxを触っているなら、次を実行する。これらはDebianに移行後も同じコマンドだ。

```bash
# CPU
lscpu

# メモリ
free -h

# ストレージ
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE

# PCIデバイス（GPU、無線LANなど）
lspci -nnk

# USBデバイス
lsusb

# 入っているパッケージ（Debian/Ubuntu系）
dpkg -l | awk '{print $2, $3}' | head -50

# カーネルと発行版
uname -a
cat /etc/os-release
```

### Claudeに聞いてみよう①：コマンド群を自分のOS向けに調整

> 私は現在〔Windows 11 / macOS Sonoma / Ubuntu 22.04 など〕を使っています。
> この章の「環境情報を取り出すコマンド集」を、私のOSに合わせて一度に流せる形にまとめてください。
> 各コマンドが何を取るものかのコメントを添えてください。Claudeに渡すときに見やすいように、出力はMarkdownのコードブロックで返す形にしてください。

Claudeにコマンドを整形してもらう発想自体が、この本の流儀だ。自分で覚える必要はない。

## 第二節 出力から「Claudeに渡すべき部分」を選ぶ

### 全部渡すとノイズになる

`Get-ComputerInfo` や `lspci -v` の出力は、全部貼ると数百行になる。全部渡すとClaudeが迷う。**渡すべきはポイントを絞った要約だ。**

以下の項目を拾って、一枚のMarkdownファイルに整える。

### `my-system.md` の骨格

```markdown
# 私のシステム情報（2026-04-23 時点）

## 機械
- メーカー / モデル / 年式：
- CPU（モデル名、コア数、周波数）：
- メモリ：〇GB
- ストレージ：〇GB（SSD/HDD、NVMe/SATA）
- GPU：
- ディスプレイ：解像度、内蔵/外付け
- 無線LANチップ（Intel AX210, Realtek RTL8821CE 等）：
- Bluetooth：有/無
- 指紋認証・顔認証：有/無、メーカー・型番
- USB ポート構成：Type-A ×〇、Type-C ×〇、Thunderbolt 有/無

## 現在のOS
- OS名・バージョン：
- BitLocker/FileVault の有効/無効：
- Secure Boot の有効/無効：
- TPM：有無とバージョン

## 日常的に使うソフト
- ブラウザ：
- メール：
- オフィス：
- 画像編集：
- 音楽・動画：
- 仕事で必須のもの：

## 周辺機器
- プリンタ（メーカー、モデル）：
- スキャナ：
- ペンタブレット：
- 外付けモニター：

## ネットワーク環境
- 自宅の Wi-Fi（2.4/5/6 GHz、暗号化方式）：
- 職場の VPN の種類（もしあれば）：
- 日本語入力の現在の方法：
```

各項目に、第一節で取ったコマンドの出力から該当する情報を入れる。全項目を埋める必要はない。分からない項目は「不明」と書いておく。

### 「無線LANチップ」と「GPU」が特に重要

Debianインストールで最初に引っかかるのはこの二つだ。

- **無線LANチップ**：ノートPCは機種ごとに違う。Intel系はほぼ問題なく動く。Broadcomと一部Realtekはファームウェアが別途必要。
- **GPU**：内蔵グラフィックス（Intel、AMD）は問題ない。NVIDIA独立GPUはドライバで少し手間がかかる。

この二つは、必ず `my-system.md` に書き込む。後でClaudeに「私のチップでDebianは安定しますか」と聞くと、具体的な答えが返る。

### Claudeに聞いてみよう②：取った情報の整形を依頼

> 私のPCから次の情報を取りました。〔第一節のコマンドの出力を貼る〕
>
> これを、私の `my-system.md` の骨格に整えてください：
> 〔上のテンプレートを貼る〕
>
> 分からない項目は「要確認」と書き、それを調べるためのコマンドを添えてください。

この一往復で、あなたの手元にシステム情報の要約ファイルができる。

## 第三節 Claudeにとって読みやすい書き方

### Claudeが得意な形式

Claudeは次の形式を特に読みやすい。

- **Markdownの見出しと箇条書き**：階層構造が明確で、どこに何があるか迷わない
- **表**：項目と値の対応が明確
- **コードブロック**：コマンドの出力や設定ファイルは必ず ``` で囲む
- **短い段落**：一段落3〜4行まで

逆に、次は避ける。

- スクリーンショットの画像（OCRの手間がかかる）
- PDFの貼り付け（レイアウトが壊れて読めない）
- 絵文字の装飾的な多用（処理コストが上がる）
- 3000行を超える超長文（途中から注意が薄れる）

### ファイル全体をまるごと渡すコツ

`my-system.md` のような設定ファイルやログは、Claudeに「ファイル名を明示して」渡す。

```
my-system.md:
〔ファイルの中身をそのまま貼る〕
```

この書き方をすると、Claudeは「これはファイルだ」と認識して、後の対話で「`my-system.md` の GPU 欄を書き換えてください」のように名前で参照できる。

### Claudeに聞いてみよう③：書き方そのものを検証

> 次の二つの書き方のどちらが、Claudeにとって扱いやすいですか。理由も添えてください。
>
> A：「私のPCはDell Latitude 7420で、メモリは16GB、CPUはi7、ストレージは512GBのSSDで、無線はIntelの何かです」
>
> B：
> ```
> - メーカー / モデル：Dell Latitude 7420（2021）
> - CPU：Intel Core i7-1165G7（4コア8スレッド、最大4.7GHz）
> - メモリ：16GB DDR4-3200
> - ストレージ：Samsung PM981a 512GB（NVMe SSD）
> - 無線LAN：Intel Wi-Fi 6 AX201
> ```

Claudeは後者を推すはずだ。以降、自分もそういう書き方をする。

## 第四節 プライバシーを守りながら渡す

### 見落としがちな情報漏れ

環境情報の中には、そのままClaudeに渡すべきでないものが混じる。

- **シリアル番号**：PCのシリアルは、保証や盗難対応に使える情報。渡す必要はない
- **MAC アドレス / BSSID**：家の Wi-Fi のMACアドレスや BSSID は、場所特定に繋がる
- **ユーザー名を含むパス**：`C:\Users\John_Smith\Documents\` の `John_Smith` は本名の一部
- **メールのフォルダ名**：取引先名や個人名が入っていることが多い
- **ホスト名**：会社名を含むことがある

### 渡す前に一度読み返す

コマンドの出力をコピーしたら、**貼り付ける前に一度目で読む**。気になる文字列があれば、`[REDACTED]` などに置き換える。

```
# 置き換え例
ホスト名：YAMADA-LATITUDE-7420  →  [hostname]
ユーザー名パス：C:\Users\yamada\  →  C:\Users\[user]\
MAC：A1:B2:C3:D4:E5:F6  →  [mac]
```

これだけでClaudeの答えの質は変わらない。プライバシーは守られる。

### Claudeに聞いてみよう④：情報の機微を確認

> 次のテキストをClaudeに渡す前に、プライバシーの観点で置き換えるべき箇所を指摘してください：
>
> 〔自分が集めた情報を貼る〕
>
> 置き換え後の推奨表記も添えてください。

Claudeに情報の機微を判断させるのは逆説的だが、実用上うまく機能する。一度この作業をすると、次回からは自分で気付くようになる。

## まとめ

この章でやったこと：

1. 現OSから環境情報を取り出すコマンドを実行した
2. 出力から「Claudeに渡すべき要点」を選別した
3. `my-system.md` に一枚にまとめた
4. 書き方の形式（Markdown、表、コードブロック）を整えた
5. プライバシー上問題のある情報を置換した

手元に残ったもの：
- `my-system.md`（自分のシステム情報要約）
- 第2章で作った `my-claude-profile.md` と並べると、あなたの「Claudeに渡すセット」が完成する

次の第4章では、この環境情報を元に、**依存関係の棚卸し**をする。「このソフトは何に依存しているか」「このデータは何に紐付いているか」を Claude と一緒に整理して、Windows を消す前に確認すべきものを全て洗い出す。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
