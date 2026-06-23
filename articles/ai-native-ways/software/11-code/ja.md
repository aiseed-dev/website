---
slug: code
number: "03"
part: "2"
title: コードを手元に ── Forgejo と Zed
subtitle: ビルダーの仕事場を、自分の側に ── リポジトリも CI も、Microsoft の外へ
description: ビルダーの仕事は、AI にコードを書かせ、評価し、統合すること。その置き場 ── リポジトリ ── を自分の側に立てる。Forgejo は GitHub・Azure DevOps を置き換える単一の Git フォージで、Actions で CI/CD まで賄う。第1章の PostgreSQL に乗せ、第2章の門番の内側に。手元の道具は Zed と Claude。コードは資産であり、置き場の主導権は自分が持つ。
date: 2026.07.06
label: Independence 3
title_html: コードの置き場を、<br><span class="accent">自分の側</span>に。
prev_slug: auth
prev_title: "門番を立てる ── PocketBase で認証を一つに"
next_slug: documents
next_title: "文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む"
---

# コードを手元に ── Forgejo と Zed

ビルダーの仕事は、コードを書くことではない。**AI に書かせ、評価し、
統合すること**だ(導入編 第4章)。だが、生まれたコードには置き場が要る ──
それがリポジトリだ。AI が大量に生むコードほど、**その置き場の主導権**が
効いてくる。

GitHub も Azure DevOps も、他社のサーバの上にある。ここでは、その仕事場を
**自分の側**に立てる。

## なぜコードを自分の側に置くのか

コードは資産だ。事業の中身そのものが、そこに書かれている。それを他社の
プラットフォームに預けたままにする理由は、もう薄い。

- **依存を断つ** ── 料金体系・規約・可用性が、他社の都合で変わらない
- **AI と密につなぐ** ── 生成・レビュー・CI を、自分のルールで回す
- **門番と一つに** ── 第2章の認証の内側に、コードも入れる

汎用の Git ホスティングは、すでに OSS にある。**書くのではなく、立てる**。

## Forgejo を立てる

仕事場は **Forgejo**。Gitea 系の単一バイナリで、リポジトリ・Issue・
プルリクエスト・レビュー・CI を一つに備える。GitHub・GitLab・Azure
DevOps の置き換えだ。データは **第1章の PostgreSQL** に乗せる。

```yaml
# compose.yaml ── Forgejo を第1章の DB に乗せて立てる
services:
  code:
    image: codeberg.org/forgejo/forgejo:latest
    environment:
      FORGEJO__database__DB_TYPE: postgres
      FORGEJO__database__HOST: db:5432      # 第1章の PostgreSQL
      FORGEJO__database__NAME: forgejo
      FORGEJO__database__USER: postgres
      FORGEJO__database__PASSWD: change-me
    volumes: ["./forgejo:/data"]
    ports: ["3000:3000", "2222:22"]
    restart: always
```

```bash
docker compose up -d
git remote add origin ssh://git@localhost:2222/team/app.git
git push -u origin main          # もう自分のサーバに乗っている
```

## CI/CD ── Forgejo Actions

テスト・ビルド・デプロイの自動化は **Forgejo Actions**。GitHub Actions と
**同じ書式**のワークフローがそのまま動く。リポジトリに一枚置くだけだ。

```yaml
# .forgejo/workflows/ci.yml
on: [push]
jobs:
  test:
    runs-on: docker
    steps:
      - uses: actions/checkout@v4
      - run: pytest          # 自分のランナーで、追加料金ゼロ
```

GitHub Actions の従量課金から降りる。**ランナーも自分の側**にあるので、
回す回数を気にせず、AI が書いたコードを何度でも検証できる。

## 手元の道具 ── Zed と Claude

サーバが Forgejo なら、手元の編集は **Zed**。Rust 製で軽く、複数人の
同時編集と **AI 連携**を備えたエディタだ。Claude をその場に呼び、生成・
修正・説明をさせながら、ビルダーは **評価と統合**に集中する。

```bash
git clone ssh://git@localhost:2222/team/app.git
zed app/          # Claude を呼んで、書かせ、評価し、push する
```

書くのは AI、決めるのは人。仕事場(Forgejo)と道具(Zed)が揃えば、
その分担がそのまま回る。

## 門番の内側に置き、移行する

Forgejo はリバースプロキシの内側に置く(第2章)。GitHub からの移行は、
Forgejo の **「新規移行」** が Issue・PR ごとリポジトリを取り込む。

```caddy
git.example.com { reverse_proxy code:3000 }
```

一度に切り替えなくてよい。**GitHub をミラーにしたまま並行で動かし**、
慣れたら本番を Forgejo に寄せる(親シリーズ第7章)。

> コードは、事業の中身そのものだ。
> その置き場の主導権は、**他社ではなく自分が持つ**。

## まとめ

ビルダーの仕事場を、自分の側に。

- **Forgejo** ── リポジトリ・Issue・PR・レビューを一つに(第1章の PostgreSQL に乗る)
- **Forgejo Actions** ── GitHub Actions 互換の CI/CD、ランナーも自分の側
- **Zed + Claude** ── 軽量エディタに AI を呼び、書かせ・評価し・push する
- **門番の内側** ── リバースプロキシで囲い、GitHub から段階移行

書いたコードは、設定だけ。**汎用は、すでに OSS として在る**。次章では、
**メール(Stalwart)** を自分の側に立て、Exchange と Outlook の依存を断つ。

---

## 関連記事

- [導入編 第4章: ビルダーという役割](/ai-native-ways/software/builder/)
- [第2章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [親シリーズ第9章: アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ](/ai-native-ways/apps/)
