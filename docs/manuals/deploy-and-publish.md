# サイトの公開手順（ビルド → 確認 → Cloudflare Pages デプロイ）

aiseed.dev を **Cloudflare Pages** に公開するための運用マニュアル。
ツールは `tools/build_article.py`（ビルド）と `tools/cloudflare_pages_deploy.py`
（アップロード）。**ビルドと本番デプロイは必ず分け、間に確認を挟む**。

> 原則：**確認した物と、本番に上げる物を一致させる。**
> ビルドした瞬間の `html/` を凍結し、それを目で確認し、同じ物をデプロイする。
> 自動再ビルドや「ビルド＋デプロイ一括」は使わない（裏で勝手に作り直されると、
> 確認した物とずれる。blog-026 で書いた「現行を正解器に確かめてから切り替える」
> と同じ思想）。

---

## 前提（一度だけ）

### 1. Python 仮想環境 `./.venv`

ビルドもデプロイも、リポジトリ直下の `./.venv/bin/python` で動かす（依存を一元化
し、デプロイスクリプトが裏で `tools/.venv` を勝手に作る動きも避ける）。

```bash
python3 -m venv .venv
./.venv/bin/pip install pillow markdown-it-py jinja2 httpx blake3
```

- ビルド系: `pillow` / `markdown-it-py` / `jinja2`
- デプロイ系: `httpx` / `blake3`

### 2. Cloudflare の認証情報

`CLOUDFLARE_API_TOKEN`（「Cloudflare Pages: 編集」権限）と
`CLOUDFLARE_ACCOUNT_ID` を、環境変数か `~/.config/cloudflare/pages.env`
（`KEY=VALUE` 形式）に置く。環境変数があればそちらが優先。

---

## 公開フロー（各ステップは独立。手で順に実行する）

### 1. ビルド

```bash
./.venv/bin/python tools/build_article.py --all
```

`articles/` から `html/` を生成する。

### 2. ローカルで確認（ビルド済み html をそのまま配信）

```bash
./.venv/bin/python -m http.server --directory html 8000
```

`http://localhost:8000/` を開いて目で確認。**再ビルドも監視もしない**ので、
ステップ1で作った物がそのまま見える。

### 3. プレビューURLへデプロイ（本番前の答え合わせ）

```bash
./.venv/bin/python tools/cloudflare_pages_deploy.py html --project aiseed-dev --branch preview
```

`--branch` が `main` 以外だと、本番ではなく**プレビューURL**が払い出される。
実プラットフォーム上での最終確認に使う。

### 4. 本番へデプロイ（確認後のみ）

```bash
./.venv/bin/python tools/cloudflare_pages_deploy.py html --project aiseed-dev --branch main
```

`--branch main` が本番。**3 で確認してからのみ**実行する。
初回でプロジェクトが無いときは `--create`（既定で作成。作らせたくなければ
`--no-create`）。

---

## Zed タスク（`.zed/tasks.json`）

Zed には Cloudflare Pages 専用のプラグインは無い。拡張で足せるのは言語・LSP・
MCP サーバー・テーマ等だけ。代わりに **Tasks** に上記コマンドを登録して、
コマンドパレット（`task: spawn`）から実行する。

> **注意**: このリポジトリは `.gitignore` で `.zed` を除外しているため、
> `.zed/tasks.json` はコミットされない（各自のローカルにのみ置く）。
> 内容をここに控えておく。`.zed/tasks.json` として保存すれば使える。

```json
[
  {
    "label": "1. Build site",
    "command": "./.venv/bin/python tools/build_article.py --all",
    "cwd": "$ZED_WORKTREE_ROOT"
  },
  {
    "label": "2. Preview (ビルド済み html を配信)",
    "command": "./.venv/bin/python -m http.server --directory html 8000",
    "cwd": "$ZED_WORKTREE_ROOT"
  },
  {
    "label": "3. Deploy to PREVIEW URL",
    "command": "./.venv/bin/python tools/cloudflare_pages_deploy.py html --project aiseed-dev --branch preview",
    "cwd": "$ZED_WORKTREE_ROOT"
  },
  {
    "label": "4. Deploy to PRODUCTION",
    "command": "./.venv/bin/python tools/cloudflare_pages_deploy.py html --project aiseed-dev --branch main",
    "cwd": "$ZED_WORKTREE_ROOT"
  }
]
```

- **「ビルド＋デプロイ一括」タスクは作らない**。本番デプロイは必ず人が選ぶ独立アクション。
- デプロイタスクは自前でビルドしない（古い `html/` を誤って上げないよう、ビルドは明示ステップに分離）。

---

## 補足

- **シンボリックリンク**: `tools/cloudflare_pages_deploy.py` は `os.walk(followlinks=True)`
  で収集するので、`html/` 配下のソフトリンク（ファイル・ディレクトリ両方）も
  対象になる。Cloudflare Pages はリンクの概念を持たないため、リンクは**実体のコピー**
  として配信される。壊れたリンクは除外、循環リンクは実体パスの既訪チェックで停止。
- **1ファイル上限 25MiB**（Pages の制限）。超えるとエラーで止まる。
- 隠しファイル・隠しディレクトリ（`.` 始まり）はアップロード対象外。
- このスクリプトは wrangler / npm 不要（Direct Upload API を直接叩く）。API 変更で
  動かなくなったら wrangler か Git 連携へ退避する。
