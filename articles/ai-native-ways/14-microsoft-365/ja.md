---
slug: microsoft-365
number: "14"
title: Microsoft 365 を丸ごと置き換える ── 10の一対一マッピング
subtitle: ビジネスの土台を、ベンダーの檻から自分の手元へ
description: ビジネス用 Microsoft 365 は、認証・文書・共有・メール・ポータル・AI の6層が一社に束ねられた構造だ。束ねられているから、一社の方針で全部が動く。6層を一つずつ、自前のオープンな道具へ置き換える ── Entra ID は PocketBase、Word/Excel/PowerPoint は OnlyOffice、SharePoint+GitHub は Forgejo+Zed、Exchange+Outlook は Postfix+Thunderbird、Power Pages は Cloudflare Pages、Copilot(従量課金)は Command A+(Apache 2.0)。会議は Teams を Jitsi / BigBlueButton、予定は CalDAV + Cal.com。さらにその下の土台 ── Azure SQL は PostgreSQL、C#/.NET/VBA は Python/Ruby + Rust。合計10、各層の構築方法まで一対一で示す。
date: 2026.05.03
label: AI Native 14
title_html: <span class="accent">Microsoft 365</span> を、<br><span class="accent">自前の道具</span>に解く。
prev_slug: one-plus-ai
prev_title: 1人+AIで作る、新しい仕事の単位
next_slug:
next_title:
---

# Microsoft 365 を丸ごと置き換える ── 6つの一対一マッピング

**ビジネス用 Microsoft 365 の本当の正体は「束ねられている」ことだ**。

第6章で事務処理を Office から離し、第7章で業務システムを並行稼働で
書き換えた。この章は、その二つを **会社全体の土台** に広げる ──
認証・文書・共有・メール・ポータル・AI の6層を、一社の契約から
解いて、自分の側に置き直す。

やることは一つだけ。**束を解いて、6本の独立した道具に分ける**。

## 「束ねられている」ことが、ロックインの正体だ

Microsoft 365 が便利なのは、ログイン(Entra ID)が文書(Office)に、
文書が共有(SharePoint)に、共有がメール(Exchange)に、メールが
ポータル(Power Pages)に、そして全部に AI(Copilot)が、**同じ
アカウントで一直線に繋がっている** からだ。

しかしこの「一直線」が、そのままロックインの構造でもある。

- 値上げは **6層まとめて** 効く ── 逃げ場が無い
- データポリシーの変更は **6層まとめて** 効く
- 一社の障害は **6層まとめて** 止まる(序章の単一障害点)
- Copilot の判断基準は **6層すべてに** 浸透する

> 束ねられているから便利で、束ねられているから人質になる。
> **便利さと人質は、同じ一本の鎖の表と裏だ**。

解き方も一つだ。**6層を、6本の独立した道具に分ける**。一本ずつ
置き換えられて、一本が倒れても他は動く ── これが第13章「1人+AI」と
同じ、**自立した N は集中した 1 より強い** の、会社版である。

## 6つの一対一マッピング

束を解くと、各層はこう対応する。**一対一**で、左を右に置き換える。

| Microsoft 365(束) | 自前の置き換え | その層の役割 |
| --- | --- | --- |
| **Entra ID**(ID 基盤) | **PocketBase** | ユーザー認証・OAuth2・権限管理 |
| **Word / Excel / PowerPoint** | **OnlyOffice** | 文書・表計算・スライドの編集 |
| **SharePoint + GitHub** | **Forgejo + Zed** | 共有・版管理 + 手元の編集 |
| **Exchange + Outlook** | **Postfix + Thunderbird** | メールの配送 + 閲覧 |
| **Power Pages** | **Cloudflare Pages** | 業務ポータル・社外向けサイト |
| **Copilot**(従量課金) | **Command A+**(Apache 2.0) | AI ── 完全ローカル・オープンウェイト |

右側の6本は **別々の組織が作った、別々のオープンな道具** だ。
だから、一本の方針変更が他に波及しない。一本を別のものに差し替えても、
残り5本は何も変わらない。**束が解けている** ── これが核心だ。

```mermaid
flowchart TB
  subgraph Bundle["Microsoft 365 ── 1社が6層を束ねる"]
    direction TB
    E1["Entra ID"]
    O1["Word / Excel / PowerPoint"]
    S1["SharePoint + GitHub"]
    X1["Exchange + Outlook"]
    P1["Power Pages"]
    C1["Copilot(従量課金)"]
    E1 --- O1 --- S1 --- X1 --- P1 --- C1
  end

  subgraph Unbundled["自前 ── 6本の独立した道具"]
    direction TB
    E2["PocketBase"]
    O2["OnlyOffice"]
    S2["Forgejo + Zed"]
    X2["Postfix + Thunderbird"]
    P2["Cloudflare Pages"]
    C2["Command A+"]
  end

  Bundle ==>|束を解く = 値上げ・障害・方針が層をまたがなくなる| Unbundled

  classDef bad fill:#fef3e7,stroke:#c89559,color:#5a3f1a
  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  class E1,O1,S1,X1,P1,C1 bad
  class E2,O2,S2,X2,P2,C2 good
```

