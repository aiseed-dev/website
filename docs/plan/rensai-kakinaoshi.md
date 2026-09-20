# 連載の書き直し(2026-09-20)

「AI ネイティブな仕事の作法 ── ソフトウェア開発編」を、サブ連載ではなく
独立した連載として一から書き直す。発注者の指示。

- 元の指示: officework の `docs/sekkei/rensai-shusei-matome.ja.adoc`(6 項目)
- 元の文書: 同 `docs/sekkei/ai-kakumei-shita-kara.ja.adoc`、
  `docs/articles/ai-ni-makaseru-server.ja.adoc`
- 2026-09-20 に発注者から追加で渡された事情: ONLYOFFICE が日本語で使い物に
  ならないので officework(aiseed office)を作っている。さらに Claude Docs が
  出た。

## 置き場

| | |
|---|---|
| ファイル | `articles/ai-native-software.adoc` |
| URL | `/ai-native-software/`、英語は `/en/ai-native-software/` |
| 表示名 | AI ネイティブなソフトウェア開発 |
| 表紙 | 記事カードの 1 番目(項目 1) |

元の `articles/ai-native-ways-software.adoc` は消さずに残す。site.json から
外すかどうかは発注者が決める。

## 章立て(25 章)

### 導入編 ── なぜ変わるのか

| 番号 | 記事ID | 題 |
|---|---|---|
| 1-01 | 01-coder-top | AI は、世界で最も難しいコーディング問題を解く |
| 1-02 | 02-maintenance-shift | 保守フェーズの構造変化こそ本質 |
| 1-03 | 03-coder-end | ソフトウェアエンジニアの仕事を AI がするようになる |
| 1-04 | 04-builder | ビルダーという役割 |
| 1-05 | 05-customer-codev | 顧客が AI と協働して開発する時代 |

### 自立編 ── AI に読ませて実行できる仕様書(項目 3)

| 番号 | 記事ID | 題 | 備考 |
|---|---|---|---|
| 2-01 | 06-independence | Microsoft と Google から自立する ── 全体像と対応表 | |
| 2-02 | 07-ai-pc | AI に PC を一台渡す | **新**(項目 2) |
| 2-03 | 08-foundation | 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars | |
| 2-04 | 09-auth | 門番を立てる ── PocketBase で認証を一つに | |
| 2-05 | 10-code | コードを手元に ── Forgejo と Zed | |
| 2-06 | 11-documents | 文書を取り戻す ── 原稿は adoc、様式は aiseed office | **全面書き直し**(項目 5) |
| 2-07 | 12-mail | メールを自分の側に ── Stalwart と Thunderbird | |
| 2-08 | 13-meetings | 会議と予約を自分の側に ── Jitsi と Cal.com | |
| 2-09 | 14-web | Web を公開する ── Cloudflare Pages | |
| 2-10 | 15-fastapi | API を作る ── FastAPI で基幹のロジックを出す | |
| 2-11 | 16-knowledge | 社内情報を整える ── 整備こそ本体、AI は最後の一手 | |
| 2-12 | 17-own-ai | 自前の AI を据える ── LLM と RAG | |

### 転換編 ── なぜ産業構造が変わるのか

| 番号 | 記事ID | 題 | 備考 |
|---|---|---|---|
| 3-01 | 18-two-worlds | 企業は自分でコードを書かない ── 事務と基幹、二つの世界の並立 | |
| 3-02 | 19-sovereignty | デジタル主権 ── Microsoft 問題と Trump 問題 | |
| 3-03 | 20-sier-uneconomic | SIer 委託モデルの構造的不経済 | |
| 3-04 | 21-lockin | ロックイン問題 | |
| 3-05 | 22-hiring-builders | 各社がビルダーを雇用する時代 | |
| 3-06 | 23-japan-transition | 日本の SIer 業界の転換と雇用流動性 | |
| 3-07 | 24-revolution-from-below | AI 革命は下から起きる | **新**(項目 4) |
| 3-08 | 25-five-years | もう戻らない構造転換 | |

## 6 項目の割り当て

1. 表紙で 1 番目 → `html/index.html` の記事カード。道具(aiseed office)と
   入口の頁は、サイトにまだ無いので今回は置かない。
2. 「AI の PC」の章 → 2-02。Debian を土台にして Windows は箱の中、も含める。
3. 自立編の各章を仕様書に → 2-01〜2-12 の全章に三つの節を足す(下の型)。
4. 「AI 革命は下から」→ 3-07。18 の主張を発注者の一人称でその順に。
5. 「文書を取り戻す」→ 2-06 を全面書き直し。
6. 書き方 → 下の決め。

## 自立編の三点セット(項目 3)

各章の「まとめ」の前に、この三つをこの順で置く。見出しは全章で同じにする。

```
== 確かめ方
（「これができていれば済み」を番号付きで。ログインできる、メールが届く、
  会議に入れる、のように、人が見て分かる形で書く）

== 人が持つ物
*人が渡す値*（ドメイン、鍵、パスワードなど）
*AI が「やる前に言う」操作*（DNS を替える、メールを送る、外のデータを消す）

== 確かめた版と日付
（手順を書いたときの道具の版と日付。版が上がっていたら AI に公式の手順を
  確かめさせてから進める、と書く）
```

