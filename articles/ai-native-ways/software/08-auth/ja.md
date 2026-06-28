---
slug: auth
number: "03"
part: "2"
title: 門番を立てる ── PocketBase で認証を一つに
subtitle: 共有するのは身元(認証)だけ ── アクセス制御は各サーバーが持つ。中央は最小限、守りは多層で
description: 認証は、各アプリが個別に作るものではない。一度立てて皆で共有する門番だ。だが門番が持つのは最小限の共通＝身元だけ。「何ができるか」=アクセス制御は、各アプリ・各サーバーが自分で持つ(多層防御)。「通った者は中ではどこでも通す」境界防御には頼らない。PocketBase は単一バイナリに、メール認証・OAuth2・ワンタイム・MFA・管理画面・REST API を備える。身元は門番が持ち、業務データは PostgreSQL に置く。Microsoft Entra ID への月額・人数課金から降りる。
date: 2026.07.02
label: Independence 3
title_html: 身元は<span class="accent">一つ</span>、<br>守りは<span class="accent">各サーバー</span>で。
prev_slug: foundation
prev_title: "土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars"
next_slug: code
next_title: "コードを手元に ── Forgejo と Zed"
---

# 門番を立てる ── PocketBase で認証を一つに

土台(PostgreSQL・SQLite)の上に、最初に立てるのは **門番** ── 認証だ。
どのアプリも、入口で「誰か」を確かめる。その確認を **アプリごとに作るのは、
車輪の再発明の筆頭**であり、しかも一番間違えやすい(セキュリティの中心だ)。

だから認証も、書かない。**立てる**。汎用中の汎用は、すでに OSS にある。

## なぜ認証を最初に立てるのか

土台の次が門番である理由は単純だ。**この後に立てる全アプリが、同じ身元
(誰か)を共有する**。文書も、講座の予約も、基幹システムも ── 利用者は一度
ログインすればいい。

ただし、ここで思想を一つ決めておく。**門番が持つのは、最小限の共通＝
身元(認証)だけ**だ。「何ができるか」=アクセス制御は、**各アプリ・各
サーバーが、自分で持つ**。「門番を通った者は、中ではどこでも通す」── この
一枚の壁(境界防御)に頼る思想は採らない。一箇所破られれば全部が抜けるからだ。
**中央は最小限、守りは各サーバーで多層に**。これが、分散して強い形だ。

自前のログイン実装は、ハッシュ化・セッション・トークン失効・二要素・
パスワード再設定・ソーシャルログイン ── どれ一つ手を抜けない。**身元の
確認だけを一度立てて共有し、権限の判断は各アプリに残す**ほうが、速く、
安全で、強い。

## PocketBase を立てる

門番は **PocketBase**。Go 製の **単一バイナリ**に、認証・管理画面・REST /
リアルタイム API・ファイル保管まで入っている。2-02で触れた **SQLite の上で
動く**ので、別のサーバも要らない。`compose.yaml` 一枚で立つ。

```yaml
# compose.yaml ── 単一バイナリの門番を置くだけ
services:
  auth:
    image: ghcr.io/muchobien/pocketbase:latest
    ports: ["8090:8090"]
    volumes: ["./pb_data:/pb_data"]
    restart: always
```

```bash
docker compose up -d
# 管理者を一人作る
docker compose exec auth pocketbase superuser create admin@example.com 'change-me'
```

`http://localhost:8090/_/` が管理画面だ。ユーザー、ログイン方法、発行する
トークンの寿命 ── すべてここから設定する。コードは、まだ一行も書いていない。

## メール・OAuth・ワンタイムを開く

PocketBase の `users` コレクションに、要る入口を有効にするだけでよい。

- **メール + パスワード** ── 既定。確認メールとパスワード再設定も内蔵
- **OAuth2** ── Google・Microsoft・GitHub を「ログイン」ボタンに足す
- **ワンタイム(OTP)** ── メールに届く番号だけで入る、パスワードレス
- **MFA** ── 二要素を全体、または管理者だけに強制

Entra ID(旧 Azure AD)からの移行中も、**OAuth2 に Microsoft を残せば**、
利用者は今までの Microsoft アカウントのまま入れる。門番だけ自分の側へ
移し、利用者の体験は変えない。

