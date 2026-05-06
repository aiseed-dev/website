---
slug: claude-debian-17-updates-maintenance
number: "17"
title: 第17章 アップデートとメンテナンス
subtitle: 日常を崩さずにシステムを最新に保つ
description: Debianのアップデートの考え方、安全な手順、ディスク整理、ログの見方。月次・年次のメンテナンスリズム、メジャーアップグレード（Debian 12→13）の準備。Claudeと一緒に、長く使える状態を維持する。
date: 2026.04.23
label: Claude × Debian 17
prev_slug: claude-debian-16-python-flutter-other
prev_title: 第16章 Python、Flutter、その他の環境
next_slug: claude-debian-18-when-things-break
next_title: 第18章 問題が起きた時の対処
cta_label: Claudeと学ぶ
cta_title: 毎日使い続けるために、週一で世話をする。
cta_text: Debianは放っておいても動くが、定期的な世話をすれば長く快適に動く。週一、月一、年一のリズムを作れば、トラブルの9割は予防できる。
cta_btn1_text: 第18章へ進む
cta_btn1_link: /claude-debian/18-when-things-break/
cta_btn2_text: 第16章に戻る
cta_btn2_link: /claude-debian/16-python-flutter-other/
---

## アップデートの三層

Debianのアップデートは三つの層に分かれる。

1. **パッケージのマイナー更新**:セキュリティパッチ、バグ修正。週1〜月1
2. **ポイントリリース**:Debian 12.x → 12.x+1(半年に一度くらい)
3. **メジャーアップグレード**:Debian 12 → Debian 13(2年に一度くらい)

それぞれ扱いが違う。同じコマンドで済まそうとすると、ある日壊れる。

加えて、第 11 章で Flatpak を導入した以上、**「apt と Flatpak の二系統を
同時に回す」** が今の Debian 運用の基本姿勢になる。

| 配布元 | 何が入っている | 更新コマンド | 頻度 |
|---|---|---|---|
| **apt** | OS 基盤、シェル、開発ツール、Firefox-ESR | `sudo apt upgrade` | 週 1 |
| **Flatpak** | Chromium 系ブラウザ、Slack/Zoom、Bitwarden、Krita 等 | `flatpak update` | 週 1(自動でも可) |
| **uv tool** | Python 製 CLI(`pre-commit`、`httpie`、`ruff` 等) | `uv tool upgrade --all` | 月 1 |
| **miniforge / conda** | DS / ML 環境(PyTorch + CUDA、GDAL、scipy など) | `conda update --all -n <env>` | 月 1(プロジェクト単位) |

apt 側だけ更新して Chromium が古いまま放置 ── これが一番ありがちな落とし穴。
**全系統を同じ曜日に走らせる**スクリプトを作るのが本書の推奨。

## 第一節 パッケージのマイナー更新

### 基本コマンド

```bash
# パッケージリストを最新に
sudo apt update

# 実際に更新
sudo apt upgrade

# 不要になったパッケージを削除
sudo apt autoremove

# ディスクの空き容量を戻す
sudo apt clean
```

### やる頻度

- 一週間に一度で十分（月曜の朝などリズムを決める）
- 急ぎの脆弱性パッチ（カーネル、ブラウザ）があるときは、週中でも適用

### unattended-upgrades で自動化

セキュリティ更新だけは自動で入れる設定ができる。

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

これで、バックグラウンドでセキュリティ更新が適用される。ただし再起動が必要なカーネル更新は手動で再起動する。

### Flatpak 側の更新

```bash
# 全 Flatpak アプリと Runtime を更新
flatpak update -y

# 不要 Runtime を整理(ディスクが膨らむ最大要因)
flatpak uninstall --unused -y

# 各アプリの権限を見直す(Flatseal でも可)
flatpak info --show-permissions com.google.Chrome
```

ブラウザ(Chromium 系)を Flatpak で入れたなら、**ここがセキュリティ上の主戦場**。
apt の `firefox-esr` は週次で十分でも、Chromium 系はゼロデイの公開即日に
当てたい場面もある。

### uv tool 側の更新

```bash
uv tool list
uv tool upgrade --all
```

第 16 章で uv tool / pipx に入れた CLI(ruff、httpie、pre-commit 等)も
別系統で更新する必要がある。

### miniforge / conda 側の更新

```bash
# 既存の DS 環境を最新に
conda update --all -n ds
conda update --all -n dl    # GPU 環境

# conda 自体の更新
conda update -n base -c conda-forge conda

# キャッシュ整理(ディスク削減)
conda clean --all -y
```

