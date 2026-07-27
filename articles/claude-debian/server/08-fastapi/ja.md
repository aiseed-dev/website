---
slug: claude-debian-server-08-fastapi
number: "08"
title: 第8章 自作アプリを動かす
subtitle: ディレクトリ構成、Python、FastAPI
description: コンテナを使わないこの本では、アプリは「ふつうのディレクトリ + venv + systemd」で動かす。だからこそ、どこに何を置くかという規約が、コンテナの代わりに秩序を作る。ディレクトリ構成を決め、PythonとFastAPIで最小のAPIを建て、systemdのサービスにして、第7章のデータベースの上で動かす——コードはClaudeに書かせ、あなたは構成を決めて動かして守る。
date: 2026.06.10
label: Claude × Debian サーバー編 08
prev_slug: claude-debian-server-07-database
prev_title: 第7章 データベースという土台
next_slug: claude-debian-server-09-publishing
next_title: 第9章 外の世界に公開する
cta_label: Claudeと学ぶ
cta_title: アプリは、ふつうのディレクトリで動く。
cta_text: コンテナを使わなくても、自作アプリは動く。ふつうのディレクトリ、venv、systemdのサービス——この三つだけで、自分のサーバーの上に自分のアプリが立つ。コードはClaudeが書く。あなたは構成を決め、動かし、守る。
cta_btn1_text: 第9章へ進む
cta_btn1_link: /claude-debian/server/09-publishing/
cta_btn2_text: 第7章に戻る
cta_btn2_link: /claude-debian/server/07-database/
---

## なぜ自作アプリの章か

第6章で「サービスという単位」が手に入り、第7章で「データという土台」が据わった。動かす型と、載せるデータ。ここまで来れば、もう自分のアプリを建てられる。

この本は、最後までコンテナを使わない。Docker も Kubernetes も出てこない。**アプリは「ふつうのディレクトリ + venv + systemd」で動かす**——これがこの本の一貫した方針だ。なぜか。コンテナは便利だが、その下で何が起きているかを覆い隠す。この本が目指すのは、覆いを外して、自分の手で直せる範囲を広げることだ。だからアプリも、ディレクトリにコードを置き、Pythonの仮想環境を作り、第6章のsystemdで動かす——それだけで、ちゃんと動く。

ただし、コンテナを使わないということは、コンテナが代わりにやってくれていた「整理」を、自分でやるということでもある。どこにコードを置き、どこに秘密を置き、何をgitで管理し、何をバックアップするか。**コンテナの代わりに秩序を作るのは、ディレクトリ構成の規約だ。** この章は、まずその規約を決めることから始める。

そしてもう一つ。**2026年、アプリのコードはClaudeが書く。** あなたが一行ずつタイプするのではない。本編[第15章「Claudeとの開発」](/claude-debian/15-claude-development/)で身につけた開発の作法——仕様を言葉にし、書かせ、レビューし、動かして直す——を、今度はサーバーの上で実践する。コードを書くのはClaudeの仕事で、**構成を決め、動かして守るのが、あなたの仕事**だ。

## 第一節 ディレクトリ構成を決める

コンテナが無い分、置き場所の規約がすべての土台になる。ここでは本書の規約を一例として示すが、これは絶対ではない——意味を理解したうえで、自分流に変えてよい。

アプリの家を `/srv/myapp/` に置く。`/srv` は「このマシンが提供するサービスのデータ」を置くための、Debianが昔から用意している場所だ。中身はこう分ける。

```
/srv/myapp/
├── app/        コード本体（git管理）
├── .venv/      Pythonの仮想環境（使い捨て・git外）
├── .env        接続情報などの秘密（chmod 600・git外）
└── data/       アプリが書くファイルがあれば（任意）
```

四つの役割をはっきり分ける。**`app/` はコード**で、gitで管理する。**`.venv/` は仮想環境**で、次節で作るが、これは「いつでも作り直せる使い捨て」だからgitには入れない。**`.env` は秘密**——データベースのパスワードなどが入るので `chmod 600` で本人しか読めなくし、これもgitには絶対に入れない。**`data/` はアプリが書くファイル置き場**だが、これは必要な場合だけだ。