英語は `== How to check you are done` / `== What the human holds` /
`== Versions checked, and when`。

狙いは、AI のいるサーバーで「2-04 を読んで、そのとおりにやって」と言えば
動く形にすること。

## 書き方(項目 6)

- 普通の言葉。1 文に 1 つ。
- 比喩と造語を使わない。太字を並べない。格言にしない。
- 根拠の無い文を足さない。発注者の言葉と、確かめられる証拠だけ。
- 数字は日付付き。
- どちらの側かを言わない中立の書き方をしない。
- 日本語は である調。英語は平叙。日英で節の数と順番を揃える。

## 2-06「文書を取り戻す」で変えること

元の章は OnlyOffice Docs を立てることを結論にしていた。これを変える。

- ONLYOFFICE は日本語の様式で使い物にならない。だから aiseed office
  (`aiseed-dev/officework`)を作っている。版は 0.1.0-alpha。官公庁の様式を
  Word と突き合わせて直し続けている。
- Claude Docs が 2026-09-16 にベータで出た(2026-09-20 確認)。文書の下書き
  から共同編集・共有までが Claude の中で完結する。**有料プランなら、もう
  使える。**
  - 対象は Pro・Max・Team・Enterprise のベータ。Free は対象外
  - CMEK(顧客管理の暗号鍵)・ZDR(ゼロデータ保持)・HIPAA 対応構成を使う
    組織では、まだ使えない
  - 中身は、書式のある本文・表・複数のタブ。コメントが語句に付き、
    スレッドになる。@claude で直しを頼める。編集権のある人が同時に編集する
  - 既定は非公開。共有はヘッダーの Share から範囲を選ぶ
  - 共有リンクを開くには Claude のアカウントが要る。Team と Enterprise の
    文書は、まだ組織の外へ共有できない
  - 書き出しは Word・PDF・Markdown・Google Docs
  - 実体は claude.ai の artifact。**外から取りに行けない。** Web で取得する
    ことはできず、読めるのは Claude の道具からだけ。持ち出せるのは書き出した
    写しである
  - 同時に Claude Cowork がチャットに統合され、Claude Slides も出た
- Claude Docs と aiseed office は、競合ではなく役割が違う。Claude Docs は
  **原稿を作って回す場所**。日本語の様式(docx の頁割り、行の位置、列幅)を
  Word と一致させることは目的にしていない。**様式の仕事は aiseed office**。
- 連載の主張から見ると、Claude Docs は Microsoft 365 と同じ形をしている。
  便利で、全部つながっていて、鍵は他人の手元にある。違うのは、出口
  (Markdown への書き出し)がはっきりあることだ。だから「通過させる」道具
  として使える。
- 答えは原稿の持ち方にある。**原稿は adoc の文字で持つ。git に入れるのは
  原稿だけで、デザイン(テンプレート)は入れない。** そうすれば、
  aiseed office も Claude Docs も Word も「通過させる」道具になる。
- adoc 形式でのデータ交換が、これから重要になる。
- aiseed office は **もう使える**。エンジンは 0.5.0 が PyPI に出ている
  (2026-09-04 公開、2026-09-20 確認)。β を外した版で、関数 404 個、
  Word の文書が書いてあるとおりに刷れる。役所の PDF と行末のずれを比べた
  数字が RELEASE に載っている。配っているのはエンジンだけで、アプリはまだ。
  AsciiDoc の読み書きはまだ配っていない。

## 事実の扱い

この環境は外向きの通信が絞られていて、公式の頁の大半に到達できない。
確認できた物だけを、日付を付けて書く。

| 事実 | 確認 |
|---|---|
| Claude Pro 月 20 ドル、Max 月 100 ドルから | 2026-09-20、検索で確認 |
| Claude Docs は 2026-09-16 にベータ公開。Pro・Max・Team・Enterprise で使える。Free は対象外 | 2026-09-20、公式ヘルプの記載を検索で確認。Axios・VentureBeat・国内記事も一致 |
| Claude Docs は CMEK・ZDR・HIPAA 構成の組織では使えない | 2026-09-20、公式ヘルプの記載を検索で確認 |
| 書き出しは Word・PDF・Markdown・Google Docs。共有リンクは Claude のアカウントが要る。Team と Enterprise は組織の外へ共有できない | 2026-09-20、検索で確認 |
| Debian 13(trixie)が安定版 | 既存連載「Claudeと一緒に学ぶDebian」で発注者が実機で確認 |
| ウクライナの FPV ドローン、2024 年に年 200 万機超、2025 年は 300 万機の見込み | 2026-09-20、Kyiv Independent ほかで確認 |
| Delta は 2016 年に志願者団体 Aerorozvidka が始め、2023 年に国防省へ移り、2024 年 8 月に正式採用 | 2026-09-20、検索で確認 |

Windows Server の課金の形と Windows 10/11 のライセンス条項は、公式の頁に
到達できず確認できなかった。だから記事には書かない。
