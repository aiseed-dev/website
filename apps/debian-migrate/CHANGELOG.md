# Changelog

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