データの本体は、第7章で据えたPostgreSQL（または SQLite）に入る。`data/` を作るのは、アップロードされた画像のような「ファイルそのもの」を置く必要があるときだけで、構造を持ったデータはデータベースに任せる。

ログも自前で作らない。**ログは journald に任せる。** 第6章で `journalctl -u myapp` を覚えたが、systemdのサービスとして動かす限り、アプリが標準出力に吐いた行は自動でジャーナルに集まる。自分でログファイルを作って肥大化を心配するより、systemdに任せるほうが筋がいい。

そして、アプリは**専用のシステムユーザー**で動かす。第5章で叩き込んだ「必要最小限の権限」の実践だ。アプリが乗っ取られても、そのユーザーにできることしかできない。

```bash
# myapp という専用ユーザーを作る（ログインさせない・/srv/myapp を家とする）
sudo adduser --system --group --home /srv/myapp myapp
```

`--system` はログイン用でないシステムユーザー、`--group` は同名のグループも作る、`--home` は家のディレクトリだ。第7章で作ったデータベースのロール名 `myapp` と、ここで作るOSユーザー名 `myapp` を揃えておくと、後で頭がこんがらがらない。

作ったら、家全体の所有権を渡し、よそからは覗けないようにしておく。

```bash
# /srv/myapp 以下を myapp のものにする
sudo chown -R myapp:myapp /srv/myapp

# 家の中は本人と同グループだけが入れるようにする
sudo chmod 750 /srv/myapp
```

コンテナを使う流儀では、この「誰が何に触れるか」をコンテナの壁が引き受けていた。コンテナを使わない本書では、**Linuxの所有権とパーミッションがその壁になる。** アプリは `myapp` ユーザーの権限しか持たず、`/srv/myapp` の外には書き込めない。壁の素材が違うだけで、やっていることは同じ「隔離」だ。この壁は第三節で、systemdの砂場機能を使ってもう一段厚くする。

ここで、この章でいちばん効く一枚の表を作る。何を、どこに置き、gitで管理するか、そしてバックアップ対象か。

| 何を | どこに | git管理 | 復旧の方法 |
|---|---|---|---|
| コード | `/srv/myapp/app/` | する | gitから戻す |
| 仮想環境 | `/srv/myapp/.venv/` | しない | 作り直す（次節の手順） |
| 秘密（接続情報） | `/srv/myapp/.env` | しない | **バックアップ（第10章）** |
| アプリが書くファイル | `/srv/myapp/data/` | しない | バックアップ（第10章） |
| データ本体 | PostgreSQL `myappdb` | しない | DBダンプ（第7章 `pg_dump`） |

この表を眺めると、第10章のバックアップ思想がディレクトリ構成にそのまま現れていることが見えてくる。**コードはgitで戻せる。venvは作り直せる。戻せないのは `.env` とデータだけだ。** だからバックアップで本当に守るべきは、その二つに絞られる。構成をこう分けておくと、「何を守ればいいのか」が構成図そのものから読める。逆に言えば、すべてを一つのディレクトリにごちゃ混ぜにすると、この区別が消えてしまう。

### Claudeに聞いてみよう①：自分のアプリの構成とテーブルを設計させる

> 私はDebian 13サーバーで、次のアプリを自作したいです：
> 〔例：自分用の家計簿API、家族で使うメモ共有、小さな在庫管理……など、作りたいものを具体的に〕
>
> このアプリを、コンテナを使わず「`/srv/アプリ名/` の下に app/（コード）・.venv/・.env・data/ を分ける」という規約に沿って配置する構成を提案してください。あわせて、このアプリが必要とするデータを入れる PostgreSQL 17 のテーブルを、第7章の流儀で設計してください（`CREATE TABLE` 文と、各カラムの型を選んだ理由つきで）。「git管理するもの・作り直せるもの・バックアップすべきもの」の対応表も付けてください。