以下、6本それぞれの **構築方法** を順に示す。すべて、小さな miniPC か
VPS 一台、または手元のマシンで動く。順番に意味はない ── やりやすい
層から始めて、一本ずつ束から外していけばいい。

前提として、置き場所を一つ用意する。**Linux が一台**(Debian/Ubuntu の
VPS、または社内 LAN の miniPC)。ここに Docker を入れておく。

```bash
# Debian/Ubuntu に Docker を入れる(置き場所の土台)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"   # 入れ直してグループ反映
docker compose version            # 動作確認
```

## Entra ID → PocketBase ── 認証を自分の手元に持つ

**Entra ID は「誰がログインできるか」を Microsoft に預ける仕組み**だ。
これを外すと、束の一番上が切れる。

PocketBase は、**一個の実行ファイル**(約 15 MB の Go バイナリ)に
SQLite・認証・管理画面が全部入っている。メール+パスワード認証、
15 種類以上の OAuth2 プロバイダ(Google, GitHub, Microsoft …)、
ユーザーの役割管理、管理ダッシュボード ── ID 基盤に要るものが揃う。

### 構築する

```bash
# バイナリ1個を置いて起動するだけ
mkdir -p ~/pb && cd ~/pb
wget https://github.com/pocketbase/pocketbase/releases/latest/download/pocketbase_linux_amd64.zip
unzip pocketbase_*.zip
./pocketbase serve --http=0.0.0.0:8090
```

起動したら `http://<サーバー>:8090/_/` で管理画面が開く。最初に
管理者を作り、`users` 認証コレクションを開いて、社員アカウントを
登録する。OAuth2 を使うなら、設定画面でプロバイダの Client ID /
Secret を入れれば、Google や GitHub のアカウントでログインできる。

各アプリ(後述の OnlyOffice、社内 Web、ポータル)は、ログインを
この PocketBase に **API で問い合わせる**。`POST /api/collections/
users/auth-with-password` が JWT を返す ── これが社内共通の通行証に
なる。認証ロジックは自分の SQLite の中にあり、Microsoft を経由しない。

> 認証を握っている者が、土台を握っている。
> **その土台を、15 MB のファイル一個で自分の側に戻す**。

## Word / Excel / PowerPoint → OnlyOffice

**Office の本体は「アプリ」ではなく「.docx / .xlsx / .pptx という形式」**だ。
OnlyOffice は、この三形式を **そのまま** 読み書きする ── 互換性が高く、
組織が Office 形式を要求し続けても、出口で困らない(第6章「出口で
変換」の、変換すら要らない版)。

選択肢は二つある。**個人の編集**にはデスクトップ版、**ブラウザでの
共同編集**には Document Server を立てる。

### デスクトップ版(各自のマシン)

```bash
# Debian/Ubuntu
wget https://download.onlyoffice.com/install/desktop/editors/linux/onlyoffice-desktopeditors_amd64.deb
sudo apt install ./onlyoffice-desktopeditors_amd64.deb
```

Windows / macOS は公式サイトのインストーラ、Flatpak なら
`flatpak install flathub org.onlyoffice.desktopeditors`。これで
`.docx` をダブルクリックすれば Word の代わりに開く。

### ブラウザ共同編集(Document Server)

```bash
# 複数人で同じ文書を同時編集する場合
docker run -d --name onlyoffice -p 8081:80 \
  -e JWT_ENABLED=true -e JWT_SECRET=change-me \
  onlyoffice/documentserver
```

`JWT_SECRET` は、先の PocketBase が発行する通行証と組み合わせて、
ログインした社員だけが文書を開ける構成にできる。文書の実体は
Forgejo(次節)か共有ストレージに置き、OnlyOffice はその **編集面**
として動く。**中身は第6章どおり Markdown / SQLite に降ろし、
Office 形式は「人に渡す出口」だけ** ── OnlyOffice はその出口を、
変換なしで担う道具だ。

## SharePoint + GitHub → Forgejo + Zed

**SharePoint は「共有と版管理」、GitHub も「共有と版管理」**。
社内向けと社外向けで二つに分かれていたものを、**Forgejo 一本に
畳む**。Forgejo は Gitea から派生した、軽量なセルフホスト Git
フォージ ── リポジトリ、Issue、Wiki、Pull Request、CI が、
miniPC 一台で動く。文書も表もコードも、すべて Git で版管理する。

編集する手元の道具が **Zed**。高速なエディタで、Markdown も
コードも書け、AI 連携も持つ。SharePoint の「ブラウザで開いて
ロックして編集」の代わりに、**Zed で開いて、Forgejo に push する**。

### Forgejo を構築する

```yaml
# compose.yaml ── Forgejo を miniPC/VPS に立てる
services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:9
    ports: ["3000:3000", "222:22"]
    volumes: ["./forgejo:/data"]
    environment:
      - FORGEJO__server__DOMAIN=git.example.com
    restart: always
```

