# WordPressへのサイバー攻撃対策設計書 - 攻撃が増加するので至急

## 現状

WordPressは全ウェブサイトの約4割(2026年時点で41.9〜43%)を占め、攻撃者にとって一つの脆弱性が数千万サイトに効く標的である。新規に発見された脆弱性は2024年の7,966件から2025年は11,334件へ、前年比42%増えた(Patchstack)。その91〜96%はプラグイン由来であり、2025年上半期に発見された脆弱性の57.6%が認証不要(Unauthenticated)——訪問者が誰でもそのまま悪用できるものだった。46%はパッチが提供される前に公開されている。攻撃は自動化されており、放置されたフォームとログイン画面は、サイトの規模に関係なく無差別に叩かれる。

そして攻撃は今後さらに増える。最新の大規模AIモデルに加え、DeepSeekやQwenなど中国のオープンモデルが普及した。性能はフロンティアモデルに迫り、価格はAPIで一桁安いか、手元で動かせば無料である。これらは攻撃への協力を拒否するガードレールが弱く、オープンウェイトのため制限なしに脆弱性の探索と攻撃コードの自動生成に使える。AIを悪用した攻撃活動は前年比89%増(CrowdStrike、2026年)。脆弱性の公開から悪用までの時間(Time to Exploit)は、かつての年単位から数時間〜数十分単位へ短縮された。技能のない攻撃者もAIを道具として使えるため、これまで費用対効果が合わず狙われなかった中小のサイトが、AIボットによる無差別スキャンで自動的に捕捉されるようになった。パッチの適用速度でAIの自動攻撃に追いつくことは、統計的に不可能になりつつある。守り続ける対策は、この増加と永久に追いかけっこになる。

問い合わせフォームが狙われるのは、その背後に顧客データ(名前、メールアドレス、問い合わせ内容)が溜まっているからである。本書はそのデータをWordPressから分離(デカップリング)して自分のPCに引き取り、攻撃対象領域(アタックサーフェス)を最小化する手順である。侵入されても、そこに失うデータがない状態を作る。

## 本書の内容

WordPressの問い合わせフォームのデータを、Cloudflare Worker + D1の受信箱に一時的に受け、ローカルPCから取りに行って引き取る(プル型)。コードはこの仕様書からClaudeが実装する。

システムは三つの場所からなる。

```
[Webサイト]                    [Cloudflare]              [ローカルPC]
素のHTMLフォーム               Worker + D1               取得 → SQLite → 人が確認
  + Turnstile → 直POST  ───→  POST /submit で一時保存 ←── GET /items / POST /ack
                              (Turnstile検証)
```

## 方針: フォームの分離

問い合わせデータの置き場所をWordPressから分離(デカップリング)し、ローカルPCに移す。WordPressに残るのはフォームの入力画面だけで、データは溜まらない。

WordPressに加える変更は、問い合わせフォームを素のHTMLフォーム(Turnstileウィジェット付き)に差し替え、送信先をWorkerの /submit に直接向けるだけである。CF7やCF7 to Webhookのようなフォーム系プラグインは使わない——むしろ外す。テーマ・PHPには触れず、カスタムHTMLブロックにフォームを一つ置く。

フォーム系プラグインを外すのは、それ自体が攻撃対象を増やすからである。データ転送に使われるCF7 to Webhookには、2026年6月に認証不要で悪用可能なSSRF脆弱性が公表された(CVE-2026-11395、CVSS 7.2、5.0.0以前が影響)。プラグインを入れれば脆弱性が付いてくる——例外はない。守るために穴を足す愚を避け、フォームは素のHTML、恒久的に使うもの(Worker、ローカルの管理アプリ、データ)はすべてWordPressの外に置く。

書き込みの門は、WordPress内に置く共有トークンではなく、送信ごとのTurnstileトークンをWorkerがサーバー側で検証(siteverify)することで担う。破られる箱の中に長期の鍵を置かないため、WordPressが侵入されても /submit を開ける鍵は漏れない。