作りたいものを最初に言葉にして、構成とテーブルを一度に設計させる。ここで構成の地図ができていれば、この先の節がすべて「その地図を埋める作業」に変わる。

## 第二節 PythonとFastAPI

構成が決まった。中身を建てる。Webアプリのフレームワークは数あるが、ここでは **FastAPI** を使う。理由は三つ。**少ないコードでWeb APIになる**こと。**ドキュメント（`/docs`）が自動で生える**こと。そして**Claudeが最も書き慣れているフレームワークの一つ**だということだ。この本の方針は「コードはClaudeに書かせる」だから、Claudeが得意なものを選ぶのは理にかなっている。

### なぜvenvが必須か——PEP 668

まず、ここで一つ関門がある。Debian 13 のシステムPythonは「externally managed（外部管理）」とマークされていて、`pip install` を直接叩くと**拒否される**。

```
error: externally-managed-environment
```

これはバグではない。**OSが動かすためのPythonと、あなたのアプリのためのPythonを、混ぜないための設計**だ（PEP 668という取り決めで決まっている）。システムのPythonに勝手にパッケージを足すと、Debian自身が使っているPythonの土台が壊れかねない。だから、アプリ専用のPythonの箱——**仮想環境（venv）**——を別に作る。これは第一節で「使い捨て・作り直せる」と位置づけたものだ。

```bash
# venv を作るためのパッケージを入れる
sudo apt install python3-venv

# /srv/myapp の中に .venv を作る（myapp ユーザーとして）
cd /srv/myapp
sudo -u myapp python3 -m venv .venv

# その .venv の中に FastAPI と PostgreSQL ドライバを入れる
sudo -u myapp .venv/bin/pip install "fastapi[standard]" "psycopg[binary]"
```

`.venv/bin/pip` という、`.venv` の中のpipを名指しで叩くのがポイントだ。これなら `externally-managed` に弾かれない。システムのPythonには一切触らず、`/srv/myapp/.venv/` の中だけにパッケージが入る。Debian 13 で入るPythonは **3.13** だ。`fastapi[standard]` はFastAPI本体と開発に必要な一式、`psycopg[binary]` は第7章のPostgreSQLに繋ぐためのドライバだ。

### 最小のFastAPIアプリ

`app/main.py` を一つ、丸ごと載せる。メモを保存・一覧するだけの最小APIで、第7章で作った `myappdb` に psycopg で繋ぐ。

```python
# /srv/myapp/app/main.py
import os
import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

# 接続情報は .env から環境変数で受け取る（コードに秘密を書かない）
DB = os.environ["DATABASE_URL"]

app = FastAPI()


class Note(BaseModel):
    body: str


@app.on_event("startup")
def init_db():
    # 起動時にテーブルが無ければ作る
    with psycopg.connect(DB) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id SERIAL PRIMARY KEY, body TEXT NOT NULL, "
            "created TIMESTAMP DEFAULT now())"
        )


@app.get("/notes")
def list_notes():
    # 全件を新しい順で返す
    with psycopg.connect(DB) as conn:
        rows = conn.execute(
            "SELECT id, body, created FROM notes ORDER BY id DESC"
        ).fetchall()
    return [{"id": r[0], "body": r[1], "created": r[2]} for r in rows]


@app.post("/notes")
def add_note(note: Note):
    # 一件追加して、付いたidを返す
    with psycopg.connect(DB) as conn:
        row = conn.execute(
            "INSERT INTO notes (body) VALUES (%s) RETURNING id",
            (note.body,),
        ).fetchone()
    return {"id": row[0], "body": note.body}
```

40行ほどだ。これは**読んで理解するための見本**であって、丸暗記するものではない。秘密（接続情報）はコードに書かず `os.environ` から受け取る、`%s` でSQLに値を渡す（文字列連結ではなく、こうすると不正な入力を防げる）、`pydantic` の `Note` で入力の形を決める——この三つだけ目で追えれば十分だ。自分のアプリは、この見本を出発点にClaudeに書かせてよい。

