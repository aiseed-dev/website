---
slug: claude-debian-11-application-selection
number: "11"
title: 第11章 アプリケーションの選択
subtitle: Windowsで使っていたアプリを、Debianで何に置き換えるか
description: ブラウザ、メール、オフィス、画像・動画、コミュニケーション、ファイル同期、パスワード管理——カテゴリごとにWindowsアプリをDebianアプリに置き換える。Claudeと一緒に、用途に合わせた選択を下す。
date: 2026.04.23
label: Claude × Debian 11
prev_slug: claude-debian-10-japanese-input
prev_title: 第10章 日本語入力の設定
next_slug: claude-debian-12-config-management
next_title: 第12章 設定の理解と管理
cta_label: Claudeと学ぶ
cta_title: 代替は一つではない。
cta_text: 「Officeの代わりに何？」という問いには、文脈ごとに複数の答えがある。Claudeと対話して、あなたの用途にとっての最適を絞り込む。
cta_btn1_text: 第12章へ進む
cta_btn1_link: /claude-debian/12-config-management/
cta_btn2_text: 第10章に戻る
cta_btn2_link: /claude-debian/10-japanese-input/
---

## まず Flatpak を入れる

カテゴリごとの置き換えに入る前に、**Flatpak** を導入しておく。
Debian の `apt` だけでは、デスクトップアプリで困る場面が必ず出てくる。

### なぜ apt だけでは足りないか

Debian は安定性を最優先するディストリビューションで、`apt` が提供する
パッケージは **古めだが堅い**。これはサーバーや基盤ソフトには嬉しいが、
デスクトップアプリには逆風になることがある。

- **Slack / Zoom / Discord / Spotify**: 公式 deb はあるが配布が遅れがち、
  自動更新が信頼しづらい
- **Bitwarden / Signal / Element**: deb 提供はあるが、Flatpak 版のほうが
  常に最新
- **OBS Studio / Krita / Inkscape**: apt 版は数バージョン古い、
  最新機能を使うなら Flatpak が現実的
- **GIMP**: Debian の apt は安定版だが、Flatpak は次期版を含む

要するに、**Debian の `apt` は OS 基盤と "成熟したアプリ"** を扱い、
**Flatpak は "更新が速いアプリ"** を扱う、と役割を分けるのが現実的。

### Flatpak とは何か

Flatpak は Linux 用の **配布フォーマット + サンドボックス + 自動更新** の
セット。次の特徴がある。

- **どのディストロでも動く**: Debian / Ubuntu / Fedora / Arch のどこでも
  同じファイルが動く。アプリ作者が一度ビルドすれば多くの環境に届く
- **依存ライブラリを同梱**: アプリが必要とするライブラリを Runtime として
  バンドルし、システムの apt パッケージに干渉しない
- **サンドボックス**: 既定では各アプリがホームディレクトリ全体やシステムを
  自由に読み書きできない。`Documents/` だけ、`Downloads/` だけ、と権限を
  絞れる
- **自動更新**: Flathub から各アプリの新版が出ると `flatpak update` で一括
  更新される
- **権限の見える化**: `flatpak info --show-permissions <app>` でそのアプリが
  何にアクセスできるかを確認できる

すべての利点の裏返しとして、**ディスクを少し多く使う**(Runtime を
共有しても重複は出る)、**起動が apt 版より気持ち遅い**、という弱点がある。
ノート PC のディスクが残り 10 GB を切っているような状況では、Flatpak を
何でも入れる前に Runtime のサイズを意識する必要がある。

### セットアップ(3 分)

```bash
# Debian 12 / 13 で
sudo apt install flatpak

# GNOME の「ソフトウェア」と統合したい場合
sudo apt install gnome-software-plugin-flatpak

# Flathub(Flatpak アプリの最大の配布元)を登録
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# 一度ログアウト → ログインで PATH と .desktop が反映される
```

これで `flatpak install flathub <app-id>` でほぼあらゆるデスクトップアプリが
入る。

### 基本のコマンド

