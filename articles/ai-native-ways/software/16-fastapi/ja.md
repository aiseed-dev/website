---
slug: fastapi
number: "08"
part: "2"
title: API を作る ── FastAPI で基幹のロジックを出す
subtitle: 自社固有のロジックを一箇所の API にまとめ、どのアプリからも使えるようにする
description: 自立編の OSS で汎用は揃った。残るのは自社固有のロジック ── 基幹システムの中身だ。それを FastAPI で API として出し、公開Webのフォームからも社内アプリからも同じものを呼べるようにする。第1章の PostgreSQL を読み書きし、第2章の門番のトークンで本人確認する ── 新しい基盤は要らない。基幹はいきなり全部ではなく、よく使う処理から一本ずつ、現行を正解器に対話で。参考実装は kura。
date: 2026.07.15
label: Independence 8
title_html: 自社固有のロジックを、<br>一箇所の <span class="accent">API</span> に。
prev_slug: web
prev_title: "Webを公開する ── Cloudflare Pages（WordPress 代替）"
next_slug: ai
next_title: "自前の AI を据える ── LLM と RAG"
---

# API を作る ── FastAPI で基幹のロジックを出す

自立編の OSS で、汎用は揃った ── 認証、文書、メール、会議、公開Web。残るのは
**自社固有のロジック**、つまり基幹システムの中身だ。それを **FastAPI** で
API として出し、どのアプリからも使えるようにする。

## なぜ API にするのか

- 基幹ロジック(在庫・受発注・料金計算…)を、画面ごとに書き散らさず、**一箇所
  にまとめて API にする**
- 公開Web(第7章)のフォームも、社内アプリも、同じ API を呼ぶ ── 重複が消える
- Python(FastAPI)なら AI が速く書け、型と自動ドキュメント(OpenAPI)が付く

## 土台と門番の上に乗せる

API は、第1章の **PostgreSQL** を読み書きし、第2章の **門番(PocketBase)** の
トークンで本人確認する。新しい基盤は要らない ── すでにあるものに乗せる。

```python
# FastAPI ── 門番のトークンを確かめ、土台(DB)を引く
from fastapi import FastAPI, Depends
app = FastAPI()

@app.get("/orders")
def orders(user=Depends(verify_token)):       # 第2章の門番が誰かを確かめる
    return db.query("SELECT * FROM orders WHERE user_id=%s", [user.id])  # 第1章の DB
```

## 対話で、薄く

基幹をいきなり全部ではない。**よく使う処理から、一本ずつ**。AI と対話して
書き、現行と突き合わせて確かめる(導入編 第6章 VBA→Python と同じやり方だ)。
重い処理は裏で Python が捌き、結果だけ返す。

## 参考実装 ── kura

公開リポジトリ **kura**(`aiseed-dev/workspace`)が、この構成だ ── PocketBase
認証＋**FastAPI**＋Flet フロント。コードは第3章の Forgejo に置き、第7章の公開
Web や社内アプリから呼ぶ。

## まとめ

- 自社固有のロジックは、FastAPI で **一箇所の API** に
- **第1章の DB・第2章の門番**に乗る ── 新しい基盤は要らない
- よく使う処理から一本ずつ、**現行を正解器に、対話で薄く**

次章では、これらすべての上に **AI(自前の LLM と RAG)** を乗せ、Copilot の
依存を断つ。

---

## 関連記事

- [第1章: 土台を据える ── PostgreSQL・SQLite ほか](/ai-native-ways/software/foundation/)
- [第2章: 門番を立てる ── PocketBase で認証を一つに](/ai-native-ways/software/auth/)
- [参考実装 kura ── 自前の Microsoft 365 / Google Workspace 代替](https://github.com/aiseed-dev/workspace)