接続情報を `.env` に書く。ここが第一節で `chmod 600` にした秘密のファイルだ。

```bash
# /srv/myapp/.env （myapp だけが読める秘密ファイル）
sudo -u myapp tee /srv/myapp/.env > /dev/null <<'EOF'
DATABASE_URL=postgresql://myapp:あなたのパスワード@localhost/myappdb
EOF
sudo chmod 600 /srv/myapp/.env
```

### 起動と確認

開発中の動作確認は、`.venv` の中の uvicorn（FastAPIを動かすサーバー）を名指しで叩く。

```bash
cd /srv/myapp
# .env を読み込んでから、127.0.0.1:8000 で起動する
sudo -u myapp bash -c 'set -a; . .env; .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000'
```

別の端末から、ブラウザを使わずに `curl` で叩いて確かめる。

```bash
# 一件追加する
curl -X POST http://127.0.0.1:8000/notes -H "Content-Type: application/json" -d '{"body":"最初のメモ"}'

# 一覧を取る
curl http://127.0.0.1:8000/notes
```

FastAPIの嬉しいところは、`/docs` に**自動のドキュメント**が生えることだ。`GET /notes` も `POST /notes` も、説明と試せるフォーム付きで一覧される。ただしサーバーには画面が無いので、手元のブラウザから見るにはSSHのポート転送という小技を使う。

```bash
# 手元のPCから：サーバーの8000番を、手元の8000番に繋ぐ
ssh -L 8000:127.0.0.1:8000 あなたのサーバー
# これを張ったまま、手元のブラウザで http://127.0.0.1:8000/docs を開く
```

ここで `--host 127.0.0.1` にした意味を、第5章の言葉で確かめておく。**127.0.0.1 にバインドする**とは、「同じマシンの中からしか繋げない」という意味だ。アプリは外の世界には一切耳を開いていない。第7章でPostgreSQLが `127.0.0.1:5432` に閉じていたのと同じ、安全側の構えだ。外に出す経路は、第9章のリバースプロキシ一本に限る——攻撃面を、自分の手で最小に保つ。

### Claudeに聞いてみよう②：見本を自分の用途のAPIに作り替えさせる

> 次の `main.py` を出発点に、〔自分の用途。例：家計簿（日付・品目・金額を記録して月別合計も返す）／在庫管理／読書記録〕のAPIに作り替えてください。FastAPIとpsycopgで、PostgreSQL 17の `myappdb` に繋ぐ前提です。
> ```
> 〔上の main.py をそのまま貼る〕
> ```
> 作り替えたコードを示したうえで、追加・変更した各部分が何をしているかを説明してください。秘密（接続情報）はコードに書かず .env から読む形を保ってください。

見本をそのまま渡して「これを土台に作り替えて」と頼むのがコツだ。ゼロから書かせるより、動く形を起点にしたほうが、構成も流儀もブレない。返ってきたコードは、第6章のunit fileと同じく、各部分の意味を一度は説明させて読む。

## 第三節 systemdサービスにする

uvicornを手で起動するのは、確認のためだけだ。端末を閉じれば止まってしまう。**第6章で学んだ「サービスにする型」を、そのまま当てる。** 落ちても自動で復活し、サーバーを再起動しても勝手に立ち上がる、本物のサービスにする。

unit fileを `/etc/systemd/system/myapp.service` として書く。

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My FastAPI app
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
User=myapp
Group=myapp
WorkingDirectory=/srv/myapp
EnvironmentFile=/srv/myapp/.env
ExecStart=/srv/myapp/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

第6章の三段構成がそのまま生きている。第6章との違いを三点だけ押さえる。**`After=...postgresql.service`** は、データベースが立ち上がってからアプリを起こすため——アプリはDBに繋ぐので、順番が大事だ。**`EnvironmentFile=/srv/myapp/.env`** は、第二節の `.env` をsystemdが読み込んで環境変数にしてくれる仕組みで、これで `DATABASE_URL` がアプリに渡る。**`ExecStart`** が `.venv` の中のuvicornを名指ししている——システムのpythonではなく、第二節で作った仮想環境のものを使う。`User=myapp` で、第一節の専用ユーザーとして動かす。

