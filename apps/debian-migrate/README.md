# Debian 移行ウィザード (debian-migrate)

Windows / macOS / Linux で動くデスクトップアプリ。Debian への移行を「**始める前**」に手元の PC で走らせて、移行の準備を整える。

aiseed.dev 連載「[Claudeと一緒に学ぶDebian](https://aiseed.dev/claude-debian/)」の **第 4 章 (依存関係の棚卸し) / 第 6 章 (ハードウェアの選択) / 第 7 章 (インストール実行)** を GUI に落としたもの。初心者向け ── 専門用語を出さない／一画面一判断／既定値で動く。

## できること

1. **アプリ棚卸し** ── 今インストールされているアプリを検出し、Debian で動く代替を提案
2. **ハードウェアチェック** ── CPU / メモリ / ストレージ / GPU を検出し、Debian 動作の可否を表示
3. **USB インストーラ作成ウィザード** ── Debian の ISO を入手して USB に書き込むまでを順を追って案内
4. **Claude 用プロンプト生成** ── 詰まったら「Claude にこの状態を渡すプロンプト」をワンクリックでコピー

API キーは不要。すべてオフラインで動作する。Claude との会話はユーザーがブラウザで claude.ai に貼り付けて使う。

## 開発

```bash
cd apps/debian-migrate

# 依存関係を入れる (uv 推奨)
uv sync

# 起動 (開発モード)
uv run flet run src/debian_migrate

# テスト
uv run pytest
```

## ビルド (3 OS のバイナリを作る)

```bash
# Windows .exe
uv run flet build windows

# macOS .app
uv run flet build macos

# Linux パッケージ
uv run flet build linux
```

それぞれのバイナリは `build/<platform>/` に出力される。Flet 1.0 Beta (0.85+) を使用。

## ディレクトリ構成

```
apps/debian-migrate/
├── pyproject.toml
├── README.md
├── src/debian_migrate/
│   ├── main.py              # ft.run エントリ
│   ├── app.py               # トップレベル App + Router
│   ├── state.py             # 画面間で共有する状態
│   ├── pages/               # 各画面 (welcome / inventory / replacements / hardware / usb / export)
│   ├── scanners/            # OS 別のアプリ検出
│   ├── hardware/            # ハードウェア検出
│   ├── usb/                 # USB デバイス列挙
│   ├── prompts/             # Claude 用プロンプトテンプレート
│   └── data/                # 代替アプリの静的テーブル
├── tests/
└── assets/
```

## 設計指針

- **Flet 1.0 Beta (0.80.0 / 0.85.0+) の declarative API** を使う (`@ft.component`, `ft.Router`, hooks)。詳細は `.agents/skills/building-flet-apps/SKILL.md`。
- **GUI は wizard 形式** ── ユーザーは「次へ」だけで進める。各画面に「Claude 用プロンプトをコピー」ボタンを置く。
- **読み取り中心** ── インストール済みアプリの検出、ハードウェア情報の取得などは行うが、**システムを書き換えない**。USB 書き込みも v1 では「ガイド表示」までで、実際の書き込みはユーザーが Balena Etcher 等で手動。安全側に倒す。
- **API キー不要** ── AI 連携はプロンプトコピーボタンのみ。誰でもすぐ使える。

## 関連

- 本書: [Claudeと一緒に学ぶDebian](https://aiseed.dev/claude-debian/) (全 24 章)
- 関連シリーズ: [AIネイティブな仕事の作法 — AI 時代の自由人のための道具たち](https://aiseed.dev/ai-native-ways/)
- Flet 開発 SKILL: `.agents/skills/building-flet-apps/SKILL.md`
