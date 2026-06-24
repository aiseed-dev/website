---
slug: ai
number: "10"
part: "2"
title: 自前の AI を据える ── LLM と RAG
subtitle: 全ての上に AI を乗せる ── 自社データに通じた答えを、自分の側で
description: 自立編の最後に、全ての上に AI を乗せる。2-02で有効化した pgvector が、ここで効く。Ollama や vLLM でオープンモデルを立て、社内文書・コード・メールを pgvector に埋め込んで RAG を組み、Open WebUI で使う。機密と常時処理は自前、難しい判断は Claude に借りる ── 主導権は自分、能力は借りる。Copilot 依存を断ち、汎用は OSS で立てる自立編を締める。
date: 2026.07.16
label: Independence 10
title_html: 全ての上に、<br><span class="accent">自前の AI</span>を乗せる。
prev_slug: fastapi
prev_title: "API を作る ── FastAPI で基幹のロジックを出す"
next_slug: sier-uneconomic
next_title: "SIer委託モデルの構造的不経済"
---

# 自前の AI を据える ── LLM と RAG

自立編の最後に、これまで立てた全ての上に **AI** を乗せる。土台・門番・
文書・コード・メール・会議 ── そこに積まれた自社のデータに通じた AI を、
自分の側に持つ。2-02で有効にした **pgvector** が、ここでようやく効く。

## なぜ自前の AI か

- **データを外に出さない** ── 機密の社内文書を、他社の API に渡さない
- **常時処理が安い** ── 分類・要約・抽出を、追加料金ゼロで回し続けられる
- **自社データに通じる** ── 社内の文書・コード・履歴を踏まえて答える

## モデルを立てる ── Ollama と vLLM

手軽に始めるなら **Ollama**。オープンモデル(Qwen・Llama など)を一行で
立て、API として使える。

```bash
docker run -d -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull qwen2.5    # モデルを取得して即使える
```

処理量が増えたら、スループットの高い **vLLM** に載せ替える。より高い品質が
要る常時処理には、私的デプロイできる **Command A**(2-02で触れた)を選ぶ
こともできる。**まず立てて、必要に応じて差し替える**。

## RAG ── pgvector に効かせる

ここが2-02の回収だ。社内の文書・コード・メールを **埋め込み(ベクトル)**
にして pgvector に入れ、質問に近い断片を引いて、モデルに答えさせる ──
これが **RAG**(検索拡張生成)だ。

```python
# 1) 文書を埋め込み、2-02の pgvector に入れる
emb = embed(text)                       # ローカルの埋め込みモデル
pg.execute("INSERT INTO docs(body, embedding) VALUES (%s, %s)", [text, emb])

# 2) 質問に近い断片を引き、モデルに渡して答えさせる
hits = pg.execute(
  "SELECT body FROM docs ORDER BY embedding <=> %s LIMIT 5", [embed(q)])
answer = llm(f"次の資料に基づいて答えよ:\n{hits}\n\n質問: {q}")
```

2-02で「器だけ用意した」テーブルが、いま中身を得る。**自社の実データに
基づいて、出典つきで答える AI** が、自分の側に立つ。

## チャット UI ── Open WebUI

人が使う窓口は **Open WebUI**。ChatGPT や Copilot に似た画面で、立てた
モデルと RAG につながる。2-03の門番の内側、リバースプロキシの先に置く。

```caddy
ai.example.com { reverse_proxy open-webui:8080 }
```

## どこまで自前にするか ── 正直に

オープンモデルは実用十分まで来た。だが、**最も難しい判断や大規模な
コード生成では、いまも Claude のような最前線モデルが強い**。これは
メールの送信中継(2-06)や Cloudflare(2-08)と同じ構図だ。

- **自前に持つ** ── 機密データの処理、常時の分類・要約・RAG(主導権の本体)
- **借りる** ── 難しい判断、重い生成は、最前線モデルの API に出す

**主導権は自分の側に、能力は必要な分だけ借りる**。全部を自前にすることが
目的ではない ── データと日常処理を手元に置き、難所だけ外に出す。

> 自前の AI の価値は、賢さの最大化ではない。
> **自社データを手放さずに、AI を日常に組み込めること**だ。

## まとめ ── 自立編の終わりに

全ての上に、自前の AI を。

- **Ollama / vLLM** ── オープンモデルを立てる、品質が要れば Command A
- **RAG(pgvector)** ── 2-02の器に社内データを入れ、出典つきで答える
- **Open WebUI** ── ChatGPT 風の窓口、門番の内側に
- **自前と借用の線引き** ── データと常時処理は自前、難所は最前線モデルに借りる

2-02から2-10まで、Microsoft 365 と基幹のベンダー製品を、一つずつ
OSS に置き換えてきた。土台・門番・文書・コード・メール・会議・予約・
Web・AI ── そのどれも、**書いたのではなく、立てた**。

> 2-02の最初に書いたとおり ── **AI の効果より、OSS の効果のほうが
> 大きい**。汎用は、すでに世界で共有されている。

これで「**どう作るか(自立編)**」は終わる。次章からは視点が変わる ──
「**なぜこれが産業構造を変えるのか(転換編)**」。自分で立てられる時代に、
SIer 委託モデルがなぜ構造的に不経済になるのかを問う。

---

## 関連記事

- [2-02: 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [3-01: SIer委託モデルの構造的不経済](/ai-native-ways/software/sier-uneconomic/)
- [2-01: Microsoft と Google から自立する ── 全体像と対応表](/ai-native-ways/software/independence/)