この構成は、将来サイトを静的HTMLに作り直しても変わらない。フォームは既に素のHTML + Turnstile + 直POSTであり、Worker・ローカル側もそのまま。静的化のとき捨てるのはフォームを載せていたページの器だけで、フォームもデータの引き取りも一日も途切れない。

そしてその作り直しも、同じ方法でできる。既存ページの静的HTML化とCloudflare Pagesへの公開は、仕様を書いてClaudeに実装させれば数時間の作業である。かつては制作会社に発注する案件だった。PHPもMySQLも動かない静的サイトになれば、WordPressの脆弱性は根元から消える。本書はその手前の、今日できる一歩である。

## 1. Cloudflare(Worker + D1)

### アカウント登録(初めての場合)

1. https://dash.cloudflare.com/sign-up でアカウントを作成する。必要なのはメールアドレスとパスワードのみ。無料で、クレジットカードの登録も不要
2. 届いた確認メールのリンクを開いて有効化する
3. WorkerとD1は無料プランに含まれ、問い合わせフォームの受付程度の量なら無料枠で足りる。サイトのDNSをCloudflareに移す必要はない(この用途ではアカウントだけでよい)

### worker.js 仕様(Cloudflare上で動く受付プログラム)

素のfetchハンドラ一枚。フレームワーク・npmパッケージ不使用。

#### D1スキーマ(テーブル inbox)

| 列 | 型 | 内容 |
|---|---|---|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | |
| created_at | TEXT NOT NULL DEFAULT (datetime('now')) | 受付時刻 |
| name / email / body | TEXT NOT NULL | 抽出した値 |
| payload | TEXT NOT NULL | 受信JSON全文(cf-turnstile-response を除く、20000字まで)。フィールド名の取りこぼし保険 |
| ip | TEXT | 訪問者IP |

#### POST /submit — フォームからの受付

フォームはブラウザから直接POSTする(クロスオリジン)。人間かどうかの検証はWorkerがTurnstileのsiteverifyで行う。検証の順に:

0. **CORS**: メソッドがOPTIONSならプリフライトに204+CORSヘッダ(Access-Control-Allow-Origin: ALLOWED_ORIGIN、Allow-Methods: POST/OPTIONS、Allow-Headers: Content-Type)で応答。POST以外は405
1. **Origin検証**: Origin ヘッダーが環境変数 ALLOWED_ORIGIN と一致すること。違反は403(※Originは非ブラウザでは偽装可能な弱い多層防御。本当の門は次のTurnstile検証)
2. **サイズ検証**: JSON全体が20000字を超えるなら400
3. **Turnstile検証**: 本文の cf-turnstile-response を、Secret TURNSTILE_SECRET・接続元IP(CF-Connecting-IP)と共に `challenges.cloudflare.com/turnstile/v0/siteverify` へPOSTし、`success:true` を要求。違反は403。トークンは1回限り・約5分で失効し、siteverifyがサーバー側で一度だけ消費するのでリプレイは塞がる
4. **抽出**: payload から cf-turnstile-response を除いたものを保存対象とする。name/email/body を代表キー(your-name, name, お名前 / your-email, email / your-message, message, 本文 等)から最初に見つかった値で採る。上限: name 100字、email 254字、body 5000字。三つとも空なら400。訪問者IPは接続元(CF-Connecting-IP)で採る
5. **レート制限**: 同一訪問者IP(CF-Connecting-IP)の直近10分の行数をinbox自体から数え、3件以上なら429。直接POSTになったことで接続元IPが本物の訪問者ごとに分かれるため、このキーが正しく効く。訪問者IPが取れない投稿は制限せず通す(止めて失うより、通して人が確認する側に倒す)
6. INSERTして200(Access-Control-Allow-Origin ヘッダ付き)。INSERTがD1の容量上限超過(Exceeded maximum DB size)で失敗したときは507を返す(受信箱が満杯=ローカルの引き取りが滞っているサイン。下記参照)