## 身元は門番、業務データは倉庫

ここが設計の要だ。**身元(誰か)は門番が持ち、業務データ(何をしたか)は
PostgreSQL に置く**(2-02)。門番と倉庫を分ける。

アプリは、門番が発行した **トークンの署名を手元で確かめて `user.id` を
取り出す**(門番に毎回問い合わせない ── 門番が一瞬落ちても動く)。そのうえで、
**この利用者がこの操作をしてよいか**は、アプリ自身が判断する。

```python
# 業務アプリ側 ── 署名を手元で確かめ、権限も自分で判断する
user_id = verify_token(request.headers["Authorization"])   # 門番の公開鍵で署名検証(毎回問い合わせない)
require(can_read_orders(user_id))                           # 「何ができるか」は、このアプリが決める
orders  = pg.execute("SELECT * FROM orders WHERE user_id = %s", [user_id])
```

身元の確認は門番に集約し、**権限の判断は各アプリに残す**。身元を共有し
つつ、守りは各サーバーに分散する ── これが多層防御だ。

> 身元は、各アプリが各々作るものではない ── 一度立てて皆で共有する。
> **だが「何ができるか」は、各サーバーが自分で守る**。

## 入口の前に立てる ── リバースプロキシ

自作アプリは PocketBase の SDK でそのまま守れる。一方、文書(OnlyOffice)や
コード(Forgejo)のような **既製の OSS は、各々が自前のログインを持つ**。
これらは入口の前に **リバースプロキシ(Caddy)** を一枚置き、社外には
門番を通った者だけを通す ── ただしこれは**最初の一枚**であって、各アプリも
自分で身元と権限を確かめる(境界の中も信用しない＝多層防御)。

```caddy
# Caddyfile ── 門番を通した先に各アプリを並べる
auth.example.com   { reverse_proxy auth:8090 }
docs.example.com   { reverse_proxy onlyoffice:80 }
git.example.com    { reverse_proxy forgejo:3000 }
```

将来、これらを **一度のログインで束ねる(SSO)** なら、OIDC を話す層を
前に足す ── だが多くの社内利用は、門番と各アプリのログインで足りる。
**まず身元を一つに共有することが先**で、完全な統合は後でよい。

## Entra ID から降りる

Microsoft Entra ID は、利用者数で月額が積み上がる。門番を自分の側に
立てれば、その課金から降りる。手順は段階的でよい。

1. PocketBase を立て、OAuth2 に Microsoft を残す(既存アカウントで入れる)
2. 新しいアプリは PocketBase のトークンで作る
3. 利用者を順に PocketBase の `users` へ移す(CSV で一括登録できる)
4. 全員が移ったら、OAuth2 の Microsoft を外す ── Entra への依存が切れる

止めるのは一度ではない。**並行で動かし、移り終えてから古い門を閉じる**
(2-09)。

## まとめ

土台の上に、最初の門番を。

- **PocketBase** ── 単一バイナリに認証・管理画面・API・ファイル保管(SQLite の上)
- **メール / OAuth2 / OTP / MFA** ── 要る入口だけ管理画面から開く
- **門番と倉庫を分ける** ── 身元は PocketBase、業務データは PostgreSQL
- **中央は最小限、守りは各サーバーで** ── 門番は身元だけ、アクセス制御は各アプリ(多層防御)
- **リバースプロキシ** ── 既製 OSS は門を通した先に並べる(最初の一枚であって、唯一の壁ではない)
- **Entra ID から降りる** ── OAuth2 で橋を架け、移り終えてから断つ

書いたコードは、署名を確かめ、権限を判断する数行だけ。**身元は共有し、
守りは各サーバーで**。
次章では、その門の内側に **文書(OnlyOffice)** を据え、Word・Excel・
PowerPoint を自分の側に置く。

---

## 関連記事

- [2-02: 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [参考実装 kura ── PocketBase を門番に使う自前ワークスペース](https://github.com/aiseed-dev/workspace)
- [2-01: Microsoft と Google から自立する ── 全体像と対応表](/ai-native-ways/software/independence/)
- [2-09: API を作る ── FastAPI で基幹のロジックを出す](/ai-native-ways/software/fastapi/)
