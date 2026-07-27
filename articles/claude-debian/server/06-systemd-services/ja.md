---
slug: claude-debian-server-06-systemd-services
number: "06"
title: 第6章 サービスという単位
subtitle: systemdで動かし、journalctlで読む
description: サーバーの中身は結局「systemdが面倒を見るプロセスの集まり」だ。systemctlの基本動詞、journalctlでのログの読み方、自作スクリプトをサービスにするunit fileの書き方、systemd timerによる定期実行——「サービス」という一つの単位で、起動も停止もログも障害対応も扱えるようにする。
date: 2026.06.10
label: Claude × Debian サーバー編 06
prev_slug: claude-debian-server-05-security-basics
prev_title: 第5章 守りの基本
next_slug: claude-debian-server-07-database
next_title: 第7章 データベースという土台
cta_label: Claudeと学ぶ
cta_title: サーバーは「サービスの集まり」だ。
cta_text: 起動、停止、自動起動、ログ、障害対応——バラバラに見える操作は、すべて「サービス」という一つの単位に還元できる。この型を手にすれば、未知のソフトも同じ手つきで扱える。
cta_btn1_text: 第7章へ進む
cta_btn1_link: /claude-debian/server/07-database/
cta_btn2_text: 第5章に戻る
cta_btn2_link: /claude-debian/server/05-security-basics/
---

## なぜ「サービス」という単位を学ぶか

サーバーを触り始めると、覚えることが多すぎるように見える。SSHの起動、ファイアウォールの状態、Webサーバーの再起動、自作アプリの自動起動、ログの確認、障害時の対応——一つずつ別物の作法に思える。

だが、種明かしをすると、**サーバーの中身は結局「systemdが面倒を見るプロセスの集まり」**でしかない。SSHも、cronも、第5章で入れたfail2banも、これから動かすあなたのアプリも、すべて systemd から見れば同じ「サービス（service unit）」だ。

ここが本章の肝だ。**「サービス」という一つの単位で考えられるようになると、起動・停止・自動起動・ログ・障害対応が、全部同じ型で扱える。** 新しいソフトを入れても、「これもサービスだろう」と当たりをつけて、同じ動詞で操れる。覚えることが増えるのではなく、一つの型に集約される。この章はその型を体に入れる章だ。

## 第一節 systemctl の基本動詞

systemd を操る入口は `systemctl` コマンドだ。動詞はほんの数個で、それが全サービスに共通して効く。

```bash
# 状態を見る（最もよく使う）
systemctl status ssh

# 動かす / 止める
sudo systemctl start  ssh
sudo systemctl stop   ssh

# 再起動 / 設定だけ読み直す（接続を切らずに）
sudo systemctl restart ssh
sudo systemctl reload  ssh

# 自動起動を有効化 / 無効化（次回起動以降に効く）
sudo systemctl enable  ssh
sudo systemctl disable ssh

# いま動いているサービスの一覧
systemctl list-units --type=service
```

`start`/`stop` は「いまこの瞬間」を操る。`enable`/`disable` は「次回の起動でどうなるか」を操る。**この二つは別物**だ。第5章で打った `disable --now` は、両方を一度にやる省略形（`stop` + `disable`）だった。

`status` の出力は、慣れると数秒で全体像がつかめる。`ssh` を例に読んでみる。

```bash
systemctl status ssh
```

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-06-10 09:12:01 JST; 3h ago
   Main PID: 701 (sshd)
      Tasks: 1 (limit: 4915)
     Memory: 5.2M
        CPU: 120ms
     CGroup: /system.slice/ssh.service
             └─701 "sshd: /usr/sbin/sshd -D ..."

Jun 10 11:30:14 myserver sshd[1820]: Accepted publickey for user from 192.168.1.5
```

読みどころは四つ。**`Active: active (running)`** はいま動いていること。**`enabled`** は次回起動でも自動で立ち上がること。**`Main PID: 701`** はそのプロセス番号。そして末尾に、**直近のログが数行ぶら下がる**。status を見るだけで「動いてる・自動起動する・最近こうログを吐いた」が一目で分かる。

cron も同じ型で覗ける。

```bash
systemctl status cron
```

### Claudeに聞いてみよう①：`systemctl status` の出力を解説させる

> 私のDebian 13サーバーで `systemctl status 〔サービス名〕` を実行したら、次の出力でした：
> ```
> 〔status の出力をそのまま貼る〕
> ```
> 各行が何を意味するか説明してください。特に Active / Loaded（enabled か）/ Main PID / 末尾のログ行を一つずつ。
> この状態は健全ですか。気にすべき兆候があれば指摘してください。

status の出力は情報が詰まっているぶん、最初は圧倒される。**まるごと貼って一行ずつ解説させる。** 一度やれば、次から自分の目で同じ場所を見られるようになる。

## 第二節 ジャーナルを読む

systemd は全サービスのログを一箇所に集める。それを読むのが `journalctl` だ。サービスを名指しして、そのログだけを引き出せる。

```bash
# 特定サービスのログ全部
journalctl -u ssh

