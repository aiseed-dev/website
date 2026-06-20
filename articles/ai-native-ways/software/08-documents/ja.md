---
slug: documents
number: "08"
title: 文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む
subtitle: 別の置き場は足さない ── 第7章の門番に文書を乗せ、編集エンジンだけを組み込む
description: Word・Excel・PowerPoint は、人が書き人が読む入出力の道具だ。Nextcloud のような別の保管アプリは足さず、第7章で立てた PocketBase をそのまま文書の置き場(保管・認証・共有)にして、OnlyOffice Docs を編集エンジンだけ組み込む ── 独自の、薄い文書アプリ。docx・xlsx・pptx を高互換で開き、同時編集し、門番の内側に最初から入る。完成品の DocSpace は Active Directory を呼び戻すので使わない。形式は変えず、主導権だけ取り戻す。
date: 2026.07.04
label: Software 08
title_html: 文書を、<span class="accent">門番の中</span>に<br>そのまま置く。
prev_slug: auth
prev_title: 門番を立てる ── PocketBase で認証を一つに
next_slug: code
next_title: コードを手元に ── Forgejo と Zed
---

# 文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む

門番(第7章)の内側に、最初に置く道具は **文書**だ。Word・Excel・
PowerPoint ── これらは、人が書き、人が読む **入出力の道具**であって、
その役割は変わらない(第6章)。変えるのは、**形式の互換と、置き場の
主導権**だけだ。

だから新しい文書形式に乗り換えるのではない。**`docx`・`xlsx`・`pptx` を
そのまま**読み書きできる編集エンジンを、自分のアプリに組み込む。

## なぜ別の保管アプリを足さないのか

文書というと Nextcloud のような「OneDrive 代替」を丸ごと立てたくなる。
だが Nextcloud は、PHP の重厚なモノリスで、**旧来型の重いソフト**だ。
別のユーザ体系・別のデータベースまで抱え込む ── この導入編が選んできた
**単一バイナリの軽さ**(PocketBase・Stalwart・Forgejo)とは、逆を向いている。

第7章で、認証も保管も REST も持つ **PocketBase** をもう立てた。文書の
置き場は、**それで足りる**。

- **保管** ── PocketBase のファイル付きレコードに、文書を置く
- **認証** ── 第7章の門番がそのまま効く(別ログインを作らない)
- **共有** ── PocketBase のアクセスルールで、社内・社外リンクを出す

足すのは、**編集エンジンだけ**だ。OnlyOffice は「Docs(Document
Server)」という編集エンジンを単体で提供していて、保管は任意のアプリに
任せられる。だから **OnlyOffice Docs を PocketBase に組み込む** ── これが
いちばん薄い。

## Docs を選ぶ ── DocSpace は選ばない

ONLYOFFICE には、完成品のプラットフォーム **DocSpace** もある。だが、これは
**選ばない**。理由は二つだ。

- **Active Directory を呼び戻す** ── DocSpace は LDAP / AD / SAML SSO を前提に
  作られている。第7章でせっかく切った **Microsoft の認証(AD)が、また居座る**
- **無料版に同時接続20の制限** ── DocSpace Community は、同時に開ける編集タブが
  20までに制限される。増えればエンタープライズ版(有償)へ ── ロックインの入口だ

要るのは、**編集エンジンだけ**だ。そして朗報がある ── **Docs 9.4 で、
Community 版の「同時接続20」制限が撤廃された**(エンジン単体では無制限)。
さらに RabbitMQ や別 DB への依存も外れ、**単一プロセス**になった。PocketBase
(単一バイナリ)と組めば、エンタープライズ級の同時編集が、**無料で・軽く**
手に入る。

> プラットフォーム(DocSpace)は、自由と引き換えに AD を連れてくる。
> **エンジン(Docs)だけを取り、認証は第7章の門番に委ねる**。

## OnlyOffice Docs を立てる

編集エンジン **OnlyOffice Docs** を立てる。これは編集だけを担い、ファイル
そのものは持たない。改ざん防止に **JWT の秘密鍵**を一つ設定する。

```yaml
# compose.yaml ── 編集エンジンだけを立てる
services:
  onlyoffice:
    image: onlyoffice/documentserver:latest
    environment:
      JWT_SECRET: change-me        # PocketBase 側と共有する署名鍵
    restart: always
```