DS / ML プロジェクトを複数持っているなら、**プロジェクトごとに更新時期を
ずらす** のが安全。深層学習の環境は数値再現性に敏感なので、論文・実験を
回している期間は固定し、**節目だけ `conda update`** する。

### 全系統まとめて回すスクリプト例

```bash
#!/bin/bash
# ~/.local/bin/weekly-update
set -e
echo "=== apt ==="
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt clean

echo "=== flatpak ==="
flatpak update -y
flatpak uninstall --unused -y

echo "=== uv tool ==="
uv tool upgrade --all 2>/dev/null || true

echo "=== conda (miniforge) ==="
# conda が入っていれば実行(無ければスキップ)
if command -v conda >/dev/null 2>&1; then
    conda update -n base -c conda-forge conda -y
    # 個別の env はここで列挙(週次は base のみ、env は月次でも可)
    # conda update --all -n ds -y
    conda clean --all -y
fi

echo "=== ディスク状態 ==="
df -h /
du -sh ~/.cache ~/.local/share/flatpak ~/.local/share/uv ~/miniforge3 2>/dev/null
```

cron(`0 8 * * 1`)で月曜 08:00 に走らせれば、apt + Flatpak + uv tool +
conda(base) の **四系統を一回でメンテできる**。個別の conda env は
プロジェクト単位で月次更新するのが推奨。

### Claudeに聞いてみよう①:週次メンテの自動化

> 私の Debian での週次メンテナンスを、次の項目で一つのシェルスクリプトに
> まとめてください:
> (1) apt update / upgrade / autoremove
> (2) flatpak update + flatpak uninstall --unused
> (3) uv tool upgrade --all
> (4) conda(miniforge)の base と clean(env は月次でも可)
> (5) ディスク空き容量のチェック(80%超で警告)
> (6) 失敗したサービスの確認
> (7) 古いカーネルの削除候補の表示
> (8) ログのエラー検出
>
> cron で週一(月曜 08:00)に走らせたい。結果をメールか通知で見る想定で。

## 第二節 ポイントリリース

数ヶ月に一度、Debian 12.5 → 12.6 のようなポイントリリースが出る。

```bash
# sources.list の版表記は変えず（"bookworm" のまま）
sudo apt update
sudo apt full-upgrade
sudo reboot
```

`apt upgrade` ではなく `apt full-upgrade` を使う。依存が変わっているパッケージも更新される。

### リリースノートを読む

Debianの公式サイトで、ポイントリリースごとに「何が変わったか」が公開される。**重大な変更はここで告知される**。5分でいいので目を通す。

## 第三節 メジャーアップグレード（Debian 12 → 13）

2年に一度、新しいバージョンがリリースされる。**これは別の仕事**として扱う。

### 事前準備

1. **重要データを完全バックアップ**（`rsync` で外付けSSDへ）
2. **システム全体のスナップショット**（Timeshift）
3. **半日以上の時間を確保**
4. **戻せる道を確認**（スナップショット復元、最悪クリーンインストール）

### 手順の骨格

```bash
# 1. 現状を完全に最新化
sudo apt update
sudo apt full-upgrade
sudo apt autoremove

# 2. sources.list を新バージョンに書き換え
# bookworm → trixie（例）
sudo sed -i 's/bookworm/trixie/g' /etc/apt/sources.list

# 3. アップグレード
sudo apt update
sudo apt upgrade --without-new-pkgs
sudo apt full-upgrade

# 4. 再起動
sudo reboot
```

**この手順は Claude に最新版を確認させる**。Debianの公式アップグレード手順書が最新の推奨。

### Claudeに聞いてみよう②：メジャーアップグレードの計画

> 私は Debian 12 を使っています。Debian 13 リリース後、半年くらい経ってからアップグレードしたいです。
>
> (1) 事前にバックアップすべきファイル・設定
> (2) アップグレード当日の手順（公式手順書を参照）
> (3) よくある失敗と対処
> (4) アップグレード後に確認すべき動作（Wi-Fi、日本語入力、各種アプリ）
> (5) 戻すしか手がない場合の復旧手順
>
> チェックリスト形式で。

## 第四節 ディスク整理

### 何が容量を食っているか

```bash
# ホーム配下
du -sh ~/*

# システム全体のどこが大きいか
sudo du -sh /* 2>/dev/null | sort -h

# ログ
sudo du -sh /var/log/*

# パッケージキャッシュ
du -sh /var/cache/apt/archives/
```

### 掃除の定石

```bash
# apt キャッシュ
sudo apt clean
sudo apt autoremove

# 古いカーネル（手動で確認しながら）
sudo apt list --installed | grep linux-image
# 不要なものを sudo apt remove

# journald のログ（古いもの）
sudo journalctl --vacuum-time=30d     # 30日より古いログを削除

# 各言語のキャッシュ
# Python: ~/.cache/pip
# Node: ~/.npm
# Docker: docker system prune -af
```

