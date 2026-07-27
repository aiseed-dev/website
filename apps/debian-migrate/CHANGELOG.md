# Changelog

## 0.4.0 — 2026-05-22 (第 12 + 17 章追加、wizard 11 ステップに)

### 追加
- **運用と長期メンテ** (`/operations`) ── 本書 第 12 章 (dotfiles
  管理) と 第 17 章 (アップデートとメンテ) を 1 ページに統合。
  - dotfiles 管理対象の一覧 (.bashrc / .profile / .config / .ssh /
    .gitconfig / .config/nvim / VSCode settings)
  - 初期化スクリプト例 (Git init + symlink) をコピー可
  - 秘密鍵をコミットしない注意書き
  - 週次 / 月次のメンテコマンド 5 件 (apt upgrade / autoremove /
    flatpak update / 容量確認 / timeshift スナップショット)
- `operations_prompt()` テンプレート (dotfiles 構成 + アップグレード
  手順を Claude に相談)
- Markdown レポートに第 12 + 17 章のサマリーを出力

### 変更
- step 数 10 → 11。Install Plan → Operations → Export の順に。

## 0.3.0 — 2026-05-22 (第 9・10・11 章追加、ポストインストール計画完成)

### 追加
- **第 9 章 デスクトップ環境** (`/desktop`) ── GNOME / KDE Plasma /
  XFCE / Cinnamon / LXQt の 5 つを比較カードで提示。メモリから推奨
  DE を自動算出 (RAM 2GB→LXQt / 4GB→XFCE / 16GB→GNOME 等)。
  各 DE の「いいところ」「注意点」を 2 列で並べ、後から入れる
  `apt install task-*-desktop` コマンドを生成。
- **第 10 章 日本語入力** (`/ime`) ── Fcitx5 + Mozc 導入の 4
  ステップコマンドをコピーボタン付きで提示。よくある困りごと
  (半角/全角・変換キー設定・Wayland / Electron での挙動) と、
  `fcitx5-diagnose` などの診断コマンド。
- **第 11 章 アプリ導入計画** (`/install-plan`) ── ステップ 3 で
  「OK」を押した代替候補から、Debian での導入方法を自動引き当て。
  apt / Flatpak / 手動の 3 種類に分類し、**一括スクリプト**として
  まとめてコピーできる。`data/install_commands.py` に 100+ 件の
  アプリ → Debian 導入方法マップ。
- 各章対応の Claude プロンプトテンプレート (`desktop_env_prompt`
  / `ime_prompt` / `install_plan_prompt`)。
- Markdown レポートに第 9・10・11 章の選択結果と一括スクリプトを
  出力。

### 変更
- step 数 7 → 10 (Troubleshooting → Desktop → IME → Install Plan
  → Export の順)。
- step indicator が長くなったので wrap 表示で折り返し可能。
- Troubleshooting の「次へ」を /desktop に。Export の「戻る」を
  /install-plan に。

## 0.2.0 — 2026-05-22 (第 8 章「事前トラブル予防」追加)

### 追加
- 新ステップ `/troubleshooting` を USB と Export のあいだに追加。
  本書 第 8 章「最初のトラブルシューティング」の七つのカテゴリ
  (ディスプレイ / Wi-Fi / Bluetooth / サウンド / サスペンド /
  日本語入力 / 周辺機器) を提示し、検出したハードウェアから
  当たりそうなカテゴリに ⚠ マーク。
- Debian 起動後にコピペで使う共通診断コマンドを 5 件 (journalctl /
  lspci / lsusb / dmesg / systemctl --failed)、コピーボタン付き。
- `troubleshooting_prompt()` — 第 8 章の統一テンプレートを
  ハードウェア情報込みで生成。
- Markdown レポートにも第 8 章ガイダンス (7 カテゴリと診断コマンド)
  を出力。

### 変更
- step 数 6 → 7、USB → Troubleshoot → Export の順に変更。
- `welcome` / step indicator も 7 ステップに対応。

## 0.1.0 — 2026-05-22 (v1, 初版)

### 追加
- Wizard 形式の事前移行ツール (Welcome → Inventory → Replacements → Hardware → USB → Export)。
- アプリ棚卸し: Windows (registry) / macOS (.app + Info.plist) / Linux (.desktop) の検出。
- 代替候補テーブル: 79 件 (Office / Adobe / dev tools / 日本のソフト / iWork など)。
- ハードウェア検出: psutil + OS 別コマンド。Apple Silicon / NVIDIA / 低メモリ / 容量不足を警告。
- USB ガイド: デバイス列挙のみ。書き込みは `dd` コマンドまたは Balena Etcher への誘導。
- Claude 用プロンプトのワンクリックコピー機能 (5 種類のテンプレート)。
- Markdown レポートのエクスポート (`~/debian-migrate-report-YYYYMMDD-HHMMSS.md`)。
- 朱色 (#c8442a) のアクセントで aiseed.dev と統一感のあるテーマ。

### 技術
- Flet 1.0 Beta (0.85.x) の declarative API (`@ft.component`, `ft.Router`, `use_state`, `use_route_outlet`)。
- API キー不要・完全オフライン動作。
- システムを書き換えない (検出と提案のみ)。