```bash
docker compose up -d              # 起動
# http://<サーバー>:3000 で初期設定 → 管理者作成
```

ブラウザで開いて管理者を作り、組織(Organization)を一つ作る。
ここが社内の「共有の場」になる。議事録(第3章の Markdown)、
顧客データ(第5章の JSON / SQLite)、業務コード(第2章の Python)
── すべてリポジトリに入れて push すれば、**誰が・いつ・何を
変えたかが全部残る**。SharePoint の「最新版どれ?」問題が消える。

### Zed を入れる

```bash
curl -f https://zed.dev/install.sh | sh   # Linux / macOS
```

Zed で文書フォルダを開き、編集して、`git push`。共同作業は
Forgejo の Pull Request で受ける ── 文章のレビューも、コードの
レビューも、同じ仕組みで回る。

> 社内 SharePoint と社外 GitHub を、**Forgejo 一本に統合する**。
> 共有と版管理は、もともと同じ問題だった。

## Exchange + Outlook → Postfix + Thunderbird

**メールは6層で一番難しい**。ここは正直に書く。

Exchange は「メールサーバー(配送・保管)」、Outlook は「メール
クライアント(閲覧)」。クライアント側の置き換えは簡単だ ──
**Thunderbird** を入れて、IMAP/SMTP のアカウントを設定するだけ。
Outlook の代わりに、今日から使える。

```bash
sudo apt install thunderbird       # Debian/Ubuntu
# Windows/macOS は thunderbird.net のインストーラ
```

難しいのはサーバー側だ。完全なメールサーバーは Postfix(送信 SMTP)
だけでは足りず、実際には **Postfix + Dovecot(受信 IMAP)+
Rspamd(迷惑メール)+ OpenDKIM(署名)** の組み合わせになる。
さらに DNS の **MX / SPF / DKIM / DMARC** を正しく設定しないと、
送ったメールが他社に届かない(迷惑メール扱いされる)。

だから現実的には、これらを一括で立てる **mailcow** か
**Mail-in-a-Box** を使う。

```bash
# mailcow ── Postfix+Dovecot+Rspamd 等を docker で一括起動
git clone https://github.com/mailcow/mailcow-dockerized && cd mailcow-dockerized
./generate_config.sh              # ドメインを聞かれる
docker compose up -d
```

立てたら、DNS にレコードを入れる(管理画面が必要な値を表示する)。

- **MX** → 自分のメールサーバーを指す
- **SPF / DKIM / DMARC** → なりすまし防止・配送率を上げる
- **PTR(逆引き)** → VPS 事業者側で設定(配送率に効く)

設定が済めば、Thunderbird から IMAP/SMTP で繋ぐ。**メールの実体が、
Microsoft のクラウドではなく自分のディスクにある** 状態になる。

> メールは難しい。だが「難しいから預ける」を続けると、
> **通信の中身を一社に握られ続ける**。一度立てれば、あとは動く。

## Power Pages → Cloudflare Pages

**Power Pages は「業務ポータル・社外向けサイトを、ローコードで
作って Microsoft にホストさせる」仕組み**だ。これも、束の一部として
ロックインに数えられる。

置き換えは **Cloudflare Pages**。第8章「HTML+CSS+JavaScript の
原点回帰」で作った静的サイトを、Git push するだけで世界中に配信
する。動的な処理が要れば **Pages Functions**(Workers)で足す。
無料枠が広く、独自ドメインも無料、SSL も自動。

### 構築する

一番簡単な道は、先に立てた Forgejo(または GitHub)のリポジトリを
繋ぐか、`wrangler` で直接デプロイする。

```bash
npm i -D wrangler                 # Cloudflare の CLI
npx wrangler pages deploy ./public --project-name=portal
```

これで `https://portal.pages.dev` に即公開される。独自ドメインは
ダッシュボードで割り当てる。ログインが要る業務ポータルなら、
**認証は先の PocketBase に問い合わせる** ── Pages Functions から
PocketBase の API を叩いて、社員だけが入れる画面にする。

Cloudflare もまた一社ではある。だが Power Pages と違い、
**中身は標準の HTML / JavaScript** だ。気に入らなければ、同じ
ファイルを Netlify でも、自前の Nginx でも、そのまま配れる ──
**ロックインが無い**。これが「ベンダーを使う」と「ベンダーに
握られる」の違いだ。

## Copilot(従量課金)→ Command A+(完全ローカル・Apache 2.0)

最後の層、AI。**Copilot は「6層すべてに同じ AI を、人数×月額で
浸透させる」設計**だ。値上げも、判断基準の画一化も、ここから全層に
広がる(第6章「Copilot ── AI まで人質に取られる構造」)。