```bash
# 検索
flatpak search slack

# インストール(Flathub 指定推奨)
flatpak install flathub com.slack.Slack

# 起動(普通はメニューから / コマンドからも可)
flatpak run com.slack.Slack

# 一覧
flatpak list

# 全部更新
flatpak update

# 削除
flatpak uninstall com.slack.Slack

# 不要 Runtime を整理
flatpak uninstall --unused
```

### 権限を絞る(Flatseal)

サンドボックスの効果を最大化するなら、**Flatseal** という GUI を入れる。

```bash
flatpak install flathub com.github.tchx84.Flatseal
```

これで各アプリが「ホームディレクトリ全部見えていいか」「ネットワーク越しに
何でも繋いでいいか」「マイクは?」を細かく設定できる。**「Slack に Documents
を見せる必要はない」**といった判断を、後付けで適用できる。

これは Windows / macOS には標準で無い、**Linux ならではの透明性** だ。

### apt と Flatpak の使い分け

本書のおすすめ:

| 種類 | 推奨 | 理由 |
|---|---|---|
| Firefox | **apt**(`firefox-esr`)/ Flatpak も可 | Debian Security Team が ESR を高頻度バックポート、ネイティブ連携が楽 |
| Chromium / Chrome / Brave / Vivaldi | **Flatpak** | apt は遅れがち、Chrome は deb 入れ直しが面倒、サンドボックスが追加ボーナス |
| デスクトップ環境 / フォント / IME | **apt** | OS 基盤、Flatpak 化しても恩恵がない |
| LibreOffice | **apt or Flatpak** | apt 版で十分、最新機能が要るなら Flatpak |
| Slack / Zoom / Discord / Spotify | **Flatpak** | 更新の速さ + サンドボックス |
| Bitwarden / Signal / Element | **Flatpak** | 同上、暗号化アプリは新しいほうが安心 |
| OBS / Krita / Inkscape / GIMP(最新) | **Flatpak** | apt 版だと数バージョン古い |
| 開発ツール(Python / git / Docker) | **apt** | サンドボックスがむしろ邪魔 |
| エディタ・IDE(Zed / Neovim / PyCharm) | **Flatpak**(Neovim は apt) | 詳細は第 13 章。VS Code は本書では推奨しない |

### Snap には触れない

Ubuntu には Snap という似た仕組みがあるが、Debian では **Flatpak が事実上の
デファクト** で、Snap を入れる必要はほぼ無い。本書も Snap は扱わない。
Flatpak だけ覚えれば足りる。

### Claudeに聞いてみよう⓪:apt vs Flatpak の振り分け

> 私が Debian で使いたいアプリのリストは次の通りです:
> 〔アプリ名を列挙〕
>
> それぞれを apt と Flatpak のどちらで入れるべきか、推奨と根拠を
> 表で出してください。Flatpak の場合は権限で絞るべき項目(ファイル
> アクセス・ネットワーク・カメラなど)も提案してください。

これで準備が整った。各カテゴリの選択に進む。

## カテゴリ別に置き換える

第4章で作った依存関係マップを開きながら、次の八カテゴリで置き換えを決めていく。

1. ブラウザ
2. メール・カレンダー
3. オフィス（文書・表計算・プレゼン）
4. コミュニケーション（チャット・ビデオ会議）
5. 画像・動画・音声
6. ファイル同期・クラウドストレージ
7. パスワード管理・認証
8. ユーティリティ（PDF、スクリーンショット、クリップボード）

## 第一節 ブラウザ

ブラウザは攻撃面が一番広いアプリで、**更新の速さ** がほぼそのまま安全性に
直結する。ここだけは Firefox 系と Chromium 系で扱いを変える。

### Firefox は apt(`firefox-esr`)で十分

```bash
sudo apt install firefox-esr
```

Debian の Firefox-ESR は **Debian Security Team が継続的にバックポート** していて、
上流の Mozilla リリースとほぼ同日にセキュリティ修正が届く。Mozilla 自身も ESR を
「企業・サーバー向けの安定 + 即時セキュリティ」と公式に位置付けているので、
**「Debian で apt が古い」という典型問題が起きない数少ない例外**。

