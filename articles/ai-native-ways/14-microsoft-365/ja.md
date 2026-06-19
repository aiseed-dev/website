---
slug: microsoft-365
number: "14"
title: Microsoft 365 を丸ごと置き換える ── 8つの一対一マッピング
subtitle: ビジネスの土台を、ベンダーの檻から自分の手元へ
description: ビジネス用 Microsoft 365 は、認証・文書・共有・メール・ポータル・AI の6層が一社に束ねられた構造だ。束ねられているから、一社の方針で全部が動く。6層を一つずつ、自前のオープンな道具へ置き換える ── Entra ID は PocketBase、Word/Excel/PowerPoint は OnlyOffice、SharePoint+GitHub は Forgejo+Zed、Exchange+Outlook は Postfix+Thunderbird、Power Pages は Cloudflare Pages、Copilot(従量課金)は Command R+(無料)。さらにその下の土台 ── Azure SQL は PostgreSQL、C#/.NET/VBA は Python/Ruby + Rust。合計8つ、各層の構築方法まで一対一で示す。
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
| **Copilot**(従量課金) | **Command R+**(無料) | AI ── 自前・オープンウェイト |

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
    C2["Command R+"]
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

## Copilot(従量課金)→ Command R+(無料)

最後の層、AI。**Copilot は「6層すべてに同じ AI を、人数×月額で
浸透させる」設計**だ。値上げも、判断基準の画一化も、ここから全層に
広がる(第6章「Copilot ── AI まで人質に取られる構造」)。

これを、**自前で動かすオープンウェイトの AI** に置き換える。
Command R+ は Cohere が公開した 104B のオープンウェイトモデルで、
**Hugging Face からダウンロードして自分のマシンで動かせる**。
RAG とツール利用に強く、日本語を含む多言語に対応する。従量課金の
クラウドではなく、**自分の GPU の上で、何回呼んでも追加料金ゼロ**。

### 構築する(Ollama が最短)

```bash
# Ollama を入れて、Command R(軽い 35B 版)から試す
curl -fsSL https://ollama.com/install.sh | sh
ollama run command-r              # 35B ── まず動かす
ollama run command-r-plus         # 104B ── GPU メモリに余裕があれば
```

`command-r`(35B)は量子化すれば 24GB 級の GPU 一枚で動く。
`command-r-plus`(104B)は本格的な GPU(複数枚 or 大容量)が要る。
社内の常駐 AI として、議事録要約・FAQ 応答・分類など **量の多い
定型処理** を、追加料金ゼロで回し続けられるのが効く。

API として叩く形(各アプリから呼ぶ)はこうなる。

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "command-r",
  "prompt": "次の議事録を3点に要約して: ..."
}'
```

二点、正直に書く。**第一に、ライセンス**。Command R+ の公開ウェイトは
CC-BY-NC-4.0(非商用)だ。社内検証や非商用には自由に使えるが、
商用利用には Cohere のライセンスが要る ── 商用前提なら、同じ手順で
**Llama / Mistral / Qwen / gpt-oss** など商用可のオープンウェイトに
差し替えられる(Ollama なら `ollama run` のモデル名を変えるだけ)。
**第二に、役割分担**。込み入った判断や設計の相談は、引き続き Claude
のような最前線のモデルを「同僚」として使えばいい(第11章)。要は、
**6層に同じ AI を強制連結する Copilot 型をやめ、AI を選べる側に
立つ** ことだ ── 定型は自前のオープンモデル、判断は選んだ同僚、と。

> Copilot は「AI を選べなくする」設計。
> オープンウェイトは「AI を選べる」状態。**選べることが自立だ**。

## その下の土台 ── Azure SQL と .NET も解く

6層の束の下に、もう一つ Microsoft の土台がある ── **データベース
(Azure SQL)と、業務アプリの実行系(C# / .NET / VBA)**。ここは
第7章「並行稼働で書き換える」で詳しく扱った層だ。365 の6行に、この
**2行を足すと、Microsoft 依存はほぼ全部、一対一で解ける**。

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

> 365 の束6つに、土台の2つ。**合わせて8つ、すべて一対一**。
> これで Microsoft 依存は、ほぼ残らず解ける。

## 何が変わるか ── コストと自立

6本に解くと、月額の構造が変わる。Microsoft 365 は **人数 × 月額**
(Business Standard で月 1,500〜2,500 円/人、Copilot を足すとさらに
+数千円/人)── 人が増えるほど線形に増える。自前の6本は **サーバー
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
5. **Command R+(または商用可オープンモデル)** ── 定型 AI 処理を
   Copilot から移す
6. **PocketBase / メールサーバー** ── 認証とメール配送。最後に、
   全アプリの土台として据える

各ステップは、第7章の **並行稼働** で進める。旧(Microsoft)を
止めず、横で新を動かし、同じ仕事が回ることを確かめてから、旧を
解約する。**契約更新の時期に間に合わせる** ── これも第7章どおりだ。

## まとめ

ビジネス用 Microsoft 365 は、6層を一社に束ねた構造だ。便利さと
人質は、同じ一本の鎖の表と裏だった。

- **Entra ID → PocketBase**(認証を 15MB のファイル一個に)
- **Word/Excel/PowerPoint → OnlyOffice**(Office 形式をそのまま)
- **SharePoint + GitHub → Forgejo + Zed**(共有と版管理を一本に)
- **Exchange + Outlook → Postfix + Thunderbird**(通信を手元に)
- **Power Pages → Cloudflare Pages**(ロックインの無いホスト)
- **Copilot(従量課金) → Command R+(無料)**(AI を選べる側へ)
- **Azure SQL → PostgreSQL**(その下の土台 ── データベース)
- **C# / .NET / VBA → Python / Ruby + Rust**(その下の土台 ── 実行系)

一対一で、左を右に置き換える。右の8本は別々の組織が作った別々の
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
