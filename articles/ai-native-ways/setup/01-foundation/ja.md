---
slug: foundation
number: "01"
title: 土台を据える ── PostgreSQL・pgvector・DuckDB
subtitle: すべてが乗るデータ基盤を、最初に自分の側に立てる
description: 導入編の最初は、すべてが乗るデータ基盤 ── PostgreSQL。認証も分析も AI の RAG も予約も、ここに乗る。docker で立て、pgvector を有効化し、Azure SQL から pgloader で移す。分析は列指向の DuckDB を重ね、Excel や Power BI を大差で抜く。汎用は OSS で共有されている ── 書くのではなく、立てる。
date: 2026.07.01
label: Setup 01
title_html: まず<span class="accent">データ基盤</span>を、<br>自分の手元に立てる。
prev_slug:
prev_title:
next_slug:
next_title:
---

# 土台を据える ── PostgreSQL・pgvector・DuckDB

**ビルダーの仕事は、コードを書くことから始まらない。実績ある OSS を
立てることから始まる**(開発編 第5章)。汎用的な機能は、もう世界で
共有されている ── だから「書く」のではなく「立てる」。

この導入編では、Microsoft 365 と基幹のベンダー製品を置き換える OSS を、
一つずつ実際に立てていく。最初は **データ基盤**だ。認証も、分析も、AI の
RAG も、講座の予約も、基幹システムも ── **すべてがこの上に乗る**。だから
最初に据える。

## なぜ土台(データ)から始めるのか

順番には理由がある。後の章で立てるものの多くが、データベースに依存する:

- **分析**(DuckDB)は、ここのテーブルと Parquet を読む
- **AI の RAG**(Command A+)は、`pgvector` で類似検索する
- **講座の予約**(Cal.com)や **基幹システム**は、ここに読み書きする

土台が先にあれば、上に立つものは「すでにある DB に乗せる」だけになる。
**先に据えるほど、後が軽い**。

## PostgreSQL を立てる

データベースは **PostgreSQL**。オープンソース、無料、商用可。Oracle や
SQL Server と同等以上の機能を持ち、Claude が最も得意とする方言だ
(開発編・親シリーズ第14章)。

`compose.yaml` 一枚で立つ。

```yaml
# compose.yaml ── PostgreSQL + pgvector 同梱イメージ
services:
  db:
    image: pgvector/pgvector:pg17
    environment:
      POSTGRES_PASSWORD: change-me
      POSTGRES_DB: app
    ports: ["5432:5432"]
    volumes: ["./pgdata:/var/lib/postgresql/data"]
    restart: always
```

```bash
docker compose up -d            # 起動
docker compose exec db psql -U postgres -d app -c '\l'   # 接続確認
```

`pgvector/pgvector` イメージを使うと、後で要る **ベクトル拡張が最初から
入っている**。素の `postgres` イメージでも動くが、その場合は拡張を別途
入れる(次節)。

## pgvector を有効化する

AI の RAG(導入編・後の章)で使う **ベクトル検索**を、いま有効にして
おく。拡張を一行で足すだけだ。

```sql
-- データベースに一度だけ実行
CREATE EXTENSION IF NOT EXISTS vector;

-- 埋め込みを持つテーブルの例(1024 次元は bge-m3 の例)
CREATE TABLE docs (
  id    bigserial PRIMARY KEY,
  body  text,
  embedding vector(1024)
);
```

これで、文書を「意味」で検索する土台ができた。`embedding` に埋め込みを
入れ、`ORDER BY embedding <=> :query` で近いものを引く ── 実際の RAG
パイプラインは AI の章で組む。**いまは器だけ用意しておく**。

## Azure SQL から移す

既存の Azure SQL / SQL Server がある場合は、`pgloader` がスキーマも
データも一括で運ぶ。

```bash
pgloader mssql://user:pass@azure-host/db \
         postgresql://postgres:change-me@localhost/app
```

標準 SQL(`SELECT`・`JOIN`・ウィンドウ関数)はそのまま動く。捨てるのは
**ベンダー方言の T-SQL だけ**だ。ストアドに埋まった業務ロジックは、
Claude が抽出して Python / Ruby に翻訳する(開発編)。あとは旧 DB と
並行稼働で出力を突き合わせ、差分が消えたら旧を止める(親シリーズ第7章)。

> 移行は「全部を書き直す」ことではない。
> **標準に乗せ替え、方言だけ捨てる** ことだ。

## DuckDB で分析する ── Excel と Power BI を大差で抜く

集計・分析は、PostgreSQL の上に **DuckDB** を重ねる。列指向(カラムナ)の
分析エンジンで、1 ファイル、サーバー不要。Excel が約 104 万行で頭打ち
なのに対し、**ノート PC 一台で数億行を秒で集計する**。

```bash
pip install duckdb polars       # これだけ
```

```python
import duckdb
# Parquet も PostgreSQL も CSV も、その場で SQL で串刺し集計
duckdb.sql("INSTALL postgres; LOAD postgres;")
duckdb.sql("ATTACH 'dbname=app user=postgres host=localhost' AS pg (TYPE postgres)")
duckdb.sql("SELECT 部門, sum(売上) FROM pg.sales GROUP BY 部門 ORDER BY 2 DESC")
```

データを移し替えず、**置いた場所のまま** 分析できる。SQL は Claude が
書く ── 「先月比で異常な部門は」を、手元の実データに対して、追加料金
ゼロで何度でも問える。Power BI のクラウド従量・人数課金から見れば、
これは別次元だ。

巨大データを常時集計するなら、列指向 DB サーバーの **ClickHouse** に
載せ替える。だが大半の社内分析は、DuckDB 一つで足りる。

## まとめ

データ基盤を、最初に自分の側へ。

- **PostgreSQL**(+ pgvector)── 認証・予約・基幹・RAG が乗る器
- **pgvector** ── 意味検索の土台(RAG は AI の章で)
- **pgloader** ── Azure SQL からの一括移行、方言だけ捨てる
- **DuckDB**(+ Polars)── 列指向分析で Excel / Power BI を大差で抜く

書いたコードは、ほとんど無い。**汎用は、すでに OSS として在る**。
ビルダーは、それを立てる。次章では、その上に **認証(PocketBase)** を
据え、全アプリ共通の門番にする。

---

## 関連記事

- [開発編 第5章: 顧客がAIと協働して開発する時代](/ai-native-ways/software/customer-codev/)
- [親シリーズ第14章: Microsoft 365 を丸ごと置き換える](/ai-native-ways/microsoft-365/)
- [第7章: 業務システムと付き合う ── 並行稼働で書き換える](/ai-native-ways/business-systems/)
