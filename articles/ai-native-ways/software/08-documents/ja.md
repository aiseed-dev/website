---
slug: documents
number: "08"
title: 文書を取り戻す ── Nextcloud と OnlyOffice
subtitle: Word・Excel・PowerPoint を、自分の側で開く ── 形式はそのまま、置き場も自分の手に
description: Word・Excel・PowerPoint は、人が書き人が読む入出力の道具だ。OnlyOffice は docx・xlsx・pptx をそのまま読み書きし、同時編集もできる。置き場は Nextcloud で、OneDrive・SharePoint を自分の側に。第6章の PostgreSQL に乗せ、第7章の門番の内側に置く。形式は変えず、データの主導権だけ取り戻す。
date: 2026.07.04
label: Software 08
title_html: 文書を、<span class="accent">自分の側</span>で<br>開いて、しまう。
prev_slug: auth
prev_title: 門番を立てる ── PocketBase で認証を一つに
next_slug: code
next_title: コードを手元に ── Forgejo と Zed
---

# 文書を取り戻す ── Nextcloud と OnlyOffice

門番(第7章)の内側に、最初に置く道具は **文書**だ。Word・Excel・
PowerPoint ── これらは、人が書き、人が読む **入出力の道具**であって、
その役割は変わらない(第6章)。変えるのは、**形式の互換と、置き場の
主導権**だけだ。

だから新しい文書形式に乗り換えるのではない。**`docx`・`xlsx`・`pptx` を
そのまま**読み書きできる OSS を、自分の側に立てる。

## なぜ OnlyOffice か

文書編集は **OnlyOffice**。理由は一つ、**Microsoft Office 形式との互換が
高い**ことだ。`docx`・`xlsx`・`pptx` をレイアウト崩れなく開き、同じ形式で
保存し、複数人で **同時編集**できる。人の入出力の道具は、人の慣れた形式の
ままでなければ意味がない ── だから互換が最優先だ。

置き場・共有は **Nextcloud**。OneDrive と SharePoint の代わりに、ファイル
保管・共有・バージョン管理・社外リンクを担う。OnlyOffice はこの Nextcloud
の中で開く。

## Nextcloud を立てる

`compose.yaml` で立てる。データは **第6章の PostgreSQL** にそのまま乗せる。

```yaml
# compose.yaml ── 置き場(Nextcloud)を立て、第6章の DB に乗せる
services:
  files:
    image: nextcloud:apache
    environment:
      POSTGRES_HOST: db          # 第6章で立てた PostgreSQL
      POSTGRES_DB: nextcloud
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: change-me
    volumes: ["./nc_data:/var/www/html"]
    restart: always
```

```bash
docker compose up -d
# 管理者を作り、初期設定を済ませる(ブラウザで開くだけ)
```

倉庫(PostgreSQL)はもう在る。Nextcloud は **その上にファイルの層を足す**
だけだ。新しい DB サーバは要らない。

## OnlyOffice をつなぐ

文書を Nextcloud の中で編集できるよう、**OnlyOffice Document Server** を
横に立て、コネクタで結ぶ。

```yaml
  # 同じ compose.yaml に追記
  onlyoffice:
    image: onlyoffice/documentserver:latest
    restart: always
```

あとは Nextcloud の管理画面で **OnlyOffice コネクタ**アプリを入れ、
Document Server の場所を指すだけ。これで一覧から `.xlsx` を開けば、
ブラウザ内で表計算が立ち上がり、**そのまま Excel 形式で保存**される。

## 門番の内側に置く

Nextcloud は自前のアカウントを持つ。第7章の方針どおり、**リバース
プロキシの内側**に置き、社外には門を通った者だけを通す。

```caddy
docs.example.com { reverse_proxy files:80 }
```

将来、一度のログインで束ねるなら、Nextcloud の OIDC アプリを足して
門番と結ぶ ── だが、まずは置き場を自分の側に移すことが先だ。

## 既存の文書を移す

OneDrive・SharePoint に積まれた文書は、**形式を変えずに**運べる。
`docx`・`xlsx`・`pptx` は OnlyOffice がそのまま開くので、変換は要らない。

```bash
# rclone で OneDrive / SharePoint から Nextcloud へ一括コピー
rclone copy onedrive:Documents nextcloud:Documents --progress
```

移行は段階的でよい。**並行で動かし、移り終えてから旧ストレージを
解約する**(親シリーズ第7章)。リンクの貼り直しも、急がなくてよい。

## 人は OnlyOffice、機械は Polars

ここで第6章とつながる。**人は OnlyOffice(Excel 形式)で入れて読み、
機械は Polars と DuckDB で裏のデータを捌く**。同じ `.xlsx` を、人は編集の
道具として、機械は入力として扱う ── 役割で分ける。

- 人が作る集計表・申請書・提案書 ── OnlyOffice で開いて、しまう
- 数百万行の突き合わせ・全社集計 ── Polars が `.xlsx` を読み、PostgreSQL に書く

表計算は「人の道具」に戻り、重い処理は「機械の道具」へ移る。**どちらも
同じ形式・同じ置き場**を共有する。

> 文書形式は変えない。変えるのは、**それが置かれる場所**だ。
> 人の道具はそのまま、主導権だけ自分の側へ。

## まとめ

門番の内側に、文書の置き場を。

- **OnlyOffice** ── `docx`・`xlsx`・`pptx` を高互換で開き、同時編集
- **Nextcloud** ── OneDrive・SharePoint の代わりの保管・共有(第6章の PostgreSQL に乗る)
- **門番の内側** ── リバースプロキシで囲い、将来 OIDC で束ねる
- **rclone** ── 既存文書を形式そのままで移行、並行稼働で切り替え
- **人と機械の分担** ── 人は OnlyOffice、機械は Polars / DuckDB

書いたコードは、ほとんど無い。**汎用は、すでに OSS として在る**。
次章では、ビルダーの仕事場 ── **コードの共有(Forgejo)** を立て、
GitHub と Azure DevOps を自分の側に置く。

---

## 関連記事

- [第6章: 土台を据える ── PostgreSQL・SQLite・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [第7章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