ネイティブメッセージング(KeePassXC / Bitwarden の連携)、YubiKey、
GNOME / KDE のデフォルトブラウザ統合 ── これらが全部素直に動く。

複数プロファイルを厳格に分離したい / 追加サンドボックスが欲しい場合は
Flatpak の `org.mozilla.firefox`(これも Mozilla 公式ビルド)も選べる。

### Chromium 系は Flatpak が現実解

Chromium / Chrome / Brave / Vivaldi は Firefox と事情が違う。

- **Chromium**: Debian の apt 版は **上流ゼロデイ修正から数日〜2 週間遅れる
  ことがある**(セキュリティチームの作業量次第)。ブラウザの 1 週間遅れは大きい
- **Google Chrome**: Debian の公式 apt リポジトリには無い。手段は (a) Google の
  deb をダウンロード、(b) Google の apt 第三者リポジトリを追加、(c) Flatpak。
  **(c) が一番簡単** ── レポジトリ追加もサインキーも要らず、`flatpak install`
  1 行で済む
- **Brave / Vivaldi**: 公式 deb もあるが、第三者 apt リポジトリが必要。
  Flatpak 版なら remote-add 不要

加えて Chromium 系は **Flatpak のサンドボックスが効きやすい** ── Firefox と
違ってプロセス分離は強力なものの、外側にもう一層被せると意味がある。
ブラウザは攻撃面が広いので、保険として妥当。

```bash
# 例
flatpak install flathub org.chromium.Chromium
flatpak install flathub com.google.Chrome
flatpak install flathub com.brave.Browser
flatpak install flathub com.vivaldi.Vivaldi
```

### Flatpak ブラウザの注意点

サンドボックスの代償として、次の連携は **追加設定が要る**:

- **パスワードマネージャのネイティブメッセージング**(KeePassXC-Browser、
  Bitwarden の自動入力):portal 経由の許可が必要、初回に Flatseal で
  通信ソケットを開ける
- **YubiKey 等のハードウェアトークン**:Flatseal で `Devices: All` を許可
- **VA-API ハードウェアデコード**(動画再生時の CPU 削減):環境変数の追加が
  apt 版より一手間多い
- **「デフォルトアプリで開く」**:portal 経由になるので一瞬間が空く

「業務でパスワード管理と SSO トークンを使う」「映像編集をしながら YouTube
を流す」── このあたりの頻度が高ければ apt 版(Firefox)を選ぶ価値が残る。

### 選ぶ軸

- **ブックマークとパスワードの同期**:今使っているブラウザから移行しやすいか
- **プライバシー**:広告・トラッカーへの態度
- **Electron アプリとの統合**:一部業務ツールは特定ブラウザ前提
- **更新速度** ⇒ Chromium 系なら Flatpak、Firefox なら apt-esr で十分

### 本書の推奨

- **Firefox は `apt install firefox-esr`** が第一選択
- **Chromium 系を使うなら Flatpak**(Chrome / Chromium / Brave / Vivaldi のどれも)
- 業務 SSO 等で Chrome 必須なら、迷わず Flatpak 版の `com.google.Chrome`

### Claudeに聞いてみよう①:ブラウザ移行

> 私は現在〔Edge / Chrome / Safari〕を使っています。ブックマーク、パスワード、
> 拡張機能、開いているタブを、Debian の〔Firefox(apt firefox-esr) /
> Chrome(Flatpak)〕に移すための手順を教えてください。
> データロスを最小限にするやり方と、移行後すぐに確認すべき項目を列挙して
> ください。あわせて、Flatpak 版を選んだ場合に Flatseal で確認すべき
> 権限項目(ファイルアクセス、ホームディレクトリ、ネイティブメッセージング、
> デバイス、ホスト D-Bus)も挙げてください。

## 第二節 メール・カレンダー

### 候補

- **Thunderbird**（`sudo apt install thunderbird`）：老舗、機能豊富、POP/IMAP/Exchange対応
- **Evolution**（`sudo apt install evolution`）：GNOME標準、Exchange連携が比較的強い
- **Geary**：シンプルで軽快、GNOMEに馴染む
- **ウェブメール**：Gmail／Outlookをブラウザで使い続ける選択肢もある