書いたら、第6章で一本に繋いだ流れをそのまま通す。

```bash
# 1. unit file を書いたら、まず読み直させる
sudo systemctl daemon-reload

# 2. いま起動し、自動起動も有効にする
sudo systemctl enable --now myapp

# 3. 動いているか確認
systemctl status myapp

# 4. ログを追う
journalctl -u myapp -f
```

`status` が `active (running)` なら、もうサービスとして動いている。`curl http://127.0.0.1:8000/notes` がそのまま通るはずだ。もし `failed` なら、慌てずに `journalctl -u myapp` のエラーを読む——第6章でやったとおり、**エラーはそのままClaudeに貼る**のが基本動作だ。

### systemdの砂場——コンテナ無しの隔離

ここで、当然の疑問に答えておく。**「コンテナを使わないなら、隔離はどうするのか」。** 実は、コンテナの隔離とは、Linuxカーネルが持つ機能（名前空間、cgroups、権限の制限）の包装だ。そしてsystemdは、同じカーネル機能を unit file の数行で直接使える。`[Service]` に次を足す。

```ini
# [Service] に追記する——systemdの砂場（サンドボックス）
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/srv/myapp/data
```

意味は上から順に、「実行中に権限を昇格できない」「OS領域（`/usr` や `/etc`）を読み取り専用にする」「他ユーザーの家（`/home`）を見えなくする」「`/tmp` をこのサービス専用にする」「書き込みは `data/` だけ許す」。これでアプリが乗っ取られても、**書けるのは `/srv/myapp/data` と、journaldへ流れるログだけ**になる。第一節の所有権が一枚目の壁、この砂場が二枚目の壁だ。

全部を一度に暗記しなくていい。`systemd-analyze security myapp` と打つと、いまのサービスの「無防備さ」が項目ごとに採点される。その出力をClaudeに貼って、「この中で、私のアプリに今すぐ足すべき設定はどれですか。足すと壊れる可能性があるものはどれですか」と聞く——砂場の設計も、対話で詰めればいい。

コードを直したときの再反映も覚えておく。`app/main.py` を書き換えたら、サービスを再起動する。

```bash
sudo systemctl restart myapp
```

### Claudeに聞いてみよう③：起動失敗のエラーを診断させる

> 私のFastAPIアプリ myapp がサービスとして起動に失敗しています。`systemctl status myapp` は failed です。
> `journalctl -u myapp -p err -b --no-pager | tail -n 50` の出力はこれです：
> ```
> 〔エラー行をそのまま貼る〕
> ```
> unit file はこれです：
> ```
> 〔/etc/systemd/system/myapp.service の中身を貼る〕
> ```
> 原因の候補を可能性の高い順に挙げ、それぞれの確認手順を教えてください。.env の読み込み・venvのパス・データベース接続・ユーザー権限のどれが怪しいか、切り分けの順番も示してください。

第6章と同じく、**unit fileとエラーログを両方貼る**のがコツだ。FastAPIのアプリでよく詰まるのは、`.env` が読めていない（`DATABASE_URL` が無い）か、`.venv` のパスが違うか、DBのパスワードが合わないかの三つ。Claudeは設定と結果を突き合わせて、その切り分けを示してくれる。

## 第四節 Claudeと開発を回す

ここまでで、アプリ・データベース・サービスが繋がった。最後に、この先ずっと使う**開発のループ**を型として確認する。本編[第15章](/claude-debian/15-claude-development/)で身につけた作法の、サーバー版だ。

ループはこうだ。**仕様を言葉で伝える → Claudeがコードを書く → あなたがレビューして動かす → エラーをそのまま貼る → 直す。** この輪を回し続けるのが、2026年の開発だ。あなたが一行ずつ書くのではなく、何を作りたいかを正確に伝え、出てきたものを動かして守る。

この輪で最も効くのは、**要件の伝え方**だ。三つを揃えて渡すと、返ってくるコードの質が一段上がる。