これを、**自社のマシンの中だけで動かすオープンウェイトの AI** に
置き換える。本命は **Command A+**(2026年5月公開、Cohere)── 218B の
疎な MoE(実働 25B パラメータ)で、**Hugging Face からウェイトを落とし、
自社のサーバー、あるいは外部非接続(エアギャップ)の社内ネットワークで
丸ごと動かせる**。引用付き出力・推論・画像入力・多言語に対応し、
**H100 が2枚あれば動く**。

**決定的なのは、これが完全にローカルで完結すること**だ。Copilot は
入力を必ず Microsoft のクラウドに通す ── 機密も個人情報も、社外を
経由する。Command A+ は逆だ。**業務データは一歩も社外に出ない**。
従量課金のクラウドもなく、自社の GPU の上で **何回呼んでも追加料金
ゼロ**、ベンダーの料金改定にも API 障害にも左右されない。

それを商用で可能にするのが、ライセンスだ。**Command A+ は Cohere 初の
Apache 2.0 モデル** ── 商用利用が無条件で自由。従来の Command R+ /
Command A は CC-BY-NC(非商用)で、ローカルに置けても **ビジネスでは
使えなかった**。その最後の枷が外れた。**機密データを抱えた会社ほど、
ローカルで動く Command A+ が効く**。

### 構築する

本命(Command A+)は Hugging Face の量子化版を落として vLLM で配信
する。まず軽い Command R で感触を掴むなら Ollama が最短だ。

```bash
# まず軽い Command R(35B)で感触を掴む
curl -fsSL https://ollama.com/install.sh | sh
ollama run command-r

# 本命 Command A+ は量子化版(w4a4 / fp8)を HF から取り、vLLM で配信
pip install vllm
vllm serve CohereLabs/command-a-plus-05-2026-fp8   # H100×2 級
```

社内の常駐 AI として、議事録要約・分類・下書きのような **生成タスク**
は、この OpenAI 互換 API(`/v1/chat/completions`)を直接叩けばいい。
追加料金ゼロで回し続けられる。

```bash
# これは「生成」── 要約。RAG ではない(RAG は後述、別物だ)
curl http://localhost:8000/v1/chat/completions -d '{
  "model": "command-a-plus",
  "messages": [{"role":"user","content":"次の議事録を3点に要約して: ..."}]
}'
```

一点だけ、役割分担を補う。込み入った判断や設計の相談は、引き続き
Claude のような最前線のモデルを「同僚」として使えばいい(第11章)。
要は、**6層に同じ AI を強制連結する Copilot 型をやめ、AI を選べる側に
立つ** ことだ ── 定型は自前の Command A+(他に Llama / Qwen / gpt-oss
など商用可のオープンモデルも選べる)、判断は選んだ同僚、と。Apache
2.0 だから、**選んだ AI を会社の資産として手元に持てる**。

> Copilot は入力を社外(クラウド)に通す設計。
> Apache 2.0 のローカル AI は、**データも判断も社内に閉じる**。
> 選べて、持てて、外に出さない ── **それが自立だ**。

### 性能 ── 素の推論は frontier、RAG では互角以上

正直に比べておく。**Copilot は「モデル」ではなく「製品」**だ ── 中身は
GPT-5.x や Claude といった最前線モデルにルーティングし、Microsoft
Graph で社内データに接続する層である。だから「Copilot のスコア」という
単一の数字は無い。比べられるのは **Command A+ と、Copilot が中で回す
frontier モデル** だ。

その土俵では、**素の推論とコーディングは frontier(= Copilot の中身)が
上**だ。隠す必要はない ── GPQA や難問コーディングのような「頭の中の
知識と推論」を測るベンチでは、GPT-5.x 帯には届かない。

だが、**業務 AI の大半は RAG** だ ── 社内 FAQ、規程・契約・マニュアルの
Q&A、ナレッジ検索。ここは「頭の良さ」ではなく **取ってきた自社文書に
根拠を置いて、引用付きで答える** タスクで、frontier の推論優位はほとんど
効かない。そして Command 系は、**まさに RAG のために設計されている**:

- **ネイティブな span 単位のインライン引用** ── 文ごとに「どの文書の
  どこが根拠か」を返す
- **引用忠実度で GPT-4-turbo を上回る**(Cohere の人手評価)── 関連する
  箇所を、短く根拠付きで引く
- **低ハルシネーション**(grounding 前提の設計)、速度は GPT-4o の
  約 1.75 倍

| | 素の推論・コーディング | RAG(根拠付き Q&A・引用) |
| --- | --- | --- |
| Copilot(GPT-5.x) | 上 | 良いが、データはクラウド経由 |
| ローカル Command A+ | 届かない | **互角以上・引用忠実度は上・完全ローカル** |

しかも RAG の精度を最後に決めるのは、モデルより **取ってくる文書の質
(retrieval)** だ。ここは PocketBase / Forgejo / PostgreSQL に貯めた
自社データと埋め込み検索で、**自分で設計・改善できる** 領域である。