ブラウザは直POSTなので、これらの結果(200 / 4xx / 5xx)をそのまま受け取る。フォームは成功時のみ「送信しました」を表示し、失敗時は**入力値を保持したまま**再送を促す。CF7 to Webhook経由の旧構成では、Worker側で弾いても訪問者には送信成功と表示され問い合わせが黙って消えたが、直POSTではその取りこぼしが起きない。

#### GET /items — ローカルPCの取得

Authorization: Bearer <PULL_TOKEN> を検証(違反401)。クエリ `?after=<id>&limit=<n>`(after省略時は0、limit省略時は500・上限500)で、id が after より大きい行を **id昇順で最大limit件** 返す。全行を一度に返さないのは、受信箱が膨れてもWorkerのメモリとD1のクエリ応答上限に収まる範囲で確実に取り出すため。ローカルは、返り件数がlimit未満になるまで after を最後のidへ進めて繰り返し呼び、全件を引き取る。削除しない。

#### POST /ack — 人の確認後の削除

同じBearer検証。ボディ {"ids": [整数...]} の行をDELETEし、削除件数を返す。ids検証(非空・全て整数)違反は400。**削除経路はここのみ。自動削除・期限切れ削除を実装しない**

D1の無料枠はデータベース1つあたり500MBが上限で、超えると新規のINSERTが「Exceeded maximum DB size」で拒否される(/submit は507を返す)。ただし**上限に達しても読み取りとDELETEは実行でき**、DELETEで空けば書き込みは再開する。つまり満杯は行き詰まりではなく「引き取りが滞っているサイン」である——/items はページングで必ず全件引き取れ、/ack はidさえあれば満杯でも削除できるので、満杯からは常に回復できる。加えて、削除は人の確認=/ackで起きるため、**管理アプリの「未確認」件数がそのまま受信箱の残件数**にあたる。ここを日々ゼロに近づけて空けておけば満杯には至らない(問い合わせ本文は1件が数KB、500MBは数十万件に相当し、Turnstileとレート制限で自動投稿も抑えられるため、長期に放置しない限り実際に満杯になることはまずない)。管理アプリでの定期的な確認と削除は、業務のためだけでなく、受信箱を空け続けるための運用でもある。

### 自社サーバーで受ける場合(代替構成)

受信箱は自社サーバーにも置ける。違いは次の通り。

- Cloudflareで受ける(Worker + D1): 受け口が自社サーバーの外にあり、24時間の受付をCloudflareに任せる。ローカルPCは外向き接続のみで、固定IP・開放ポート・常時稼働のいずれも不要(普通の回線のNAT裏で成立する)
- 自社サーバーで受ける: 受信箱が自社の機械にあり、Cloudflareにデータを置かない。部品が減る(Worker・D1・deploy.pyが消える)。サーバーは固定IP・開放ポート(443番)で立ち、その前に**CDN(Cloudflareプロキシ)を置くのが原則**。DNSをCloudflareに置いてプロキシを有効にするだけで、DoS攻撃はエッジで吸収され、サーバーのIPは公開DNSに出ない。例外として、固定IPがない環境でもCloudflare Tunnel(cloudflared、サーバーから外向きに接続)経由なら受けられる
- 自社サーバー受けの残る条件は稼働時間のみ。夜間に止める運用も選べる。その場合はフォームに受付時間を書いておく(例: 受付時間 9:00〜18:00)。24時間受けたいならWorker + D1構成を選ぶ

自社サーバーで受ける場合、仕様の変更は次の通りで、それ以外(エンドポイント、検証の順、削除の規則)はすべて同一。

- worker.js の代わりに **FastAPI** で同じ三エンドポイントを実装する(Python、raw SQL)。D1の代わりに**SQLite**
- **deploy.py は不要**。構成は CDN(Cloudflareプロキシ)→ Caddy(自動TLS)→ FastAPI(systemd起動)。トークン類は環境変数
- Turnstile検証はWorker構成と同じ(siteverify)。訪問者IPはCF-Connecting-IPヘッダーで採る。ブラウザ直POSTを受けるためCORSも同じく必要

