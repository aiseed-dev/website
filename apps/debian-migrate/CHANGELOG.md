# Changelog

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