### Claudeに聞いてみよう③：ディスクの棚卸し

> 私のDebian のディスクが埋まってきました。現状：
> ```
> 〔df -h の出力〕
> 〔du -sh ~/* の出力〕
> ```
>
> 安全に消せるもの、消してはいけないもの、圧縮できるものを分類してください。
> 各分類の中で優先順（効果の大きいもの順）を付けてください。

## 第五節 ログの見方

Debianのログは主に `/var/log/` と `journalctl` にある。

### journalctl の基本

```bash
# 直近のエラー
journalctl -b -p err

# 特定サービス
journalctl -u nginx -f        # -f はライブ追従

# 期間指定
journalctl --since "yesterday"
journalctl --since "2026-04-20" --until "2026-04-22"
```

### 要観察ファイル

- `/var/log/syslog`：全般
- `/var/log/auth.log`：認証・sudo
- `/var/log/dpkg.log`：パッケージ操作
- `/var/log/apt/history.log`：apt の履歴

### Claudeに聞いてみよう④：ログから異変を検出

> 次のログから、注意すべき事象を抽出してください：
> ```
> 〔journalctl -b -p warning の出力〕
> ```
> 各警告について、（A）無視してよい、（B）後で確認、（C）即対応、のどれか判定してください。

## 第六節 年次メンテナンス

年に一度（あなたの誕生日など、覚えやすい日）、次を行う。

1. **dotfiles の棚卸し**：使っていない設定、古いスクリプトを削除
2. **パッケージの棚卸し**：`apt list --manual-installed` を見て、使っていないものをremove
3. **バックアップの動作確認**：実際にリストアできるか、別のPCで試す
4. **パスワードの見直し**：ssh、GitHub、主要サービスのパスワード変更
5. **ハードウェアのクリーニング**：物理的に、ファンのホコリを取る

### Claudeに聞いてみよう⑤：年次棚卸しのテンプレート

> Debianユーザーの年次メンテナンスのチェックリストを作ってください。
> 次のカテゴリで、各項目に所要時間と優先度を付けて：
> (1) 設定とdotfiles
> (2) パッケージとアプリ
> (3) データバックアップ
> (4) セキュリティ
> (5) ハードウェア
> (6) ドキュメント（自分の環境の記録更新）

## 第七節 「動かなくなる」を予防する

### 変更を一気にしない

新しいパッケージを入れる、設定を変える、ドライバを更新する——これらを一度にやると、何が原因か分からなくなる。

**一度に一つ**。変更したら、再起動して一日使う。問題なければ次の変更。

### バックアップを取ってから変更する

大きな変更（カーネル更新、GPUドライバ変更、DE乗り換え）の前には、Timeshiftでスナップショット。

### 実験は別ユーザーか仮想マシンで

本番環境で新しい設定を試すと、日常が止まる。Debian 12 を仮想マシン（virt-manager）に入れて、そこで実験するのがよい。

## 第八節 メンテナンスを習慣にする

### カレンダーに入れる

- 毎週月曜 08:00：マイナー更新
- 毎月1日 09:00：ディスク整理、ログ確認
- 毎年誕生日：年次棚卸し

GNOME Calendar、Thunderbird Lightning、KOrganizer——どれを使ってもいい。**カレンダーに書くと、やる確率が上がる**。

### 記録を残す

メンテナンスの履歴を `~/maintenance-log.md` に。

```markdown
# 2026-04-28 週次メンテ
- apt update/upgrade: 17パッケージ更新（主にfirefox, kernel）
- autoremove: 3パッケージ削除
- 再起動要：はい（カーネル更新）
- 気になる点：なし
```

これが**年次棚卸しの材料**になる。

## まとめ

この章でやったこと：

1. アップデートの三層（マイナー／ポイント／メジャー）を理解した
2. 週次メンテの自動化を設計した
3. メジャーアップグレードの計画を立てた
4. ディスク整理の定石を押さえた
5. ログの見方を覚えた
6. 年次メンテナンスのテンプレートを作った

手元に残ったもの：
- 週次メンテスクリプト（cron設定済み）
- メンテナンス記録 `maintenance-log.md`
- カレンダーに入った予定

次の第18章では、**実際に問題が起きたときの対処**を扱う。起動できない、画面が出ない、アプリが動かない——それぞれに Claude と対応する作法を身につける。

---

シリーズ全体は[Claudeと一緒に学ぶDebian 一覧](/claude-debian/)から辿れる。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
