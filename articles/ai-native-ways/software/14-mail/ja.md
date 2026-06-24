---
slug: mail
number: "06"
part: "2"
title: メールを自分の側に ── Stalwart と Thunderbird
subtitle: Exchange と Outlook の外へ ── 受信は自分で、送信は正直に
description: メールは事業の記録そのものだ。Stalwart は Rust 製の単一サーバで、SMTP・IMAP・JMAP・スパム対策・DKIM 署名を一つに備え、Exchange を置き換える。第2章の PostgreSQL に乗せ、Thunderbird など任意のクライアントで読む。ただし送信の到達性は難しい ── そこは認証付き中継に頼り、メールボックスの主導権だけ自分が持つ、という正直な設計を示す。
date: 2026.07.09
label: Independence 6
title_html: メールボックスを、<br><span class="accent">自分の側</span>に。
prev_slug: documents
prev_title: "文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む"
next_slug: meetings
next_title: "会議と予約を自分の側に ── Jitsi と Cal.com"
---

# メールを自分の側に ── Stalwart と Thunderbird

メールは、事業の記録そのものだ。やり取り・契約・履歴が、すべてそこに
積まれている。それを他社のサーバに預けたままにせず、**受信箱の主導権**を
自分の側に取り戻す。

ただし、メールは正直に語るべき領域でもある。**受信は易しく、送信(到達性)
は難しい**。この章は、その線引きをはっきりさせて立てる。

## なぜメールを自分の側に置くのか

- **記録の主導権** ── 過去メールの保管・検索・書き出しを、自分のルールで
- **人数課金から降りる** ── メールボックスの数で月額が積み上がらない
- **門番と一つに** ── アカウントを第3章の認証と揃える

## Stalwart を立てる

メールサーバは **Stalwart**。Rust 製の単一サーバに、**SMTP・IMAP・JMAP・
スパム対策・DKIM 署名**まで入っている。Exchange の置き換えだ。保管は
**第2章の PostgreSQL** に寄せられる。

```yaml
# compose.yaml ── 単一のメールサーバを立てる
services:
  mail:
    image: stalwartlabs/mail-server:latest
    volumes: ["./stalwart:/opt/stalwart-mail"]
    ports: ["25:25", "587:587", "465:465", "993:993", "8080:8080"]
    restart: always
```

管理画面(`:8080`)でドメインとメールボックスを作る。コードは書かない。

## DNS を整える ── MX・SPF・DKIM・DMARC

メールは、立てるより **DNS が本体**だ。次の四つを正しく置く。

```dns
example.com.      MX    10 mail.example.com.
example.com.      TXT   "v=spf1 mx -all"
default._domainkey.example.com.  TXT  "v=DKIM1; k=rsa; p=...(Stalwart が生成)"
_dmarc.example.com.  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

逆引き(PTR)も、サーバの IP に対して設定する。**ここを外すと、送ったメールが
相手に届かない**。

## 送信の到達性 ── 正直な話

自前サーバからの直接送信は、IP 評価・ブロックリスト・各社の判定に左右され、
**届かないことがある**。これは OSS の優劣ではなく、メールという仕組みの
現実だ。

だから、現実的な設計はこうする:

- **受信・保管・検索** ── 自分の Stalwart が持つ(ここが主導権の本体)
- **外向きの送信** ── 認証付きの **SMTP 中継**(送信専用サービス)を経由する

中継は送信の到達性だけを借りる薄い層で、メールボックスそのものは自分の側に
残る。**主導権を握る場所と、到達性を借りる場所を分ける** ── これが正直で
堅実なやり方だ。

> メールは「全部自前」が正解とは限らない。
> **受信箱は自分の側に、送信の到達性は借りる** ── 線を引いて立てる。

## クライアント ── Thunderbird

読み書きは、IMAP / JMAP を話す **任意のクライアント**でよい。**Thunderbird**
なら無料で、Windows・Mac・Linux で同じように動く。スマホは標準のメール
アプリがそのまま JMAP / IMAP でつながる。

## 移行 ── Microsoft 365 から

既存のメールは、IMAP 同士をまるごと同期する **imapsync** で運ぶ。

```bash
imapsync --host1 outlook.office365.com --user1 you@old \
         --host2 mail.example.com      --user2 you@new
```

一斉に切り替えなくてよい。**しばらく両方で受け、転送をかけて並行運用**し、
落ち着いてから MX を Stalwart に向ける(第9章)。

## まとめ

受信箱を、自分の側に。

- **Stalwart** ── SMTP・IMAP・JMAP・スパム対策・DKIM を単一サーバで(第2章 PostgreSQL に乗る)
- **DNS(MX・SPF・DKIM・DMARC・PTR)** ── メールの本体はここ
- **送信は中継に頼る** ── 受信箱は自分、到達性は借りる、と線を引く
- **Thunderbird** ── 無料・全 OS 共通のクライアント
- **imapsync** ── Microsoft 365 から並行移行、最後に MX を向ける

次章では、**会議と予約(Jitsi・Cal.com)** を立て、Teams と予約サービスを
自分の側に置く。

---

## 関連記事

- [第2章: 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [第3章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [第1章: Microsoft と Google から自立する ── 全体像と対応表](/ai-native-ways/software/independence/)