### Outlook（業務用）からの移行

Microsoft 365のExchange Onlineは、IMAPまたはMicrosoft純正のEWS経由でThunderbirdから読める。会社のIT部門がIMAPを許可していれば問題なく動く。

### 過去メールの移行

Outlookの`.pst`ファイルをThunderbirdにインポートするツールがある。

```bash
# ImportExportTools NG（Thunderbird拡張）
```

### Claudeに聞いてみよう②：メールクライアントの選択

> 私のメール環境は：
> - 仕事：〔会社ドメイン、Exchange Online／独自サーバー〕
> - 個人：〔Gmail / iCloud等〕
> - 過去メール：〔.pst、.mboxなど〕
>
> 最適なメールクライアントを推薦し、初期設定と過去メール移行の手順を教えてください。

## 第三節 オフィス

### LibreOffice（`sudo apt install libreoffice libreoffice-l10n-ja`）

Debianのオフィス代表。Writer（文書）、Calc（表計算）、Impress（プレゼン）、Draw（図）、Base（データベース）、Math（数式）。

**Officeファイルとの互換性の現実：**
- シンプルな文書は問題なし
- 表やフォーム、簡単な関数：ほぼ問題なし
- 複雑なExcelマクロ：壊れることがある
- PowerPointのアニメーション：微妙にずれる

### OnlyOffice（deb配布）

Officeファイルとの見た目の再現性は LibreOffice より高い。ビジネス文書で MS Office ユーザーと頻繁にやり取りするなら候補。

### Google Workspace / Microsoft 365 Online

「Officeファイルを完全に扱う必要があるときだけブラウザでオンライン版」という割り切りもあり。

### Claudeに聞いてみよう③：オフィス戦略

> 私は次の頻度でOfficeファイルを扱います：
> - Word：週〇件、自作か受領か、複雑度
> - Excel：〇件、マクロ有無、複雑度
> - PowerPoint：〇件、アニメ有無、複雑度
>
> LibreOffice、OnlyOffice、Microsoft 365 Online、Google Workspaceのどれを主に、どれを副にすべきですか。
> 互換性で事故りやすいポイントと回避策も教えてください。

## 第四節 コミュニケーション

### 候補

- **Slack**：公式 deb あり、または Flatpak
- **Microsoft Teams**：公式 Linux 版は停止、ブラウザ版を使う
- **Zoom**：公式 deb、動作良好
- **Discord**：公式 deb
- **LINE**：公式 Linux クライアントなし。LINE Web か 仮想マシン、もしくはスマホ主体
- **Signal / Element**：公式 deb

### LINE問題

LINEのデスクトップ Linux 版は公式に存在しない。選択肢：

1. LINE Web（ログインはQRでスマホから）
2. スマホをメインにする
3. Windows 仮想マシンに LINE を入れる

### Claudeに聞いてみよう④：コミュニケーションの残存問題

> 私が使うコミュニケーションツールは〔リスト〕です。
> Debianで各ツールを使う最良の方法（公式deb／Flatpak／Snap／Web版／代替）を表にしてください。
> LINEなどLinux非対応のものについては、使用頻度に応じた現実的な対処を提案してください。

## 第五節 画像・動画・音声

### 画像

- **GIMP**：Photoshop代替
- **Krita**：イラスト・デジタルペイント
- **Inkscape**：ベクター（Illustrator代替）
- **darktable / RawTherapee**：RAW現像（Lightroom代替）
- **Shotwell / digiKam**：写真管理

### 動画

- **DaVinci Resolve**：プロ向け編集、無料版で十分。Linux版あり
- **Kdenlive**：オープンソース編集ソフト
- **OBS Studio**：配信・録画
- **HandBrake**：エンコード

### 音声

- **Audacity**：波形編集
- **Ardour**：DAW
- **LMMS**：作曲

### Claudeに聞いてみよう⑤：クリエイティブツール

