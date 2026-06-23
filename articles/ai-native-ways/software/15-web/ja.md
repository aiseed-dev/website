---
slug: web
number: "07"
part: "2"
title: Webを公開する ── Cloudflare Pages（WordPress 代替）
subtitle: 動的な WordPress をやめ、静的サイトをサーバ無しで公開する ── ビルド・確認・デプロイを分けて
description: 導入編で AI と作った静的サイトを、自分の側から公開する。動的な WordPress をやめ、焼いた HTML を Cloudflare Pages に置く ── サーバは持たない。CDN と自動 HTTPS は Cloudflare に任せ、ソースとビルドは自分の手元に残す。肝は「ビルド → 確認 → デプロイ」を分けること。確認した HTML と本番に上げる HTML を同じにする。内部の道具は門番の内側に残す ── 窓は借り、金庫は自分に。
date: 2026.07.14
label: Independence 7
title_html: WordPress をやめ、<br><span class="accent">サーバ無し</span>で公開する。
prev_slug: meetings
prev_title: "会議と予約を自分の側に ── Jitsi と Cal.com"
next_slug: fastapi
next_title: "API を作る ── FastAPI で基幹のロジックを出す"
---

# Webを公開する ── Cloudflare Pages（WordPress 代替）

導入編で、AI と対話して静的な Web サイトを作った(導入編 第7章)。ここでは、
それを **自分の側から公開する**。動的な **WordPress をやめ**、焼いた HTML を
**Cloudflare Pages** に置く ── サーバは持たない。

## なぜ WordPress をやめるのか

WordPress は、動的サーバ・データベース・プラグインの塊だ。更新・保守・
セキュリティの負担が、ずっと続く。会社サイトの中身はめったに変わらないの
だから、**静的でよい**。静的なら、サーバも DB も要らず、攻撃される面も
ほぼ無い。導入編で作った `html/` を、そのまま公開する。

## Cloudflare Pages に置く ── サーバを持たない

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

問い合わせフォームのような **動く部分だけ**、裏につなぐ。送信先は、門番
(第2章)の内側に置いた自分の API(認証は門番、保存は第1章の DB、通知は
第5章のメール)。**大半は静的、動くのは要る所だけ**。

## 内部の道具は別 ── 窓は借り、金庫は自分に

公開サイトは Cloudflare Pages に **借りる**。だが、自立編で立てた **内部の
道具**(門番・文書・コード・メール・会議)は別だ。秘密や生のデータが通る
ので、門番(自分のリバースプロキシ)の内側に残す。

- **公開サイト**(静的・秘密なし)── Cloudflare Pages に借りる
- **内部の道具**(認証・業務データ)── 自分の側、門番の内側に持つ

**窓は借り、金庫は自分に**。借りる所と、自分で持つ所を、分けて決める。

## まとめ

- **WordPress をやめる** ── 動的サーバ・DB・プラグインの保守負担を捨てる
- **Cloudflare Pages** ── サーバ無しで公開、CDN・自動 HTTPS を借りる
- **ビルド → 確認 → デプロイを分ける** ── 確認した物を、そのまま本番へ
- **ドメインは自動で切り替わる** ── カスタムドメインで A レコードが Pages を指す、メールは触らない
- **窓は借り、金庫は自分に** ── 内部の道具は門番の内側に残す

次章では、基幹システムのロジックを **API(FastAPI)** として出し、各アプリ
から使えるようにする。

---

## 関連記事

- [導入編 第7章: Webサイトを作る ── AI と対話して](/ai-native-ways/software/website/)
- [第2章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
