---
slug: web
number: "12"
title: Webサイトを作る
subtitle: 会社サイトもブログも静的に作り、サーバを持たず Cloudflare Pages へ ── ビルド・確認・デプロイを分けて
description: 社外に見せる Web は、ほとんど静的でよい。自前のビルドや Hugo で Markdown から HTML を作り、Cloudflare Pages に置く ── サーバは持たない。CDN と自動 HTTPS は Cloudflare に任せ、ソースとビルドは自分の手元に残す。肝は「ビルド → 確認 → デプロイ」を分けること。自動の作り直しや一括デプロイを避け、確認した HTML と本番に上げる HTML を同じにする。内部の道具は第7章の門番の内側に残す。
date: 2026.07.14
label: Software 12
title_html: Web サイトは<span class="accent">静的</span>に作り、<br><span class="accent">サーバ無し</span>で公開する。
prev_slug: meetings
prev_title: 会議と予約を自分の側に ── Jitsi と Cal.com
next_slug: ai
next_title: 自前の AI を据える ── LLM と RAG
---

# Webサイトを作る

社内向けの道具は揃った。最後に、社外に見せる Web サイトを作る。会社
サイト、製品ページ、ドキュメント、ブログ ── その大半は、静的でよい。

静的なら、自分のサーバは要らない。作った HTML を **Cloudflare Pages** に
置けば、それで公開できる。

## なぜ静的にするのか

社外サイトの中身は、めったに変わらない。だから毎回サーバで組み立てず、
先に HTML を作って置く。そのほうが、速く、安全で、安い。

- **速い** ── ただのファイル配信。データベースを待たない
- **安全** ── 動く部分がないので、攻撃される面がほぼ無い
- **楽** ── 中身は Markdown。Claude に書かせ、ビルドが HTML にする

このサイト(aiseed.dev)も静的だ。Markdown から HTML を作って置いている。
動的なサーバは無い。

## 記事・ブログを書く

ここでやることは、テンプレート選びではない。**サイトを運用する人が、記事や
ブログを書くこと**だ。

中身は Markdown で書く。決まった置き場(例:`articles/`)に、記事を一つ
ファイルとして足し、ビルドで HTML に変換する。

```bash
# articles/ に Markdown を書き、ビルドで html/ にする
python tools/build.py
```

見た目(テンプレート)を Astro や Hugo、あるいは自前で作るのは、**最初に
一度だけの別作業**だ ── そこは好きにすればいい。日々の運用は、**Markdown を
書いて、ビルドして、上げる**、それだけ。出力は、ただのファイル群(`html/`)。

## Cloudflare Pages に置く

作った HTML は **Cloudflare Pages** に置く。サーバは要らない。ファイルを
アップロードすれば、世界中の CDN から配信され、HTTPS も自動でつく。

配信と防御は Cloudflare に任せ、**ソースとビルドは自分の手元に残す**。
公開する HTML に秘密は無いので、ここは安心して任せられる。

## ビルド・確認・デプロイを分ける

公開は、手順を分けてやる。一つにまとめない。

```bash
# 1. ビルド ── html/ を作る
python tools/build.py
# 2. 確認 ── 作った html/ をそのまま開いて、目で見る
python -m http.server --directory html 8000
# 3. プレビューに上げる ── 本番の前に、実環境で確認
python tools/deploy_pages.py html --branch preview
# 4. 確認できたら、本番に上げる
python tools/deploy_pages.py html --branch main
```

自動で作り直す設定や、「ビルドして上げる」を一つにまとめたコマンドは
使わない。**確認した HTML と、本番に上がる HTML を、同じにする**ためだ
(詳しい運用は社内マニュアルに分ける)。アップロードに npm や Node は
要らない ── Cloudflare の API を直接叩くスクリプト一つでよい。

## ドメインをつなぐ

独自ドメインは、Cloudflare Pages の **カスタムドメイン**に追加する。DNS を
Cloudflare で持っていれば、今までサーバを指していた **A レコードが、自動で
Pages に切り替わる**。証明書も自動でつく。

**メール(MX・SPF)は触らない**。Web の置き場を替えるだけだ。不安なら、
旧サーバを止めず、プレビューで確認してから本番ドメインを向ける。

## 動く部分だけ、つなぐ

問い合わせフォームのような **動く部分だけ**、裏につなぐ。送信先は、第7章の
門番の内側に置いた自分の API(認証は門番、保存は第6章の DB、通知は第10章
のメール)。**大半は静的、動くのは要る所だけ**。

## 内部の道具は別

公開サイトは Cloudflare Pages に置く。だが、第7〜11章で作った **内部の道具**
(認証・文書・コード・会議)は別だ。秘密や生のデータが通るので、第7章の
門番(自分のリバースプロキシ)の内側に置く。

- **公開サイト**(静的・秘密なし)── Cloudflare Pages
- **内部の道具**(認証・業務データ)── 自分の側、門番の内側

借りる所と、自分で持つ所を、分けて決める。

## まとめ

- **記事・ブログを書く** ── 運用は Markdown を書くこと。テンプレートは最初に一度だけ(Astro / Hugo / 自前は好みで)
- **Cloudflare Pages** ── サーバ無しで公開、CDN・自動 HTTPS を任せる
- **ビルド → 確認 → デプロイを分ける** ── 自動の作り直しを避け、確認した物を上げる
- **ドメインは自動で切り替わる** ── カスタムドメインで A レコードが Pages を指す、メールは触らない
- **内部の道具は別** ── 第7章の門番の内側に置く

次章では、これらすべての上に **AI(自前の LLM と RAG)** を乗せ、Copilot の
依存を断つ。

---

## 関連記事

- [第7章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [第10章: メールを自分の側に ── Stalwart と Thunderbird](/ai-native-ways/software/mail/)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