引用付きで返る、ということは **出力を人間が検証できる** ということだ ──
第12章「AIで物語を検証する」で説いた **検証層** そのもの。frontier の
ブラックボックスな回答より、**根拠リンク付きで返るローカル RAG のほうが、
業務としては信頼できる**。

> 素の頭脳では frontier に譲る。
> だが業務の主戦場(RAG)では、**引用付き・低幻覚・完全ローカル**。
> 性能で張り合う必要はない ── **勝てる土俵で、勝つ**。

### ローカル RAG は「検索」を自分で組む

ひとつ、はっきりさせておく。**RAG は API を一回叩いて終わり、ではない**。
`/v1/chat/completions` にプロンプトを投げるのは「生成」であって、RAG では
ない。RAG の質は、生成モデルより **検索(retrieval)** で決まる ── ここを
自分で組む。

完全ローカルの最小構成はこうなる(すべて手元で動く):

- **埋め込み**:`bge-m3`(多言語)を Ollama で(`ollama pull bge-m3`)
- **保管 + 検索**:**pgvector**(= すでに立てた PostgreSQL の拡張)。
  PocketBase 側なら `sqlite-vec`
- **ハイブリッド検索**:意味検索(pgvector)+ キーワード検索(BM25 /
  全文検索)を併用 ── これだけで精度が 20〜30% 上がる
- **再ランク**:`bge-reranker-v2-m3` で上位を並べ替え(さらに 15〜30%)
- **生成(引用付き)**:取ってきた塊を **`documents[]` として渡す**
  grounded generation。Command A+ が `[1] [2]` の span 引用を返す

```sql
-- pgvector: 意味検索(すでにある PostgreSQL に拡張を足すだけ)
CREATE EXTENSION IF NOT EXISTS vector;
SELECT id, body FROM docs ORDER BY embedding <=> :query_vec LIMIT 20;
```

肝心の **引用** は、プロンプトに本文を貼り付けても出ない。Command の
**grounded generation テンプレート**(`documents` を渡す形式)を使う必要
がある ── 自前配信なら `vllm>=0.21` と Cohere の `melody`(`cohere_melody`)
で、引用を正しく解析する。

要は、**Copilot が Microsoft Graph で隠してやっていた「検索 + 接地」を、
自分の側で組む** ということだ。手間は増える。だが retrieval を握ることは、
**精度を握る** ことであり、**データを社外に出さない** ことでもある。

> RAG は「賢いモデルを API で呼ぶ」ことではない。
> **自社データを検索して、根拠ごと答えさせる** ことだ。
> 検索は自分で組む ── そこが業務 AI の本体だ。

## 会議と講座 ── Teams とカレンダーを解く

6層の束には、毎日の共同作業の面がもう一つある ── **会議(Teams)と
予定(カレンダー)**。とくに **講座を開く** なら、ここが要る。受講者を
集め、枠を取らせ、教室で話す ── その3つを自前で揃える。

| Microsoft 365 | 自前の置き換え | その層の役割 |
| --- | --- | --- |
| **Teams**(ビデオ会議) | **Jitsi Meet**(講座は BigBlueButton) | 会議・オンライン講座 |
| **Outlook / Bookings**(予定・予約) | **CalDAV(Radicale)+ Cal.com** | カレンダー + 受講予約 |

### Teams → Jitsi Meet(講座は BigBlueButton)

ふつうの会議は **Jitsi Meet**。docker で一台に立てれば、URL を配るだけで
会議室が開く ── アカウント登録も要らない。

```bash
# Jitsi Meet を docker で自前ホスト
git clone https://github.com/jitsi/docker-jitsi-meet && cd docker-jitsi-meet
cp env.example .env && ./gen-passwords.sh
docker compose up -d        # https://<ドメイン> で会議室が開く
```

**講座**には **BigBlueButton** を使う。これは最初から **オンライン授業の
ために作られた仮想教室** だ ── リアルタイムのホワイトボード、資料共有、
ブレイクアウト(小グループ)、投票、そして **録画**。受講者の体験は本物の
教室に近い。Jitsi より重い(16GB 級のサーバーが要る)が、**講座を本気で
やるなら、こちらが本命**。受講者の情報を第三者に渡さず、自分のサーバーの
中だけで完結する。

### Outlook / Bookings → CalDAV + Cal.com

カレンダーの実体は **CalDAV**。**Radicale**(数 MB の Python、5分で立つ)
を置けば、すでに使っている **Thunderbird** がそのまま予定表になる ──
第4の層で入れた Thunderbird は、メールとカレンダーを兼ねる。

```bash
# Radicale ── 最小の CalDAV サーバー
pip install radicale
python3 -m radicale --storage-filesystem-folder ~/radicale/collections
# Thunderbird に CalDAV を追加: http://<サーバー>:5232/
```

**講座の予約**(受講者が自分で枠を取る)は **Cal.com** ── オープン
ソースの Calendly だ。docker で立て、公開ページを渡せば、受講者が空き枠を
選んで予約する。Microsoft Bookings がやっていたことを、**自分のドメインで、
手数料ゼロで** こなす。