## 2. ローカルPC

作るものは三つで、役割が違う。三つともコードはClaudeが書く。人が書くのはこの仕様書だけで、これが従来との一番の違いである——プロのエンジニアが1日以上かけていたものが、10分でできる。コードの後の設定作業(デプロイ、トークンの設置、WordPressの設定)も、詰まったらその場でClaudeに聞けば手順を教えてくれる。

- **worker.js** — Cloudflare上で動く受付プログラム本体(仕様は「1. Cloudflare」)
- **deploy.py** — worker.jsをCloudflareに設置するための道具。手元で一回実行する
- **管理アプリ(admin.py)** — 取り込み・確認・削除を行うFletデスクトップアプリ。日常はこれだけを使う

### Python環境の準備

1. Python 3をインストールする。手順は公式ドキュメント「Pythonのセットアップと利用」(https://docs.python.org/ja/3/using/index.html)の自分のOSの章に従う。それで分からなければ、自分のOSと状況を添えてClaudeに聞く
2. 作業フォルダを作り、その中に仮想環境を作って有効化する:

```sh
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
```

3. 仮想環境の中でFletをインストールする: `pip install flet`

以降のこの節の作業は、すべてこの仮想環境の中で行う。

### Claudeにコードを書かせる

1. この仕様書の全文をClaudeに渡し、「この仕様書の通りに実装して」と依頼する
2. 生成されたコードを仕様と照合して確認する。worker.jsは: /submitの検証の順、エンドポイントが三つだけであること、自動削除が書かれていないこと。deploy.pyは: 外部パッケージを使っていないこと、処理の順。管理アプリは: 削除の引き金が確認操作のみであること
3. 確認できたら同じフォルダに保存する

コードを書くのはClaude、仕様と照合して確認するのは人。以降の修正も同じ流れで行う(仕様書を直し、Claudeに再実装させ、照合する)。

モデルはOpusで十分である。Fableのような長時間の自律実行に向くモデルは要らない。それが要るのは仕様が曖昧で、AIが探索しながら道を作る場合であり、本書は仕様が確定していて部品も小さい。設計が書き切れていれば、実装に必要な能力は小さくて済む。

### deploy.py 仕様(設置の道具、手元で一回実行)

Python標準ライブラリのみ(urllib.request, json, secrets, pathlib)。wranglerの代わりにCloudflare REST API(api.cloudflare.com/client/v4)を直接呼ぶ。外部ツール・外部パッケージに依存しない。

- 入力: 環境変数 CF_API_TOKEN(権限: Workers Scripts:Edit, D1:Edit)、CF_ACCOUNT_ID、TURNSTILE_SECRET(Turnstileのsecret key)、ALLOWED_ORIGIN(フォームを置くサイトのオリジン、例 https://example.com)
- 処理の順:
  1. D1データベース collection-point を作成。同名が既存ならそのuuidを使う
  2. スキーマ適用(/d1/database/{uuid}/query)
  3. worker.jsをモジュール形式でアップロードする(PUT /accounts/{account_id}/workers/scripts/{script_name})。リクエストは `multipart/form-data`。**スクリプト本体は文字列フィールドではなくファイルパートとして送り、そのパートのContent-Typeに `application/javascript+module` を指定する**(これを外すと「main module name is not present in bundle」等で拒否される)。metadataパート(JSON)には `main_module` にファイル名、compatibility_date、バインディング(D1: name=DB、plain_text: ALLOWED_ORIGIN)を記述する
  4. secrets.token_urlsafe(32)でPULL_TOKENを生成しSecretに設定。入力のTURNSTILE_SECRETもSecretに設定
  5. workers.devのURLを有効化
- 出力: Worker URL、/submit のURL、PULL_TOKEN(再表示不可の旨を添える)
- 再実行可能であること: D1は再利用、Workerは上書き更新。worker.js修正の反映も同じコマンド

PyPIパッケージ cf-publish　(pip install cf-publish)にdeploy.py機能追加する予定。deploy.pyを作成しなくても、こちらを使うこともできる。

### 管理アプリ(admin.py)の仕様

Python + Fletのデスクトップアプリ。PULL_TOKENとWorker URLは環境変数から読む。

#### ローカルSQLiteスキーマ(テーブル contact、ファイル data/inbox.db)

| 列 | 型 | 内容 |
|---|---|---|
| remote_id | INTEGER NOT NULL UNIQUE | Worker側のid。重複取得を弾く |
| pulled_at | TEXT NOT NULL DEFAULT (datetime('now')) | 取得時刻 |
| created_at | TEXT NOT NULL | Worker側の受付時刻 |
| name / email / body / payload | TEXT NOT NULL | 取得した値 |
| confirmed | INTEGER NOT NULL DEFAULT 0 | 人が確認済み=1 |
| handled | INTEGER NOT NULL DEFAULT 0 | 返信等の対応済み=1 |

#### 機能

- **取得**: /items を**ページングで**取得する。after=(ローカルにある最大remote_id)から始め、返り件数が上限未満になるまで after を最後のidへ進めて全件を引き取り、`INSERT OR IGNORE` で保存(remote_idのUNIQUE制約で重複無視)。起動時と「取得」ボタンで実行。受信箱からの削除はしない
- **一覧**: 未確認 / 確認済み / 対応済み のフィルタ表示
- **確認操作**: 人が内容を読んだ行に対して実行。confirmed=1 にし、そのremote_idを /ack へ送って受信箱から削除する。**削除の引き金はこの操作のみ**
- **対応済み操作**: 返信等を終えた行に handled=1
- **バックアップ**: 日次でinbox.dbを日付名でコピー(shutil)。直近30日分を保持

#### 実装の注意

- Riverpod/provider等の状態管理ライブラリは使わない。小さな自己完結型Widgetで構成し、SQLiteを直接読み書きする(sqlite3標準ライブラリ、raw SQL)
- **Flet版はFletの最新版を使う**: Fletは1.0に向けて大規模な破壊的変更を重ねている。0.21.0で内部アーキテクチャを非同期(FastAPI + Uvicorn)ベースへ移行し、UserControlを廃止(既存コントロールを直接継承し`__init__()`で`super().__init__()`を呼ぶ形が標準に)。さらに0.80以降の1.0系では: `ft.app(target=main)` → `ft.run(main)`、FilePicker等がサービス化され`page.services`への登録が必須に、ダイアログは`page.open()` → `page.show_dialog()`、`ft.alignment.center` → `ft.Alignment.CENTER`、ボタンの`text` → `content`など、基本APIの名前が広く変わった。宣言的UI(ControlBuilder)も導入された。AIの学習データはこれらの変更前のコードが大半であり、記憶で書くと実行時エラーになる。実装前に必ずインストールされているバージョンを確認し、最新の公式ドキュメントに照らして書く。学習データの記憶でFletコードを書かない

### 構築

1. Cloudflare Turnstileでウィジェットを作成し、site key(公開・HTMLに埋める)とsecret key(非公開・Workerに置く)を取得する。ドメインに自サイトを設定する
2. CloudflareのAPIトークンを作成(ダッシュボード → プロフィール → APIトークン。権限: Workers Scripts:Edit、D1:Edit)
3. 仮想環境の中で実行: `CF_API_TOKEN=... CF_ACCOUNT_ID=... TURNSTILE_SECRET=... ALLOWED_ORIGIN=https://example.com python3 deploy.py`
4. 出力されたPULL_TOKENとWorker URLを管理アプリの環境変数に控える。Worker URLとsite keyは「3. Webサイト」のフォーム設定で使う

### 確認(次に進む前に)

```sh
curl https://<worker>/items -H "Authorization: Bearer <PULL_TOKEN>"
```

`{"items":[]}` が返れば、Worker・D1・PULL_TOKENの三つがすべて動いている。401なら貼ったトークンが違う。

```sh
curl -X POST https://<worker>/submit \
  -H "Origin: https://example.com" -H "Content-Type: application/json" \
  -d '{"your-name":"テスト","your-message":"テスト送信"}'
```

Turnstileトークンが無いので403(Turnstile検証で弾かれる)が返れば、siteverifyが効いている証拠。**正常系(200)は有効なTurnstileトークンが要るため、ブラウザからの実送信でしか確認できない**。実フォームからの送信確認は「全体の確認」で行う。

## 3. Webサイト(WordPress)

管理画面のみの作業。Worker URLとsite keyは「2. ローカルPC」の構築で得たもの。

1. 問い合わせページのフォームを、カスタムHTMLブロックの素のHTMLフォームに差し替える(雛形は下)。`data-sitekey` にsite key、`fetch` の宛先に `https://<worker>/submit` を入れる
2. **CF7 to Webhookは使わない**(入れない。入っていれば外す)。CF7も、このフォームには不要
3. 「Simple Cloudflare Turnstile」等のプラグインは、wp-loginのボット対策に使うなら残す(このフォームは自前のTurnstileウィジェットを持つので、フォーム連携としては不要)
4. 稼働中のフォームなので、新フォームを別ページ等で通し確認してから旧フォームと差し替える(リードの入口を落とさない)

素のHTMLフォーム雛形(カスタムHTMLブロックに貼る。`0xここにsite_key` と `<worker>` を置き換える):

```html
<form id="contact-form">
  <input type="text"  name="your-name"    placeholder="お名前" required>
  <input type="email" name="your-email"   placeholder="メールアドレス" required>
  <textarea          name="your-message" placeholder="お問い合わせ内容" required></textarea>
  <div class="cf-turnstile" data-sitekey="0xここにsite_key"></div>
  <button type="submit">送信</button>
  <p id="contact-status" aria-live="polite"></p>
</form>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<script>
(function () {
  const form = document.getElementById('contact-form');
  const status = document.getElementById('contact-status');
  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const data = {};
    new FormData(form).forEach((v, k) => { data[k] = v; }); // cf-turnstile-response も自動で含まれる
    if (!data['cf-turnstile-response']) { status.textContent = '確認を完了してください。'; return; }
    status.textContent = '送信中...';
    try {
      const res = await fetch('https://<worker>/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      status.textContent = res.ok
        ? '送信しました。ありがとうございました。'
        : '送信に失敗しました。時間をおいて再度お試しください。';
      if (res.ok) form.reset();
    } catch (_) {
      status.textContent = '通信エラーが発生しました。';
    } finally {
      if (window.turnstile) window.turnstile.reset(); // トークンは使い捨て。毎回リセット
    }
  });
})();
</script>
```

Turnstileウィジェットが隠しフィールド `cf-turnstile-response` をフォームに自動注入するので、`FormData` がそのまま拾う。

## 全体の確認

1. サイトの問い合わせフォームから実際にテスト送信する
2. 管理アプリを起動(または「取得」ボタン)し、テスト送信が一覧に表示されることを見る
3. 内容を読み、確認操作を行う
4. `curl https://<worker>/items ...` で受信箱から消えていることを見る

ここまで通れば、問い合わせはフォームから自分の机の上まで流れ、削除は人が確認してする。構築は完了である。

これが最初の一歩である。問い合わせを引き取ったのと同じ形——仕様書を書き、Claudeが実装し、人が確認することで、注文、顧客台帳、在庫と、業務のデータを一つずつ自分の手元に移していける。
WordPressの公開Webサーバーも、Claudeが静的サイトに変換してくれる。修正もClaudeに頼めばプログラムを作ってくれる。静的サイトになれば、Claouflare Pagesで、無料で運用できる。データの処理が必要な部分だけを今回のようにすればいい。