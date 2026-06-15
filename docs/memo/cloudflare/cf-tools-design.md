# Cloudflare 道具立て 設計メモ v0.1

ローカル中心で開発し、GitHub を使いたくない作り手（静的サイトジェネレータ＋毎日更新する個人）
のための、Cloudflare を土台にした小さな道具立ての設計メモ。
`tools/cloudflare_pages_deploy.py`（既存）を起点に、検討の結論を残す。

> このメモは「何を作る / 作らない / 保留するか」と、その判断理由を記録するもの。
> 実装はまだ着手していない。

---

## 0. 出発点と問い

- 既存: `tools/cloudflare_pages_deploy.py` — wrangler が内部で使う Pages の
  **Direct Upload API**（半公式）を、npm/wrangler 無しで Python 単体に再実装した CLI。
- 問い: これを「アプリ化」し、さらに PyPI パッケージとして配るべきか。
  アップロードだけでなくダウンロード・削除・バックアップ・共有もできるべきか。

検討を重ねた結論として、**用途ごとに対象サービスが違う**ことがはっきりした。
ひとつの万能アプリではなく、**役割で分けた 2 本立て＋共通の下層**に落ち着く。

---

## 1. 結論サマリ

| 道具 | 仕事 | 行き先 | 向き | 既存との関係 |
|---|---|---|---|---|
| `cf pages deploy` | ビルド**出力**を公開 | Pages | 一方向（deploy のみで十分） | 既存スクリプトをほぼ流用 |
| `cf snapshot push/pull/list/share` | 開発**ソース**の保全＋スナップショット共有 | R2 | 双方向 | rclone の隙間（固める＋1リンク共有）を埋める薄いもの |

その下に、UI を持たない再利用層を敷く。

```
┌ アプリ層（UI を持つ・消費者）
│   cf snapshot CLI   /   cf pages deploy CLI   /   〔将来・保留〕R2 ドライブ GUI(Flet)
├ API 層（UI 非依存・再利用可能）
│   R2Client:    put/get/list/stat/delete/copy/move/presign   （boto3 の薄いラッパ）
│   PagesClient: deploy/...                                    （既存 httpx ロジック）
└ Cloudflare（R2 / Pages）
```

**設計原則（最重要）**: API 層は純粋なライブラリにする。値を返す / 例外を投げるだけで、
`print` / `sys.exit` / `argparse` を入れない。これを守れば CLI でも Flet でも
ドライブアプリでもそのまま再利用できる（既存 `deploy()` が `sys.exit`/`print` を
持つ点は、GUI から呼ぶ前にここを直す必要がある）。

---

## 2. Pages 側 — deploy だけでよい

### 2.1 なぜ deploy のみか

- Pages は **publish-only（一方通行）**。サーバー側に個別編集できる状態は無く、
  毎回の deploy が**フォルダ全体のスナップショットを丸ごと差し替える**動作。
- 静的サイトジェネレータ運用では**正本はローカルのソース**で、いつでも再生成できる。
  Pages を原本扱いしないので、pull も削除系も本質的に要らない。
- 「ファイル削除」も専用機能は不要 — ローカルでファイルを消して再 deploy すれば、
  新しいスナップショットからそのファイルは消える（`collect()` がフォルダをミラーするため）。

### 2.2 「公開物＝手元フォルダ」だが "常に一致" には但し書き

一致するのは **最後に deploy した時点のフォルダ** との間。さらに以下の非対称がある。

- **隠しファイル（`.` 始まり）は上がらない** — `collect()` が `.git` 回避のため除外する
  （`cloudflare_pages_deploy.py` の dotfile スキップ）。副作用として `.well-known/` 等も
  公開されない。必要ならここに例外を入れる実装が要る。
- **25MiB 超のファイルは載らない**（Pages の 1 ファイル上限）。
- **HTTP で取り戻しても完全な逆写像にはならない** — 実体アセットのバイトは
  content-addressed なので GET すれば中身は一致するが、`_redirects` / `_headers` /
  `_routes.json` は Pages が設定として消費し**静的配信されない**ので取り戻せない。
  クリーン URL / index 解決で URL とファイル名も 1:1 でない。

→ **保証される向きは deploy（フォルダ→公開）だけ**。逆向き（公開→フォルダ）は近似復旧。

### 2.3 削除（保留・必要時のみ）

Pages の「削除」は 3 階層。今回の運用では deploy のみで足りるため未実装だが、記録として残す。

| 対象 | API | 注意 |
|---|---|---|
| 個別デプロイ | `DELETE …/deployments/{id}` | **アクティブな本番デプロイは削除不可**。先に別をロールバック/昇格が要る |
| プロジェクトごと | `DELETE …/projects/{name}` | 破壊的。**カスタムドメインの紐付け・設定・履歴が消え、再作成まで 404** |
| 公開サイトの個別ファイル | なし | デプロイは不変スナップショット。再 deploy で実現 |

「プロジェクトごと削除して作り直す」を掃除に使えるのは、**カスタムドメインが無く
ダウンタイムと履歴消失を許容できる** `*.pages.dev` のスクラッチ用途に限る。

