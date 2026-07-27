# 「AIネイティブな仕事の作法」に登場する Linux アプリ一覧

本文（`articles/ai-native-ways/`）を走査して抽出した、Linux で動く自前アプリ・
ツールの一覧。中心は **自立編（2-02〜2-11）の自前サーバ群**、加えて親シリーズ
個別トラックの CLI／デスクトップツール。章番号は `部-章`（例 `2-05`）。

各サーバは基本 `docker compose` 一枚で立てる構成。**Cloudflare Pages**（2-08）と
最前線モデル API（難所だけ借りる）は自前 Linux アプリではなく外部サービスである。

## 自前サーバ（自立編の中核スタック）

| アプリ | 役割 | 置き換える対象 | 章 |
|---|---|---|---|
| **PocketBase** | 認証・管理画面・REST/realtime・ファイル保管（Go 単一バイナリ、SQLite 上） | Entra ID / Google ID | 2-03 |
| **Caddy** | リバースプロキシ・自動 TLS（社内アプリの前段） | — | 2-03 |
| **OnlyOffice Docs**（Document Server） | docx/xlsx/pptx 編集エンジン・同時編集 | Office / M365 | 2-05 |
| **Forgejo** | Git ホスティング・CI | GitHub / Azure DevOps | 2-04 |
| **Zed** | コードエディタ | — | 2-04 |
| **Stalwart** | メールサーバ（Rust 単一バイナリ） | Exchange / Gmail | 2-06 |
| **Thunderbird** | メールクライアント（デスクトップ） | Outlook | 2-06 |
| **Jitsi**（Meet） | ビデオ会議 | Teams / Google Meet | 2-07 |
| **Cal.com** | 予約 | Bookings / Calendar | 2-07 |
| **BigBlueButton** | オンライン講座 | — | 2-07 |
| **FastAPI + Uvicorn** | 基幹ロジックの API（Python） | Power Apps / Apps Script | 2-09 |
| **Flet** | デスクトップ/モバイル/Web アプリ（Python、kura で使用） | — | kura |

## データ基盤（2-02）

| ツール | 役割 | 置き換える対象 |
|---|---|---|
| **PostgreSQL** | RDB（共有・同時実行時） | Azure SQL / Cloud SQL |
| **SQLite** | 組み込み DB（既定。「普通はこれで十分」） | — |
| **pgvector** | PostgreSQL のベクトル拡張（RAG 用） | — |
| **DuckDB** | 分析用 DB | — |
| **Polars** | データフレーム（重い集計） | Power BI / Excel |

## AI スタック（2-11）

| ツール | 役割 |
|---|---|
| **Ollama / vLLM** | ローカル LLM 実行基盤 |
| **North Mini Code**（Cohere, オープンウェイト Apache 2.0） | 手元で動かす LLM の出発点 |
| **Command A+**（Cohere） | 社内文書 RAG（Ryzen AI Max PRO 400 想定の将来構成） |
| **Open WebUI** | ChatGPT 風の窓口（門番の内側） |
| **pgvector** | RAG のベクトルストア |

## 情報整備・OCR（2-10）

| ツール | 役割 |
|---|---|
| **Tesseract** | 活字 OCR |
| **ocrmypdf** | スキャン PDF にテキスト層を付与 |
| **オープンウェイトのビジョンモデル** | 帳票・図表混じりを Markdown に起こす |

## 親シリーズ個別トラックの CLI／デスクトップツール

| ツール | 役割 |
|---|---|
| **rclone** | OneDrive/SharePoint からの吸い出し（2-05） |
| **pandoc** | ドキュメント形式変換 |
| **WeasyPrint** | HTML → PDF |
| **Whisper** | 録音の文字起こし（議事録自動化） |
| **Firefox** | ブラウザ（apt 直、snap 回避の文脈） |
| **sqlite3 / jq / ImageMagick / webp** | データ・画像・整形の小道具 |
| Python ライブラリ | Pillow・python-docx・openpyxl・pandas・matplotlib・reportlab・markdown-it-py・jinja2・qrcode 等 |

## 参考実装

- **kura**（`aiseed-dev/workspace`）── 上記を組んだ自前 Microsoft 365 /
  Google Workspace 代替（FastAPI + Flet + PocketBase、ファイルネイティブ）。

---

# おまけ（シリーズ外）── 夏休みの Linux ゲーム

本編はゲームを扱っていない。以下は **シリーズとは無関係の付録**で、自前の
Linux 環境を家族で使うときの、評判の良いオープンソース／無料ゲーム。すべて
Linux ネイティブで動く。

## オープンソースゲーム（家族向け）

| ゲーム | ジャンル | 近いもの |
|---|---|---|
| **SuperTuxKart** | カートレース | マリオカート |
| **SuperTux** | 横スクロールアクション | スーパーマリオ |
| **0 A.D.** | リアルタイム戦略（RTS） | Age of Empires |
| **The Battle for Wesnoth** | ターン制ストラテジー | ファイアーエムブレム系 |
| **Luanti**（旧 Minetest） | サンドボックス／クラフト | Minecraft |
| **Mindustry** | タワーディフェンス＋工場 | Factorio 寄り |
| **OpenTTD** | 経営シミュレーション | Transport Tycoon |
| **Warzone 2100** | RTS | — |
| **Hedgewars** | ターン制砲撃 | Worms |
| **Frozen Bubble** | パズル | パズルボブル |
| **Pingus** | パズル | レミングス |
| **Armagetron Advanced** | 対戦 | Tron ライトサイクル |
| **Xonotic / Teeworlds（DDNet）** | 対戦アクション | アリーナ FPS / 2D 対戦 |
| **Endless Sky** | 宇宙探索 RPG | — |
| **Veloren** | ボクセル RPG | — |

## 小さい子向け（教育寄り）

| アプリ | 役割 |
|---|---|
| **GCompris** | 未就学〜小学生向けの学習ゲーム集 |
| **Tux Paint** | お絵かき |
| **Luanti（Minetest）** | クリエイティブ・ものづくり |

## ランチャー・互換層（市販ゲームも遊びたいとき）

| ツール | 役割 |
|---|---|
| **Steam + Proton** | Windows 向け Steam ゲームを Linux で動かす（公式） |
| **Lutris** | GOG/Epic/各種ゲームの統合ランチャー |
| **Heroic Games Launcher** | Epic / GOG / Amazon のゲーム |
| **Bottles** | Wine ベースで Windows アプリ/ゲームを動かす |
| **RetroArch** | レトロゲームのエミュレータ統合フロントエンド |

> どれも `docker` ではなく、ディストリのパッケージ（apt / Flatpak）や Steam から
> 入れるのが普通。Flatpak（Flathub）経由が、ディストリを問わず一番手軽。