# いま流れるログを追いかける（Ctrl+C で抜ける）
journalctl -u ssh -f

# 直近10分ぶんだけ
journalctl -u ssh --since "10 min ago"

# 今回の起動以降の、エラー以上のレベルだけ
journalctl -p err -b
```

`-u` でサービスを絞り、`--since` で時間を絞り、`-p err -b` で重大度と起動回を絞る。長いログをいきなり全部読まず、**こうやって絞ってから読む・渡す**のがコツだ。

そして、これが本章で最も大事な一行だ。**ログをそのままClaudeに貼るのが、サーバー運用の基本動作になる。** これは本編[第8章のトラブルシュート](/claude-debian/08-first-troubleshooting/)で身につけた「ログをそのまま渡す」作法の、サーバー版の継承だ。デスクトップでは画面やWi-Fiのログだったものが、サーバーではサービスのジャーナルになる。やることは同じ——**読めない行を恐れず、絞って、貼る。**

ログが長すぎてClaudeに渡しにくいときは、絞ってから渡す。

```bash
# エラーだけを今回の起動分から抜き出して、コピーしやすくする
journalctl -u myapp -p err -b --no-pager | tail -n 50
```

`--no-pager` を付けると一気に出力されてコピーしやすい。`tail -n 50` で末尾だけに絞れる。

### Claudeに聞いてみよう②：自分のスクリプトをサービスにするunit fileを書かせる

> 私のDebian 13サーバーで、次の自作スクリプトを起動時に自動で動かしたいです：
> - 起動コマンド：〔例：/usr/bin/python3 /home/user/myapp/server.py〕
> - 実行ユーザー：〔例：一般ユーザー user。rootでは動かしたくない〕
> - 作業ディレクトリ：〔例：/home/user/myapp〕
> - 落ちたら自動で再起動してほしい
>
> systemd の unit file（/etc/systemd/system/myapp.service）を書いてください。
> そのうえで、[Unit][Service][Install] の各セクション・各行が何をしているか、一行ずつ説明してください。
> 反映から自動起動までの `systemctl` コマンドの手順も添えてください。

**unit file はClaudeに書かせて、自分はレビューする**——これがAI時代の流儀だ。ただし丸呑みはしない。**各行の意味を一度はClaudeに説明させて**、自分が読めるようにしておく。次節で、実際に手を動かして確かめる。

## 第三節 自分のサービスを書く

理屈は分かった。小さな実例で、自作のものを「サービス」に昇格させてみる。題材は何でもいい——手元のPythonスクリプトでも、お試しなら標準ライブラリだけで動く簡易Webサーバーでもいい。

```bash
# 題材：8000番ポートで簡易HTTPサーバーを動かすだけのもの
#   python3 -m http.server 8000
# これを「再起動しても、落ちても、自動で立ち上がるサービス」にする
```

unit file を `/etc/systemd/system/myapp.service` として作る。最小形は [Unit] [Service] [Install] の三段だ。

```bash
sudo tee /etc/systemd/system/myapp.service > /dev/null <<'EOF'
[Unit]
Description=My sample HTTP server
After=network.target

[Service]
# 一般ユーザーで動かす（rootで動かさない）
User=user
WorkingDirectory=/home/user/myapp
ExecStart=/usr/bin/python3 -m http.server 8000
# 異常終了したら自動で再起動
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
```

三段の意味はこうだ。**[Unit]** はこのサービスの説明と起動順（`After=network.target` でネットワークが立ち上がってから動かす）。**[Service]** は何を・誰として・どこで動かし、落ちたらどうするか（`Restart=on-failure`）。**[Install]** は `enable` したときに「いつ起動するか」——`multi-user.target` は「通常のサーバー稼働状態になったとき」を意味する。

書いたら、第一節の動詞で動かす。一連の流れはいつも同じだ。

```bash
# 1. unit file を書き換えたら、まず systemd に読み直させる
sudo systemctl daemon-reload

# 2. いま起動し、かつ自動起動も有効にする
sudo systemctl enable --now myapp

# 3. 動いているか確認
systemctl status myapp

