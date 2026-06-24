---
slug: foundation
number: "02"
part: "2"
title: 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars
subtitle: すべてが乗るデータ基盤を、最初に自分の側に立てる
description: 導入編の最初は、すべてが乗るデータ基盤。普通は SQLite で十分 ── サーバ不要の単一ファイルだ。共有して複数人で書くときだけ PostgreSQL に上げる。pgvector で意味検索、DuckDB と Polars で列指向分析 ── Excel は人の入出力に残し、その裏のデータは機械が捌く。Power BI を大差で抜く。汎用は OSS で共有されている ── 書くのではなく、立てる。
date: 2026.07.01
label: Independence 2
title_html: まず<span class="accent">データ基盤</span>を、<br>自分の手元に立てる。
prev_slug: independence
prev_title: "Microsoft と Google から自立する ── 全体像と対応表"
next_slug: auth
next_title: "門番を立てる ── PocketBase で認証を一つに"
---

# 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars

**ビルダーの仕事は、コードを書くことから始まらない。実績ある OSS を
立てることから始まる**(導入編 第5章)。汎用的な機能は、もう世界で
共有されている ── だから「書く」のではなく「立てる」。

全体像と対応表(第1章)に続いて、この自立編では、Microsoft 365 と
Google Workspace、そして基幹のベンダー製品を置き換える OSS を、一つずつ
実際に立てていく。最初に据えるのは **データ基盤**だ。分析も、AI の
RAG も、講座の予約も、基幹システムも ── **データは、すべてこの上に乗る**。
だから最初に据える。そして、**普通は SQLite で十分だ** ── 重い倉庫から
始めなくていい。

## なぜ土台(データ)から始めるのか

順番には理由がある。後の章で立てるものの多くが、データベースに依存する:

- **分析**(DuckDB)は、ここのテーブルと Parquet を読む
- **AI の RAG**(Command A+)は、`pgvector` で類似検索する
- **講座の予約**(Cal.com)や **基幹システム**は、ここに読み書きする

土台が先にあれば、上に立つものは「すでにある DB に乗せる」だけになる。
**先に据えるほど、後が軽い**。

そして、その土台は最初から重くしなくていい。

> **普通は SQLite で十分だ。共有して複数人で書くときだけ、PostgreSQL に上げる**。

一人で、一つのアプリで、たいていの用途なら ── まず SQLite から始める。
据える順番もこれに従う。

## 単一ファイルで持つ ── SQLite

データベースの既定は **SQLite** だ。サーバを立てず、**一つのファイル**に
収まる。Python に最初から入っていて、追加のインストールも要らない。世界で
最も多く使われているデータベースで ── スマホにもブラウザにも入っている。

```bash
# ライブラリも不要 ── 標準で入っている
sqlite3 app.db 'CREATE TABLE memo(id integer primary key, body text)'
```

一人で持つ設定も、端末の手元の小さなデータも、これで足りる。次章で立てる
**門番(PocketBase)も、この SQLite の上で動く**。**一つのアプリが手元で
持つだけなら、まず SQLite**。標準 SQL なので、Claude がそのまま書く。

足りなくなるのは、**共有して複数人が同時に書く**ときだ。そのときだけ、
倉庫を一段上げる。

## 共有・複数人で書くなら PostgreSQL

複数のアプリや人が同時に読み書きする共有の倉庫が要るなら、**PostgreSQL**
に上げる。オープンソース、無料、商用可。Oracle や SQL Server と同等以上の
機能を持ち、Claude が最も得意とする方言だ(導入編 第5章・第1章)。
SQLite と同じ標準 SQL だから、上げても書き方は変わらない。**手帳(SQLite)
から倉庫(PostgreSQL)へ、用途で持ち替える**。

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
Claude が抽出して Python / Ruby に翻訳する(導入編 第5章)。あとは旧 DB と
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

### Excel データを扱う ── Polars

Excel は、人が数字を入れ、人が結果を読む **入出力の道具**だ。その役割は
変わらない ── だから次章では Excel 互換の **OnlyOffice** を自分の側に立てる。
変わるのは、**その裏でデータを捌く側**だ。

手元に積み上がった `.xlsx` は、**Polars** がそのまま読む。Rust 製の高速
データフレームで、Excel が固まる行数でも瞬時に処理し、結果を Excel・
PostgreSQL・Parquet のどれにでも書き戻す。

```python
import polars as pl
df  = pl.read_excel("売上_2025.xlsx")                # 人が作った Excel を読む
agg = df.group_by("部門").agg(pl.col("売上").sum())  # 重い集計は一行
agg.write_excel("部門集計.xlsx")                      # 人が読む Excel に書き戻す
```

人は Excel で入れて読み、機械は Polars と DuckDB で捌く。**人の道具と機械の
道具を、役割で分ける**。SQL で書きたい処理は DuckDB、データフレームで
捏ねたい処理は Polars ── 同じデータを、好きな道具で触れる。

巨大データを常時集計するなら、列指向 DB サーバーの **ClickHouse** に
載せ替える。だが大半の社内分析は、DuckDB と Polars で足りる。

## まとめ

データ基盤を、最初に自分の側へ。

- **SQLite** ── 既定。サーバ不要の単一ファイル、Python に同梱。一人・一アプリ・たいていの用途はこれで十分(門番もこの上)
- **PostgreSQL**(+ pgvector)── 共有して複数人で書くときだけ上げる、予約・基幹・RAG が乗る倉庫
- **pgvector** ── 意味検索の土台(RAG は AI の章で)
- **pgloader** ── Azure SQL からの一括移行、方言だけ捨てる
- **DuckDB / Polars** ── 列指向分析と高速データフレーム。Excel は人の入出力に残し、重い集計は機械側で ── Power BI を大差で抜く

書いたコードは、ほとんど無い。**汎用は、すでに OSS として在る**。
ビルダーは、それを立てる。次章では、その上に **認証(PocketBase)** を
据え、アプリ共通の門番にする。

---

## 関連記事

- [導入編 第5章: 顧客がAIと協働して開発する時代](/ai-native-ways/software/customer-codev/)
- [第1章: Microsoft と Google から自立する ── 全体像と対応表](/ai-native-ways/software/independence/)
- [親シリーズ第7章: 業務システムと付き合う ── 並行稼働で書き換える](/ai-native-ways/business-systems/)
