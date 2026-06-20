---
slug: web
number: "12"
title: 社外に見せる窓 ── 静的サイトと Caddy
subtitle: 会社サイトもドキュメントも静的に、入口は一つの Caddy に集める
description: 社外に見せる Web は、ほとんど静的でよい。Astro や Hugo で Markdown から組み、Caddy が自動 HTTPS で配る。Caddy は同時に、これまで立てた全アプリの入口(リバースプロキシ)を一枚に束ねる。動的が要るのはフォームなど一部だけで、そこは第6章の DB と第7章の門番につなぐ。前段に Cloudflare を置けば、配信と防御も借りられる。
date: 2026.07.14
label: Software 12
title_html: 社外の窓は<span class="accent">静的</span>に、<br>入口は<span class="accent">一つ</span>に。
prev_slug: meetings
prev_title: 会議と予約を自分の側に ── Jitsi と Cal.com
next_slug: ai
next_title: 自前の AI を据える ── LLM と RAG
---

# 社外に見せる窓 ── 静的サイトと Caddy

ここまでは社内向けの道具だった。最後に、社外に見せる **窓** ── Web を
立てる。会社サイト、製品ページ、ドキュメント、ブログ ── その大半は、
**静的**でよい。

そして、これまで各章で何度も出てきた **Caddy** に、ここで正面から向き合う。
全アプリの入口を、一枚に束ねる門だ。

## なぜ静的か

社外サイトの中身は、めったに変わらない。だから毎回サーバで組み立てる必要は
なく、**あらかじめ HTML に焼いて置く**ほうが、速く・安全・安い。

- **速い** ── ただのファイル配信。データベースを待たない
- **安全** ── 動く部分がないから、攻撃面がほぼ無い
- **AI と相性がいい** ── Markdown を書けば、Claude が HTML に組む

> このサイト(aiseed.dev)自身が、その実例だ。Markdown を静的 HTML に
> 焼いて配っている ── 動的サーバは、無い。

## 静的サイトを立てる

文章は Markdown で書き、**Astro** や **Hugo** で HTML に組む。出力は
ただのファイル群だ。

```bash
npm create astro@latest site && cd site
npm run build        # dist/ に HTML が焼ける
```

`dist/` を Caddy に渡せば、それで公開できる。中身の更新は「書いて、
組んで、置く」だけ ── ここでも、書くのはコードではなく文章だ。

## Caddy ── 自動 HTTPS と、全アプリの入口

**Caddy** は、静的サイトを配るだけでなく、**これまで立てた全アプリの入口**
を一枚に束ねる。証明書は **Let's Encrypt で自動取得・自動更新**、設定は
数行だ。

```caddy
# Caddyfile ── 一枚で、窓も、全アプリの入口も
example.com           { root * /srv/site/dist
                        file_server }            # 静的サイト
auth.example.com      { reverse_proxy auth:8090 }       # 第7章 門番
docs.example.com      { reverse_proxy onlyoffice:80 }   # 第8章 文書(編集エンジン)
git.example.com       { reverse_proxy code:3000 }       # 第9章 コード
meet.example.com      { reverse_proxy jitsi-web:80 }    # 第11章 会議
book.example.com      { reverse_proxy booking:3000 }    # 第11章 予約
```

これまで各章で書いてきた一行ずつが、**この一枚に集まる**。HTTPS は
全ドメインで自動。入口が一つなら、守る場所も一つだ。

## 動的が要る所だけ、つなぐ

問い合わせフォームや申込みのような **動く部分だけ**、裏につなぐ。送信先は
**第6章の PostgreSQL**、本人確認が要るなら **第7章の門番**、通知は
**第10章のメール**だ。

静的な窓に、動的な点を最小限だけ足す ── サイト全体を動的にする必要は
ない。**大半は静的、要る所だけ動的**。

## Cloudflare で前段を借りる

配信を世界中で速くし、攻撃を弾く前段は、**Cloudflare** に借りられる。
自分のサーバを隠し、CDN と DDoS 防御をかぶせる ── メールの送信中継
(第10章)と同じ考え方だ。**主導権は自分の側に残し、規模と防御だけ借りる**。

## まとめ

社外の窓を静的に、入口を一つに。

- **静的サイト(Astro / Hugo)** ── Markdown を HTML に焼いて配る、速く・安全・安い
- **Caddy** ── 自動 HTTPS と、全アプリの入口を一枚に束ねる門
- **動的は最小限** ── フォームだけ第6章 DB・第7章門番・第10章メールにつなぐ
- **Cloudflare** ── 配信と防御を前段で借りる、主導権は自分の側

社内の道具と、社外の窓が揃った。最後の章では、これらすべての上に
**AI(自前の LLM と RAG)** を乗せ、Copilot の依存を断つ。

---

## 関連記事

- [第7章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [第9章: コードを手元に ── Forgejo と Zed](/ai-native-ways/software/code/)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