### 2.4 SDK 状況

公式 `cloudflare` SDK は Pages の**プロジェクト/デプロイ管理**は持つが、wrangler 流の
**アセット blob 投入（check-missing → upload）は薄い**。よって **既存の手書き httpx
スクリプトを維持**するのが正解（どの SDK も埋めていない隙間）。

---

## 3. R2 側 — ソースの保全＋スナップショット共有

### 3.1 役割

deploy が「**出力**を公開」する仕事なのに対し、これは「**ソース（原本）**を保全・共有」する別の仕事。
GitHub を使わない人が失っている「原本の置き場」を埋める。対象がストレージなので **R2**（S3 互換）。

用途は **バックアップ＋読み取り共有（他人にスナップショットを渡す）** に確定。
双方向の共同編集は対象外（それは GitHub 以外の git や Syncthing の領域）。

### 3.2 設計の鍵 — スナップショット（1 アーカイブ）を基本単位にする

バックアップと共有を別々に作らず、**ソースを tar.gz 1 個に固めて R2 に置く**ことで両立する。

- **バックアップ** = アーカイブを時刻つきで貯める／戻すときは選んで展開
- **共有** = そのアーカイブの URL を 1 本渡すだけ（相手は 1 ファイルで丸ごと入手）

ソースはテキスト中心で MB 級なので、毎回まるごと固め直しても問題ない。
ファイル単位同期だと「フォルダを他人に渡す」のが URL バラバラで面倒になる点を、
アーカイブ化（1 リンク＝1 スナップショット）で回避できる。

```
cf snapshot push  <dir>  --bucket B            # .gitignore 尊重で tar.gz → アップロード（時刻つき）
cf snapshot list  --bucket B                   # スナップショット一覧
cf snapshot pull  <latest|時刻> <dest>         # 復元（ダウンロード＋展開）
cf snapshot share <latest|時刻> [--expire 7d]  # 署名付き URL を 1 本発行して渡す
cf snapshot prune --bucket B --keep N          # 古いスナップショットを掃除（R2 は本物の削除が正当）
```

- 除外は **`.gitignore` を流用**（`.git` / `node_modules` / ビルド成果物を自然に外す）。
- 圧縮は標準ライブラリ `tarfile`+gzip でゼロ追加依存。R2 アクセスは `boto3`。

### 3.3 制約

- **署名付き URL は最長 7 日**（SigV4 の上限）。恒久共有が要るなら
  **公開バケット＋カスタムドメイン**で恒久 URL に切り替える（設計分岐として明示）。
- **R2 の認証情報は Pages のトークンと別物**（ダッシュボード発行の S3 アクセスキー）。
  `~/.config/cloudflare/r2.env` に分けて保存。

---

## 4. R2Client（API 層）

「API を使えるようにしておく」= ゼロから S3 を実装するのではなく、
**boto3 の上の薄いラッパ**として、UI 非依存・ドライブ対応の粒度で API を切る。

```python
put(key, src, *, content_type=None, metadata=None)   # 大きいものは自動マルチパート
get(key) / download(key, dest) / open(key)           # ストリーム取得も
list(prefix="", *, delimiter=None)                   # delimiter="/" で“フォルダ”表示
stat(key) / exists(key)
delete(key) / delete_prefix(prefix)
copy(src, dst) / move(src, dst)                      # move = copy+delete
presign_get(key, expire) / presign_put(key, expire)
```

`R2Client` の存在意義は「S3 の再発明」ではなく、**R2 固有の癖を一度だけ吸収して
上のアプリ全部を楽にする**こと。具体的には:

- ⚠️ **新しめの boto3 が既定で付ける整合性チェックサム(CRC32)を R2 が受け付けず
  壊れる**事例がある。`request_checksum_calculation="when_required"` 等の設定で吸収する。
- ページング（continuation token）、マルチパート、エンドポイント
  （`https://<account_id>.r2.cloudflarestorage.com`）の面倒もここに閉じ込める。

バケット管理（作成・一覧・削除）など制御系が要れば、公式 `cloudflare` SDK を併用する。

---

## 5. 既存ツールとの関係（車輪の再発明を避ける）

各機能には成熟した既存解があり、自前で作る正当性は「隙間を埋める」か「統合・単純化」に限る。

| 領域 | 既存の定番 | 自前の立ち位置 |
|---|---|---|
| Pages へフォルダを公開 | wrangler（Node 必須）、ダッシュボード D&D、Git 連携 | **Node/wrangler を避けたい層**向けに Python 単体（隙間） |
| R2 へバックアップ/同期 | `rclone sync ./src r2:bucket`（ほぼ完璧） | 素の同期は rclone に任せる。自前は不要 |
| スナップショット＋1 リンク共有 | （rclone だと tar→upload→presign を自分で繋ぐ） | **ここが薄い自前ツールの唯一の価値**（100 行級） |
| R2 をドライブとしてマウント | rclone mount、Cyberduck / Mountain Duck、R2Drop(mac) | フル GUI は成熟ツールと競合 → **保留** |

---

## 6. スコープ判断