`docx`・`xlsx`・`pptx` を、レイアウト崩れなく開き、同じ形式で保存し、
複数人で **同時編集**できる ── そのエンジンが、これで手に入る。

社内で使う分には、Community 版(AGPLv3)で問題ない。**自社 SaaS として
外販する場合だけ**、AGPL のコピーレフトと表示義務(画面に ONLYOFFICE を
明記)に注意する ── そこは商用ライセンスを検討する。

## PocketBase に文書を置く

文書は、第7章の **PocketBase** に `documents` コレクションを作り、ファイル
フィールドに収める。所有者・共有先・更新日時も、同じレコードに持つ。

```js
// 文書を一つ、門番(PocketBase)に保存する
await pb.collection('documents').create({
  title: '見積_2026.xlsx',
  owner: pb.authStore.model.id,   // 第7章の門番が誰かを知っている
  file:  xlsxBlob,                // 実体は PocketBase が保管する
})
```

新しい DB も、新しいログインも要らない。**文書は最初から門番の中にある**。

## つなぐ ── 開いて、保存する

一覧から文書を開くと、ブラウザに OnlyOffice の編集画面が立ち上がる。
アプリは **ファイルの場所**と **保存先(コールバック)**を、JWT で署名して
エンジンに渡すだけだ。

```js
// 編集画面を開く ── 署名つきの設定をエンジンに渡す
new DocsAPI.DocEditor("editor", {
  document:     { url: fileUrl, key: docId },          // PocketBase 上の実体
  editorConfig: { callbackUrl: saveBackUrl },          // 保存先も PocketBase
  token:        jwt,                                    // JWT_SECRET で署名
})
```

人が編集を終えると、OnlyOffice Docs が **コールバックに編集後ファイルを
返し**、それを PocketBase のレコードへ書き戻す。同時編集の調停は、エンジン
が引き受ける。アプリが書くのは、この受け渡しの数行だけだ。

## 門番はそのまま ── 別ログインを作らない

ここが「独自に組む」最大の利点だ。文書は **第7章の門番の中に最初から
ある**ので、Nextcloud のような別アカウントも、前段の認証プロキシも要ら
ない。誰がどの文書を開けるかは、PocketBase のアクセスルール一つで決まる。

## 既存の文書を移す

OneDrive・SharePoint に積まれた文書は、**形式を変えずに**運べる。
`docx`・`xlsx`・`pptx` は OnlyOffice Docs がそのまま開くので、変換は要らない。

```bash
# rclone で吸い出し、PocketBase のレコードへ取り込む
rclone copy onedrive:Documents ./inbox --progress
# inbox/ の各ファイルを documents コレクションへ登録(スクリプト一回)
```

移行は段階的でよい。**並行で動かし、移り終えてから旧ストレージを
解約する**(親シリーズ第7章)。

## 人は OnlyOffice、機械は Polars

ここで第6章とつながる。**人は OnlyOffice(Excel 形式)で入れて読み、
機械は Polars と DuckDB で裏のデータを捌く**。同じ `.xlsx` を、人は編集の
道具として、機械は入力として扱う ── 役割で分ける。

- 人が作る集計表・申請書・提案書 ── OnlyOffice Docs で開いて、しまう
- 数百万行の突き合わせ・全社集計 ── Polars が `.xlsx` を読み、PostgreSQL に書く

表計算は「人の道具」に戻り、重い処理は「機械の道具」へ移る。

> 文書形式も置き場も、別物を足して増やさない。
> **門番の中にそのまま置き、編集エンジンだけを組み込む**。

## まとめ

門番の中に、文書をそのまま。

- **OnlyOffice Docs** ── `docx`・`xlsx`・`pptx` を高互換で開く編集エンジン(保管は持たない)
- **PocketBase** ── 第7章の門番を、そのまま文書の保管・認証・共有に使う
- **組み込みは数行** ── ファイルの場所と保存先を JWT で署名して渡すだけ
- **別ログインなし** ── 文書は最初から門番の中、アクセスはルール一つ
- **人と機械の分担** ── 人は OnlyOffice Docs、機械は Polars / DuckDB

別の保管アプリを足さず、**手元の門番に組み込んだ**。次章では、ビルダーの
仕事場 ── **コードの共有(Forgejo)** を立て、GitHub と Azure DevOps を
自分の側に置く。

---

## 関連記事

- [第6章: 土台を据える ── PostgreSQL・SQLite・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [第7章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