> 私は〔写真／動画／イラスト／音楽〕を〔頻度〕で扱います。現在使っているのは〔アプリ名〕です。
> Debianでの代替を、機能互換性と学習コストの観点で評価してください。
> 特に、失われる機能と、代わりに得られる機能を明確にしてください。

## 第六節 ファイル同期・クラウド

### 候補

- **Nextcloud**：セルフホスト可能、サブスク型サービスあり（OwnCloudの分派）
- **Syncthing**：P2Pで複数PC間同期。サーバー不要
- **Rclone**：様々なクラウドストレージへのCLIツール
- **OneDrive**：公式Linuxクライアントなし。非公式の `onedrive` CLI
- **Google Drive**：公式Linuxクライアントなし。`rclone` か GNOME Online Accounts
- **Dropbox**：公式Linux版あり
- **MEGA**：公式 Linux 版あり

### 本書の推奨

**自宅のNASと Syncthing、または Nextcloudのサブスク**。他社クラウドへの依存を減らす。

特に Syncthing はクラウド業者に依存せず、PCとスマホとNASの間で暗号化同期できる。ベンダーロックインの対極。

### Claudeに聞いてみよう⑥：同期戦略

> 私の同期対象は〔ドキュメント、写真、コード、音楽〕で、端末は〔Debian、スマホ、家族PC〕です。
> Syncthing、Nextcloud、rclone+既存クラウドのどれを主にすべきか、容量とプライバシーとコストの観点で推薦してください。

## 第七節 パスワード管理・認証

### 候補

- **Bitwarden**：サービス型、Linux公式クライアント、ブラウザ拡張
- **KeePassXC**（`sudo apt install keepassxc`）：ローカル保存、オープンソース
- **1Password**：公式Linux版あり、サブスク

### セキュリティキーとの連携

Yubikeyなどのセキュリティキーは、Linuxでも問題なく動く。`yubico-authenticator` パッケージで OATH 対応。

### Claudeに聞いてみよう⑦：パスワード管理

> 現在、〔Chromeのパスワードマネージャ／Apple キーチェーン／Bitwarden／その他〕を使っています。
> Debian環境での最良の選択と、現在のパスワードを安全にインポート／エクスポートする手順を教えてください。

## 第八節 ユーティリティ

### PDF

- **Evince / Okular**：閲覧
- **Xournal++**：注釈、手書き
- **pdftk-java**、**qpdf**：コマンドライン操作
- **LibreOffice Draw**：簡単な編集

### スクリーンショット

- **Flameshot**：高機能、注釈付き
- **GNOMEスクリーンショット**／**Spectacle**（KDE）：標準
- **Shutter**：豊富な機能

### クリップボード履歴

- **CopyQ**：クロスDE対応
- **KDE**：標準で Klipper
- **GNOME**：拡張の `Clipboard Indicator`

## 第九節 移行のペース

一度に全部移行しない。次の順で進める。

**一日目**：ブラウザ、メール、メッセンジャー（毎日必須のもの）
**一週目**：オフィス、クラウド同期、パスワード管理
**一ヶ月目**：画像・動画、ユーティリティ、特殊用途

優先度を付けて、焦らない。

### Claudeに聞いてみよう⑧：私のアプリ移行計画

> 私の依存関係マップ（`dependency-map.md` の B・D カテゴリ）と使用頻度を前提に、アプリ移行のスケジュールを一日目・一週目・一ヶ月目に分けて立ててください。
> 各項目にリスクレベル（移行失敗の影響度）を添えてください。

## まとめ

この章でやったこと：

1. 八カテゴリでWindowsアプリをDebianアプリに置き換えた
2. LINE、Teamsなど完全には置き換わらないものを正直に扱った
3. 移行ペース（一日・一週・一ヶ月）を設計した

手元の状態：
- 日常で使えるDebianアプリ一式
- 移行計画表

次の第12章「設定の理解と管理」では、Debianの設定ファイルの場所、dotfilesの管理、バックアップ、Gitでの追跡を扱う。自分の環境を**ドキュメントとして残す**作法を身につける。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
