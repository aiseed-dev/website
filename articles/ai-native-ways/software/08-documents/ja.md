---
slug: documents
number: "08"
title: 文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む
subtitle: 別の置き場は足さない ── 第7章の門番に文書を乗せ、編集エンジンだけを組み込む
description: Word・Excel・PowerPoint は、人が書き人が読む入出力の道具だ。Nextcloud のような別の保管アプリは足さず、文書はファイルのまま自分のストレージに置き、認証は第7章の PocketBase、権限は xattr に持たせ、OnlyOffice Docs を編集エンジンだけ組み込む ── 独自の、薄い文書アプリ。docx・xlsx・pptx を高互換で開き、同時編集し、権限のための別 DB もログインも持たない。完成品の DocSpace は Active Directory を呼び戻すので使わない。実装は公開リポジトリ kura。形式は変えず、主導権だけ取り戻す。
date: 2026.07.04
label: Software 08
title_html: 文書は<span class="accent">ファイル</span>のまま、<br>認証だけ門番に。
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

第7章で、認証を持つ **PocketBase** をもう立てた。文書の置き場は、**それを
門番にして、あとはファイルで足りる**。

- **実体** ── ファイルそのもの(自分のストレージ)。重い保管アプリは要らない
- **認証** ── 第7章の門番(PocketBase)がそのまま効く(別ログインを作らない)
- **権限・共有** ── ファイル自身(xattr)が持ち、門番が身元を確かめる

足すのは、**編集エンジンだけ**だ。OnlyOffice は「Docs(Document
Server)」という編集エンジンを単体で提供していて、保管は任意のアプリに
任せられる。だから **門番(PocketBase)で守ったファイルに、OnlyOffice Docs
を重ねる** ── これがいちばん薄い。

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

## 文書はファイルで持つ ── 認証は門番、権限は xattr

文書の実体は、**ただのファイル**として自分のストレージに置く。PocketBase の
レコードに blob として埋め込むのではなく、`docx`・`xlsx`・`pptx` をファイルの
まま持つ ── そのほうが、後で機械(Polars・AI)がそのまま読める。

- **実体** ── ファイルシステム上のファイル(自分のストレージ)
- **認証** ── 第7章の門番(PocketBase)が「誰か」を確かめる
- **権限** ── ファイル自身に持たせる ── 拡張属性(xattr)

```bash
# 権限は、別 DB ではなくファイル自身に貼る
setfattr -n user.ws.perm    -v 'team:rw' 見積_2026.xlsx
setfattr -n user.ws.creator -v 'alice'   見積_2026.xlsx
```

権限のためだけの別データベースは要らない。**門番が身元を、ファイルが権限を**
持つ ── 役割を分ける。

## つなぐ ── 開いて、保存する

一覧から文書を開くと、ブラウザに OnlyOffice の編集画面が立ち上がる。
アプリは **ファイルの場所**と **保存先(コールバック)**を、JWT で署名して
エンジンに渡すだけだ。

```js
// 編集画面を開く ── 署名つきの設定をエンジンに渡す
new DocsAPI.DocEditor("editor", {
  document:     { url: fileUrl, key: docId },          // ファイルの場所
  editorConfig: { callbackUrl: saveBackUrl },          // 保存先(ファイルへ書き戻す)
  token:        jwt,                                    // JWT_SECRET で署名
})
```

人が編集を終えると、OnlyOffice Docs が **コールバックに編集後ファイルを
返し**、それを **元のファイルへ書き戻す**。同時編集の調停は、エンジンが
引き受ける。アプリが書くのは、この受け渡しの数行だけだ。

## 門番はそのまま ── 別ログインを作らない

ここが「独自に組む」最大の利点だ。**認証は第7章の門番がそのまま効き、
権限はファイル(xattr)が持つ**ので、Nextcloud のような別アカウントも、
権限のための別データベースも要らない。誰がどの文書を開けるかは、門番が
確かめた身元と、ファイルに貼った権限だけで決まる。

## 既存の文書を移す

OneDrive・SharePoint に積まれた文書は、**形式を変えずに**運べる。
`docx`・`xlsx`・`pptx` は OnlyOffice Docs がそのまま開くので、変換は要らない。

```bash
# rclone で吸い出し、自分のストレージへ並べる
rclone copy onedrive:Documents ./inbox --progress
# inbox/ の各ファイルに xattr で権限を貼る(スクリプト一回)
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
> **ファイルのまま置き、認証だけ門番に委ね、編集エンジンだけを組み込む**。

## 参考実装 ── kura

この構成を実際に組んだのが、公開リポジトリ **kura**(`aiseed-dev/workspace`)
だ。中小の業務利用(1 インスタンス約 100 人、増えれば分散)を狙った、
Microsoft 365 / Google Workspace の自前代替で、本章とそのまま重なる。

- **認証** ── PocketBase(差し替え可能なトークン検証＋短期キャッシュ)
- **権限** ── ファイルの xattr(`user.ws.perm` / `user.ws.creator`)、権限 DB を持たない
- **実体** ── ファイルそのもの(「AI との接面はファイル」)
- **編集** ── OnlyOffice Docs を JWT・コールバックで重ねる(FastAPI + Flet)

本章は、この設計を言葉にしたものだ。コードで見たければ、kura を読めばいい。

## まとめ

ファイルのまま、認証だけ門番に。

- **OnlyOffice Docs** ── `docx`・`xlsx`・`pptx` を高互換で開く編集エンジン(保管は持たない)
- **実体はファイル** ── 自分のストレージに置き、機械(Polars・AI)がそのまま読める
- **認証は門番(PocketBase)/権限は xattr** ── 権限のための別 DB を持たない
- **組み込みは数行** ── ファイルの場所と保存先を JWT で署名して渡すだけ
- **人と機械の分担** ── 人は OnlyOffice Docs、機械は Polars / DuckDB

別の保管アプリを足さず、**ファイルのまま、手元の門番に組み込んだ**。次章
では、ビルダーの仕事場 ── **コードの共有(Forgejo)** を立て、GitHub と
Azure DevOps を自分の側に置く。

---

## 関連記事

- [第6章: 土台を据える ── PostgreSQL・SQLite・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [第7章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [参考実装 kura ── 自前の Microsoft 365 / Google Workspace 代替](https://github.com/aiseed-dev/workspace)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