- **何のデータを**扱うのか（例：メモの本文と作成日時）
- **誰が、どう読み書きするのか**（例：自分だけが、追加と一覧をする）
- **第7章のスキーマ**をそのまま貼る（`\d notes` の出力）

そして、**「動いたら終わり」ではない。** サービスが動いた後に、公開前のチェックを必ず一度通す。第9章で外に出す前の、最後の確認だ。

- 秘密は `.env` にあるか（コードやgitに漏れていないか）
- バインドは `127.0.0.1` か（`ss -tlnp | grep 8000` で確かめる）
- 専用ユーザー（`myapp`）で動いているか（`systemctl status myapp` の `User=` 行）

この三点は、第5章の守りと第一節の構成が、アプリの上で正しく効いているかの確認だ。ここが通っていれば、第9章でリバースプロキシの後ろに置く準備が整っている。

### Claudeに聞いてみよう④：公開前チェックリストを点検させる

> 私はDebian 13サーバーで、FastAPIアプリ myapp を /srv/myapp に置き、systemdのサービスとして動かしています。第9章で外に公開する前に、構成を点検したいです。
> 次の出力を渡します：
> ```
> 〔systemctl status myapp の出力〕
> ```
> ```
> 〔ss -tlnp | grep 8000 の出力〕
> ```
> ```
> 〔ls -l /srv/myapp の出力（.env の権限が分かるように）〕
> ```
> これらから、(1) 秘密がコード外の .env に隔離されているか、(2) アプリが 127.0.0.1 にだけバインドされているか、(3) 専用ユーザーで動いているか、を点検してください。公開前に直すべき点があれば、優先度つきで挙げてください。

公開という不可逆な一歩の前に、自分の構成をClaudeの目で一度点検させる。出力を貼るだけで、見落としていた穴が一つは見つかる。これが第9章への準備運動になる。

## まとめ

この章でやったこと：

1. コンテナを使わず「ふつうのディレクトリ + venv + systemd」でアプリを動かす方針と、その代わりにディレクトリ構成の規約が秩序を作ることを確認した
2. `/srv/myapp/` に app/・.venv/・.env・data/ を分け、専用ユーザー `myapp` を作り、「git管理・作り直せる・バックアップ」の対応表を引いた
3. PEP 668（externally managed）の理由を押さえ、`python3-venv` で仮想環境を作り、FastAPIとpsycopgを `.venv` に入れた
4. 最小のメモAPI `app/main.py` を読み、第7章の `myappdb` に繋いで `curl` で動作を確かめた（`/docs` の自動ドキュメントとSSHポート転送も）
5. 第6章の型で `myapp.service` を書き、daemon-reload → enable --now → status → journalctl を通してサービスにした
6. 仕様を伝えて書かせ、動かして直す開発ループと、公開前チェック（秘密・バインド・専用ユーザー）を型にした

手元に残ったもの：
- 専用ユーザーで動き、落ちても復活する自作のFastAPIサービス（`myapp.service`）
- git管理のコード・使い捨てのvenv・秘密の `.env` を分けたディレクトリ構成（`/srv/myapp/`）
- 第7章の `myappdb` に繋がって動く、最初の自作API
- 「見本を渡して作り替えさせる」「公開前に構成を点検させる」対話の型

自分のアプリが、自分のサーバーの上で、自分のデータベースを使って動いた。だがいまはまだ、`127.0.0.1` という自分のマシンの中だけの世界だ。外からは誰にも見えない——それは弱さではなく、いまは守りだ。次の[第9章「外の世界に公開する」](/claude-debian/server/09-publishing/)で、このアプリをCaddyというリバースプロキシの後ろに置き、TLSをまとって、いよいよ世界から見える場所に出す。公開という不可逆な一歩を、第5章の守りと、この章で通した公開前チェックを携えて踏み出す。

---

シリーズ全体は[Claudeと一緒に学ぶDebian サーバー編 一覧](/claude-debian/server/)から辿れる。本編（デスクトップ編）は[全章一覧](/claude-debian/)へ。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