- **今やる候補**:
  - UI 非依存の `R2Client`（snapshot にどのみち要る・ドライブ対応粒度・R2 固有の癖を吸収）
  - `cf snapshot`（固める＋置く＋1 リンク共有＋`--keep` 掃除）
  - `cf pages deploy`（既存ロジックを取り込み。GUI 化に備え `sys.exit`→例外 /
    `print`→callback のリファクタを入れておくとライブラリとして使いやすい）
- **保留**:
  - R2 ドライブ GUI 本体（rclone mount / Cyberduck と競合。同期・衝突解決という
    重い部分の要否を別途決めてから）
  - Flet デスクトップ GUI（deploy だけなら CLI で足り、GUI の利得は薄い）
- **作らない**:
  - Pages の pull / 削除系（publish-only 運用では原本がローカルにあり不要）
  - 自前の S3 プロトコル実装・自前の同期エンジン（boto3 / rclone がある）

---

## 7. 実装ステップ（着手時）

1. パッケージ骨組み（`pyproject.toml` + `cf` サブコマンド、依存は boto3 / httpx）
2. `R2Client`（boto3 ラッパ。`stat`/`list`/`put`/`get` から。R2 固有設定を吸収）
3. `cf snapshot push`（`.gitignore` 除外 → tar.gz → upload、`--dry-run` 先行）
4. `cf snapshot pull` / `list`（復元・一覧）
5. `cf snapshot share`（署名 URL）/ `prune`（`--keep`）
6. `cf pages deploy` 移植（既存ロジック＋ UI 非依存化）
7. 配布（README / LICENSE → PyPI、Trusted Publishing。パッケージ名は空き確認）

---

## 8. 未決事項

- パッケージの置き場所: この `website` リポジトリ内のサブパッケージか、専用リポジトリか。
  当面 `tools/` 配下で育て、公開直前に判断。
- パッケージ名: `cf` は PyPI で空いていない可能性大。`cfsync` / `r2sync` 等を候補に空き確認。
  コマンド名 `cf` を維持できると使い勝手が良い。
- 恒久共有が要るか（署名 URL 7 日で足りるか、公開バケット＋カスタムドメインを用意するか）。
- A〜B の最終決定: 自分のサイト用に留めるなら既存スクリプトで足り、PyPI 化の利得は薄い。
  「Node を入れたくない人に配る」ことに意味を見出すなら PyPI 化に進む。

---

## 9. 4 スタック試作（trial）の結果

`apps/cf-publish/{rust,flet,flutter,pypi}/` に「フォルダ→Pages 公開」コアを 4 通りで試作し、
配布方法ごとの選定材料にした（いずれも既存 `tools/cloudflare_pages_deploy.py` 準拠）。
配布物は端末を前提にしない方が広く使えるため Flet / Flutter は GUI、Rust は単体バイナリ CLI、
PyPI は `pip install` で配る CLI とした。この環境に Cloudflare 認証情報は無いため、
**実デプロイの動作確認まではしていない**（ビルド/インストール/コンパイル/ロジック単体まで）。

| スタック | 形 | この環境での検証 | 位置づけ |
|---|---|---|---|
| **Rust**（`rust/`） | 単体バイナリ CLI | `cargo build` 成功・`cf-publish --help` 動作（独立に再ビルド確認） | ランタイム不要バイナリの核。GUI は別途 Tauri/egui が要る |
| **Flet**（`flet/`） | Python＋Flutter GUI | flet 0.85.3 導入・`py_compile`/import 通過 | Python ロジック流用で GUI が最速に作れる。`flet build` は Flutter SDK 要 |
| **Flutter**（`flutter/`） | Dart ネイティブ GUI | SDK 不在によりコンパイル不可。**レビュー済みソース雛形**。`blake3` パッケージは要確認 | UI 品質・モバイルの最終形候補。Cloudflare/S3 を Dart で再実装するコスト |
| **PyPI**（`pypi/`） | `pip install` 配布 CLI | `uv build`（wheel+sdist）→ クリーン venv へ install →`cf-publish --help`・import・認証無し時の親切エラー まで確認 | `pip install cf-publish` で配る版。ロジックは UI 非依存で GUI からも import 可 |

- 共通仕様: dotfile 除外・25MiB 上限・`blake3(base64(bytes)+ext)[:32]`・check-missing→batched upload→
  upsert-hashes→multipart deploy・`{success,errors,result}` 包絡。deploy ロジックは UI 非依存
  （例外を投げる／`sys.exit`・`process::exit` を持たない）に統一。
- **方針**: 本命スタックは固定しない。4 つとも残し、実際に使ってもらって選ぶ。
  目安として GUI 配布は Flet が最速、端末派には Rust 単体バイナリか PyPI、UI 本格化は Flutter。
- 既知の要対応: Flutter の `blake3` 依存の実在/API 確認、Flet/Flutter の実ビルド（Flutter SDK のある環境）、
  PyPI はパッケージ名の空き確認と実公開（Trusted Publishing）、4 スタックとも実 Cloudflare アカウントでの
  deploy 動作確認。
