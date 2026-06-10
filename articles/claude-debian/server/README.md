# サーバー編 — Claudeと一緒に学ぶDebian

**副題: GUIのない世界で、Claudeと一緒に自分のインフラを持つ**

親シリーズ「Claudeと一緒に学ぶDebian」(`../`)のサブシリーズ。親シリーズは
主としてデスクトップ用(自分の机を取り戻す話)、本サブシリーズはサーバー用
(自分のインフラを持つ話)。画面のないDebianをSSHで操り、守りを固め、
データベースと自作アプリを動かし、公開し、データを守るまでを11章で歩く。
コンテナは使わない——アプリは「ディレクトリ + venv + systemd」で動かし、
専用ユーザーと権限設計、systemdのサンドボックスで隔離する方針。
データは他社のクラウドではなく、自分の機械の上のデータベース
（SQLite / PostgreSQL）に置く。

サーバー管理はログも設定もエラーもすべてテキストであり、「Claudeと一緒に
学ぶ」方式が最も深く効く領域——これが本サブシリーズの立脚点。各章末の
「Claudeに聞いてみよう」枠を自分の状況で埋めながら進む構成は親シリーズと
共通。EN 版 README は [`README.en.md`](README.en.md)。

## 状態

**全 11 章公開済み**(JA + EN、各 22 ファイル)。

## ファイル構成

```
articles/claude-debian/server/
├── README.md           ── このファイル (JA)
├── README.en.md        ── EN 版
└── NN-slug/            ── サブシリーズ内で 01 から再採番
    ├── ja.md
    └── en.md
```

ビルドは親シリーズと同じ book パイプライン(`tools/build_article.py` の
`BOOK_SUBSERIES` registry)。テンプレート・フロントマター schema も親シリーズ
と共通。EN 版は `lang: en` を明示する。slug は `claude-debian-server-NN-…`
の形で、URL の stem はこの prefix を取り除いたもの。

## URL

| ソース | 出力 | URL |
|---|---|---|
| `01-what-is-a-server/ja.md` | `html/claude-debian/server/01-what-is-a-server/index.html` | `/claude-debian/server/01-what-is-a-server/` |
| `01-what-is-a-server/en.md` | `html/en/claude-debian/server/01-what-is-a-server/index.html` | `/en/claude-debian/server/01-what-is-a-server/` |
| (サブシリーズ目次・自動生成) | `html/claude-debian/server/index.html` | `/claude-debian/server/` |
| (サブシリーズ目次・自動生成) | `html/en/claude-debian/server/index.html` | `/en/claude-debian/server/` |

## 章ラベル

frontmatter の `label` は次の形を使う。

- JA: `Claude × Debian サーバー編 NN`
- EN: `Claude × Debian Server NN`

パンくず・サイドバー目次では、シリーズ名は
`Claudeと一緒に学ぶDebian — サーバー編` / `Learning Debian with Claude — Server Edition`
と連結表示される。

## prev / next チェーン

サブシリーズ**内**で閉じる。01 章は `prev_slug:` 空、最終章(11 章)は
`next_slug:` 空のままにする。親シリーズにブリッジしない(最終章の CTA
ボタンで親シリーズへ誘導するのは可)。

## 親シリーズ目次との関係

- 親シリーズ目次 (`/claude-debian/`) は先頭にヒーローカードでこの
  サブシリーズへ誘導する(自動生成)。
- 親シリーズの章リスト本体にこのサブシリーズの章は **含まれない**。
- サブシリーズ目次 (`/claude-debian/server/`) は親シリーズ目次への
  「← 目次へ戻る」リンクを冒頭に持つ(自動生成)。

## 章一覧

| # | slug (stem) | 日本語タイトル |
|---|---|---|
| 01 | `01-what-is-a-server` | 第1章 サーバーとは何か |
| 02 | `02-where-to-run` | 第2章 サーバーをどこに置くか |
| 03 | `03-minimal-install` | 第3章 最小インストール |
| 04 | `04-ssh` | 第4章 SSHという玄関 |
| 05 | `05-security-basics` | 第5章 守りの基本 |
| 06 | `06-systemd-services` | 第6章 サービスという単位 |
| 07 | `07-database` | 第7章 データベースという土台 |
| 08 | `08-fastapi` | 第8章 自作アプリを動かす |
| 09 | `09-publishing` | 第9章 外の世界に公開する |
| 10 | `10-backup` | 第10章 データを守る |
| 11 | `11-operations` | 第11章 サーバーを育てる |

slug は確定済み。URL の安定性のため、以後変更しない。

## ビルド

```bash
python3 tools/build_article.py --all                                        # 全部
python3 tools/build_article.py articles/claude-debian/server/01-what-is-a-server/ja.md  # 1章だけ
```