> 講座は、場所を借りずに開ける。
> **教室(BigBlueButton)も、予約表(Cal.com)も、自分の側に持てる**。

## その下の土台 ── Azure SQL と .NET も解く

6層の束の下に、もう一つ Microsoft の土台がある ── **データベース
(Azure SQL)と、業務アプリの実行系(C# / .NET / VBA)**。ここは
第7章「並行稼働で書き換える」で詳しく扱った層だ。ここに土台の
**2行を足せば、Microsoft 依存はほぼ全部が一対一で解ける**。

| Microsoft の土台 | 自前の置き換え | その層の役割 |
| --- | --- | --- |
| **Azure SQL** | **PostgreSQL** | データベース |
| **C# / .NET / VBA** | **Python / Ruby + Rust** | 業務ロジックの実行系 |

### Azure SQL → PostgreSQL

Azure SQL は SQL Server のクラウド版だ。標準 SQL(`SELECT`・`JOIN`・
ウィンドウ関数)はそのまま残し、**ベンダー方言の T-SQL だけ捨てる**
(第7章)。移行は `pgloader` がスキーマもデータも一括で運ぶ。

```bash
# PostgreSQL を立てる
docker run -d --name pg -p 5432:5432 \
  -e POSTGRES_PASSWORD=change-me -v ./pg:/var/lib/postgresql/data postgres:17

# Azure SQL → PostgreSQL を一括移行(スキーマ + データ)
pgloader mssql://user:pass@azure-host/db postgresql://postgres:change-me@localhost/db
```

T-SQL のストアドに埋まった業務ロジックは、Claude が抽出して Python /
Ruby に翻訳する ── **不可視のストアドが、読めるコードに戻る**(第7章)。
あとは第7章どおり、旧 Azure SQL と並行稼働で出力を突き合わせ、差分が
消えたら旧を止める。ライセンスと従量課金が、まるごと消える。

### C# / .NET / VBA → Python / Ruby + Rust

実行系は三層に分けて考える。

- **接着層は Python / Ruby** ── 業務ロジックを書く薄い言語。C# / .NET
  のアプリは Python(FastAPI)や Ruby(Sinatra + 生の SQL)に置き換え、
  Excel / Access の **VBA は Python に外部化** する(第2章・第6章)
- **重い処理と型安全は Rust(下層)** ── 速度と厳密さが要る所は、人間が
  書くのではなく **Rust 製のパッケージに降ろす**(Polars・Pydantic 中核
  など)。型安全は下層の責任、という本シリーズの原則どおり
- **書くのは Claude、実行は手元** ── ベンダーランタイム(.NET CLR)への
  依存が消え、コードが読めて、テストが書ける状態になる

C# の静的型に慣れた人ほど「Python は型が緩い」と心配する。だが要点は
**型安全を人間のコードで担保しない** ことだ ── それは Rust 製の下層
(Polars / Pydantic)に任せ、Python / Ruby は **判断を書く接着剤** に
徹する。これも第7章の **並行稼働** で、旧 .NET と出力を突き合わせ
ながら、一つずつ置き換える。

> 365 の束6つ、会議と予定の2つ、土台の2つ。**合わせて10、すべて一対一**。
> これで Microsoft 依存は、ほぼ残らず解ける。

## 何が変わるか ── コストと自立

自前に解くと、月額の構造が変わる。Microsoft 365 は **人数 × 月額**
(Business Standard で月 1,500〜2,500 円/人、Copilot を足すとさらに
+数千円/人)── 人が増えるほど線形に増える。自前の道具一式は **サーバー
一台分の固定費**(VPS なら月 1,000〜数千円、社内 miniPC なら電気代)
── 人が増えても、ほぼ増えない。

しかし本質はコストではない(第6章と同じだ)。本質は **束が解けて
いる** ことにある。

- 一社が値上げしても、その一層だけ差し替えればいい
- 一社が障害を起こしても、他の5層は動き続ける
- 一社がデータポリシーを変えても、影響はその層に閉じる
- AI の判断基準を、会社が選べる

```mermaid
flowchart LR
  Q["この層を<br>差し替えたい"]
  Bundle["Microsoft 365<br>(束)"]
  Unb["自前<br>(6本)"]
  R1["6層まとめて<br>移行 = 事実上不能"]
  R2["その1本だけ<br>差し替え = 他は無傷"]

  Q --> Bundle ==>|束ねられている| R1
  Q --> Unb ==>|解けている| R2

  classDef bad fill:#fef3e7,stroke:#c89559,color:#5a3f1a
  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  class Bundle,R1 bad
  class Unb,R2 good
```

## どの順で解くか

一気にやらなくていい(第6章と同じ作法だ)。**束から外しやすい順**に、
一本ずつ。

1. **Thunderbird**(クライアントだけ先に)── サーバーは Exchange の
   まま、閲覧を Outlook から移す。リスクゼロで始められる
2. **OnlyOffice デスクトップ** ── 各自の編集を Office から移す
3. **Forgejo + Zed** ── 共有と版管理を SharePoint から移す。
   ここで「最新版どれ?」が消える
4. **Cloudflare Pages** ── 社外サイト・ポータルを移す
5. **Command A+(Apache 2.0 のオープンモデル)** ── 定型 AI 処理を
   Copilot から移す
6. **PocketBase / メールサーバー** ── 認証とメール配送。最後に、
   全アプリの土台として据える

各ステップは、第7章の **並行稼働** で進める。旧(Microsoft)を
止めず、横で新を動かし、同じ仕事が回ることを確かめてから、旧を
解約する。**契約更新の時期に間に合わせる** ── これも第7章どおりだ。

## 運用は、一人 + AI で回る

ここで当然の疑問が出る ── **10 個も自前で抱えて、誰が面倒を見るのか**。
答えは **一人 + AI** だ。第13章「1人+AI」で示した新しい仕事の単位が、
そのまま会社のインフラ運用に効く。

なぜ一人で回るのか。理由は三つ。

- **どれも標準的な、箱に入ったオープンな道具** ── PocketBase は1ファイル、
  ほかは docker compose 一枚。Claude が compose を書き、DNS と DKIM を
  整え、ログを読み、不調を切り分ける。**運用の相棒が AI** だ
- **束が解けているから、障害が連鎖しない** ── M365 なら一社の不調が全部を
  巻き込むが、ここでは Forgejo が落ちてもメールは生き、AI が止まっても
  会議は続く。**一個ずつ、独立に直せる**
- **見える・読める・テストできる** ── 設定もログも自分の手元にある。
  ブラックボックスの Copilot と違い、AI と一緒に **中を読んで直せる**

正直に、重いところも書く。**運用負荷が集中するのは2つ ── メールと
BigBlueButton** だ。メールは配送(DKIM / SPF / 評判)が繊細なので、送信
だけ外部リレーに逃がす手もある。BigBlueButton は重いので、**講座の期間
だけ立てて、終わったら畳む**(クラウドの GPU を時間借りしてもいい)。
残り8つは、立てたらほぼ放っておける。

これは第13章の主旨そのものだ。**縦割りの情報システム部門は要らない**。
業務を分かっている一人が、AI を相棒に、認証からメール、講座、AI、
データベースまでを横断して持つ。**個人の自立が、会社のインフラの
レベルで成立する**。

> 10 個のオープンな道具を、一人 + AI が運用する。
> Microsoft 365 を一社に預けるのと、**手間は変わらない ── 主導権だけが、
> 自分の側に移る**。

## そして、基幹システムへ

ここまで組んだものは、そのまま **基幹システムを書き換える土台** になる。
第7章「業務システムと付き合う」で説いた並行稼働の書き換えは、実は
**立つ場所(プラットフォーム)を前提にしていた** ── その場所が、この章で
全部そろった。

- **新しい基幹システムが動く DB** ── PostgreSQL + pgvector(既出)
- **実行系** ── Python / Ruby + Rust(既出)
- **版管理と CI** ── Forgejo(既出)
- **認証** ── PocketBase が、新システムのログインを一手に引き受ける
- **業務ロジックの抽出** ── レガシーのコード・SQL・手順書を、**ローカルの
  Command A+ + RAG** で読み解いて Markdown に出す。第7章の「業務知識を
  一気に Markdown に出す」を、**ソースを一歩も社外に出さずに** やれる

そもそも、これまで **基幹システムと Microsoft 365 が共有していたのは、
たった二つ ── Entra ID(認証)と SharePoint(文書共有)だけ** だった。
業務システムの世界とオフィスの世界は本来ほとんど別物で、この二つの継ぎ目
だけで繋がっていた。

その二つは、この章で **PocketBase と Forgejo** に置き換え済みだ。つまり
**継ぎ目は、もう自分の側にある**。新しい基幹システムは、オフィス系と同じ
PocketBase で認証し、同じ Forgejo で文書と版を共有する ── Microsoft を
介さずに、二つの世界が再び一点で出会う。

```mermaid
flowchart TB
  Core["基幹システム<br/>Python/Ruby+Rust + PostgreSQL"]
  Office["オフィス系<br/>OnlyOffice / メール / 会議 / 講座"]
  Auth["PocketBase<br/>認証 = 旧 Entra ID の継ぎ目"]
  Share["Forgejo<br/>共有・版管理 = 旧 SharePoint の継ぎ目"]
  Core -->|同じ認証| Auth
  Office -->|同じ認証| Auth
  Core -->|同じ共有| Share
  Office -->|同じ共有| Share

  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  class Core,Office,Auth,Share good
```

二つの継ぎ目は、同じ重さではない。**SharePoint は「置き場所」、Entra ID
は「鍵」だ**。文書の置き場所は後からいくらでも動かせる。だが認証は、両方
の世界のすべてのアプリ・ログイン・権限がぶら下がる一点 ── ここを握られて
いる限り、何を自前にしても **入口は他人のもの** だ。

だから、この章で本当に効く一手は **Entra ID → PocketBase** だ。識別の
継ぎ目を自分の側に移した瞬間、基幹もオフィスも **自分の門番に対して認証
する**。Microsoft が最も深く食い込ませようとするのも、ここ ── **ID 基盤
こそ、束の根** だからだ。ここを押さえれば、残りは時間の問題になる。

だから、SAP や Oracle、20 年もののレガシーを書き換える作業は、**「もう
一つアプリを、同じ土台の上に立てる」だけ** になる。難しかったのは土台の
ほうで、それはもう手元にある。あとは第7章どおり ── 旧を止めず、横で新を
動かし、出力を突き合わせ、差分が消えたら旧を殺す。

> Microsoft 365 を解いて作った土台は、**基幹システムを解く土台でもある**。
> 一度プラットフォームを自分の側に持てば、置き換えは「もう一段」でしかない。

## AI ネイティブの時代には、作り直しが当然になる

最後に、一段引いて見る。Microsoft のシステムを書き換えるのは、**特別な
決断ではない**。AI ネイティブの時代には、**作り直しのほうが当然**になる。

理由は二つが噛み合っている。

**一つ目 ── Microsoft の作りは、構造的に「反 AI ネイティブ」だ**。中身を
Office の書式に閉じ込め(第6章)、Python をクラウドに幽閉し、Copilot を
検証層なしで業務に直結し(第6章)、T-SQL や .NET CLR で逃げ場を塞ぐ。
これらは偶然ではない ── **AI が触れる場所(素のテキスト・開いた形式・
手元実行・読めるコード)から、中身を遠ざける設計**だ。AI を同僚にしよう
とするほど、この壁にぶつかる。

**二つ目 ── 書き換えのコストが、10 分の 1 になった**(第7章)。AI が業務
ロジックを抽出し、Python に翻訳し、テストを書く。数年・数億円のプロジェクト
が、現場の一人 + AI の数ヶ月になった。

古い構造が **AI ネイティブと噛み合わず**、しかも作り直しが **安い** ──
この二つが重なれば、結論は一つだ。**残すほうが不自然**になる。かつて
「動いているものに触るな」が正解だったのは、書き換えが高すぎたからに
すぎない。その前提が消えた今、**作り直さない理由のほうが、説明を要する**。

これは Microsoft への敵意ではない。IT 革命が積み上げたものを、AI 革命が
**作り直して引き継ぐ** ── その自然な一巡だ(序章・第13章)。問われている
のは「やるか」ではなく「いつ、誰が主導でやるか」。**ベンダーに預けたまま
にするか、自分の側で作り直すか** ── それだけだ。

> AI ネイティブの時代に、Microsoft のシステムを作り直すのは、
> 革命ではない。**当然の更新だ**。

## まとめ

ビジネス用 Microsoft 365 は、6層を一社に束ねた構造だ。便利さと
人質は、同じ一本の鎖の表と裏だった。

- **Entra ID → PocketBase**(認証を 15MB のファイル一個に)
- **Word/Excel/PowerPoint → OnlyOffice**(Office 形式をそのまま)
- **SharePoint + GitHub → Forgejo + Zed**(共有と版管理を一本に)
- **Exchange + Outlook → Postfix + Thunderbird**(通信を手元に)
- **Power Pages → Cloudflare Pages**(ロックインの無いホスト)
- **Copilot(従量課金) → Command A+(完全ローカル・Apache 2.0)**(データを社外に出さず AI を持つ)
- **Teams → Jitsi Meet / BigBlueButton**(会議とオンライン講座)
- **Outlook / Bookings → CalDAV(Radicale)+ Cal.com**(予定と受講予約)
- **Azure SQL → PostgreSQL**(その下の土台 ── データベース)
- **C# / .NET / VBA → Python / Ruby + Rust**(その下の土台 ── 実行系)

一対一で、左を右に置き換える。右の10本は別々の組織が作った別々の
オープンな道具だから、**一本の方針変更が他に波及しない**。これは
効率化の話ではない ── 第13章「1人+AI」を、会社の土台の高さで
言い直したものだ。**集中した 1 より、自立した N が強い**。

束を解く。一本ずつ、自分のペースで。解けた分だけ、会社は
ベンダーの人質ではなくなり、**自分たちの判断で動けるようになる**。

---

## 関連記事

- [第6章: 事務処理を変える ── Officeから離れる現実的な道筋](/ai-native-ways/office-replacement/)
- [第7章: 業務システムと付き合う ── 並行稼働で書き換える](/ai-native-ways/business-systems/)
- [第8章: Webを作る ── HTML+CSS+JavaScriptという原点回帰](/ai-native-ways/web/)
- [第13章: 1人+AIで作る、新しい仕事の単位](/ai-native-ways/one-plus-ai/)
- [構造分析08: 企業ITの税を引く](/insights/enterprise-tax/)
- [それでも Windows と Office を使い続けますか?](/blog/windows-office-facts/)