# 4. ログを読む
journalctl -u myapp
```

`daemon-reload` を忘れると、書き換えが反映されない。ここは詰まりやすいので、**「unit file をいじったら daemon-reload」**と覚える。`enable --now` で立ち上げ、`status` で確認し、`journalctl -u myapp` でログを読む——第一節・第二節の動詞が、ここで一本に繋がる。

### Claudeに聞いてみよう③：journalctl のエラー行から次の一手を聞く

> 私のサービス myapp が起動に失敗しています。`systemctl status myapp` は failed と出ます。
> `journalctl -u myapp -p err -b --no-pager` の出力はこれです：
> ```
> 〔エラー行をそのまま貼る〕
> ```
> 私のunit fileはこれです：
> ```
> 〔/etc/systemd/system/myapp.service の中身を貼る〕
> ```
> 原因の候補を可能性の高い順に三つ挙げ、それぞれの確認手順を教えてください。
> ファイル権限・パス・ユーザー指定のどれが怪しいか、切り分けの順番も示してください。

unit file とエラーログを**両方**渡すのがコツだ。Claudeは「設定（unit file）」と「結果（ログ）」を突き合わせて、`ExecStart` のパスが間違っているのか、`User=` に権限がないのか、といった切り分けを示してくれる。これは第5章の点検対話と同じ作法だ。

## 第四節 定期実行——cron と systemd timer

「毎晩バックアップを取る」「毎時ログを集計する」といった定期実行は、伝統的には cron の仕事だった。cron はいまも健在で、`crontab -e` で簡潔に書ける。

ただし systemd には、サービスと同じ単位で扱える **timer** がある。利点は、実行結果が journalctl で読めること、`systemctl list-timers` で次回実行が一覧できること、そして「ネットワークが上がってから」のような依存を書けることだ。

timer は `.timer` と `.service` の**ペア**で作る。`.service` が「何をするか」、`.timer` が「いつ動かすか」だ。

```bash
# 何をするか：/etc/systemd/system/mybackup.service
sudo tee /etc/systemd/system/mybackup.service > /dev/null <<'EOF'
[Unit]
Description=Daily backup job

[Service]
Type=oneshot
ExecStart=/home/user/bin/backup.sh
EOF

# いつ動かすか：/etc/systemd/system/mybackup.timer
sudo tee /etc/systemd/system/mybackup.timer > /dev/null <<'EOF'
[Unit]
Description=Run mybackup daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

`OnCalendar=daily` は「毎日0時」を意味する。`Persistent=true` は、サーバーが止まっていて実行時刻を逃したら、次に起動したとき遅れて実行する。タイマー本体（`.timer`）を有効化すれば動き出す。

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mybackup.timer

# 登録されたタイマーと「次回いつ動くか」を一覧
systemctl list-timers
```

`list-timers` の `NEXT` 列に、次回実行の時刻が並ぶ。これが**第10章のバックアップ自動化への伏線**だ。バックアップという「定期的に・確実に・記録を残して」やりたい仕事は、まさにこの timer + service の型にはまる。

## まとめ

この章でやったこと：

1. `systemctl` の基本動詞（status/start/stop/restart/reload/enable/disable/list-units）を押さえた
2. `status` の出力（Active・enabled・Main PID・末尾ログ）を読めるようになった
3. `journalctl` でサービス・時間・重大度を絞ってログを読み、Claudeに渡す作法を確立した（本編第8章からの継承）
4. 自作スクリプトを `/etc/systemd/system/myapp.service` にし、daemon-reload → enable --now → status → journalctl の流れを通した
5. systemd timer（.timer + .service）で定期実行の最小形を作った

手元に残ったもの：
- 自動起動し、落ちても復活する自作サービス（myapp.service）
- 定期実行のひな型（.timer + .service のペア）
- 「設定（unit file）と結果（ログ）を両方Claudeに渡して切り分ける」対話の型
- 未知のソフトも「これもサービスだろう」と同じ動詞で扱える手つき

「サービス」という単位を手に入れた。だが、サービスが動くだけでは半分だ。サービスが読み書きする**データ**を、どこに・どんな形で置くか。次の[第7章「データベースという土台」](/claude-debian/server/07-database/)では、SQLiteとPostgreSQLの使い分けを整理し、PostgreSQLを実際にインストールして、データの置き場所という土台を作る。

---

シリーズ全体は[Claudeと一緒に学ぶDebian サーバー編 一覧](/claude-debian/server/)から辿れる。本編（デスクトップ編）は[全章一覧](/claude-debian/)へ。コメント・議論は Facebook グループへ：[AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
