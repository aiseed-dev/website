---
slug: ai
number: "11"
part: "2"
title: 自前の AI を据える ── LLM と RAG
subtitle: 全ての上に AI を乗せる ── 自社データに通じた答えを、自分の側で
description: 自立編の最後に、全ての上に AI を乗せる。2-02で有効化した pgvector が、ここで効く。まず Cohere のオープンウェイト・コーディングモデル North Mini Code を Ollama で手元に置き(データを外に出さない)、RAG 用に汎用モデルと埋め込みを並べる。社内文書・コード・メールを pgvector に埋め込んで RAG を組み、Open WebUI で使う。機密と常時処理は自前、難しい判断は Claude に借りる ── 主導権は自分、能力は借りる。Copilot 依存を断ち、汎用は OSS で立てる自立編を締める。
date: 2026.07.16
label: Independence 10
title_html: 全ての上に、<br><span class="accent">自前の AI</span>を乗せる。
prev_slug: structure-knowledge
prev_title: "社内情報を整える ── 整備こそ本体、AI は最後の一手"
next_slug: two-worlds
next_title: "企業は自分でコードを書かない ── 事務と基幹、二つの世界の並立"
---

# 自前の AI を据える ── LLM と RAG

自立編の最後に、これまで立てた全ての上に **AI** を乗せる。土台・門番・
文書・コード・メール・会議 ── そこに積まれた自社のデータに通じた AI を、
自分の側に持つ。2-02で有効にした **pgvector** が、ここでようやく効く。

## なぜ自前の AI か

- **データを外に出さない** ── 機密の社内文書を、他社の API に渡さない
- **常時処理が安い** ── 分類・要約・抽出を、追加料金ゼロで回し続けられる
- **自社データに通じる** ── 社内の文書・コード・履歴を踏まえて答える

## モデルを立てる ── North Mini Code を Ollama で

手軽に始めるなら **Ollama**。オープンウェイトのモデルを一行で立て、API
として使える。

最初に入れるのは **North Mini Code**(Cohere)── **オープンウェイト
(Apache 2.0)の、エージェント型コーディングモデル**だ。「ビルダーが AI に
コードを書かせる」という、本シリーズの中心の道具にあたる。30B の MoE で
アクティブは 3B と軽く、ローカル機でも低遅延で動く。

```bash
docker run -d -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull north-mini-code    # オープンウェイト、手元で動く
```

試すだけなら OpenRouter の無料枠で叩けるが、**本番は自前で動かし、コードも
データも外に出さない**。Cohere は、欧州の Aleph Alpha と並ぶ **ソブリン
AI** の一角だ(→ [ブログ 027](/blog/autonomy-distribution-diversity/))。

RAG やチャットには、これとは別に **汎用モデル(Qwen など)と埋め込み
モデル**を、同じ Ollama に並べて乗せる。処理量が増えたら、スループットの
高い **vLLM** に載せ替え、より高い品質が要る常時処理には、私的デプロイ
できる **Command A**(Cohere、2-02で触れた)を選ぶこともできる。**まず
立てて、必要に応じて差し替える**。

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

そして、自前に持てる範囲は、ハードの進化とともに広がる。AMD の **Ryzen
AI Max PRO 400** シリーズ(2026 年 Q3、ASUS・HP・Lenovo から)は、最大
192GB の統合メモリ(うち最大 160GB を VRAM に)を積み、**x86 クライアント
で初めて 300B 級のモデルをローカルで動かせる**。これが載った PC が手元に
来れば、**社内文書管理を主目的に、Command A+**(Cohere、私的デプロイ可、
出典つきの RAG)を、丸ごと自前で回せる。いま「借りる」しかない重い文書
RAG も、手元に降りてくる ── **借りる側の線は、年々後退していく**。

> 自前の AI の価値は、賢さの最大化ではない。
> **自社データを手放さずに、AI を日常に組み込めること**だ。

## まとめ ── 自立編の終わりに

全ての上に、自前の AI を。

- **Ollama / vLLM** ── North Mini Code(Cohere、オープンウェイトの
  コーディングモデル)から始め、RAG 用に汎用モデルを併置、品質が要れば Command A
- **RAG(pgvector)** ── 2-02の器に社内データを入れ、出典つきで答える
- **Open WebUI** ── ChatGPT 風の窓口、門番の内側に
- **自前と借用の線引き** ── データと常時処理は自前、難所は最前線モデルに借りる

2-02から2-11まで、Microsoft 365 と基幹のベンダー製品を、一つずつ
OSS に置き換えてきた。土台・門番・文書・コード・メール・会議・予約・
Web・情報の整備・AI ── そのどれも、**書いたのではなく、立てた**。

> 2-02の最初に書いたとおり ── **AI の効果より、OSS の効果のほうが
> 大きい**。汎用は、すでに世界で共有されている。

これで「**どう作るか(自立編)**」は終わる。次章からは視点が変わる ──
「**なぜこれが産業構造を変えるのか(転換編)**」。自分で立てられる時代に、
SIer 委託モデルがなぜ構造的に不経済になるのかを問う。

---

## 関連記事

- [2-02: 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars](/ai-native-ways/software/foundation/)
- [3-03: SIer委託モデルの構造的不経済](/ai-native-ways/software/sier-uneconomic/)
- [2-01: Microsoft と Google から自立する ── 全体像と対応表](/ai-native-ways/software/independence/)
