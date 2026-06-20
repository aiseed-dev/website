---
slug: meetings
number: "11"
title: 会議と予約を自分の側に ── Jitsi と Cal.com
subtitle: Teams の会議も、Calendly の予約も、講座のウェビナーも ── 自分のドメインで
description: ビデオ会議は Jitsi、予約は Cal.com、講座・ウェビナーは BigBlueButton。Teams・Zoom・Calendly・Microsoft Bookings を、自分のドメインと自分のサーバに置き換える。予約は第6章の PostgreSQL に乗り、第10章のメールで確認を送る。人数・分課金から降り、会議のリンクも記録も自分の側に持つ。
date: 2026.07.11
label: Software 11
title_html: 会議も予約も、<br><span class="accent">自分のドメイン</span>で。
prev_slug: mail
prev_title: メールを自分の側に ── Stalwart と Thunderbird
next_slug: web
next_title: 社外に見せる窓 ── 静的サイトと Caddy
---

# 会議と予約を自分の側に ── Jitsi と Cal.com

会議も予約も、汎用の機能だ。Teams の打ち合わせ、Calendly の日程調整、
Microsoft Bookings の講座予約 ── どれも、すでに OSS で共有されている。
ここでは三つを立て、自分のドメインの上に置く。

- **ビデオ会議** ── Jitsi Meet(Teams・Zoom の代わり)
- **予約** ── Cal.com(Calendly・Bookings の代わり)
- **講座・ウェビナー** ── BigBlueButton(大人数の授業向け)

## Jitsi Meet を立てる

少人数〜中人数の会議は **Jitsi Meet**。**参加者はブラウザだけ**でよく、
アプリのインストールも、アカウントも要らない。リンクを送れば会議が始まる。

```bash
# 公式の compose 一式を使う
git clone https://github.com/jitsi/docker-jitsi-meet
cd docker-jitsi-meet && cp env.example .env && ./gen-passwords.sh
docker compose up -d        # web・prosody・jicofo・jvb が立つ
```

`meet.example.com` を、自分のロゴと自分のドメインで配れる。録画もチャットも
画面共有も、標準で揃う。

> 大人数(数百人)の会議は、映像中継(JVB)を増設して捌く。これは
> 「立てる」より「足す」── 規模に応じてサーバを並べる作業だ。

## 講座は BigBlueButton

セミナーや授業のように、**ホワイトボード・挙手・ブレイクアウト・出席**が
要る場面は **BigBlueButton**。教育向けに作られたウェビナー基盤で、第6章で
触れた「講座」のための道具だ。

BigBlueButton は専用のインストーラを持ち、Jitsi より重い。**日常会議は
Jitsi、講座は BigBlueButton**、と用途で分けて立てる。

## 予約は Cal.com

日程調整・講座予約は **Cal.com**。Calendly と Microsoft Bookings の置き換え
で、データは **第6章の PostgreSQL** に乗る。

```yaml
# compose.yaml ── 予約を第6章の DB に乗せて立てる
services:
  booking:
    image: calcom/cal.com:latest
    environment:
      DATABASE_URL: postgres://postgres:change-me@db:5432/calcom
      NEXT_PUBLIC_WEBAPP_URL: https://book.example.com
    restart: always
```

予約が入れば、**第10章のメール**で確認と前日リマインドが飛び、Jitsi の
会議リンクが自動で添えられる。**土台(DB)・門番(認証)・メール**の上に、
予約がそのまま乗る ── 先に据えたものが、ここで効いてくる。

## カレンダーと門番

予定の同期は **CalDAV**(Radicale、または第8章の Nextcloud カレンダー)で、
Thunderbird やスマホの標準カレンダーとつながる。Cal.com と各アプリは、
第7章の門番の内側、リバースプロキシの先に置く。

```caddy
meet.example.com { reverse_proxy jitsi-web:80 }
book.example.com { reverse_proxy booking:3000 }
```

## まとめ

会議も予約も、自分のドメインで。

- **Jitsi Meet** ── ブラウザだけの会議、Teams・Zoom の代わり
- **BigBlueButton** ── ホワイトボードと出席のある講座・ウェビナー
- **Cal.com** ── Calendly・Bookings の代わり(第6章 PostgreSQL に乗る)
- **連携** ── 予約 → 第10章のメールで確認、Jitsi リンクを自動添付
- **CalDAV + 門番** ── 標準カレンダーと同期、リバースプロキシの内側に

ここまでで、土台・門番・文書・コード・メール・会議・予約が揃った。
次章では、これらを社外に見せる窓 ── **Web(静的サイトと Caddy)** を立てる。

---

## 関連記事

- [第6章: 土台を据える ── PostgreSQL・SQLite・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [第10章: メールを自分の側に ── Stalwart と Thunderbird](/ai-native-ways/software/mail/)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
